"""
Database Initialization Script
Creates SQLite database with required tables for the car damage detection system
"""

import sqlite3
import os
from datetime import datetime

def init_database():
    """Initialize the SQLite database with required tables"""
    
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect('database/car_damage.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create damage_analyses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS damage_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            car_category TEXT NOT NULL,
            damage_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            confidence REAL NOT NULL,
            estimated_cost REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create cost_matrix table for repair cost calculations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cost_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            damage_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            base_cost REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default cost matrix data
    cost_data = [
        ('dent', 'low', 150.0),
        ('dent', 'medium', 300.0),
        ('dent', 'high', 600.0),
        ('scratch', 'low', 100.0),
        ('scratch', 'medium', 250.0),
        ('scratch', 'high', 500.0),
        ('crack', 'low', 200.0),
        ('crack', 'medium', 400.0),
        ('crack', 'high', 800.0),
        ('broken_glass', 'low', 300.0),
        ('broken_glass', 'medium', 500.0),
        ('broken_glass', 'high', 1000.0),
        ('rust', 'low', 120.0),
        ('rust', 'medium', 280.0),
        ('rust', 'high', 550.0),
    ]
    
    # Check if cost matrix is already populated
    cursor.execute('SELECT COUNT(*) FROM cost_matrix')
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            'INSERT INTO cost_matrix (damage_type, severity, base_cost) VALUES (?, ?, ?)',
            cost_data
        )
        print("✅ Cost matrix initialized with default values")
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_user ON damage_analyses(user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cost_lookup ON cost_matrix(damage_type, severity)')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print("📁 Database location: database/car_damage.db")
    print("📊 Tables created: users, damage_analyses, cost_matrix")

if __name__ == '__main__':
    init_database()