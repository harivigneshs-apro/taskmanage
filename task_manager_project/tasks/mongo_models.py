from mongoengine import Document, EmbeddedDocument, fields
from django.contrib.auth.models import User
from datetime import datetime


class MongoUserProfile(Document):
    user_id = fields.IntField(required=True, unique=True)
    username = fields.StringField(max_length=150, required=True)
    email = fields.EmailField()
    phone_number = fields.StringField(max_length=15)
    date_of_birth = fields.DateTimeField()
    profile_picture = fields.StringField()  # Store file path
    email_notifications = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'user_profiles',
        'indexes': ['user_id', 'username']
    }

    def __str__(self):
        return f"{self.username}'s Profile"


class MongoTag(Document):
    name = fields.StringField(max_length=50, required=True)
    color = fields.StringField(max_length=7, default='#007bff')
    created_by_id = fields.IntField(required=True)
    created_by_username = fields.StringField(max_length=150)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'tags',
        'indexes': ['created_by_id', 'name']
    }

    def __str__(self):
        return self.name


class MongoTaskComment(EmbeddedDocument):
    user_id = fields.IntField(required=True)
    username = fields.StringField(max_length=150, required=True)
    comment = fields.StringField(required=True)
    created_at = fields.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Comment by {self.username}"


class MongoTask(Document):
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

    title = fields.StringField(max_length=200, required=True)
    description = fields.StringField()
    due_date = fields.DateTimeField(required=True)
    priority = fields.StringField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = fields.StringField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Tags as list of tag IDs and names for easy querying
    tag_ids = fields.ListField(fields.ObjectIdField())
    tag_names = fields.ListField(fields.StringField(max_length=50))
    
    # User information
    created_by_id = fields.IntField(required=True)
    created_by_username = fields.StringField(max_length=150, required=True)
    assigned_to_id = fields.IntField()
    assigned_to_username = fields.StringField(max_length=150)
    
    # Timestamps
    created_at = fields.DateTimeField(default=datetime.now)
    updated_at = fields.DateTimeField(default=datetime.now)
    completed_at = fields.DateTimeField()
    
    # Comments as embedded documents
    comments = fields.ListField(fields.EmbeddedDocumentField(MongoTaskComment))

    meta = {
        'collection': 'tasks',
        'indexes': [
            'created_by_id',
            'status',
            'priority',
            'due_date',
            'tag_names',
            ('created_by_id', 'status'),
            ('created_by_id', 'due_date')
        ]
    }

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = datetime.now()
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        return self.due_date < datetime.now() and self.status != 'completed'

    @property
    def days_until_due(self):
        delta = self.due_date - datetime.now()
        return delta.days

    def get_priority_display(self):
        priority_dict = dict(self.PRIORITY_CHOICES)
        return priority_dict.get(self.priority, self.priority)

    def get_status_display(self):
        status_dict = dict(self.STATUS_CHOICES)
        return status_dict.get(self.status, self.status)


class MongoTaskReminder(Document):
    task_id = fields.ObjectIdField(required=True)
    task_title = fields.StringField(max_length=200, required=True)
    user_id = fields.IntField(required=True)
    user_email = fields.EmailField(required=True)
    reminder_time = fields.DateTimeField(required=True)
    is_sent = fields.BooleanField(default=False)
    created_at = fields.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'task_reminders',
        'indexes': ['task_id', 'user_id', 'reminder_time', 'is_sent']
    }

    def __str__(self):
        return f"Reminder for {self.task_title}"
