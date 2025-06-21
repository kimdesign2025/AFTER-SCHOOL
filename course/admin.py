from django.contrib import admin
from .models import Course, Module, CourseReview, CourseEnrollment

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1
    fields = ['title', 'description', 'order', 'video', 'content']
    ordering = ['order']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_teacher_name', 'class_level', 'category', 'status', 'price', 'created_at']
    list_filter = ['status', 'category', 'class_level', 'is_public']
    search_fields = ['title', 'description', 'teacher__user__email', 'teacher__user__last_name']
    inlines = [ModuleInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'thumbnail', 'class_level', 'category')
        }),
        ('Content', {
            'fields': ('video', 'content', 'prerequisites')
        }),
        ('Details', {
            'fields': ('teacher', 'status', 'is_public', 'estimated_duration', 'price')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )
    list_editable = ['status', 'price']

    def get_teacher_name(self, obj):
        return obj.teacher.user.full_name
    get_teacher_name.short_description = 'Teacher'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('teacher__user')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'description', 'course__title']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'description', 'order')
        }),
        ('Content', {
            'fields': ('video', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course')

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'rating', 'created_at']
    list_filter = ['course', 'rating']
    search_fields = ['course__title', 'user__email', 'user__last_name', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('course', 'user', 'rating', 'comment')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'user')

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'created_at']
    list_filter = ['course']
    search_fields = ['course__title', 'user__email', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': ('course', 'user')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'id', 'ip_address', 'author', 'metadata')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('course', 'user')