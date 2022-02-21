"""Model libraries"""
from django import forms
from .models import person

"""Authentication Libraries"""
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from django.forms.fields import EmailField  

"""User creation Form"""
class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:   
            return email
        raise forms.ValidationError('This email address is already in use.')

"""Person Detail /Registration (Modelform)"""
class PrForm(forms.ModelForm):
    # create meta class
    class Meta:
        # specify model to be used
        model = person
 
        # specify fields to be used
        fields = "__all__"



