from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Teacher
from course.models import TeacherApplication

class TeacherListView(LoginRequiredMixin, ListView):
    model = Teacher
    template_name = 'users/student/teacher_list.html'
    context_object_name = 'teachers'

    def get_queryset(self):
        """Return only active and approved teachers."""
        return Teacher.objects.filter(is_active=True, is_approved=True).select_related('user')