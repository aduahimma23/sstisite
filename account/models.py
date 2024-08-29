from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=122, unique=False, blank=False)
    last_name = models.CharField(max_length=122, unique=False, blank=False)
    other_name = models.CharField(max_length=50, blank=True, unique=False)
    phone_number = models.CharField(max_length=20, blank=False, unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self) -> str:
        return f'Nmae of user: {self.first_name} {self.last_name}'
