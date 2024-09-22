from django import forms
from .models import *


class InstructorprofileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = [
            'phone_number', 'profile_picture', 'qualications', 'experience_years',
            'specialties', 'social_media_link', 'location'
        ]

        widget = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.ImageField(),
            'qualifications': forms.Textarea(attrs={'class': 'form-control', 'row': 5, 'placeholder': 'Enter your Qualification'}),
            'experience_years': forms.IntegerField(),
            'specialties': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Speciality'}),
            'social_media_link': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class':  'form-control', 'placeholder': 'Enter your location'})
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
        model = Video
        fields = ['section', 'title', 'video_file']

        widgets = {
            'section': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select the section'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title of the here'}),
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


class AnnouncementForm(forms.ModelForm):
    class meta:
        model = Announcement
        fields = [
            'title', 'message'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'class-control', 'placeholder': 'Enter the title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter the message here", 'row': 4})
        }
