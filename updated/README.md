# Museum Artifact Management

A beginner-friendly interactive Tkinter + SQLite desktop application.

## Run
1. Install Python 3.10+ (Tkinter is included with standard Windows Python).
2. Extract this folder.
3. Open a terminal in the extracted folder.
4. Run: `python main.py`

Create an account from the login screen. No bcrypt or Pillow installation is needed.
The SQLite database is created automatically at `app/data/museum.db`.

Features:
- Account registration and sign-in (PBKDF2 password hashing)
- Artifact catalogue with live search
- Gallery/location management
- Preservation and conservation log
- SQLite persistence, tabbed interface, validation, and searchable tables
