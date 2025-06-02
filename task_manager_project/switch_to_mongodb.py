#!/usr/bin/env python3
"""
MongoDB Switch Script for Task Manager
This script switches the database from SQLite to MongoDB
"""

import os
import sys
import subprocess
import re


def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",  # Blue
        "SUCCESS": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "RESET": "\033[0m"  # Reset
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")


def check_mongodb_running():
    """Check if MongoDB is running"""
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        client.close()
        return True
    except Exception:
        return False


def switch_to_mongodb():
    """Switch Django settings to use MongoDB"""
    settings_file = 'task_manager_project/settings.py'
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        # Comment out SQLite configuration
        sqlite_pattern = r"DATABASES = \{\s*'default': \{\s*'ENGINE': 'django\.db\.backends\.sqlite3',\s*'NAME': BASE_DIR / 'db\.sqlite3',\s*\}\s*\}"
        sqlite_replacement = '''# SQLite Database (commented out for MongoDB)
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
"""'''
        
        content = re.sub(sqlite_pattern, sqlite_replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Uncomment MongoDB configuration
        mongodb_pattern = r'# MongoDB Configuration \(Ready for production\)\s*# Uncomment below and comment SQLite above to use MongoDB\s*"""\s*DATABASES = \{\s*\'default\': \{\s*\'ENGINE\': \'djongo\',\s*\'NAME\': \'task_manager_db\',\s*\'CLIENT\': \{\s*\'host\': \'mongodb://localhost:27017\',\s*\}\s*\}\s*\}\s*"""'
        
        mongodb_replacement = '''# MongoDB Configuration (Active)
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'task_manager_db',
        'CLIENT': {
            'host': 'mongodb://localhost:27017',
        }
    }
}'''
        
        content = re.sub(mongodb_pattern, mongodb_replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Write back to file
        with open(settings_file, 'w') as f:
            f.write(content)
        
        print_status("Settings updated to use MongoDB", "SUCCESS")
        return True
        
    except Exception as e:
        print_status(f"Failed to update settings: {e}", "ERROR")
        return False


def run_mongodb_migrations():
    """Run Django migrations for MongoDB"""
    try:
        print_status("Running Django migrations for MongoDB...", "INFO")
        
        # Make migrations
        result = subprocess.run([sys.executable, 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print_status(f"Make migrations warning: {result.stderr}", "WARNING")
        
        # Run migrations
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_status("MongoDB migrations completed successfully!", "SUCCESS")
        else:
            print_status(f"Migration error: {result.stderr}", "ERROR")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"Migration failed: {e}", "ERROR")
        return False


def create_superuser():
    """Create superuser for MongoDB"""
    try:
        print_status("Creating superuser for MongoDB...", "INFO")
        
        create_superuser_script = """
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"""
        
        result = subprocess.run([sys.executable, 'manage.py', 'shell', '-c', create_superuser_script],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Superuser setup completed!", "SUCCESS")
            return True
        else:
            print_status(f"Superuser creation failed: {result.stderr}", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Superuser creation failed: {e}", "ERROR")
        return False


def main():
    """Main function"""
    print_status("=== Switching to MongoDB ===", "INFO")
    
    # Check if MongoDB is running
    if not check_mongodb_running():
        print_status("MongoDB is not running!", "ERROR")
        print_status("Please start MongoDB first:", "INFO")
        print_status("Windows: mongod --dbpath C:\\data\\db", "INFO")
        print_status("Linux/Mac: sudo systemctl start mongod", "INFO")
        return
    
    print_status("MongoDB is running ✅", "SUCCESS")
    
    # Switch to MongoDB
    if not switch_to_mongodb():
        return
    
    # Run migrations
    if not run_mongodb_migrations():
        return
    
    # Create superuser
    if not create_superuser():
        return
    
    print_status("=== MongoDB Switch Complete! ===", "SUCCESS")
    print_status("Your Django app is now using MongoDB", "INFO")
    print_status("Run: python manage.py runserver", "INFO")
    print_status("Access: http://127.0.0.1:8000", "INFO")
    print_status("Login: admin / admin123", "INFO")


if __name__ == "__main__":
    main()
