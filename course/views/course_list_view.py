from django.views.generic import ListView
from course.models import Course
from course.enums import CourseStatus

class CourseListView(ListView):
    model = Course
    template_name = 'users/student/course/course_list.html'
    context_object_name = 'courses'
    queryset = Course.objects.filter(status=CourseStatus.PUBLISHED)