from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, Teacher, TeacherRequest, TwoFactorCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'role', 'is_active')
        }),
        ('Contact', {
            'fields': ('phone', 'photo')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'bio', 'address')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'qualifications', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'qualifications', 'bio', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(TeacherRequest)
class TeacherRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'reviewed_at', 'reviewed_by']
    list_filter = ['status']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'qualifications']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'qualifications', 'status', 'reviewed_at', 'reviewed_by')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

@admin.register(TwoFactorCode)
class TwoFactorCodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'expiry', 'created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'code']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('user', 'code', 'expiry')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )