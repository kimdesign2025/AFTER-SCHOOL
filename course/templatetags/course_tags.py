from django import template

from django import template
from course.models import TeacherApplication

register = template.Library()
register = template.Library()

@register.filter
def lookup(dictionary, key):
    return dictionary.get(key)


@register.filter
def has_pending_application(user):
    """Check if the user has a pending teacher application."""
    return TeacherApplication.objects.filter(user=user, status='pending').exists()

@register.filter
def has_approved_application(user):
    """Check if the user has an approved teacher application."""
    return TeacherApplication.objects.filter(user=user, status='approved').exists()