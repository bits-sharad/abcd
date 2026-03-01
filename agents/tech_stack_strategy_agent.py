"""
Tech Stack Strategy Agent
Provides technology recommendations based on project requirements.
"""

import json
from typing import Dict, Any, List
import google.generativeai as genai

import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TechStackStrategyAgent:
    """Agent specialized in technology stack recommendations."""
    
    def __init__(self):
        """Initialize the agent with Gemini API."""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info("TechStackStrategyAgent initialized")
    
    def recommend(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate technology stack recommendations.
        
        Args:
            requirements: Dictionary containing:
                - project_type: Type of project (web app, API, mobile, etc.)
                - scale: Expected scale/load
                - performance_requirements: Performance needs
                - team_expertise: Team's technology expertise
                - constraints: Budget, compliance, or other constraints
        
        Returns:
            Dictionary containing:
                - recommendations: Recommended tech stack with justifications
                - alternatives: Alternative options with trade-offs
                - cost_analysis: Cost estimates
                - learning_curve: Learning curve assessment
                - confidence_score: Confidence level (0.0-1.0)
        """
        try:
            prompt = self._build_recommendation_prompt(requirements)
            
            response = self.model.generate_content(prompt)
            recommendation_text = response.text
            
            result = self._parse_recommendation_response(recommendation_text, requirements)
            
            logger.info("Tech stack recommendations generated")
            return result
            
        except Exception as e:
            logger.error(f"Error in tech stack recommendation: {e}")
            return {
                'recommendations': {},
                'alternatives': [],
                'cost_analysis': {},
                'learning_curve': 'Unknown',
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    def _build_recommendation_prompt(self, requirements: Dict[str, Any]) -> str:
        """Build the recommendation prompt for Gemini."""
        project_type = requirements.get('project_type', 'Not specified')
        scale = requirements.get('scale', 'Not specified')
        performance = requirements.get('performance_requirements', 'Not specified')
        team_expertise = requirements.get('team_expertise', [])
        constraints = requirements.get('constraints', {})
        
        prompt = f"""You are an expert technology consultant. Recommend an optimal technology stack for the following project requirements.

PROJECT REQUIREMENTS:
- Project Type: {project_type}
- Expected Scale: {scale}
- Performance Requirements: {performance}
- Team Expertise: {', '.join(team_expertise) if team_expertise else 'Not specified'}
- Constraints: {json.dumps(constraints, indent=2)}

AVAILABLE OPTIONS:
- Languages: {', '.join(config.SUPPORTED_LANGUAGES)}
- Cloud Providers: {', '.join(config.CLOUD_PROVIDERS)}
- Architecture Patterns: {', '.join(config.ARCHITECTURE_PATTERNS)}

Please provide comprehensive technology stack recommendations covering:

1. RECOMMENDED STACK
   - Frontend framework/library
   - Backend framework/runtime
   - Database(s)
   - Caching layer
   - Message queue/event streaming
   - Cloud infrastructure
   - DevOps tools
   - Monitoring and logging

2. JUSTIFICATION
   - Why each technology was chosen
   - How it fits the requirements
   - Performance characteristics
   - Ecosystem and community support

3. ALTERNATIVES
   - Alternative options for each layer
   - Trade-offs compared to recommendations
   - When to consider alternatives

4. COST ANALYSIS
   - Infrastructure costs (estimated monthly/yearly)
   - Licensing costs if applicable
   - Development time impact
   - Maintenance costs

5. LEARNING CURVE
   - Difficulty level for team
   - Training requirements
   - Time to productivity
   - Available resources and documentation

6. MIGRATION CONSIDERATIONS
   - If migrating from existing stack
   - Migration complexity
   - Risk factors

Format your response as structured JSON with:
- recommendations: Object with categories (frontend, backend, database, etc.) and technologies
- alternatives: Array of alternative stacks with trade-offs
- cost_analysis: Object with cost breakdown
- learning_curve: Assessment text
- confidence_score: Float between 0.0 and 1.0

Be specific with versions, frameworks, and provide actionable recommendations."""
        
        return prompt
    
    def _parse_recommendation_response(self, response_text: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the recommendation response."""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    'recommendations': parsed.get('recommendations', {}),
                    'alternatives': parsed.get('alternatives', []),
                    'cost_analysis': parsed.get('cost_analysis', {}),
                    'learning_curve': parsed.get('learning_curve', 'Unknown'),
                    'confidence_score': parsed.get('confidence_score', 0.8)
                }
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from response")
        
        return {
            'recommendations': {},
            'alternatives': [],
            'cost_analysis': {},
            'learning_curve': response_text[:500] if len(response_text) > 500 else response_text,
            'confidence_score': 0.7
        }
