import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import uuid as uuid_module

class SessionManager:
    def __init__(self, db_path: str = "sessions.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_count INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                message TEXT NOT NULL,
                is_user BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_session(self, session_id: str, first_message: str) -> Dict:
        session_name = self._generate_session_name(first_message)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO sessions (id, name, created_at, updated_at, message_count)
            VALUES (?, ?, ?, ?, 0)
        ''', (session_id, session_name, datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
        
        return {
            'id': session_id,
            'name': session_name,
            'created_at': datetime.now().isoformat(),
            'message_count': 0
        }
    
    def _generate_session_name(self, first_message: str) -> str:
        clean_message = first_message.strip()
        
        if len(clean_message) > 50:
            clean_message = clean_message[:47] + "..."
        
        timestamp = datetime.now().strftime("%m/%d %H:%M")
        
        return f"{clean_message} - {timestamp}"
    
    def add_message(self, session_id: str, message_id: str, message: str, is_user: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (id, session_id, message, is_user, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (message_id, session_id, message, is_user, datetime.now()))
        
        cursor.execute('''
            UPDATE sessions 
            SET message_count = message_count + 1, updated_at = ?
            WHERE id = ?
        ''', (datetime.now(), session_id))
        
        conn.commit()
        conn.close()
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, message, is_user, timestamp
            FROM messages
            WHERE session_id = ?
            ORDER BY timestamp ASC
        ''', (session_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'id': row[0],
                'message': row[1],
                'isUser': bool(row[2]),
                'timestamp': row[3],
                'sessionId': session_id
            })
        
        conn.close()
        return messages
    
    def get_all_sessions(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, created_at, updated_at, message_count
            FROM sessions
            ORDER BY updated_at DESC
        ''')
        
        sessions = []
        for row in cursor.fetchall():
            sessions.append({
                'id': row[0],
                'name': row[1],
                'created_at': row[2],
                'updated_at': row[3],
                'message_count': row[4]
            })
        
        conn.close()
        return sessions
    
    def get_session_info(self, session_id: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, created_at, updated_at, message_count
            FROM sessions
            WHERE id = ?
        ''', (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'created_at': row[2],
                'updated_at': row[3],
                'message_count': row[4]
            }
        return None
    
    def delete_session(self, session_id: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM messages WHERE session_id = ?', (session_id,))
        cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted