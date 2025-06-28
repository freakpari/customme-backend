from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("ایمیل الزامی است.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10)
    education = models.CharField(max_length=20, blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    mobile = models.CharField(max_length=11)
    phone = models.CharField(max_length=15)
    province = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    postal_code = models.CharField(max_length=10)
    full_address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'national_code', 'birth_date']

    def __str__(self):
        return self.email



class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    purchase_score = models.PositiveIntegerField(default=0)
    total_designs = models.PositiveIntegerField(default=0)
    orders_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email

class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='کاربر'
    )
    name = models.CharField(max_length=255, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات", blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name="قیمت (تومان)")
    image = models.ImageField(upload_to='product_images/', verbose_name="عکس محصول")
    is_liked = models.BooleanField(default=False, verbose_name="لایک شده؟")

    def __str__(self):
        return self.name


class UserStats(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    current_orders = models.PositiveIntegerField(default=0, verbose_name="سفارش جاری")
    delivered_orders = models.PositiveIntegerField(default=0, verbose_name="ارسال شده")
    gallery_products = models.PositiveIntegerField(default=0, verbose_name="محصول در گالری")
    physical_products = models.PositiveIntegerField(default=0, verbose_name="محصول فیزیکی")
    canceled_orders = models.PositiveIntegerField(default=0, verbose_name="سفارش لغو شده")
    comments = models.PositiveIntegerField(default=0, verbose_name="تعداد نظر")

    def __str__(self):
        return f"آمار کاربر: {self.user.email}"
