import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class StudentInterface(ttk.Frame):
    def __init__(self, parent, db, user):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.setup_ui()

    def setup_ui(self):
        # Welcome label
        welcome_label = ttk.Label(self, text=f"Welcome, {self.user.get('full_name', self.user.get('username', 'User'))}!", font=("Helvetica", 14, "bold"))
        welcome_label.pack(pady=(10, 0))

        # Create main container
        self.main_container = ttk.Frame(self)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.available_courses_tab = ttk.Frame(self.notebook)
        self.enrolled_courses_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.available_courses_tab, text="Available Courses")
        self.notebook.add(self.enrolled_courses_tab, text="Enrolled Courses")

        # Setup available courses tab
        self.setup_available_courses_tab()
        
        # Setup enrolled courses tab
        self.setup_enrolled_courses_tab()

    def setup_available_courses_tab(self):
        # Create Treeview for available courses
        columns = ('course_id', 'course_name', 'course_code', 'credits', 'ects', 'level', 'type', 'department', 'instructor')
        self.available_tree = ttk.Treeview(
            self.available_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.available_tree.heading('course_id', text='ID')
        self.available_tree.heading('course_name', text='Course Name')
        self.available_tree.heading('course_code', text='Course Code')
        self.available_tree.heading('credits', text='Credits')
        self.available_tree.heading('ects', text='ECTS')
        self.available_tree.heading('level', text='Level')
        self.available_tree.heading('type', text='Type')
        self.available_tree.heading('department', text='Department')
        self.available_tree.heading('instructor', text='Instructor')

        # Define columns
        self.available_tree.column('course_id', width=50)
        self.available_tree.column('course_name', width=200)
        self.available_tree.column('course_code', width=100)
        self.available_tree.column('credits', width=70)
        self.available_tree.column('ects', width=70)
        self.available_tree.column('level', width=100)
        self.available_tree.column('type', width=150)
        self.available_tree.column('department', width=150)
        self.available_tree.column('instructor', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.available_courses_tab, orient=tk.VERTICAL, command=self.available_tree.yview)
        self.available_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.available_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.available_tree.bind('<Double-1>', self.on_available_course_select)

        # Load initial data
        self.refresh_available_courses()

    def setup_enrolled_courses_tab(self):
        # Create Treeview for enrolled courses
        columns = ('course_id', 'course_name', 'course_code', 'credits', 'ects', 'level', 'type', 'department', 'semester', 'year')
        self.enrolled_tree = ttk.Treeview(
            self.enrolled_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.enrolled_tree.heading('course_id', text='ID')
        self.enrolled_tree.heading('course_name', text='Course Name')
        self.enrolled_tree.heading('course_code', text='Course Code')
        self.enrolled_tree.heading('credits', text='Credits')
        self.enrolled_tree.heading('ects', text='ECTS')
        self.enrolled_tree.heading('level', text='Level')
        self.enrolled_tree.heading('type', text='Type')
        self.enrolled_tree.heading('department', text='Department')
        self.enrolled_tree.heading('semester', text='Semester')
        self.enrolled_tree.heading('year', text='Year')

        # Define columns
        self.enrolled_tree.column('course_id', width=50)
        self.enrolled_tree.column('course_name', width=200)
        self.enrolled_tree.column('course_code', width=100)
        self.enrolled_tree.column('credits', width=70)
        self.enrolled_tree.column('ects', width=70)
        self.enrolled_tree.column('level', width=100)
        self.enrolled_tree.column('type', width=150)
        self.enrolled_tree.column('department', width=150)
        self.enrolled_tree.column('semester', width=150)
        self.enrolled_tree.column('year', width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.enrolled_courses_tab, orient=tk.VERTICAL, command=self.enrolled_tree.yview)
        self.enrolled_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.enrolled_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.enrolled_tree.bind('<Double-1>', self.on_enrolled_course_select)

        # Load initial data
        self.refresh_enrolled_courses()

    def refresh_available_courses(self):
        # Clear existing items
        for item in self.available_tree.get_children():
            self.available_tree.delete(item)

        # Get student ID
        student = self.db.get_student(self.user['user_id'])
        if not student:
            return

        # Get all offered courses for the student (with instructor)
        courses = self.db.get_all_offered_courses_for_student(student[0])
        # courses: (course_id, course_name, course_code, credits, ects, level, type, department_name, instructor_name)
        # Remove already enrolled courses
        enrolled_courses = self.db.get_student_courses(student[0])  # student[0] is student_id
        enrolled_course_ids = {course[0] for course in enrolled_courses}

        for course in courses:
            if course[0] not in enrolled_course_ids:
                self.available_tree.insert('', tk.END, values=course)

    def refresh_enrolled_courses(self):
        # Clear existing items
        for item in self.enrolled_tree.get_children():
            self.enrolled_tree.delete(item)

        # Get student ID
        student = self.db.get_student(self.user['user_id'])
        if not student:
            return

        # Fetch and display enrolled courses
        courses = self.db.get_student_courses(student[0])  # student[0] is student_id
        for course in courses:
            self.enrolled_tree.insert('', tk.END, values=course)

    def on_available_course_select(self, event):
        # Get selected item
        item = self.available_tree.selection()[0]
        course_id = self.available_tree.item(item)['values'][0]
        
        # Show course enrollment dialog
        self.show_course_enrollment_dialog(course_id)

    def on_enrolled_course_select(self, event):
        # Get selected item
        item = self.enrolled_tree.selection()[0]
        course_id = self.enrolled_tree.item(item)['values'][0]
        
        # Show course details
        self.show_course_details(course_id)

    def show_course_enrollment_dialog(self, course_id):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Course Enrollment")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found")
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display course details
        row = 0
        for label, value in zip(
            ['Course ID', 'Course Name', 'Course Code', 'Credits', 'ECTS', 'Level', 'Type', 'Department'],
            course
        ):
            ttk.Label(details_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=str(value)).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        # Add enroll button
        enroll_btn = ttk.Button(
            details_frame,
            text="Enroll in Course",
            command=lambda: self.enroll_in_course(course_id, dialog)
        )
        enroll_btn.grid(row=row, column=0, columnspan=2, pady=20)

    def show_course_details(self, course_id):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Course Details")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found")
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display course details
        row = 0
        for label, value in zip(
            ['Course ID', 'Course Name', 'Course Code', 'Credits', 'ECTS', 'Level', 'Type', 'Department'],
            course
        ):
            ttk.Label(details_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=str(value)).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        # Add drop course button
        drop_btn = ttk.Button(
            details_frame,
            text="Drop Course",
            command=lambda: self.drop_course(course_id, dialog)
        )
        drop_btn.grid(row=row, column=0, columnspan=2, pady=20)

    def enroll_in_course(self, course_id, dialog):
        try:
            # Get student ID
            student = self.db.get_student(self.user['user_id'])
            if not student:
                messagebox.showerror("Error", "Student not found")
                return

            # Check if already enrolled
            if self.db.is_student_enrolled(student[0], course_id):
                messagebox.showerror("Error", "Already enrolled in this course")
                return

            # Enroll student
            success, message = self.db.enroll_student(student[0], course_id)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                # Refresh both course lists
                self.refresh_available_courses()
                self.refresh_enrolled_courses()
            else:
                messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll in course: {str(e)}")

    def drop_course(self, course_id, dialog):
        if messagebox.askyesno("Confirm Drop", "Are you sure you want to drop this course?"):
            try:
                # Get student ID
                student = self.db.get_student(self.user['user_id'])
                if not student:
                    messagebox.showerror("Error", "Student not found")
                    return

                query = "DELETE FROM enrolls_in WHERE student_id = %s AND course_id = %s"
                self.db.execute_query(query, (student[0], course_id))
                messagebox.showinfo("Success", "Successfully dropped course!")
                dialog.destroy()
                self.refresh_available_courses()
                self.refresh_enrolled_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to drop course: {str(e)}") 