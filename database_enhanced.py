"""
Enhanced Database Module with Security
Production-level database operations with proper error handling
"""

import sqlite3
import hashlib
import secrets
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import os


class DatabaseManager:
    """Production-grade database manager with security"""
    
    def __init__(self, db_path: str = "resume_analyzer.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection with safety settings"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Users table with improved security fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    profile_picture TEXT,
                    bio TEXT
                )
            """)
            
            # Analysis history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    resume_filename TEXT NOT NULL,
                    resume_text TEXT,
                    job_description TEXT,
                    semantic_score REAL,
                    skill_score REAL,
                    keyword_score REAL,
                    experience_score REAL,
                    education_score REAL,
                    formatting_score REAL,
                    overall_score REAL,
                    matched_skills TEXT,
                    missing_skills TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Multi-resume comparison table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resume_comparison (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    resume1_id INTEGER,
                    resume2_id INTEGER,
                    resume3_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (resume1_id) REFERENCES analysis_history(id),
                    FOREIGN KEY (resume2_id) REFERENCES analysis_history(id),
                    FOREIGN KEY (resume3_id) REFERENCES analysis_history(id)
                )
            """)
            
            # Session management table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            # Settings/preferences table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE NOT NULL,
                    theme TEXT DEFAULT 'light',
                    notifications_enabled BOOLEAN DEFAULT 1,
                    language TEXT DEFAULT 'en',
                    privacy_level TEXT DEFAULT 'private',
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            print("Database initialized successfully")
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password using SHA-256 with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        return password_hash, salt
    
    def register_user(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user with secure password storage
        Returns: (success, message)
        """
        if not username or not email or not password:
            return False, "All fields are required"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            password_hash, salt = self.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, salt))
            
            user_id = cursor.lastrowid
            
            # Create user settings
            cursor.execute("""
                INSERT INTO user_settings (user_id)
                VALUES (?)
            """, (user_id,))
            
            conn.commit()
            return True, f"User '{username}' registered successfully"
            
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return False, "Username already exists"
            elif 'email' in str(e):
                return False, "Email already registered"
            return False, str(e)
        except Exception as e:
            return False, f"Registration error: {str(e)}"
        finally:
            conn.close()
    
    def login_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Login user and create session
        Returns: (success, user_data, message)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, username, email, password_hash, salt, is_active
                FROM users
                WHERE username = ?
            """, (username,))
            
            user = cursor.fetchone()
            
            if not user:
                return False, None, "Invalid username or password"
            
            if not user['is_active']:
                return False, None, "Account is inactive"
            
            # Verify password
            password_hash, _ = self.hash_password(password, user['salt'])
            
            if password_hash != user['password_hash']:
                return False, None, "Invalid username or password"
            
            # Create session
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now().isoformat()
            
            cursor.execute("""
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (?, ?, datetime('now', '+30 days'))
            """, (user['id'], session_token))
            
            # Update last login
            cursor.execute("""
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user['id'],))
            
            conn.commit()
            
            user_data = {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'session_token': session_token
            }
            
            return True, user_data, "Login successful"
            
        except Exception as e:
            return False, None, f"Login error: {str(e)}"
        finally:
            conn.close()
    
    def save_analysis(
        self,
        user_id: int,
        resume_filename: str,
        resume_text: str,
        job_description: str,
        scores: Dict,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> Tuple[bool, str, Optional[int]]:
        """
        Save resume analysis to database
        Returns: (success, message, analysis_id)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO analysis_history (
                    user_id, resume_filename, resume_text, job_description,
                    semantic_score, skill_score, keyword_score, experience_score,
                    education_score, formatting_score, overall_score,
                    matched_skills, missing_skills
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                resume_filename,
                resume_text,
                job_description,
                scores.get('semantic_match', 0),
                scores.get('skill_match', 0),
                scores.get('keyword_optimization', 0),
                scores.get('experience_relevance', 0),
                scores.get('education_relevance', 0),
                scores.get('formatting_structure', 0),
                scores.get('overall', 0),
                ','.join(matched_skills),
                ','.join(missing_skills)
            ))
            
            analysis_id = cursor.lastrowid
            conn.commit()
            
            return True, "Analysis saved successfully", analysis_id
            
        except Exception as e:
            return False, f"Save error: {str(e)}", None
        finally:
            conn.close()
    
    def get_user_history(
        self,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """Retrieve user's analysis history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM analysis_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
        finally:
            conn.close()
    
    def delete_analysis(self, analysis_id: int, user_id: int) -> Tuple[bool, str]:
        """Delete an analysis record (with user verification)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verify ownership before deleting
            cursor.execute("""
                SELECT user_id FROM analysis_history WHERE id = ?
            """, (analysis_id,))
            
            result = cursor.fetchone()
            
            if not result or result['user_id'] != user_id:
                return False, "Unauthorized or analysis not found"
            
            cursor.execute("""
                DELETE FROM analysis_history WHERE id = ?
            """, (analysis_id,))
            
            conn.commit()
            return True, "Analysis deleted successfully"
            
        except Exception as e:
            return False, f"Delete error: {str(e)}"
        finally:
            conn.close()
    
    def get_user_settings(self, user_id: int) -> Optional[Dict]:
        """Retrieve user settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT * FROM user_settings WHERE user_id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            return dict(result) if result else None
            
        except Exception as e:
            print(f"Error retrieving settings: {e}")
            return None
        finally:
            conn.close()
    
    def update_user_settings(self, user_id: int, settings: Dict) -> Tuple[bool, str]:
        """Update user settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            values = []
            
            for key, value in settings.items():
                updates.append(f"{key} = ?")
                values.append(value)
            
            values.append(user_id)
            
            cursor.execute(f"""
                UPDATE user_settings
                SET {', '.join(updates)}
                WHERE user_id = ?
            """, values)
            
            conn.commit()
            return True, "Settings updated successfully"
            
        except Exception as e:
            return False, f"Update error: {str(e)}"
        finally:
            conn.close()
    
    def logout_user(self, session_token: str) -> bool:
        """Invalidate session on logout"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE sessions
                SET is_active = 0
                WHERE session_token = ?
            """, (session_token,))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Logout error: {e}")
            return False
        finally:
            conn.close()


# Backward compatibility functions
def create_database():
    """Legacy function"""
    db = DatabaseManager()


def register_user(username: str, password: str):
    """Legacy function"""
    db = DatabaseManager()
    db.register_user(username, "", password)


def login_user(username: str, password: str):
    """Legacy function"""
    db = DatabaseManager()
    success, user, _ = db.login_user(username, password)
    return user if success else None


def save_history(username: str, resume_name: str, semantic_score: float,
                skill_score: float, overall_score: float):
    """Legacy function"""
    pass


def get_history(username: str):
    """Legacy function"""
    return []
