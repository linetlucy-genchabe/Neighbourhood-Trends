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
    all_neighbourhoods = Neighbourhood.get_neighbourhoods()
    
    
    if 'neighbourhood' in request.GET and request.GET["neighbourhood"]:
        neighbourhoods = request.GET.get("neighbourhood")
        searched_neighbourhood = Business.get_by_neighbourhood(neighbourhoods)
        all_posts = Posts.get_by_neighbourhood(neighbourhoods)
        message = f"{neighbourhoods}"
        all_neighbourhoods = Neighbourhood.get_neighbourhoods()        
        
        return render(request, 'index.html', {"message":message,"location": searched_neighbourhood,
                                               "all_neighbourhoods":all_neighbourhoods, "all_posts":all_posts})

    else:
        message = "No Neighborhood Found!"

    return render(request, 'index.html', {"date": date,"all_neighbourhoods":all_neighbourhoods,})

def user_login(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']  
        
        user = authenticate (request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome , you are now logged in")
            return redirect ("index")
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
    profile = Profile.objects.get(user=request.user)
    # profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        form2 = NewNeighbourhoodForm(request.POST)
        
        if form2.is_valid():
            neighbourhood = form2.save(commit=False)
            neighbourhood.Admin = current_user
            neighbourhood.admin_profile = profile
            neighbourhood.save()
            return redirect('profile')
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            form.save()
            return redirect('profile')
            
    else:
        form = ProfileUpdateForm()
        form2 = NewNeighbourhoodForm()

    return render(request, 'registration/profile.html', {"form":form, "form2":form2,})



@login_required(login_url='/accounts/login/')
def search_businesses(request):
    if 'keyword' in request.GET and request.GET["keyword"]:
        search_term = request.GET.get("keyword")
        searched_projects = Business.search_business(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message":message,"businesses": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})


def get_business(request, id):

    try:
        project = Business.objects.get(pk = id)
        
    except ObjectDoesNotExist:
        raise Http404()
    
    
    return render(request, "projects.html", {"project":project})
@login_required(login_url='/accounts/login/')
def new_post(request):
    current_user = request.user
    profile = request.user.profile
    neighbourhood = request.user.profile.neighbourhood

    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.Author = current_user
            post.author_profile = profile
            post.neighbourhood = neighbourhood
            post.save()
        return redirect('index')

    else:
        form = NewPostForm()
    return render(request, 'new-post.html', {"form": form})

@login_required(login_url='/accounts/login/')
def new_business(request):
    current_user = request.user
    profile = request.user.profile

    if request.method == 'POST':
        form = NewBusinessForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.Admin = current_user
            project.admin_profile = profile
            project.save()
        return redirect('index')

    else:
        form = NewBusinessForm()
    return render(request, 'new-business.html', {"form": form})

def signout(request):
    logout(request)
    messages.success(request,"You have logged out")
           
    return redirect("/")

