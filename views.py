from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.all()
    return render(request, "index.html", {"tasks": tasks})

def add_task(request): 
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        title = request.POST.get("title")                                       

        if title:
            Task.objects.create(title=title)

    return redirect('index')

def delete_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect('login')

    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('index')

def update_task(request, task_id):
    if not request.user.is_authenticated:
        return redirect('login')
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')