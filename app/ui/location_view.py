import tkinter as tk
from tkinter import messagebox, ttk
from app.database import get_all_locations, add_location

class LocationView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ttk.Label(self, text="Location Management", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        # Form Frame for Adding Locations
        form_frame = ttk.LabelFrame(self, text="Add New Location", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Location Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(form_frame, width=25)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Description:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.desc_entry = ttk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Button(form_frame, text="Add Location", command=self.handle_add_location).grid(row=0, column=4, padx=10, pady=2)

        # Treeview Table for displaying locations
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Name", "Description")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        locations = get_all_locations()
        for loc in locations:
            self.tree.insert("", "end", values=loc)

    def handle_add_location(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Location name is required.")
            return

        try:
            add_location(name, description)
            messagebox.showinfo("Success", "Location added successfully!")
            self.name_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add location (Name might already exist): {e}")