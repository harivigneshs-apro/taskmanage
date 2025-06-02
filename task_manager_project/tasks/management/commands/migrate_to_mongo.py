from django.core.management.base import BaseCommand
from tasks.mongo_service import MongoMigrationService
import mongoengine


class Command(BaseCommand):
    help = 'Migrate data from SQLite to MongoDB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force migration even if MongoDB collections exist'
        )

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
            # Migrate tags first
            self.stdout.write('Migrating tags to MongoDB...')
            tag_count = MongoMigrationService.migrate_tags_to_mongo()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Migrated {tag_count} tags to MongoDB')
            )

            # Migrate tasks
            self.stdout.write('Migrating tasks to MongoDB...')
            task_count = MongoMigrationService.migrate_tasks_to_mongo()
            self.stdout.write(
                self.style.SUCCESS(f'✅ Migrated {task_count} tasks to MongoDB')
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 Migration completed successfully!'
                    f'\n📊 Total migrated: {tag_count} tags, {task_count} tasks'
                    f'\n🗄️  Data is now available in MongoDB'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Migration failed: {str(e)}')
            )
