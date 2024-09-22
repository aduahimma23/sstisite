from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import random
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    first_name = models.CharField(max_length=155, null=False, blank=False, unique=False)
    last_name = models.CharField(max_length=255, )
    instructor_id = models.CharField(max_length=8, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)


class InstructorProfile(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='instructor_pictures', blank=True, null=True)
    qualifications = models.TextField(blank=False, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    specialties = models.CharField(max_length=255, blank=True)
    social_media_link = models.URLField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Instructor Profile"

    def save(self, *args, **kwargs):
        if not self.instructor_id:
            self.instructor_id = self.generate_unique_instructor_id()
        super().save(*args, **kwargs)

    def generate_unique_instructor_id(self):
        while True:
            instructor_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            if not InstructorProfile.objects.filter(instructor_id = instructor_id).exists():
                return instructor_id

class PaymentStatus(models.Model):
    instructor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_status')
    has_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.instructor.username} - {'Paid' if self.has_paid else 'Not Paid'}"
    

class Course(models.Model):
    instructor_profile = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=False, blank=False)
    course_id = models.CharField(max_length=8, unique=True, editable=False)
    description = models.TextField()
    image_flyer = models.ImageField(upload_to='course_image/', blank=False, unique=True)
    status = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Instructor Name: {self.instructor_profile.instructor.first_name} {self.instructor_profile.instructor.last_name} | Course Title: {self.title} | Date Created: {self.date_created}'

    def save(self, *args, **kwargs):
        if not self.course_id:
            self.course_id = self.generate_unique_course_id()
        super().save(*args, **kwargs)

    def generate_unique_course_id(self):
        while True:
            course_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            if not Course.objects.filter(course_id=course_id).exists():
                return course_id

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    section_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    section_number = models.PositiveIntegerField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # If the section is being created
            last_section = Section.objects.filter(course=self.course).order_by('section_number').last()
            self.section_number = last_section.section_number + 1 if last_section else 1
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Section {self.section_number}: {self.section_title} - {self.course.title}'


class Video(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='course_videos/')
    video_number = models.PositiveIntegerField(editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_video = Video.objects.filter(section = self.section).order_by('video_number').last()
            self.video_number = last_video.video_number + 1 if last_video else 1

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.video_title} in {self.section.section_title}'


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Assessment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=50)
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.assessment_type}"


class CreateAssessment(models.Model):
    QUESTION_CHOICE_TYPE = [
        ('MCQ', 'Multiple Choice Questions'),
        ('SUB', 'Subjective Questions'),
    ]

    CORRECT_ANSWER_OPTION = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    question_type = models.CharField(max_length=10, choices=QUESTION_CHOICE_TYPE, blank=False, default='MCQ')
    question_text = models.CharField(max_length=255, unique=True, blank=False)

    # Options for MCQ
    option_a = models.CharField(max_length=255, blank=True)
    option_b = models.CharField(max_length=255, blank=True)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)

    marks = models.PositiveIntegerField(blank=False)

    correct_answer = models.CharField(max_length=1, blank=False, choices=CORRECT_ANSWER_OPTION)

    # Subjective answer
    answer_text = models.TextField(blank=True, null=True)

    def clean(self) -> None:
        if self.question_type == 'MCQ' and not (self.option_a or self.option_b or self.correct_answer):
            raise ValidationError('MCQ type questions require options and a correct answer.')
        if self.question_type == 'SUB' and not self.answer_text:
            raise ValidationError("Subjective questions require an answer text.")
    
    def __str__(self):
        return self.question_text


class StudentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submission_file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submission_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class MarkAssessment(models.Model):
    student_submission = models.ForeignKey(StudentSubmission, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_submission.student.username} - Marks: {self.marks_obtained}"
    

class Announcement(models.Model):
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    message = models.TextField(blank=False)
    date_created = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    

