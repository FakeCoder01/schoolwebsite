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



# loads the deafult landing page : url = '/'
def index(request):
    return render(request, 'index.html',)



# loads the dashboard : url = '/home'
@login_required(login_url='/login/')
def homePage(request):     
    
    # checks if the user is logged in else redirects to the login page
    if request.user.is_authenticated:
        
        # checks for session in the request
        # then get the userType from the session
        if 'user_status' in request.session and request.session['user_status'].get('isLoggedIn') == True:
            userType = request.session['user_status'].get('userType')
            
            # if the userType is Student then get all the students
            if userType == 'Student':
                teachers = teacher.objects.all()
                
                # if there is any filter (gender or stream) then filters the students accondingly
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
                
                # return the result 
                return render(request, 'student-dash.html', {'context':context})
            
            
            # if the userType is Teacher then get all the teachers
            elif userType == 'Teacher':
                students = student.objects.all()
                
                # if there is any filter (gender or stream) then filters the teachers accondingly
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
                # return the result 
                return render(request, 'teacher-dash.html', {'context':context})
            else:
                pass  
            
    return redirect('/login/')




# loads the register user : url = '/reg'
def NewUserReg(request):
    
    # gets the type of the request, if POST then create the user else render the create_user form
    if request.method == 'POST':
        form = userRegForm(request.POST)
        
        # the therequest and userRegForm is valid then create the user and login the user
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # login the user
            user = authenticate(request, username=username, password=password)
            
            
            # group the user as Teachers or Students as per the form
            if request.POST['typeofuser']  == "Student": 
                group = Group.objects.get(name='Students')
            elif request.POST['typeofuser']  == "Teacher":
                group = Group.objects.get(name='Teachers')
            else:
                return redirect('/reg?form=invalid---type')

            # adds the user to that group
            group.user_set.add(user)
            
            # login the user
            login(request, user)
            
            # sets a session with value of userType
            request.session['user_status'] = {
                'isLoggedIn' : True,
                'userType' : request.POST['typeofuser']
            }
            
            # if all succeded then redirects to the new-student or new-teacher            
            return redirect(f"/new-{request.POST['typeofuser'].lower()}/")

        else:
            return redirect('/reg?form=invalid')
    # render the form    
    form = userRegForm()        
    return render(request, 'register.html', {'form':form})


# login : url ='/login
def userLogin(request):
    # if the trquest is not POST render the login form
    if request.method == 'POST':

        # gets the username and password
        username = request.POST['username']
        password = request.POST['password']

        # finds and authenticate the user with the username, password from the form
        user = authenticate(request, username=username, password=password)
        
        # if a user exists with the username and password login the user
        if user is not None:
            
            # login the user
            login(request, user)
            
            # gets the group of the user and sets in the variable userType
            # if no groups exists redirects to the login page
            
            if user.groups.filter(name='Students').exists():
                userType = "Student"
            elif user.groups.filter(name='Teachers').exists():
                userType = "Teacher"
            else : 
                return redirect('/login?form=invalid--type')
            
            # sets a session with value of userType
            request.session['user_status'] = {
                'isLoggedIn' : True,
                'userType' : userType
            }
            
            # redirects to the dashboard ('/home')
            return redirect('/home/')  
        else:
            # if no user exists, the credentials are invalid and redirects to the login page
            return redirect('/login?form=invalid')
        
    # render the login form in the login.html   
    form = userLoginForm()        
    return render(request, 'login.html', {'form':form})


# logout page : url = '/logout'
def userLogOut(request):
    # trirs to delete the session
    try :
        del request.session['user_status']
    except:
        pass    
    # logout the user
    logout(request)
    return redirect('/')


# create new student profile : url = '/new-student'
def newStudentProfile(request):
    
    # checks the request is POST or not
    if request.method == 'POST':
        
        form = studentProfileForm(request.POST, request.FILES, instance=request.user)
        
        # if the form is valid save the user in student and redirects to the dashboard ('/home')
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
    # else render the create new student profile form
    form = studentProfileForm()        
    return render(request, 'student-profile.html', {'form':form})

# create new student profile : url = '/new-teacher'
def newTeacherProfile(request):
    if request.method == 'POST':
        form = teacherRegForm(request.POST, request.FILES)
        
        # if the form is valid save the user in teacher table and redirects to the dashboard ('/home')
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
    # else render the create new teacher profile form    
    form = teacherRegForm()        
    return render(request, 'teacher-profile.html', {'form':form})    

# the api to get a particular student or teacher details : url = ('/api/userid')
# takes an argument userid which is the id for the users User model
@login_required(login_url="/login/")
def userDetails(request, userid):
    msg=''
    
    # checks wherever loggedin or not 
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            # if the type in request.POST id 't', the requested user is  teacher
            if request.POST['type'] == 't':
                # if any user with the userid exists in Usertable and teachertable
                if teacher.objects.filter(user_id=userid, id=request.POST['profile_id']).exists() and User.objects.filter(id=userid, username=request.POST['username']).exists() :
                    
                    # gets the teacher profile
                    profile = teacher.objects.filter(user_id=userid, id=request.POST['profile_id'])
                    
                    # gets the teacher account
                    account = User.objects.filter(id=userid, username=request.POST['username'])
                    
                    # convert the data in json and return as a JSONResponse 
                    return JsonResponse({
                        'status': '200', 
                        'profile': list(profile.values()),
                        'account': list(account.values()),
                    }) 
                msg = msg+'No teachers exists, '     

            # if the type in request.POST id 's', the requested user is  student
            elif request.POST['type'] == 's':
                
                # if any user with the userid exists in Usertable and studenttable
                if student.objects.filter(user_id = userid, id=request.POST['profile_id']).exists() and User.objects.filter(id=userid, username=request.POST['username']).exists() :
                    
                    # gets the student profile
                    profile = student.objects.filter(user_id=userid, id=request.POST['profile_id'])
                    
                    # gets the student account
                    account = User.objects.filter(id=userid, username=request.POST['username'])
                    
                    # convert the data in json and return as a JSONResponse 
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


# userprofile page : url = '/profile'
@login_required(login_url="/login/")
def userProfile(request):
    
    #  checks the user is logged in or not
    if request.user.is_authenticated:
        
        if request.method == 'POST':
            
            # get the form and the user
            form = userEmailForm(request.POST, instance=request.user)
            
            # the the userType is student update the student profile
            if request.session['user_status'].get('userType') == "Student":
                profile_form = studentProfileForm(request.POST, request.FILES, instance=request.user.studentprofile) 
                if form.is_valid():
                    # updates the student model and user model
                    user_form = form.save()
                    custom_form = profile_form.save(False)
                    custom_form.user = user_form
                    custom_form.save()
                    return redirect("/profile?updated=True")

            # the the userType is teacher update the teacher profile
            elif request.session['user_status'].get('userType') == "Teacher":
                
                profile_form = teacherRegForm(request.POST, request.FILES, instance=request.user.teacherprofile) 
                if form.is_valid():
                    # updates the teacher model and user model
                    user_form = form.save()
                    custom_form = profile_form.save(False)
                    custom_form.user = user_form
                    custom_form.save()
                    return redirect("/profile?updated=True")

            else:
                return redirect("/login?updated=False")

        form = userEmailForm(instance=request.user)      
        
        # sets the modelForm according to the student type
        if request.session['user_status'].get('userType') == "Student":
            profile_form = studentProfileForm(instance=request.user.studentprofile)  
        elif request.session['user_status'].get('userType') == "Teacher":
            profile_form = teacherRegForm(instance=request.user.teacherprofile)  
        else:
            return redirect("/login?updated=False")
        
        # passes the form to the profile page
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form 
    return render(request, 'profile.html', args)       

      
