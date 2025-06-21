from django.urls import path
from .views.cours_create_view import CourseCreateView
from .views.course_list_view import CourseListView
from .views.course_detail_view import CourseDetailView, CourseEnrollView, DownloadCertificateView
from .views.module_detail_view import ModuleDetailView

app_name="courses"

urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('', CourseListView.as_view(), name='course_list'),
    path('course/<uuid:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<uuid:pk>/enroll/', CourseEnrollView.as_view(), name='course_enroll'),
    path('course/<uuid:pk>/certificate/', DownloadCertificateView.as_view(), name='download_certificate'),
    path('module/<uuid:pk>/', ModuleDetailView.as_view(), name='module_detail'),
]