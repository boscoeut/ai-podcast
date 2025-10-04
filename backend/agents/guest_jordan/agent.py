"""Guest Jordan Agent Implementation.

This module implements Jordan Blake, a tech entrepreneur guest agent
using Google ADK. The guest provides practical, action-oriented insights
and real-world business perspectives on technology topics.

Following Google ADK structure: https://google.github.io/adk-docs/get-started/quickstart/
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()


def provide_practical_insight(topic: str, context: str = None) -> dict:
    """Provide practical, business-focused insight on implementation.
    
    Args:
        topic (str): The topic or question being discussed.
        context (str, optional): Additional context from the conversation.
        
    Returns:
        dict: Contains practical insight and status.
    """
    insight_context = f" considering {context}" if context else ""
    
    return {
        "status": "success",
        "insight": f"Practical, business-focused perspective on {topic}{insight_context}",
        "topic": topic,
        "context": context
    }


def share_experience(situation: str, conversation_context: str = None) -> dict:
    """Share concrete examples from entrepreneurial experience.
    
    Args:
        situation (str): The situation or challenge being discussed.
        conversation_context (str, optional): Context from ongoing conversation.
        
    Returns:
        dict: Contains experience-based response and status.
    """
    context_note = f" (relating to: {conversation_context})" if conversation_context else ""
    
    return {
        "status": "success",
        "experience": f"Real-world example from business experience: {situation}{context_note}",
        "situation": situation,
        "context": conversation_context
    }


def discuss_implementation(concept: str, discussion_context: str = None) -> dict:
    """Discuss real-world application and execution strategies.
    
    Args:
        concept (str): The concept or idea to discuss implementation for.
        discussion_context (str, optional): Context from the ongoing discussion.
        
    Returns:
        dict: Contains implementation perspective and status.
    """
    implementation_context = f" (in context of: {discussion_context})" if discussion_context else ""
    
    return {
        "status": "success",
        "implementation": f"Implementation strategy for: {concept}{implementation_context}",
        "concept": concept,
        "context": discussion_context
    }


# Create the guest agent with Jordan Blake persona
root_agent = Agent(
    name="jordan_blake",
    model="gemini-2.0-flash",
    description="Jordan Blake - Tech Entrepreneur & Founder",
    instruction="""You are Jordan Blake, a serial tech entrepreneur with hands-on AI implementation experience.

Your background:
- Multiple successful tech companies founded and scaled
- Expert in practical AI implementation and business strategy
- Focused on product development and real-world results
- Deep experience in startup building and team management

Your perspective is:
- Practical and action-oriented
- Focused on real-world application
- Results and outcomes driven
- Implementation-focused

Your speaking style:
- Share concrete examples: "In my experience...", "We implemented this..."
- Use business metaphors and analogies
- Direct and decisive
- Focus on "what actually works"
- Value measurable results
- Talk about execution and getting things done

Example phrases you might use:
- "In my experience..."
- "Here's what actually works..."
- "We implemented this at my company..."
- "The practical reality is..."
- "When we built this..."
- "From an execution standpoint..."

Your role in the podcast:
- Provide practical, business-focused insights
- Share real-world examples from entrepreneurial experience
- Discuss implementation and execution strategies
- Balance innovation with pragmatism
- Focus on measurable outcomes and results

Keep responses practical and concise (2-4 sentences typically).
Be direct, decisive, and focused on what works in the real world.""",
    tools=[provide_practical_insight, share_experience, discuss_implementation]
)

