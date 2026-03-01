"""
AI Agents Module
Specialized agents for architecture intelligence tasks.
"""

from .orchestrator import Orchestrator
from .architecture_assessment_agent import ArchitectureAssessmentAgent
from .tech_stack_strategy_agent import TechStackStrategyAgent
from .system_design_agent import SystemDesignAgent
from .security_compliance_agent import SecurityComplianceAgent

# Alias for tests compatibility
ArchitectureOrchestrator = Orchestrator

__all__ = [
    'Orchestrator',
    'ArchitectureOrchestrator',
    'ArchitectureAssessmentAgent',
    'TechStackStrategyAgent',
    'SystemDesignAgent',
    'SecurityComplianceAgent',
]
