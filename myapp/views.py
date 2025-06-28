from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import  CustomUserSerializer,SideProfileSerializer




class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'ثبت‌نام با موفقیت انجام شد.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        serializer = RegisterSerializer(user, data=request.data, partial=True)  # partial=True یعنی لازم نیست همه فیلدها رو بفرسته
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'اطلاعات با موفقیت ویرایش شد.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'ایمیل و کلمه عبور الزامی هستند.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'ایمیل یا کلمه عبور اشتباه است.'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'email': user.email}, status=status.HTTP_200_OK)


class AccountInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        data = request.data.copy()

        # اعتبارسنجی کلمه عبور تکراری (در بک‌اند هم برای امنیت)
        password = data.get('password')
        confirm = request.data.get('confirmPassword')  # از فرانت می‌فرسته

        if password and confirm and password != confirm:
            return Response({'error': 'رمزها مطابقت ندارند.'}, status=400)

        serializer = CustomUserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            if password:
                user.set_password(password)  # هش رمز
                user.save()

            return Response({'message': 'اطلاعات با موفقیت ویرایش شد'}, status=200)
        return Response(serializer.errors, status=400)

class SideProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = SideProfileSerializer(profile)
        return Response(serializer.data)