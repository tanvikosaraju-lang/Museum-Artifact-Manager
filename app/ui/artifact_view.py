import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from app.database import get_all_artifacts, add_artifact

class ArtifactView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_image_path = ""
        self.thumbnail_image = None
        self.detail_image = None  # Reference to prevent garbage collection of preview images

        # Title
        ttk.Label(self, text="Artifact Management", font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        # Form Frame for Adding Artifacts
        form_frame = ttk.LabelFrame(self, text="Add New Artifact", padding=10)
        form_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Category:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.category_entry = ttk.Entry(form_frame, width=20)
        self.category_entry.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(form_frame, text="Status:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.status_entry = ttk.Entry(form_frame, width=20)
        self.status_entry.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Description:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.desc_entry = ttk.Entry(form_frame, width=20)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=2)

        # Image Picker Section
        ttk.Label(form_frame, text="Image:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.image_path_label = ttk.Label(form_frame, text="No file selected", foreground="gray")
        self.image_path_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(form_frame, text="Browse Image", command=self.browse_image).grid(row=2, column=2, padx=5, pady=5)

        # Form Thumbnail Preview
        self.preview_label = ttk.Label(form_frame, text="[No Preview]")
        self.preview_label.grid(row=0, column=4, rowspan=3, padx=15)

        ttk.Button(form_frame, text="Add Artifact", command=self.handle_add_artifact).grid(row=3, column=0, columnspan=4, pady=10)

        # Main Container for Table + Image Preview Panel
        content_frame = ttk.Frame(self, padding=10)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview Table frame (Left side)
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(side="left", fill="both", expand=True)

        columns = ("ID", "Name", "Category", "Description", "Location", "Status", "Image Path")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=105)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind row selection event to display the image
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Dedicated Image Preview Panel (Right side)
        preview_panel = ttk.LabelFrame(content_frame, text="Selected Artifact Photo", padding=10)
        preview_panel.pack(side="right", fill="both", padx=10)

        self.selected_img_label = ttk.Label(preview_panel, text="Click a row in the table\nto view artifact photo", anchor="center")
        self.selected_img_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()

    def browse_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Artifact Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            self.image_path_label.config(text=filename, foreground="black")

            try:
                img = Image.open(file_path)
                img.thumbnail((80, 80))
                self.thumbnail_image = ImageTk.PhotoImage(img)
                self.preview_label.config(image=self.thumbnail_image, text="")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image preview: {e}")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        artifacts = get_all_artifacts()
        for art in artifacts:
            self.tree.insert("", "end", values=art)

    def on_row_select(self, event):
        """Triggered when user clicks an artifact row in the table."""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = self.tree.item(selected_items[0])
        values = item['values']

        # Image path is stored at index 6
        if values and len(values) > 6:
            img_path = values[6]
            if img_path and os.path.exists(str(img_path)):
                try:
                    img = Image.open(img_path)
                    img.thumbnail((220, 220))  # Resize nicely for the preview panel
                    self.detail_image = ImageTk.PhotoImage(img)
                    self.selected_img_label.config(image=self.detail_image, text="")
                    return
                except Exception:
                    pass

            # Fallback if no image or invalid path
            self.selected_img_label.config(image="", text="No image found for\nthis artifact")

    def handle_add_artifact(self):
        name = self.name_entry.get().strip()
        category = self.category_entry.get().strip()
        status = self.status_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Artifact name is required.")
            return

        add_artifact(name, category, description, None, status, self.selected_image_path)
        messagebox.showinfo("Success", "Artifact added successfully!")

        # Reset form
        self.name_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.selected_image_path = ""
        self.image_path_label.config(text="No file selected", foreground="gray")
        self.preview_label.config(image="", text="[No Preview]")
        self.thumbnail_image = None

        self.load_data()