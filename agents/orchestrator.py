"""
Orchestrator - Central AI Coordinator
Coordinates specialized AI agents for complete architecture advisory.
"""

from typing import Dict, Any, Optional
import json

from .architecture_assessment_agent import ArchitectureAssessmentAgent
from .tech_stack_strategy_agent import TechStackStrategyAgent
from .system_design_agent import SystemDesignAgent
from .security_compliance_agent import SecurityComplianceAgent

from utils.logger import setup_logger
import config

logger = setup_logger(__name__)


class Orchestrator:
    """Central coordinator for AI agent orchestration."""
    
    def __init__(self):
        """Initialize orchestrator with all specialized agents."""
        self.architecture_agent = ArchitectureAssessmentAgent()
        self.tech_stack_agent = TechStackStrategyAgent()
        self.system_design_agent = SystemDesignAgent()
        self.security_agent = SecurityComplianceAgent()
        # Aliases for test compatibility
        self.assessment_agent = self.architecture_agent
        self.design_agent = self.system_design_agent
        logger.info("Orchestrator initialized with all agents")
    
    def assess_architecture(self, project_data: Dict[str, Any]) -> str:
        """
        Analyze current architecture and identify issues.
        
        Args:
            project_data: Dictionary containing:
                - current_architecture: Description of current architecture
                - components: List of architecture components
                - tech_stack: Current technology stack
                - pain_points: Known issues or concerns
                - team_size: Size of development team
                - scale: Current scale/load requirements
        
        Returns:
            Comprehensive architecture assessment report as JSON string
        """
        try:
            logger.info(f"Starting architecture assessment for project: {project_data.get('project_id', 'unknown')}")
            
            # Use run() if available (for test mocking), else assess()
            if hasattr(self.architecture_agent, 'run'):
                response = self.architecture_agent.run(project_data)
                try:
                    result = json.loads(response.content) if isinstance(getattr(response, 'content', None), str) else getattr(response, 'content', {})
                except (json.JSONDecodeError, TypeError):
                    result = {'assessment': getattr(response, 'content', str(response))}
            else:
                result = self.architecture_agent.assess(project_data)
            
            # Format as readable report
            report = self._format_architecture_report(result)
            
            logger.info("Architecture assessment completed")
            return report
            
        except Exception as e:
            logger.error(f"Error in architecture assessment orchestration: {e}")
            return json.dumps({
                'error': str(e),
                'assessment': 'Failed to complete architecture assessment'
            }, indent=2)
    
    def recommend_tech_stack(self, requirements: Dict[str, Any]) -> str:
        """
        Generate technology stack recommendations.
        
        Args:
            requirements: Dictionary containing:
                - project_type: Type of project
                - scale: Expected scale/load
                - performance_requirements: Performance needs
                - team_expertise: Team's technology expertise
                - constraints: Budget, compliance, or other constraints
        
        Returns:
            Technology stack recommendations report as JSON string
        """
        try:
            logger.info("Starting tech stack recommendation")
            
            if hasattr(self.tech_stack_agent, 'run'):
                response = self.tech_stack_agent.run(requirements)
                try:
                    result = json.loads(response.content) if isinstance(getattr(response, 'content', None), str) else getattr(response, 'content', {})
                except (json.JSONDecodeError, TypeError):
                    result = {'recommendations': {}, 'content': getattr(response, 'content', str(response))}
            else:
                result = self.tech_stack_agent.recommend(requirements)
            
            report = self._format_tech_stack_report(result)
            
            logger.info("Tech stack recommendation completed")
            return report
            
        except Exception as e:
            logger.error(f"Error in tech stack recommendation orchestration: {e}")
            return json.dumps({
                'error': str(e),
                'recommendations': 'Failed to generate tech stack recommendations'
            }, indent=2)
    
    def design_system_architecture(self, design_requirements: Dict[str, Any]) -> str:
        """
        Generate complete system design architecture.
        
        Args:
            design_requirements: Dictionary containing:
                - functional_requirements: List of functional requirements
                - non_functional_requirements: Performance, scalability, etc.
                - scale_requirements: Expected scale and load
                - integration_requirements: Third-party integrations needed
        
        Returns:
            Complete system design report as JSON string
        """
        try:
            logger.info("Starting system design")
            
            if hasattr(self.system_design_agent, 'run'):
                response = self.system_design_agent.run(design_requirements)
                try:
                    result = json.loads(response.content) if isinstance(getattr(response, 'content', None), str) else getattr(response, 'content', {})
                except (json.JSONDecodeError, TypeError):
                    result = {'architecture': getattr(response, 'content', str(response))}
            else:
                result = self.system_design_agent.design(design_requirements)
            
            report = self._format_system_design_report(result)
            
            logger.info("System design completed")
            return report
            
        except Exception as e:
            logger.error(f"Error in system design orchestration: {e}")
            return json.dumps({
                'error': str(e),
                'design': 'Failed to generate system design'
            }, indent=2)
    
    def assess_security_compliance(self, security_requirements: Dict[str, Any]) -> str:
        """
        Perform security and compliance assessment.
        
        Args:
            security_requirements: Dictionary containing:
                - current_security_posture: Current security measures
                - compliance_standards: Required compliance standards
                - sensitive_data: Types of sensitive data handled
                - threat_model: Known threats or concerns
        
        Returns:
            Security assessment report as JSON string
        """
        try:
            logger.info("Starting security compliance assessment")
            
            if hasattr(self.security_agent, 'run'):
                response = self.security_agent.run(security_requirements)
                try:
                    result = json.loads(response.content) if isinstance(getattr(response, 'content', None), str) else getattr(response, 'content', {})
                except (json.JSONDecodeError, TypeError):
                    result = {'assessment': getattr(response, 'content', str(response))}
            else:
                result = self.security_agent.assess(security_requirements)
            
            report = self._format_security_report(result)
            
            logger.info("Security compliance assessment completed")
            return report
            
        except Exception as e:
            logger.error(f"Error in security assessment orchestration: {e}")
            return json.dumps({
                'error': str(e),
                'assessment': 'Failed to complete security assessment'
            }, indent=2)
    
    def comprehensive_architecture_review(self, project_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Execute all 4 agents sequentially for complete architecture review.
        
        Args:
            project_data: Complete project data dictionary
        
        Returns:
            Dictionary with results from all agents:
                - architecture_assessment: Architecture assessment report
                - tech_stack_recommendations: Tech stack recommendations
                - system_design: System design architecture
                - security_compliance: Security assessment
        """
        try:
            logger.info("Starting comprehensive architecture review")
            
            results = {}
            
            # 1. Architecture Assessment
            logger.info("Step 1/4: Architecture Assessment")
            results['architecture_assessment'] = self.assess_architecture(project_data)
            
            # 2. Tech Stack Recommendations
            logger.info("Step 2/4: Tech Stack Recommendations")
            tech_requirements = {
                'project_type': project_data.get('project_type', 'Not specified'),
                'scale': project_data.get('scale', 'Not specified'),
                'performance_requirements': project_data.get('performance_requirements', 'Not specified'),
                'team_expertise': project_data.get('team_expertise', []),
                'constraints': project_data.get('constraints', {})
            }
            results['tech_stack_recommendations'] = self.recommend_tech_stack(tech_requirements)
            
            # 3. System Design
            logger.info("Step 3/4: System Design")
            design_requirements = {
                'functional_requirements': project_data.get('functional_requirements', []),
                'non_functional_requirements': project_data.get('non_functional_requirements', {}),
                'scale_requirements': project_data.get('scale_requirements', {}),
                'integration_requirements': project_data.get('integration_requirements', [])
            }
            results['system_design'] = self.design_system_architecture(design_requirements)
            
            # 4. Security & Compliance
            logger.info("Step 4/4: Security & Compliance")
            security_requirements = {
                'current_security_posture': project_data.get('current_security_posture', {}),
                'compliance_standards': project_data.get('compliance_standards', []),
                'sensitive_data': project_data.get('sensitive_data', []),
                'threat_model': project_data.get('threat_model', {})
            }
            results['security_compliance'] = self.assess_security_compliance(security_requirements)
            
            logger.info("Comprehensive architecture review completed")
            # Map to test-expected keys
            return {
                'assessment': results.get('architecture_assessment', ''),
                'tech_stack': results.get('tech_stack_recommendations', ''),
                'design': results.get('system_design', ''),
                'security': results.get('security_compliance', '')
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive review: {e}")
            return {
                'assessment': 'Failed',
                'tech_stack': 'Failed',
                'design': 'Failed',
                'security': 'Failed',
                'error': str(e)
            }
    
    def _format_architecture_report(self, result: Dict[str, Any]) -> str:
        """Format architecture assessment result as readable report."""
        return json.dumps(result, indent=2)
    
    def _format_tech_stack_report(self, result: Dict[str, Any]) -> str:
        """Format tech stack recommendation result as readable report."""
        return json.dumps(result, indent=2)
    
    def _format_system_design_report(self, result: Dict[str, Any]) -> str:
        """Format system design result as readable report."""
        return json.dumps(result, indent=2)
    
    def _format_security_report(self, result: Dict[str, Any]) -> str:
        """Format security assessment result as readable report."""
        return json.dumps(result, indent=2)

    def _format_components(self, components: list) -> str:
        """Format components list into readable text."""
        lines = []
        for i, comp in enumerate(components, 1):
            name = comp.get('name', comp.get('component_name', 'Unknown'))
            ctype = comp.get('type', comp.get('component_type', ''))
            desc = comp.get('description', comp.get('description', ''))
            lines.append(f"{i}. {name} ({ctype}): {desc}")
        return '\n'.join(lines) if lines else 'No components'

    def _format_tech_stack(self, tech_stack: dict) -> str:
        """Format tech stack dict into readable text."""
        lines = []
        for category, val in (tech_stack or {}).items():
            if isinstance(val, dict):
                name = val.get('name', val.get('technology_name', str(val)))
                version = val.get('version', '')
                lines.append(f"- {category}: {name} {version}".strip())
            else:
                lines.append(f"- {category}: {val}")
        return '\n'.join(lines) if lines else 'No tech stack'

    def _format_list(self, items: list) -> str:
        """Format list into readable bullet-point text."""
        if not items:
            return ''
        return '\n'.join(f"- {item}" for item in items)

    def _format_dict(self, d: dict) -> str:
        """Format dict into readable key-value text."""
        if not d:
            return ''
        return '\n'.join(f"- {k}: {v}" for k, v in d.items())
