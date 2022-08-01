from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, get_user_model
from requests import Response
from .forms import userRegForm, userLoginForm, studentProfileForm, teacherRegForm, userEmailForm
from django.contrib.auth.decorators import login_required
from .models import student, teacher
from django.contrib.auth.models import Group, User
import json, datetime

# Create your views here.

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def index(request):
    return render(request, 'index.html',)


@login_required(login_url='/login/')
def homePage(request):     
    if request.user.is_authenticated:
        if 'user_status' in request.session and request.session['user_status'].get('isLoggedIn') == True:
            userType = request.session['user_status'].get('userType')
            if userType == 'Student':
                teachers = teacher.objects.all()
                if 'gender' in request.GET:
                    teachers = teachers.filter(gender=request.GET['gender'])
                if 'stream' in request.GET:
                    teachers = teachers.filter(stream=request.GET['stream'])    
                context = {
                    'total_teachers' : teacher.objects.all().count(),
                    'teachers' : teachers,
                    'userType' : userType,
                    'search_result_count' : teachers.count()
                }
                return render(request, 'student-dash.html', {'context':context})

            elif userType == 'Teacher':
                students = student.objects.all()
                if 'gender' in request.GET:
                    students = students.filter(gender=request.GET['gender'])
                if 'stream' in request.GET:
                    students = students.filter(stream=request.GET['stream'])  
                context = {
                    'total_students' : student.objects.all().count(),
                    'students' : students,
                    'userType' : userType,
                    'search_result_count' : students.count()
                }
                return render(request, 'teacher-dash.html', {'context':context})
            else:
                pass  
    return redirect('/login/')


def NewUserReg(request):
    if request.method == 'POST':
        form = userRegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)

            if request.POST['typeofuser']  == "Student": 
                group = Group.objects.get(name='Students')
            elif request.POST['typeofuser']  == "Teacher":
                group = Group.objects.get(name='Teachers')
            else:
                return redirect('/reg?form=invalid---type')


            group.user_set.add(user)

            login(request, user)
            request.session['user_status'] = {
                'isLoggedIn' : True,
                'userType' : request.POST['typeofuser']
            }
            return redirect(f"/new-{request.POST['typeofuser'].lower()}/")

        else:
            return redirect('/reg?form=invalid')
    form = userRegForm()        
    return render(request, 'register.html', {'form':form})


def userLogin(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='Students').exists():
                userType = "Student"
            elif user.groups.filter(name='Teachers').exists():
                userType = "Teacher"
            else : 
                return redirect('/login?form=invalid--type')
            request.session['user_status'] = {
                'isLoggedIn' : True,
                'userType' : userType
            }
            return redirect('/home/')  
        else:
            return redirect('/login?form=invalid')
    form = userLoginForm()        
    return render(request, 'login.html', {'form':form})


def userLogOut(request):
    try :
        del request.session['user_status']
    except:
        pass    
    logout(request)
    return redirect('/')


def newStudentProfile(request):
    if request.method == 'POST':
        form = studentProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            account = student.objects.create(
                user=request.user,
                full_name = form.cleaned_data.get('full_name'),
                gender = form.cleaned_data.get('gender'),
                standard = form.cleaned_data.get('standard'),
                stream = form.cleaned_data.get('stream'),
                section = form.cleaned_data.get('section'),
                roll_no = form.cleaned_data.get('roll_no'),
                contact = form.cleaned_data.get('contact'),
                address = form.cleaned_data.get('address'),
                img = form.cleaned_data['img'],
            ) 
            return redirect('/home/')
        else:
            return redirect('/new-student?form=invalid')
    form = studentProfileForm()        
    return render(request, 'student-profile.html', {'form':form})


def newTeacherProfile(request):
    if request.method == 'POST':
        form = teacherRegForm(request.POST, request.FILES)
        if form.is_valid():
            account = teacher.objects.create(
                user=request.user,
                full_name = form.cleaned_data.get('full_name'),
                gender = form.cleaned_data.get('gender'),
                stream = form.cleaned_data.get('stream'),
                classes_taught = form.cleaned_data.get('classes_taught'),
                contact = form.cleaned_data.get('contact'),
                address = form.cleaned_data.get('address'),
                img = form.cleaned_data['img'],
            ) 
            return redirect('/home/')
        else:
            return redirect('/new-teacher?form=invalid')
    form = teacherRegForm()        
    return render(request, 'teacher-profile.html', {'form':form})    


@login_required(login_url="/login/")
def userDetails(request, userid):
    msg=''
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['type'] == 't':
                if teacher.objects.filter(user_id=userid, id=request.POST['profile_id']).exists() and User.objects.filter(id=userid, username=request.POST['username']).exists() :
                    profile = teacher.objects.filter(user_id=userid, id=request.POST['profile_id'])
                    account = User.objects.filter(id=userid, username=request.POST['username'])
                    return JsonResponse({
                        'status': '200', 
                        'profile': list(profile.values()),
                        'account': list(account.values()),
                    }) 
                msg = msg+'No teachers exists, '     

            elif request.POST['type'] == 's':
                if student.objects.filter(user_id = userid, id=request.POST['profile_id']).exists() and User.objects.filter(id=userid, username=request.POST['username']).exists() :
                    profile = student.objects.filter(user_id=userid, id=request.POST['profile_id'])
                    account = User.objects.filter(id=userid, username=request.POST['username'])
                    return JsonResponse({
                        'status': '200', 
                        'profile': list(profile.values()),
                        'account': list(account.values()),
                    }) 
                msg = msg+'No students exists, '       
            else:
                msg = msg+'Type not set, '
        msg = msg+'Request invalid, '         
    else:
        msg = msg+'Not logged in, '       
    return JsonResponse(json.dumps({
        'status': '404', 
        'msg': msg,
    }), safe=False) 

@login_required(login_url="/login/")
def userProfile(request):
    dp = ''
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = userEmailForm(request.POST, instance=request.user)
            if request.session['user_status'].get('userType') == "Student":
                profile_form = studentProfileForm(request.POST, request.FILES, instance=request.user.studentprofile) 
                if form.is_valid():
                    user_form = form.save()
                    custom_form = profile_form.save(False)
                    custom_form.user = user_form
                    custom_form.save()
                    return redirect("/profile?updated=True")

            elif request.session['user_status'].get('userType') == "Teacher":
                profile_form = teacherRegForm(request.POST, request.FILES, instance=request.user.teacherprofile) 
                if form.is_valid():
                    user_form = form.save()
                    custom_form = profile_form.save(False)
                    custom_form.user = user_form
                    custom_form.save()
                    return redirect("/profile?updated=True")

            else:
                return redirect("/login?updated=False")

        form = userEmailForm(instance=request.user)      
        if request.session['user_status'].get('userType') == "Student":
            profile_form = studentProfileForm(instance=request.user.studentprofile)  
        elif request.session['user_status'].get('userType') == "Teacher":
            profile_form = teacherRegForm(instance=request.user.teacherprofile)  
        else:
            return redirect("/login?updated=False")
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form 
    return render(request, 'profile.html', args)       

      