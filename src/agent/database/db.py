import os
import sqlite3
from typing import Optional
from datetime import datetime



def init_db(force: bool = False):
    db_name = ".cache/search.db"

    if not os.path.exists(".cache/search.db"):
        if not os.path.exists(".cache"):
            os.makedirs(".cache")
        os.mknod(".cache/search.db")
    
    if force and os.path.exists(".cache/search.db"):
        os.remove(".cache/search.db")
    conn = sqlite3.connect(db_name)
     
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS queries
                 (query TEXT PRIMARY KEY, 
                  answer TEXT, 
                  created_at TIMESTAMP, 
                  updated_at TIMESTAMP)''')
    if force:
        current_time = datetime.now().isoformat()
        c.execute("INSERT OR REPLACE INTO queries VALUES (?, ?, ?, ?)", 
                  ("What is the purpose of this database?", 
                   "To cache query results for faster retrieval.",
                   current_time,
                   current_time))
        print("Database has been initialized with default data.")
        
    conn.commit()
    conn.close()

def save_query(query: str, answer: str):
    conn = sqlite3.connect('.cache/search.db')
    c = conn.cursor()
    current_time = datetime.now().isoformat()
    
    # Check if the query already exists
    c.execute("SELECT created_at FROM queries WHERE query = ?", (query,))
    existing = c.fetchone()
    
    if existing:
        # Update existing query
        c.execute("UPDATE queries SET answer = ?, updated_at = ? WHERE query = ?", 
                  (answer, current_time, query))
    else:
        # Insert new query
        c.execute("INSERT INTO queries VALUES (?, ?, ?, ?)", 
                  (query, answer, current_time, current_time))
    
    conn.commit()
    conn.close()

    
def get_cached_answer(query: str) -> Optional[tuple]:
    conn = sqlite3.connect('.cache/search.db')
    c = conn.cursor()
    c.execute("SELECT answer, created_at, updated_at FROM queries WHERE query = ?", (query,))
    result = c.fetchone()
    conn.close()
    return result if result else None

def remove_query(query: str) -> bool:
    conn = sqlite3.connect('cache/search.db')
    c = conn.cursor()
    
    try:
        c.execute("DELETE FROM queries WHERE query = ?", (query,))
        conn.commit()
        
        if c.rowcount > 0:
            print(f"Query '{query}' has been removed from the database.")
            return True
        else:
            print(f"Query '{query}' was not found in the database.")
            return False
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()