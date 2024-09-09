from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import random


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    full_name = models.CharField(max_length=155, null=False, blank=False, unique=False)
    expertise = models.CharField(max_length=255, blank=False, null=True)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    instructor_id = models.CharField(max_length=8, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)


class InstructorProfile(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1024, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='instructor_pictures', blank=True, null=True)

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


class Course(models.Model):
    instructor_profile = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=False, blank=False)
    course_id = models.CharField(max_length=8, unique=True, editable=False)
    description = models.TextField()
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


class CourseDetail(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    content_type = models.CharField(max_length=255, blank=False, null=False)
    content = models.FileField(upload_to='course_content/')
    video_number = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Details for {self.course_name.title}'


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
    '''For the Instructor to create a question'''

    QUESTION_CHOICE_TYPE = [
        ('MCQ', 'Multiplle Choice Questions'),
        ('SUB', 'Subjective Quesitions'),
    ]

    CORRECT_ANSWER_OPTION = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    question_type = models.CharField(max_length=10, choices=QUESTION_CHOICE_TYPE, blank=False, default='MCQ')
    question_text = models.CharField(max_length=255, unique=True, blank=False)

    # If the question is multiple choice
    option_a = models.CharField(max_length=255, blank=True, unique=True)
    option_b = models.CharField(max_length=255, blank=True, unique=True)
    option_c = models.CharField(max_length=255, blank=True, unique=True)
    option_d = models.CharField(max_length=255, blank=True, unique=True)

    marks = models.PositiveIntegerField(unique=False, blank=False)

    correct_answer = models.CharField(max_length=1, blank=False, null=False, unique=False, choices=CORRECT_ANSWER_OPTION)

    # if the question is subjective
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
    

class PaymentStatus(models.Model):
    instructor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_status')
    has_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.instructor.username} - {'Paid' if self.has_paid else 'Not Paid'}"
