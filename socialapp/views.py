from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView
from socialapp.forms import RegisterForm,LoginForms,UserprofileForm,PostForm,CommentForm,StoryForm
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from socialapp.models import UserProfile,Posts,Stories
from socialapp.decorators import login_requird
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages

decs=[login_requird,never_cache]

# Create your views here.

class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegisterForm

    def get_success_url(self):
        return reverse("signin")

class signInView(FormView):
    template_name="login.html"
    form_class=LoginForms

    def post(self,request,*args,**kwargs):
        forms=LoginForms(request.POST)
        if forms.is_valid():
            uname=forms.cleaned_data.get("username")
            pwd=forms.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:
                login(request,user_object)
                print("successfully.............")
                return redirect("index")
        print("error in login")
        messages.error(request,"faild to login invalid credentilas")
        return render(request ,"login.html",{"form":forms})
    
@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="data"


    def form_valid(self,form):
         form.instance.user=self.request.user
         return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('index')
    
    def get_queryset(self):
        blocked_profiles=self.request.user.profile.block.all()
        blockedprofile_id=[pr.user.id for pr in blocked_profiles]
        print(blockedprofile_id)

        qs=Posts.objects.all().exclude(user__id__in=blockedprofile_id).order_by("-created_date")
        return qs

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        current_date=timezone.now()
        context["stories"]=Stories.objects.filter(expiry_date__gte=current_date)
        return context

@method_decorator(decs,name="dispatch")
class signoutView(View):
    def get(self,request,*args,**kwargs):
         logout(request)
         return redirect("signin")
    
@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
     template_name='profile_add.html'
     form_class=UserprofileForm
     model=UserProfile

     def get_success_url(self):
          return reverse('index')

@method_decorator(decs,name="dispatch")   
class ProfileDetailView(DetailView):
     template_name='Profile_detail.html'
     model=UserProfile
     context_object_name="data"

@method_decorator(decs,name="dispatch")
class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all()
        return render(request,"profile_list.html",{"data":qs})

@method_decorator(decs,name="dispatch")  
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)

        action=request.POST.get("action")
        if action == "like":
            post_object.liked_by.add(request.user)
        elif action == "dislike":
            post_object.liked_by.remove(request.user)

        return redirect("index")

@method_decorator(decs,name="dispatch") 
class CommentView(CreateView):
    template_name="index.html"
    form_class=CommentForm

    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self,form):
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)

@method_decorator(decs,name="dispatch")  
class ProfileBlockView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action == "block":
            request.user.profile.block.add(profile_object)
        elif action == "unblock":
            request.user.profile.block.add(profile_object)
        return redirect("index")

@method_decorator(decs,name="dispatch")
class StorieCreateView(View):
    def post(self,request,*args,**kwargs):
        form=StoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")

    




    


# current classine callcheyyuvan -self
# parent classine callcheyyuvan-super
# query set change -get_query 
# redirect-success_url 
# add cheyyan-form_valid


