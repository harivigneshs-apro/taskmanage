from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from tasks.models import Task


class Command(BaseCommand):
    help = 'Send email reminders for upcoming tasks'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Send reminders for tasks due within this many hours (default: 24)'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        now = timezone.now()
        reminder_time = now + timedelta(hours=hours)
        
        # Get tasks due within the specified time frame
        upcoming_tasks = Task.objects.filter(
            due_date__gte=now,
            due_date__lte=reminder_time,
            status__in=['pending', 'in_progress']
        ).select_related('created_by')
        
        sent_count = 0
        
        for task in upcoming_tasks:
            if task.created_by.email and task.created_by.userprofile.email_notifications:
                try:
                    subject = f'Task Reminder: {task.title}'
                    message = f"""
Hello {task.created_by.get_full_name() or task.created_by.username},

This is a reminder that your task "{task.title}" is due on {task.due_date.strftime('%B %d, %Y at %I:%M %p')}.

Task Details:
- Title: {task.title}
- Description: {task.description or 'No description'}
- Priority: {task.get_priority_display()}
- Status: {task.get_status_display()}
- Due Date: {task.due_date.strftime('%B %d, %Y at %I:%M %p')}

Please log in to your task manager to update the task status.

Best regards,
Task Manager System
                    """
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [task.created_by.email],
                        fail_silently=False,
                    )
                    sent_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Sent reminder for task "{task.title}" to {task.created_by.email}'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Failed to send reminder for task "{task.title}": {str(e)}'
                        )
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {sent_count} reminder emails')
        )
