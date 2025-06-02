from django import forms
from django.contrib.auth.models import User
from .models import Task, Tag, TaskComment


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status', 'tags', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter task title...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(created_by=user)
            self.fields['assigned_to'].queryset = User.objects.all()


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'name': forms.TextInput(attrs={'placeholder': 'Enter tag name...'}),
        }


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }


class TaskFilterForm(forms.Form):
    PRIORITY_CHOICES = [('', 'All Priorities')] + Task.PRIORITY_CHOICES
    STATUS_CHOICES = [('', 'All Statuses')] + Task.STATUS_CHOICES
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search tasks...'})
    )
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False)
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    due_date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    due_date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(created_by=user)
