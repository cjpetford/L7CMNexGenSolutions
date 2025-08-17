from django import forms
from .models import Task

# Admin uses this form to create/edit tasks fully
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'progress']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Staff just need to update progress — but we handle that in views, so this can be minimal
class ProgressForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['progress']
