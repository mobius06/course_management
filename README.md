# Course Management System

A comprehensive, GUI-based course management system developed with Python's Tkinter library and a PostgreSQL database. This system is designed for educational institutions to efficiently manage courses, students, teachers, departments, and enrollments through a role-based interface.

## Features

- **Role-Based Access Control:** Separate interfaces and permissions for Admins, Teachers, and Students.
- **User Management (Admin):** Admins can add, edit, and delete user accounts for all roles.
- **Department Management (Admin):** Admins can create and manage academic departments.
- **Course Management (Admin/Teacher):** Admins can manage all courses, while teachers can manage courses within their own department.
- **Semester & Course Offerings (Admin/Teacher):** Manage academic semesters and offer courses for specific semesters, assigning teachers to them.
- **Student Enrollment (Student):** Students can view available courses and enroll in them based on their department and level.
- **Dynamic GUI:** The user interface, built with `ttkthemes`, is intuitive and responsive.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher

## Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd course_management
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up PostgreSQL Database:**
    -   Log in to PostgreSQL: `psql -U postgres`
    -   Create a database and a user (replace with your own credentials):
        ```sql
        CREATE DATABASE course_management;
        CREATE USER your_username WITH PASSWORD 'your_password';
        GRANT ALL PRIVILEGES ON DATABASE course_management TO your_username;
        \q
        ```
    -   Run the setup script to create tables and insert sample data:
        ```bash
        psql -d course_management -U your_username -f database_setup.sql
        ```

4.  **Configure the Application:**
    -   Create a file named `config.py` in the root directory.
    -   Add the following dictionary with your database credentials:
        ```python
        DB_CONFIG = {
            'dbname': 'course_management',
            'user': 'your_username',
            'password': 'your_password',
            'host': 'localhost',
            'port': '5432' # also check your port number
        }
        ```

## Running the Application

To start the system, run the following command from the project's root directory:
```bash
python main.py
```
This will open the login window.

---

## How to Use the Course Management System

The system provides different functionalities based on the user's role. Here are the default credentials for initial login:
- **Admin:** `admin` / `password123`
- **Teachers:** `teacher1` / `password123`, `teacher2` / `password123`
- **Students:** `student1` / `password123`, `student2` / `password123`

### 1. Admin Interface

The admin has full control over the system through a tabbed interface.

#### **Users Tab**
- **View Users:** A list of all users (admins, teachers, students) is displayed with their ID, username, role, and creation date.
- **Add a New User:**
    1.  Click the "Add User" button.
    2.  Fill in the user's details: username, password, role, first name, and last name.
    3.  If the role is "Student" or "Teacher," additional fields for department, email, etc., will appear. Fill these in.
    4.  Click "Save" to create the user.
- **Edit or Delete a User:**
    1.  Double-click on a user in the list to open the details view.
    2.  Click "Edit" to open the edit form. You can update the username, role, name, and set a new password.
    3.  Click "Delete" to permanently remove the user.

#### **Departments Tab**
- **View Departments:** Shows a list of all academic departments.
- **Add a Department:**
    1.  Click "Add Department."
    2.  Enter the department name and click "Save."
- **Edit a Department:**
    1.  Select a department from the list.
    2.  Click "Edit Department."
    3.  Modify the name and click "Save Changes."
- **Delete a Department:**
    1.  Select a department from the list.
    2.  Click "Delete Department" and confirm the action.

### 2. Teacher Interface

Teachers manage their courses and course offerings.

#### **Teaching Courses Tab**
This tab displays the courses the logged-in teacher is assigned to teach, grouped by semester.
- **Add a New Course:**
    1.  Click "Add Course."
    2.  Fill in the course details: name, code, credits, ECTS, level, and type. The department is automatically set to the teacher's department.
    3.  Click "Save."
- **Edit a Course:**
    1.  Select a course from the list.
    2.  Click "Edit Course."
    3.  Modify the course details and save the changes. Teachers can only edit courses within their own department.

#### **Course Offerings Tab**
This tab allows teachers to manage which courses are offered in which semester.
- **View Course Offerings:** Displays a list of all courses offered across all departments and semesters.
- **Add a Course Offering:**
    1.  Click "Add Course Offering."
    2.  Select a course and a semester from the dropdown menus. The instructor is automatically set to you.
    3.  Click "Save Offering." This makes the course available for student enrollment in that semester.
- **Remove a Course Offering:**
    1.  Select a course offering from the list.
    2.  Click "Remove Offering" and confirm.

### 3. Student Interface

Students can browse and enroll in courses.

#### **Available Courses Tab**
- **View Available Courses:** Shows a list of courses offered in the current semester that the student is eligible to enroll in. This includes the course details and the instructor's name.
- **Enroll in a Course:**
    1.  Double-click on a course in the "Available Courses" list.
    2.  A dialog with course details will appear.
    3.  Click "Enroll in Course" to register for it. The course will then move to your "Enrolled Courses" tab.

#### **Enrolled Courses Tab**
- **View Enrolled Courses:** Displays a list of all courses the student is currently enrolled in.
- **Drop a Course:**
    1.  Double-click on a course in the "Enrolled Courses" list.
    2.  In the details dialog, click "Drop Course" and confirm. The course will be removed from your list and will reappear in the "Available Courses" tab if the enrollment period is still active.

### Logging Out
- At any point, a user can click the "Logout" button at the bottom of the window to return to the login screen.

---
## Project Structure

```
course_management/
  ├── database.py
  ├── database_setup.sql
  ├── main.py
  ├── requirements.txt
  ├── README.md
  ├── config.py
  └── gui/
      ├── course_management.py
      ├── student_interface.py
      ├── teacher_interface.py
      └── user_management.py
```
- `main.py`: The entry point of the application. Handles login and navigation.
- `database.py`: Manages all database connections and queries.
- `database_setup.sql`: SQL script to initialize the database schema and sample data.
- `config.py`: Contains the database connection configuration.
- `gui/`: A package containing all the UI modules.
  - `user_management.py`: Admin's interface for managing users and departments.
  - `course_management.py`: Admin's interface for managing all courses.
  - `teacher_interface.py`: Teacher's interface for managing their courses and offerings.
  - `student_interface.py`: Student's interface for enrolling in courses.

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
 
