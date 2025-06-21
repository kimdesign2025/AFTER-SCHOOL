from django.views.generic import DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from course.models import Course, CourseEnrollment, ModuleCompletion
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import io

class CourseDetailView(DetailView):
    model = Course
    template_name = 'users/student/course/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_courses'] = Course.objects.filter(
            is_public=True, status='published'
        ).exclude(id=self.object.id)[:3]
        if self.request.user.is_authenticated:
            context['is_enrolled'] = CourseEnrollment.objects.filter(
                user=self.request.user, course=self.object
            ).exists()
            if context['is_enrolled']:
                context['can_download_certificate'] = CourseEnrollment.objects.get(
                    user=self.request.user, course=self.object
                ).is_completed
            # Add module completion status
            context['module_completions'] = {
                module.id: ModuleCompletion.objects.filter(
                    user=self.request.user, module=module
                ).exists() for module in self.object.modules.all()
            }
        return context

class CourseEnrollView(LoginRequiredMixin, View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        CourseEnrollment.objects.get_or_create(user=request.user, course=course)
        return redirect('courses:course_detail', pk=pk)

class DownloadCertificateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
        if not enrollment.is_completed:
            return redirect('courses:course_detail', pk=pk)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Certificat d'achèvement", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Ce certificat est décerné à {request.user.full_name}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"pour avoir complété avec succès le cours", styles['Normal']))
        story.append(Paragraph(f"{course.title}", styles['Heading2']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Date d'achèvement: {enrollment.updated_at.strftime('%d %B %Y')}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Enseignant: {course.teacher.user.full_name}", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="certificate_{course.title}.pdf"'
        response.write(buffer.read())
        return response