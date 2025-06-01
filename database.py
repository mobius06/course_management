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
        """Hash a password using SHA-256 with a random salt"""
        salt = secrets.token_hex(16)
        # Ensure password is encoded as UTF-8
        password_bytes = password.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
        # Combine password and salt
        combined = password_bytes + salt_bytes
        # Generate hash
        hashed = hashlib.sha256(combined).hexdigest()
        return f"{salt}${hashed}"

    def verify_password(self, stored_password, provided_password):
        """Verify a password against its hash"""
        try:
            salt, hashed = stored_password.split('$')
            # Ensure password is encoded as UTF-8
            password_bytes = provided_password.encode('utf-8')
            salt_bytes = salt.encode('utf-8')
            # Combine password and salt
            combined = password_bytes + salt_bytes
            # Generate hash
            expected = hashlib.sha256(combined).hexdigest()
            return hashed == expected
        except Exception as e:
            print(f"Error in verify_password: {str(e)}")
            return False

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

    def create_user(self, username, password, role):
        """Create a new user with password"""
        try:
            # Check if username already exists
            if self.check_username_exists(username):
                return False

            # Hash password
            hashed_password = self.hash_password(password)

            # Insert user
            query = """
            INSERT INTO "user" (username, password, role)
            VALUES (%s, %s, %s)
            """
            self.execute_query(query, (username, hashed_password, role.lower()))
            return True
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return False

    def update_user(self, user_id, username, password=None, role=None):
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
                hashed_password = self.hash_password(password)
                update_fields.append("password = %s")
                params.append(hashed_password)

            if role:
                update_fields.append("role = %s")
                params.append(role.lower())

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
        print(f"Stored password hash: {user[2]}")
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

    def create_student(self, user_id, student_number, first_name, last_name, email, department_id):
        query = """
        INSERT INTO student (user_id, student_number, first_name, last_name, email, department_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING student_id
        """
        return self.fetch_one(query, (user_id, student_number, first_name, last_name, email, department_id))

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
        query = "SELECT * FROM enrolls_in WHERE user_id = %s AND course_id = %s"
        return bool(self.fetch_one(query, (student_id, course_id)))

    def get_student_courses(self, student_id):
        """Get courses enrolled by a student with proper semester and year information"""
        query = """
        SELECT c.course_id, c.course_name, c.course_code, c.credits, c.ects, 
               c.level, c.type, d.department_name, s.semester_name, co.year
        FROM course c 
        JOIN enrolls_in e ON c.course_id = e.course_id 
        JOIN department d ON c.department_id = d.department_id
        JOIN course_offering co ON c.course_id = co.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        WHERE e.user_id = %s
        ORDER BY co.year DESC, s.semester_name
        """
        return self.fetch_all(query, (student_id,))

    def enroll_student(self, student_id, course_id):
        """Enroll a student in a course with proper validation"""
        try:
            # Start transaction
            self.connection.autocommit = False
            
            # Check if already enrolled
            if self.is_student_enrolled(student_id, course_id):
                return False, "Already enrolled in this course"
            
            # Check if course is available for enrollment
            query = """
            SELECT co.offering_id 
            FROM course_offering co
            JOIN semester s ON co.semester_id = s.semester_id
            WHERE co.course_id = %s 
            AND s.start_date <= CURRENT_DATE 
            AND s.end_date >= CURRENT_DATE
            """
            if not self.fetch_one(query, (course_id,)):
                return False, "Course is not available for enrollment"
            
            # Perform enrollment
            enroll_query = "INSERT INTO enrolls_in (user_id, course_id) VALUES (%s, %s)"
            self.execute_query(enroll_query, (student_id, course_id))
            
            # Commit transaction
            self.connection.commit()
            return True, "Successfully enrolled in course"
        except Exception as e:
            self.connection.rollback()
            return False, f"Failed to enroll: {str(e)}"

    # Course offering operations
    def get_course_offerings(self, semester_id=None):
        """Get course offerings with department names"""
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, 
               s.semester_name, co.year, d.department_name
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        JOIN department d ON c.department_id = d.department_id
        """
        if semester_id:
            query += " WHERE co.semester_id = %s"
            return self.fetch_all(query, (semester_id,))
        return self.fetch_all(query)

    def get_teaching_courses(self, teacher_id):
        """Get courses taught by a teacher with department names"""
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, 
               s.semester_name, co.year, d.department_name
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        JOIN department d ON c.department_id = d.department_id
        WHERE co.instructor_id = %s
        ORDER BY co.year DESC, s.semester_name
        """
        return self.fetch_all(query, (teacher_id,))

    def create_course_offering(self, course_id, semester_id, instructor_id, year):
        query = """
        INSERT INTO course_offering (course_id, semester_id, instructor_id, year)
        VALUES (%s, %s, %s, %s)
        RETURNING offering_id
        """
        return self.fetch_one(query, (course_id, semester_id, instructor_id, year))

    def update_course_offering(self, offering_id, course_id, semester_id, instructor_id, year):
        query = """
        UPDATE course_offering 
        SET course_id = %s, semester_id = %s, instructor_id = %s, year = %s
        WHERE offering_id = %s
        """
        return self.execute_query(query, (course_id, semester_id, instructor_id, year, offering_id))

    def update_user_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)
        query = "UPDATE \"user\" SET password = %s WHERE user_id = %s"
        return self.execute_query(query, (hashed_password, user_id))

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