import sqlite3

def create_db():
    con = sqlite3.connect(database="rms.db")    
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS course(
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            duration TEXT,
            charges TEXT,
            description TEXT
        )
    """)
    con.commit()
    
    # Student Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student(
            roll TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            gender TEXT,
            dob TEXT,
            contact TEXT,
            course TEXT,
            admission_date TEXT,
            state TEXT,
            city TEXT,
            pin TEXT,
            address TEXT
        )
    """)
    con.commit()
    con.close()

create_db()
