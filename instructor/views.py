from django.shortcuts import render,  redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *

class HomeView(TemplateView):
    template_name = 'instructor/index.html'

class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'forms/course_form.html'
    success_url = reverse_lazy('course_list')

    def form_valid(self, form):
        try:
            messages.success(self.request, 'Course Created Successfully')
            return super().form_valid(form)
        except ValueError as err:
            form.add_error(None, f'Check Your Form and Submit it Again: {err}')
            return self.form_invalid(form)
        
def course_detail_create(request):
    if request.method == 'POST':
        form = CourseDetailsForm(request.POST)
        if form.is_valid():
            files = request.FILES.getlist('content')
            course_name = form.cleaned_data('course_name')
            course_type = form.changed_data('course_type')
            video_number = form.cleaned_data('video_number')

            for file in files:
                Video.objects.create(
                    course_name = course_name,
                    course_type = course_type,
                    content = file,
                    video_number = video_number
                )
            
            messages.success(request, 'Details Saved Successfully')
            return redirect('course_list')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = CourseDetailsForm()

    return render(request, 'forms/course_detail_form.html', {'form': form})

def create_annoucement(request, course_id):
    if request.method == 'POST':
        forms = AnnouncementForm(request.POST)
        if forms.is_valid():
            forms.save(commit=False)
            messages.success(request, 'Annoucement created successfully')
        else:
            messages.error(request, 'Fill all the fields')
    else:
        forms = Announcement()

class MarkAssessmentView(View):
    template_name = 'instructor/mark_assessment.html'

    def get(self, request, *args, **kwargs):
        form = MarkAssessmentForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MarkAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assessment marked successfully.')
            return redirect(reverse_lazy('assessment_list'))
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, self.template_name, {'form': form})
    

