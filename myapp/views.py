import json
import requests
 
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt

"""Http Libraries"""
from django.shortcuts import HttpResponse, HttpResponseRedirect, redirect, render
from django.http import JsonResponse
from rest_framework import status

"""Database libraries"""
from .models import person
from django.db.models import Q

"""Form Libraries"""
from .form import PrForm, UserForm

"""Authhentication Libraries"""
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

"""Serialization REST API libraries"""
from .serializers import PrSerializer

"""API View"""
from rest_framework import permissions
from rest_framework.response import Response
from myapp.utility import success,unsuccess

# APIView
from rest_framework.views import APIView

# ModelViewset
from rest_framework import viewsets

"""Home Page and Login Page"""
def home(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('main')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    context = {
        "form": form
    }
    # logout(request)
    return render(request, "login.html", context)
def main(request):
    return render(request, "home.html")

"""SignUp Form (Create User)"""
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, ("Registration Successful!"))
            #login(request, user)
            """greetings mail to User for successfully registration """
            # subject = 'welcome to Rishi first site'
            # message = f'Hi {user.username}, thank you for registering in or site.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            # send_mail( subject, message, email_from, recipient_list )
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

"""LogOut Page"""
def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    #return render(request, 'logout.html')
    return redirect("home")

"""Change Password Form"""
@login_required(login_url='home')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_pass.html', {'form': form})

"""create details form(model database)"""
@login_required(login_url='home')
def Reg_View(request):
    context = {}
    form = PrForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/ListView/")
    context['form'] = form
    return render(request, 'View.html', context)

"""Retrieve List View Database"""
@login_required(login_url='home')
def list_view(request):
    context = person.objects.all()
    return render(request, "List_view.html", {'context': context})

"""Retrieve detail View Database"""
@login_required(login_url='home')
def detail_view(request, id):
    context = person.objects.get(id=id)
    return render(request, "detail_view.html", {'context': context})

"""Update View Database"""
@login_required(login_url='home')
def update_view(request, id):
    context = {}
    Emp1 = person.objects.get(id=id)
    form = PrForm(request.POST or None, instance=Emp1)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/ListView/")
    context["form"] = form
    return render(request, "update_view.html", context)

"""Delete View Database"""
@login_required(login_url='home')
def delete_view(request, id):
    context = {}
    ob = person.objects.get(id=id)
    if request.method == "POST":
        ob.delete()
        return HttpResponseRedirect("/ListView/")
    return render(request, "delete_view.html", context)

"""Search View Database"""
@login_required(login_url='home')
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        context = person.objects.filter(Q(name__contains=searched) | Q(
            age__contains=searched) | Q(job_type=searched) | Q(address=searched))

        return render(request, 'List_view.html', {'context': context})
    else:
        return render(request, 'List_view.html', {})

"""API VIEW METHOD"""
class ListUsers(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        Email = [user.email for user in User.objects.all()]
        return Response({"username": usernames, "Email": Email})

class Data(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):  
        Emp1 = person.objects.all()
        serializer = PrSerializer(Emp1, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data=request.data
        serializer = PrSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            code = status.HTTP_201_CREATED 
            return Response(success(code, "Data inserted", serializer.data),code)
        code = status.HTTP_404_NOT_FOUND
        return Response(unsuccess(code,serializer.errors),code)

# class Datadetail(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     def get(self, request, obj, format=None):
#         Emp1 = person.objects.get(id=obj)
#         serializer = PrSerializer(Emp1)
#         return Response(serializer.data)

#     def put(self, request, obj, format=None):
#         Emp1 = person.objects.get(id=obj)
#         data = request.data
#         serializer = PrSerializer(Emp1, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             code = status.HTTP_200_OK 
#             return Response(success(code,"Data Updated Successfully!", serializer.data),code)
#         code = status.HTTP_404_NOT_FOUND
#         return Response(unsuccess(code,serializer.errors),code)

#     def patch(self, request, obj, format=None):
#         Emp1 = person.objects.get(id=obj)
#         data = request.data
#         serializer = PrSerializer(Emp1, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             code = status.HTTP_200_OK 
#             return Response(success(code,"Partialy Data Updated Successfully!", serializer.data),code)
#         code = status.HTTP_404_NOT_FOUND
#         return Response(unsuccess(code,serializer.errors),code)

#     def delete(self, request, obj, format=None):
#         try:
#             stu = person.objects.get(id=obj)
#             stu.delete()
#             code=status.HTTP_204_NO_CONTENT
#             return Response(success(code,"Data deleted successfully!","null"),code)
#         except:
#             code = status.HTTP_404_NOT_FOUND
#             return Response(unsuccess(code,"null"),code)

"""MODELVIEWSET Method"""
class PersonViewset(viewsets.ModelViewSet):
    queryset = person.objects.all()
    serializer_class = PrSerializer
