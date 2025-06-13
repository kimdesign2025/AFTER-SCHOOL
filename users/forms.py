from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User

class SignUpForm(UserCreationForm):
    """Formulaire pour l'inscription des utilisateurs."""
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text=_("Adresse email valide requise. Vous recevrez un lien d'activation."),
        label=_("Email")
    )
    first_name = forms.CharField(
        max_length=150,
        required=False,
        help_text=_("Facultatif."),
        label=_("Prénom")
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        help_text=_("Obligatoire."),
        label=_("Nom de famille")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cet email est déjà utilisé."))
        return email