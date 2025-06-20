# Database Structure Documentation

## Tables Overview

### 1. department
Stores information about academic departments.
```sql
CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. course
Stores information about courses offered by departments.
```sql
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
```

### 3. semester
Manages academic semesters and their time periods.
```sql
CREATE TABLE semester (
    semester_id SERIAL PRIMARY KEY,
    semester_name VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. user
Stores user account information with role-based access.
```sql
CREATE TABLE "user" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) CHECK (role IN ('admin', 'teacher', 'student')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. teacher
Stores detailed information about teachers.
```sql
CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. student
Stores detailed information about students.
```sql
CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(user_id),
    student_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INTEGER REFERENCES department(department_id),
    level VARCHAR(20) CHECK (level IN ('Bachelor', 'Master')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 7. course_offering
Manages course offerings for specific semesters.
```sql
CREATE TABLE course_offering (
    offering_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES course(course_id),
    semester_id INTEGER REFERENCES semester(semester_id),
    instructor_id INTEGER REFERENCES teacher(teacher_id),
    year INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 8. enrolls_in
Tracks student enrollments in courses.
```sql
CREATE TABLE enrolls_in (
    enrollment_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES student(student_id),
    course_id INTEGER REFERENCES course(course_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Relationships

1. **Department Relationships**:
   - One-to-Many with `course`
   - One-to-Many with `teacher`
   - One-to-Many with `student`

2. **User Relationships**:
   - One-to-One with `teacher` (for teacher users)
   - One-to-One with `student` (for student users)

3. **Course Relationships**:
   - Many-to-One with `department`
   - One-to-Many with `course_offering`
   - Many-to-Many with `student` (through `enrolls_in`)

4. **Semester Relationships**:
   - One-to-Many with `course_offering`

5. **Teacher Relationships**:
   - One-to-One with `user`
   - Many-to-One with `department`
   - One-to-Many with `course_offering`

6. **Student Relationships**:
   - One-to-One with `user`
   - Many-to-One with `department`
   - Many-to-Many with `course` (through `enrolls_in`)

## Constraints

1. **Unique Constraints**:
   - `course.course_code`
   - `user.username`
   - `teacher.email`
   - `student.email`
   - `student.student_number`

2. **Check Constraints**:
   - `course.level` must be either 'Bachelor' or 'Master'
   - `course.type` must be either 'Must', 'Elective', or 'Technical Elective'
   - `user.role` must be either 'admin', 'teacher', or 'student'

3. **Foreign Key Constraints**:
   - All relationships are enforced with foreign key constraints
   - Cascading deletes are not enabled by default

## Indexes

The following columns are automatically indexed:
- All PRIMARY KEY columns
- All FOREIGN KEY columns
- All UNIQUE constraint columns

## Sample Data

The database comes with sample data including:
- 4 departments
- 5 courses
- 3 semesters
- 2 teachers
- 2 students
- Course offerings and enrollments

To view the sample data, run:
```bash
psql -d course_management_new -f view_data.sql
``` 