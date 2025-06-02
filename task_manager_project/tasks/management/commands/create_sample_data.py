from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, Tag, TaskComment
import random


class Command(BaseCommand):
    help = 'Create sample data for demonstration'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )

        # Create sample tags
        tag_data = [
            {'name': 'Work', 'color': '#007bff'},
            {'name': 'Personal', 'color': '#28a745'},
            {'name': 'Urgent', 'color': '#dc3545'},
            {'name': 'Meeting', 'color': '#ffc107'},
            {'name': 'Project', 'color': '#17a2b8'},
            {'name': 'Study', 'color': '#6f42c1'},
        ]

        tags = []
        for tag_info in tag_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_info['name'],
                created_by=admin_user,
                defaults={'color': tag_info['color']}
            )
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Create sample tasks
        task_data = [
            {
                'title': 'Complete Project Proposal',
                'description': 'Finish the quarterly project proposal for the new client management system.',
                'priority': 'high',
                'status': 'in_progress',
                'days_offset': 3,
                'tags': ['Work', 'Project']
            },
            {
                'title': 'Team Meeting - Sprint Planning',
                'description': 'Weekly sprint planning meeting with the development team.',
                'priority': 'medium',
                'status': 'pending',
                'days_offset': 1,
                'tags': ['Work', 'Meeting']
            },
            {
                'title': 'Buy Groceries',
                'description': 'Weekly grocery shopping - milk, bread, vegetables, fruits.',
                'priority': 'low',
                'status': 'pending',
                'days_offset': 2,
                'tags': ['Personal']
            },
            {
                'title': 'Submit Tax Documents',
                'description': 'Gather and submit all required tax documents before deadline.',
                'priority': 'urgent',
                'status': 'pending',
                'days_offset': 7,
                'tags': ['Personal', 'Urgent']
            },
            {
                'title': 'Code Review - Authentication Module',
                'description': 'Review the new authentication module implementation.',
                'priority': 'high',
                'status': 'completed',
                'days_offset': -2,
                'tags': ['Work', 'Project']
            },
            {
                'title': 'Study Django Advanced Features',
                'description': 'Learn about Django signals, middleware, and custom management commands.',
                'priority': 'medium',
                'status': 'in_progress',
                'days_offset': 5,
                'tags': ['Study', 'Personal']
            },
            {
                'title': 'Client Presentation Preparation',
                'description': 'Prepare slides and demo for the upcoming client presentation.',
                'priority': 'high',
                'status': 'pending',
                'days_offset': 4,
                'tags': ['Work', 'Meeting']
            },
            {
                'title': 'Database Backup',
                'description': 'Perform weekly database backup and verify integrity.',
                'priority': 'medium',
                'status': 'completed',
                'days_offset': -1,
                'tags': ['Work']
            },
        ]

        for task_info in task_data:
            due_date = timezone.now() + timedelta(days=task_info['days_offset'])
            
            task, created = Task.objects.get_or_create(
                title=task_info['title'],
                created_by=admin_user,
                defaults={
                    'description': task_info['description'],
                    'priority': task_info['priority'],
                    'status': task_info['status'],
                    'due_date': due_date,
                }
            )
            
            if created:
                # Add tags to task
                for tag_name in task_info['tags']:
                    tag = next((t for t in tags if t.name == tag_name), None)
                    if tag:
                        task.tags.add(tag)
                
                # Add sample comments for some tasks
                if random.choice([True, False]):
                    TaskComment.objects.create(
                        task=task,
                        user=admin_user,
                        comment=f"Working on this task. Current progress looks good."
                    )
                
                self.stdout.write(f'Created task: {task.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for demonstration!')
        )
