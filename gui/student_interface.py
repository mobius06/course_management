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
        # Create buttons frame
        buttons_frame = ttk.Frame(self.available_courses_tab)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_available_courses
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for available courses
        columns = ('course_id', 'course_name', 'course_code', 'credits', 'ects', 'level', 'type', 'department')
        self.available_courses_tree = ttk.Treeview(
            self.available_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.available_courses_tree.heading('course_id', text='ID')
        self.available_courses_tree.heading('course_name', text='Course Name')
        self.available_courses_tree.heading('course_code', text='Course Code')
        self.available_courses_tree.heading('credits', text='Credits')
        self.available_courses_tree.heading('ects', text='ECTS')
        self.available_courses_tree.heading('level', text='Level')
        self.available_courses_tree.heading('type', text='Type')
        self.available_courses_tree.heading('department', text='Department')

        # Define columns
        self.available_courses_tree.column('course_id', width=50)
        self.available_courses_tree.column('course_name', width=200)
        self.available_courses_tree.column('course_code', width=100)
        self.available_courses_tree.column('credits', width=70)
        self.available_courses_tree.column('ects', width=70)
        self.available_courses_tree.column('level', width=100)
        self.available_courses_tree.column('type', width=100)
        self.available_courses_tree.column('department', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.available_courses_tab, orient=tk.VERTICAL, command=self.available_courses_tree.yview)
        self.available_courses_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.available_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.available_courses_tree.bind('<Double-1>', self.on_available_course_select)

        # Load initial data
        self.refresh_available_courses()

    def setup_enrolled_courses_tab(self):
        # Create buttons frame
        buttons_frame = ttk.Frame(self.enrolled_courses_tab)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_enrolled_courses
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for enrolled courses
        columns = ('course_id', 'course_name', 'course_code', 'credits', 'ects', 'level', 'type', 'department')
        self.enrolled_courses_tree = ttk.Treeview(
            self.enrolled_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.enrolled_courses_tree.heading('course_id', text='ID')
        self.enrolled_courses_tree.heading('course_name', text='Course Name')
        self.enrolled_courses_tree.heading('course_code', text='Course Code')
        self.enrolled_courses_tree.heading('credits', text='Credits')
        self.enrolled_courses_tree.heading('ects', text='ECTS')
        self.enrolled_courses_tree.heading('level', text='Level')
        self.enrolled_courses_tree.heading('type', text='Type')
        self.enrolled_courses_tree.heading('department', text='Department')

        # Define columns
        self.enrolled_courses_tree.column('course_id', width=50)
        self.enrolled_courses_tree.column('course_name', width=200)
        self.enrolled_courses_tree.column('course_code', width=100)
        self.enrolled_courses_tree.column('credits', width=70)
        self.enrolled_courses_tree.column('ects', width=70)
        self.enrolled_courses_tree.column('level', width=100)
        self.enrolled_courses_tree.column('type', width=100)
        self.enrolled_courses_tree.column('department', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.enrolled_courses_tab, orient=tk.VERTICAL, command=self.enrolled_courses_tree.yview)
        self.enrolled_courses_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.enrolled_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.enrolled_courses_tree.bind('<Double-1>', self.on_enrolled_course_select)

        # Load initial data
        self.refresh_enrolled_courses()

    def refresh_available_courses(self):
        # Clear existing items
        for item in self.available_courses_tree.get_children():
            self.available_courses_tree.delete(item)

        # Fetch and display available courses
        courses = self.db.get_all_courses()
        enrolled_courses = self.db.get_student_courses(self.user['user_id'])
        enrolled_course_ids = {course[0] for course in enrolled_courses}

        for course in courses:
            if course[0] not in enrolled_course_ids:
                self.available_courses_tree.insert('', tk.END, values=course)

    def refresh_enrolled_courses(self):
        # Clear existing items
        for item in self.enrolled_courses_tree.get_children():
            self.enrolled_courses_tree.delete(item)

        # Fetch and display enrolled courses
        courses = self.db.get_student_courses(self.user['user_id'])
        for course in courses:
            self.enrolled_courses_tree.insert('', tk.END, values=course)

    def on_available_course_select(self, event):
        # Get selected item
        item = self.available_courses_tree.selection()[0]
        course_id = self.available_courses_tree.item(item)['values'][0]
        
        # Show course details and enrollment dialog
        self.show_course_enrollment_dialog(course_id)

    def on_enrolled_course_select(self, event):
        # Get selected item
        item = self.enrolled_courses_tree.selection()[0]
        course_id = self.enrolled_courses_tree.item(item)['values'][0]
        
        # Show course details dialog
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
            ['Course ID', 'Course Name', 'Course Code', 'Credits', 'ECTS', 'Level', 'Type'],
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
            ['Course ID', 'Course Name', 'Course Code', 'Credits', 'ECTS', 'Level', 'Type'],
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
            self.db.enroll_student(self.user['user_id'], course_id)
            messagebox.showinfo("Success", "Successfully enrolled in course!")
            dialog.destroy()
            self.refresh_available_courses()
            self.refresh_enrolled_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll in course: {str(e)}")

    def drop_course(self, course_id, dialog):
        if messagebox.askyesno("Confirm Drop", "Are you sure you want to drop this course?"):
            try:
                query = "DELETE FROM enrolls_in WHERE user_id = %s AND course_id = %s"
                self.db.execute_query(query, (self.user['user_id'], course_id))
                messagebox.showinfo("Success", "Successfully dropped course!")
                dialog.destroy()
                self.refresh_available_courses()
                self.refresh_enrolled_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to drop course: {str(e)}") 