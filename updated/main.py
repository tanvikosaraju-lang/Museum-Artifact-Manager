import tkinter as tk
from tkinter import ttk, messagebox
from app.database import init_db
from app.auth import authenticate_user, register_user
from app.ui.main_window import MainWindow

def launch():
    init_db()
    root=tk.Tk()
    root.title("Museum Artifact Management")
    root.geometry("480x430")
    root.configure(bg="#17252a")
    style=ttk.Style()
    style.theme_use("clam")
    style.configure("TButton",padding=9)
    style.configure("TLabel",background="#17252a",foreground="#f4f1de",font=("Segoe UI",11))
    style.configure("TEntry",padding=7)
    style.configure("TFrame",background="#17252a")
    ttk.Label(root,text="🏛  THE MUSEUM",font=("Segoe UI",23,"bold")).pack(pady=(35,5))
    ttk.Label(root,text="Artifact Management • Collection Desk",font=("Segoe UI",10)).pack(pady=(0,24))
    box=ttk.Frame(root,padding=22)
    box.pack(fill="x",padx=40)
    ttk.Label(box,text="Username").pack(anchor="w")
    user=ttk.Entry(box); user.pack(fill="x",pady=(5,13))
    ttk.Label(box,text="Password").pack(anchor="w")
    pwd=ttk.Entry(box,show="•"); pwd.pack(fill="x",pady=5)
    def go():
        u=user.get().strip(); p=pwd.get()
        if not u or not p:
            messagebox.showwarning("Missing details","Enter both username and password."); return
        if authenticate_user(u,p):
            root.destroy()
            app=tk.Tk(); MainWindow(app); app.mainloop()
        else: messagebox.showerror("Login failed","Those details don't match. Register if you're new.")
    def signup():
        u=user.get().strip(); p=pwd.get()
        if len(u)<3 or len(p)<6:
            messagebox.showwarning("Create account","Use a username of 3+ characters and password of 6+ characters."); return
        if register_user(u,p): messagebox.showinfo("Welcome","Account created! You can now sign in.")
        else: messagebox.showerror("Account exists","That username may already be registered.")
    ttk.Button(box,text="Enter Museum",command=go).pack(fill="x",pady=(12,7))
    ttk.Button(box,text="Create Account",command=signup).pack(fill="x")
    ttk.Label(root,text="A little history, carefully catalogued.",font=("Segoe UI",9)).pack(side="bottom",pady=18)
    root.mainloop()
if __name__=="__main__": launch()
