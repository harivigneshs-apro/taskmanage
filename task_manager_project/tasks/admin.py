from django.contrib import admin
from .models import Task, Tag, TaskComment, TaskReminder


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'due_date', 'created_by', 'is_overdue']
    list_filter = ['priority', 'status', 'created_by', 'due_date', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags']
    date_hierarchy = 'due_date'

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'


@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['comment', 'task__title']


@admin.register(TaskReminder)
class TaskReminderAdmin(admin.ModelAdmin):
    list_display = ['task', 'reminder_time', 'is_sent', 'created_at']
    list_filter = ['is_sent', 'reminder_time', 'created_at']
    search_fields = ['task__title']
