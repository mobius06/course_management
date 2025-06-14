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
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a container frame for centering
        container = ttk.Frame(self.login_frame)
        container.grid(row=0, column=0, padx=20, pady=20)

        # Title
        title_label = ttk.Label(container, text="Course Management System", font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        ttk.Label(container, text="Username:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(container, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        # Password
        ttk.Label(container, text="Password:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(container, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        # Login button
        login_button = ttk.Button(container, text="Login", command=self.login, width=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Configure grid weights
        container.columnconfigure(1, weight=1)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Authenticate user
        user = self.db.authenticate_user(username, password)
        if not user:
            messagebox.showerror("Error", "Invalid username or password")
            return

        print(f"Authenticated user: {user}")
        self.current_user = {
            'user_id': user[0],
            'username': user[1],
            'role': user[3]  # Changed from user[2] to user[3] for role
        }
        print(f"Current user data: {self.current_user}")

        # Clear login frame and show appropriate interface
        self.login_frame.destroy()
        self.show_main_interface()

    def show_main_interface(self):
        print(f"Showing interface for role: {self.current_user['role']}")
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