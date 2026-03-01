"""
System Configuration
Centralizes API keys, server config, and architecture constants.
"""

import os
from typing import List

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_api_key_here")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

# Database Configuration
DB_FILE = os.getenv("DB_FILE", "architecture.db")

# Application Configuration
APP_VERSION = "1.0.0"
APP_NAME = "Architecture Intelligence System"

# Supported Languages
SUPPORTED_LANGUAGES: List[str] = [
    "Python", "JavaScript", "TypeScript", "Java", "C#", "Go", "Rust",
    "Ruby", "PHP", "Swift", "Kotlin", "Scala", "Dart", "R", "C++", "C"
]

# Architecture Patterns
ARCHITECTURE_PATTERNS: List[str] = [
    "Microservices", "Monolithic", "Serverless", "Event-Driven",
    "Layered Architecture", "Hexagonal Architecture", "CQRS",
    "Event Sourcing", "Service-Oriented Architecture (SOA)",
    "Domain-Driven Design (DDD)", "Clean Architecture"
]

# Cloud Providers
CLOUD_PROVIDERS: List[str] = ["AWS", "Azure", "GCP", "DigitalOcean", "Heroku"]

# Security Standards
SECURITY_STANDARDS: List[str] = [
    "OWASP Top 10", "PCI DSS", "HIPAA", "GDPR", "SOC 2",
    "ISO 27001", "NIST", "CIS Benchmarks"
]

# Default Configuration
DEFAULT_CONFIDENCE_THRESHOLD = 0.7
DEFAULT_MAX_RETRIES = 3
DEFAULT_TIMEOUT_SECONDS = 30

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "architecture_intelligence.log")
