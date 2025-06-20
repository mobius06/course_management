-- Add departments if they don't exist
INSERT INTO department (department_name)
SELECT d.department_name
FROM (VALUES 
    ('Computer Science'),
    ('Electrical Engineering'),
    ('Mechanical Engineering'),
    ('Mathematics')
) AS d(department_name)
WHERE NOT EXISTS (
    SELECT 1 FROM department WHERE department_name = d.department_name
);

-- Add semesters if they don't exist
INSERT INTO semester (semester_name, year, start_date, end_date)
SELECT 
    s.semester_name, 
    s.year, 
    s.start_date::DATE, 
    s.end_date::DATE
FROM (VALUES 
    ('2024-2025 Fall', 2024, '2024-09-01', '2025-01-31'),
    ('2024-2025 Spring', 2025, '2025-02-01', '2025-06-30'),
    ('2025 Summer', 2025, '2025-07-01', '2025-08-31')
) AS s(semester_name, year, start_date, end_date)
WHERE NOT EXISTS (
    SELECT 1 FROM semester 
    WHERE semester_name = s.semester_name 
    AND year = s.year
);

-- Add users if they don't exist
WITH new_users AS (
    SELECT 
        username,
        password,
        role,
        first_name,
        last_name
    FROM (VALUES 
        ('teacher1', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'teacher', 'John', 'Smith'),
        ('teacher2', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'teacher', 'Jane', 'Doe'),
        ('student1', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'student', 'Alice', 'Johnson'),
        ('student2', '5c44c5326f03a7d13fb3092af58258a4$58c00299abd0858b5aedf33c7307c694ed6ff7165cee720f0b5a1255cd7864e2', 'student', 'Bob', 'Williams')
    ) AS u(username, password, role, first_name, last_name)
    WHERE NOT EXISTS (
        SELECT 1 FROM "user" WHERE username = u.username
    )
)
INSERT INTO "user" (username, password, role, first_name, last_name)
SELECT username, password, role, first_name, last_name
FROM new_users;

-- Add teachers if they don't exist
WITH teacher_data AS (
    SELECT 
        u.user_id,
        d.department_id,
        CASE 
            WHEN u.username = 'teacher1' THEN 'John'
            WHEN u.username = 'teacher2' THEN 'Jane'
        END as first_name,
        CASE 
            WHEN u.username = 'teacher1' THEN 'Smith'
            WHEN u.username = 'teacher2' THEN 'Doe'
        END as last_name,
        CASE 
            WHEN u.username = 'teacher1' THEN 'john.smith@university.edu'
            WHEN u.username = 'teacher2' THEN 'jane.doe@university.edu'
        END as email
    FROM "user" u
    CROSS JOIN department d
    WHERE u.role = 'teacher'
    AND d.department_name = 'Computer Science'
    AND NOT EXISTS (
        SELECT 1 FROM teacher t WHERE t.user_id = u.user_id
    )
)
INSERT INTO teacher (user_id, department_id, first_name, last_name, email)
SELECT 
    user_id,
    department_id,
    first_name,
    last_name,
    email
FROM teacher_data;

-- Add students if they don't exist
WITH student_data AS (
    SELECT 
        u.user_id,
        d.department_id,
        CASE 
            WHEN u.username = 'student1' THEN 'STU0001'
            WHEN u.username = 'student2' THEN 'STU0002'
        END as student_number,
        CASE 
            WHEN u.username = 'student1' THEN 'Alice'
            WHEN u.username = 'student2' THEN 'Bob'
        END as first_name,
        CASE 
            WHEN u.username = 'student1' THEN 'Johnson'
            WHEN u.username = 'student2' THEN 'Williams'
        END as last_name,
        CASE 
            WHEN u.username = 'student1' THEN 'alice.johnson@university.edu'
            WHEN u.username = 'student2' THEN 'bob.williams@university.edu'
        END as email,
        CASE 
            WHEN u.username = 'student1' THEN 'Bachelor'
            WHEN u.username = 'student2' THEN 'Bachelor'
        END as level
    FROM "user" u
    CROSS JOIN department d
    WHERE u.role = 'student'
    AND d.department_name = 'Computer Science'
    AND NOT EXISTS (
        SELECT 1 FROM student s WHERE s.user_id = u.user_id
    )
)
INSERT INTO student (user_id, department_id, student_number, first_name, last_name, email, level)
SELECT 
    user_id,
    department_id,
    student_number,
    first_name,
    last_name,
    email,
    level
FROM student_data;

-- Add courses if they don't exist
INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id)
SELECT 
    c.course_name,
    c.course_code,
    c.credits,
    c.ects,
    c.level,
    c.type,
    d.department_id
FROM (VALUES 
    ('Introduction to Programming', 'CS101', 3, 6, 'Bachelor', 'Must'),
    ('Data Structures', 'CS201', 4, 7, 'Bachelor', 'Must'),
    ('Database Systems', 'CS301', 3, 6, 'Bachelor', 'Must'),
    ('Machine Learning', 'CS401', 4, 7, 'Master', 'Technical Elective'),
    ('Advanced Algorithms', 'CS501', 3, 6, 'Master', 'Must')
) AS c(course_name, course_code, credits, ects, level, type)
CROSS JOIN department d
WHERE d.department_name = 'Computer Science'
AND NOT EXISTS (
    SELECT 1 FROM course WHERE course_code = c.course_code
);

-- Add course offerings if they don't exist
WITH course_offerings AS (
    SELECT 
        c.course_id,
        s.semester_id,
        t.teacher_id,
        s.year
    FROM course c
    CROSS JOIN semester s
    CROSS JOIN teacher t
    WHERE NOT EXISTS (
        SELECT 1 FROM course_offering co 
        WHERE co.course_id = c.course_id 
        AND co.semester_id = s.semester_id
    )
    ORDER BY c.course_id, s.semester_id, t.teacher_id
)
INSERT INTO course_offering (course_id, semester_id, instructor_id, year)
SELECT 
    course_id,
    semester_id,
    teacher_id,
    year
FROM (
    SELECT 
        course_id,
        semester_id,
        teacher_id,
        year,
        ROW_NUMBER() OVER (PARTITION BY course_id, semester_id ORDER BY teacher_id) as rn
    FROM course_offerings
) ranked
WHERE rn = 1;

-- Add enrollments if they don't exist
WITH enrollments AS (
    SELECT 
        s.student_id,
        c.course_id
    FROM student s
    CROSS JOIN course c
    WHERE NOT EXISTS (
        SELECT 1 FROM enrolls_in e 
        WHERE e.user_id = s.student_id 
        AND e.course_id = c.course_id
    )
    ORDER BY s.student_id, c.course_id
)
INSERT INTO enrolls_in (user_id, course_id)
SELECT 
    student_id,
    course_id
FROM (
    SELECT 
        student_id,
        course_id,
        ROW_NUMBER() OVER (PARTITION BY student_id ORDER BY course_id) as rn
    FROM enrollments
) ranked
WHERE rn <= 3;  -- Each student enrolls in up to 3 courses 