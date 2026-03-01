"""
Security Compliance Agent
Evaluates security posture and compliance requirements.
"""

import json
from typing import Dict, Any, List
import google.generativeai as genai

import config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SecurityComplianceAgent:
    """Agent specialized in security assessment and compliance evaluation."""
    
    def __init__(self):
        """Initialize the agent with Gemini API."""
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
        logger.info("SecurityComplianceAgent initialized")
    
    def assess(self, security_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform security and compliance assessment.
        
        Args:
            security_requirements: Dictionary containing:
                - current_security_posture: Current security measures
                - compliance_standards: Required compliance (OWASP, PCI DSS, GDPR, etc.)
                - sensitive_data: Types of sensitive data handled
                - threat_model: Known threats or concerns
        
        Returns:
            Dictionary containing:
                - security_assessment: Comprehensive security evaluation
                - vulnerabilities: List of identified vulnerabilities
                - compliance_checklist: Compliance status for each standard
                - remediation_roadmap: Prioritized remediation steps
                - confidence_score: Confidence level (0.0-1.0)
        """
        try:
            prompt = self._build_security_prompt(security_requirements)
            
            response = self.model.generate_content(prompt)
            assessment_text = response.text
            
            result = self._parse_security_response(assessment_text, security_requirements)
            
            logger.info("Security assessment completed")
            return result
            
        except Exception as e:
            logger.error(f"Error in security assessment: {e}")
            return {
                'security_assessment': f"Error during assessment: {str(e)}",
                'vulnerabilities': [],
                'compliance_checklist': {},
                'remediation_roadmap': [],
                'confidence_score': 0.0,
                'error': str(e)
            }
    
    def _build_security_prompt(self, security_requirements: Dict[str, Any]) -> str:
        """Build the security assessment prompt for Gemini."""
        current_posture = security_requirements.get('current_security_posture', 'Not specified')
        compliance_standards = security_requirements.get('compliance_standards', [])
        sensitive_data = security_requirements.get('sensitive_data', [])
        threat_model = security_requirements.get('threat_model', {})
        
        prompt = f"""You are an expert cybersecurity consultant. Perform a comprehensive security and compliance assessment.

CURRENT SECURITY POSTURE:
{json.dumps(current_posture, indent=2) if isinstance(current_posture, dict) else current_posture}

COMPLIANCE STANDARDS REQUIRED:
{', '.join(compliance_standards) if compliance_standards else 'Not specified'}
Available standards: {', '.join(config.SECURITY_STANDARDS)}

SENSITIVE DATA HANDLED:
{json.dumps(sensitive_data, indent=2) if sensitive_data else 'Not specified'}

THREAT MODEL:
{json.dumps(threat_model, indent=2) if threat_model else 'Not specified'}

Please provide a comprehensive security assessment covering:

1. SECURITY POSTURE EVALUATION
   - Overall security maturity level
   - Strengths and weaknesses
   - Security architecture review

2. VULNERABILITY ASSESSMENT
   - OWASP Top 10 vulnerabilities check
   - Application security vulnerabilities
   - Infrastructure security issues
   - Data security concerns
   - For each vulnerability: severity (Critical/High/Medium/Low), impact, affected components

3. COMPLIANCE CHECKLIST
   - For each required standard, provide compliance status
   - Gap analysis for each standard
   - Required controls and their implementation status
   - Evidence needed for compliance

4. DATA PROTECTION
   - Encryption (at rest and in transit)
   - Data access controls
   - Data retention and deletion policies
   - Privacy considerations (GDPR, CCPA, etc.)

5. ACCESS CONTROL & AUTHENTICATION
   - Authentication mechanisms
   - Authorization model
   - Multi-factor authentication
   - Privileged access management

6. NETWORK SECURITY
   - Network segmentation
   - Firewall rules
   - DDoS protection
   - Intrusion detection/prevention

7. INCIDENT RESPONSE
   - Incident response plan
   - Logging and monitoring
   - Security event detection
   - Breach notification procedures

8. REMEDIATION ROADMAP
   - Prioritized list of security improvements
   - Quick wins vs long-term initiatives
   - Estimated effort and impact
   - Timeline recommendations

Format your response as structured JSON with:
- security_assessment: Text summary of security posture
- vulnerabilities: Array of vulnerability objects with {name, severity, category, impact, affected_components, remediation}
- compliance_checklist: Object with standard names as keys and {status, gaps, required_controls} as values
- remediation_roadmap: Array of remediation items with {action, priority, effort, impact, timeline}
- confidence_score: Float between 0.0 and 1.0

Provide actionable, specific security recommendations."""
        
        return prompt
    
    def _parse_security_response(self, response_text: str, security_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and structure the security response."""
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                parsed = json.loads(json_str)
                
                return {
                    'security_assessment': parsed.get('security_assessment', response_text),
                    'vulnerabilities': parsed.get('vulnerabilities', []),
                    'compliance_checklist': parsed.get('compliance_checklist', {}),
                    'remediation_roadmap': parsed.get('remediation_roadmap', []),
                    'confidence_score': parsed.get('confidence_score', 0.8)
                }
        except json.JSONDecodeError:
            logger.warning("Could not parse JSON from response")
        
        return {
            'security_assessment': response_text,
            'vulnerabilities': [],
            'compliance_checklist': {},
            'remediation_roadmap': [],
            'confidence_score': 0.7
        }
