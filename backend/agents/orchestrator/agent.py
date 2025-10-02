"""Orchestrator Agent Implementation.

This module implements the main orchestrator agent that coordinates
the podcast conversation flow between host and guest agents.

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

# Import host agent
try:
    from agents.host_agent.agent import root_agent as host_agent
except ImportError:
    host_agent = None
    print("Warning: Could not import host agent")


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
    description="Orchestrates AI-powered podcast conversations with multiple agents",
    instruction="""You are the orchestrator for an AI-powered podcast system. Your role is to:

1. Welcome users and collect discussion topics
2. Coordinate conversations between host and guest agents
3. Manage the flow of the podcast session
4. Handle user interactions and input
5. Provide smooth transitions and summaries

You have access to a host agent (Alex Rivera) who facilitates the discussion.
When starting a session, use the host agent to provide introductions.
When ending a session, use the host agent to provide closing remarks.

Be helpful, engaging, and professional. Guide users through the podcast experience and ensure smooth conversation flow.

Available tools:
- get_podcast_topic: Get the discussion topic from the user
- call_host_agent: Coordinate with the host agent for introductions, questions, summaries, or closing
- start_podcast_session: Start a new podcast session on a topic
- end_podcast_session: End the current podcast session

When a user provides a topic, use start_podcast_session to begin the episode.""",
    tools=[get_podcast_topic, call_host_agent, start_podcast_session, end_podcast_session]
)
