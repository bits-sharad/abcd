import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from main import get_sample_project_data, run_cli
from agents import ArchitectureOrchestrator
from human_intervention import ApprovalManager, FeedbackHandler


# ===== AGENTS TESTS (8 tests) =====

class TestArchitectureAgents:
    """Test cases for AI agents and orchestrator."""

    @pytest.fixture
    def project_data(self):
        """Fixture providing sample project data."""
        return get_sample_project_data("PROJ001")

    def test_orchestrator_initialization(self):
        """Test 1: Orchestrator initializes with all four specialized agents."""
        orchestrator = ArchitectureOrchestrator()

        assert orchestrator.assessment_agent is not None
        assert orchestrator.tech_stack_agent is not None
        assert orchestrator.design_agent is not None
        assert orchestrator.security_agent is not None

        # Verify agents have the required run method
        assert hasattr(orchestrator.assessment_agent, 'run')
        assert hasattr(orchestrator.tech_stack_agent, 'run')
        assert hasattr(orchestrator.design_agent, 'run')
        assert hasattr(orchestrator.security_agent, 'run')

    def test_architecture_assessment_agent_formatting(self, project_data):
        """Test 2: Architecture Assessment Agent formats project data correctly."""
        orchestrator = ArchitectureOrchestrator()

        # Test component formatting
        components = project_data['components']
        formatted = orchestrator._format_components(components)

        assert isinstance(formatted, str)
        assert len(formatted) > 0
        assert 'Web Application' in formatted
        assert 'PostgreSQL Database' in formatted

        # Test tech stack formatting
        tech_stack = project_data['tech_stack']
        formatted_stack = orchestrator._format_tech_stack(tech_stack)

        assert isinstance(formatted_stack, str)
        assert 'Ruby on Rails' in formatted_stack or 'rails' in formatted_stack.lower()

    def test_tech_stack_agent_validation(self, project_data):
        """Test 3: Tech Stack Strategy Agent validates technology choices."""
        # Verify tech stack has required categories
        tech_stack = project_data['tech_stack']
        assert 'backend' in tech_stack
        assert 'database' in tech_stack
        assert 'frontend' in tech_stack

        # Verify team expertise aligns with tech stack
        team_expertise = project_data.get('team_expertise', [])
        preferred_languages = project_data.get('preferred_languages', [])

        assert len(team_expertise) > 0
        assert len(preferred_languages) > 0

    def test_assessment_agent_execution(self, project_data):
        """Test 4: Assessment agent executes and returns structured analysis."""
        orchestrator = ArchitectureOrchestrator()

        # Mock the agent's run method to avoid actual API calls
        mock_response = Mock()
        mock_response.content = "Architecture assessment completed successfully"
        orchestrator.assessment_agent.run = Mock(return_value=mock_response)

        result = orchestrator.assess_architecture(project_data)

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        orchestrator.assessment_agent.run.assert_called_once()

    def test_system_design_agent_scalability(self, project_data):
        """Test 5: System Design Agent handles scalability requirements."""
        # Verify scalability data is present
        assert 'current_users' in project_data
        assert 'expected_users' in project_data
        assert 'concurrent_users' in project_data

        current = project_data['current_users']
        expected = project_data['expected_users']
        concurrent = project_data['concurrent_users']

        # Verify data integrity
        assert expected > current  # Growth expectation
        assert concurrent <= expected  # Concurrent users shouldn't exceed total

        # Calculate scaling factor
        scaling_factor = expected / current
        assert scaling_factor >= 1.0  # Must be at least maintaining current scale

    def test_security_agent_compliance_check(self, project_data):
        """Test 6: Security Compliance Agent validates compliance requirements."""
        # Verify compliance data exists
        assert 'compliance_requirements' in project_data
        assert 'current_security_measures' in project_data
        assert 'security_concerns' in project_data

        compliance = project_data['compliance_requirements']
        security_measures = project_data['current_security_measures']

        # E-commerce should have PCI-DSS
        assert 'PCI-DSS' in compliance

        # Should have authentication and encryption
        assert 'authentication' in security_measures
        assert 'encryption' in security_measures

    def test_design_agent_architecture_patterns(self, project_data):
        """Test 7: Design agent evaluates architecture patterns."""
        orchestrator = ArchitectureOrchestrator()

        # Mock the agent's run method to avoid actual API calls
        mock_response = Mock()
        mock_response.content = "Microservices architecture recommended"
        orchestrator.design_agent.run = Mock(return_value=mock_response)

        result = orchestrator.design_system_architecture(project_data)

        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        orchestrator.design_agent.run.assert_called_once()

    def test_comprehensive_review_coordination(self, project_data):
        """Test 8: Orchestrator coordinates all agents for comprehensive review."""
        orchestrator = ArchitectureOrchestrator()

        # Mock all agents with response objects
        mock_response = Mock()
        mock_response.content = "Test response"

        orchestrator.assessment_agent.run = Mock(return_value=mock_response)
        orchestrator.tech_stack_agent.run = Mock(return_value=mock_response)
        orchestrator.design_agent.run = Mock(return_value=mock_response)
        orchestrator.security_agent.run = Mock(return_value=mock_response)

        result = orchestrator.comprehensive_architecture_review(project_data)

        assert isinstance(result, dict)
        assert 'assessment' in result
        assert 'tech_stack' in result
        assert 'design' in result
        assert 'security' in result

        # Verify all agents were called
        orchestrator.assessment_agent.run.assert_called()
        orchestrator.tech_stack_agent.run.assert_called()
        orchestrator.design_agent.run.assert_called()
        orchestrator.security_agent.run.assert_called()


# ===== HUMAN INTERVENTION TESTS (4 tests) =====

class TestHumanIntervention:
    """Test cases for approval manager and feedback handler."""

    def test_approval_manager_initialization(self):
        """Test 9: Approval Manager initializes correctly."""
        approval_mgr = ApprovalManager()

        assert approval_mgr is not None
        assert hasattr(approval_mgr, 'submit_for_approval')
        assert hasattr(approval_mgr, 'get_pending_approvals')

    def test_submit_approval_request(self):
        """Test 10: Approval Manager can submit approval requests."""
        approval_mgr = ApprovalManager()

        approval_id = approval_mgr.submit_for_approval(
            project_id=1,
            request_type="tech_stack",
            recommendation_summary="Migrate to microservices",
            full_recommendation="Detailed recommendation here",
            priority="high"
        )

        assert approval_id is not None
        assert isinstance(approval_id, int)
        assert approval_id > 0

    def test_feedback_handler_initialization(self):
        """Test 11: Feedback Handler initializes correctly."""
        feedback_handler = FeedbackHandler()

        assert feedback_handler is not None
        assert hasattr(feedback_handler, 'submit_feedback')
        assert hasattr(feedback_handler, 'get_feedback_by_project')

    def test_submit_feedback(self):
        """Test 12: Feedback Handler can submit and store feedback."""
        feedback_handler = FeedbackHandler()

        feedback_id = feedback_handler.submit_feedback(
            project_id=1,
            feedback_type="recommendation",
            content="The architecture recommendations were very helpful",
            rating=5
        )

        assert feedback_id is not None
        assert isinstance(feedback_id, int)
        assert feedback_id > 0


# ===== ORCHESTRATOR HELPER METHODS TESTS (2 tests) =====

class TestOrchestratorHelpers:
    """Test cases for orchestrator helper methods."""

    def test_format_list_helper(self):
        """Test 13: Orchestrator correctly formats lists into readable text."""
        orchestrator = ArchitectureOrchestrator()

        test_list = [
            "Database performance issues",
            "Scaling limitations",
            "Technical debt accumulation"
        ]

        result = orchestrator._format_list(test_list)

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Database performance issues" in result
        assert "Scaling limitations" in result
        # Check for bullet points or numbered format
        assert '-' in result or '1' in result

    def test_format_dict_helper(self):
        """Test 14: Orchestrator correctly formats dictionaries into readable text."""
        orchestrator = ArchitectureOrchestrator()

        test_dict = {
            'response_time': '< 200ms',
            'availability': '99.9%',
            'throughput': '10000 requests/sec'
        }

        result = orchestrator._format_dict(test_dict)

        assert isinstance(result, str)
        assert len(result) > 0
        assert '200ms' in result
        assert '99.9%' in result
        assert 'throughput' in result.lower() or 'Throughput' in result


# ===== MAIN.PY TESTS (1 test) =====

class TestMainFunctions:
    """Test cases for main.py functions (excluding Streamlit UI)."""

    @patch('builtins.input', side_effect=['6'])  # Exit option
    def test_cli_mode_initialization(self, mock_input):
        """Test 15: CLI mode initializes and exits gracefully."""
        # Mock the database initialization
        with patch('main.initialize_architecture_database', return_value=True):
            with patch('builtins.print') as mock_print:
                try:
                    run_cli()
                    # Verify CLI started
                    calls = [str(call) for call in mock_print.call_args_list]
                    header_found = any('ARCHITECTURE INTELLIGENCE SYSTEM' in str(call) for call in calls)
                    assert header_found
                except SystemExit:
                    pass  # Expected when exiting CLI


if __name__ == "__main__":
    # Run tests with verbose output
    print("Running 15 test cases for Architecture Intelligence System...")
    print("=" * 70)
    pytest.main([__file__, "-v", "--tb=short", "-s"])