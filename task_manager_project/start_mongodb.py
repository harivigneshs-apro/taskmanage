#!/usr/bin/env python3
"""
Simple MongoDB Setup and Start Script
"""

import os
import sys
import subprocess
import time
import urllib.request
import zipfile
from pathlib import Path


def print_status(message, status="INFO"):
    """Print colored status messages"""
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m", 
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")


def download_mongodb():
    """Download MongoDB portable version"""
    print_status("Downloading MongoDB Community Server...", "INFO")
    
    mongodb_url = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.4.zip"
    
    try:
        urllib.request.urlretrieve(mongodb_url, "mongodb.zip")
        print_status("MongoDB downloaded successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Download failed: {e}", "ERROR")
        return False


def extract_mongodb():
    """Extract MongoDB"""
    print_status("Extracting MongoDB...", "INFO")
    
    try:
        with zipfile.ZipFile("mongodb.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Rename to simpler name
        if Path("mongodb-windows-x86_64-7.0.4").exists():
            if Path("mongodb").exists():
                import shutil
                shutil.rmtree("mongodb")
            Path("mongodb-windows-x86_64-7.0.4").rename("mongodb")
        
        # Clean up
        os.remove("mongodb.zip")
        
        print_status("MongoDB extracted successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Extraction failed: {e}", "ERROR")
        return False


def setup_mongodb():
    """Setup MongoDB directories"""
    print_status("Setting up MongoDB directories...", "INFO")
    
    try:
        # Create data directory
        data_dir = Path("data/db")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log directory
        log_dir = Path("data/log")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        print_status("MongoDB directories created!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Setup failed: {e}", "ERROR")
        return False


def start_mongodb():
    """Start MongoDB server"""
    print_status("Starting MongoDB server...", "INFO")
    
    mongod_path = Path("mongodb/bin/mongod.exe")
    
    if not mongod_path.exists():
        print_status("MongoDB executable not found!", "ERROR")
        return False
    
    try:
        # Start MongoDB
        cmd = [
            str(mongod_path),
            "--dbpath", "data/db",
            "--logpath", "data/log/mongodb.log",
            "--port", "27017"
        ]
        
        # Start in background
        process = subprocess.Popen(cmd, 
                                 creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
        
        print_status("MongoDB starting... (PID: {})".format(process.pid), "INFO")
        
        # Wait for MongoDB to start
        time.sleep(5)
        
        # Test connection
        if test_mongodb_connection():
            print_status("MongoDB started successfully!", "SUCCESS")
            return True
        else:
            print_status("MongoDB failed to start properly", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Failed to start MongoDB: {e}", "ERROR")
        return False


def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=3000)
        client.admin.command('ping')
        client.close()
        return True
    except Exception:
        return False


def main():
    """Main function"""
    print_status("=== MongoDB Setup for Django Task Manager ===", "INFO")
    
    # Check if MongoDB is already running
    if test_mongodb_connection():
        print_status("MongoDB is already running!", "SUCCESS")
        return True
    
    # Check if MongoDB is already downloaded
    if not Path("mongodb/bin/mongod.exe").exists():
        print_status("MongoDB not found. Downloading...", "INFO")
        
        if not download_mongodb():
            return False
        
        if not extract_mongodb():
            return False
    
    # Setup directories
    if not setup_mongodb():
        return False
    
    # Start MongoDB
    if not start_mongodb():
        return False
    
    print_status("=== MongoDB Setup Complete! ===", "SUCCESS")
    print_status("MongoDB is running on localhost:27017", "INFO")
    print_status("You can now run: python manage.py migrate", "INFO")
    print_status("Then: python manage.py runserver", "INFO")
    
    return True


if __name__ == "__main__":
    if main():
        print_status("Setup successful! MongoDB is ready.", "SUCCESS")
    else:
        print_status("Setup failed. Please check the errors above.", "ERROR")
