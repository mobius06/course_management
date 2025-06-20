import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class TeacherInterface(ttk.Frame):
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
        self.teaching_courses_tab = ttk.Frame(self.notebook)
        self.course_offerings_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.teaching_courses_tab, text="Teaching Courses")
        self.notebook.add(self.course_offerings_tab, text="Course Offerings")

        # Setup teaching courses tab
        self.setup_teaching_courses_tab()
        
        # Setup course offerings tab
        self.setup_course_offerings_tab()

    def setup_teaching_courses_tab(self):
        # Create buttons frame
        buttons_frame = ttk.Frame(self.teaching_courses_tab)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Add Course button
        add_course_btn = ttk.Button(
            buttons_frame,
            text="Add Course",
            command=self.show_add_course_dialog
        )
        add_course_btn.pack(side=tk.LEFT, padx=5)

        # Add buttons
        edit_btn = ttk.Button(
            buttons_frame,
            text="Edit Course",
            command=self.edit_teaching_course
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_teaching_courses
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for teaching courses
        columns = ('offering_id', 'course_name', 'course_code', 'semester', 'year', 'department')
        self.teaching_tree = ttk.Treeview(
            self.teaching_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.teaching_tree.heading('offering_id', text='ID')
        self.teaching_tree.heading('course_name', text='Course Name')
        self.teaching_tree.heading('course_code', text='Course Code')
        self.teaching_tree.heading('semester', text='Semester')
        self.teaching_tree.heading('year', text='Year')
        self.teaching_tree.heading('department', text='Department')

        # Define columns
        self.teaching_tree.column('offering_id', width=50)
        self.teaching_tree.column('course_name', width=200)
        self.teaching_tree.column('course_code', width=100)
        self.teaching_tree.column('semester', width=150)
        self.teaching_tree.column('year', width=100)
        self.teaching_tree.column('department', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.teaching_courses_tab, orient=tk.VERTICAL, command=self.teaching_tree.yview)
        self.teaching_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.teaching_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.teaching_tree.bind('<Double-1>', self.on_teaching_course_select)

        # Load initial data
        self.refresh_teaching_courses()

    def setup_course_offerings_tab(self):
        # Create buttons frame
        buttons_frame = ttk.Frame(self.course_offerings_tab)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Add Course Offering button
        add_offering_btn = ttk.Button(
            buttons_frame,
            text="Add Course Offering",
            command=self.show_add_offering_dialog
        )
        add_offering_btn.pack(side=tk.LEFT, padx=5)

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_course_offerings
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Remove button
        remove_btn = ttk.Button(
            buttons_frame,
            text="Remove Offering",
            command=self.remove_course_offering
        )
        remove_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for course offerings
        columns = ('offering_id', 'course_name', 'course_code', 'semester', 'year', 'department')
        self.offerings_tree = ttk.Treeview(
            self.course_offerings_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.offerings_tree.heading('offering_id', text='ID')
        self.offerings_tree.heading('course_name', text='Course Name')
        self.offerings_tree.heading('course_code', text='Course Code')
        self.offerings_tree.heading('semester', text='Semester')
        self.offerings_tree.heading('year', text='Year')
        self.offerings_tree.heading('department', text='Department')

        # Define columns
        self.offerings_tree.column('offering_id', width=50)
        self.offerings_tree.column('course_name', width=200)
        self.offerings_tree.column('course_code', width=100)
        self.offerings_tree.column('semester', width=150)
        self.offerings_tree.column('year', width=100)
        self.offerings_tree.column('department', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.course_offerings_tab, orient=tk.VERTICAL, command=self.offerings_tree.yview)
        self.offerings_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.offerings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.offerings_tree.bind('<Double-1>', self.on_offering_select)

        # Load initial data
        self.refresh_course_offerings()

    def refresh_teaching_courses(self):
        # Clear existing items
        for item in self.teaching_tree.get_children():
            self.teaching_tree.delete(item)

        # Get teacher ID
        teacher = self.db.get_teacher(self.user['user_id'])
        if not teacher:
            return

        # Fetch and display teaching courses
        courses = self.db.get_teaching_courses(teacher[0])  # teacher[0] is teacher_id
        
        # Group courses by semester and year
        current_semester = None
        current_year = None
        
        for course in courses:
            semester = course[3]  # semester_name
            year = course[4]      # year
            # Add header if semester/year changes
            if semester != current_semester or year != current_year:
                # Add semester/year header
                header = f"{semester} {year}"
                self.teaching_tree.insert('', tk.END, values=('', header, '', '', '', ''), tags=('header',))
                current_semester = semester
                current_year = year
            # Add course
            self.teaching_tree.insert('', tk.END, values=course, tags=('course',))

        # Configure tags for styling
        self.teaching_tree.tag_configure('header', background='#f0f0f0', font=('TkDefaultFont', 10, 'bold'))
        self.teaching_tree.tag_configure('course', background='white')

    def refresh_course_offerings(self):
        # Clear existing items
        for item in self.offerings_tree.get_children():
            self.offerings_tree.delete(item)

        # Fetch and display course offerings with department name
        offerings = self.db.get_course_offerings()
        for offering in offerings:
            self.offerings_tree.insert('', tk.END, values=offering)

    def show_add_offering_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Course Offering")
        dialog.geometry("420x340")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Add Course Offering", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course selection
        ttk.Label(form_frame, text="Course:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=4)
        course_var = tk.StringVar()
        courses = self.db.get_all_courses()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var, font=("Helvetica", 11))
        course_combo['values'] = [f"{course[2]} - {course[1]}" for course in courses]
        course_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Semester selection
        ttk.Label(form_frame, text="Semester:", font=("Helvetica", 11)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=4)
        semester_var = tk.StringVar()
        semesters = self.db.get_all_semesters()
        semester_combo = ttk.Combobox(form_frame, textvariable=semester_var, font=("Helvetica", 11))
        semester_combo['values'] = [sem[1] for sem in semesters]
        semester_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        form_frame.columnconfigure(1, weight=1)

        def save_offering():
            try:
                # Validate required fields
                if not all([course_var.get(), semester_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields", parent=dialog)
                    return
                # Get course ID
                course_code = course_var.get().split(' - ')[0]
                course_id = next(course[0] for course in courses if course[2] == course_code)
                # Get semester ID
                semester_name = semester_var.get()
                semester_id = next(sem[0] for sem in semesters if sem[1] == semester_name)
                # Get teacher ID
                teacher = self.db.get_teacher(self.user['user_id'])
                if not teacher:
                    messagebox.showerror("Error", "Teacher not found", parent=dialog)
                    return
                # Create course offering
                self.db.create_course_offering(
                    course_id,
                    semester_id,
                    teacher[0]  # teacher_id
                )
                messagebox.showinfo("Success", "Course offering added successfully!", parent=dialog)
                dialog.destroy()
                self.refresh_course_offerings()
                self.refresh_teaching_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course offering: {str(e)}", parent=dialog)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        save_btn = ttk.Button(button_frame, text="Save", width=14, command=save_offering)
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=14, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

    def on_teaching_course_select(self, event):
        # Get selected item
        item = self.teaching_tree.selection()[0]
        values = self.teaching_tree.item(item)['values']
        offering_id = values[0]
        # Ignore header/separator/empty rows
        if not offering_id or offering_id == '':
            return
        # Show course offering details
        self.show_course_offering_details(offering_id)

    def on_offering_select(self, event):
        # Get selected item
        item = self.offerings_tree.selection()[0]
        offering_id = self.offerings_tree.item(item)['values'][0]
        
        # Show course offering details
        self.show_course_offering_details(offering_id)

    def show_course_offering_details(self, offering_id):
        dialog = tk.Toplevel(self)
        dialog.title("Course Offering Details")
        dialog.geometry("420x340")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Course Offering Details", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get course offering details
        offering = next(
            (o for o in self.db.get_course_offerings() if o[0] == offering_id),
            None
        )
        if not offering:
            messagebox.showerror("Error", "Course offering not found", parent=dialog)
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="24 18 24 18")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display course offering details
        labels = ['Offering ID', 'Course Name', 'Course Code', 'Semester', 'Year', 'Department']
        for row, (label, value) in enumerate(zip(labels, offering)):
            ttk.Label(details_frame, text=f"{label}:", font=("Helvetica", 11, "bold")).grid(row=row, column=0, sticky=tk.W, pady=8, padx=4)
            ttk.Label(details_frame, text=str(value), font=("Helvetica", 11)).grid(row=row, column=1, sticky=tk.W, pady=8, padx=4)
        details_frame.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        teacher = self.db.get_teacher(self.user['user_id'])
        if teacher and offering[3] == teacher[0]:  # instructor_id
            edit_btn = ttk.Button(button_frame, text="Edit", width=12, command=lambda: [dialog.destroy(), self.edit_course_offering(offering_id, dialog)])
            edit_btn.pack(side=tk.RIGHT, padx=8)
            delete_btn = ttk.Button(button_frame, text="Delete", width=12, command=lambda: self.delete_course_offering(offering_id, dialog))
            delete_btn.pack(side=tk.RIGHT, padx=8)

    def edit_course_offering(self, offering_id, parent_dialog=None):
        dialog = tk.Toplevel(self)
        dialog.title("Edit Course Offering")
        dialog.geometry("420x540")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Edit Course Offering", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get selected item
        selection = self.teaching_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to edit")
            return
        item = selection[0]
        values = self.teaching_tree.item(item)['values']
        course_id = None
        # Find course_id from offering_id
        offering_id = values[0]
        offering = next((o for o in self.db.get_course_offerings() if o[0] == offering_id), None)
        if offering:
            course_code = offering[2]
            course = next((c for c in self.db.get_all_courses() if c[2] == course_code), None)
            if course:
                course_id = course[0]
        if not course_id:
            messagebox.showerror("Error", "Course not found")
            return
        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found")
            return
        # Get teacher info
        teacher = self.db.get_teacher(self.user['user_id'])
        if not teacher:
            messagebox.showerror("Error", "Teacher not found")
            dialog.destroy()
            return
        department_id = teacher[3]  # department_id
        department_name = self.db.get_department_name(department_id)
        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18", font=("Helvetica", 11))
        form_frame.pack(fill=tk.BOTH, expand=True)
        # Course Name
        ttk.Label(form_frame, text="Course Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_name_var = tk.StringVar(value=course[1])
        ttk.Entry(form_frame, textvariable=course_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        # Course Code
        ttk.Label(form_frame, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        course_code_var = tk.StringVar(value=course[2])
        ttk.Entry(form_frame, textvariable=course_code_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        # Credits
        ttk.Label(form_frame, text="Credits:").grid(row=2, column=0, sticky=tk.W, pady=5)
        credits_var = tk.StringVar(value=str(course[3]))
        ttk.Entry(form_frame, textvariable=credits_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        # ECTS
        ttk.Label(form_frame, text="ECTS:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ects_var = tk.StringVar(value=str(course[4]))
        ttk.Entry(form_frame, textvariable=ects_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        # Level
        ttk.Label(form_frame, text="Level:").grid(row=4, column=0, sticky=tk.W, pady=5)
        level_var = tk.StringVar(value=course[5])
        level_combo = ttk.Combobox(form_frame, textvariable=level_var)
        level_combo['values'] = ('Bachelor', 'Master')
        level_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        # Type
        ttk.Label(form_frame, text="Type:").grid(row=5, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value=course[6])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var)
        type_combo['values'] = ('Must', 'Elective', 'Technical Elective')
        type_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        # Department (fixed)
        ttk.Label(form_frame, text="Department:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(form_frame, text=department_name).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)
        def save_changes():
            try:
                # Validate required fields
                if not all([course_name_var.get(), course_code_var.get(), credits_var.get(), ects_var.get(), level_var.get(), type_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return
                # Update course
                result, msg = self.db.update_course(course_id, {
                    'course_name': course_name_var.get(),
                    'course_code': course_code_var.get(),
                    'credits': int(credits_var.get()),
                    'ects': int(ects_var.get()),
                    'level': level_var.get(),
                    'type': type_var.get(),
                    'department_id': department_id
                })
                if result:
                    messagebox.showinfo("Success", "Course updated successfully!")
                    dialog.destroy()
                    self.refresh_teaching_courses()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course: {str(e)}")
        save_btn = ttk.Button(form_frame, text="Save Changes", command=save_changes)
        save_btn.grid(row=7, column=0, columnspan=2, pady=20)
        form_frame.columnconfigure(1, weight=1)

    def delete_course_offering(self, offering_id, parent_dialog=None):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course offering?"):
            try:
                query = "DELETE FROM course_offering WHERE offering_id = %s"
                self.db.execute_query(query, (offering_id,))
                messagebox.showinfo("Success", "Course offering deleted successfully!")
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_course_offerings()
                self.refresh_teaching_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course offering: {str(e)}")

    def edit_teaching_course(self):
        dialog = tk.Toplevel(self)
        dialog.title("Edit Teaching Course")
        dialog.geometry("420x540")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Edit Teaching Course", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get selected item
        selection = self.teaching_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to edit")
            return
        item = selection[0]
        values = self.teaching_tree.item(item)['values']
        course_id = None
        # Find course_id from offering_id
        offering_id = values[0]
        offering = next((o for o in self.db.get_course_offerings() if o[0] == offering_id), None)
        if offering:
            course_code = offering[2]
            course = next((c for c in self.db.get_all_courses() if c[2] == course_code), None)
            if course:
                course_id = course[0]
        if not course_id:
            messagebox.showerror("Error", "Course not found")
            return
        # Get course details
        course = self.db.get_course_by_id(course_id)
        if not course:
            messagebox.showerror("Error", "Course not found")
            return
        # Get teacher info
        teacher = self.db.get_teacher(self.user['user_id'])
        if not teacher:
            messagebox.showerror("Error", "Teacher not found")
            dialog.destroy()
            return
        department_id = teacher[3]  # department_id
        department_name = self.db.get_department_name(department_id)
        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18", font=("Helvetica", 11))
        form_frame.pack(fill=tk.BOTH, expand=True)
        # Course Name
        ttk.Label(form_frame, text="Course Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_name_var = tk.StringVar(value=course[1])
        ttk.Entry(form_frame, textvariable=course_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        # Course Code
        ttk.Label(form_frame, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        course_code_var = tk.StringVar(value=course[2])
        ttk.Entry(form_frame, textvariable=course_code_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        # Credits
        ttk.Label(form_frame, text="Credits:").grid(row=2, column=0, sticky=tk.W, pady=5)
        credits_var = tk.StringVar(value=str(course[3]))
        ttk.Entry(form_frame, textvariable=credits_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        # ECTS
        ttk.Label(form_frame, text="ECTS:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ects_var = tk.StringVar(value=str(course[4]))
        ttk.Entry(form_frame, textvariable=ects_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        # Level
        ttk.Label(form_frame, text="Level:").grid(row=4, column=0, sticky=tk.W, pady=5)
        level_var = tk.StringVar(value=course[5])
        level_combo = ttk.Combobox(form_frame, textvariable=level_var)
        level_combo['values'] = ('Bachelor', 'Master')
        level_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        # Type
        ttk.Label(form_frame, text="Type:").grid(row=5, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar(value=course[6])
        type_combo = ttk.Combobox(form_frame, textvariable=type_var)
        type_combo['values'] = ('Must', 'Elective', 'Technical Elective')
        type_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
        # Department (fixed)
        ttk.Label(form_frame, text="Department:").grid(row=6, column=0, sticky=tk.W, pady=5)
        ttk.Label(form_frame, text=department_name).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)
        def save_changes():
            try:
                # Validate required fields
                if not all([course_name_var.get(), course_code_var.get(), credits_var.get(), ects_var.get(), level_var.get(), type_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return
                # Update course
                result, msg = self.db.update_course(course_id, {
                    'course_name': course_name_var.get(),
                    'course_code': course_code_var.get(),
                    'credits': int(credits_var.get()),
                    'ects': int(ects_var.get()),
                    'level': level_var.get(),
                    'type': type_var.get(),
                    'department_id': department_id
                })
                if result:
                    messagebox.showinfo("Success", "Course updated successfully!")
                    dialog.destroy()
                    self.refresh_teaching_courses()
                else:
                    messagebox.showerror("Error", msg)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course: {str(e)}")
        save_btn = ttk.Button(form_frame, text="Save Changes", command=save_changes)
        save_btn.grid(row=7, column=0, columnspan=2, pady=20)
        form_frame.columnconfigure(1, weight=1)

    def remove_course_offering(self):
        # Get selected item
        selection = self.offerings_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course offering to remove")
            return
            
        item = selection[0]
        offering_id = self.offerings_tree.item(item)['values'][0]
        self.delete_course_offering(offering_id)

    def show_add_course_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Course")
        dialog.geometry("420x540")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Add Course", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get teacher info
        teacher = self.db.get_teacher(self.user['user_id'])
        if not teacher:
            messagebox.showerror("Error", "Teacher not found")
            dialog.destroy()
            return
        department_id = teacher[3]  # department_id
        department_name = self.db.get_department_name(department_id)

        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18", font=("Helvetica", 11))
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course Name
        ttk.Label(form_frame, text="Course Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=course_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Course Code
        ttk.Label(form_frame, text="Course Code:").grid(row=1, column=0, sticky=tk.W, pady=5)
        course_code_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=course_code_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Credits
        ttk.Label(form_frame, text="Credits:").grid(row=2, column=0, sticky=tk.W, pady=5)
        credits_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=credits_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # ECTS
        ttk.Label(form_frame, text="ECTS:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ects_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=ects_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        # Level
        ttk.Label(form_frame, text="Level:").grid(row=4, column=0, sticky=tk.W, pady=5)
        level_var = tk.StringVar()
        level_combo = ttk.Combobox(form_frame, textvariable=level_var)
        level_combo['values'] = ('Bachelor', 'Master')
        level_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

        # Type
        ttk.Label(form_frame, text="Type:").grid(row=5, column=0, sticky=tk.W, pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(form_frame, textvariable=type_var)
        type_combo['values'] = ('Must', 'Elective', 'Technical Elective')
        type_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)

        # Department (fixed)
        ttk.Label(form_frame, text="Department:").grid(row=6, column=0, sticky=tk.W, pady=5)
        department_var = tk.StringVar(value=department_name)
        ttk.Label(form_frame, text=department_name).grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

        def save_course():
            try:
                # Validate required fields
                if not all([course_name_var.get(), course_code_var.get(), credits_var.get(), 
                          ects_var.get(), level_var.get(), type_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return

                # Check for duplicate course code
                if self.db.check_course_code_exists(course_code_var.get()):
                    messagebox.showerror("Error", "This course code already exists.")
                    return

                # Insert course using teacher's department and teacher id
                self.db.create_course(
                    course_name_var.get(),
                    course_code_var.get(),
                    int(credits_var.get()),
                    int(ects_var.get()),
                    level_var.get(),
                    type_var.get(),
                    department_id,
                    creator_teacher_id=teacher[0]
                )
                messagebox.showinfo("Success", "Course added successfully!")
                dialog.destroy()
                self.refresh_teaching_courses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save", command=save_course)
        save_btn.grid(row=7, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)