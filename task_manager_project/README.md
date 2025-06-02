# 📋 Task Management System

A comprehensive web-based task management application built with **Django Backend** and **MongoDB Database**, featuring user authentication, task CRUD operations, categorization, status tracking, and email notifications.

## 🏗️ **ARCHITECTURE**
- **Backend**: Django 3.2.13 (Web Framework)
- **Database**: MongoDB (NoSQL Database)
- **ORM**: Djongo (Django + MongoDB integration)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

## 🚀 **QUICK START FOR PRESENTATION**

### **Option 1: Current Setup (SQLite - Ready Now)**
```bash
cd "C:\Users\Hari Vignesh S\task_manager_project"
python manage.py runserver 8000
```

### **Option 2: Switch to MongoDB**
```bash
cd "C:\Users\Hari Vignesh S\task_manager_project"
# First install and start MongoDB, then:
python switch_to_mongodb.py
python manage.py runserver 8000
```

### **Option 3: Automatic MongoDB Setup**
```bash
cd "C:\Users\Hari Vignesh S\task_manager_project"
python setup_mongodb.py
python manage.py runserver 8000
```

### **Option 4: Windows Batch File**
```bash
cd "C:\Users\Hari Vignesh S\task_manager_project"
run_with_mongodb.bat
```

### **Access URLs:**
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### **Login Credentials:**
- **Username**: `admin`
- **Password**: `admin123`

---

## ✅ **IMPLEMENTED FEATURES**

### 1. **User Authentication System**
- ✅ User registration with email and password
- ✅ User login/logout functionality
- ✅ User profile management
- ✅ Password reset functionality

### 2. **Task Management (CRUD Operations)**
- ✅ Create tasks with title, description, due date, priority
- ✅ Read/View tasks in list and detail views
- ✅ Update/Edit task properties and status
- ✅ Delete tasks with confirmation

### 3. **Task Properties & Features**
- ✅ Title and description
- ✅ Due date and time
- ✅ Priority levels (Low, Medium, High, Urgent)
- ✅ Status tracking (Pending, In Progress, Completed, Cancelled)
- ✅ Task categorization with colored tags

### 4. **Task Organization**
- ✅ Tag system for categorization (work, personal, etc.)
- ✅ Filter tasks by priority, status, tags, date range
- ✅ Search functionality
- ✅ Task sorting and pagination

### 5. **Status Management**
- ✅ Mark tasks as complete/in-progress
- ✅ Quick status update buttons
- ✅ Edit task details
- ✅ Task progress tracking

### 6. **Notifications & Reminders**
- ✅ Email notification system
- ✅ Automated reminder emails for upcoming tasks
- ✅ Customizable reminder timing
- ✅ Email preferences in user profile

---

## 🎯 **DEMO FEATURES FOR PRESENTATION**

### **Dashboard Overview**
- Task statistics (total, completed, pending, overdue)
- Recent tasks display
- Upcoming tasks (next 7 days)
- Visual progress indicators

### **Task Management**
- Create new tasks with all properties
- Filter and search existing tasks
- Quick status updates
- Task detail view with comments

### **Tag System**
- Create colored tags for organization
- Assign multiple tags to tasks
- Filter tasks by tags

### **Email Notifications**
```bash
# Demo command to send reminders
python manage.py send_reminders --hours 24
```

---

## 🛠 **TECHNICAL STACK**

- **Backend**: Django 3.2.13 (Web Framework)
- **Database**: MongoDB (NoSQL Database)
- **ORM**: Djongo (Django + MongoDB Bridge)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Forms**: Django Crispy Forms
- **Icons**: Font Awesome 6
- **Email**: Django Email Backend

## 🗄️ **MONGODB INTEGRATION**

### **Why MongoDB?**
- **NoSQL Flexibility**: Perfect for task management with varying data structures
- **Scalability**: Handles large amounts of task data efficiently
- **JSON-like Documents**: Natural fit for web applications
- **Rich Queries**: Complex filtering and searching capabilities

### **Django + MongoDB Setup:**
- **Djongo**: Translates Django ORM to MongoDB queries
- **Native MongoDB**: Direct MongoDB operations when needed
- **Hybrid Approach**: Best of both Django and MongoDB worlds

### **Data Structure in MongoDB:**
```javascript
// Tasks Collection
{
  "_id": ObjectId("..."),
  "title": "Complete Project",
  "description": "Finish the task management system",
  "due_date": ISODate("2024-06-15T10:00:00Z"),
  "priority": "high",
  "status": "in_progress",
  "tags": ["work", "project"],
  "created_by": 1,
  "created_at": ISODate("2024-06-01T08:00:00Z")
}
```

---

## 📊 **SAMPLE DATA INCLUDED**

The system comes pre-loaded with:
- ✅ 8 sample tasks with various priorities and statuses
- ✅ 6 colored tags (Work, Personal, Urgent, Meeting, Project, Study)
- ✅ Task comments for demonstration
- ✅ Admin user account ready to use

---

## 🎬 **PRESENTATION FLOW**

1. **Start**: `python manage.py runserver 8000`
2. **Login**: Use admin/admin123 credentials
3. **Dashboard**: Show task statistics and overview
4. **Create Task**: Demonstrate task creation with all features
5. **Task List**: Show filtering, search, and management
6. **Tags**: Demonstrate tag creation and organization
7. **Email**: Run `python manage.py send_reminders` command
8. **Profile**: Show user profile management

---

## 🔧 **ADDITIONAL COMMANDS**

```bash
# Create more sample data
python manage.py create_sample_data

# Send email reminders
python manage.py send_reminders --hours 24

# Access admin panel
# Go to: http://127.0.0.1:8000/admin/

# Create new superuser (if needed)
python manage.py createsuperuser
```

---

## 🎉 **READY FOR PRESENTATION!**

Your Task Management System is fully functional with all requested features implemented. Simply run the command above and start demonstrating!

**Features Checklist:**
- ✅ User registration and login
- ✅ Task CRUD operations
- ✅ Task properties (title, description, due date, priority)
- ✅ Task categorization (tags)
- ✅ Status tracking and editing
- ✅ Email notifications and reminders
- ✅ Modern responsive UI
- ✅ Sample data for demonstration
