-- Create tables
CREATE TABLE IF NOT EXISTS department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL,
    credits INTEGER NOT NULL,
    ects INTEGER NOT NULL,
    level VARCHAR(20) NOT NULL,
    type VARCHAR(20) NOT NULL,
    department_id INTEGER REFERENCES department(department_id)
);

CREATE TABLE IF NOT EXISTS semester (
    semester_id SERIAL PRIMARY KEY,
    semester_name VARCHAR(50) UNIQUE NOT NULL,
    year INTEGER
);

CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS course_offering (
    offering_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES course(course_id),
    semester_id INTEGER REFERENCES semester(semester_id),
    instructor_id INTEGER REFERENCES "user"(user_id),
    year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS enrolls_in (
    user_id INTEGER REFERENCES "user"(user_id),
    course_id INTEGER REFERENCES course(course_id),
    PRIMARY KEY (user_id, course_id)
);

-- Insert test data
-- Departments
INSERT INTO department (department_name) VALUES 
('Computer Science'),
('Mathematics'),
('Physics'),
('Engineering');

-- Courses
INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id) VALUES
('Introduction to Programming', 'CS101', 3, 6, 'Bachelor', 'Mandatory', 1),
('Data Structures', 'CS201', 4, 7, 'Bachelor', 'Mandatory', 1),
('Database Systems', 'CS301', 3, 6, 'Bachelor', 'Mandatory', 1),
('Calculus I', 'MATH101', 4, 7, 'Bachelor', 'Mandatory', 2),
('Linear Algebra', 'MATH201', 3, 6, 'Bachelor', 'Mandatory', 2),
('Classical Mechanics', 'PHYS101', 4, 7, 'Bachelor', 'Mandatory', 3),
('Circuit Analysis', 'ENG101', 3, 6, 'Bachelor', 'Mandatory', 4);

-- Semesters
INSERT INTO semester (semester_name, year) VALUES 
('Fall 2023', 2023),
('Spring 2024', 2024),
('Fall 2024', 2024);

-- Users
INSERT INTO "user" (username, password, role) VALUES
('admin', 'salt$admin123', 'admin'),
('teacher1', 'salt$teacher1_pass', 'teacher'),
('teacher2', 'salt$teacher2_pass', 'teacher'),
('teacher3', 'salt$teacher3_pass', 'teacher'),
('teacher4', 'salt$teacher4_pass', 'teacher'),
('student1', 'salt$student1_pass', 'student'),
('student2', 'salt$student2_pass', 'student'),
('student3', 'salt$student3_pass', 'student');

-- Course Offerings
INSERT INTO course_offering (course_id, semester_id, instructor_id, year) VALUES
(1, 1, 2, 2023),  -- CS101 in Fall 2023
(2, 1, 2, 2023),  -- CS201 in Fall 2023
(3, 2, 2, 2024),  -- CS301 in Spring 2024
(4, 1, 3, 2023),  -- MATH101 in Fall 2023
(5, 2, 3, 2024),  -- Linear Algebra in Spring 2024
(6, 1, 3, 2023),  -- Physics in Fall 2023
(7, 2, 4, 2024);  -- Engineering in Spring 2024

-- Enrollments
INSERT INTO enrolls_in (user_id, course_id) VALUES
(6, 1),  -- student1 enrolled in Introduction to Programming
(6, 2),  -- student1 enrolled in Data Structures
(7, 1),  -- student2 enrolled in Introduction to Programming
(7, 4),  -- student2 enrolled in Calculus I
(8, 1),  -- student3 enrolled in Introduction to Programming
(8, 6);  -- student3 enrolled in Classical Mechanics 