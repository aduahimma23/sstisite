from django import forms
from .models import *


class InstructorprofileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = '__all__'

        widget = {

        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'status']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Course Title'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'row': 3, 'placeholder': 'Enter Course Description'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class CourseDetailsForm(forms.ModelForm):
    class Meta:
        model = CourseDetail
        fields = ['course_name', 'content_type', 'content', 'video_number']

        widgets = {
            
        }

class MarkAssessmentForm(forms.ModelForm):
    class Meta:
        model = MarkAssessment
        fields = ['student_submission', 'marks_obtained', 'feedback']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'

        widgets = {

        }


class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = CreateAssessment
        fields = '__all__'