from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .forms import SignUpForm
from .models import User, TeacherRequest
from .tokens import registration_token
def home(request):
    """Vue pour la page d'accueil."""
    if request.user.is_authenticated:
        return redirect('users:profile')
    return render(request, 'index.html')
def signup(request):
    """Vue pour l'inscription des utilisateurs."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Désactiver jusqu'à l'activation par email
            user.save()
            # Envoyer l'email d'activation
            current_site = get_current_site(request)
            mail_subject = _("Activez votre compte After School")
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': registration_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, _("Veuillez vérifier votre email pour activer votre compte."))
            return redirect('users:login')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    """Vue pour activer le compte via le lien d'activation."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and registration_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, _("Votre compte a été activé avec succès !"))
        return redirect('users:profile')
    else:
        messages.error(request, _("Le lien d'activation est invalide ou a expiré."))
        return redirect('users:signup')

def login_view(request):
    """Vue pour la connexion des utilisateurs."""
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('users:profile')
            else:
                messages.error(request, _("Votre compte n'est pas activé. Vérifiez votre email."))
        else:
            messages.error(request, _("Email ou mot de passe incorrect."))
    return render(request, 'users/login.html')

def logout_view(request):
    """Vue pour la déconnexion des utilisateurs."""
    logout(request)
    messages.success(request, _("Vous avez été déconnecté avec succès."))
    return redirect('users:login')

@login_required
def profile(request):
    """Vue pour afficher et mettre à jour le profil utilisateur."""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def submit_teacher_request(request):
    """Vue pour soumettre une demande pour devenir enseignant."""
    if request.method == 'POST':
        qualifications = request.POST.get('qualifications')
        if not TeacherRequest.objects.filter(user=request.user, status='pending').exists():
            TeacherRequest.objects.create(user=request.user, qualifications=qualifications)
            messages.success(request, _("Votre demande a été soumise avec succès."))
        else:
            messages.error(request, _("Vous avez déjà une demande en attente."))
        return redirect('users:profile')
    return render(request, 'users/submit_teacher_request.html')

def is_admin(user):
    """Vérifie si l'utilisateur est un superutilisateur."""
    return user.is_superuser

@user_passes_test(is_admin)
def admin_teacher_requests(request):
    """Vue pour afficher les demandes d'enseignant (admin uniquement)."""
    requests = TeacherRequest.objects.all()
    return render(request, 'users/admin_teacher_requests.html', {'requests': requests})

@user_passes_test(is_admin)
def approve_teacher_request(request, request_id):
    """Vue pour approuver une demande d'enseignant (admin uniquement)."""
    try:
        teacher_request = TeacherRequest.objects.get(id=request_id)
        teacher_request.status = 'approved'
        teacher_request.reviewed_at = timezone.now()
        teacher_request.reviewed_by = request.user
        teacher_request.save()
        teacher_request.user.role = 'teacher'
        teacher_request.user.save()
        messages.success(request, _("Demande approuvée avec succès."))
    except TeacherRequest.DoesNotExist:
        messages.error(request, _("Demande introuvable."))
    return redirect('users:admin_teacher_requests')

@user_passes_test(is_admin)
def reject_teacher_request(request, request_id):
    """Vue pour rejeter une demande d'enseignant (admin uniquement)."""
    try:
        teacher_request = TeacherRequest.objects.get(id=request_id)
        teacher_request.status = 'rejected'
        teacher_request.reviewed_at = timezone.now()
        teacher_request.reviewed_by = request.user
        teacher_request.save()
        messages.success(request, _("Demande rejetée avec succès."))
    except TeacherRequest.DoesNotExist:
        messages.error(request, _("Demande introuvable."))
    return redirect('users:admin_teacher_requests')