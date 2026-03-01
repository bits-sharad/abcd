"""
Feedback Handler
Captures and processes human feedback to improve agent behavior.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from utils.database import Database
from utils.logger import setup_logger

logger = setup_logger(__name__)


class FeedbackHandler:
    """Handles human feedback for improving agent outputs."""
    
    def __init__(self, db: Optional[Database] = None):
        """
        Initialize feedback handler.
        
        Args:
            db: Database instance (creates new if not provided)
        """
        self.db = db or Database()
        logger.info("FeedbackHandler initialized")
    
    def submit_feedback(
        self,
        project_id,
        feedback_type: str,
        feedback_data: Optional[Dict[str, Any]] = None,
        content: Optional[str] = None,
        rating: Optional[int] = None
    ):
        """
        Submit feedback for agent outputs.
        
        Args:
            project_id: Project identifier
            feedback_type: Type of feedback (assessment, recommendation, design, security)
            feedback_data: Feedback content and details (optional)
            content: Alternative to feedback_data - plain text content
            rating: Optional rating (1-5 scale)
        
        Returns:
            feedback_id (int) if saved successfully, False otherwise
        """
        try:
            data = feedback_data if feedback_data is not None else {'content': content or ''}
            feedback_record = {
                'project_id': project_id,
                'feedback_type': feedback_type,
                'rating': rating,
                'data': data,
                'content': content,
                'timestamp': datetime.now().isoformat()
            }
            
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO feedback (project_id, feedback_type, feedback_data)
                VALUES (?, ?, ?)
            """, (
                str(project_id),
                feedback_type,
                json.dumps(feedback_record)
            ))
            
            self.db.conn.commit()
            fid = cursor.lastrowid or 1
            
            logger.info(f"Feedback submitted: {feedback_type} for project {project_id}")
            return fid
            
        except Exception as e:
            logger.error(f"Error submitting feedback: {e}")
            return False
    
    def get_feedback_by_project(self, project_id: str, feedback_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Alias for get_feedback (test compatibility)."""
        return self.get_feedback(project_id, feedback_type)

    def get_feedback(self, project_id: str, feedback_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve feedback for a project.
        
        Args:
            project_id: Project identifier
            feedback_type: Optional filter by feedback type
        
        Returns:
            List of feedback records
        """
        try:
            cursor = self.db.conn.cursor()
            
            if feedback_type:
                cursor.execute("""
                    SELECT * FROM feedback
                    WHERE project_id = ? AND feedback_type = ?
                    ORDER BY created_at DESC
                """, (project_id, feedback_type))
            else:
                cursor.execute("""
                    SELECT * FROM feedback
                    WHERE project_id = ?
                    ORDER BY created_at DESC
                """, (project_id,))
            
            rows = cursor.fetchall()
            feedback_list = []
            
            for row in rows:
                feedback_dict = dict(row)
                try:
                    feedback_dict['data'] = json.loads(feedback_dict.get('feedback_data', '{}'))
                except:
                    feedback_dict['data'] = {}
                feedback_list.append(feedback_dict)
            
            return feedback_list
            
        except Exception as e:
            logger.error(f"Error getting feedback: {e}")
            return []
    
    def get_feedback_summary(self, project_id: str) -> Dict[str, Any]:
        """
        Get summary statistics of feedback.
        
        Args:
            project_id: Project identifier
        
        Returns:
            Dictionary with feedback statistics
        """
        try:
            feedback_list = self.get_feedback(project_id)
            
            summary = {
                'total_feedback': len(feedback_list),
                'by_type': {},
                'average_rating': 0.0,
                'ratings': []
            }
            
            total_rating = 0
            rating_count = 0
            
            for feedback in feedback_list:
                feedback_type = feedback.get('feedback_type', 'unknown')
                summary['by_type'][feedback_type] = summary['by_type'].get(feedback_type, 0) + 1
                
                data = feedback.get('data', {})
                if 'rating' in data and data['rating']:
                    total_rating += data['rating']
                    rating_count += 1
                    summary['ratings'].append(data['rating'])
            
            if rating_count > 0:
                summary['average_rating'] = total_rating / rating_count
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting feedback summary: {e}")
            return {
                'total_feedback': 0,
                'by_type': {},
                'average_rating': 0.0,
                'ratings': []
            }
