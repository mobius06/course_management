import psycopg2
from psycopg2 import Error
from config import DB_CONFIG
import hashlib
import secrets

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("Successfully connected to the database")
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
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${hashed}"

    def verify_password(self, stored_password, provided_password):
        """Verify a password against its hash"""
        try:
            expected = f'salt${provided_password}'
            return stored_password == expected
        except Exception as e:
            print(f"Error in verify_password: {str(e)}")
            return False

    # User operations
    def get_user(self, username):
        query = "SELECT * FROM \"user\" WHERE username = %s"
        return self.fetch_one(query, (username,))

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM \"user\" WHERE user_id = %s"
        return self.fetch_one(query, (user_id,))

    def get_all_users(self):
        query = "SELECT user_id, username, role, created_at FROM \"user\" ORDER BY user_id"
        return self.fetch_all(query)

    def create_user(self, username, password, role):
        hashed_password = self.hash_password(password)
        query = """
        INSERT INTO \"user\" (username, password, role) 
        VALUES (%s, %s, %s) 
        RETURNING user_id
        """
        return self.fetch_one(query, (username, hashed_password, role))

    def authenticate_user(self, username, password):
        user = self.get_user(username)
        print(f"Found user: {user}")
        if user and self.verify_password(user[4], password):  # user[4] is the password field
            return user
        return None

    def update_user_password(self, user_id, new_password):
        hashed_password = self.hash_password(new_password)
        query = "UPDATE \"user\" SET password = %s WHERE user_id = %s"
        return self.execute_query(query, (hashed_password, user_id))

    # Course operations
    def get_all_courses(self):
        query = """
        SELECT c.*, d.department_name 
        FROM course c 
        JOIN department d ON c.department_id = d.department_id
        """
        return self.fetch_all(query)

    def get_course_by_id(self, course_id):
        query = "SELECT * FROM course WHERE course_id = %s"
        return self.fetch_one(query, (course_id,))

    # Department operations
    def get_all_departments(self):
        query = "SELECT * FROM department"
        return self.fetch_all(query)

    # Semester operations
    def get_all_semesters(self):
        query = "SELECT * FROM semester"
        return self.fetch_all(query)

    # Enrollment operations
    def enroll_student(self, user_id, course_id):
        query = "INSERT INTO enrolls_in (user_id, course_id) VALUES (%s, %s)"
        return self.execute_query(query, (user_id, course_id))

    def get_student_courses(self, user_id):
        query = """
        SELECT c.*, d.department_name 
        FROM course c 
        JOIN enrolls_in e ON c.course_id = e.course_id 
        JOIN department d ON c.department_id = d.department_id
        WHERE e.user_id = %s
        """
        return self.fetch_all(query, (user_id,))

    # Course offering operations
    def get_course_offerings(self, semester_id=None):
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, co.instructor_id, s.semester_name, co.year
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        """
        if semester_id:
            query += " WHERE co.semester_id = %s"
            return self.fetch_all(query, (semester_id,))
        return self.fetch_all(query)

    def get_teaching_courses(self, instructor_id):
        query = """
        SELECT co.offering_id, c.course_name, c.course_code, s.semester_name, co.year
        FROM course_offering co
        JOIN course c ON co.course_id = c.course_id
        JOIN semester s ON co.semester_id = s.semester_id
        WHERE co.instructor_id = %s
        """
        return self.fetch_all(query, (instructor_id,)) 