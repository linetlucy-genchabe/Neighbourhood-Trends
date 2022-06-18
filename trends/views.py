from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.templatetags.static import static
# from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.http import HttpResponse, Http404
import datetime as dt
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import *



# Create your views here.

def index(request):
    date = dt.date.today()
    # business = Business.get_allbusiness()
    # all_neighborhoods = Neighborhood.get_neighborhoods()
    
    
    # if 'neighborhood' in request.GET and request.GET["neighborhood"]:
    #     neighborhoods = request.GET.get("neighborhood")
    #     searched_neighborhood = Business.get_by_neighborhood(neighborhoods)
    #     all_posts = Posts.get_by_neighborhood(neighborhoods)
    #     message = f"{neighborhoods}"
    #     all_neighborhoods = Neighborhood.get_neighborhoods()        
        
    #     return render(request, 'index.html', {"message":message,"location": searched_neighborhood,
    #                                            "all_neighborhoods":all_neighborhoods, "all_posts":all_posts})

    # else:
    #     message = "No Neighborhood Found!"

    return render(request, 'index.html', {"date": date})

def user_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']  
        
        user = authenticate (request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome , you are now logged in")
            return redirect ("home")
    return render(request, 'registration/login.html')




def register(request):
    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2= request.POST['password2']
        
        if password1 != password2:
            messages.error(request,"confirm your passwords")
            return redirect('/register')
        
        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password1)
        
        new_user.save()
        return render(request,'registration/login.html')
    return render(request, 'registration/registration.html')

def signout(request):
    logout(request)
    messages.success(request,"You have logged out")
           
    return redirect("/")


@login_required(login_url='/accounts/login/')
def user_profiles(request):
    current_user = request.user
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        form2 = NewNeighborhoodForm(request.POST)
        
        if form2.is_valid():
            neighborhood = form2.save(commit=False)
            neighborhood.Admin = current_user
            neighborhood.admin_profile = profile
            neighborhood.save()
            return redirect('profile')
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('profile')
            
    else:
        form = ProfileUpdateForm()
        form2 = NewNeighborhoodForm()

    return render(request, 'registration/profile.html', {"form":form, "form2":form2})