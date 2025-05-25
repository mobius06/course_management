# Course Management System

A Python-based course management system with a GUI interface, built using tkinter and PostgreSQL.

## Features

- User Authentication (Admin, Teacher, Student roles)
- Course Management
- User Management
- Course Enrollment
- Course Offerings Management

## Prerequisites

- Python 3.x
- PostgreSQL
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd course_management
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
   - Create a new database named 'course_management'
   - Run the SQL commands in `database_setup.sql` to create the necessary tables

4. Configure the database connection:
   - Open `config.py`
   - Update the DB_CONFIG with your PostgreSQL credentials:
```python
DB_CONFIG = {
    'dbname': 'course_management',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432'
}
```

## Running the Application

```bash
python main.py
```

## Default Test Accounts

### Admin
- Username: `admin`
- Password: `admin123`
- Role: admin

### Teachers
- Username: `teacher1`, Password: `teacher1_pass`
- Username: `teacher2`, Password: `teacher2_pass`
- Username: `teacher3`, Password: `teacher3_pass`
- Username: `teacher4`, Password: `teacher4_pass`

### Students
- Username: `student1`, Password: `student1_pass`
- Username: `student2`, Password: `student2_pass`
- Username: `student3`, Password: `student3_pass`

## Project Structure

- `main.py`: Main application entry point
- `database.py`: Database connection and operations
- `config.py`: Configuration settings
- `gui/`: GUI components
  - `student_interface.py`: Student interface
  - `teacher_interface.py`: Teacher interface
  - `course_management.py`: Course management interface
  - `user_management.py`: User management interface

## Features by Role

### Admin
- Full user management
- Full course management
- System-wide access

### Teacher
- View teaching courses
- Manage course offerings
- Add/Edit/Delete course offerings

### Student
- View available courses
- View enrolled courses
- Enroll in courses
- Drop courses 