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

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_teaching_courses
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for teaching courses
        columns = ('offering_id', 'course_name', 'course_code', 'semester', 'year')
        self.teaching_courses_tree = ttk.Treeview(
            self.teaching_courses_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.teaching_courses_tree.heading('offering_id', text='ID')
        self.teaching_courses_tree.heading('course_name', text='Course Name')
        self.teaching_courses_tree.heading('course_code', text='Course Code')
        self.teaching_courses_tree.heading('semester', text='Semester')
        self.teaching_courses_tree.heading('year', text='Year')

        # Define columns
        self.teaching_courses_tree.column('offering_id', width=50)
        self.teaching_courses_tree.column('course_name', width=200)
        self.teaching_courses_tree.column('course_code', width=100)
        self.teaching_courses_tree.column('semester', width=100)
        self.teaching_courses_tree.column('year', width=70)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.teaching_courses_tab, orient=tk.VERTICAL, command=self.teaching_courses_tree.yview)
        self.teaching_courses_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.teaching_courses_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.teaching_courses_tree.bind('<Double-1>', self.on_teaching_course_select)

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

        # Create Treeview for course offerings
        columns = ('offering_id', 'course_name', 'course_code', 'semester', 'year')
        self.course_offerings_tree = ttk.Treeview(
            self.course_offerings_tab,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.course_offerings_tree.heading('offering_id', text='ID')
        self.course_offerings_tree.heading('course_name', text='Course Name')
        self.course_offerings_tree.heading('course_code', text='Course Code')
        self.course_offerings_tree.heading('semester', text='Semester')
        self.course_offerings_tree.heading('year', text='Year')

        # Define columns
        self.course_offerings_tree.column('offering_id', width=50)
        self.course_offerings_tree.column('course_name', width=200)
        self.course_offerings_tree.column('course_code', width=100)
        self.course_offerings_tree.column('semester', width=100)
        self.course_offerings_tree.column('year', width=70)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.course_offerings_tab, orient=tk.VERTICAL, command=self.course_offerings_tree.yview)
        self.course_offerings_tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.course_offerings_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.course_offerings_tree.bind('<Double-1>', self.on_course_offering_select)

        # Load initial data
        self.refresh_course_offerings()

    def refresh_teaching_courses(self):
        # Clear existing items
        for item in self.teaching_courses_tree.get_children():
            self.teaching_courses_tree.delete(item)

        # Fetch and display teaching courses
        offerings = self.db.get_course_offerings()
        for offering in offerings:
            if offering[3] == self.user['user_id']:  # instructor_id
                self.teaching_courses_tree.insert('', tk.END, values=offering)

    def refresh_course_offerings(self):
        # Clear existing items
        for item in self.course_offerings_tree.get_children():
            self.course_offerings_tree.delete(item)

        # Fetch and display course offerings
        offerings = self.db.get_course_offerings()
        for offering in offerings:
            self.course_offerings_tree.insert('', tk.END, values=offering)

    def on_teaching_course_select(self, event):
        # Get selected item
        item = self.teaching_courses_tree.selection()[0]
        offering_id = self.teaching_courses_tree.item(item)['values'][0]
        
        # Show course offering details
        self.show_course_offering_details(offering_id)

    def on_course_offering_select(self, event):
        # Get selected item
        item = self.course_offerings_tree.selection()[0]
        offering_id = self.course_offerings_tree.item(item)['values'][0]
        
        # Show course offering details
        self.show_course_offering_details(offering_id)

    def show_course_offering_details(self, offering_id):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Course Offering Details")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Get course offering details
        offering = next(
            (o for o in self.db.get_course_offerings() if o[0] == offering_id),
            None
        )
        if not offering:
            messagebox.showerror("Error", "Course offering not found")
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display course offering details
        row = 0
        for label, value in zip(
            ['Offering ID', 'Course Name', 'Course Code', 'Semester', 'Year'],
            offering
        ):
            ttk.Label(details_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=str(value)).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        # Add buttons
        buttons_frame = ttk.Frame(details_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        if offering[3] == self.user['user_id']:  # instructor_id
            edit_btn = ttk.Button(
                buttons_frame,
                text="Edit",
                command=lambda: self.edit_course_offering(offering_id, dialog)
            )
            edit_btn.pack(side=tk.LEFT, padx=5)

            delete_btn = ttk.Button(
                buttons_frame,
                text="Delete",
                command=lambda: self.delete_course_offering(offering_id, dialog)
            )
            delete_btn.pack(side=tk.LEFT, padx=5)

    def show_add_offering_dialog(self):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add Course Offering")
        dialog.geometry("400x400")
        dialog.transient(self)
        dialog.grab_set()

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course selection
        ttk.Label(form_frame, text="Course:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_var = tk.StringVar()
        courses = self.db.get_all_courses()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var)
        course_combo['values'] = [f"{c[1]} ({c[2]})" for c in courses]
        course_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Semester selection
        ttk.Label(form_frame, text="Semester:").grid(row=1, column=0, sticky=tk.W, pady=5)
        semester_var = tk.StringVar()
        semesters = self.db.get_all_semesters()
        semester_combo = ttk.Combobox(form_frame, textvariable=semester_var)
        semester_combo['values'] = [s[1] for s in semesters]
        semester_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Year
        ttk.Label(form_frame, text="Year:").grid(row=2, column=0, sticky=tk.W, pady=5)
        year_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=year_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        def save_offering():
            try:
                # Get course ID
                course_name = course_var.get().split(' (')[0]
                course_id = next(c[0] for c in courses if c[1] == course_name)

                # Get semester ID
                semester_name = semester_var.get()
                semester_id = next(s[0] for s in semesters if s[1] == semester_name)

                # Insert course offering
                query = """
                INSERT INTO course_offering (course_id, semester_id, instructor_id, year)
                VALUES (%s, %s, %s, %s)
                """
                self.db.execute_query(query, (
                    course_id,
                    semester_id,
                    self.user['user_id'],
                    int(year_var.get())
                ))
                messagebox.showinfo("Success", "Course offering added successfully!")
                dialog.destroy()
                self.refresh_teaching_courses()
                self.refresh_course_offerings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course offering: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save", command=save_offering)
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def edit_course_offering(self, offering_id, dialog):
        # TODO: Implement course offering editing
        pass

    def delete_course_offering(self, offering_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course offering?"):
            try:
                query = "DELETE FROM course_offering WHERE offering_id = %s"
                self.db.execute_query(query, (offering_id,))
                messagebox.showinfo("Success", "Course offering deleted successfully!")
                dialog.destroy()
                self.refresh_teaching_courses()
                self.refresh_course_offerings()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete course offering: {str(e)}") 