import tkinter as tk
from tkinter import messagebox, ttk
from app.auth import authenticate_user, register_user

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("MUSEUM ARTIFACT MANAGER - Login")
        self.root.geometry("400x300")
        self.on_login_success = on_login_success

        ttk.Label(root, text="Museum Login", font=("Segoe UI", 16, "bold")).pack(pady=20)

        form_frame = ttk.Frame(root)
        form_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(form_frame, text="Username:").pack(anchor="w")
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack(pady=(0, 10), fill="x")

        ttk.Label(form_frame, text="Password:").pack(anchor="w")
        self.password_entry = ttk.Entry(form_frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 10), fill="x")

        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Login", command=self.handle_login).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Register", command=self.handle_register).pack(side="left", padx=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if authenticate_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if register_user(username, password):
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
        else:
            messagebox.showerror("Error", "Username already exists.")