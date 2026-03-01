"""
Validation Utilities
Data validation functions for project data and requirements.
"""

from typing import Dict, Any, List, Optional


def validate_project_data(project_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate project data structure and required fields.
    
    Args:
        project_data: Dictionary containing project information
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = [
        'project_id', 'project_name', 'current_architecture',
        'components', 'tech_stack'
    ]
    
    for field in required_fields:
        if field not in project_data:
            return False, f"Missing required field: {field}"
    
    if not isinstance(project_data.get('components'), list):
        return False, "components must be a list"
    
    if not isinstance(project_data.get('tech_stack'), dict):
        return False, "tech_stack must be a dictionary"
    
    return True, None


def validate_requirements(requirements: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate requirements dictionary structure.
    
    Args:
        requirements: Dictionary containing project requirements
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(requirements, dict):
        return False, "requirements must be a dictionary"
    
    if 'project_type' not in requirements:
        return False, "Missing required field: project_type"
    
    return True, None


def validate_security_requirements(security_requirements: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate security requirements dictionary.
    
    Args:
        security_requirements: Dictionary containing security requirements
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(security_requirements, dict):
        return False, "security_requirements must be a dictionary"
    
    return True, None
