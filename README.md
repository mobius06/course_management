# Course Management System

A web-based course management system built with Python Flask and PostgreSQL, designed for educational institutions to manage courses, students, teachers, and enrollments.

## Features

- User authentication with role-based access (Admin, Teacher, Student)
- Department management
- Course management with ECTS credits and course types
- Semester management
- Course offering management
- Student enrollment system
- Teacher assignment to courses
- Student grade tracking

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd course_management
```

2. Create a virtual environment and activate it:
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

4. Set up the PostgreSQL database:
```bash
# Connect to PostgreSQL
psql -U postgres

# Create the database and user
CREATE DATABASE course_management_new;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE course_management_new TO your_username;
\q

# Run the database setup script
psql -d course_management_new -f database_setup_new.sql
```

5. Configure the application:
   - Copy `.env.example` to `.env`
   - Update the database connection settings in `.env`:
     ```
     DATABASE_URL=postgresql://your_username:your_password@localhost:5432/course_management_new
     SECRET_KEY=your_secret_key
     ```

## Running the Application

1. Start the Flask development server:
```bash
flask run
```

2. Access the application at `http://localhost:5000`

## Default Users

The system comes with the following default users:

1. Admin:
   - Username: `admin`
   - Password: `password123`

2. Teachers:
   - Username: `teacher1`, Password: `password123`
   - Username: `teacher2`, Password: `password123`

3. Students:
   - Username: `student1`, Password: `password123`
   - Username: `student2`, Password: `password123`

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
- 5 courses in Computer Science
- 2 teachers and 2 students
- Course offerings and enrollments

To view the sample data, run:
```bash
psql -d course_management_new -f view_data.sql
```

## Security Notes

- The default passwords are for testing purposes only
- In a production environment:
  - Change all default passwords
  - Use strong, unique passwords
  - Enable HTTPS
  - Set up proper user authentication
  - Implement password reset functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers. 