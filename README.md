# Architecture Intelligence System

AI-powered multi-agent platform for software architecture advisory, technology recommendations, system design guidance, and security assessment.

## Features

- **Architecture Assessment**: Analyze current architecture for technical debt, scalability issues, and design flaws
- **Tech Stack Strategy**: Get optimal technology recommendations based on project requirements
- **System Design**: Generate complete system architecture blueprints
- **Security & Compliance**: Assess security posture and compliance requirements
- **Comprehensive Review**: Multi-agent analysis combining all assessments
- **Human-in-the-Loop**: Approval workflows and feedback mechanisms
- **Dual Interface**: Web UI (Streamlit) and CLI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Agnos
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# Get your API key from: https://makersuite.google.com/app/apikey
```

5. (Optional) Run tests to verify installation:
```bash
python tests.py
```

## Configuration

Update `.env` file with your configuration:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `GEMINI_MODEL`: Model to use (default: gemini-2.0-flash-exp)
- `DB_FILE`: SQLite database file path
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Log file path

## Usage

### Web Interface (Streamlit)

Launch the Streamlit web interface:
```bash
streamlit run main.py
```

Or:
```bash
python main.py --mode web
```

### Command-Line Interface

Run the CLI:
```bash
python main.py --mode cli
```

## Project Structure

```
Project/
├── agents/                    # AI agents
│   ├── orchestrator.py       # Central coordinator
│   ├── architecture_assessment_agent.py
│   ├── tech_stack_strategy_agent.py
│   ├── system_design_agent.py
│   └── security_compliance_agent.py
├── utils/                     # Utilities
│   ├── database.py           # Database operations
│   ├── logger.py             # Logging setup
│   └── validators.py         # Data validation
├── human_intervention/        # HITL workflows
│   ├── approval_manager.py   # Approval management
│   └── feedback_handler.py   # Feedback handling
├── main.py                   # Main application
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Sample Projects

The system includes two sample projects:
- **PROJ001**: E-Commerce Platform
- **PROJ002**: SaaS Analytics Platform

Select these from the project dropdown in the web UI or specify them in the CLI.

## Agent Architecture

The system uses a multi-agent orchestration pattern:
1. **Orchestrator**: Coordinates all agents and manages workflows
2. **Architecture Assessment Agent**: Analyzes architecture quality
3. **Tech Stack Strategy Agent**: Recommends technologies
4. **System Design Agent**: Creates architecture blueprints
5. **Security Compliance Agent**: Assesses security posture

## Web Interface Pages

- **Dashboard**: Project overview and metrics
- **Architecture Assessment**: AI-powered architecture analysis
- **Tech Stack Strategy**: Technology recommendations
- **System Design**: Complete architecture blueprints
- **Security & Compliance**: Security assessments
- **Comprehensive Review**: Multi-agent analysis results
- **Project Management**: Approvals and feedback
- **Settings**: Configuration

## CLI Menu Options

1. Architecture Assessment
2. Tech Stack Recommendations
3. System Design
4. Security & Compliance
5. Comprehensive Review
6. Exit

## Requirements

- Python 3.8+
- Google Gemini API key (get one at https://makersuite.google.com/app/apikey)
- Internet connection (for API calls)

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set API key**: Add your Gemini API key to `.env` file
3. **Launch web UI**: `streamlit run main.py`
4. **Or use CLI**: `python main.py --mode cli`

## Getting Your Gemini API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## License

[Your License Here]

## Support

For issues and questions, please open an issue in the repository.
