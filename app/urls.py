from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.homePage, name='dash'),
    path('reg/', views.NewUserReg, name='register'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogOut, name='logout'),
    path('new-student/', views.newStudentProfile, name='newStudentProfile'),
    path('new-teacher/', views.newTeacherProfile, name='newTeacherProfile'),
    path('api/user-details/<str:userid>/', views.userDetails, name='userDetails'),
    path('profile/', views.userProfile, name='userProfile'),
]
