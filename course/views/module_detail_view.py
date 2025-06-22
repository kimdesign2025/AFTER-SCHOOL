from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from course.models import Module, ModuleCompletion
from django.shortcuts import redirect

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = 'users/student/course/module_detail.html'
    context_object_name = 'module'

    def post(self, request, *args, **kwargs):
        module = self.get_object()
        ModuleCompletion.objects.get_or_create(user=request.user, module=module)
        return redirect('courses:module_detail', pk=module.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_completed'] = ModuleCompletion.objects.filter(
            user=self.request.user, module=self.object
        ).exists()
        return context