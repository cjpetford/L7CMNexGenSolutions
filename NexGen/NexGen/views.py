from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Task
from .forms import TaskForm

# Hardcoded users demo
HARDCODED_USERS = {
    'admin': {'password': 'adminpass', 'is_superuser': True},
    'staff': {'password': 'staffpass', 'is_superuser': False},
}

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_info = HARDCODED_USERS.get(username)
        if user_info and user_info['password'] == password:
            # Get or create the User object
            user, created = User.objects.get_or_create(username=username)
            user.is_superuser = user_info['is_superuser']
            user.is_staff = True
            user.set_unusable_password()  # no real password login via Django admin
            user.save()
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


@login_required
def home(request):
    tasks_todo = Task.objects.filter(category='todo')
    tasks_inprogress = Task.objects.filter(category='inprogress')
    tasks_completed = Task.objects.filter(category='completed')
    return render(request, 'home.html', {
        'tasks_todo': tasks_todo,
        'tasks_inprogress': tasks_inprogress,
        'tasks_completed': tasks_completed,
    })


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def create_task(request):
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


@login_required
def update_task(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'task_form.html', {'form': form})


@login_required
def delete_task(request, pk):
    if request.user.is_superuser:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
    return redirect('home')


@login_required
def update_progress(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user.is_superuser:
        # Admins don't update progress like this
        return redirect('home')
    if task.progress < 100:
        task.progress += 10
        if task.progress >= 100:
            task.progress = 100
            task.category = 'completed'
        elif task.progress > 0 and task.category == 'todo':
            task.category = 'inprogress'
        task.save()
    return redirect('home')
