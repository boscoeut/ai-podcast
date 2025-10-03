"""Guest Maya Agent Implementation.

This module implements Dr. Maya Chen, an academic AI researcher guest agent
using Google ADK. The guest provides research-based insights and analytical
perspectives on technology topics.

Following Google ADK structure: https://google.github.io/adk-docs/get-started/quickstart/
"""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent

# Load environment variables
load_dotenv()


def provide_expert_insight(topic: str, context: str = None) -> dict:
    """Provide research-based expert insight on a topic.
    
    Args:
        topic (str): The topic or question being discussed.
        context (str, optional): Additional context from the conversation.
        
    Returns:
        dict: Contains expert insight and status.
    """
    insight_context = f" on {context}" if context else ""
    
    return {
        "status": "success",
        "insight": f"Research-based perspective on {topic}{insight_context}",
        "topic": topic,
        "context": context
    }


def respond_to_question(question: str, conversation_context: str = None) -> dict:
    """Respond to a question with academic rigor and research backing.
    
    Args:
        question (str): The question being asked.
        conversation_context (str, optional): Context from ongoing conversation.
        
    Returns:
        dict: Contains response and status.
    """
    context_note = f" (considering: {conversation_context})" if conversation_context else ""
    
    return {
        "status": "success",
        "response": f"Academic response to: {question}{context_note}",
        "question": question,
        "context": conversation_context
    }


def engage_in_discussion(point: str, discussion_context: str = None) -> dict:
    """Engage with a discussion point by building on others' ideas academically.
    
    Args:
        point (str): The discussion point or idea to engage with.
        discussion_context (str, optional): Context from the ongoing discussion.
        
    Returns:
        dict: Contains engagement response and status.
    """
    engagement_context = f" (building on: {discussion_context})" if discussion_context else ""
    
    return {
        "status": "success",
        "engagement": f"Academic engagement with: {point}{engagement_context}",
        "point": point,
        "context": discussion_context
    }


# Create the guest agent with Dr. Maya Chen persona
root_agent = Agent(
    name="maya_chen",
    model="gemini-2.0-flash",
    description="Dr. Maya Chen - AI Researcher & Academic",
    instruction="""You are Dr. Maya Chen, an academic AI researcher with expertise in ethics and social impacts.

Your background:
- PhD in Computer Science and Social Sciences
- University researcher specializing in AI ethics and social impacts of technology
- Expert in machine learning research and technology adoption studies

Your perspective is:
- Analytical and evidence-based
- Grounded in research and data
- Theoretical and frameworks-oriented
- Nuanced and precise

Your speaking style:
- Reference studies when relevant: "Research from MIT shows...", "Studies indicate..."
- Think in frameworks and models
- Ask clarifying questions
- Value precision: "Based on the data...", "The research is clear that..."
- Consider multiple variables and complexity
- Use qualifiers like "From a theoretical standpoint...", "The evidence suggests..."

Example phrases you might use:
- "Studies from MIT have shown..."
- "From a theoretical standpoint..."
- "The research is quite clear that..."
- "We need to consider multiple variables..."
- "Based on current research..."
- "The data indicates that..."

Your role in the podcast:
- Provide research-based insights and analysis
- Share theoretical perspectives on technology topics
- Ask thoughtful clarifying questions
- Build on others' ideas with academic rigor
- Maintain evidence-based discourse

Keep responses substantive but conversational (2-5 sentences typically).
Be thoughtful, precise, and academically rigorous while remaining accessible.""",
    tools=[provide_expert_insight, respond_to_question, engage_in_discussion]
)
