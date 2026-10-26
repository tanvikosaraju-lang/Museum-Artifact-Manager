import tkinter as tk
from app.database import init_db
from app.ui.login_window import LoginWindow
from app.ui.main_window import MainWindow

def launch_main_app():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

def main():
    # Initialize the SQLite database tables
    init_db()

    # Launch the Login window first
    root = tk.Tk()
    login = LoginWindow(root, on_login_success=launch_main_app)
    root.mainloop()

if __name__ == "__main__":
    main()