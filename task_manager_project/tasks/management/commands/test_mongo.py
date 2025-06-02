from django.core.management.base import BaseCommand
from tasks.mongo_models import MongoTask, MongoTag
from tasks.mongo_service import MongoTaskService, MongoTagService
from django.contrib.auth.models import User
import mongoengine
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Test MongoDB integration and create sample data'

    def handle(self, *args, **options):
        try:
            # Test MongoDB connection
            mongoengine.connection.get_connection()
            self.stdout.write(self.style.SUCCESS('✅ MongoDB connection successful'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ MongoDB connection failed: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('Make sure MongoDB is running on localhost:27017')
            )
            return

        try:
            # Get admin user
            admin_user = User.objects.get(username='admin')
            
            # Test tag creation
            self.stdout.write('Testing MongoDB tag creation...')
            tag = MongoTagService.create_tag(admin_user, 'MongoDB Test', '#ff6b6b')
            self.stdout.write(f'✅ Created tag: {tag.name}')
            
            # Test task creation
            self.stdout.write('Testing MongoDB task creation...')
            due_date = datetime.now() + timedelta(days=3)
            task = MongoTaskService.create_task(
                user=admin_user,
                title='MongoDB Integration Test',
                description='Testing MongoDB integration with the task management system',
                due_date=due_date,
                priority='high',
                tag_names=['MongoDB Test']
            )
            self.stdout.write(f'✅ Created task: {task.title}')
            
            # Test comment addition
            self.stdout.write('Testing comment addition...')
            MongoTaskService.add_comment(
                task.id, 
                admin_user, 
                'This is a test comment for MongoDB integration'
            )
            self.stdout.write('✅ Added comment to task')
            
            # Test statistics
            self.stdout.write('Testing statistics retrieval...')
            stats = MongoTaskService.get_task_statistics(admin_user)
            self.stdout.write(f'✅ Statistics: {stats}')
            
            # Display MongoDB data
            self.stdout.write('\n📊 MongoDB Data Summary:')
            mongo_tasks = MongoTask.objects(created_by_id=admin_user.id)
            mongo_tags = MongoTag.objects(created_by_id=admin_user.id)
            
            self.stdout.write(f'📋 Tasks in MongoDB: {mongo_tasks.count()}')
            self.stdout.write(f'🏷️  Tags in MongoDB: {mongo_tags.count()}')
            
            if mongo_tasks:
                self.stdout.write('\n📋 Recent MongoDB Tasks:')
                for task in mongo_tasks.order_by('-created_at')[:5]:
                    self.stdout.write(f'  • {task.title} ({task.status})')
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 MongoDB integration test completed successfully!'
                    '\n🗄️  MongoDB is ready for use!'
                )
            )

        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Admin user not found. Please create a superuser first.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Test failed: {str(e)}')
            )
