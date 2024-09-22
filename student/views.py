from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from .forms import *
from .models import *
from instructor.models import Course, Video


def home_view(request):
    
    return render(request, 'student/index.html')

def student_profile(request):
    profile = StudentProfile.objects.get(student=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view page
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student/student_profile.html', {'form': form})

def edit_profile(request):
    return render(request, 'student/forms/edit_profile.html', )

def add_to_wishlist(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    wishlist, created = Wishlist.objects.get_or_create(student = request.user, course=course)
    if created:
        return redirect('wishlist')
    else:
        return redirect('course_detail', course_id=course.id)
    
def remove_from_wishlist(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    wishlist = Wishlist.objects.filter(student=request.user, course=course)
    if wishlist.exists():
        wishlist.delete()
    return redirect('wishlist')

def wishlist(request):
    wishlist = Wishlist.objects.filter(student=request.user).select_related('course')
    return render(request, 'wishlist/wishlist.html', {'wishlist': wishlist})

# Course to be displayed from the instructor or the admin
def course_list(request):
    courses = Course.objects.filter(status=True)

    return render(request, 'student/course.html', {'courses': courses})

# Details for the related course
def course_detail(request, course_id):
    courses = get_object_or_404(Course, id=course_id)

    videos = courses.video.all()

    context = {
        'courses': courses,
        'videos': videos
    }

    return render(request, 'student/course_detail.html', context)

def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    student = request.user.studentprofile
    
    if EnrollCourse.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'You have already enrolled in this course')
    else:
        EnrollCourse.objects.create(student=student, course=course)
        messages.success(request, f'You have successfully enrolled in {course.title}')
        
    return redirect('course_detail', course=course_id)

def submit_assessment(request, assessment_id):
    assessment = get_object_or_404(CreateAssessment, id=assessment_id)
    
    if request.method == 'POST':
        selected_answer = request.POST.get('selected_answer')
        
        attempt = AttemptAssessment(
            student=request.user,
            assessment=assessment,
            selected_answer=selected_answer
        )
        attempt.save()
        return redirect('assessment_results', attempt_id=attempt.id)
    
    return render(request, 'student/submit_assessment.html', {'assessment': assessment})

def assessment_results(request, attempt_id):
    attempt = get_object_or_404(AttemptAssessment, id=attempt_id)
    return render(request, 'student/assessment_result.html', {'attempt': attempt})

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

def certificate_status_view(request):
    student = request.user.student
    certificate_requests = CertificateRequest.objects.filter(student=student)

    return render(request, 'student/certificate_status.html', {'certificate_requests': certificate_requests})

def download_certificate(request, certificate_id):
    certificate_request = get_object_or_404(CertificateRequest, id=certificate_id, student=request.user.student)
    
    if certificate_request.is_approved and certificate_request.certificate_file:
        # Serve the certificate file for download
        response = HttpResponse(certificate_request.certificate_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{certificate_request.course.title}_certificate.pdf"'
        return response
    else:
        return redirect('certificate_status') 

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

def add_to_favorites(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    favorite, created = Favorite.objects.get_or_create(student=student, course=course)
    return redirect('student:course_list')

def remove_from_favorites(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    favorite = Favorite.objects.filter(student=student, course=course).delete()
    return redirect('student:favorite_list')

def favorite_list(request):
    # student = request.user.student
    favorites = Favorite.objects.filter()
    return render(request, 'student/courses/favorite_list.html', {'favorites': favorites})