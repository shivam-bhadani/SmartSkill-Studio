from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from core.models import TimeStampAndUUIModel
from .manager import CustomUserManager

def upload_profile_picture(instance, filename):
    return "profile_picture/{0}".format(filename)

class User(AbstractBaseUser, PermissionsMixin, TimeStampAndUUIModel):

    # These fields tie to the roles!
    ADMIN = 1
    INSTRUCTOR = 2
    STUDENT = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (INSTRUCTOR, 'Instructor'),
        (STUDENT, 'Student')
    )

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to=upload_profile_picture, null=True, blank=True, default='default_profile_picture.png')
    about = models.TextField(blank=True, null=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can access the admin site.',
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.email} <-> {self.role}"
