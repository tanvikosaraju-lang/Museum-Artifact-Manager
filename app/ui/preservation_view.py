import tkinter as tk
from tkinter import messagebox, ttk
from app.database import get_all_preservation_records, add_preservation_record, get_all_artifacts

class PreservationView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Title
        ttk.Label(self, text="Preservation Records", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        # Form Frame for Adding Preservation Records
        form_frame = ttk.LabelFrame(self, text="Add Preservation Record", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Artifact:").grid(row=0, column=0, sticky="w", padx=5, pady=2)

        # Fetch artifact options for dropdown
        self.artifact_map = {}
        artifacts = get_all_artifacts()
        artifact_names = []
        for art in artifacts:
            # art[0] is ID, art[1] is Name
            name_label = f"{art[0]}: {art[1]}"
            self.artifact_map[name_label] = art[0]
            artifact_names.append(name_label)

        self.artifact_combo = ttk.Combobox(form_frame, values=artifact_names, width=25, state="readonly")
        self.artifact_combo.grid(row=0, column=1, padx=5, pady=2)
        if artifact_names:
            self.artifact_combo.current(0)

        ttk.Label(form_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.date_entry = ttk.Entry(form_frame, width=20)
        self.date_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Conservator:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.conservator_entry = ttk.Entry(form_frame, width=25)
        self.conservator_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Notes:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.notes_entry = ttk.Entry(form_frame, width=25)
        self.notes_entry.grid(row=1, column=3, padx=5, pady=2)

        ttk.Button(form_frame, text="Add Record", command=self.handle_add_record).grid(row=2, column=0, columnspan=4, pady=10)

        # Treeview Table for displaying records
        table_frame = ttk.Frame(self, padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("ID", "Artifact Name", "Date", "Notes", "Conservator")
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

        records = get_all_preservation_records()
        for rec in records:
            self.tree.insert("", "end", values=rec)

    def handle_add_record(self):
        selected_artifact_str = self.artifact_combo.get()
        date = self.date_entry.get().strip()
        conservator = self.conservator_entry.get().strip()
        notes = self.notes_entry.get().strip()

        if not selected_artifact_str or not date:
            messagebox.showerror("Error", "Please select an artifact and provide a date.")
            return

        artifact_id = self.artifact_map[selected_artifact_str]

        try:
            add_preservation_record(artifact_id, date, notes, conservator)
            messagebox.showinfo("Success", "Preservation record added successfully!")
            self.date_entry.delete(0, tk.END)
            self.conservator_entry.delete(0, tk.END)
            self.notes_entry.delete(0, tk.END)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Could not add preservation record: {e}")