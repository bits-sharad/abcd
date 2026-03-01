"""
Architecture Assessment Agent
Analyzes current architecture for technical debt, scalability issues, and design flaws.
"""

import json
from typing import Dict, Any, Optional

import google.generativeai as genai

import config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Agent system instructions for architecture assessment
ARCHITECTURE_ASSESSMENT_INSTRUCTIONS = """You are an expert software architecture consultant agent. Your role is to analyze system architectures and provide actionable insights. You MUST cover these four areas in every assessment:

1. SYSTEM ARCHITECTURE PATTERNS ANALYSIS
   - Identify the architecture pattern(s) in use (e.g., Microservices, Monolithic, Serverless, Event-Driven, Layered, Hexagonal, CQRS)
   - Evaluate alignment with industry best practices
   - Assess pattern fit for the stated scale and team size
   - Compare against alternative patterns and their trade-offs

2. TECHNICAL DEBT IDENTIFICATION
   - Identify specific technical debt items with clear evidence
   - Rate severity: High (blocks scaling/security), Medium (impacts maintainability), Low (minor improvements)
   - Estimate remediation effort (S/M/L) and business impact
   - Prioritize by risk and ROI

3. SCALABILITY AND PERFORMANCE ASSESSMENT
   - Identify scalability bottlenecks (database, caching, compute, network)
   - Assess horizontal vs vertical scaling capabilities
   - Evaluate performance under load (latency, throughput, resource utilization)
   - Identify single points of failure and capacity limits

4. ACTIONABLE RECOMMENDATIONS
   - Provide prioritized, specific recommendations (not generic advice)
   - Include quick wins (low effort, high impact) and long-term improvements
   - Suggest migration strategies where applicable
   - Each recommendation must have: what to do, why, effort, and expected impact

Always respond with valid JSON containing: assessment, technical_debt, scalability_issues, recommendations, confidence_score."""


class ArchitectureAssessmentAgent:
    """Agent specialized in architecture assessment and analysis."""

    def __init__(self):
        """Initialize the agent with Gemini model and architecture assessment instructions."""
        # Import Agent, Gemini, settings
        settings = getattr(config, 'settings', config)
        api_key = getattr(settings, 'GEMINI_API_KEY', config.GEMINI_API_KEY)
        model_name = getattr(settings, 'GEMINI_MODEL', config.GEMINI_MODEL)

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name,
            system_instruction=ARCHITECTURE_ASSESSMENT_INSTRUCTIONS
        )
        logger.info("ArchitectureAssessmentAgent initialized")
    
    def run(self, project_data: Dict[str, Any]):
        """Run assessment (for test mocking). Returns object with .content attribute."""
        result = self.assess(project_data)
        return type('Response', (), {'content': json.dumps(result)})()

    def assess(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive architecture assessment.
        
        Args:
            project_data: Dictionary containing project architecture information
                - current_architecture: Description of current architecture
                - components: List of architecture components
                - tech_stack: Current technology stack
                - pain_points: Known issues or concerns
                - team_size: Size of development team
                - scale: Current scale/load requirements
        
        Returns:
            Dictionary containing:
                - assessment: Comprehensive assessment report
                - technical_debt: List of technical debt items
                - scalability_issues: List of scalability concerns
                - recommendations: List of improvement recommendations
                - confidence_score: Confidence level (0.0-1.0)
        """
        try:
            prompt = self._build_assessment_prompt(project_data)
            
            response = self.model.generate_content(prompt)
            assessment_text = response.text
            
            # Parse structured response
            result = self._parse_assessment_response(assessment_text, project_data)
            
            logger.info(f"Architecture assessment completed for project: {project_data.get('project_id', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error in architecture assessment: {e}")
            return {
                'assessment': f"Error during assessment: {str(e)}",
                'technical_debt': [],
                'scalability_issues': [],
                'recommendations': [],
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    def _build_assessment_prompt(self, project_data: Dict[str, Any]) -> str:
        """Build the assessment prompt for Gemini."""
        current_arch = project_data.get('current_architecture', 'Not specified')
        components = project_data.get('components', [])
        tech_stack = project_data.get('tech_stack', {})
        pain_points = project_data.get('pain_points', [])
        team_size = project_data.get('team_size', 'Not specified')
        scale = project_data.get('scale', 'Not specified')
        
        prompt = f"""You are an expert software architecture consultant. Analyze the following architecture and provide a comprehensive assessment.

PROJECT INFORMATION:
- Current Architecture: {current_arch}
- Components: {json.dumps(components, indent=2)}
- Technology Stack: {json.dumps(tech_stack, indent=2)}
- Known Pain Points: {pain_points if pain_points else 'None specified'}
- Team Size: {team_size}
- Scale Requirements: {scale}

Please provide a detailed architecture assessment covering:

1. ARCHITECTURE OVERVIEW
   - Overall architecture pattern and style
   - Strengths and weaknesses
   - Alignment with best practices

2. TECHNICAL DEBT ANALYSIS
   - Identify specific technical debt items
   - Rate severity (High/Medium/Low)
   - Estimate impact and remediation effort

3. SCALABILITY ASSESSMENT
   - Current scalability bottlenecks
   - Horizontal vs vertical scaling capabilities
   - Performance concerns under load

4. DESIGN QUALITY
   - Code organization and modularity
   - Separation of concerns
   - Design pattern usage
   - Maintainability score

5. RISK ASSESSMENT
   - High-risk areas
   - Single points of failure
   - Dependency risks

6. RECOMMENDATIONS
   - Prioritized improvement recommendations
   - Migration strategies if needed
   - Quick wins vs long-term improvements

Format your response as a structured JSON with the following keys:
- assessment: Comprehensive text assessment
- technical_debt: Array of objects with {{name, severity, impact, effort}}
- scalability_issues: Array of objects with {{issue, severity, affected_components}}
- recommendations: Array of objects with {{recommendation, priority, effort, impact}}
- confidence_score: Float between 0.0 and 1.0

Provide actionable, specific recommendations based on industry best practices."""
        
        return prompt
    
    def _parse_assessment_response(self, response_text: str, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the assessment response."""
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    'assessment': parsed.get('assessment', response_text),
                    'technical_debt': parsed.get('technical_debt', []),
                    'scalability_issues': parsed.get('scalability_issues', []),
                    'recommendations': parsed.get('recommendations', []),
                    'confidence_score': parsed.get('confidence_score', 0.8)
                }
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from response, using text format")
        
        # Fallback to text-only response
        return {
            'assessment': response_text,
            'technical_debt': [],
            'scalability_issues': [],
            'recommendations': [],
            'confidence_score': 0.7
        }
