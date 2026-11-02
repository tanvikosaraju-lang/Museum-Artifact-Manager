import tkinter as tk
from tkinter import ttk, messagebox
from app.database import *

class MainWindow:
    def __init__(self,root):
        self.root=root; root.title("Museum Artifact Management"); root.geometry("1100x700"); root.minsize(900,600)
        root.configure(bg="#17252a")
        st=ttk.Style(); st.theme_use("clam")
        st.configure("TNotebook",background="#17252a",borderwidth=0)
        st.configure("TNotebook.Tab",padding=(18,10),font=("Segoe UI",10,"bold"))
        st.configure("Treeview",rowheight=29,font=("Segoe UI",10))
        st.configure("Treeview.Heading",font=("Segoe UI",10,"bold"))
        st.configure("TButton",padding=7)
        head=tk.Frame(root,bg="#2b7a78",height=90); head.pack(fill="x")
        tk.Label(head,text="🏛  MUSEUM COLLECTIONS",bg="#2b7a78",fg="white",font=("Segoe UI",21,"bold")).pack(anchor="w",padx=25,pady=(15,0))
        tk.Label(head,text="Catalog • Discover • Preserve",bg="#2b7a78",fg="#def2f1",font=("Segoe UI",10)).pack(anchor="w",padx=28)
        self.tabs=ttk.Notebook(root); self.tabs.pack(fill="both",expand=True,padx=18,pady=16)
        self.build_artifacts(); self.build_locations(); self.build_preservation()
        self.refresh_all()
    def page(self,title):
        f=ttk.Frame(self.tabs,padding=16); self.tabs.add(f,text=title); return f
    def build_artifacts(self):
        f=self.page("✨ Artifacts")
        ttk.Label(f,text="Collection Explorer",font=("Segoe UI",17,"bold")).pack(anchor="w")
        ttk.Label(f,text="Add treasures to the catalogue and search your collection.").pack(anchor="w",pady=(2,12))
        form=ttk.LabelFrame(f,text="New artifact",padding=12); form.pack(fill="x",pady=6)
        self.a_name=tk.StringVar(); self.a_cat=tk.StringVar(); self.a_status=tk.StringVar(value="On display"); self.a_desc=tk.StringVar(); self.a_loc=tk.StringVar()
        fields=[("Artifact name",self.a_name),("Category",self.a_cat),("Status",self.a_status),("Description",self.a_desc)]
        for i,(label,var) in enumerate(fields):
            ttk.Label(form,text=label).grid(row=0,column=i,sticky="w",padx=4)
            ttk.Entry(form,textvariable=var,width=22).grid(row=1,column=i,padx=4,pady=5,sticky="ew")
        ttk.Label(form,text="Gallery / location").grid(row=2,column=0,sticky="w",padx=4)
        self.loc_combo=ttk.Combobox(form,textvariable=self.a_loc,state="readonly",width=22)
        self.loc_combo.grid(row=3,column=0,padx=4,pady=5,sticky="ew")
        ttk.Button(form,text="＋ Add to collection",command=self.add_art).grid(row=3,column=1,padx=4)
        self.search=tk.StringVar()
        bar=ttk.Frame(f); bar.pack(fill="x",pady=8)
        ttk.Label(bar,text="🔎 Find artifact").pack(side="left")
        ent=ttk.Entry(bar,textvariable=self.search); ent.pack(side="left",fill="x",expand=True,padx=8); ent.bind("<KeyRelease>",lambda e:self.refresh_artifacts())
        ttk.Button(bar,text="Clear",command=lambda:(self.search.set(""),self.refresh_artifacts())).pack(side="right")
        self.art_tree=self.table(f,("ID","Name","Category","Description","Location","Status"))
    def build_locations(self):
        f=self.page("🗺 Galleries")
        ttk.Label(f,text="Gallery Directory",font=("Segoe UI",17,"bold")).pack(anchor="w")
        ttk.Label(f,text="Create places to organize the museum's collection.").pack(anchor="w",pady=(2,12))
        form=ttk.LabelFrame(f,text="Add gallery",padding=12); form.pack(fill="x",pady=6)
        self.l_name=tk.StringVar(); self.l_desc=tk.StringVar()
        ttk.Label(form,text="Gallery name").grid(row=0,column=0,sticky="w")
        ttk.Entry(form,textvariable=self.l_name,width=30).grid(row=1,column=0,padx=(0,10),pady=5)
        ttk.Label(form,text="Description").grid(row=0,column=1,sticky="w")
        ttk.Entry(form,textvariable=self.l_desc,width=50).grid(row=1,column=1,padx=5,pady=5)
        ttk.Button(form,text="＋ Add gallery",command=self.add_loc).grid(row=1,column=2,padx=10)
        self.loc_tree=self.table(f,("ID","Gallery","Description"))
    def build_preservation(self):
        f=self.page("🧰 Preservation")
        ttk.Label(f,text="Care & Conservation Log",font=("Segoe UI",17,"bold")).pack(anchor="w")
        ttk.Label(f,text="Keep a record of restoration and routine care.").pack(anchor="w",pady=(2,12))
        form=ttk.LabelFrame(f,text="New care record",padding=12); form.pack(fill="x",pady=6)
        self.p_art=tk.StringVar(); self.p_date=tk.StringVar(); self.p_by=tk.StringVar(); self.p_notes=tk.StringVar()
        for i,(label,var) in enumerate([("Artifact",self.p_art),("Date (YYYY-MM-DD)",self.p_date),("Conservator",self.p_by),("Care notes",self.p_notes)]):
            ttk.Label(form,text=label).grid(row=0,column=i,sticky="w",padx=4)
            if i==0: self.p_combo=ttk.Combobox(form,textvariable=var,state="readonly",width=23); widget=self.p_combo
            else: widget=ttk.Entry(form,textvariable=var,width=23)
            widget.grid(row=1,column=i,padx=4,pady=5,sticky="ew")
        ttk.Button(form,text="＋ Save record",command=self.add_record).grid(row=1,column=4,padx=5)
        self.p_tree=self.table(f,("ID","Artifact","Date","Notes","Conservator"))
    def table(self,parent,columns):
        holder=ttk.Frame(parent); holder.pack(fill="both",expand=True,pady=8)
        tree=ttk.Treeview(holder,columns=columns,show="headings")
        for col in columns:
            tree.heading(col,text=col); tree.column(col,width=145,anchor="w")
        sy=ttk.Scrollbar(holder,orient="vertical",command=tree.yview); sx=ttk.Scrollbar(holder,orient="horizontal",command=tree.xview)
        tree.configure(yscrollcommand=sy.set,xscrollcommand=sx.set)
        tree.grid(row=0,column=0,sticky="nsew"); sy.grid(row=0,column=1,sticky="ns"); sx.grid(row=1,column=0,sticky="ew")
        holder.rowconfigure(0,weight=1); holder.columnconfigure(0,weight=1)
        return tree
    def fill(self,tree,rows):
        tree.delete(*tree.get_children())
        for row in rows: tree.insert("","end",values=row)
    def refresh_all(self):
        self.refresh_artifacts(); locations=get_all_locations(); self.fill(self.loc_tree,locations)
        self.loc_combo["values"]=["Unassigned"]+[r[1] for r in locations]
        if not self.a_loc.get(): self.a_loc.set("Unassigned")
        arts=get_all_artifacts(); self.p_combo["values"]=[f"{r[0]}: {r[1]}" for r in arts]
        if arts and not self.p_art.get(): self.p_art.set(f"{arts[0][0]}: {arts[0][1]}")
        self.fill(self.p_tree,get_all_preservation_records())
    def refresh_artifacts(self):
        query=self.search.get().lower() if hasattr(self,"search") else ""
        rows=[r[:6] for r in get_all_artifacts() if query in " ".join(str(x) for x in r).lower()]
        self.fill(self.art_tree,rows)
    def add_art(self):
        name=self.a_name.get().strip()
        if not name: messagebox.showwarning("Missing name","Please enter an artifact name."); return
        loc=next((r[0] for r in get_all_locations() if r[1]==self.a_loc.get()),None)
        try:
            add_artifact(name,self.a_cat.get().strip(),self.a_desc.get().strip(),loc,self.a_status.get().strip() or "On display","")
            for v in [self.a_name,self.a_cat,self.a_desc]: v.set("")
            self.refresh_all(); messagebox.showinfo("Added","Artifact added to the collection!")
        except Exception as e: messagebox.showerror("Could not add",str(e))
    def add_loc(self):
        name=self.l_name.get().strip()
        if not name: messagebox.showwarning("Missing name","Enter a gallery name."); return
        try:
            add_location(name,self.l_desc.get().strip()); self.l_name.set(""); self.l_desc.set(""); self.refresh_all()
        except Exception as e: messagebox.showerror("Could not add",str(e))
    def add_record(self):
        try:
            artifact_id=int(self.p_art.get().split(":",1)[0])
            if not self.p_date.get().strip(): raise ValueError("Enter a date.")
            add_preservation_record(artifact_id,self.p_date.get().strip(),self.p_notes.get().strip(),self.p_by.get().strip())
            self.p_date.set(""); self.p_by.set(""); self.p_notes.set(""); self.refresh_all()
            messagebox.showinfo("Saved","Care record saved.")
        except Exception as e: messagebox.showerror("Could not save",str(e))
