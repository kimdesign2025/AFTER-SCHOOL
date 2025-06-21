from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from users.models import Teacher, BaseModel
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
        Teacher,
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
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Price"),
        help_text=_("Price of the course (0.00 for free)."),
        validators=[MinValueValidator(0.00)]
    )

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ["-created_at"]

    def clean(self):
        """Validation: Ensure teacher is active."""
        if not self.teacher.is_active:
            raise ValidationError(_("Only active teachers can create courses."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_class_level_display()}) by {self.teacher.user.full_name}"

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

class ModuleCompletion(BaseModel):
    """Model to track module completion by users."""
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="module_completions",
        verbose_name=_("User"),
        help_text=_("User who completed the module.")
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="completions",
        verbose_name=_("Module"),
        help_text=_("Module that was completed.")
    )

    class Meta:
        verbose_name = _("Module Completion")
        verbose_name_plural = _("Module Completions")
        unique_together = ('user', 'module')
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.full_name} completed {self.module.title}"

class CourseReview(BaseModel):
    """Model for user reviews of a course."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name=_("Course"),
        help_text=_("Course being reviewed.")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="course_reviews",
        verbose_name=_("User"),
        help_text=_("User who submitted the review.")
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rating"),
        help_text=_("Rating from 1 to 5.")
    )
    comment = models.TextField(
        verbose_name=_("Comment"),
        help_text=_("Review comment.")
    )

    class Meta:
        verbose_name = _("Course Review")
        verbose_name_plural = _("Course Reviews")
        unique_together = ('course', 'user')
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review of {self.course.title} by {self.user.full_name} ({self.rating}/5)"

class CourseEnrollment(BaseModel):
    """Model to track users enrolled in a course."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("Course"),
        help_text=_("Course the user is enrolled in.")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("User"),
        help_text=_("User enrolled in the course.")
    )

    class Meta:
        verbose_name = _("Course Enrollment")
        verbose_name_plural = _("Course Enrollments")
        unique_together = ('course', 'user')
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.full_name} enrolled in {self.course.title}"

    @property
    def progress(self):
        """Calculate progress as percentage of completed modules."""
        total_modules = self.course.modules.count()
        if total_modules == 0:
            return 0
        completed_modules = ModuleCompletion.objects.filter(
            user=self.user, module__course=self.course
        ).count()
        return (completed_modules / total_modules) * 100

    @property
    def is_completed(self):
        """Check if all modules are completed."""
        total_modules = self.course.modules.count()
        if total_modules == 0:
            return False
        completed_modules = ModuleCompletion.objects.filter(
            user=self.user, module__course=self.course
        ).count()
        return completed_modules == total_modules