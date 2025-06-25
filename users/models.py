from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import uuid
from .managers import UserManager

# Choices pour le rôle de l'utilisateur
USER_ROLES = (
    ('learner', 'Apprenant'),
    ('admin', 'Administrateur'),
)

# Choices pour le statut de la demande d'enseignant
TEACHER_REQUEST_STATUS = (
    ('pending', 'En attente'),
    ('approved', 'Approuvé'),
    ('rejected', 'Rejeté'),
)

class BaseModel(models.Model):
    """Base class to add common fields to all models."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Date and time when the record was created.")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
        help_text=_("Date and time when the record was last updated.")
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted"),
        help_text=_("Indicates whether the record is marked as deleted.")
    )
    id = models.UUIDField(
        default=uuid.uuid4,
        null=False,
        blank=False,
        unique=True,
        primary_key=True,
        verbose_name=_("ID"),
        help_text=_("Unique identifier for the model instance.")
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_("IP address"),
        help_text=_("IP address of the user who created the record.")
    )
    author = models.EmailField(
        max_length=254,
        null=True,
        blank=True,
        verbose_name=_("Author"),
        help_text=_("Email of the user who created the record.")
    )
    metadata = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        verbose_name=_("Metadata"),
        help_text=_("Additional metadata stored as JSON.")
    )

    class Meta:
        abstract = True
        verbose_name = _("Base Model")
        verbose_name_plural = _("Base Models")

class User(AbstractUser, BaseModel):
    """Custom user model managing users: superuser, learner, and admin."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name=_("Email"),
        help_text=_("User's email address (unique)."),
        null=False,
        blank=False
    )
    phone = models.CharField(
        verbose_name=_("Phone number"),
        blank=True,
        null=True,
        max_length=30,
        help_text=_("User's phone number (optional).")
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=150,
        blank=True,
        null=True,
        help_text=_("User's first name.")
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=150,
        blank=False,
        null=False,
        help_text=_("User's last name.")
    )
    photo = models.ImageField(
        upload_to="profile_photos/",
        verbose_name=_("Profile photo"),
        null=True,
        blank=True,
        help_text=_("Profile photo of the user (optional).")
    )
    is_active = models.BooleanField(
        verbose_name=_("Active"),
        default=False,
        help_text=_("Designates whether this user should be treated as active.")
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='learner',
        verbose_name=_("Role"),
        help_text=_("User's role (learner or admin).")
    )
    username = None
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name}".strip()

class Profile(BaseModel):
    """User profile linked to User."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("User"),
        help_text=_("Associated user account.")
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Bio"),
        help_text=_("User's biography or description.")
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Address"),
        help_text=_("User's address (optional).")
    )

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"Profile of {self.user.full_name}"

class Teacher(BaseModel):
    """Model representing a teacher, linked to a User."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher",
        verbose_name=_("Instructor"),
        help_text=_("User associated with the teacher profile.")
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Bio"),
        help_text=_("Teacher's biography or description.")
    )
    subject_expertise = models.CharField(
        max_length=255,
        verbose_name=_("Subject Expertise"),
        help_text=_("Subjects the teacher is qualified to teach."),
        null=True,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="teacher_profiles/",
        verbose_name=_("Profile Image"),
        null=True,
        blank=True,
        help_text=_("Profile image of the teacher (optional).")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this teacher is active."
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approved",
        help_text=_("Designates whether this teacher has been approved by an admin.")
    )

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ["-created_at"]

    def clean(self):
        if self.user.role not in ['learner', 'admin']:
            raise ValidationError(_("Only users with learner or admin roles can be teachers."))

    def __str__(self):
        return f"Teacher: {self.user.full_name}"

class TwoFactorCode(BaseModel):
    """Model for two-factor authentication codes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User associated with the 2FA code.")
    )
    code = models.CharField(
        max_length=6,
        verbose_name=_("Code"),
        help_text=_("6-digit verification code.")
    )
    expiry = models.DateTimeField(
        verbose_name=_("Expiry"),
        help_text=_("Date and time when the code expires.")
    )

    def is_valid(self):
        """Check if the code is still valid (not expired)."""
        return timezone.now() <= self.expiry

    def save(self, *args, **kwargs):
        """Set default expiry to 10 minutes if not provided."""
        if not self.expiry:
            self.expiry = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Two Factor Code")
        verbose_name_plural = _("Two Factor Codes")

    def __str__(self):
        return f"2FA Code for {self.user.email} - {self.code}"