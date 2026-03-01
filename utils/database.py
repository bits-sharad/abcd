"""
Database operations for the Software Architecture Intelligence System.
Uses SQLite for storing project data, architecture assessments, and recommendations.
"""


import sqlite3
from typing import List, Dict, Any, Optional
from config import settings
from .logger import setup_logger


logger = setup_logger(__name__)




def get_connection():
   """Get database connection."""
   return sqlite3.connect(settings.DB_FILE)




def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
   """
   Execute a SELECT query and return results as list of dictionaries.


   Args:
       query: SQL query string
       params: Query parameters tuple


   Returns:
       List of dictionaries representing rows
   """
   try:
       conn = get_connection()
       conn.row_factory = sqlite3.Row
       cursor = conn.cursor()
       cursor.execute(query, params)
       rows = cursor.fetchall()
       conn.close()


       return [dict(row) for row in rows]
   except Exception as e:
       logger.error(f"Query execution error: {e}")
       return []




def insert_data(table: str, data: Dict[str, Any]) -> Optional[int]:
   """
   Insert data into a table.


   Args:
       table: Table name
       data: Dictionary of column: value pairs


   Returns:
       Last inserted row ID or None on error
   """
   try:
       columns = ', '.join(data.keys())
       placeholders = ', '.join(['?' for _ in data])
       query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"


       conn = get_connection()
       cursor = conn.cursor()
       cursor.execute(query, tuple(data.values()))
       conn.commit()
       last_id = cursor.lastrowid
       conn.close()


       logger.info(f"Inserted data into {table}, ID: {last_id}")
       return last_id
   except Exception as e:
       logger.error(f"Insert error: {e}")
       return None




def initialize_architecture_database() -> bool:
   """
   Initialize the database with required tables for architecture management.


   Returns:
       True if successful, False otherwise
   """
   try:
       conn = get_connection()
       cursor = conn.cursor()


       # Projects table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS projects (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_name TEXT NOT NULL,
               contact_email TEXT NOT NULL,
               project_type TEXT,
               scale TEXT,
               team_size INTEGER,
               budget_range TEXT,
               timeline TEXT,
               current_users INTEGER,
               expected_users INTEGER,
               compliance_requirements TEXT,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           )
       """)


       # Architecture components table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS architecture_components (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               component_name TEXT NOT NULL,
               component_type TEXT,
               architecture_pattern TEXT,
               scalability_tier TEXT,
               description TEXT,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Technology stack table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS tech_stack (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               technology_name TEXT NOT NULL,
               category TEXT,
               version TEXT,
               justification TEXT,
               maturity_level TEXT,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Architecture assessments table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS architecture_assessments (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               assessment_type TEXT,
               score INTEGER,
               strengths TEXT,
               weaknesses TEXT,
               recommendations TEXT,
               assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Security assessments table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS security_assessments (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               security_level TEXT,
               vulnerabilities TEXT,
               compliance_status TEXT,
               recommendations TEXT,
               assessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Design patterns table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS design_patterns (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               pattern_name TEXT NOT NULL,
               pattern_type TEXT,
               use_case TEXT,
               implementation_notes TEXT,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Architecture advisors table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS architecture_advisors (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL,
               specialization TEXT,
               experience_years INTEGER,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
           )
       """)


       # Project advisors mapping table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS project_advisors (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               advisor_id INTEGER,
               role TEXT,
               assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id),
               FOREIGN KEY (advisor_id) REFERENCES architecture_advisors(id)
           )
       """)


       # Approvals table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS approvals (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               request_type TEXT,
               recommendation_summary TEXT,
               full_recommendation TEXT,
               status TEXT DEFAULT 'pending',
               priority TEXT,
               submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               reviewed_at TIMESTAMP,
               reviewer_notes TEXT,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       # Feedback table
       cursor.execute("""
           CREATE TABLE IF NOT EXISTS feedback (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               project_id INTEGER,
               feedback_type TEXT,
               content TEXT,
               rating INTEGER,
               submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (project_id) REFERENCES projects(id)
           )
       """)


       conn.commit()
       conn.close()


       logger.info("Architecture database initialized successfully")
       return True


   except Exception as e:
       logger.error(f"Database initialization error: {e}")
       return False