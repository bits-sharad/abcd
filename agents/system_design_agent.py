"""
System Design Agent
Creates complete system architecture blueprints and designs.
"""

import json
import os
from typing import Dict, Any
import google.generativeai as genai

import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SystemDesignAgent:
    """Agent specialized in system architecture design."""
    
    def __init__(self):
        """Initialize the agent with Gemini API."""
        api_key = getattr(config, 'GEMINI_API_KEY', None) or os.getenv('GEMINI_API_KEY', '')
        model_name = getattr(config, 'GEMINI_MODEL', None) or os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        logger.info("SystemDesignAgent initialized")
    
    def run(self, design_requirements: Dict[str, Any]):
        """Run design (for test mocking). Returns object with .content attribute."""
        result = self.design(design_requirements)
        return type('Response', (), {'content': json.dumps(result)})()

    def design(self, design_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete system design architecture.
        
        Args:
            design_requirements: Dictionary containing:
                - functional_requirements: List of functional requirements
                - non_functional_requirements: Performance, scalability, etc.
                - scale_requirements: Expected scale and load
                - integration_requirements: Third-party integrations needed
        
        Returns:
            Dictionary containing:
                - architecture: Complete architecture design
                - components: System components and their responsibilities
                - apis: API design and endpoints
                - databases: Database schema and design
                - caching_strategy: Caching approach
                - deployment: Deployment architecture
                - confidence_score: Confidence level (0.0-1.0)
        """
        try:
            prompt = self._build_design_prompt(design_requirements)
            
            response = self.model.generate_content(prompt)
            design_text = response.text
            
            result = self._parse_design_response(design_text, design_requirements)
            
            logger.info("System design generated")
            return result
            
        except Exception as e:
            logger.error(f"Error in system design: {e}")
            return {
                'architecture': f"Error during design: {str(e)}",
                'components': [],
                'apis': [],
                'databases': [],
                'caching_strategy': {},
                'deployment': {},
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    def _build_design_prompt(self, design_requirements: Dict[str, Any]) -> str:
        """Build the design prompt for Gemini."""
        functional_reqs = design_requirements.get('functional_requirements', [])
        non_functional_reqs = design_requirements.get('non_functional_requirements', {})
        scale_reqs = design_requirements.get('scale_requirements', {})
        integration_reqs = design_requirements.get('integration_requirements', [])
        
        prompt = f"""You are an expert system architect. Design a complete, scalable system architecture based on the following requirements.

FUNCTIONAL REQUIREMENTS:
{json.dumps(functional_reqs, indent=2) if functional_reqs else 'Not specified'}

NON-FUNCTIONAL REQUIREMENTS:
{json.dumps(non_functional_reqs, indent=2) if non_functional_reqs else 'Not specified'}

SCALE REQUIREMENTS:
{json.dumps(scale_reqs, indent=2) if scale_reqs else 'Not specified'}

INTEGRATION REQUIREMENTS:
{json.dumps(integration_reqs, indent=2) if integration_reqs else 'None'}

Please provide a comprehensive system design covering:

1. ARCHITECTURE OVERVIEW
   - High-level architecture pattern (microservices, monolith, serverless, etc.)
   - Architecture diagram description
   - Key architectural decisions and rationale

2. SYSTEM COMPONENTS
   - List all major components/services
   - Responsibilities of each component
   - Communication patterns between components
   - Data flow

3. API DESIGN
   - RESTful API endpoints or GraphQL schema
   - Request/response formats
   - Authentication and authorization
   - Rate limiting and throttling
   - API versioning strategy

4. DATABASE DESIGN
   - Database selection (SQL, NoSQL, or hybrid)
   - Schema design for key entities
   - Data partitioning strategy
   - Replication and backup strategy
   - Data consistency model

5. CACHING STRATEGY
   - What to cache and where
   - Cache invalidation strategy
   - Cache warming approach
   - Distributed caching if needed

6. SCALABILITY DESIGN
   - Horizontal scaling approach
   - Load balancing strategy
   - Auto-scaling policies
   - Database scaling (sharding, read replicas)

7. DEPLOYMENT ARCHITECTURE
   - Infrastructure components
   - Container orchestration (if applicable)
   - CI/CD pipeline design
   - Monitoring and observability
   - Disaster recovery

8. SECURITY CONSIDERATIONS
   - Authentication and authorization
   - Data encryption (at rest and in transit)
   - Network security
   - API security

Format your response as structured JSON with:
- architecture: Text description of overall architecture
- components: Array of component objects with {{name, responsibility, interfaces, dependencies}}
- apis: Array of API endpoint objects with {{method, path, description, request, response}}
- databases: Array of database objects with {{type, schema, replication_strategy}}
- caching_strategy: Object describing caching approach
- deployment: Object describing deployment architecture
- confidence_score: Float between 0.0 and 1.0

Provide production-ready, scalable design recommendations."""
        
        return prompt
    
    def _parse_design_response(self, response_text: str, design_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the design response."""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    'architecture': parsed.get('architecture', response_text),
                    'components': parsed.get('components', []),
                    'apis': parsed.get('apis', []),
                    'databases': parsed.get('databases', []),
                    'caching_strategy': parsed.get('caching_strategy', {}),
                    'deployment': parsed.get('deployment', {}),
                    'confidence_score': parsed.get('confidence_score', 0.8)
                }
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from response")
        
        return {
            'architecture': response_text,
            'components': [],
            'apis': [],
            'databases': [],
            'caching_strategy': {},
            'deployment': {},
            'confidence_score': 0.7
        }
