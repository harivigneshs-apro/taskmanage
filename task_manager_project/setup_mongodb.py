#!/usr/bin/env python3
"""
MongoDB Setup Script for Task Manager
This script helps set up MongoDB for the Django Task Manager application.
"""

import os
import sys
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path


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


def check_mongodb_installed():
    """Check if MongoDB is already installed"""
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_status("MongoDB is already installed!", "SUCCESS")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return False


def check_mongodb_running():
    """Check if MongoDB is running"""
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        client.close()
        print_status("MongoDB is running!", "SUCCESS")
        return True
    except Exception:
        return False


def install_mongodb_windows():
    """Install MongoDB on Windows"""
    print_status("Installing MongoDB on Windows...", "INFO")
    
    # MongoDB Community Server download URL
    mongodb_url = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-6.0.8.zip"
    download_path = "mongodb.zip"
    
    try:
        print_status("Downloading MongoDB...", "INFO")
        urllib.request.urlretrieve(mongodb_url, download_path)
        
        print_status("Extracting MongoDB...", "INFO")
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Move MongoDB to a standard location
        mongodb_dir = Path("mongodb-windows-x86_64-6.0.8")
        target_dir = Path("C:/mongodb")
        
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        shutil.move(str(mongodb_dir), str(target_dir))
        
        # Create data directory
        data_dir = Path("C:/data/db")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Clean up
        os.remove(download_path)
        
        print_status("MongoDB installed successfully!", "SUCCESS")
        print_status("MongoDB installed at: C:/mongodb", "INFO")
        print_status("Data directory created at: C:/data/db", "INFO")
        
        return True
        
    except Exception as e:
        print_status(f"Failed to install MongoDB: {e}", "ERROR")
        return False


def start_mongodb():
    """Start MongoDB server"""
    system = platform.system().lower()
    
    if system == "windows":
        mongodb_path = Path("C:/mongodb/bin/mongod.exe")
        if not mongodb_path.exists():
            print_status("MongoDB not found. Please install MongoDB first.", "ERROR")
            return False
        
        try:
            print_status("Starting MongoDB server...", "INFO")
            # Start MongoDB in background
            subprocess.Popen([str(mongodb_path), "--dbpath", "C:/data/db"],
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
            
            # Wait a moment for startup
            import time
            time.sleep(3)
            
            if check_mongodb_running():
                print_status("MongoDB started successfully!", "SUCCESS")
                return True
            else:
                print_status("MongoDB failed to start", "ERROR")
                return False
                
        except Exception as e:
            print_status(f"Failed to start MongoDB: {e}", "ERROR")
            return False
    
    else:
        print_status("Auto-start only supported on Windows. Please start MongoDB manually.", "WARNING")
        return False


def setup_django_mongodb():
    """Set up Django with MongoDB"""
    try:
        print_status("Setting up Django with MongoDB...", "INFO")
        
        # Run Django migrations
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Django migrations completed!", "SUCCESS")
        else:
            print_status(f"Migration warning: {result.stderr}", "WARNING")
        
        # Create superuser if needed
        print_status("Creating superuser...", "INFO")
        create_superuser_script = """
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"""
        
        result = subprocess.run([sys.executable, 'manage.py', 'shell', '-c', create_superuser_script],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print_status("Superuser setup completed!", "SUCCESS")
        
        return True
        
    except Exception as e:
        print_status(f"Django setup failed: {e}", "ERROR")
        return False


def main():
    """Main setup function"""
    print_status("=== Django + MongoDB Setup ===", "INFO")
    
    # Check if MongoDB is already running
    if check_mongodb_running():
        print_status("MongoDB is already running. Proceeding with Django setup...", "SUCCESS")
        setup_django_mongodb()
        return
    
    # Check if MongoDB is installed
    if not check_mongodb_installed():
        if platform.system().lower() == "windows":
            print_status("MongoDB not found. Installing...", "INFO")
            if not install_mongodb_windows():
                print_status("MongoDB installation failed. Please install manually.", "ERROR")
                return
        else:
            print_status("Please install MongoDB manually for your system:", "WARNING")
            print_status("Ubuntu/Debian: sudo apt-get install mongodb", "INFO")
            print_status("macOS: brew install mongodb/brew/mongodb-community", "INFO")
            return
    
    # Start MongoDB
    if start_mongodb():
        # Setup Django
        setup_django_mongodb()
        
        print_status("=== Setup Complete! ===", "SUCCESS")
        print_status("You can now run: python manage.py runserver", "INFO")
        print_status("Access your app at: http://127.0.0.1:8000", "INFO")
        print_status("Admin panel: http://127.0.0.1:8000/admin", "INFO")
        print_status("Login: admin / admin123", "INFO")
    else:
        print_status("Setup incomplete. Please start MongoDB manually and run Django migrations.", "WARNING")


if __name__ == "__main__":
    main()
