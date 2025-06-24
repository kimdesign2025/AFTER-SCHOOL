from django.urls import path

from course.views.urse_edit_view import CourseEditView

from .views.course_list_view import CourseListView
from .views.teacher_course_list_view import TeacherCourseListView
from .views.course_detail_view import (
    CourseDetailView,
    CourseEnrollView,
    DownloadCertificateView,
)

from .views.module_detail_view import ModuleDetailView
from .views.teacher_application_view import (
    CourseCreateView,
    TeacherApplicationStep1View,
    TeacherApplicationStep1QualificationsView,
    TeacherApplicationStep2View,
    TeacherApplicationConfirmView,
    TeacherDashboardView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="course_list"),
    path("create-course/", CourseCreateView.as_view(), name="create_course"),
    path("course/<uuid:pk>/", CourseDetailView.as_view(), name="course_detail"),
    path("course/<uuid:pk>/edit/", CourseEditView.as_view(), name="course_edit"),
    path("course/<uuid:pk>/enroll/", CourseEnrollView.as_view(), name="course_enroll"),
    path(
        "course/<uuid:pk>/certificate/",
        DownloadCertificateView.as_view(),
        name="download_certificate",
    ),
    path("module/<uuid:pk>/", ModuleDetailView.as_view(), name="module_detail"),
    path(
        "teacher-application/step1/",
        TeacherApplicationStep1View.as_view(),
        name="teacher_application_step1",
    ),
    path(
        "teacher-application/step1/qualifications/",
        TeacherApplicationStep1QualificationsView.as_view(),
        name="teacher_application_step1_qualifications",
    ),
    path(
        "teacher-application/step2/",
        TeacherApplicationStep2View.as_view(),
        name="teacher_application_step2",
    ),
    path(
        "teacher-application/confirm/",
        TeacherApplicationConfirmView.as_view(),
        name="teacher_application_confirm",
    ),
    path(
        "teacher-dashboard/", TeacherDashboardView.as_view(), name="teacher_dashboard"
    ),
    path("teacher-courses/", TeacherCourseListView.as_view(), name="teacher_courses"),
    path(
        "teacher-course/<uuid:pk>/",
        TeacherCourseListView.as_view(),
        name="teacher_course_detail",
    ),
]
