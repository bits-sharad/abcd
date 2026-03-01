"""
Software Architecture Intelligence System - Main Application
Multi-interface architecture advisory platform with AI-powered insights.
"""

import sys
import sqlite3
from pathlib import Path

# Ensure project root is in Python path (fixes ImportError when run from different directories)
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import argparse
import json
from typing import Dict, Any, Optional

import streamlit as st
try:
    from streamlit_option_menu import option_menu
except ImportError:
    # Fallback if streamlit-option-menu is not installed
    def option_menu(*args, **kwargs):
        return st.selectbox("Navigation", kwargs.get('options', []))

import config

# Provide config.settings for utils.database (database.py expects "from config import settings")
if not hasattr(config, 'settings'):
    config.settings = type('Settings', (), {'DB_FILE': config.DB_FILE})()

from utils.database import get_connection, initialize_architecture_database
import utils.database as _db_module


class Database:
    """Database manager using utils.database. Provides .conn for ApprovalManager and FeedbackHandler."""

    def __init__(self, db_file: Optional[str] = None):
        # Use get_connection from database.py
        self.conn = get_connection()
        self.conn.row_factory = sqlite3.Row
        # Create HITL tables first (ApprovalManager/FeedbackHandler schema)
        self._ensure_hitl_tables()
        # Initialize remaining database tables from database.py
        initialize_architecture_database()

    def _ensure_hitl_tables(self):
        """Ensure approvals and feedback tables have schema expected by ApprovalManager/FeedbackHandler."""
        cursor = self.conn.cursor()
        # Create approvals table if not exists (aligns with ApprovalManager expectations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                approval_type TEXT NOT NULL,
                status TEXT NOT NULL,
                comments TEXT,
                approver TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Create feedback table if not exists (aligns with FeedbackHandler expectations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT NOT NULL,
                feedback_type TEXT NOT NULL,
                feedback_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

# Inject Database into utils.database for ApprovalManager and FeedbackHandler
_db_module.Database = Database

from utils.logger import setup_logger
from utils.database import Database
from utils.validators import validate_project_data
from agents.orchestrator import Orchestrator
from human_intervention.approval_manager import ApprovalManager
from human_intervention.feedback_handler import FeedbackHandler

logger = setup_logger(__name__)


def get_sample_project_data(project_id: str) -> Dict[str, Any]:
    """
    Return project data dict for PROJ001 and PROJ002.
    
    Args:
        project_id: Project identifier (PROJ001 or PROJ002)
    
    Returns:
        Dictionary containing project data
    """
    sample_projects = {
        "PROJ001": {
            "project_id": "PROJ001",
            "project_name": "E-Commerce Platform",
            "description": "Modern e-commerce platform with microservices architecture",
            "current_architecture": "Monolithic application with some microservices",
            "components": [
                {"name": "User Service", "type": "Microservice", "description": "Handles user authentication and profiles"},
                {"name": "Product Catalog", "type": "Microservice", "description": "Product information and search"},
                {"name": "Order Service", "type": "Microservice", "description": "Order processing and management"},
                {"name": "Payment Gateway", "type": "Integration", "description": "Third-party payment processing"},
                {"name": "Legacy Inventory", "type": "Monolith", "description": "Legacy inventory management system"}
            ],
            "tech_stack": {
                "backend": {"name": "Java Spring Boot", "version": "2.7.0"},
                "frontend": {"name": "React", "version": "18.0"},
                "database": {"name": "PostgreSQL", "version": "14.0"},
                "cache": {"name": "Redis", "version": "7.0"},
                "messaging": {"name": "RabbitMQ", "version": "3.11"}
            },
            "pain_points": [
                "Legacy inventory system causing bottlenecks",
                "Inconsistent API design across services",
                "Database performance issues under load",
                "Limited horizontal scaling capability"
            ],
            "team_size": 15,
            "scale": "100K+ daily active users, 10K+ orders/day",
            "project_type": "E-Commerce Platform",
            "performance_requirements": "Sub-200ms API response time, 99.9% uptime",
            "team_expertise": ["Java", "React", "PostgreSQL", "AWS"],
            "constraints": {"budget": "Medium", "compliance": ["PCI DSS"]},
            "functional_requirements": [
                "User registration and authentication",
                "Product catalog browsing and search",
                "Shopping cart management",
                "Order placement and tracking",
                "Payment processing",
                "Inventory management"
            ],
            "non_functional_requirements": {
                "scalability": "High",
                "performance": "Sub-200ms response time",
                "availability": "99.9% uptime",
                "security": "PCI DSS compliant"
            },
            "scale_requirements": {
                "users": "100K+ daily active users",
                "transactions": "10K+ orders per day",
                "peak_load": "5x normal load during sales events"
            },
            "integration_requirements": [
                "Payment gateway (Stripe/PayPal)",
                "Shipping providers (FedEx, UPS)",
                "Email service (SendGrid)",
                "Analytics (Google Analytics)"
            ],
            "current_security_posture": {
                "authentication": "JWT tokens",
                "encryption": "TLS 1.3",
                "firewall": "AWS Security Groups",
                "monitoring": "Basic logging"
            },
            "compliance_standards": ["OWASP Top 10", "PCI DSS"],
            "sensitive_data": ["Credit card information", "Personal user data", "Order history"],
            "threat_model": {
                "threats": ["SQL injection", "XSS attacks", "DDoS", "Data breaches"]
            }
        },
        "PROJ002": {
            "project_id": "PROJ002",
            "project_name": "SaaS Analytics Platform",
            "description": "Real-time analytics platform for business intelligence",
            "current_architecture": "Serverless architecture with Lambda functions",
            "components": [
                {"name": "Data Ingestion", "type": "Lambda", "description": "Real-time data ingestion"},
                {"name": "Data Processing", "type": "Lambda", "description": "ETL and data transformation"},
                {"name": "Analytics Engine", "type": "ECS Service", "description": "Analytics computation"},
                {"name": "API Gateway", "type": "API Gateway", "description": "RESTful API endpoints"},
                {"name": "Dashboard Frontend", "type": "S3 + CloudFront", "description": "React-based dashboard"}
            ],
            "tech_stack": {
                "backend": {"name": "Python", "version": "3.11"},
                "frontend": {"name": "React + TypeScript", "version": "18.0"},
                "database": {"name": "DynamoDB", "version": "Latest"},
                "warehouse": {"name": "Redshift", "version": "Latest"},
                "compute": {"name": "AWS Lambda", "version": "Latest"},
                "orchestration": {"name": "Step Functions", "version": "Latest"}
            },
            "pain_points": [
                "Cold start latency in Lambda functions",
                "Cost optimization needed",
                "Real-time processing limitations",
                "Complex data pipeline debugging"
            ],
            "team_size": 8,
            "scale": "1M+ events/day, 500+ concurrent users",
            "project_type": "SaaS Analytics Platform",
            "performance_requirements": "Real-time processing (<1s latency), 99.95% uptime",
            "team_expertise": ["Python", "React", "TypeScript", "AWS"],
            "constraints": {"budget": "Optimize costs", "compliance": ["GDPR"]},
            "functional_requirements": [
                "Real-time data ingestion",
                "Data transformation and ETL",
                "Analytics dashboard",
                "Custom report generation",
                "Data export capabilities",
                "User access control"
            ],
            "non_functional_requirements": {
                "scalability": "Very High",
                "performance": "Real-time (<1s latency)",
                "availability": "99.95% uptime",
                "cost": "Cost-optimized"
            },
            "scale_requirements": {
                "events": "1M+ events per day",
                "users": "500+ concurrent users",
                "data_volume": "100GB+ daily ingestion"
            },
            "integration_requirements": [
                "Data sources (APIs, databases)",
                "Third-party analytics tools",
                "Notification services (SNS, SES)"
            ],
            "current_security_posture": {
                "authentication": "OAuth 2.0",
                "encryption": "TLS 1.3, encryption at rest",
                "access_control": "IAM roles",
                "monitoring": "CloudWatch, GuardDuty"
            },
            "compliance_standards": ["OWASP Top 10", "GDPR"],
            "sensitive_data": ["User analytics data", "Business metrics", "Customer data"],
            "threat_model": {
                "threats": ["Data leakage", "Unauthorized access", "API abuse"]
            }
        }
    }
    
    return sample_projects.get(project_id, {})


def render_streamlit_ui():
    """Create Streamlit web interface with all pages."""
    st.set_page_config(
        page_title="Architecture Intelligence System",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = Orchestrator()
    if 'db' not in st.session_state:
        st.session_state.db = Database()
    if 'approval_manager' not in st.session_state:
        st.session_state.approval_manager = ApprovalManager(st.session_state.db)
    if 'feedback_handler' not in st.session_state:
        st.session_state.feedback_handler = FeedbackHandler(st.session_state.db)
    if 'selected_project' not in st.session_state:
        st.session_state.selected_project = None
    if 'project_data' not in st.session_state:
        st.session_state.project_data = None
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🏗️ Architecture Intelligence")
        st.markdown("---")
        
        # Project selection
        project_options = ["PROJ001", "PROJ002"]
        selected_project = st.selectbox(
            "Select Project",
            options=[""] + project_options,
            index=0
        )
        
        if selected_project:
            st.session_state.selected_project = selected_project
            st.session_state.project_data = get_sample_project_data(selected_project)
            st.success(f"Loaded: {st.session_state.project_data.get('project_name', selected_project)}")
        
        st.markdown("---")
        
        # Navigation menu
        selected = option_menu(
            menu_title="Navigation",
            options=[
                "Dashboard",
                "Architecture Assessment",
                "Tech Stack Strategy",
                "System Design",
                "Security & Compliance",
                "Comprehensive Review",
                "Project Management",
                "Settings"
            ],
            icons=[
                "speedometer2",
                "clipboard-check",
                "stack",
                "diagram-3",
                "shield-check",
                "file-text",
                "kanban",
                "gear"
            ],
            menu_icon="cast",
            default_index=0
        )
    
    # Page routing
    if selected == "Dashboard":
        render_dashboard_page()
    elif selected == "Architecture Assessment":
        render_architecture_assessment_page()
    elif selected == "Tech Stack Strategy":
        render_tech_stack_page()
    elif selected == "System Design":
        render_system_design_page()
    elif selected == "Security & Compliance":
        render_security_page()
    elif selected == "Comprehensive Review":
        render_comprehensive_review_page()
    elif selected == "Project Management":
        render_project_management_page()
    elif selected == "Settings":
        render_settings_page()


def render_dashboard_page():
    """Dashboard - Project overview, metrics, pain points."""
    st.header("📊 Dashboard")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    project = st.session_state.project_data
    
    # Project overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project ID", project.get('project_id', 'N/A'))
    with col2:
        st.metric("Team Size", project.get('team_size', 'N/A'))
    with col3:
        st.metric("Architecture", project.get('current_architecture', 'N/A')[:20] + "...")
    with col4:
        st.metric("Scale", project.get('scale', 'N/A')[:20] + "...")
    
    st.markdown("---")
    
    # Project details
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Project Information")
        st.write(f"**Name:** {project.get('project_name', 'N/A')}")
        st.write(f"**Description:** {project.get('description', 'N/A')}")
        st.write(f"**Type:** {project.get('project_type', 'N/A')}")
        
        st.subheader("Technology Stack")
        tech_stack = project.get('tech_stack', {})
        for category, tech in tech_stack.items():
            if isinstance(tech, dict):
                st.write(f"- **{category.title()}:** {tech.get('name', 'N/A')} {tech.get('version', '')}")
            else:
                st.write(f"- **{category.title()}:** {tech}")
    
    with col2:
        st.subheader("Architecture Components")
        components = project.get('components', [])
        for comp in components:
            st.write(f"- **{comp.get('name', 'N/A')}** ({comp.get('type', 'N/A')})")
            st.caption(comp.get('description', ''))
        
        st.subheader("Pain Points")
        pain_points = project.get('pain_points', [])
        for i, point in enumerate(pain_points, 1):
            st.write(f"{i}. {point}")


def render_architecture_assessment_page():
    """Architecture Assessment - AI-powered analysis & recommendations."""
    st.header("🔍 Architecture Assessment")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    if st.button("Run Architecture Assessment", type="primary"):
        with st.spinner("Analyzing architecture..."):
            result = st.session_state.orchestrator.assess_architecture(st.session_state.project_data)
            
            try:
                assessment_data = json.loads(result)
                st.session_state.assessment_result = assessment_data
            except:
                st.session_state.assessment_result = {"assessment": result}
    
    if 'assessment_result' in st.session_state:
        result = st.session_state.assessment_result
        
        st.subheader("Assessment Report")
        st.write(result.get('assessment', 'No assessment available'))
        
        if result.get('technical_debt'):
            st.subheader("Technical Debt")
            for debt in result['technical_debt']:
                with st.expander(f"{debt.get('name', 'Unknown')} - {debt.get('severity', 'N/A')}"):
                    st.write(f"**Impact:** {debt.get('impact', 'N/A')}")
                    st.write(f"**Effort:** {debt.get('effort', 'N/A')}")
        
        if result.get('scalability_issues'):
            st.subheader("Scalability Issues")
            for issue in result['scalability_issues']:
                st.write(f"- **{issue.get('issue', 'Unknown')}** ({issue.get('severity', 'N/A')})")
        
        if result.get('recommendations'):
            st.subheader("Recommendations")
            for rec in result['recommendations']:
                with st.expander(f"{rec.get('recommendation', 'Unknown')} - Priority: {rec.get('priority', 'N/A')}"):
                    st.write(f"**Effort:** {rec.get('effort', 'N/A')}")
                    st.write(f"**Impact:** {rec.get('impact', 'N/A')}")


def render_tech_stack_page():
    """Tech Stack Strategy - Technology recommendations & comparisons."""
    st.header("📚 Tech Stack Strategy")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    project = st.session_state.project_data
    
    requirements = {
        'project_type': project.get('project_type', ''),
        'scale': project.get('scale', ''),
        'performance_requirements': project.get('performance_requirements', ''),
        'team_expertise': project.get('team_expertise', []),
        'constraints': project.get('constraints', {})
    }
    
    if st.button("Generate Tech Stack Recommendations", type="primary"):
        with st.spinner("Generating recommendations..."):
            result = st.session_state.orchestrator.recommend_tech_stack(requirements)
            
            try:
                rec_data = json.loads(result)
                st.session_state.tech_stack_result = rec_data
            except:
                st.session_state.tech_stack_result = {"recommendations": result}
    
    if 'tech_stack_result' in st.session_state:
        result = st.session_state.tech_stack_result
        
        if result.get('recommendations'):
            st.subheader("Recommended Technology Stack")
            recs = result['recommendations']
            if isinstance(recs, dict):
                for category, tech in recs.items():
                    st.write(f"**{category.title()}:** {tech}")
            else:
                st.write(recs)
        
        if result.get('alternatives'):
            st.subheader("Alternative Options")
            for alt in result['alternatives']:
                with st.expander(f"Alternative {result['alternatives'].index(alt) + 1}"):
                    st.write(alt)
        
        if result.get('cost_analysis'):
            st.subheader("Cost Analysis")
            st.json(result['cost_analysis'])
        
        if result.get('learning_curve'):
            st.subheader("Learning Curve Assessment")
            st.write(result['learning_curve'])


def render_system_design_page():
    """System Design - Complete architecture blueprints."""
    st.header("🏛️ System Design")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    project = st.session_state.project_data
    
    design_requirements = {
        'functional_requirements': project.get('functional_requirements', []),
        'non_functional_requirements': project.get('non_functional_requirements', {}),
        'scale_requirements': project.get('scale_requirements', {}),
        'integration_requirements': project.get('integration_requirements', [])
    }
    
    if st.button("Generate System Design", type="primary"):
        with st.spinner("Designing system architecture..."):
            result = st.session_state.orchestrator.design_system_architecture(design_requirements)
            
            try:
                design_data = json.loads(result)
                st.session_state.design_result = design_data
            except:
                st.session_state.design_result = {"architecture": result}
    
    if 'design_result' in st.session_state:
        result = st.session_state.design_result
        
        st.subheader("Architecture Overview")
        st.write(result.get('architecture', 'No design available'))
        
        if result.get('components'):
            st.subheader("System Components")
            for comp in result['components']:
                with st.expander(comp.get('name', 'Unknown Component')):
                    st.write(f"**Responsibility:** {comp.get('responsibility', 'N/A')}")
                    st.write(f"**Interfaces:** {comp.get('interfaces', 'N/A')}")
        
        if result.get('apis'):
            st.subheader("API Design")
            for api in result['apis']:
                st.write(f"**{api.get('method', 'N/A')}** {api.get('path', 'N/A')}")
                st.caption(api.get('description', ''))
        
        if result.get('databases'):
            st.subheader("Database Design")
            for db in result['databases']:
                st.write(f"**Type:** {db.get('type', 'N/A')}")
                st.write(f"**Schema:** {db.get('schema', 'N/A')}")


def render_security_page():
    """Security & Compliance - Vulnerability assessments & remediation."""
    st.header("🔒 Security & Compliance")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    project = st.session_state.project_data
    
    security_requirements = {
        'current_security_posture': project.get('current_security_posture', {}),
        'compliance_standards': project.get('compliance_standards', []),
        'sensitive_data': project.get('sensitive_data', []),
        'threat_model': project.get('threat_model', {})
    }
    
    if st.button("Run Security Assessment", type="primary"):
        with st.spinner("Assessing security..."):
            result = st.session_state.orchestrator.assess_security_compliance(security_requirements)
            
            try:
                security_data = json.loads(result)
                st.session_state.security_result = security_data
            except:
                st.session_state.security_result = {"security_assessment": result}
    
    if 'security_result' in st.session_state:
        result = st.session_state.security_result
        
        st.subheader("Security Assessment")
        st.write(result.get('security_assessment', 'No assessment available'))
        
        if result.get('vulnerabilities'):
            st.subheader("Identified Vulnerabilities")
            for vuln in result['vulnerabilities']:
                severity_color = {
                    'Critical': '🔴',
                    'High': '🟠',
                    'Medium': '🟡',
                    'Low': '🟢'
                }.get(vuln.get('severity', 'Unknown'), '⚪')
                
                with st.expander(f"{severity_color} {vuln.get('name', 'Unknown')} - {vuln.get('severity', 'N/A')}"):
                    st.write(f"**Category:** {vuln.get('category', 'N/A')}")
                    st.write(f"**Impact:** {vuln.get('impact', 'N/A')}")
                    st.write(f"**Remediation:** {vuln.get('remediation', 'N/A')}")
        
        if result.get('compliance_checklist'):
            st.subheader("Compliance Checklist")
            for standard, status in result['compliance_checklist'].items():
                if isinstance(status, dict):
                    compliance_status = status.get('status', 'Unknown')
                    st.write(f"**{standard}:** {compliance_status}")
                    if status.get('gaps'):
                        st.caption(f"Gaps: {status['gaps']}")
                else:
                    st.write(f"**{standard}:** {status}")
        
        if result.get('remediation_roadmap'):
            st.subheader("Remediation Roadmap")
            for item in result['remediation_roadmap']:
                st.write(f"- **{item.get('action', 'Unknown')}** (Priority: {item.get('priority', 'N/A')})")


def render_comprehensive_review_page():
    """Comprehensive Review - Multi-agent analysis results."""
    st.header("📋 Comprehensive Review")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    if st.button("Run Comprehensive Review", type="primary"):
        with st.spinner("Running comprehensive analysis (this may take a few minutes)..."):
            results = st.session_state.orchestrator.comprehensive_architecture_review(st.session_state.project_data)
            st.session_state.comprehensive_results = results
    
    if 'comprehensive_results' in st.session_state:
        results = st.session_state.comprehensive_results
        
        tabs = st.tabs([
            "Architecture Assessment",
            "Tech Stack",
            "System Design",
            "Security & Compliance"
        ])
        
        with tabs[0]:
            st.write(results.get('architecture_assessment', 'N/A'))
        
        with tabs[1]:
            st.write(results.get('tech_stack_recommendations', 'N/A'))
        
        with tabs[2]:
            st.write(results.get('system_design', 'N/A'))
        
        with tabs[3]:
            st.write(results.get('security_compliance', 'N/A'))


def render_project_management_page():
    """Project Management - Approvals, feedback, tracking."""
    st.header("📁 Project Management")
    
    if not st.session_state.project_data:
        st.warning("Please select a project from the sidebar.")
        return
    
    project_id = st.session_state.project_data.get('project_id')
    
    tabs = st.tabs(["Approvals", "Feedback", "History"])
    
    with tabs[0]:
        st.subheader("Pending Approvals")
        approvals = st.session_state.approval_manager.get_pending_approvals(project_id)
        
        if approvals:
            for approval in approvals:
                with st.expander(f"{approval.get('approval_type', 'Unknown')} - {approval.get('status', 'N/A')}"):
                    st.write(f"**Status:** {approval.get('status', 'N/A')}")
                    st.write(f"**Created:** {approval.get('created_at', 'N/A')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Approve", key=f"approve_{approval.get('id')}"):
                            st.session_state.approval_manager.approve(
                                project_id,
                                approval.get('approval_type'),
                                "User",
                                "Approved via UI"
                            )
                            st.success("Approved!")
                            st.rerun()
                    
                    with col2:
                        comments = st.text_input(f"Rejection reason", key=f"reject_{approval.get('id')}")
                        if st.button(f"Reject", key=f"reject_btn_{approval.get('id')}"):
                            if comments:
                                st.session_state.approval_manager.reject(
                                    project_id,
                                    approval.get('approval_type'),
                                    "User",
                                    comments
                                )
                                st.success("Rejected!")
                                st.rerun()
        else:
            st.info("No pending approvals")
    
    with tabs[1]:
        st.subheader("Submit Feedback")
        
        feedback_type = st.selectbox("Feedback Type", ["assessment", "recommendation", "design", "security"])
        feedback_text = st.text_area("Feedback")
        rating = st.slider("Rating (1-5)", 1, 5, 3)
        
        if st.button("Submit Feedback"):
            feedback_data = {"text": feedback_text, "rating": rating}
            if st.session_state.feedback_handler.submit_feedback(project_id, feedback_type, feedback_data, rating):
                st.success("Feedback submitted!")
        
        st.subheader("Feedback History")
        feedback_list = st.session_state.feedback_handler.get_feedback(project_id)
        for feedback in feedback_list:
            st.write(f"**{feedback.get('feedback_type', 'Unknown')}** - Rating: {feedback.get('data', {}).get('rating', 'N/A')}")
            st.caption(feedback.get('data', {}).get('text', ''))
    
    with tabs[2]:
        st.subheader("Approval History")
        history = st.session_state.approval_manager.get_approval_history(project_id)
        for item in history:
            st.write(f"**{item.get('approval_type', 'Unknown')}** - {item.get('status', 'N/A')} - {item.get('created_at', 'N/A')}")


def render_settings_page():
    """Settings - Configuration and preferences."""
    st.header("⚙️ Settings")
    
    st.subheader("Configuration")
    st.write(f"**API Model:** {config.GEMINI_MODEL}")
    st.write(f"**Database:** {config.DB_FILE}")
    st.write(f"**App Version:** {config.APP_VERSION}")
    
    st.subheader("API Key")
    api_key = st.text_input("Gemini API Key", type="password", value=config.GEMINI_API_KEY)
    if st.button("Update API Key"):
        st.info("Update API key in .env file or environment variables")
    
    st.subheader("Supported Languages")
    st.write(", ".join(config.SUPPORTED_LANGUAGES))
    
    st.subheader("Architecture Patterns")
    st.write(", ".join(config.ARCHITECTURE_PATTERNS))


def run_cli():
    """Create command-line interface with menu for all agent operations."""
    print("\n" + "="*60)
    print("🏗️  Architecture Intelligence System - CLI")
    print("="*60 + "\n")
    
    orchestrator = Orchestrator()
    db = Database()
    approval_manager = ApprovalManager(db)
    
    while True:
        print("\nMain Menu:")
        print("1. Architecture Assessment")
        print("2. Tech Stack Recommendations")
        print("3. System Design")
        print("4. Security & Compliance")
        print("5. Comprehensive Review")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == "1":
            project_id = input("Enter project ID (PROJ001/PROJ002): ").strip()
            project_data = get_sample_project_data(project_id)
            if project_data:
                print("\nRunning architecture assessment...")
                result = orchestrator.assess_architecture(project_data)
                print("\n" + result)
            else:
                print("Invalid project ID")
        
        elif choice == "2":
            project_id = input("Enter project ID (PROJ001/PROJ002): ").strip()
            project_data = get_sample_project_data(project_id)
            if project_data:
                requirements = {
                    'project_type': project_data.get('project_type', ''),
                    'scale': project_data.get('scale', ''),
                    'performance_requirements': project_data.get('performance_requirements', ''),
                    'team_expertise': project_data.get('team_expertise', []),
                    'constraints': project_data.get('constraints', {})
                }
                print("\nGenerating tech stack recommendations...")
                result = orchestrator.recommend_tech_stack(requirements)
                print("\n" + result)
            else:
                print("Invalid project ID")
        
        elif choice == "3":
            project_id = input("Enter project ID (PROJ001/PROJ002): ").strip()
            project_data = get_sample_project_data(project_id)
            if project_data:
                design_requirements = {
                    'functional_requirements': project_data.get('functional_requirements', []),
                    'non_functional_requirements': project_data.get('non_functional_requirements', {}),
                    'scale_requirements': project_data.get('scale_requirements', {}),
                    'integration_requirements': project_data.get('integration_requirements', [])
                }
                print("\nGenerating system design...")
                result = orchestrator.design_system_architecture(design_requirements)
                print("\n" + result)
            else:
                print("Invalid project ID")
        
        elif choice == "4":
            project_id = input("Enter project ID (PROJ001/PROJ002): ").strip()
            project_data = get_sample_project_data(project_id)
            if project_data:
                security_requirements = {
                    'current_security_posture': project_data.get('current_security_posture', {}),
                    'compliance_standards': project_data.get('compliance_standards', []),
                    'sensitive_data': project_data.get('sensitive_data', []),
                    'threat_model': project_data.get('threat_model', {})
                }
                print("\nRunning security assessment...")
                result = orchestrator.assess_security_compliance(security_requirements)
                print("\n" + result)
            else:
                print("Invalid project ID")
        
        elif choice == "5":
            project_id = input("Enter project ID (PROJ001/PROJ002): ").strip()
            project_data = get_sample_project_data(project_id)
            if project_data:
                print("\nRunning comprehensive review (this may take a few minutes)...")
                results = orchestrator.comprehensive_architecture_review(project_data)
                print("\n" + "="*60)
                print("COMPREHENSIVE REVIEW RESULTS")
                print("="*60)
                for key, value in results.items():
                    print(f"\n{key.upper().replace('_', ' ')}:")
                    print("-" * 60)
                    print(value[:500] + "..." if len(str(value)) > 500 else value)
            else:
                print("Invalid project ID")
        
        elif choice == "6":
            print("\nExiting...")
            db.close()
            break
        
        else:
            print("Invalid option. Please select 1-6.")


def main():
    """Parse args and launch web or cli mode."""
    parser = argparse.ArgumentParser(description="Architecture Intelligence System")
    parser.add_argument(
        '--mode',
        choices=['web', 'cli'],
        default='web',
        help='Execution mode: web (Streamlit) or cli (command-line)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'web':
        render_streamlit_ui()
    else:
        run_cli()


if __name__ == "__main__":
    # Handle Streamlit execution
    if 'streamlit' in sys.modules:
        render_streamlit_ui()
    else:
        main()
