from django.db import models
import datetime as dt
from django.contrib.auth.models import User
# from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404


# Create your models here.
   

class Neighbourhood(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    occupants_count = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    country = CountryField(blank_label='(select country)', default='NG')

        
    def save_neighbourhood(self):
        self.save()
    
    def delete_neighbourhood(self):
        self.delete()
        
    @classmethod
    def get_neighbourhoods(cls):
        projects = cls.objects.all()
        return projects
    
    @classmethod
    def search_neighbourhoods(cls, search_term):
        projects = cls.objects.filter(name__icontains=search_term)
        return projects
    
    
    @classmethod
    def get_by_admin(cls, Admin):
        projects = cls.objects.filter(Admin=Admin)
        return projects
    
    
    @classmethod
    def get_neighbourhood(request, neighborhood):
        try:
            project = Neighbourhood.objects.get(pk = id)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return project
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'My Neighbourhood'
        verbose_name_plural = 'Neighbourhoods'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('image')
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE, blank=True, default='1')

    def save_profile(self):
        self.save()
        
        

    def delete_profile(self):
        self.delete()
    
    def __str__(self):
        return f"{self.user}, {self.bio}, {self.photo}"
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
            
        
class Business(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    pub_date = models.DateTimeField(auto_now_add=True)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    admin_profile = models.ForeignKey(Profile,on_delete=models.CASCADE, blank=True, default='1')
    address = models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE, blank=True, default='1')

    
    def save_business(self):
        self.save()
    
    def delete_business(self):
        self.delete()
        
    @classmethod
    def get_allbusiness(cls):
        business = cls.objects.all()
        return business
    
    @classmethod
    def search_business(cls, search_term):
        business = cls.objects.filter(name__icontains=search_term)
        return business
    
    @classmethod
    def get_by_neighbourhood(cls, neighbourhoods):
        business = cls.objects.filter(neighbourhood__name__icontains=neighbourhoods)
        return business
    
    @classmethod
    def get_businesses(request, id):
        try:
            business = Business.objects.get(pk = id)
            
        except ObjectDoesNotExist:
            raise Http404()
        
        return business
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'My Business'
        verbose_name_plural = 'Business'


class Posts(models.Model):
    post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)    
    neighbourhood = models.ForeignKey(Neighbourhood,on_delete=models.CASCADE)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_profile = models.ForeignKey(Profile,on_delete=models.CASCADE)


    def save_post(self):
        self.save()
    
    def delete_post(self):
        self.delete()
        
    @classmethod
    def get_allpost(cls):
        posts = cls.objects.all()
        return posts
    
    @classmethod
    def get_by_neighbourhood(cls, neighbourhoods):
        posts = cls.objects.filter(neighbourhood__name__icontains=neighbourhoods)
        return posts
    
    def __str__(self):
        return self.post
    
    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'My Post'
        verbose_name_plural = 'Posts'