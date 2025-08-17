from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('todo', 'To Do'),
        ('inprogress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='todo')
    progress = models.IntegerField(default=0)  # progress from 0 to 100 (%)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
