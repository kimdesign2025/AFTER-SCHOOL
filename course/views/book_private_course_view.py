from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from users.models import Teacher
from course.models import PrivateCourse, PaymentSimulation
from django import forms
from django.utils import timezone
from datetime import timedelta
import uuid
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(
        choices=(('mtn', 'MTN Mobile Money'), ('orange', 'Orange Money')),
        widget=forms.RadioSelect,
        label="Méthode de paiement"
    )
    phone_number = forms.CharField(
        max_length=20,
        label="Numéro de téléphone",
        help_text="Entrez votre numéro pour le paiement."
    )

class BookPrivateCourseView(LoginRequiredMixin, FormView):
    template_name = 'users/student/payment_form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('users:student_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = Teacher.objects.get(id=self.kwargs['teacher_id'])
        context['price'] = 50.00
        return context

    def form_valid(self, form):
        teacher = Teacher.objects.get(id=self.kwargs['teacher_id'])
        student = self.request.user
        scheduled_time = timezone.now() + timedelta(hours=24)
        meet_link = f"https://meet.google.com/{str(uuid.uuid4())[:12].replace('-', '')}"

        # Create PrivateCourse
        private_course = PrivateCourse.objects.create(
            student=student,
            teacher=teacher,
            scheduled_time=scheduled_time,
            meet_link=meet_link,
            price=50.00,
            status='confirmed'
        )

        # Create PaymentSimulation
        PaymentSimulation.objects.create(
            private_course=private_course,
            method=form.cleaned_data['payment_method'],
            amount=50.00,
            status='completed'
        )

        # Send emails
        subject = "Confirmation de votre cours privé"
        message = (
            f"Bonjour {student.full_name},\n\n"
            f"Votre cours privé avec {teacher.user.full_name} est confirmé.\n"
            f"Date et heure : {scheduled_time.strftime('%d/%m/%Y %H:%M')}\n"
            f"Lien Google Meet : {meet_link}\n\n"
            f"Merci de votre confiance !\nÉquipe After School"
        )
        teacher_message = (
            f"Bonjour {teacher.user.full_name},\n\n"
            f"Un cours privé a été réservé avec {student.full_name}.\n"
            f"Date et heure : {scheduled_time.strftime('%d/%m/%Y %H:%M')}\n"
            f"Lien Google Meet : {meet_link}\n\n"
            f"Merci de votre disponibilité !\nÉquipe After School"
        )
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [student.email],
                fail_silently=False
            )
            send_mail(
                subject,
                teacher_message,
                settings.DEFAULT_FROM_EMAIL,
                [teacher.user.email],
                fail_silently=False
            )
            logger.info(f"Emails sent to {student.email} and {teacher.user.email} for private course {private_course.id}")
        except Exception as e:
            logger.error(f"Failed to send emails for private course {private_course.id}: {str(e)}")
            messages.warning(self.request, "Cours réservé, mais l'envoi des emails a échoué. Contactez le support.", extra_tags='toast-warning')

        messages.success(self.request, "Cours privé réservé avec succès ! Un lien Google Meet a été envoyé par email.", extra_tags='toast-success')
        return super().form_valid(form)