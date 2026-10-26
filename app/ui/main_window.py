import tkinter as tk
from tkinter import ttk
from app.ui.artifact_view import ArtifactView
from app.ui.location_view import LocationView
from app.ui.preservation_view import PreservationView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("MUSEUM ARTIFACT MANAGER - Dashboard")
        self.root.geometry("1000x650")

        # Top Title Header
        header_frame = ttk.Frame(root, padding=10)
        header_frame.pack(fill="x")

        ttk.Label(
            header_frame,
            text="Museum Artifact Management System",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left", padx=5)

        # Main Notebook / Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create placeholder tabs
        self.create_tabs()

    def create_tabs(self):
        # Artifacts Tab
        self.artifacts_frame = ArtifactView(self.notebook)
        self.notebook.add(self.artifacts_frame, text="Artifacts")

        # Locations Tab
        self.locations_frame = LocationView(self.notebook)
        self.notebook.add(self.locations_frame, text="Locations")
        ttk.Label(self.locations_frame, text="Locations Tracking View", font=("Segoe UI", 14)).pack(pady=40)

        # Preservation Tab
        self.preservation_frame = PreservationView(self.notebook)
        self.notebook.add(self.preservation_frame, text="Preservation")
        ttk.Label(self.preservation_frame, text="Preservation Records View", font=("Segoe UI", 14)).pack(pady=40)