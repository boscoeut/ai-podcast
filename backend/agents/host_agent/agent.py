"""Host Agent Implementation.

This module implements the podcast host agent using Google ADK.
The host facilitates discussions, asks questions, and maintains engagement.

Following Google ADK structure: https://google.github.io/adk-docs/get-started/quickstart/
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()


def introduce_podcast(topic: str, guest_names: list = None) -> dict:
    """Introduce the podcast episode and the topic.
    
    Args:
        topic (str): The discussion topic for this episode.
        guest_names (list, optional): Names of guest participants.
        
    Returns:
        dict: Contains introduction message and status.
    """
    if guest_names is None:
        guest_names = ["Dr. Maya Chen", "Jordan Blake"]
    
    guests_str = " and ".join(guest_names)
    
    return {
        "status": "success",
        "introduction": f"Welcome to AI-Podcast! I'm your host, Alex Rivera. Today we're diving into an exciting topic: {topic}. I'm joined by {guests_str}. Let's explore this together!"
    }


def ask_question(context: str) -> dict:
    """Generate a thoughtful question based on the conversation context.
    
    Args:
        context (str): Current conversation context or previous points.
        
    Returns:
        dict: Contains the question and status.
    """
    return {
        "status": "success",
        "message": "Question generated based on context",
        "context": context
    }


def summarize_discussion(key_points: list) -> dict:
    """Summarize key points from the discussion.
    
    Args:
        key_points (list): List of key discussion points to summarize.
        
    Returns:
        dict: Contains summary and status.
    """
    return {
        "status": "success",
        "summary": f"Great discussion! We've covered {len(key_points)} key points today.",
        "key_points": key_points
    }


def close_podcast() -> dict:
    """Provide closing remarks for the podcast episode.
    
    Returns:
        dict: Contains closing message and status.
    """
    return {
        "status": "success",
        "closing": "Thank you all for joining this fascinating discussion! To our listeners, we hope you found this conversation insightful. Until next time, keep exploring and stay curious!"
    }


# Create the host agent with Alex Rivera persona
root_agent = Agent(
    name="alex_rivera",
    model="gemini-2.0-flash",
    description="Alex Rivera - Tech Journalist & Podcast Host",
    instruction="""You are Alex Rivera, an enthusiastic tech podcast host with a journalism background.
    
Your role is to:
- Welcome listeners and introduce topics warmly
- Ask probing questions that reveal insights
- Ensure all guests contribute meaningfully
- Create smooth transitions between topics
- Summarize key points periodically
- Keep conversation accessible yet substantive
- Acknowledge user input and questions

Your style:
- Warm, curious, and articulate
- Use phrases like "That's fascinating...", "Let's dig deeper...", "Building on that..."
- Make guests and listeners feel welcome
- Bridge between technical and accessible language
- Keep responses conversational and concise (2-4 sentences typically)

Example phrases you might use:
- "That's a fascinating perspective..."
- "Let's dig deeper into that..."
- "I love how you framed that..."
- "To our listeners wondering about..."
- "Building on that point..."
- "Let's explore that further..."

Be engaging, maintain energy, and guide the conversation to be informative and entertaining.""",
    tools=[introduce_podcast, ask_question, summarize_discussion, close_podcast]
)

