from django import forms
from .models import *


class InstructorprofileForm(forms.ModelForm):
    class Meta:
        model = InstructorProfile
        fields = [
            'phone_number', 'profile_picture', 'qualifications', 
            'experience_years', 'specialties', 'social_media_link',
            'location'
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


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'due_date']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class CreateAssessmentForm(forms.ModelForm):
    class Meta:
        model = CreateAssessment
        fields = ['question_type', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'marks', 'correct_answer', 'answer_text']
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control'}),
            'option_a': forms.Select(attrs={'class': 'form-control'}),
            'option_b': forms.Select(attrs={'class': 'form-control'}),
            'option_c': forms.Select(attrs={'class': 'form-control'}),
            'option_d': forms.Select(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.Select(attrs={'class': 'form-control'}),
            'answer_text': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateAssessmentForm, self).__init__(*args, **kwargs)

        # Define dropdown options for A, B, C, and D
        OPTIONS = [
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D'),
        ]

        # Set the dropdowns for each option
        self.fields['option_a'].widget = forms.Select(choices=OPTIONS, attrs={'class': 'form-control'})
        self.fields['option_b'].widget = forms.Select(choices=OPTIONS, attrs={'class': 'form-control'})
        self.fields['option_c'].widget = forms.Select(choices=OPTIONS, attrs={'class': 'form-control'})
        self.fields['option_d'].widget = forms.Select(choices=OPTIONS, attrs={'class': 'form-control'})


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
            'title', 'message', 'course'
        ]

        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'class-control', 'placeholder': 'Enter the title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter the message here", 'row': 4})
        }


