-- Create new database
CREATE DATABASE course_management_new;

-- Connect to the new database
\c course_management_new;

-- Create tables
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    credits INTEGER NOT NULL,
    ects INTEGER NOT NULL,
    level VARCHAR(20) CHECK (level IN ('Bachelor', 'Master')),
    type VARCHAR(20) CHECK (type IN ('Must', 'Elective', 'Technical Elective')),
    department_id INTEGER REFERENCES department(department_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE semester (
    semester_id SERIAL PRIMARY KEY,
    semester_name VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id),
    student_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_offering (
    offering_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES course(course_id),
    semester_id INTEGER REFERENCES semester(semester_id),
    instructor_id INTEGER REFERENCES teacher(teacher_id),
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrolls_in (
    enrollment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES student(student_id),
    course_id INTEGER REFERENCES course(course_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
-- Departments
INSERT INTO department (department_name) VALUES
    ('Computer Science'),
    ('Electrical Engineering'),
    ('Mechanical Engineering'),
    ('Mathematics');

-- Semesters
INSERT INTO semester (semester_name, year, start_date, end_date) VALUES
    ('2024-2025 Fall', 2024, '2024-09-01', '2025-01-31'),
    ('2024-2025 Spring', 2025, '2025-02-01', '2025-06-30'),
    ('2025 Summer', 2025, '2025-07-01', '2025-08-31');

-- Users (with properly hashed passwords - default password is 'password123')
INSERT INTO "user" (username, password, role) VALUES
    ('admin', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'admin'),
    ('teacher1', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'teacher'),
    ('teacher2', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'teacher'),
    ('student1', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'student'),
    ('student2', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'student');

-- Teachers
INSERT INTO teacher (user_id, first_name, last_name, email, department_id) VALUES
    (2, 'John', 'Smith', 'john.smith@university.edu', 1),
    (3, 'Jane', 'Doe', 'jane.doe@university.edu', 1);

-- Students
INSERT INTO student (user_id, student_number, first_name, last_name, email, department_id) VALUES
    (4, 'STU0001', 'Alice', 'Johnson', 'alice.johnson@university.edu', 1),
    (5, 'STU0002', 'Bob', 'Williams', 'bob.williams@university.edu', 1);

-- Courses
INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id) VALUES
    ('Introduction to Programming', 'CS101', 3, 6, 'Bachelor', 'Must', 1),
    ('Data Structures', 'CS201', 4, 7, 'Bachelor', 'Must', 1),
    ('Database Systems', 'CS301', 3, 6, 'Bachelor', 'Must', 1),
    ('Machine Learning', 'CS401', 4, 7, 'Master', 'Technical Elective', 1),
    ('Advanced Algorithms', 'CS501', 3, 6, 'Master', 'Must', 1);

-- Course Offerings
INSERT INTO course_offering (course_id, semester_id, instructor_id, year) VALUES
    (1, 1, 1, 2024),  -- CS101 in Fall 2024
    (2, 1, 1, 2024),  -- CS201 in Fall 2024
    (3, 2, 2, 2025),  -- CS301 in Spring 2025
    (4, 2, 2, 2025),  -- CS401 in Spring 2025
    (5, 3, 1, 2025);  -- CS501 in Summer 2025

-- Enrollments
INSERT INTO enrolls_in (user_id, course_id) VALUES
    (1, 1),  -- Student 1 in CS101
    (1, 2),  -- Student 1 in CS201
    (2, 1);  -- Student 2 in CS101 