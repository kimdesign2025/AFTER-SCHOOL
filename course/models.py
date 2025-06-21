from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import uuid
from users.models import User, BaseModel  # Assuming the User model is in the 'users' app
from .enums import ClassLevel, CourseStatus, CourseCategory

class Course(BaseModel):
    """Model representing a course created by a teacher."""
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Title of the course.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed description of the course.")
    )
    thumbnail = models.ImageField(
        upload_to="course_thumbnails/",
        verbose_name=_("Thumbnail"),
        null=True,
        blank=True,
        help_text=_("Thumbnail image for the course (optional).")
    )
    class_level = models.CharField(
        max_length=20,
        choices=ClassLevel.choices,
        verbose_name=_("Class Level"),
        help_text=_("Target class level for the course.")
    )
    video = models.FileField(
        upload_to="course_videos/",
        verbose_name=_("Course Video"),
        null=True,
        blank=True,
        help_text=_("Main video content for the course (optional).")
    )
    content = models.TextField(
        verbose_name=_("Course Content"),
        help_text=_("Detailed content or syllabus of the course.")
    )
    prerequisites = models.TextField(
        verbose_name=_("Prerequisites"),
        null=True,
        blank=True,
        help_text=_("Prerequisites for taking the course (optional).")
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name=_("Teacher"),
        help_text=_("Teacher who created the course.")
    )
    status = models.CharField(
        max_length=20,
        choices=CourseStatus.choices,
        default=CourseStatus.DRAFT,
        verbose_name=_("Status"),
        help_text=_("Current status of the course.")
    )
    category = models.CharField(
        max_length=50,
        choices=CourseCategory.choices,
        default=CourseCategory.OTHER,
        verbose_name=_("Category"),
        help_text=_("Category of the course.")
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name=_("Is Public"),
        help_text=_("Indicates whether the course is accessible to all users.")
    )
    estimated_duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Duration (hours)"),
        help_text=_("Estimated duration of the course in hours (optional).")
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["-created_at"]

    def clean(self):
        """Validation: Ensure only teachers can create courses."""
        if self.teacher.role != 'teacher':
            raise ValidationError(_("Only teachers can create courses."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_class_level_display()}) by {self.teacher.full_name}"

class Module(BaseModel):
    """Model representing a module within a course."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name=_("Course"),
        help_text=_("Course to which this module belongs.")
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
        help_text=_("Title of the module.")
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Description of the module content.")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Order"),
        help_text=_("Order of the module within the course.")
    )
    video = models.FileField(
        upload_to="module_videos/",
        verbose_name=_("Module Video"),
        null=True,
        blank=True,
        help_text=_("Video content for the module (optional).")
    )
    content = models.TextField(
        verbose_name=_("Module Content"),
        help_text=_("Detailed content of the module.")
    )

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.title} (Module {self.order} of {self.course.title})"