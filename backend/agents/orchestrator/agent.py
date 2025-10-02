import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

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

def start_podcast_introduction(topic: str) -> dict:
    """Starts the podcast with an introduction to the topic.
    
    Args:
        topic (str): The discussion topic.
        
    Returns:
        dict: Contains the introduction and status.
    """
    return {
        "status": "success",
        "introduction": f"Welcome to AI-Podcast! Today we're discussing: {topic}. Let's begin our conversation!"
    }

def end_podcast() -> dict:
    """Ends the podcast session gracefully.
    
    Returns:
        dict: Contains the closing message and status.
    """
    return {
        "status": "success",
        "closing": "Thank you for joining us today! That wraps up this episode of AI-Podcast."
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

Be helpful, engaging, and professional. Guide users through the podcast experience and ensure smooth conversation flow.

When a user provides a topic, acknowledge it and begin the podcast introduction.""",
    tools=[get_podcast_topic, start_podcast_introduction, end_podcast]
)
