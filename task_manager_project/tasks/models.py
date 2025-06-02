from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        ordering = ['name']


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    tags = models.ManyToManyField(Tag, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.due_date < timezone.now() and self.status != 'completed'

    @property
    def days_until_due(self):
        delta = self.due_date - timezone.now()
        return delta.days

    class Meta:
        db_table = 'tasks'
        ordering = ['-created_at']


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"

    class Meta:
        db_table = 'task_comments'
        ordering = ['-created_at']


class TaskReminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.task.title}"

    class Meta:
        db_table = 'task_reminders'
        ordering = ['reminder_time']
