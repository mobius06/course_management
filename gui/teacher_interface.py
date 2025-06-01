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
            
            # Add separator if semester/year changes
            if semester != current_semester or year != current_year:
                if current_semester is not None:  # Don't add separator before first group
                    self.teaching_tree.insert('', tk.END, values=('', '', '', '', '', ''), tags=('separator',))
                
                # Add semester/year header
                header = f"{semester} {year}"
                self.teaching_tree.insert('', tk.END, values=('', header, '', '', '', ''), tags=('header',))
                
                current_semester = semester
                current_year = year
            
            # Add course
            self.teaching_tree.insert('', tk.END, values=course, tags=('course',))

        # Configure tags for styling
        self.teaching_tree.tag_configure('header', background='#f0f0f0', font=('TkDefaultFont', 10, 'bold'))
        self.teaching_tree.tag_configure('separator', background='#e0e0e0')
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
        course_combo['values'] = [f"{course[2]} - {course[1]}" for course in courses]
        course_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Semester selection
        ttk.Label(form_frame, text="Semester:").grid(row=1, column=0, sticky=tk.W, pady=5)
        semester_var = tk.StringVar()
        semesters = self.db.get_all_semesters()
        semester_combo = ttk.Combobox(form_frame, textvariable=semester_var)
        semester_combo['values'] = [sem[1] for sem in semesters]  # sem[1] is semester_name
        semester_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Year
        ttk.Label(form_frame, text="Year:").grid(row=2, column=0, sticky=tk.W, pady=5)
        year_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=year_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        def save_offering():
            try:
                # Validate required fields
                if not all([course_var.get(), semester_var.get(), year_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
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
                    messagebox.showerror("Error", "Teacher not found")
                    return

                # Create course offering
                self.db.create_course_offering(
                    course_id,
                    semester_id,
                    teacher[0],  # teacher_id
                    int(year_var.get())
                )
                messagebox.showinfo("Success", "Course offering added successfully!")
                dialog.destroy()
                self.refresh_course_offerings()
                self.refresh_teaching_courses()
            except ValueError:
                messagebox.showerror("Error", "Year must be a number")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add course offering: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save", command=save_offering)
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def on_teaching_course_select(self, event):
        # Get selected item
        item = self.teaching_tree.selection()[0]
        offering_id = self.teaching_tree.item(item)['values'][0]
        
        # Show course offering details
        self.show_course_offering_details(offering_id)

    def on_offering_select(self, event):
        # Get selected item
        item = self.offerings_tree.selection()[0]
        offering_id = self.offerings_tree.item(item)['values'][0]
        
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
            ['Offering ID', 'Course Name', 'Course Code', 'Semester', 'Year', 'Department'],
            offering
        ):
            ttk.Label(details_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=str(value)).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        # Add buttons
        buttons_frame = ttk.Frame(details_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        # Get teacher ID
        teacher = self.db.get_teacher(self.user['user_id'])
        if teacher and offering[3] == teacher[0]:  # instructor_id
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

    def edit_course_offering(self, offering_id, parent_dialog=None):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Edit Course Offering")
        dialog.geometry("400x400")
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

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Course selection
        ttk.Label(form_frame, text="Course:").grid(row=0, column=0, sticky=tk.W, pady=5)
        course_var = tk.StringVar(value=f"{offering[2]} - {offering[1]}")
        courses = self.db.get_all_courses()
        course_combo = ttk.Combobox(form_frame, textvariable=course_var)
        course_combo['values'] = [f"{course[2]} - {course[1]}" for course in courses]
        course_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Semester selection
        ttk.Label(form_frame, text="Semester:").grid(row=1, column=0, sticky=tk.W, pady=5)
        semester_var = tk.StringVar(value=offering[3])
        semesters = self.db.get_all_semesters()
        semester_combo = ttk.Combobox(form_frame, textvariable=semester_var)
        semester_combo['values'] = [sem[1] for sem in semesters]
        semester_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Year
        ttk.Label(form_frame, text="Year:").grid(row=2, column=0, sticky=tk.W, pady=5)
        year_var = tk.StringVar(value=str(offering[4]))
        ttk.Entry(form_frame, textvariable=year_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        def save_changes():
            try:
                # Validate required fields
                if not all([course_var.get(), semester_var.get(), year_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
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
                    messagebox.showerror("Error", "Teacher not found")
                    return

                # Update course offering
                self.db.update_course_offering(
                    offering_id,
                    course_id,
                    semester_id,
                    teacher[0],  # teacher_id
                    int(year_var.get())
                )
                messagebox.showinfo("Success", "Course offering updated successfully!")
                dialog.destroy()
                if parent_dialog:
                    parent_dialog.destroy()
                self.refresh_course_offerings()
                self.refresh_teaching_courses()
            except ValueError:
                messagebox.showerror("Error", "Year must be a number")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update course offering: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save Changes", command=save_changes)
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Configure grid weights
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
        # Get selected item
        selection = self.teaching_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course to edit")
            return
            
        item = selection[0]
        offering_id = self.teaching_tree.item(item)['values'][0]
        self.edit_course_offering(offering_id)

    def remove_course_offering(self):
        # Get selected item
        selection = self.offerings_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a course offering to remove")
            return
            
        item = selection[0]
        offering_id = self.offerings_tree.item(item)['values'][0]
        self.delete_course_offering(offering_id)