from django.shortcuts import render,  redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import *
from student.models import EnrollCourse

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

def create_assessment(request):
    if request.method == 'POST':
        form = CreateAssessmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('instructor:assessment_success')
    else:
        form = CreateAssessmentForm()

    return render(request, 'instructor/create_assessment.html', {'form': form})

def assignment_list(request):
    assignment = Assignment.objects.filter(course_instructor_profile_instructor=request.user)
    return render(request, 'instructor/assignment_list.html', {'assignment': assignment})

def create_assignment(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = form.cleaned_data['course']
            assignment.save()
            messages.success(request, 'Assignment Created Successfully')
            return redirect('instructor:assignment_list', {'form': form})
    else:
        form = AssignmentForm()
    return render(request, 'instructor/create_assignment.html')

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully!')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'edit_assignment.html', {'form': form, 'assignment': assignment})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully!')
        return redirect('assignment_list')
    return render(request, 'delete_assignment.html', {'assignment': assignment})

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
    
def create_announcement(request):
    # Ensure the user is an instructor
    if not request.user.is_instructor:
        return redirect('home')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.instructor = request.user.instructor_profile
            announcement.save()
            return redirect('instructor-announcements')
    else:
        form = AnnouncementForm()

    return render(request, 'create_announcement.html', {'form': form})  

def student_enrolled(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor_profile_instructor=request.user)

    enrollments = EnrollCourse.objects.filter(course=course)

    context = {
        'course': course,
        'enrollment': enrollments
    }

    return render(request, 'instructor/enrolled_students.html', context)