import sqlite3
import os
import bcrypt

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "museum.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Users table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        username TEXT UNIQUE NOT NULL,
                                                        password_hash TEXT NOT NULL
                   )
                   """)

    # Custom Credentials
    my_username = "tanvi"
    my_password = "Tanvi@357"

    cursor.execute("SELECT id FROM users WHERE username = ?", (my_username,))
    if not cursor.fetchone():
        hashed_pw = bcrypt.hashpw(my_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (my_username, hashed_pw))

    # Create Locations table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS locations (
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            name TEXT UNIQUE NOT NULL,
                                                            description TEXT
                   )
                   """)

    # Create Artifacts table with image_path
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS artifacts (
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            name TEXT NOT NULL,
                                                            category TEXT,
                                                            description TEXT,
                                                            location_id INTEGER,
                                                            status TEXT,
                                                            image_path TEXT,
                                                            FOREIGN KEY (location_id) REFERENCES locations(id)
                       )
                   """)

    # Create Preservation Records table
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS preservation (
                                                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                               artifact_id INTEGER,
                                                               date TEXT,
                                                               notes TEXT,
                                                               conservator TEXT,
                                                               FOREIGN KEY (artifact_id) REFERENCES artifacts(id)
                       )
                   """)

    conn.commit()
    conn.close()

# --- ARTIFACT HELPER FUNCTIONS ---
def get_all_artifacts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT a.id, a.name, a.category, a.description, l.name, a.status, a.image_path
                   FROM artifacts a
                            LEFT JOIN locations l ON a.location_id = l.id
                   """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_artifact(name, category, description, location_id, status, image_path):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO artifacts (name, category, description, location_id, status, image_path)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (name, category, description, location_id, status, image_path))
    conn.commit()
    conn.close()

def get_all_locations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM locations")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_location(name, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO locations (name, description)
                   VALUES (?, ?)
                   """, (name, description))
    conn.commit()
    conn.close()

def get_all_preservation_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.id, a.name, p.date, p.notes, p.conservator
                   FROM preservation p
                            LEFT JOIN artifacts a ON p.artifact_id = a.id
                   """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_preservation_record(artifact_id, date, notes, conservator):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO preservation (artifact_id, date, notes, conservator)
                   VALUES (?, ?, ?, ?)
                   """, (artifact_id, date, notes, conservator))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")