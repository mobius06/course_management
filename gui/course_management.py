import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class CourseManagementFrame(ttk.Frame):
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

        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_container)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Add Course button
        add_course_btn = ttk.Button(
            buttons_frame,
            text="Add Course",
            command=self.show_add_course_dialog
        )
        add_course_btn.pack(side=tk.LEFT, padx=5)

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_courses
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for courses
        columns = ('course_id', 'course_name', 'course_code', 'credits', 'ects', 'level', 'type', 'department')
        self.tree = ttk.Treeview(
            self.main_container,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.tree.heading('course_id', text='ID')
        self.tree.heading('course_name', text='Course Name')
        self.tree.heading('course_code', text='Course Code')
        self.tree.heading('credits', text='Credits')
        self.tree.heading('ects', text='ECTS')
        self.tree.heading('level', text='Level')
        self.tree.heading('type', text='Type')
        self.tree.heading('department', text='Department')

        # Define columns
        self.tree.column('course_id', width=50)
        self.tree.column('course_name', width=200)
        self.tree.column('course_code', width=100)
        self.tree.column('credits', width=70)
        self.tree.column('ects', width=70)
        self.tree.column('level', width=100)
        self.tree.column('type', width=150)
        self.tree.column('department', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_course_select)

        # Load initial data
        self.refresh_courses()

    def refresh_courses(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display courses
        courses = self.db.get_all_courses()
        for course in courses:
            self.tree.insert('', tk.END, values=course)

    def show_add_course_dialog(self):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add New Course")
        dialog.geometry("420x540")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Add New Course", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course Name
        ttk.Label(form_frame, text="Course Name:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=4)
        course_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=course_name_var, font=("Helvetica", 11)).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Course Code
        ttk.Label(form_frame, text="Course Code:", font=("Helvetica", 11)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=4)
        course_code_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=course_code_var, font=("Helvetica", 11)).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Credits
        ttk.Label(form_frame, text="Credits:", font=("Helvetica", 11)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=4)
        credits_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=credits_var, font=("Helvetica", 11)).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # ECTS
        ttk.Label(form_frame, text="ECTS:", font=("Helvetica", 11)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=4)
        ects_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=ects_var, font=("Helvetica", 11)).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Level
        ttk.Label(form_frame, text="Level:", font=("Helvetica", 11)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=4)
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(form_frame, textvariable=level_var, font=("Helvetica", 11))
        level_combo['values'] = ('Bachelor', 'Master')
        level_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Type
        ttk.Label(form_frame, text="Type:", font=("Helvetica", 11)).grid(row=5, column=0, sticky=tk.W, pady=8, padx=4)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, font=("Helvetica", 11))
        type_combo['values'] = ('Must', 'Elective', 'Technical Elective')
        type_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Department
        ttk.Label(form_frame, text="Department:", font=("Helvetica", 11)).grid(row=6, column=0, sticky=tk.W, pady=8, padx=4)
        department_var = tk.StringVar()
        departments = self.db.get_all_departments()
        department_combo = ttk.Combobox(form_frame, textvariable=department_var, font=("Helvetica", 11))
        department_combo['values'] = [dept[1] for dept in departments]
        department_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        form_frame.columnconfigure(1, weight=1)

        def save_course():
            try:
                # Validate required fields
                if not all([course_name_var.get(), course_code_var.get(), credits_var.get(), 
                          ects_var.get(), level_var.get(), type_var.get(), department_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields", parent=dialog)
                    return

                # Check for duplicate course code
                if self.db.check_course_code_exists(course_code_var.get()):
                    messagebox.showerror("Error", "This course code already exists.", parent=dialog)
                    return

                # Get department ID
                dept_name = department_var.get()
                dept_id = next(dept[0] for dept in departments if dept[1] == dept_name)

                # Insert course
                query = """
                INSERT INTO course (course_name, course_code, credits, ects, level, type, department_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                self.db.execute_query(query, (
                    course_name_var.get(),
                    course_code_var.get(),
                    int(credits_var.get()),
                    int(ects_var.get()),
                    level_var.get(),
                    type_var.get(),
                    dept_id
                ))
                messagebox.showinfo("Success", "Course added successfully!", parent=dialog)
                dialog.destroy()
                self.refresh_courses()
            except ValueError:
                messagebox.showerror("Error", "Credits and ECTS must be numbers", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {str(e)}", parent=dialog)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        save_btn = ttk.Button(button_frame, text="Save", width=14, command=save_course)
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=14, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

    def on_course_select(self, event):
        # Get selected item
        item = self.tree.selection()[0]
        course_id = self.tree.item(item)['values'][0]
        
        # Show course details dialog
        self.show_course_details(course_id)

    def show_course_details(self, course_id):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Course Details")
        dialog.geometry("420x340")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Course Details", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found", parent=dialog)
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="24 18 24 18")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display course details
        labels = ['Course ID', 'Course Name', 'Course Code', 'Credits', 'ECTS', 'Level', 'Type', 'Department']
        for row, (label, value) in enumerate(zip(labels, course)):
            ttk.Label(details_frame, text=f"{label}:", font=("Helvetica", 11, "bold")).grid(row=row, column=0, sticky=tk.W, pady=8, padx=4)
            ttk.Label(details_frame, text=str(value), font=("Helvetica", 11)).grid(row=row, column=1, sticky=tk.W, pady=8, padx=4)
        details_frame.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        edit_btn = ttk.Button(button_frame, text="Edit", width=12, command=lambda: [dialog.destroy(), self.edit_course(course_id, dialog)])
        edit_btn.pack(side=tk.RIGHT, padx=8)
        delete_btn = ttk.Button(button_frame, text="Delete", width=12, command=lambda: self.delete_course(course_id, dialog))
        delete_btn.pack(side=tk.RIGHT, padx=8)

    def edit_course(self, course_id, parent_dialog=None):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Edit Course")
        dialog.geometry("420x540")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Edit Course", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found", parent=dialog)
            dialog.destroy()
            return

        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course Name
        ttk.Label(form_frame, text="Course Name:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=4)
        course_name_var = tk.StringVar(value=course[1])
        ttk.Entry(form_frame, textvariable=course_name_var, font=("Helvetica", 11)).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Course Code
        ttk.Label(form_frame, text="Course Code:", font=("Helvetica", 11)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=4)
        course_code_var = tk.StringVar(value=course[2])
        ttk.Entry(form_frame, textvariable=course_code_var, font=("Helvetica", 11)).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Credits
        ttk.Label(form_frame, text="Credits:", font=("Helvetica", 11)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=4)
        credits_var = tk.StringVar(value=str(course[3]))
        ttk.Entry(form_frame, textvariable=credits_var, font=("Helvetica", 11)).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # ECTS
        ttk.Label(form_frame, text="ECTS:", font=("Helvetica", 11)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=4)
        ects_var = tk.StringVar(value=str(course[4]))
        ttk.Entry(form_frame, textvariable=ects_var, font=("Helvetica", 11)).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Level
        ttk.Label(form_frame, text="Level:", font=("Helvetica", 11)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=4)
        level_var = tk.StringVar(value=course[5])
        level_combo = ttk.Combobox(form_frame, textvariable=level_var, font=("Helvetica", 11))
        level_combo['values'] = ('Bachelor', 'Master')
        level_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Type
        ttk.Label(form_frame, text="Type:", font=("Helvetica", 11)).grid(row=5, column=0, sticky=tk.W, pady=8, padx=4)
        type_var = tk.StringVar(value=course[6])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var, font=("Helvetica", 11))
        type_combo['values'] = ('Must', 'Elective', 'Technical Elective')
        type_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Department
        ttk.Label(form_frame, text="Department:", font=("Helvetica", 11)).grid(row=6, column=0, sticky=tk.W, pady=8, padx=4)
        department_var = tk.StringVar(value=course[7])  # department name
        departments = self.db.get_all_departments()
        department_combo = ttk.Combobox(form_frame, textvariable=department_var, font=("Helvetica", 11))
        department_combo['values'] = [dept[1] for dept in departments]
        department_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        form_frame.columnconfigure(1, weight=1)

        def save_changes():
            try:
                # Validate required fields
                if not all([course_name_var.get(), course_code_var.get(), credits_var.get(), ects_var.get(), level_var.get(), type_var.get(), department_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields", parent=dialog)
                    return
                # Get department ID
                dept_name = department_var.get()
                dept_id = next(dept[0] for dept in departments if dept[1] == dept_name)
                # Update course
                query = """
                UPDATE course 
                SET course_name = %s, course_code = %s, credits = %s, ects = %s, 
                    level = %s, type = %s, department_id = %s
                WHERE course_id = %s
                """
                self.db.execute_query(query, (
                    course_name_var.get(),
                    course_code_var.get(),
                    int(credits_var.get()),
                    int(ects_var.get()),
                    level_var.get(),
                    type_var.get(),
                    dept_id,
                    course_id
                ))
                messagebox.showinfo("Success", "Course updated successfully!", parent=dialog)
                dialog.destroy()
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_courses()
            except ValueError:
                messagebox.showerror("Error", "Credits and ECTS must be numbers", parent=dialog)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course: {str(e)}", parent=dialog)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        save_btn = ttk.Button(button_frame, text="Save Changes", width=14, command=save_changes)
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=14, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

    def delete_course(self, course_id, parent_dialog=None):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
            try:
                query = "DELETE FROM course WHERE course_id = %s"
                self.db.execute_query(query, (course_id,))
                messagebox.showinfo("Success", "Course deleted successfully!")
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course: {str(e)}") 