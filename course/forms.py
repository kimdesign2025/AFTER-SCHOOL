from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
from .models import Course, Module
from .enums import ClassLevel, CourseCategory
from django import forms
from .models import Qualification, TeacherApplication
from .enums import CourseCategory
from django.forms import modelformset_factory

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'thumbnail', 'class_level',
            'video', 'content', 'prerequisites', 'category',
            'is_public', 'estimated_duration'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'content': forms.Textarea(attrs={'rows': 10}),
            'prerequisites': forms.Textarea(attrs={'rows': 3}),
            'class_level': forms.Select(),
            'category': forms.Select(),
            'is_public': forms.CheckboxInput(),
            'estimated_duration': forms.NumberInput(attrs={'min': 1}),
        }
        labels = {
            'title': _('Course Title'),
            'description': _('Description'),
            'thumbnail': _('Thumbnail Image'),
            'class_level': _('Class Level'),
            'video': _('Course Video'),
            'content': _('Course Content'),
            'prerequisites': _('Prerequisites'),
            'category': _('Category'),
            'is_public': _('Public Course'),
            'estimated_duration': _('Estimated Duration (hours)'),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'video', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'order': forms.HiddenInput(attrs={'value': 1}),
        }
        labels = {
            'title': _('Module Title'),
            'description': _('Module Description'),
            'video': _('Module Video'),
        }

ModuleFormSet = inlineformset_factory(
    Course, Module, form=ModuleForm, extra=1, can_delete=False
)

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['title', 'issuing_organization', 'school', 'issue_date', 'certificate_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'issuing_organization': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificate_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TeacherApplicationStep1Form(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        fields = ['teaching_experience', 'subject_expertise']
        widgets = {
            'teaching_experience': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'subject_expertise': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TeacherApplicationStep2Form(forms.ModelForm):
    class Meta:
        model = TeacherApplication
        fields = ['identity_card', 'identity_card_picture', 'city', 'phone_number']
        widgets = {
            'identity_card': forms.TextInput(attrs={'class': 'form-control'}),
            'identity_card_picture': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }