"""Orchestrator Agent Implementation.

This module implements the main orchestrator agent that coordinates
the podcast conversation flow between host and guest agents using
the persona configuration system.

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

# Import host agent
try:
    from agents.host_agent.agent import root_agent as host_agent
except ImportError:
    host_agent = None
    print("Warning: Could not import host agent")

# Import guest agents
try:
    from agents.guest_maya.agent import root_agent as guest_maya_agent
except ImportError:
    guest_maya_agent = None
    print("Warning: Could not import guest Maya agent")

try:
    from agents.guest_jordan.agent import root_agent as guest_jordan_agent
except ImportError:
    guest_jordan_agent = None
    print("Warning: Could not import guest Jordan agent")


def get_podcast_topic() -> dict:
    """Prompts the user to enter a topic for the podcast discussion.
    
    Returns:
        dict: Contains the topic and status information.
    """
    topic = input("What topic would you like to discuss today? ")
    
    if not topic.strip():
        return {
            "status": "error",
            "error_message": "Please provide a topic for discussion."
        }
    
    return {
        "status": "success",
        "topic": topic.strip()
    }


def get_available_persona_sets() -> dict:
    """Get list of available persona sets.
    
    Returns:
        dict: Contains list of available persona sets and status.
    """
    if persona_manager is None:
        return {
            "status": "error",
            "error_message": "Persona manager is not available"
        }
    
    try:
        persona_sets = persona_manager.list_available_sets()
        return {
            "status": "success",
            "persona_sets": persona_sets,
            "count": len(persona_sets)
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error loading persona sets: {str(e)}"
        }


def get_persona_set_info(set_id: str) -> dict:
    """Get information about a specific persona set.
    
    Args:
        set_id (str): The persona set identifier
        
    Returns:
        dict: Contains persona set information and status.
    """
    if persona_manager is None:
        return {
            "status": "error",
            "error_message": "Persona manager is not available"
        }
    
    try:
        info = persona_manager.get_persona_set_info(set_id)
        return {
            "status": "success",
            "persona_set_info": info
        }
    except ValueError as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def load_persona_set(set_id: str) -> dict:
    """Load a specific persona set configuration.
    
    Args:
        set_id (str): The persona set identifier
        
    Returns:
        dict: Contains persona set configuration and status.
    """
    if persona_manager is None:
        return {
            "status": "error",
            "error_message": "Persona manager is not available"
        }
    
    try:
        persona_set = persona_manager.get_persona_set(set_id)
        return {
            "status": "success",
            "persona_set": persona_set
        }
    except ValueError as e:
        return {
            "status": "error",
            "error_message": str(e)
        }


def call_host_agent(action: str, **kwargs) -> dict:
    """Call the host agent to perform various hosting duties.
    
    Args:
        action (str): The action for the host to perform 
                     ('introduce', 'ask_question', 'summarize', 'close')
        **kwargs: Additional parameters for the specific action.
        
    Returns:
        dict: Response from the host agent.
    """
    if host_agent is None:
        return {
            "status": "error",
            "error_message": "Host agent is not available"
        }
    
    action_map = {
        "introduce": "introduce_podcast",
        "ask_question": "ask_question", 
        "summarize": "summarize_discussion",
        "close": "close_podcast"
    }
    
    if action not in action_map:
        return {
            "status": "error",
            "error_message": f"Unknown action: {action}"
        }
    
    return {
        "status": "success",
        "action": action,
        "message": f"Host agent will {action}",
        "parameters": kwargs
    }


def call_guest_maya(action: str, **kwargs) -> dict:
    """Call Dr. Maya Chen guest agent to provide academic insights.
    
    Args:
        action (str): The action for the guest to perform 
                     ('provide_insight', 'respond_question', 'engage_discussion')
        **kwargs: Additional parameters for the specific action.
        
    Returns:
        dict: Response from the guest agent.
    """
    if guest_maya_agent is None:
        return {
            "status": "error",
            "error_message": "Guest Maya agent is not available"
        }
    
    action_map = {
        "provide_insight": "provide_expert_insight",
        "respond_question": "respond_to_question", 
        "engage_discussion": "engage_in_discussion"
    }
    
    if action not in action_map:
        return {
            "status": "error",
            "error_message": f"Unknown guest action: {action}"
        }
    
    return {
        "status": "success",
        "action": action,
        "message": f"Dr. Maya Chen will {action}",
        "parameters": kwargs
    }


def call_guest_jordan(action: str, **kwargs) -> dict:
    """Call Jordan Blake guest agent to provide practical business insights.
    
    Args:
        action (str): The action for the guest to perform 
                     ('provide_practical_insight', 'share_experience', 'discuss_implementation')
        **kwargs: Additional parameters for the specific action.
        
    Returns:
        dict: Response from the guest agent.
    """
    if guest_jordan_agent is None:
        return {
            "status": "error",
            "error_message": "Guest Jordan agent is not available"
        }
    
    action_map = {
        "provide_practical_insight": "provide_practical_insight",
        "share_experience": "share_experience", 
        "discuss_implementation": "discuss_implementation"
    }
    
    if action not in action_map:
        return {
            "status": "error",
            "error_message": f"Unknown guest action: {action}"
        }
    
    return {
        "status": "success",
        "action": action,
        "message": f"Jordan Blake will {action}",
        "parameters": kwargs
    }


def start_podcast_session(topic: str) -> dict:
    """Starts the podcast session with the given topic.
    
    This coordinates the host agent to provide the introduction.
    
    Args:
        topic (str): The discussion topic.
        
    Returns:
        dict: Contains session information and introduction.
    """
    # Call host agent for introduction
    host_intro = call_host_agent("introduce", topic=topic)
    
    return {
        "status": "success",
        "topic": topic,
        "session_started": True,
        "host_introduction": host_intro,
        "message": f"Podcast session started on topic: {topic}"
    }


def end_podcast_session() -> dict:
    """Ends the podcast session gracefully.
    
    This coordinates the host agent to provide closing remarks.
    
    Returns:
        dict: Contains the closing information and status.
    """
    # Call host agent for closing
    host_closing = call_host_agent("close")
    
    return {
        "status": "success",
        "session_ended": True,
        "host_closing": host_closing,
        "message": "Podcast session ended successfully"
    }


# Create the orchestrator agent
root_agent = Agent(
    name="podcast_orchestrator",
    model="gemini-2.0-flash",
    description="Orchestrates AI-powered podcast conversations with configurable personas",
    instruction="""You are the orchestrator for an AI-powered podcast system with configurable personas. Your role is to:

1. Welcome users and help them select persona sets for their discussion
2. Collect discussion topics and coordinate conversations
3. Manage the flow of podcast sessions with dynamic persona configurations
4. Handle user interactions and input
5. Provide smooth transitions and summaries

You have access to a persona configuration system that allows users to choose from different domain-specific persona sets (technology, sports, business, etc.). Each persona set includes:
- A host persona with specific expertise and speaking style
- Multiple guest personas with distinct perspectives and backgrounds

Available tools:
- get_available_persona_sets: List all available persona sets
- get_persona_set_info: Get detailed information about a specific persona set
- load_persona_set: Load a specific persona set configuration
- get_podcast_topic: Get the discussion topic from the user
- call_host_agent: Coordinate with the host agent for introductions, questions, summaries, or closing
- call_guest_maya: Coordinate with Dr. Maya Chen for academic insights, responses, and discussion engagement
- call_guest_jordan: Coordinate with Jordan Blake for practical business insights, experience sharing, and implementation discussion
- start_podcast_session: Start a new podcast session on a topic
- end_podcast_session: End the current podcast session

When users start a session:
1. Help them explore available persona sets if they haven't chosen one
2. Load the selected persona set configuration
3. Get their discussion topic
4. Start the podcast session with the configured personas

Be helpful, engaging, and professional. Guide users through the persona selection process and ensure smooth conversation flow between all participants.""",
    tools=[
        get_available_persona_sets, 
        get_persona_set_info, 
        load_persona_set,
        get_podcast_topic, 
        call_host_agent, 
        call_guest_maya,
        call_guest_jordan, 
        start_podcast_session, 
        end_podcast_session
    ]
)
