from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .forms import *
from .models import *


def update_student_profile(request):
    profile = StudentProfile.objects.get(student=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student/update_profile.html', {'form': form})


def attempt_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    if timezone.now() > assignment.duedate:
        messages.error(request, "The due date has passed. You can no longer attempt this assignment.")
        return render('assignment_list')
    
    attempt, created = AttemptAssignment.objects.get_or_create(
        student=request.user,
        assignment=assignment
    )

    if request.method == 'POST':
        attempt.submission = request.POST['submission']
        attempt.status = 'Submitted'
        attempt.submitted_at = timezone.now()
        attempt.save()

        messages.success(request, 'Assignment submitted successfully!')
        return redirect('assignment_list')
    
    return render(request, 'student/late_sub.html', {'assignment': assignment, 'attempt': attempt})


def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    student = request.user.studentprofile
    
    if EnrollCourse.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'You have already enrolled in this course')
    else:
        EnrollCourse.objects.create(student=student, course=course)
        messages.success(request, f'You have successfully enrolled in {course.title}')
        
    return redirect('course_detail', course=course_id)


def certificate_request(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    completed = ViewCourse.objects.filter(student=request.user, course=course, is_complete=True).exists()
    
    if not completed:
        messages.error(request, 'You cannot request a for a course you have not completed!')
        return redirect('course_detail', course_id=course_id)
    
    cert_request, created = CertificateRequest.objects.get_or_create(student=request.user, course=course)
    
    #Generate a certificate PDF
    if created:
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, f'Certificate of Completion')
        p.drawString(100, 700, f"Congratulations {request.user.get_full_name()}!")
        p.drawString(100, 650, f"You have successfully completed the course: {course.title}.")
        p.showPage()
        p.save()
        
        # Save the PDF in the certificate request model
        cert_request.certificate_file.save(f"{request.user.username}_{course.title}_certificate.pdf", buffer)
        
    return redirect('download_certificate', cert_id=cert_request.id)

def download_certificate(request, cert_id):
    cert_request = get_object_or_404(CertificateRequest, pk=cert_id, student=request.user)
    
    if cert_request.certificate_file:
        return FileResponse(cert_request.certificate_file.open('rb'), as_attachment=True, filename=f'certificate_{cert_request.course.title}.pdf')
    
    messages.error(request, 'Certificate not available for download.')
    return redirect('course_detail', course_id=cert_request.course.id)


def submit_feedback(request, course_id):
    course = Course.objects.get(id=course_id)
    instructor = course.instructor_profile
    student = request.user.student
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = student
            feedback.instructo = instructor
            feedback.course = course
            feedback.save()
            messages.success(request, 'Feedback submitted successfully')
            return redirect('course_detail', course_id=course.id)
        
    else:
        form = FeedbackForm()
        
    return render(request, 'student/submit_feedback', {'form': form, 'course': course})
