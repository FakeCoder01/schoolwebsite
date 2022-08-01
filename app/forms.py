from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserModel
from .models import student, teacher


# for the student creation of student model
class studentProfileForm(ModelForm):
    class Meta:
        model = student
        fields = ('full_name', 'gender', 'standard', 'stream', 'section', 'roll_no', 'contact', 'address', 'img')

# for the teacher creation of teacher model
class teacherRegForm(ModelForm):
    class Meta:
        model = teacher
        fields = ('full_name', 'gender', 'stream', 'classes_taught', 'contact', 'address', 'img')

# user registraion from for User
class userRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]

class userEmailForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email',]

# user login from for User
class userLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','password', ]
