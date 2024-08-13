from django import forms
from .models import Contact, Testimonial

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

        widget = {
            
        }
    

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'