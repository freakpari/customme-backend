from rest_framework import serializers
from .models import CustomUser, UserProfile, Product
from django.contrib.auth import get_user_model



EDUCATION_CHOICES = ['دیپلم', 'کارشناسی', 'کارشناسی ارشد', 'دکترا']
JOB_CHOICES = ['برنامه نویس', 'طراح', 'مدیر', 'سایر']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'full_name', 'national_code', 'education', 'job', 'email', 'password', 'birth_date',
            'mobile', 'phone', 'province', 'city', 'postal_code', 'full_address'
        ]

    def validate_education(self, value):
        if value and value not in EDUCATION_CHOICES:
            raise serializers.ValidationError("مقدار تحصیلات معتبر نیست.")
        return value

    def validate_job(self, value):
        if value and value not in JOB_CHOICES:
            raise serializers.ValidationError("شغل وارد شده معتبر نیست.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user

    User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = [
                "full_name", "national_code", "education", "job",
                "birth_date", "email", "mobile", "phone",
                "province", "city", "postal_code", "full_address"
            ]


class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ['title', 'image', 'price', 'type']

class UserProfileSerializer(serializers.ModelSerializer):
        user_full_name = serializers.CharField(source='user.full_name')
        email = serializers.EmailField(source='user.email')

        favorites = serializers.SerializerMethodField()
        repeated = serializers.SerializerMethodField()
        gallery = serializers.SerializerMethodField()

        class Meta:
            model = UserProfile
            fields = [
                'user_full_name',
                'email',
                'profile_image',
                'purchase_score',
                'orders_count',
                'profile_completion',
                'favorites',
                'repeated',
                'gallery',
            ]

        def get_favorites(self, obj):
            products = Product.objects.filter(user=obj.user, type='favorite')
            return ProductSerializer(products, many=True).data

        def get_repeated(self, obj):
            products = Product.objects.filter(user=obj.user, type='repeated')
            return ProductSerializer(products, many=True).data

        def get_gallery(self, obj):
            products = Product.objects.filter(user=obj.user, type='gallery')
            return ProductSerializer(products, many=True).data

class SideProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'purchase_score', 'total_designs', 'orders_count']