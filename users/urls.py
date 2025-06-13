from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),  # Nouvelle URL pour la page d'accueil
    path('signup/', views.signup, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('submit-teacher-request/', views.submit_teacher_request, name='submit_teacher_request'),
    path('admin/teacher-requests/', views.admin_teacher_requests, name='admin_teacher_requests'),
    path('admin/teacher-requests/<uuid:request_id>/approve/', views.approve_teacher_request, name='approve_teacher_request'),
    path('admin/teacher-requests/<uuid:request_id>/reject/', views.reject_teacher_request, name='reject_teacher_request'),
]