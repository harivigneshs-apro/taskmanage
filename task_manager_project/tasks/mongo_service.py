from .mongo_models import MongoTask, MongoTag, MongoTaskComment, MongoUserProfile
from django.contrib.auth.models import User
from datetime import datetime
from bson import ObjectId


class MongoTaskService:
    """Service layer for MongoDB task operations"""
    
    @staticmethod
    def create_task(user, title, description, due_date, priority='medium', status='pending', tag_names=None):
        """Create a new task in MongoDB"""
        task = MongoTask(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
            created_by_id=user.id,
            created_by_username=user.username,
            tag_names=tag_names or []
        )
        task.save()
        return task
    
    @staticmethod
    def get_user_tasks(user, status=None, priority=None, tag_names=None):
        """Get tasks for a specific user with optional filters"""
        query = {'created_by_id': user.id}
        
        if status:
            query['status'] = status
        if priority:
            query['priority'] = priority
        if tag_names:
            query['tag_names__in'] = tag_names
            
        return MongoTask.objects(**query).order_by('-created_at')
    
    @staticmethod
    def update_task_status(task_id, status):
        """Update task status"""
        try:
            task = MongoTask.objects(id=ObjectId(task_id)).first()
            if task:
                task.status = status
                task.save()
                return True
        except:
            pass
        return False
    
    @staticmethod
    def add_comment(task_id, user, comment_text):
        """Add comment to task"""
        try:
            task = MongoTask.objects(id=ObjectId(task_id)).first()
            if task:
                comment = MongoTaskComment(
                    user_id=user.id,
                    username=user.username,
                    comment=comment_text
                )
                task.comments.append(comment)
                task.save()
                return True
        except:
            pass
        return False
    
    @staticmethod
    def get_task_statistics(user):
        """Get task statistics for dashboard"""
        user_tasks = MongoTask.objects(created_by_id=user.id)
        
        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(status='completed').count()
        pending_tasks = user_tasks.filter(status='pending').count()
        in_progress_tasks = user_tasks.filter(status='in_progress').count()
        
        # Overdue tasks
        overdue_tasks = user_tasks.filter(
            due_date__lt=datetime.now(),
            status__in=['pending', 'in_progress']
        ).count()
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'in_progress_tasks': in_progress_tasks,
            'overdue_tasks': overdue_tasks
        }


class MongoTagService:
    """Service layer for MongoDB tag operations"""
    
    @staticmethod
    def create_tag(user, name, color='#007bff'):
        """Create a new tag"""
        tag = MongoTag(
            name=name,
            color=color,
            created_by_id=user.id,
            created_by_username=user.username
        )
        tag.save()
        return tag
    
    @staticmethod
    def get_user_tags(user):
        """Get all tags for a user"""
        return MongoTag.objects(created_by_id=user.id).order_by('name')
    
    @staticmethod
    def get_tag_with_task_count(user):
        """Get tags with task count"""
        tags = MongoTag.objects(created_by_id=user.id)
        tag_data = []
        
        for tag in tags:
            task_count = MongoTask.objects(
                created_by_id=user.id,
                tag_names=tag.name
            ).count()
            
            tag_data.append({
                'tag': tag,
                'task_count': task_count
            })
        
        return tag_data


class MongoUserService:
    """Service layer for MongoDB user profile operations"""
    
    @staticmethod
    def create_or_update_profile(user, **profile_data):
        """Create or update user profile in MongoDB"""
        profile = MongoUserProfile.objects(user_id=user.id).first()
        
        if not profile:
            profile = MongoUserProfile(
                user_id=user.id,
                username=user.username,
                email=user.email
            )
        
        # Update profile data
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        profile.updated_at = datetime.now()
        profile.save()
        return profile
    
    @staticmethod
    def get_profile(user):
        """Get user profile from MongoDB"""
        return MongoUserProfile.objects(user_id=user.id).first()


# Utility functions for data migration
class MongoMigrationService:
    """Service for migrating data between SQLite and MongoDB"""
    
    @staticmethod
    def migrate_tasks_to_mongo():
        """Migrate tasks from SQLite to MongoDB"""
        from .models import Task, Tag
        
        migrated_count = 0
        
        for task in Task.objects.all():
            # Get tag names
            tag_names = [tag.name for tag in task.tags.all()]
            
            mongo_task = MongoTask(
                title=task.title,
                description=task.description,
                due_date=task.due_date,
                priority=task.priority,
                status=task.status,
                created_by_id=task.created_by.id,
                created_by_username=task.created_by.username,
                tag_names=tag_names,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed_at=task.completed_at
            )
            
            # Migrate comments
            for comment in task.comments.all():
                mongo_comment = MongoTaskComment(
                    user_id=comment.user.id,
                    username=comment.user.username,
                    comment=comment.comment,
                    created_at=comment.created_at
                )
                mongo_task.comments.append(mongo_comment)
            
            mongo_task.save()
            migrated_count += 1
        
        return migrated_count
    
    @staticmethod
    def migrate_tags_to_mongo():
        """Migrate tags from SQLite to MongoDB"""
        from .models import Tag
        
        migrated_count = 0
        
        for tag in Tag.objects.all():
            mongo_tag = MongoTag(
                name=tag.name,
                color=tag.color,
                created_by_id=tag.created_by.id,
                created_by_username=tag.created_by.username,
                created_at=tag.created_at
            )
            mongo_tag.save()
            migrated_count += 1
        
        return migrated_count
