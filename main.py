import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
from database import Database
from gui.student_interface import StudentInterface
from gui.teacher_interface import TeacherInterface
from gui.course_management import CourseManagementFrame
from gui.user_management import UserManagementFrame

class CourseManagementSystem:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Course Management System")
        self.root.geometry("800x600")
        self.db = Database()
        self.current_user = None
        self.setup_login_frame()

    def setup_login_frame(self):
        # Create and configure the main frame
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Username
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.login_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        # Password
        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.login_frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Role selection
        ttk.Label(self.login_frame, text="Role:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(self.login_frame, textvariable=self.role_var)
        role_combo['values'] = ('student', 'teacher', 'admin')
        role_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Login button
        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Register button
        register_button = ttk.Button(self.login_frame, text="Register", command=self.show_register_dialog)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Configure grid weights
        self.login_frame.columnconfigure(1, weight=1)

    def show_register_dialog(self):
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Register New User")
        dialog.geometry("300x250")
        dialog.transient(self.root)
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

        # Confirm Password
        ttk.Label(form_frame, text="Confirm Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        confirm_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=confirm_var, show="*").grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Role selection
        ttk.Label(form_frame, text="Role:").grid(row=3, column=0, sticky=tk.W, pady=5)
        role_var = tk.StringVar(value="student")
        role_combo = ttk.Combobox(form_frame, textvariable=role_var)
        role_combo['values'] = ('student', 'teacher', 'admin')
        role_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        def register():
            username = username_var.get().strip()
            password = password_var.get()
            confirm = confirm_var.get()
            role = role_var.get()

            if not username or not password:
                messagebox.showerror("Error", "Please fill in all fields")
                return

            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return

            try:
                # Check if username already exists
                if self.db.get_user(username):
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Create new user
                self.db.create_user(username, password, role)
                messagebox.showinfo("Success", "Registration successful! Please login.")
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")

        # Register button
        register_btn = ttk.Button(form_frame, text="Register", command=register)
        register_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Authenticate user
        user = self.db.authenticate_user(username, password)
        if not user:
            messagebox.showerror("Error", "Invalid username or password")
            return

        if user[2] != role:  # user[2] is the role field
            messagebox.showerror("Error", "Selected role does not match user's role")
            return

        self.current_user = {
            'user_id': user[0],
            'username': user[1],
            'role': user[2]
        }

        # Clear login frame and show appropriate interface
        self.login_frame.destroy()
        self.show_main_interface()

    def show_main_interface(self):
        # Create main interface based on user role
        if self.current_user['role'] == 'student':
            self.show_student_interface()
        elif self.current_user['role'] == 'teacher':
            self.show_teacher_interface()
        else:  # admin
            self.show_admin_interface()

    def show_student_interface(self):
        # Create student interface
        student_interface = StudentInterface(self.root, self.db, self.current_user)
        student_interface.pack(fill=tk.BOTH, expand=True)

        # Add logout button
        logout_btn = ttk.Button(
            self.root,
            text="Logout",
            command=self.logout
        )
        logout_btn.pack(side=tk.BOTTOM, pady=10)

    def show_teacher_interface(self):
        # Create teacher interface
        teacher_interface = TeacherInterface(self.root, self.db, self.current_user)
        teacher_interface.pack(fill=tk.BOTH, expand=True)

        # Add logout button
        logout_btn = ttk.Button(
            self.root,
            text="Logout",
            command=self.logout
        )
        logout_btn.pack(side=tk.BOTTOM, pady=10)

    def show_admin_interface(self):
        # Create admin interface
        admin_frame = ttk.Frame(self.root)
        admin_frame.pack(fill=tk.BOTH, expand=True)

        # Create notebook for tabs
        notebook = ttk.Notebook(admin_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        course_management_tab = ttk.Frame(notebook)
        user_management_tab = ttk.Frame(notebook)

        notebook.add(course_management_tab, text="Course Management")
        notebook.add(user_management_tab, text="User Management")

        # Add course management interface
        course_management = CourseManagementFrame(course_management_tab, self.db, self.current_user)
        course_management.pack(fill=tk.BOTH, expand=True)

        # Add user management interface
        user_management = UserManagementFrame(user_management_tab, self.db, self.current_user)
        user_management.pack(fill=tk.BOTH, expand=True)

        # Add logout button
        logout_btn = ttk.Button(
            self.root,
            text="Logout",
            command=self.logout
        )
        logout_btn.pack(side=tk.BOTTOM, pady=10)

    def logout(self):
        self.current_user = None
        # Clear all widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        # Show login frame again
        self.setup_login_frame()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CourseManagementSystem()
    app.run() 