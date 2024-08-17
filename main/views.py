from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *

def home_view(request):
    return render(request, 'main/index.html')

def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save(commit=False)
            messages.success(request, 'Your message has been sent successfully!')

            return redirect('contact')
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        contact_form = ContactForm()

    return render(request, 'main/contact.html', {'form': contact_form})            

def about_view(request):
    
    return render(request, 'main/about.html')

def coures_view(request):
    return render(request, 'main/course.html')