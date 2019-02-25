from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request) :
    return render(request,'basic_app/index.html')

@login_required  #The below view will be rendered only if a user is already logged in
def user_logout(request) :
    logout(request)
    return HttpResponseRedirect(reverse('index'))#Log out and back to index page

@login_required
def special_method(request) :
    return HttpResponse("You are logged in")

def register(request) :

    registered = False

    if request.method == "POST" :
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() :
            user = user_form.save()#Saved to db
            user.set_password(user.password)
            user.save()#Saved to database

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES :
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()#Saved to database

            registered = True
        else :
            print(user_form.errors,profile_form.errors)

    else :
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',{'registered' : registered, 'user_form' : user_form, 'profile_form' : profile_form})

def user_login(request) :
    print(request.method)

    if request.method == 'POST' :
        username = request.POST.get('username')#Here usename is the name attribute of html tag input for username
        password = request.POST.get('password')#Same here too

        user = authenticate(username=username, password=password)#Authenticates the user

        if user :
            if user.is_active : #If User is already logged in and then accesses the user_login view
                login(request,user)
                return HttpResponseRedirect(reverse('index'))#Redirect the user back to the home page
            else :
                return HttpResponse("Account is not active")
        else :
            print("Someone tried to login but failed!!/Wrong Credentials")
            print(f"Username : {username} and Password {password}")
            return HttpResponse("Invalid Login Details Supplied")
    else :
        print("GET REQUEST")
        return render(request,'basic_app/login.html',{})

