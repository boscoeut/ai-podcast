"""CLI output formatting utilities.

This module provides formatting utilities for displaying podcast conversations
in a readable and engaging format in the terminal.
"""

from typing import Dict
from models.conversation import Message, Speaker


class ConversationFormatter:
    """Formats conversation output for CLI display."""
    
    # Speaker icons for visual distinction
    SPEAKER_ICONS = {
        Speaker.HOST: "🎙️",
        Speaker.GUEST_1: "👨‍🔬",
        Speaker.GUEST_2: "👔",
        Speaker.USER: "💬",
        Speaker.SYSTEM: "ℹ️"
    }
    
    # Visual separators
    SEPARATOR_MAIN = "═" * 60
    SEPARATOR_SUB = "─" * 60
    
    @staticmethod
    def format_message(message: Message) -> str:
        """Format a single message for display.
        
        Args:
            message: The message to format
            
        Returns:
            Formatted message string
        """
        icon = ConversationFormatter.SPEAKER_ICONS.get(message.speaker, "💭")
        
        # Format speaker name with icon
        speaker_line = f"{icon} {message.persona_name.upper()}"
        
        # Add role label for clarity
        role_label = ""
        if message.speaker == Speaker.HOST:
            role_label = " (Host)"
        elif message.speaker in [Speaker.GUEST_1, Speaker.GUEST_2]:
            role_label = " (Guest)"
        elif message.speaker == Speaker.USER:
            role_label = " (You)"
        
        speaker_line += role_label + ":"
        
        # Build the formatted output
        output_parts = [
            "",  # Blank line before
            ConversationFormatter.SEPARATOR_MAIN,
            speaker_line,
            ConversationFormatter.SEPARATOR_SUB,
            message.content,
            ""  # Blank line after
        ]
        
        return "\n".join(output_parts)
    
    @staticmethod
    def format_user_prompt(exchanges_count: int) -> str:
        """Format the user input prompt.
        
        Args:
            exchanges_count: Number of exchanges since last user input
            
        Returns:
            Formatted prompt string
        """
        prompt_parts = [
            "",
            ConversationFormatter.SEPARATOR_MAIN,
            "💬 YOUR TURN",
            ConversationFormatter.SEPARATOR_SUB,
            "Would you like to join the conversation?",
            "  • Type your comment or question",
            "  • Press Enter to continue listening",
            "  • Type 'stop', 'exit', or 'quit' to end the podcast",
            "",
        ]
        return "\n".join(prompt_parts)
    
    @staticmethod
    def format_quick_pause() -> str:
        """Format a quick pause for user to optionally chime in.
        
        Returns:
            Formatted quick pause prompt
        """
        prompt_parts = [
            "",
            "💭 [Pause - Press Enter to continue, or type to chime in...]",
        ]
        return "\n".join(prompt_parts)
    
    @staticmethod
    def format_welcome(topic: str, host_name: str, guest_names: list) -> str:
        """Format the welcome message at the start of the podcast.
        
        Args:
            topic: The discussion topic
            host_name: Name of the host
            guest_names: Names of the guests
            
        Returns:
            Formatted welcome message
        """
        guests_str = " and ".join(guest_names)
        
        welcome_parts = [
            "",
            "═" * 60,
            "🎙️  WELCOME TO AI-PODCAST  🎙️",
            "═" * 60,
            f"📝 Topic: {topic}",
            f"🎤 Host: {host_name}",
            f"👥 Guests: {guests_str}",
            "═" * 60,
            "",
            "🎬 Let's begin...",
            ""
        ]
        
        return "\n".join(welcome_parts)
    
    @staticmethod
    def format_goodbye() -> str:
        """Format the goodbye message at the end of the podcast.
        
        Returns:
            Formatted goodbye message
        """
        goodbye_parts = [
            "",
            "═" * 60,
            "🎙️  THANK YOU FOR LISTENING  🎙️",
            "═" * 60,
            "",
            "The podcast has ended. We hope you enjoyed the conversation!",
            "",
            "═" * 60,
            ""
        ]
        
        return "\n".join(goodbye_parts)
    
    @staticmethod
    def format_error(error_message: str) -> str:
        """Format an error message.
        
        Args:
            error_message: The error message to display
            
        Returns:
            Formatted error message
        """
        error_parts = [
            "",
            "❌ ERROR",
            "─" * 60,
            error_message,
            ""
        ]
        
        return "\n".join(error_parts)
    
    @staticmethod
    def format_system_message(message: str) -> str:
        """Format a system message.
        
        Args:
            message: The system message to display
            
        Returns:
            Formatted system message
        """
        system_parts = [
            "",
            f"ℹ️  {message}",
            ""
        ]
        
        return "\n".join(system_parts)
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen (optional, for cleaner display)."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

