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
        dialog.geometry("400x500")
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

        def save_user():
            try:
                # Validate required fields
                if not all([username_var.get(), password_var.get(), role_var.get()]):
                    messagebox.showerror("Error", "Please fill in all fields")
                    return

                # Create user
                success = self.db.create_user(
                    username_var.get(),
                    password_var.get(),
                    role_var.get()
                )
                if success:
                    messagebox.showinfo("Success", "User added successfully!")
                    dialog.destroy()
                    self.refresh_users()
                else:
                    messagebox.showerror("Error", "Failed to add user")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")

        # Save button
        save_btn = ttk.Button(form_frame, text="Save", command=save_user)
        save_btn.grid(row=3, column=0, columnspan=2, pady=20)

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

            def save_changes():
                try:
                    # Validate required fields
                    if not all([username_var.get(), role_var.get()]):
                        messagebox.showerror("Error", "Please fill in all required fields")
                        return

                    # Update user
                    success = self.db.update_user(
                        user_id,
                        username_var.get(),
                        password_var.get() if password_var.get() else None,
                        role_var.get()
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
            save_btn.grid(row=3, column=0, columnspan=2, pady=20)

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