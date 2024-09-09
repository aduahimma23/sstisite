from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import random
from django.conf import settings
from instructor.models import Instructor, Course, CourseDetail, Assignment


user = get_user_model()


class Student(models.Model):
    first_name = models.CharField(max_length=120, blank=False, unique=False)
    last_name = models.CharField(max_length=120, blank=False, unique=False)
    student_id = models.CharField(max_length=8, blank=False, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10, blank=False, unique=True)

    def __str__(self) -> str:
        return f'Student Name: {self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = self.generate_student_id()
        super().save(*args, **kwargs)

    def generate_student_id(self):
        while True:
            student_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            if not Student.objects.filter(student_id=student_id).exists():
                return student_id


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='stdent')
    profile_picture = models.ImageField(upload_to='student profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Student Name: {self.student.first_name} {self.student.last_name}'


class EnrollCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enroll courses')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student')
    enroll_at = models.DateTimeField(auto_now_add=True)
    progress = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_complete = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Student: {self.student.first_name}'
    
    def complete_course(self):
        self.is_complete = True
        
        
class ViewCourse(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor_profile')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='view course')
    course = models.ForeignKey(CourseDetail, on_delete=models.CASCADE, related_name='course_details')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Student: {self.student.first_name} {self.student.last_name} Course Name: {self.course.course_name} Instructor Name: {self.instructor.full_name}'
    
class AttemptAssignment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignment_attempts')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='assignment_attempts')
    submitted_work = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    submission_time = models.DateTimeField(blank=True, null=True)
    marks_obtained = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)


class TrackProgress(models.Model):
    student = models.ForeignKey(EnrollCourse, on_delete=models.CASCADE, related_name='track progrss')
    progress_percentage = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    
class Feedback(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_feedback')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='instructor_feedback')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_feedback')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text='Rate from 1 to 5')
    feedback_text = models.TextField(blank=True, null=True)
    
    def __str__(self) -> str:
        return f'Feedback {self.student.first_name} {self.student.last_name}'

    
class CertificateRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates_request')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificate_requests')
    request_date = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        unique_together = ('student', 'course')
        
    def __str__(self):
        return f"Certificate request by {self.student.username} for {self.course.title}"
    
    # Ensure the student has completed the course before requesting the certificate
    def clean(self):
        course_completion = ViewCourse.objects.filter(student=self.student, course=self.course, is_completed=True).exists()
        if not course_completion:
            raise ValidationError('You cannot request a certificate for a course you have not completed.')
