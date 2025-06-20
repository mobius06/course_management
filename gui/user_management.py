import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class UserManagementFrame(ttk.Frame):
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

        # Create form
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Username
        ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=username_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Role
        ttk.Label(form_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=5)
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(form_frame, textvariable=role_var)
        role_combo['values'] = ('admin', 'teacher', 'student')
        role_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

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
                first_name_label.grid(row=3, column=0, sticky=tk.W, pady=5)
                first_name_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
                last_name_label.grid(row=4, column=0, sticky=tk.W, pady=5)
                last_name_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
                student_number_label.grid(row=5, column=0, sticky=tk.W, pady=5)
                student_number_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
                level_label.grid(row=6, column=0, sticky=tk.W, pady=5)
                level_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)
                email_label.grid(row=7, column=0, sticky=tk.W, pady=5)
                email_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5)
                department_label.grid(row=8, column=0, sticky=tk.W, pady=5)
                department_combo.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5)
            elif role_var.get() == 'teacher':
                first_name_label.grid(row=3, column=0, sticky=tk.W, pady=5)
                first_name_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
                last_name_label.grid(row=4, column=0, sticky=tk.W, pady=5)
                last_name_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
                email_label.grid(row=5, column=0, sticky=tk.W, pady=5)
                email_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5)
                department_label.grid(row=6, column=0, sticky=tk.W, pady=5)
                department_combo.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5)

        role_var.trace_add('write', update_extra_fields)

        def save_user():
            try:
                # Validate required fields
                if not all([username_var.get(), password_var.get(), role_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return
                role = role_var.get()
                # Extra validation for student/teacher
                if role == 'student':
                    if not all([first_name_var.get(), last_name_var.get(), student_number_var.get(), level_var.get(), email_var.get(), department_var.get()]):
                        messagebox.showerror("Error", "Please fill in all student fields (including level)")
                        return
                elif role == 'teacher':
                    if not all([first_name_var.get(), last_name_var.get(), email_var.get(), department_var.get()]):
                        messagebox.showerror("Error", "Please fill in all teacher fields")
                        return

                # Check for duplicate username
                if self.db.check_username_exists(username_var.get()):
                    messagebox.showerror("Error", "This username already exists.")
                    return

                # Check for duplicate student number/email
                if role == 'student':
                    query = "SELECT 1 FROM student WHERE student_number = %s OR email = %s"
                    if self.db.fetch_one(query, (student_number_var.get(), email_var.get())):
                        messagebox.showerror("Error", "This student number or email already exists.")
                        return
                elif role == 'teacher':
                    query = "SELECT 1 FROM teacher WHERE email = %s"
                    if self.db.fetch_one(query, (email_var.get(),)):
                        messagebox.showerror("Error", "This teacher email already exists.")
                        return

                # Create user
                success = self.db.create_user(
                    username_var.get(),
                    password_var.get(),
                    role,
                    first_name_var.get() if role in ('student', 'teacher') else '',
                    last_name_var.get() if role in ('student', 'teacher') else ''
                )
                if not success:
                    messagebox.showerror("Error", "Failed to add user")
                    return

                # Get the new user's user_id
                user = self.db.get_user(username_var.get())
                if not user:
                    messagebox.showerror("Error", "User creation failed (user not found)")
                    return
                user_id = user[0]

                # Insert into student/teacher table if needed
                if role == 'student':
                    dept_id = next(dept[0] for dept in departments if dept[1] == department_var.get())
                    self.db.create_student(
                        user_id,
                        student_number_var.get(),
                        first_name_var.get(),
                        last_name_var.get(),
                        email_var.get(),
                        dept_id,
                        level_var.get()
                    )
                elif role == 'teacher':
                    dept_id = next(dept[0] for dept in departments if dept[1] == department_var.get())
                    self.db.create_teacher(
                        user_id,
                        first_name_var.get(),
                        last_name_var.get(),
                        email_var.get(),
                        dept_id
                    )
                messagebox.showinfo("Success", "User added successfully!")
                dialog.destroy()
                self.refresh_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save", command=save_user)
        save_btn.grid(row=30, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

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
        dialog.geometry("300x200")
        dialog.transient(self)
        dialog.grab_set()

        # Get user details
        user = self.db.get_user_by_id(user_id)
        if not user:
            messagebox.showerror("Error", "User not found")
            dialog.destroy()
            return

        # Create details frame
        details_frame = ttk.Frame(dialog, padding="20")
        details_frame.pack(fill=tk.BOTH, expand=True)

        # Display user details
        row = 0
        for label, value in zip(
            ['User ID', 'Username', 'Role', 'Created At'],
            user
        ):
            ttk.Label(details_frame, text=f"{label}:").grid(row=row, column=0, sticky=tk.W, pady=5)
            ttk.Label(details_frame, text=str(value)).grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1

        # Add buttons
        buttons_frame = ttk.Frame(details_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        edit_btn = ttk.Button(
            buttons_frame,
            text="Edit",
            command=lambda: self.edit_user(user_id)
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(
            buttons_frame,
            text="Delete",
            command=lambda: self.delete_user(user_id, dialog)
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

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

            # Create form
            form_frame = ttk.Frame(dialog, padding="20")
            form_frame.pack(fill=tk.BOTH, expand=True)

            # Username
            ttk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
            username_var = tk.StringVar(value=user[1])
            ttk.Entry(form_frame, textvariable=username_var).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

            # Password
            ttk.Label(form_frame, text="New Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
            password_var = tk.StringVar()
            ttk.Entry(form_frame, textvariable=password_var, show="*").grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

            # Role
            ttk.Label(form_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=5)
            role_var = tk.StringVar(value=user[3])
            role_combo = ttk.Combobox(form_frame, textvariable=role_var)
            role_combo['values'] = ('admin', 'teacher', 'student')
            role_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

            # First Name
            ttk.Label(form_frame, text="First Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
            first_name_var = tk.StringVar(value=user[4])
            ttk.Entry(form_frame, textvariable=first_name_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

            # Last Name
            ttk.Label(form_frame, text="Last Name:").grid(row=4, column=0, sticky=tk.W, pady=5)
            last_name_var = tk.StringVar(value=user[5])
            ttk.Entry(form_frame, textvariable=last_name_var).grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)

            def save_changes():
                try:
                    # Validate required fields
                    if not all([username_var.get(), role_var.get(), first_name_var.get(), last_name_var.get()]):
                        messagebox.showerror("Error", "Please fill in all required fields")
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
                        messagebox.showinfo("Success", "User updated successfully!")
                        dialog.destroy()
                        self.refresh_users()
                    else:
                        messagebox.showerror("Error", "Failed to update user")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update user: {str(e)}")

            # Save button
            save_btn = ttk.Button(form_frame, text="Save Changes", command=save_changes)
            save_btn.grid(row=5, column=0, columnspan=2, pady=20)

            # Configure grid weights
            form_frame.columnconfigure(1, weight=1)

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