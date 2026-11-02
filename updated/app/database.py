import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "museum.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS locations(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL, description TEXT);
        CREATE TABLE IF NOT EXISTS artifacts(id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT, description TEXT, location_id INTEGER, status TEXT DEFAULT 'On display', image_path TEXT, FOREIGN KEY(location_id) REFERENCES locations(id));
        CREATE TABLE IF NOT EXISTS preservation(id INTEGER PRIMARY KEY, artifact_id INTEGER, date TEXT, notes TEXT, conservator TEXT, FOREIGN KEY(artifact_id) REFERENCES artifacts(id));
        ''')
        # Keep existing tables compatible with older project versions.
        cols={r[1] for r in conn.execute("PRAGMA table_info(artifacts)")}
        if "image_path" not in cols: conn.execute("ALTER TABLE artifacts ADD COLUMN image_path TEXT")
        if "location_id" not in cols: conn.execute("ALTER TABLE artifacts ADD COLUMN location_id INTEGER")

def get_all_artifacts():
    with get_connection() as c:
        return c.execute("SELECT a.id,a.name,a.category,a.description,COALESCE(l.name,'Unassigned'),a.status,a.image_path FROM artifacts a LEFT JOIN locations l ON l.id=a.location_id ORDER BY a.id DESC").fetchall()

def add_artifact(name,category,description,location_id,status,image_path):
    with get_connection() as c:
        c.execute("INSERT INTO artifacts(name,category,description,location_id,status,image_path) VALUES(?,?,?,?,?,?)",(name,category,description,location_id,status,image_path))

def get_all_locations():
    with get_connection() as c: return c.execute("SELECT id,name,description FROM locations ORDER BY name").fetchall()

def add_location(name,description):
    with get_connection() as c: c.execute("INSERT INTO locations(name,description) VALUES(?,?)",(name,description))

def get_all_preservation_records():
    with get_connection() as c: return c.execute("SELECT p.id,a.name,p.date,p.notes,p.conservator FROM preservation p LEFT JOIN artifacts a ON a.id=p.artifact_id ORDER BY p.id DESC").fetchall()

def add_preservation_record(artifact_id,date,notes,conservator):
    with get_connection() as c: c.execute("INSERT INTO preservation(artifact_id,date,notes,conservator) VALUES(?,?,?,?)",(artifact_id,date,notes,conservator))
