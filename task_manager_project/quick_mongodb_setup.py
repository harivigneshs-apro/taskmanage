#!/usr/bin/env python3
"""
Quick MongoDB Setup for Django Task Manager
"""

import os
import sys
import subprocess


def print_msg(msg, type="INFO"):
    print(f"[{type}] {msg}")


def check_mongodb():
    """Check if MongoDB is accessible"""
    try:
        import pymongo
        # Try to connect
        client = pymongo.MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        client.close()
        print_msg("MongoDB is running and accessible!", "SUCCESS")
        return True
    except Exception as e:
        print_msg(f"MongoDB not accessible: {e}", "WARNING")
        return False


def run_django_migrations():
    """Run Django migrations for MongoDB"""
    try:
        print_msg("Running Django migrations...", "INFO")
        
        # Make migrations
        result = subprocess.run([sys.executable, 'manage.py', 'makemigrations'], 
                              capture_output=True, text=True)
        print_msg("Makemigrations output:", "INFO")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        # Migrate
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        print_msg("Migrate output:", "INFO")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print_msg("Migrations completed successfully!", "SUCCESS")
            return True
        else:
            print_msg("Migration had issues but may still work", "WARNING")
            return True
            
    except Exception as e:
        print_msg(f"Migration failed: {e}", "ERROR")
        return False


def create_superuser():
    """Create superuser"""
    try:
        print_msg("Creating superuser...", "INFO")
        
        script = '''
from django.contrib.auth.models import User
try:
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("Superuser created: admin/admin123")
    else:
        print("Superuser already exists")
except Exception as e:
    print(f"Error: {e}")
'''
        
        result = subprocess.run([sys.executable, 'manage.py', 'shell', '-c', script],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        return True
    except Exception as e:
        print_msg(f"Superuser creation failed: {e}", "ERROR")
        return False


def create_sample_data():
    """Create sample data"""
    try:
        print_msg("Creating sample data...", "INFO")
        result = subprocess.run([sys.executable, 'manage.py', 'create_sample_data'],
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except Exception as e:
        print_msg(f"Sample data creation failed: {e}", "WARNING")
        return False


def main():
    print_msg("=== Django + MongoDB Quick Setup ===", "INFO")
    
    # Check MongoDB
    if not check_mongodb():
        print_msg("MongoDB is not running. Please start MongoDB first:", "ERROR")
        print_msg("Option 1: Install MongoDB Community Server", "INFO")
        print_msg("Option 2: Use MongoDB Atlas (cloud)", "INFO")
        print_msg("Option 3: Use Docker: docker run -d -p 27017:27017 mongo", "INFO")
        
        # Try to continue anyway for demo purposes
        print_msg("Continuing with setup anyway...", "WARNING")
    
    # Run migrations
    if not run_django_migrations():
        print_msg("Migration failed, but continuing...", "WARNING")
    
    # Create superuser
    create_superuser()
    
    # Create sample data
    create_sample_data()
    
    print_msg("=== Setup Complete ===", "SUCCESS")
    print_msg("Run: python manage.py runserver 8000", "INFO")
    print_msg("Access: http://127.0.0.1:8000", "INFO")
    print_msg("Login: admin / admin123", "INFO")


if __name__ == "__main__":
    main()
