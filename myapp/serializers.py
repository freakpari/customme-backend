from rest_framework import serializers
from .models import CustomUser, UserProfile,Product
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

class SideProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'purchase_score', 'total_designs', 'orders_count']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'