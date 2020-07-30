from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm

def home(request):
    return render(request,'home.html')

def signupuser(request):
    if request.method == 'GET':
        # django form, auto creates a form for us
        return render(request, 'signupuser.html', {'form': UserCreationForm()})
    else:
        # create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                # using django built in user object from auth
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'Username already exists'})
        else:
            return render(request, 'signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        # django form, auto creates a form for us
        return render(request, 'loginuser.html', {'form': AuthenticationForm()})
    else:
        # check username and password with django auth
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'createtodo.html', {'form': TodoForm(), 'error':'Bad data passed in. Try again.'})

def currenttodos(request):
    return render(request, 'currenttodos.html')