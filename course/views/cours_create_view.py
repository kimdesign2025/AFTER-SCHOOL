from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from course.models import Course, Module
from course.forms import CourseForm, ModuleFormSet
from django.forms import inlineformset_factory

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course/create_course.html'
    success_url = reverse_lazy('course_list')

    def test_func(self):
        """Restrict access to teachers only."""
        return hasattr(self.request.user, 'teacher_profile') and self.request.user.teacher_profile.is_active

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['module_formset'] = ModuleFormSet(self.request.POST, self.request.FILES)
        else:
            context['module_formset'] = ModuleFormSet()
        return context

    def form_valid(self, form):
        """Set the teacher to the logged-in user's teacher profile and price to 0."""
        form.instance.teacher = self.request.user.teacher_profile
        form.instance.price = 0.00
        context = self.get_context_data()
        module_formset = context['module_formset']
        if module_formset.is_valid():
            self.object = form.save()
            module_formset.instance = self.object
            module_formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)