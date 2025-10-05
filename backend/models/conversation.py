"""Conversation state and message models.

This module defines the data structures for managing podcast conversation state,
including message history, turn tracking, and session status.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum


class ConversationStatus(Enum):
    """Status of the podcast conversation."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ENDING = "ending"
    COMPLETED = "completed"


class Speaker(Enum):
    """Speaker types in the conversation."""
    HOST = "host"
    GUEST_1 = "guest_1"
    GUEST_2 = "guest_2"
    USER = "user"
    SYSTEM = "system"


@dataclass
class Message:
    """A single message in the conversation.
    
    Attributes:
        speaker: Who is speaking (host, guest, user)
        persona_name: Display name of the speaker
        content: The message content
        timestamp: When the message was created
        turn_number: The turn number in the conversation
        speaker_id: Unique identifier for the speaker
    """
    speaker: Speaker
    persona_name: str
    content: str
    turn_number: int
    speaker_id: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self):
        """String representation of the message."""
        return f"[Turn {self.turn_number}] {self.persona_name}: {self.content}"


@dataclass
class ConversationState:
    """State of the podcast conversation.
    
    Attributes:
        topic: The discussion topic
        persona_set_id: ID of the active persona set
        status: Current conversation status
        current_turn: Current turn number
        history: List of all messages in the conversation
        persona_set: The active persona set configuration
        host_name: Name of the host persona
        guest_names: Names of guest personas
        user_has_participated: Whether user has joined the conversation
        exchanges_since_user_prompt: Counter for automatic user prompts
    """
    topic: str
    persona_set_id: str
    persona_set: Dict
    host_name: str
    guest_names: List[str]
    status: ConversationStatus = ConversationStatus.INITIALIZING
    current_turn: int = 0
    history: List[Message] = field(default_factory=list)
    user_has_participated: bool = False
    exchanges_since_user_prompt: int = 0
    max_exchanges_before_prompt: int = 3  # Prompt user every 3 exchanges
    
    def add_message(self, speaker: Speaker, persona_name: str, content: str, speaker_id: str = "") -> Message:
        """Add a message to the conversation history.
        
        Args:
            speaker: The speaker type
            persona_name: Display name of the speaker
            content: Message content
            speaker_id: Unique identifier for the speaker
            
        Returns:
            The created Message object
        """
        self.current_turn += 1
        message = Message(
            speaker=speaker,
            persona_name=persona_name,
            content=content,
            turn_number=self.current_turn,
            speaker_id=speaker_id
        )
        self.history.append(message)
        return message
    
    def get_recent_history(self, count: int = 10) -> List[Message]:
        """Get the most recent messages for context.
        
        Args:
            count: Number of recent messages to retrieve
            
        Returns:
            List of recent messages
        """
        return self.history[-count:] if len(self.history) > count else self.history
    
    def get_context_summary(self) -> str:
        """Generate a summary of recent conversation for agent context.
        
        Returns:
            String summary of recent conversation
        """
        recent = self.get_recent_history(5)
        if not recent:
            return f"Starting conversation on topic: {self.topic}"
        
        context_parts = [f"Topic: {self.topic}", "Recent discussion:"]
        for msg in recent:
            context_parts.append(f"- {msg.persona_name}: {msg.content[:100]}...")
        
        return "\n".join(context_parts)
    
    def should_prompt_user(self) -> bool:
        """Determine if it's time to prompt the user for input.
        
        Returns:
            True if user should be prompted
        """
        # Don't prompt during initialization or ending
        if self.status != ConversationStatus.ACTIVE:
            return False
        
        # Prompt after configured number of exchanges
        return self.exchanges_since_user_prompt >= self.max_exchanges_before_prompt
    
    def reset_user_prompt_counter(self):
        """Reset the counter after prompting user."""
        self.exchanges_since_user_prompt = 0
    
    def increment_exchange_counter(self):
        """Increment the exchange counter."""
        self.exchanges_since_user_prompt += 1
    
    def is_active(self) -> bool:
        """Check if conversation is active.
        
        Returns:
            True if conversation is active
        """
        return self.status == ConversationStatus.ACTIVE
    
    def is_ended(self) -> bool:
        """Check if conversation has ended.
        
        Returns:
            True if conversation has ended
        """
        return self.status in [ConversationStatus.ENDING, ConversationStatus.COMPLETED]

