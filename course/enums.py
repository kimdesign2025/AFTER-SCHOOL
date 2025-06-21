from django.db import models
from django.utils.translation import gettext_lazy as _

class ClassLevel(models.TextChoices):
    CLASS_1 = 'class_1', _('Class 1')
    CLASS_2 = 'class_2', _('Class 2')
    CLASS_3 = 'class_3', _('Class 3')
    CLASS_4 = 'class_4', _('Class 4')
    CLASS_5 = 'class_5', _('Class 5')
    CLASS_6 = 'class_6', _('Class 6')
    CLASS_7 = 'class_7', _('Class 7')
    CLASS_8 = 'class_8', _('Class 8')
    CLASS_9 = 'class_9', _('Class 9')
    CLASS_10 = 'class_10', _('Class 10')
    CLASS_11 = 'class_11', _('Class 11')
    CLASS_12 = 'class_12', _('Class 12')

class CourseStatus(models.TextChoices):
    DRAFT = 'draft', _('Draft')
    PUBLISHED = 'published', _('Published')
    ARCHIVED = 'archived', _('Archived')

class CourseCategory(models.TextChoices):
    MATH = 'math', _('Mathematics')
    SCIENCE = 'science', _('Science')
    LITERATURE = 'literature', _('Literature')
    HISTORY = 'history', _('History')
    COMPUTER_SCIENCE = 'computer_science', _('Computer Science')
    LANGUAGES = 'languages', _('Languages')
    OTHER = 'other', _('Other')