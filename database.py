import sqlite3
import json
from typing import List, Dict, Any

def init_db():
    """Initialize the SQLite database with the projects table."""
    conn = sqlite3.connect('upwork_projects.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT UNIQUE NOT NULL,
            description TEXT,
            suitability_score INTEGER,
            analysis_summary TEXT,
            technologies TEXT,
            application_status TEXT DEFAULT 'Beklemede',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_project(project_data: Dict[str, Any]) -> bool:
    """Add a project to the database."""
    conn = sqlite3.connect('upwork_projects.db')
    cursor = conn.cursor()
    
    try:
        # Check if project already exists
        cursor.execute('SELECT id FROM projects WHERE link = ?', (project_data['link'],))
        if cursor.fetchone():
            conn.close()
            return False
        
        technologies_json = json.dumps(project_data.get('technologies', []))
        
        cursor.execute('''
            INSERT INTO projects (title, link, description, suitability_score, 
                                analysis_summary, technologies)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            project_data['title'],
            project_data['link'],
            project_data['description'],
            project_data.get('suitability_score', 0),
            project_data.get('analysis_summary', ''),
            technologies_json
        ))
        
        conn.commit()
        conn.close()
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        return False

def get_all_projects() -> List[Dict[str, Any]]:
    """Get all projects sorted by suitability score."""
    conn = sqlite3.connect('upwork_projects.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, link, description, suitability_score, 
               analysis_summary, technologies, application_status, created_at
        FROM projects 
        ORDER BY suitability_score DESC, created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    projects = []
    for row in rows:
        technologies = json.loads(row[6]) if row[6] else []
        projects.append({
            'id': row[0],
            'title': row[1],
            'link': row[2],
            'description': row[3],
            'suitability_score': row[4],
            'analysis_summary': row[5],
            'technologies': technologies,
            'application_status': row[7],
            'created_at': row[8]
        })
    
    return projects

def update_status(project_id: int, status: str) -> bool:
    """Update project application status."""
    conn = sqlite3.connect('upwork_projects.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'UPDATE projects SET application_status = ? WHERE id = ?',
            (status, project_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error:
        conn.close()
        return False

def get_project_stats() -> Dict[str, int]:
    """Get statistics about projects by status."""
    conn = sqlite3.connect('upwork_projects.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT application_status, COUNT(*) 
            FROM projects 
            GROUP BY application_status
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        stats = {
            'Beklemede': 0,
            'Başvuruldu': 0,
            'Kazanıldı': 0,
            'Kaybedildi': 0
        }
        
        for status, count in rows:
            if status in stats:
                stats[status] = count
        
        return stats
        
    except sqlite3.Error:
        conn.close()
        return {'Beklemede': 0, 'Başvuruldu': 0, 'Kazanıldı': 0, 'Kaybedildi': 0}