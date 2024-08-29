from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import random

class InstructorProfile(models.Model):
    instructor = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.CharField(max_length=1024, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to='instructor_pictures', blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=False, null=True)
    phone_number = models.CharField(max_length=15, blank=False, unique=True)
    instructor_id = models.CharField(max_length=8, unique=True, editable=False)
    date_joined = models.DateTimeField(auto_now_add=True)

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
    instructor = models.ForeignKey(InstructorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=False, blank=False)
    course_id = models.CharField(max_length=5, unique=True, editable=False)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Instructor Name: {self.instructor.first_name} {self.instructor.last_name}| Course Title: {self.title} | Date Creted: {self.date_created}'
    
    def save(self, *args, **kwargs):
        if not self.course_id:
            self.course_id = self.generate_unique_course_id()
        super().save(*args, **kwargs)

    def generate_unique_course_id(self):
        while True:
            course_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            if not InstructorProfile.objects.filter(course_id = course_id).exists():
                return course_id


class CourseDetail(models.Model):
    coure = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    cover_image = models.ImageField(upload_to='course_detail', blank=False)

    def __str__(self) -> str:
        return f'Details for {self.coure.title}'
    

class VideoFile(models.Model):
    course_detail = models.ForeignKey(CourseDetail, on_delete=models.CASCADE, related_name='videos')
    video_name = models.CharField(max_length=200, blank=False, unique=True)
    video_des = models.CharField(max_length=2000, blank=True, unique=False)
    video_file = models.FileField(upload_to='course_videos', blank=False)
    video_number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('course_detail', 'video_number')

    def __str__(self) -> str:
        return f'Video {self.video_number} for {self.course_detail.coure.title}'
    
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

    marks = models.PositiveIntegerField(max_length=2, unique=False, blank=False)

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


class MarkAssessment(models.Model):
    '''Mark student assesment'''

    assessment = models.ForeignKey(CreateAssessment, on_delete=models.CASCADE, related_name='mark_assesment')
    student_id = models.CharField(max_length=8, unique=True)
    student_answer = models.TextField()
    marks_obtain = models.PositiveBigIntegerField(blank=True, null=True)
    feedback = models.TextField(max_length=500, blank=True, null=True)

    def clean(self) -> None:
        if self.assessment.question_type == 'MCQ':
            if self.student_answer not in ['A', 'B', 'C', 'D']:
                raise ValidationError("Invalid answer for MCQ. It must be one of the options: A, B, C, or D.")
            if self.student_answer == self.assessment.correct_answer:
                self.marks_obtain = self.assessment.marks
            else:
                self.marks_obtain = 0
        elif self.assessment.question_type == 'SUB':
            if not self.student_answer:
                raise ValidationError("Subjective questions require a student answer.")
            # Marks for subjective answers can be manually assigned

    def __str__(self):
        return f"Assessment: {self.assessment.question_text}, Student: {self.student_id}"