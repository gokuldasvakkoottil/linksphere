from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django import forms

from socialapp.models import UserProfile,Posts,Comments,Stories


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        

class LoginForms(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

class UserprofileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=('user','following','block')

class PostForm(forms.ModelForm):
     class Meta:
        model=Posts
        fields=('title','post_image')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['text']

class StoryForm(forms.ModelForm):
    class Meta:
        model=Stories
        fields=["title","post_image"]
