from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from course.models import Course
from course.forms import CourseForm, ModuleFormSet

class CourseEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'users/teacher/edit_course.html'
    success_url = reverse_lazy('courses:teacher_courses')

    def test_func(self):
        """Restrict access to active teachers who own the course."""
        course = self.get_object()
        return (hasattr(self.request.user, 'teacher_profile') and 
                self.request.user.teacher_profile.is_active and 
                course.teacher == self.request.user.teacher_profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['module_formset'] = ModuleFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['module_formset'] = ModuleFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """Save the course and associated modules."""
        context = self.get_context_data()
        module_formset = context['module_formset']
        if module_formset.is_valid():
            self.object = form.save()
            module_formset.instance = self.object
            module_formset.save()
            messages.success(self.request, "Cours mis à jour avec succès !", extra_tags='toast-success')
            return super().form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.", extra_tags='toast-error')
        return super().form_invalid(form)