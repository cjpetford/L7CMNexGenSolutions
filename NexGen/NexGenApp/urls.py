"""
URL configuration for NexGen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NexGen import views

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # User page
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Home page
    path('home/', views.home, name='home'),

    # Tasks
    path('create/', views.create_task, name='create_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('progress/<int:pk>/', views.update_progress, name='update_progress'),
]