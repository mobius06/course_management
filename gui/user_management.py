import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class UserManagementFrame(ttk.Frame):
    def __init__(self, parent, db, user, mode='user'):
        super().__init__(parent)
        self.db = db
        self.user = user
        self.mode = mode
        self.setup_ui()

    def setup_ui(self):
        # Welcome label
        welcome_label = ttk.Label(self, text=f"Welcome, {self.user.get('full_name', self.user.get('username', 'User'))}!", font=("Helvetica", 14, "bold"))
        welcome_label.pack(pady=(10, 0))

        if self.mode == 'user':
            self.setup_user_tab(self)
        elif self.mode == 'department':
            self.setup_department_tab(self)

    def setup_user_tab(self, parent):
        # Create main container
        self.main_container = ttk.Frame(parent)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create buttons frame
        buttons_frame = ttk.Frame(self.main_container)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))

        # Add User button
        add_user_btn = ttk.Button(
            buttons_frame,
            text="Add User",
            command=self.show_add_user_dialog
        )
        add_user_btn.pack(side=tk.LEFT, padx=5)

        # Refresh button
        refresh_btn = ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.refresh_users
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Create Treeview for users
        columns = ('user_id', 'username', 'role', 'created_at')
        self.tree = ttk.Treeview(
            self.main_container,
            columns=columns,
            show='headings'
        )

        # Define headings
        self.tree.heading('user_id', text='ID')
        self.tree.heading('username', text='Username')
        self.tree.heading('role', text='Role')
        self.tree.heading('created_at', text='Created At')

        # Define columns
        self.tree.column('user_id', width=50)
        self.tree.column('username', width=200)
        self.tree.column('role', width=100)
        self.tree.column('created_at', width=150)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.main_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click event
        self.tree.bind('<Double-1>', self.on_user_select)

        # Load initial data
        self.refresh_users()

    def refresh_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch and display users
        users = self.db.get_all_users()
        for user in users:
            user_data = list(user)  # Convert tuple to list for modification
            # Format role
            user_data[2] = user_data[2].capitalize() if user_data[2] else "N/A"
            # Format datetime
            user_data[3] = user_data[3].strftime("%Y-%m-%d %H:%M:%S") if user_data[3] else "N/A"
            self.tree.insert('', tk.END, values=user_data)

    def show_add_user_dialog(self):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Add New User")
        dialog.geometry("400x700")
        dialog.transient(self)
        dialog.grab_set()

        # Section header
        header = ttk.Label(dialog, text="Add New User", font=("Helvetica", 14, "bold"))
        header.pack(pady=(10, 0))

        # Create form
        form_frame = ttk.Frame(dialog, padding="24 18 24 18")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=4)
        username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=username_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=4)
        password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Role
        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=8, padx=4)
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(form_frame, textvariable=role_var)
        role_combo['values'] = ('admin', 'teacher', 'student')
        role_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        # Extra fields for student/teacher
        # First Name
        first_name_var = tk.StringVar()
        first_name_label = ttk.Label(form_frame, text="First Name:")
        first_name_entry = ttk.Entry(form_frame, textvariable=first_name_var)
        # Last Name
        last_name_var = tk.StringVar()
        last_name_label = ttk.Label(form_frame, text="Last Name:")
        last_name_entry = ttk.Entry(form_frame, textvariable=last_name_var)
        # Student Number (student only)
        student_number_var = tk.StringVar()
        student_number_label = ttk.Label(form_frame, text="Student Number:")
        student_number_entry = ttk.Entry(form_frame, textvariable=student_number_var)
        # Level (student only)
        level_var = tk.StringVar()
        level_label = ttk.Label(form_frame, text="Level:")
        level_combo = ttk.Combobox(form_frame, textvariable=level_var)
        level_combo['values'] = ('Bachelor', 'Master')
        # Email (student/teacher)
        email_var = tk.StringVar()
        email_label = ttk.Label(form_frame, text="Email:")
        email_entry = ttk.Entry(form_frame, textvariable=email_var)
        # Department (student/teacher)
        department_var = tk.StringVar()
        departments = self.db.get_all_departments()
        department_label = ttk.Label(form_frame, text="Department:")
        department_combo = ttk.Combobox(form_frame, textvariable=department_var)
        department_combo['values'] = [dept[1] for dept in departments]

        def update_extra_fields(*args):
            # Remove all extra fields first
            first_name_label.grid_remove()
            first_name_entry.grid_remove()
            last_name_label.grid_remove()
            last_name_entry.grid_remove()
            student_number_label.grid_remove()
            student_number_entry.grid_remove()
            level_label.grid_remove()
            level_combo.grid_remove()
            email_label.grid_remove()
            email_entry.grid_remove()
            department_label.grid_remove()
            department_combo.grid_remove()
            if role_var.get() == 'student':
                # Section header
                ttk.Label(form_frame, text="Student Details", font=("Helvetica", 11, "bold")).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(16, 4))
                first_name_label.grid(row=4, column=0, sticky=tk.W, pady=8, padx=4)
                first_name_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                last_name_label.grid(row=5, column=0, sticky=tk.W, pady=8, padx=4)
                last_name_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                student_number_label.grid(row=6, column=0, sticky=tk.W, pady=8, padx=4)
                student_number_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                level_label.grid(row=7, column=0, sticky=tk.W, pady=8, padx=4)
                level_combo.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                email_label.grid(row=8, column=0, sticky=tk.W, pady=8, padx=4)
                email_entry.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                department_label.grid(row=9, column=0, sticky=tk.W, pady=8, padx=4)
                department_combo.grid(row=9, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
            elif role_var.get() == 'teacher':
                ttk.Label(form_frame, text="Teacher Details", font=("Helvetica", 11, "bold")).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(16, 4))
                first_name_label.grid(row=4, column=0, sticky=tk.W, pady=8, padx=4)
                first_name_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                last_name_label.grid(row=5, column=0, sticky=tk.W, pady=8, padx=4)
                last_name_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                email_label.grid(row=6, column=0, sticky=tk.W, pady=8, padx=4)
                email_entry.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)
                department_label.grid(row=7, column=0, sticky=tk.W, pady=8, padx=4)
                department_combo.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

        role_var.trace_add('write', update_extra_fields)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 16), padx=24)

        def save():
            # Validate required fields
            if not username_var.get() or not password_var.get() or not role_var.get():
                messagebox.showerror("Error", "Please fill in all required fields", parent=dialog)
                return
            # For student/teacher, check extra fields
            if role_var.get() == 'student':
                if not all([first_name_var.get(), last_name_var.get(), student_number_var.get(), level_var.get(), email_var.get(), department_var.get()]):
                    messagebox.showerror("Error", "Please fill in all student fields", parent=dialog)
                    return
            elif role_var.get() == 'teacher':
                if not all([first_name_var.get(), last_name_var.get(), email_var.get(), department_var.get()]):
                    messagebox.showerror("Error", "Please fill in all teacher fields", parent=dialog)
                    return
            # Create user in DB
            success = self.db.create_user(
                username_var.get(),
                password_var.get(),
                role_var.get(),
                first_name_var.get() if role_var.get() in ('student', 'teacher') else None,
                last_name_var.get() if role_var.get() in ('student', 'teacher') else None
            )
            if not success:
                messagebox.showerror("Error", "Failed to create user. Username may already exist.", parent=dialog)
                return
            # If student/teacher, add to respective table
            user_id = self.db.get_user(username_var.get())[0]
            if role_var.get() == 'student':
                dept_id = next(dept[0] for dept in departments if dept[1] == department_var.get())
                self.db.create_student(user_id, student_number_var.get(), first_name_var.get(), last_name_var.get(), email_var.get(), dept_id, level_var.get())
            elif role_var.get() == 'teacher':
                dept_id = next(dept[0] for dept in departments if dept[1] == department_var.get())
                self.db.create_teacher(user_id, first_name_var.get(), last_name_var.get(), email_var.get(), dept_id)
            messagebox.showinfo("Success", "User added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_users()

        save_btn = ttk.Button(button_frame, text="Save", command=save)
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

    def on_user_select(self, event):
        # Get selected item
        item = self.tree.selection()[0]
        user_id = self.tree.item(item)['values'][0]
        
        # Show user details dialog
        self.show_user_details(user_id)

    def show_user_details(self, user_id):
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title("User Details")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="User Details", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Get user details
        user = self.db.get_user_by_id(user_id)
        if not user:
            messagebox.showerror("Error", "User not found", parent=dialog)
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="24 18 24 18")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display user details
        labels = ['User ID', 'Username', 'Role', 'Created At']
        for row, (label, value) in enumerate(zip(labels, user)):
            ttk.Label(details_frame, text=f"{label}:", font=("Helvetica", 11, "bold")).grid(row=row, column=0, sticky=tk.W, pady=8, padx=4)
            ttk.Label(details_frame, text=str(value), font=("Helvetica", 11)).grid(row=row, column=1, sticky=tk.W, pady=8, padx=4)
        details_frame.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        edit_btn = ttk.Button(button_frame, text="Edit", width=12, command=lambda: [dialog.destroy(), self.edit_user(user_id)])
        edit_btn.pack(side=tk.RIGHT, padx=8)
        delete_btn = ttk.Button(button_frame, text="Delete", width=12, command=lambda: self.delete_user(user_id, dialog))
        delete_btn.pack(side=tk.RIGHT, padx=8)

    def edit_user(self, user_id):
        try:
            # Get user data
            user = self.db.get_user_by_id(user_id)
            if not user:
                messagebox.showerror("Error", "User not found")
                return

            # Create dialog window
            dialog = tk.Toplevel(self)
            dialog.title("Edit User")
            dialog.geometry("400x500")
            dialog.transient(self)
            dialog.grab_set()

            # Header
            header = ttk.Label(dialog, text="Edit User", font=("Helvetica", 14, "bold"))
            header.pack(pady=(18, 0))

            # Create form
            form_frame = ttk.Frame(dialog, padding="24 18 24 18")
            form_frame.pack(fill=tk.BOTH, expand=True)

            # Username
            ttk.Label(form_frame, text="Username:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=8, padx=4)
            username_var = tk.StringVar(value=user[1])
            ttk.Entry(form_frame, textvariable=username_var, font=("Helvetica", 11)).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

            # Password
            ttk.Label(form_frame, text="New Password:", font=("Helvetica", 11)).grid(row=1, column=0, sticky=tk.W, pady=8, padx=4)
            password_var = tk.StringVar()
            ttk.Entry(form_frame, textvariable=password_var, show="*", font=("Helvetica", 11)).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

            # Role
            ttk.Label(form_frame, text="Role:", font=("Helvetica", 11)).grid(row=2, column=0, sticky=tk.W, pady=8, padx=4)
            role_var = tk.StringVar(value=user[3])
            role_combo = ttk.Combobox(form_frame, textvariable=role_var, font=("Helvetica", 11))
            role_combo['values'] = ('admin', 'teacher', 'student')
            role_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

            # First Name
            ttk.Label(form_frame, text="First Name:", font=("Helvetica", 11)).grid(row=3, column=0, sticky=tk.W, pady=8, padx=4)
            first_name_var = tk.StringVar(value=user[4])
            ttk.Entry(form_frame, textvariable=first_name_var, font=("Helvetica", 11)).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

            # Last Name
            ttk.Label(form_frame, text="Last Name:", font=("Helvetica", 11)).grid(row=4, column=0, sticky=tk.W, pady=8, padx=4)
            last_name_var = tk.StringVar(value=user[5])
            ttk.Entry(form_frame, textvariable=last_name_var, font=("Helvetica", 11)).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=4)

            form_frame.columnconfigure(1, weight=1)

            # Action buttons
            button_frame = ttk.Frame(dialog)
            button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
            save_btn = ttk.Button(button_frame, text="Save Changes", width=14, command=lambda: save_changes())
            save_btn.pack(side=tk.RIGHT, padx=8)
            cancel_btn = ttk.Button(button_frame, text="Cancel", width=14, command=dialog.destroy)
            cancel_btn.pack(side=tk.RIGHT, padx=8)

            def save_changes():
                try:
                    # Validate required fields
                    if not all([username_var.get(), role_var.get(), first_name_var.get(), last_name_var.get()]):
                        messagebox.showerror("Error", "Please fill in all required fields", parent=dialog)
                        return

                    # Update user
                    success = self.db.update_user(
                        user_id,
                        username_var.get(),
                        password_var.get() if password_var.get() else None,
                        role_var.get(),
                        first_name_var.get(),
                        last_name_var.get()
                    )
                    if success:
                        messagebox.showinfo("Success", "User updated successfully!", parent=dialog)
                        dialog.destroy()
                        self.refresh_users()
                    else:
                        messagebox.showerror("Error", "Failed to update user", parent=dialog)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update user: {str(e)}", parent=dialog)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to edit user: {str(e)}")
            # Ensure UI remains responsive
            self.after(100, self.refresh_users)

    def delete_user(self, user_id, dialog):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            try:
                query = "DELETE FROM \"user\" WHERE user_id = %s"
                self.db.execute_query(query, (user_id,))
                messagebox.showinfo("Success", "User deleted successfully!")
                dialog.destroy()
                self.refresh_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def setup_department_tab(self, parent):
        # Buttons frame
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        add_btn = ttk.Button(buttons_frame, text="Add Department", command=self.add_department_dialog)
        add_btn.pack(side=tk.LEFT, padx=5)
        edit_btn = ttk.Button(buttons_frame, text="Edit Department", command=self.edit_department_dialog)
        edit_btn.pack(side=tk.LEFT, padx=5)
        delete_btn = ttk.Button(buttons_frame, text="Delete Department", command=self.delete_department)
        delete_btn.pack(side=tk.LEFT, padx=5)
        refresh_btn = ttk.Button(buttons_frame, text="Refresh", command=self.refresh_departments)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        # Treeview
        columns = ('department_id', 'department_name')
        self.dept_tree = ttk.Treeview(parent, columns=columns, show='headings')
        self.dept_tree.heading('department_id', text='ID')
        self.dept_tree.heading('department_name', text='Department Name')
        self.dept_tree.column('department_id', width=50)
        self.dept_tree.column('department_name', width=200)
        self.dept_tree.pack(fill=tk.BOTH, expand=True)
        self.refresh_departments()

    def refresh_departments(self):
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)
        departments = self.db.get_all_departments()
        for dept in departments:
            self.dept_tree.insert('', tk.END, values=dept)

    def add_department_dialog(self):
        dialog = tk.Toplevel(self)
        dialog.title("Add Department")
        dialog.geometry("400x220")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Add Department", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Form
        form = ttk.Frame(dialog, padding="24 18 24 18")
        form.pack(fill=tk.BOTH, expand=True)
        ttk.Label(form, text="Department Name:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=12, padx=4)
        name_var = tk.StringVar()
        name_entry = ttk.Entry(form, textvariable=name_var, font=("Helvetica", 11))
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=12, padx=4)
        name_entry.focus()
        form.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        save_btn = ttk.Button(button_frame, text="Save", width=12, command=lambda: save())
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=12, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

        def save():
            if not name_var.get():
                messagebox.showerror("Error", "Please enter a department name", parent=dialog)
                return
            self.db.execute_query("INSERT INTO department (department_name) VALUES (%s)", (name_var.get(),))
            messagebox.showinfo("Success", "Department added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_departments()

    def edit_department_dialog(self):
        selection = self.dept_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a department to edit")
            return
        item = selection[0]
        values = self.dept_tree.item(item)['values']
        dept_id, dept_name = values[0], values[1]
        dialog = tk.Toplevel(self)
        dialog.title("Edit Department")
        dialog.geometry("400x220")
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = ttk.Label(dialog, text="Edit Department", font=("Helvetica", 14, "bold"))
        header.pack(pady=(18, 0))

        # Form
        form = ttk.Frame(dialog, padding="24 18 24 18")
        form.pack(fill=tk.BOTH, expand=True)
        ttk.Label(form, text="Department Name:", font=("Helvetica", 11)).grid(row=0, column=0, sticky=tk.W, pady=12, padx=4)
        name_var = tk.StringVar(value=dept_name)
        name_entry = ttk.Entry(form, textvariable=name_var, font=("Helvetica", 11))
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=12, padx=4)
        name_entry.focus()
        form.columnconfigure(1, weight=1)

        # Action buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=(0, 18), padx=24)
        save_btn = ttk.Button(button_frame, text="Save Changes", width=12, command=lambda: save())
        save_btn.pack(side=tk.RIGHT, padx=8)
        cancel_btn = ttk.Button(button_frame, text="Cancel", width=12, command=dialog.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=8)

        def save():
            if not name_var.get():
                messagebox.showerror("Error", "Please enter a department name", parent=dialog)
                return
            self.db.execute_query("UPDATE department SET department_name = %s WHERE department_id = %s", (name_var.get(), dept_id))
            messagebox.showinfo("Success", "Department updated successfully!", parent=dialog)
            dialog.destroy()
            self.refresh_departments()

    def delete_department(self):
        selection = self.dept_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a department to delete")
            return
        item = selection[0]
        values = self.dept_tree.item(item)['values']
        dept_id, dept_name = values[0], values[1]
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the department '{dept_name}'?"):
            return
        try:
            # Check for references
            student_count = self.db.fetch_one("SELECT COUNT(*) FROM student WHERE department_id = %s", (dept_id,))[0]
            teacher_count = self.db.fetch_one("SELECT COUNT(*) FROM teacher WHERE department_id = %s", (dept_id,))[0]
            course_count = self.db.fetch_one("SELECT COUNT(*) FROM course WHERE department_id = %s", (dept_id,))[0]
            if student_count > 0 or teacher_count > 0 or course_count > 0:
                messagebox.showerror("Error", "Cannot delete department: it is still referenced by students, teachers, or courses.")
                return
            self.db.execute_query("DELETE FROM department WHERE department_id = %s", (dept_id,))
            messagebox.showinfo("Success", "Department deleted successfully!")
            self.refresh_departments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete department: {str(e)}")
