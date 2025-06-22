from django.shortcuts import redirect
from django.views.generic import ListView,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from course.models import Course
from django.contrib import messages

class TeacherCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Course
    template_name = 'users/teacher/courses.html'
    context_object_name = 'courses'

    def test_func(self):
        """Restrict access to active teachers only."""
        return hasattr(self.request.user, 'teacher_profile') and self.request.user.teacher_profile.is_active

    def get_queryset(self):
        """Return all courses created by the logged-in teacher."""
        return Course.objects.filter(teacher=self.request.user.teacher_profile)

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'teacher_profile') or not request.user.teacher_profile.is_approved:
            messages.error(request, "Votre compte enseignant n'est pas encore approuvé.", extra_tags='toast-error')
            return redirect('users:student_dashboard')
        return super().dispatch(request, *args, **kwargs)
    
class TeacherCourseDetail(TemplateView, LoginRequiredMixin):
    template_name = 'users/teacher/course_detail.html'