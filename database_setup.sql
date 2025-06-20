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
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE,
    student_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    level VARCHAR(20) CHECK (level IN ('Bachelor', 'Master')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES "user"(user_id) ON DELETE CASCADE,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course_offering (
    offering_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES course(course_id) ON DELETE CASCADE,
    semester_id INTEGER REFERENCES semester(semester_id),
    instructor_id INTEGER REFERENCES teacher(teacher_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrolls_in (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES student(student_id) ON DELETE CASCADE,
    course_id INTEGER REFERENCES course(course_id) ON DELETE CASCADE,
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

-- Users (plain text passwords - default password is 'password123')
INSERT INTO "user" (username, password, role, first_name, last_name) VALUES
    ('admin', 'password123', 'admin', 'System', 'Administrator'),
    ('teacher1', 'password123', 'teacher', 'John', 'Smith'),
    ('teacher2', 'password123', 'teacher', 'Jane', 'Doe'),
    ('student1', 'password123', 'student', 'Alice', 'Johnson'),
    ('student2', 'password123', 'student', 'Bob', 'Williams'),
    ('teacher_math', 'password123', 'teacher', 'Emily', 'Brown'),
    ('teacher_ee', 'password123', 'teacher', 'Michael', 'Green');

-- Teachers
INSERT INTO teacher (user_id, email, department_id) VALUES
    (2, 'john.smith@university.edu', 1),
    (3, 'jane.doe@university.edu', 1),
    (6, 'emily.brown@university.edu', 4),
    (7, 'michael.green@university.edu', 2);

-- Students
INSERT INTO student (user_id, student_number, email, department_id, first_name, last_name, level) VALUES
    (4, 'STU0001', 'alice.johnson@university.edu', 1, 'Alice', 'Johnson', 'Bachelor'),
    (5, 'STU0002', 'bob.williams@university.edu', 1, 'Bob', 'Williams', 'Bachelor');

-- Courses
INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id) VALUES
    ('Introduction to Programming', 'CS101', 3, 6, 'Bachelor', 'Must', 1),
    ('Data Structures', 'CS201', 4, 7, 'Bachelor', 'Must', 1),
    ('Database Systems', 'CS301', 3, 6, 'Bachelor', 'Must', 1),
    ('Machine Learning', 'CS401', 4, 7, 'Master', 'Technical Elective', 1),
    ('Advanced Algorithms', 'CS501', 3, 6, 'Master', 'Must', 1),
    ('Linear Algebra', 'MATH201', 3, 6, 'Bachelor', 'Elective', 4),
    ('Advanced Calculus', 'MATH501', 3, 6, 'Master', 'Technical Elective', 4),
    ('Circuit Analysis', 'EE201', 3, 6, 'Bachelor', 'Elective', 2),
    ('Digital Signal Processing', 'EE501', 3, 6, 'Master', 'Technical Elective', 2);

-- Course Offerings
INSERT INTO course_offering (course_id, semester_id, instructor_id) VALUES
    (1, 1, 1),  -- CS101 in Fall 2024
    (2, 1, 1),  -- CS201 in Fall 2024
    (3, 2, 2),  -- CS301 in Spring 2025
    (4, 2, 2),  -- CS401 in Spring 2025
    (5, 3, 1),  -- CS501 in Summer 2025
    ((SELECT course_id FROM course WHERE course_code = 'MATH201'), 2, (SELECT teacher_id FROM teacher WHERE user_id = 6)),  -- MATH201 by Emily Brown
    ((SELECT course_id FROM course WHERE course_code = 'MATH501'), 2, (SELECT teacher_id FROM teacher WHERE user_id = 6)),  -- MATH501 by Emily Brown
    ((SELECT course_id FROM course WHERE course_code = 'EE201'), 2, (SELECT teacher_id FROM teacher WHERE user_id = 7)),    -- EE201 by Michael Green
    ((SELECT course_id FROM course WHERE course_code = 'EE501'), 2, (SELECT teacher_id FROM teacher WHERE user_id = 7));    -- EE501 by Michael Green

-- Enrollments
INSERT INTO enrolls_in (student_id, course_id) VALUES
    (1, 1),  -- Student 1 in CS101
    (1, 2),  -- Student 1 in CS201
    (2, 1);  -- Student 2 in CS101

UPDATE student SET level = 'Bachelor' WHERE level IS NULL;