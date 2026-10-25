import tkinter as tk
from tkinter import ttk
def main():
    root = tk.Tk()
    root.title("MUSEUM ARTIFACT MANAGER")
    root.geometry("900x600")
    ttk.Label(
        root,
        text="MUSEUM ARTIFACT MANAGER",
        font=("Cinzel", 18, "bold"),
    ).pack(pady=20)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)
    for name in ("Artifacts", "Locations", "Preservation"):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=name)
        ttk.Label(frame, text=f"{name} module coming soon").pack(pady=40)
    root.mainloop()
if __name__ == "__main__":
    main()
