import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'water_watch.db')

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            state TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            risk_level TEXT DEFAULT 'Safe',
            ph_level REAL,
            tds_level INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            district_id INTEGER,
            issue_type TEXT,
            description TEXT,
            reported_by TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (district_id) REFERENCES districts(id)
        );
    ''')

    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM districts")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executescript('''
            INSERT INTO districts (name, state, latitude, longitude, risk_level, ph_level, tds_level) VALUES
            ('Ahmedabad', 'Gujarat', 23.0225, 72.5714, 'Safe', 7.2, 320),
            ('Surat', 'Gujarat', 21.1702, 72.8311, 'Medium', 6.8, 580),
            ('Kanpur', 'Uttar Pradesh', 26.4499, 80.3319, 'High', 5.9, 1200),
            ('Mumbai', 'Maharashtra', 19.0760, 72.8777, 'Safe', 7.4, 280),
            ('Chennai', 'Tamil Nadu', 13.0827, 80.2707, 'Medium', 6.5, 650),
            ('Kolkata', 'West Bengal', 22.5726, 88.3639, 'High', 5.7, 1400),
            ('Jaipur', 'Rajasthan', 26.9124, 75.7873, 'Medium', 6.9, 720),
            ('Bhopal', 'Madhya Pradesh', 23.2599, 77.4126, 'Safe', 7.1, 310);
        ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized!")

if __name__ == '__main__':
    init_db()