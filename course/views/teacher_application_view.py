from django.views.generic import FormView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages
from ..models import TeacherApplication, Qualification, Course
from ..forms import QualificationForm, TeacherApplicationStep1Form, TeacherApplicationStep2Form, CourseForm, ModuleFormSet
from users.models import Teacher
import logging

logger = logging.getLogger(__name__)

class TeacherApplicationStep1View(LoginRequiredMixin, FormView):
    template_name = 'users/teacher/application/step1.html'
    form_class = TeacherApplicationStep1Form
    success_url = reverse_lazy('courses:teacher_application_step1_qualifications')

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'teacher_profile') and request.user.teacher_profile.is_approved:
            messages.info(request, "Votre compte enseignant est déjà approuvé.", extra_tags='toast-info')
            return redirect('courses:teacher_dashboard')
        if TeacherApplication.objects.filter(user=request.user, status='pending').exists():
            messages.warning(request, "Votre demande est en attente de validation. Veuillez patienter.", extra_tags='toast-warning')
            return redirect('users:student_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if TeacherApplication.objects.filter(user=self.request.user).exists():
            kwargs['instance'] = TeacherApplication.objects.get(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        logger.info(f"Form valid for user {self.request.user.email}")
        application = form.save(commit=False)
        application.user = self.request.user
        application.save()
        messages.success(self.request, "Étape 1 complétée : Expérience et expertise enregistrées.", extra_tags='toast-success')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(f"Form invalid for user {self.request.user.email}: {form.errors}")
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.", extra_tags='toast-error')
        return super().form_invalid(form)

class TeacherApplicationStep1QualificationsView(LoginRequiredMixin, FormView):
    template_name = 'users/teacher/application/step1_qualifications.html'
    form_class = QualificationForm
    success_url = reverse_lazy('courses:teacher_application_step2')

    def dispatch(self, request, *args, **kwargs):
        if not TeacherApplication.objects.filter(user=request.user).exists():
            messages.warning(request, "Veuillez d'abord compléter l'étape 1.", extra_tags='toast-warning')
            return redirect('courses:teacher_application_step1')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qualifications'] = Qualification.objects.filter(application__user=self.request.user)
        context['qualification_count'] = context['qualifications'].count()
        context['can_proceed'] = context['qualification_count'] >= 1
        context['previous_step_url'] = reverse_lazy('courses:teacher_application_step1')
        return context

    def form_valid(self, form):
        application = TeacherApplication.objects.get(user=self.request.user)
        qualification = form.save(commit=False)
        qualification.application = application
        qualification.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'qualification': {
                    'id': qualification.id,
                    'title': qualification.title,
                    'issuing_organization': qualification.issuing_organization,
                    'school': qualification.school,
                    'issue_date': qualification.issue_date.strftime('%Y-%m-%d'),
                    'certificate_file': qualification.certificate_file.url if qualification.certificate_file else None,
                },
                'qualification_count': Qualification.objects.filter(application=application).count(),
            })
        messages.success(self.request, "Étape 1 complétée : Qualification ajoutée avec succès.", extra_tags='toast-success')
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_json(),
            }, status=400)
        logger.error(f"Qualification form invalid for user {self.request.user.email}: {form.errors}")
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.", extra_tags='toast-error')
        return super().form_invalid(form)

class TeacherApplicationStep2View(LoginRequiredMixin, FormView):
    template_name = 'users/teacher/application/step2.html'
    form_class = TeacherApplicationStep2Form
    success_url = reverse_lazy('courses:teacher_application_confirm')

    def dispatch(self, request, *args, **kwargs):
        if not TeacherApplication.objects.filter(user=request.user).exists():
            messages.warning(request, "Veuillez d'abord compléter l'étape 1.", extra_tags='toast-warning')
            return redirect('courses:teacher_application_step1')
        application = TeacherApplication.objects.get(user=request.user)
        if application.qualifications.count() < 1:
            messages.error(request, "Vous devez ajouter au moins 1 qualification pour continuer.", extra_tags='toast-error')
            return redirect('courses:teacher_application_step1_qualifications')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = TeacherApplication.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['previous_step_url'] = reverse_lazy('courses:teacher_application_step1_qualifications')
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Étape 2 complétée : Informations personnelles enregistrées.", extra_tags='toast-success')
        return super().form_valid(form)

class TeacherApplicationConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'users/teacher/application/confirm.html'

    def dispatch(self, request, *args, **kwargs):
        if not TeacherApplication.objects.filter(user=request.user).exists():
            messages.warning(request, "Veuillez d'abord compléter l'étape 1.", extra_tags='toast-warning')
            return redirect('courses:teacher_application_step1')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = TeacherApplication.objects.get(user=self.request.user)
        context['previous_step_url'] = reverse_lazy('courses:teacher_application_step2')
        return context

    def post(self, request, *args, **kwargs):
        application = get_object_or_404(TeacherApplication, user=request.user)
        application.status = 'pending'
        application.save()
        messages.success(request, "Demande soumise avec succès. Vous recevrez une notification après validation.", extra_tags='toast-success')
        return redirect('users:student_dashboard')

class TeacherDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/teacher/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'teacher_profile') or not request.user.teacher_profile.is_approved:
            messages.error(request, "Votre compte enseignant n'est pas encore approuvé.", extra_tags='toast-error')
            return redirect('users:student_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = self.request.user.teacher_profile.courses.all()
        return context

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'users/teacher/create_course.html'  # Updated path
    success_url = reverse_lazy('courses:teacher_dashboard')

    def test_func(self):
        """Restrict access to active teachers only."""
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
            messages.success(self.request, "Cours créé avec succès !", extra_tags='toast-success')
            return super().form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.", extra_tags='toast-error')
        return super().form_invalid(form)