"""
Database setup and initialization for Library Management System
"""
import sqlite3
import os

DATABASE_FILE = "library.db"

def init_database():
    """Initialize the database with necessary tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            publication_year INTEGER,
            quantity INTEGER DEFAULT 1,
            available_quantity INTEGER DEFAULT 1,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Members/Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            membership_status TEXT DEFAULT 'active',
            outstanding_fine REAL DEFAULT 0.0
        )
    """)
    
    # Borrowing records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowing (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP NOT NULL,
            return_date TIMESTAMP,
            status TEXT DEFAULT 'borrowed',
            fine_amount REAL DEFAULT 0.0,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (book_id) REFERENCES books(book_id)
        )
    """)
    
    # Fine records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fines (
            fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            borrow_id INTEGER,
            amount REAL NOT NULL,
            reason TEXT,
            paid BOOLEAN DEFAULT 0,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES members(member_id),
            FOREIGN KEY (borrow_id) REFERENCES borrowing(borrow_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_connection():
    """Get a database connection"""
    return sqlite3.connect(DATABASE_FILE)

if __name__ == "__main__":
    init_database()
