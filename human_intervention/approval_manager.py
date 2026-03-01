"""
Approval Manager
Manages human approval gates for critical decisions and design sign-offs.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from utils.database import Database
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ApprovalManager:
    """Manages approval workflows for human-in-the-loop processes."""
    
    def __init__(self, db: Optional[Database] = None):
        """
        Initialize approval manager.
        
        Args:
            db: Database instance (creates new if not provided)
        """
        self.db = db or Database()
        logger.info("ApprovalManager initialized")

    def submit_for_approval(
        self,
        project_id,
        request_type: str,
        recommendation_summary: str,
        full_recommendation: str,
        priority: str = "medium"
    ) -> int:
        """Submit approval request. Returns approval ID."""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO approvals (project_id, approval_type, status, comments)
                VALUES (?, ?, 'pending', ?)
            """, (str(project_id), request_type, json.dumps({
                'recommendation_summary': recommendation_summary,
                'full_recommendation': full_recommendation,
                'priority': priority
            })))
            self.db.conn.commit()
            return cursor.lastrowid or 1
        except Exception as e:
            logger.error(f"Error submitting approval: {e}")
            return 0
    
    def request_approval(
        self,
        project_id: str,
        approval_type: str,
        approval_data: Dict[str, Any],
        confidence_score: float = 0.0,
        threshold: float = 0.7
    ) -> Dict[str, Any]:
        """
        Request approval for a decision or design.
        
        Args:
            project_id: Project identifier
            approval_type: Type of approval (architecture_design, tech_stack, security, etc.)
            approval_data: Data requiring approval
            confidence_score: AI confidence score (0.0-1.0)
            threshold: Confidence threshold requiring approval
        
        Returns:
            Dictionary with approval status and details
        """
        try:
            # Check if approval is needed based on confidence
            requires_approval = confidence_score < threshold
            
            approval_status = {
                'project_id': project_id,
                'approval_type': approval_type,
                'status': 'pending' if requires_approval else 'auto_approved',
                'confidence_score': confidence_score,
                'threshold': threshold,
                'approval_data': approval_data,
                'created_at': datetime.now().isoformat(),
                'requires_approval': requires_approval
            }
            
            # Save to database
            cursor = self.db.conn.cursor()
            cursor.execute("""
                INSERT INTO approvals (project_id, approval_type, status, comments)
                VALUES (?, ?, ?, ?)
            """, (
                project_id,
                approval_type,
                approval_status['status'],
                json.dumps(approval_data)
            ))
            self.db.conn.commit()
            
            logger.info(f"Approval requested: {approval_type} for project {project_id}, requires_approval={requires_approval}")
            return approval_status
            
        except Exception as e:
            logger.error(f"Error requesting approval: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def approve(
        self,
        project_id: str,
        approval_type: str,
        approver: str,
        comments: Optional[str] = None
    ) -> bool:
        """
        Approve a pending approval request.
        
        Args:
            project_id: Project identifier
            approval_type: Type of approval
            approver: Name/ID of approver
            comments: Optional approval comments
        
        Returns:
            True if approval successful
        """
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE approvals
                SET status = 'approved', approver = ?, comments = ?
                WHERE project_id = ? AND approval_type = ? AND status = 'pending'
            """, (approver, comments, project_id, approval_type))
            
            self.db.conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Approval granted: {approval_type} for project {project_id} by {approver}")
                return True
            else:
                logger.warning(f"No pending approval found: {approval_type} for project {project_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error approving: {e}")
            return False
    
    def reject(
        self,
        project_id: str,
        approval_type: str,
        approver: str,
        comments: str
    ) -> bool:
        """
        Reject a pending approval request.
        
        Args:
            project_id: Project identifier
            approval_type: Type of approval
            approver: Name/ID of approver
            comments: Rejection reason
        
        Returns:
            True if rejection successful
        """
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                UPDATE approvals
                SET status = 'rejected', approver = ?, comments = ?
                WHERE project_id = ? AND approval_type = ? AND status = 'pending'
            """, (approver, comments, project_id, approval_type))
            
            self.db.conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Approval rejected: {approval_type} for project {project_id} by {approver}")
                return True
            else:
                logger.warning(f"No pending approval found: {approval_type} for project {project_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error rejecting: {e}")
            return False
    
    def get_pending_approvals(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of pending approvals.
        
        Args:
            project_id: Optional project ID to filter by
        
        Returns:
            List of pending approval dictionaries
        """
        try:
            cursor = self.db.conn.cursor()
            
            if project_id:
                cursor.execute("""
                    SELECT * FROM approvals
                    WHERE project_id = ? AND status = 'pending'
                    ORDER BY created_at DESC
                """, (project_id,))
            else:
                cursor.execute("""
                    SELECT * FROM approvals
                    WHERE status = 'pending'
                    ORDER BY created_at DESC
                """)
            
            rows = cursor.fetchall()
            approvals = [dict(row) for row in rows]
            
            # Parse JSON comments
            for approval in approvals:
                if approval.get('comments'):
                    try:
                        approval['approval_data'] = json.loads(approval['comments'])
                    except:
                        pass
            
            return approvals
            
        except Exception as e:
            logger.error(f"Error getting pending approvals: {e}")
            return []
    
    def get_approval_history(self, project_id: str) -> List[Dict[str, Any]]:
        """
        Get approval history for a project.
        
        Args:
            project_id: Project identifier
        
        Returns:
            List of approval history records
        """
        try:
            cursor = self.db.conn.cursor()
            cursor.execute("""
                SELECT * FROM approvals
                WHERE project_id = ?
                ORDER BY created_at DESC
            """, (project_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except Exception as e:
            logger.error(f"Error getting approval history: {e}")
            return []
