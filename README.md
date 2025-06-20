# Course Management System

A desktop course management system built with Python (Tkinter) and PostgreSQL, designed for educational institutions to manage courses, students, teachers, and enrollments.

## Features

- User authentication with role-based access (Admin, Teacher, Student)
- Department management
- Course management with ECTS credits and course types
- Semester management
- Course offering management
- Student enrollment system
- Teacher assignment to courses

## Prerequisites

- **Python 3.8 or higher**
- **PostgreSQL 12 or higher**
- **pip** (Python package manager)

## Installation & Setup

### 1. Install Python and pip
- Download and install Python from [python.org](https://www.python.org/downloads/).
- Make sure to check "Add Python to PATH" during installation.
- pip is included with modern Python versions.

### 2. Install PostgreSQL
- Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/).
- During installation, set a password for the `postgres` superuser and remember it.

### 3. Clone the repository
```bash
git clone <repository-url>
cd course_management
```

### 4. Install required Python packages
```bash
pip install -r requirements.txt
```

### 5. Set up the PostgreSQL database
- Open a terminal/command prompt and run:
```bash
psql -U postgres
```
- Create the database and user (replace `your_username` and `your_password`):
```sql
CREATE DATABASE course_management;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE course_management TO your_username;
\q
```
- Run the database setup script:
```bash
psql -d course_management -U your_username -f database_setup.sql
```

### 6. Configure the application
- Open `config.py` in a text editor.
- Set your database credentials:
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

Start the desktop application:
```bash
python main.py
```
The application window will open for login and management.

---

## How to Use the Course Management System

### 1. Login
- Launch the application and enter your username and password.
- Default users: admin, teacher1, teacher2, teacher_math, teacher_ee, student1, student2 (all password123).
- Click Login.

### 2. Admin Panel
- **User Management:** Add, edit, or delete users (students, teachers, admins).
- **Department Management:** Add, edit, or remove departments. (departments with student and course records cannot be deleted)
- **Course Management:** Add, edit, or delete courses. Deleting a course removes all related offerings/enrollments.
- **Semester Management:** Add, edit, or remove semesters (e.g., "2024-2025 Spring").
- **Course Offerings:** Assign courses to semesters and teachers.

### 3. Teacher Panel
- **Teaching Courses Tab:** View, add, edit, or refresh courses you offer. Edit all course details for your department's courses.
- **Course Offerings Tab:** View, add, edit, or delete course offerings for your courses in specific semesters.

### 4. Student Panel
- **Available Courses Tab:** View and enroll in eligible courses for the current semester. See instructor names. Cannot enroll in previous semester courses.
- **Enrolled Courses Tab:** View and drop courses you are enrolled in.

### 5. General Rules
- Students can only enroll in courses offered in the current semester and matching their level.
- Students can take all course types in their department, but only Elective/Technical Elective from other departments.
- Teachers can only offer/edit courses from their own department.
- Deleting a course, teacher, or student will automatically remove all related offerings/enrollments.

### 6. Troubleshooting
- If you see errors about foreign key constraints, ensure you are not deleting referenced items or that cascade deletes are set up.
- If you get a "transaction aborted" error, restart the application.

### 7. Logging Out
- Click the "Logout" button at the bottom of the window to return to the login screen.

---

## Default Users

The system comes with the following default users:

1. Admin:
   - Username: `admin`
   - Password: `password123`

2. Teachers:
   - Username: `teacher1`, Password: `password123`
   - Username: `teacher2`, Password: `password123`
   - Username: `teacher_math`, Password: `password123`
   - Username: `teacher_ee`, Password: `password123`

3. Students:
   - Username: `student1`, Password: `password123`
   - Username: `student2`, Password: `password123`

## Project Structure

```
course_management/
  database_setup.sql
  database.py
  config.py
  main.py
  requirements.txt
  README.md
  gui/
    course_management.py
    student_interface.py
    teacher_interface.py
    user_management.py
```

- `database_setup.sql`: Database schema and sample data
- `database.py`: Database access and logic
- `config.py`: Database connection configuration
- `main.py`: Main entry point for the desktop GUI
- `requirements.txt`: Python dependencies
- `gui/`: GUI modules for different user roles

## Database Structure

The database consists of the following main tables:

- `department`: Stores department information
- `course`: Stores course details including credits and ECTS
- `semester`: Manages academic semesters
- `user`: Stores user accounts with role-based access
- `teacher`: Stores teacher information
- `student`: Stores student information
- `course_offering`: Manages course offerings for each semester
- `enrolls_in`: Tracks student enrollments in courses

## Sample Data

The system comes with sample data including:
- 4 departments (Computer Science, Electrical Engineering, Mechanical Engineering, Mathematics)
- 3 semesters (Fall 2024, Spring 2025, Summer 2025)
- Multiple courses in Computer Science, Mathematics, and Electrical Engineering
- 4 teachers and 2 students
- Course offerings and enrollments

## Security Notes

- The default passwords are for testing purposes only
- In a production environment:
  - Change all default passwords
  - Use strong, unique passwords
  - Set up proper user authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
 
