from email.policy import default
from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.contrib.auth.models import User
# Create your models here.

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other")
) 

STREAM_CHOICES = (
    ("Science", "Science"),
    ("Arts", "Arts"),
    ("Commerce", "Commerce"),
    ("Other", "Other")
)

STANDARD_CHOICES = (
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("Other", "Other")
) 

SECTION_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
)

class student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True, related_name="studentprofile")
    full_name = models.CharField(max_length=100,)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default="Male")
    standard = models.CharField(max_length=7, choices=STANDARD_CHOICES, default="10")
    stream = models.CharField(max_length=10, choices=STREAM_CHOICES, default="Science")
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, default="A")
    roll_no = models.IntegerField(max_length=8)
    contact = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    img = models.ImageField(upload_to="students/", blank=True, default="s-avatar.jpg")

    def __str__(self) :
        return self.full_name


class teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True, related_name="teacherprofile")
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default="Male")
    stream = models.CharField(max_length=10, choices=STREAM_CHOICES, default="Science")
    classes_taught = models.CharField(max_length=10, choices=STANDARD_CHOICES, default="10",)
    contact = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    img = models.ImageField(upload_to="teachers/", blank=True, default="t-avatar.jpg")
    def __str__(self) :
        return self.full_name


def teacherCreateProfile(sender, **kwargs):
    if kwargs['created']:
        student_profile = teacher.objects.created(user=kwargs['instance'])
    post_save.connect(teacherCreateProfile, sender=User)

def studentCreateProfile(sender, **kwargs):
    if kwargs['created']:
        student_profile = student.objects.created(user=kwargs['instance'])
    post_save.connect(teacherCreateProfile, sender=User)