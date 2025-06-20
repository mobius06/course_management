import psycopg2
from psycopg2 import Error
from config import DB_CONFIG
import hashlib
import secrets
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("Successfully connected to the database")
            # Test the connection with a simple query
            cursor = self.connection.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"PostgreSQL version: {version}")
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except Error as e:
            print(f"Error executing query: {e}")
            return None

    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchall()
        return []

    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        if cursor:
            return cursor.fetchone()
        return None

    def hash_password(self, password):
        # For simplicity, just return the password as is (plain text)
        return password

    def verify_password(self, stored_password, provided_password):
        # For simplicity, just compare plain text passwords
        return stored_password == provided_password

    # User operations
    def get_user(self, username):
        query = "SELECT * FROM \"user\" WHERE username = %s"
        result = self.fetch_one(query, (username,))
        print(f"get_user query result for {username}: {result}")
        return result

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM \"user\" WHERE user_id = %s"
        return self.fetch_one(query, (user_id,))

    def get_all_users(self):
        query = "SELECT user_id, username, role, created_at FROM \"user\" ORDER BY user_id"
        return self.fetch_all(query)

    def create_user(self, username, password, role, first_name, last_name):
        """Create a new user with plain text password and name"""
        try:
            if self.check_username_exists(username):
                return False
            # Store password as plain text
            query = """
            INSERT INTO "user" (username, password, role, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.execute_query(query, (username, password, role.lower(), first_name, last_name))
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    def update_user(self, user_id, username, password=None, role=None, first_name=None, last_name=None):
        """Update user information"""
        try:
            # Check if username already exists (excluding current user)
            if self.check_username_exists(username, user_id):
                return False

            # Build update query based on provided fields
            update_fields = []
            params = []

            if username:
                update_fields.append("username = %s")
                params.append(username)

            if password:
                update_fields.append("password = %s")
                params.append(password)

            if role:
                update_fields.append("role = %s")
                params.append(role.lower())

            if first_name is not None:
                update_fields.append("first_name = %s")
                params.append(first_name)

            if last_name is not None:
                update_fields.append("last_name = %s")
                params.append(last_name)

            if not update_fields:
                return False

            # Add user_id to params
            params.append(user_id)

            # Execute update
            query = f"""
            UPDATE "user" 
            SET {', '.join(update_fields)}
            WHERE user_id = %s
            """
            self.execute_query(query, tuple(params))
            return True
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            return False

    def check_username_exists(self, username, exclude_id=None):
        """Check if a username already exists"""
        query = "SELECT user_id FROM \"user\" WHERE username = %s"
        params = [username]
        if exclude_id:
            query += " AND user_id != %s"
            params.append(exclude_id)
        return bool(self.fetch_one(query, tuple(params)))

    def authenticate_user(self, username, password):
        print(f"\nAttempting to authenticate user: {username}")
        user = self.get_user(username)
        if not user:
            print(f"User not found: {username}")
            return None
            
        print(f"Found user data: {user}")
        print(f"Stored password: {user[2]}")
        print(f"Attempting to verify password...")
        
        if self.verify_password(user[2], password):
            print(f"Password verified successfully for user: {username}")
            return user
        print(f"Password verification failed for user: {username}")
        return None

    # Student operations
    def get_student(self, user_id):
        query = """
        SELECT s.*, d.department_name 
        FROM student s 
        JOIN department d ON s.department_id = d.department_id 
        WHERE s.user_id = %s
        """
        return self.fetch_one(query, (user_id,))

    def create_student(self, user_id, student_number, first_name, last_name, email, department_id, level):
        query = """
        INSERT INTO student (user_id, student_number, first_name, last_name, email, department_id, level)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING student_id
        """
        return self.fetch_one(query, (user_id, student_number, first_name, last_name, email, department_id, level))

    # Teacher operations
    def get_teacher(self, user_id):
        query = """
        SELECT t.*, d.department_name 
        FROM teacher t 
        JOIN department d ON t.department_id = d.department_id 
        WHERE t.user_id = %s
        """
        return self.fetch_one(query, (user_id,))

    def create_teacher(self, user_id, first_name, last_name, email, department_id):
        query = """
        INSERT INTO teacher (user_id, first_name, last_name, email, department_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING teacher_id
        """
        return self.fetch_one(query, (user_id, first_name, last_name, email, department_id))

    # Course operations
    def get_all_courses(self):
        """Get all courses with department names"""
        query = """
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.ects, 
               c.level, c.type, d.department_name
        FROM course c 
        JOIN department d ON c.department_id = d.department_id
        ORDER BY c.course_code
        """
        return self.fetch_all(query)

    def get_course_by_id(self, course_id):
        """Get course by ID with department name"""
        query = """
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.ects, 
               c.level, c.type, d.department_name
        FROM course c 
        JOIN department d ON c.department_id = d.department_id 
        WHERE c.course_id = %s
        """
        return self.fetch_one(query, (course_id,))

    # Department operations
    def get_all_departments(self):
        query = "SELECT * FROM department"
        return self.fetch_all(query)

    def get_department_name(self, department_id):
        """Get department name by ID"""
        try:
            if not isinstance(department_id, (int, str)) or not str(department_id).isdigit():
                return "N/A"
            query = "SELECT department_name FROM department WHERE department_id = %s"
            result = self.fetch_one(query, (int(department_id),))
            return result[0] if result else "N/A"
        except Exception as e:
            print(f"Error getting department name: {str(e)}")
            return "N/A"

    # Semester operations
    def get_all_semesters(self):
        query = "SELECT * FROM semester ORDER BY start_date DESC"
        return self.fetch_all(query)

    def get_current_semester(self):
        current_date = datetime.now().date()
        query = """
        SELECT * FROM semester 
        WHERE start_date <= %s AND end_date >= %s
        """
        return self.fetch_one(query, (current_date, current_date))

    # Enrollment operations
    def is_student_enrolled(self, student_id, course_id):
        """Check if a student is already enrolled in a course"""
        query = "SELECT * FROM enrolls_in WHERE student_id = %s AND course_id = %s"
        return bool(self.fetch_one(query, (student_id, course_id)))

    def get_student_courses(self, student_id):
        """Get courses enrolled by a student with proper semester and year information"""
        query = """
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.ects, 
               c.level, c.type, d.department_name, s.semester_name, s.year
        FROM course c 
        JOIN enrolls_in e ON c.course_id = e.course_id 
        JOIN department d ON c.department_id = d.department_id
        JOIN course_offering co ON c.course_id = co.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        WHERE e.student_id = %s
        ORDER BY s.year DESC, s.semester_name
        """
        return self.fetch_all(query, (student_id,))

    def enroll_student(self, student_id, course_id):
        """Enroll a student in a course with proper validation and restrictions"""
        try:
            # Start transaction
            self.connection.autocommit = False

            # Get student info (including level and department)
            student_query = "SELECT level, department_id FROM student WHERE student_id = %s"
            student_info = self.fetch_one(student_query, (student_id,))
            if not student_info:
                return False, "Student not found"
            student_level, student_dept = student_info

            # Get course info (level, type, department)
            course_query = "SELECT level, type, department_id FROM course WHERE course_id = %s"
            course_info = self.fetch_one(course_query, (course_id,))
            if not course_info:
                return False, "Course not found"
            course_level, course_type, course_dept = course_info

            # Restriction 1: Level must match
            if student_level != course_level:
                return False, f"You can only enroll in {student_level} level courses."

            # Restriction 2: Department/type rules
            if student_dept == course_dept:
                # Can take any type
                pass
            else:
                # Can only take Elective or Technical Elective
                if course_type not in ("Elective", "Technical Elective"):
                    return False, "You can only take Elective or Technical Elective courses from other departments."

            # Check if already enrolled
            if self.is_student_enrolled(student_id, course_id):
                return False, "Already enrolled in this course"

            # Check if course is available for enrollment and not in a previous semester
            query = """
            SELECT co.offering_id, s.end_date
            FROM course_offering co
            JOIN semester s ON co.semester_id = s.semester_id
            WHERE co.course_id = %s
            """
            result = self.fetch_one(query, (course_id,))
            if not result:
                return False, "Course is not available for enrollment"
            _, semester_end_date = result
            from datetime import date
            if semester_end_date < date.today():
                return False, "Cannot enroll in previous semester courses."

            # Perform enrollment
            enroll_query = "INSERT INTO enrolls_in (student_id, course_id) VALUES (%s, %s)"
            self.execute_query(enroll_query, (student_id, course_id))

            # Commit transaction
            self.connection.commit()
            return True, "Successfully enrolled in course"
        except Exception as e:
            self.connection.rollback()
            return False, f"Failed to enroll: {str(e)}"

    # Course offering operations
    def get_course_offerings(self, semester_id=None):
        """Get course offerings with department names and instructor name"""
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, s.semester_name, s.year, d.department_name, u.first_name || ' ' || u.last_name as instructor_name
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        JOIN department d ON c.department_id = d.department_id
        JOIN teacher t ON co.instructor_id = t.teacher_id
        JOIN "user" u ON t.user_id = u.user_id
        """
        if semester_id:
            query += " WHERE co.semester_id = %s"
            return self.fetch_all(query, (semester_id,))
        return self.fetch_all(query)

    def get_teaching_courses(self, teacher_id):
        """Get courses taught by a teacher with department names"""
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, 
               s.semester_name, s.year, d.department_name
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        JOIN department d ON c.department_id = d.department_id
        WHERE co.instructor_id = %s
        ORDER BY s.year DESC, s.semester_name
        """
        return self.fetch_all(query, (teacher_id,))

    def create_course_offering(self, course_id, semester_id, instructor_id):
        # Check that the teacher is from the same department as the course
        teacher_dept = self.fetch_one("SELECT department_id FROM teacher WHERE teacher_id = %s", (instructor_id,))
        course_dept = self.fetch_one("SELECT department_id FROM course WHERE course_id = %s", (course_id,))
        if not teacher_dept or not course_dept or teacher_dept[0] != course_dept[0]:
            raise Exception("You can only offer courses from your own department.")
        # Prevent duplicate offerings for the same course/semester
        exists = self.fetch_one("SELECT 1 FROM course_offering WHERE course_id = %s AND semester_id = %s", (course_id, semester_id))
        if exists:
            raise Exception("This course is already offered by another teacher in this semester.")
        query = """
        INSERT INTO course_offering (course_id, semester_id, instructor_id)
        VALUES (%s, %s, %s)
        RETURNING offering_id
        """
        return self.fetch_one(query, (course_id, semester_id, instructor_id))

    def update_course_offering(self, offering_id, course_id, semester_id, instructor_id):
        query = """
        UPDATE course_offering 
        SET course_id = %s, semester_id = %s, instructor_id = %s
        WHERE offering_id = %s
        """
        return self.execute_query(query, (course_id, semester_id, instructor_id, offering_id))

    def update_user_password(self, user_id, new_password):
        query = "UPDATE \"user\" SET password = %s WHERE user_id = %s"
        return self.execute_query(query, (new_password, user_id))

    def check_course_code_exists(self, course_code, exclude_id=None):
        """Check if a course code already exists"""
        query = "SELECT course_id FROM course WHERE course_code = %s"
        params = [course_code]
        if exclude_id:
            query += " AND course_id != %s"
            params.append(exclude_id)
        return bool(self.fetch_one(query, tuple(params)))

    def update_course(self, course_id, course_data):
        """Update course information"""
        try:
            # Check if course code already exists (excluding current course)
            if self.check_course_code_exists(course_data['course_code'], course_id):
                return False, "Course code already exists"

            query = """
            UPDATE course 
            SET course_name = %s, course_code = %s, credits = %s, 
                ects = %s, level = %s, type = %s, department_id = %s
            WHERE course_id = %s
            """
            self.execute_query(query, (
                course_data['course_name'],
                course_data['course_code'],
                course_data['credits'],
                course_data['ects'],
                course_data['level'],
                course_data['type'],
                course_data['department_id'],
                course_id
            ))
            return True, "Course updated successfully"
        except Exception as e:
            return False, f"Failed to update course: {str(e)}"

    def create_course(self, course_name, course_code, credits, ects, level, type, department_id, creator_teacher_id=None):
        # If a teacher is creating, restrict department
        if creator_teacher_id is not None:
            teacher_dept = self.fetch_one("SELECT department_id FROM teacher WHERE teacher_id = %s", (creator_teacher_id,))
            if not teacher_dept or teacher_dept[0] != department_id:
                raise Exception("You can only add courses to your own department.")
        query = """
        INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING course_id
        """
        return self.fetch_one(query, (course_name, course_code, credits, ects, level, type, department_id))

    def get_all_offered_courses_for_student(self, student_id):
        """Get all courses offered in the current semester for the student's level and department restrictions, including instructor name"""
        # Get student info
        student = self.fetch_one("SELECT level, department_id FROM student WHERE student_id = %s", (student_id,))
        if not student:
            return []
        student_level, student_dept = student
        # Get current semester
        semester = self.get_current_semester()
        if not semester:
            return []
        semester_id = semester[0]
        # Only show courses that are offered in the current semester
        query = """
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.ects, c.level, c.type, d.department_name, u.first_name || ' ' || u.last_name as instructor_name
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN department d ON c.department_id = d.department_id
        JOIN teacher t ON co.instructor_id = t.teacher_id
        JOIN "user" u ON t.user_id = u.user_id
        WHERE co.semester_id = %s AND c.level = %s
        """
        params = [semester_id, student_level]
        # Department/type rules
        query += " AND (c.department_id = %s OR c.type IN ('Elective', 'Technical Elective'))"
        params.append(student_dept)
        return self.fetch_all(query, tuple(params)) 