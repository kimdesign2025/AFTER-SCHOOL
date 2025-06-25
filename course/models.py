from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from users.models import Teacher, BaseModel
from .enums import ClassLevel, CourseStatus, CourseCategory, TeacherApplicationStatus

class Qualification(BaseModel):
    """Model representing a teacher's qualification or certificate."""
    application = models.ForeignKey(
        'TeacherApplication',
        on_delete=models.CASCADE,
        related_name='qualifications',
        verbose_name=_("Application"),
        help_text=_("Teacher application this qualification belongs to.")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title"),
        help_text=_("Title of the qualification or certificate.")
    )
    issuing_organization = models.CharField(
        max_length=200,
        verbose_name=_("Issuing Organization"),
        help_text=_("Organization that issued the qualification.")
    )
    issue_date = models.DateField(
        verbose_name=_("Issue Date"),
        help_text=_("Date the qualification was issued.")
    )
    certificate_file = models.FileField(
        upload_to='certificates/',
        verbose_name=_("Certificate File"),
        blank=True,
        null=True,
        help_text=_("Optional file upload for the certificate (PDF or image).")
    )
    school = models.CharField(
        max_length=200,
        verbose_name=_("School/Institution"),
        help_text=_("School or institution where the qualification was earned.")
    )

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")
        ordering = ["-issue_date"]

    def __str__(self):
        return f"{self.title} - {self.application.user.username}"

class TeacherApplication(BaseModel):
    """Model representing a user's application to become a teacher."""
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='teacher_applications',
        verbose_name=_("User"),
        help_text=_("User submitting the application.")
    )
    teaching_experience = models.TextField(
        verbose_name=_("Teaching Experience"),
        help_text=_("Details of teaching experience, including years and roles.")
    )
    subject_expertise = models.CharField(
        max_length=200,
        verbose_name=_("Subject Expertise"),
        help_text=_("Subjects the applicant is qualified to teach.")
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Bio"),
        help_text=_("Teacher's biography or description.")
    )
    identity_card = models.CharField(
        max_length=100,
        verbose_name=_("Identity Card Number"),
        help_text=_("National identity card number."),
        blank=True,
        null=True
    )
    identity_card_picture = models.ImageField(
        upload_to='identity_cards/',
        verbose_name=_("Identity Card Picture"),
        help_text=_("Upload a clear image of your identity card."),
        null=True,
        blank=True
    )
    profile_image = models.ImageField(
        upload_to="teacher_profiles/",
        verbose_name=_("Profile Image"),
        help_text=_("Profile image for the teacher profile (optional)."),
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        help_text=_("City of residence."),
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=20,
        verbose_name=_("Phone Number"),
        help_text=_("Contact phone number (optional)."),
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=TeacherApplicationStatus.choices,
        default=TeacherApplicationStatus.PENDING,
        verbose_name=_("Status"),
        help_text=_("Current status of the application.")
    )

    class Meta:
        verbose_name = _("Teacher Application")
        verbose_name_plural = _("Teacher Applications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.get_status_display()}"

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



class PrivateCourse(BaseModel):
    student = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="private_courses_as_student",
        verbose_name=_("Student"),
        help_text=_("Student booked for the private course.")
    )
    teacher = models.ForeignKey(
        'users.Teacher',
        on_delete=models.CASCADE,
        related_name="private_courses_as_teacher",
        verbose_name=_("Teacher"),
        help_text=_("Teacher conducting the private course.")
    )
    scheduled_time = models.DateTimeField(
        verbose_name=_("Scheduled Time"),
        help_text=_("Date and time when the private course is scheduled.")
    )
    meet_link = models.URLField(
        verbose_name=_("Google Meet Link"),
        help_text=_("Link to the Google Meet for the private course.")
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ),
        default='pending',
        verbose_name=_("Status"),
        help_text=_("Status of the private course.")
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50.00,  # Example price
        verbose_name=_("Price"),
        help_text=_("Price of the private course.")
    )

    class Meta:
        verbose_name = _("Private Course")
        verbose_name_plural = _("Private Courses")
        ordering = ["-scheduled_time"]

    def __str__(self):
        return f"Private Course: {self.student.full_name} with {self.teacher.user.full_name}"

class PaymentSimulation(BaseModel):
    private_course = models.OneToOneField(
        PrivateCourse,
        on_delete=models.CASCADE,
        related_name="payment",
        verbose_name=_("Private Course"),
        help_text=_("Private course associated with the payment.")
    )
    method = models.CharField(
        max_length=20,
        choices=(
            ('mtn', 'MTN Mobile Money'),
            ('orange', 'Orange Money'),
        ),
        verbose_name=_("Payment Method"),
        help_text=_("Simulated payment method used.")
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Amount"),
        help_text=_("Amount paid for the private course.")
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('failed', 'Failed'),
        ),
        default='pending',
        verbose_name=_("Status"),
        help_text=_("Status of the simulated payment.")
    )

    class Meta:
        verbose_name = _("Payment Simulation")
        verbose_name_plural = _("Payment Simulations")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment for {self.private_course} via {self.get_method_display()}"