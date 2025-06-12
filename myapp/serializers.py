from rest_framework import serializers
from .models import CustomUser

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
