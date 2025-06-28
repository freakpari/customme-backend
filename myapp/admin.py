from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,UserProfile,Product,UserStats

from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'city')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('full_name', 'national_code', 'birth_date', 'education', 'job')}),
        ('اطلاعات تماس', {'fields': ('mobile', 'phone', 'province', 'city', 'postal_code', 'full_address')}),
        ('دسترسی‌ها', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'national_code', 'birth_date', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'purchase_score', 'orders_count', 'total_designs')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_liked', 'user', 'image_tag')  # اضافه کردن image_tag
    readonly_fields = ('image_tag',)
    list_filter = ('is_liked', 'user')
    search_fields = ('name',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:8px;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'پیش‌نمایش تصویر'


@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "current_orders", "delivered_orders", "gallery_products")
    search_fields = ("user__email",)