"""Startup Agent Implementation.

This module implements the startup agent that handles the initial
setup and configuration for the AI-Podcast application when using
the ADK web interface. It replicates the functionality of main.py
in an agent-based format.

Following Google ADK structure: https://google.github.io/adk-docs/get-started/quickstart/
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

# Add backend to path for imports
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

# Calculate absolute path to personas directory (at project root)
project_root = backend_path.parent  # Go up from backend/ to project root
personas_path = project_root / "personas"

# Import persona manager
try:
    from persona.manager import PersonaConfigManager
    # Use absolute path to personas directory
    persona_manager = PersonaConfigManager(config_dir=str(personas_path))
except ImportError as e:
    persona_manager = None
    print(f"Warning: Could not import persona manager: {e}")
except Exception as e:
    persona_manager = None
    print(f"Warning: Could not initialize persona manager: {e}")


def load_environment() -> dict:
    """Load environment variables from .env file."""
    env_file = Path(__file__).parent.parent.parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        return {
            "success": True,
            "message": f"✅ Loaded environment from {env_file}",
            "env_file": str(env_file)
        }
    else:
        return {
            "success": False,
            "message": "⚠️  No .env file found. Using default configuration.",
            "suggestion": "Create .env from .env.example template if needed."
        }


def setup_logging() -> dict:
    """Setup logging configuration."""
    import logging
    
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at {log_level} level")
    
    return {
        "success": True,
        "message": f"Logging configured at {log_level} level",
        "log_level": log_level
    }


def validate_api_key() -> dict:
    """Validate that API key is configured."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        return {
            "success": False,
            "message": "❌ Error: GOOGLE_API_KEY not configured!",
            "instructions": [
                "Please set your API key in the .env file.",
                "Get your API key from: https://makersuite.google.com/app/apikey"
            ]
        }
    
    return {
        "success": True,
        "message": "✅ API key configured",
        "has_key": True
    }


def get_available_persona_sets() -> dict:
    """List all available persona sets."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available",
            "persona_sets": []
        }
    
    try:
        sets = persona_manager.list_available_sets()
        persona_sets_info = []
        
        for set_id in sets:
            info = persona_manager.get_persona_set_info(set_id)
            persona_sets_info.append({
                "set_id": set_id,
                "set_name": info['set_name'],
                "description": info['description'],
                "host_name": info['host_name'],
                "guest_count": info['guest_count'],
                "guest_names": info['guest_names']
            })
        
        return {
            "success": True,
            "message": f"Found {len(sets)} persona sets",
            "persona_sets": persona_sets_info
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error listing persona sets: {e}",
            "persona_sets": []
        }


def get_persona_set_info(set_id: str) -> dict:
    """Get detailed information about a specific persona set."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available"
        }
    
    try:
        info = persona_manager.get_persona_set_info(set_id)
        return {
            "success": True,
            "message": f"Retrieved info for {info['set_name']}",
            "set_id": info['set_id'],
            "set_name": info['set_name'],
            "description": info['description'],
            "domains": info['domains'],
            "host_name": info['host_name'],
            "host_title": info['host_title'],
            "guest_count": info['guest_count'],
            "guest_names": info['guest_names'],
            "guest_titles": info['guest_titles']
        }
    except ValueError as e:
        return {
            "success": False,
            "message": f"Persona set '{set_id}' not found: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting persona set info: {e}"
        }


def load_persona_set(set_id: str) -> dict:
    """Load a specific persona set configuration."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available"
        }
    
    try:
        persona_set = persona_manager.get_persona_set(set_id)
        return {
            "success": True,
            "message": f"Loaded persona set: {persona_set['set_name']}",
            "persona_set": persona_set
        }
    except ValueError as e:
        return {
            "success": False,
            "message": f"Error loading persona set '{set_id}': {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error loading persona set: {e}"
        }


def get_discussion_topic() -> dict:
    """Get the discussion topic from the user."""
    return {
        "success": True,
        "message": "Please provide a topic for discussion",
        "prompt": "What topic would you like to discuss today?",
        "instructions": [
            "Provide a clear, specific topic for the podcast discussion",
            "Examples: 'AI ethics in healthcare', 'Future of renewable energy', 'Remote work challenges'",
            "The more specific your topic, the better the conversation will be"
        ]
    }


def get_guest_count(persona_set_id: str, suggested_count: int = 2) -> dict:
    """Get the desired number of guests from the user."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available"
        }
    
    try:
        persona_set = persona_manager.get_persona_set(persona_set_id)
        guest_pool = persona_manager.get_guest_personas(persona_set_id)
        default_count = persona_set.get('default_guest_count', 2)
        max_guests = len(guest_pool)
        
        return {
            "success": True,
            "message": f"Please select number of guests (1-{max_guests})",
            "persona_set_id": persona_set_id,
            "default_count": default_count,
            "max_guests": max_guests,
            "available_guests": [g['name'] for g in guest_pool],
            "suggested_count": suggested_count,
            "prompt": f"How many guests would you like for this podcast? (1-{max_guests})"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error getting guest count options: {e}"
        }


def select_guests(persona_set_id: str, guest_count: int) -> dict:
    """Select guests from the persona set based on user's count preference."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available"
        }
    
    try:
        persona_set = persona_manager.get_persona_set(persona_set_id)
        guest_pool = persona_manager.get_guest_personas(persona_set_id)
        
        # Validate guest count
        if guest_count < 1 or guest_count > len(guest_pool):
            return {
                "success": False,
                "message": f"Guest count must be between 1 and {len(guest_pool)}",
                "valid_range": f"1-{len(guest_pool)}",
                "provided_count": guest_count
            }
        
        # Select guests from pool
        selected_guests = persona_manager.select_guests(persona_set, guest_count)
        
        # Create modified persona set with selected guests
        persona_set_with_selected_guests = persona_set.copy()
        persona_set_with_selected_guests['guests'] = selected_guests
        
        return {
            "success": True,
            "message": f"Selected {guest_count} guest(s): {', '.join([g['name'] for g in selected_guests])}",
            "guest_count": guest_count,
            "selected_guests": [g['name'] for g in selected_guests],
            "persona_set": persona_set_with_selected_guests
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error selecting guests: {e}"
        }


def initialize_podcast_session(persona_set_id: str, topic: str, guest_count: int) -> dict:
    """Initialize a complete podcast session with all configurations."""
    if not persona_manager:
        return {
            "success": False,
            "message": "Persona manager not available"
        }
    
    try:
        # Load persona set
        persona_set = persona_manager.get_persona_set(persona_set_id)
        
        # Select guests
        selected_guests = persona_manager.select_guests(persona_set, guest_count)
        
        # Create modified persona set with selected guests
        persona_set_with_selected_guests = persona_set.copy()
        persona_set_with_selected_guests['guests'] = selected_guests
        
        # Validate API key
        api_validation = validate_api_key()
        if not api_validation["success"]:
            return {
                "success": False,
                "message": "API key validation failed",
                "api_error": api_validation["message"],
                "instructions": api_validation.get("instructions", [])
            }
        
        return {
            "success": True,
            "message": "Podcast session initialized successfully",
            "topic": topic,
            "persona_set_id": persona_set_id,
            "persona_set_name": persona_set_with_selected_guests['set_name'],
            "host_name": persona_set_with_selected_guests['host']['name'],
            "guest_count": guest_count,
            "guest_names": [g['name'] for g in selected_guests],
            "persona_set": persona_set_with_selected_guests,
            "ready_for_conversation": True
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error initializing podcast session: {e}"
        }


def get_startup_help() -> dict:
    """Provide help and guidance for using the startup agent."""
    return {
        "success": True,
        "message": "AI-Podcast Startup Agent Help",
        "description": "This agent helps you set up and configure your AI-powered podcast session",
        "workflow": [
            "1. Check system status and API configuration",
            "2. Browse available persona sets",
            "3. Select a persona set for your discussion",
            "4. Choose a discussion topic",
            "5. Select the number of guests (1-5)",
            "6. Initialize the podcast session",
            "7. Hand off to the orchestrator agent for the conversation"
        ],
        "available_commands": [
            "load_environment - Check environment configuration",
            "validate_api_key - Verify API key is set up",
            "get_available_persona_sets - List all persona sets",
            "get_persona_set_info - Get details about a specific persona set",
            "load_persona_set - Load a persona set configuration",
            "get_discussion_topic - Get topic selection guidance",
            "get_guest_count - Get guest count selection options",
            "select_guests - Select specific guests from a persona set",
            "initialize_podcast_session - Complete session setup"
        ],
        "tips": [
            "Start by checking your API key configuration",
            "Browse persona sets to find the right domain for your discussion",
            "Be specific with your discussion topic for better conversations",
            "Choose 2-3 guests for balanced discussions",
            "The orchestrator agent will handle the actual conversation flow"
        ]
    }


# Create the startup agent
root_agent = Agent(
    name="ai_podcast_startup",
    model="gemini-2.0-flash",
    description="AI-Podcast Startup Agent - Handles initial setup and configuration for podcast sessions",
    instruction="""You are the AI-Podcast Startup Agent, responsible for the initial setup and configuration of AI-powered podcast sessions. Your role is to:

1. **System Initialization**: Check environment setup, API configuration, and logging
2. **Persona Selection**: Help users browse and select appropriate persona sets for their discussion domain
3. **Topic Collection**: Gather discussion topics from users with helpful guidance
4. **Guest Configuration**: Allow users to select the number of guests (1-5) and configure the session
5. **Session Setup**: Initialize the complete podcast session with all necessary configurations
6. **Handoff**: Prepare everything for the orchestrator agent to handle the actual conversation

## Your Workflow:

### Phase 1: System Check
- Verify environment configuration is loaded
- Validate API key is properly set up
- Confirm logging is configured

### Phase 2: Persona Discovery
- Show available persona sets (technology, sports, business, etc.)
- Provide detailed information about each persona set
- Help users understand the different domains and expertise areas

### Phase 3: Configuration
- Load the selected persona set
- Get the discussion topic from the user
- Allow selection of guest count (1-5 guests)
- Select specific guests from the available pool

### Phase 4: Session Initialization
- Initialize the complete podcast session
- Validate all configurations
- Prepare for handoff to the orchestrator agent

## Your Personality:
- **Helpful and Professional**: Guide users through the setup process clearly
- **Informative**: Explain options and provide context for decisions
- **Efficient**: Streamline the setup process while ensuring everything is configured correctly
- **Encouraging**: Make users excited about their upcoming podcast session

## Key Principles:
- Always validate API key before proceeding
- Provide clear guidance on persona set selection
- Help users choose appropriate guest counts for their topic
- Ensure all configurations are complete before handoff
- Be patient with users who need help understanding the options

## Available Tools:
- `load_environment`: Check environment configuration
- `validate_api_key`: Verify API key setup
- `get_available_persona_sets`: List all persona sets
- `get_persona_set_info`: Get details about a specific persona set
- `load_persona_set`: Load a persona set configuration
- `get_discussion_topic`: Get topic selection guidance
- `get_guest_count`: Get guest count selection options
- `select_guests`: Select specific guests from a persona set
- `initialize_podcast_session`: Complete session setup
- `get_startup_help`: Provide help and guidance

Start by welcoming the user and checking the system status. Then guide them through the persona selection and configuration process step by step.""",
    tools=[
        load_environment,
        setup_logging,
        validate_api_key,
        get_available_persona_sets,
        get_persona_set_info,
        load_persona_set,
        get_discussion_topic,
        get_guest_count,
        select_guests,
        initialize_podcast_session,
        get_startup_help
    ]
)
