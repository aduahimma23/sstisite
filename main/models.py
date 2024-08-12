from django.db import models

class Address(models.Model):
    street_address = models.CharField(max_length=122, unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=False, unique=True)
    email_address = models.EmailField()


class SociolMedia(models.Model):
    facebook_address = models.URLField()
    twitter_address = models.URLField()
    youtube_address = models.URLField()
    linkedin_address = models.URLField()
    instagram_address = models.URLField()


class Courses(models.Model):
    course_name = models.CharField(max_length=128, unique=True, null=False)
    short_content = models.CharField(max_length=255, null=False, unique=True)
    main_content = models.CharField(max_length=2500, blank=True, unique=True)
    created_by = models.CharField(max_length=50, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Course Name: {self.course_name}'


class Contact(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)


class ContactQuery(models.Model):
    name = models.CharField(max_length=120, blank=False)
    email_address = models.EmailField()
    subject = models.CharField(max_length=128, blank=False, unique=False)
    message = models.CharField(max_length=500, blank=False)

    def __str__(self) -> str:
        return f'Contacted Person: {self.name}'

class Testimonial(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField()
    text = models.CharField(max_length=1000, blank=False)

    def __str__(self) -> str:
        return f'Name: {self.name}'
    
