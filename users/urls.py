from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),  # Nouvelle URL pour la page d'accueil
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('submit-teacher-request/', views.submit_teacher_request, name='submit_teacher_request'),
    path('admin/teacher-requests/', views.admin_teacher_requests, name='admin_teacher_requests'),
    path('admin/teacher-requests/<uuid:request_id>/approve/', views.approve_teacher_request, name='approve_teacher_request'),
    path('admin/teacher-requests/<uuid:request_id>/reject/', views.reject_teacher_request, name='reject_teacher_request'),
    path('logout/', views.logout_view, name='logout'),
    # path('course/', views.course, name='course'),
    path('admin-admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-teacher/', views.teacher_dashboard, name='admin_teacher'),

    path('student/dashboard/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/my-courses/', views.MyCoursesView.as_view(), name='my_courses'),
    path('student/progress/', views.ProgressView.as_view(), name='progress'),
    path('student/certificates/', views.CertificatesView.as_view(), name='certificates'),
    path('student/messages/', views.MessagesView.as_view(), name='messages'),
    path('student/settings/', views.SettingsView.as_view(), name='settings'),

    # path('admin/teacher/<uuid:user_id>/approve/', views.approve_teacher, name='approve_teacher'),
    # path('admin/teacher/<uuid:user_id>/reject/', views.reject_teacher, name='reject_teacher'),
]