"""Conversation Service - Main conversation loop orchestration.

This module implements the core conversation loop that manages the podcast
dialogue between host, guests, and user participants.
"""

import logging
import time
from typing import Dict, List, Optional
from models.conversation import ConversationState, ConversationStatus, Message, Speaker
from cli.formatter import ConversationFormatter

logger = logging.getLogger(__name__)


class ConversationService:
    """Manages the podcast conversation flow and agent coordination."""
    
    EXIT_COMMANDS = ['stop', 'exit', 'quit', 'end', 'bye']
    
    def __init__(self, persona_set: Dict, topic: str):
        """Initialize the conversation service.
        
        Args:
            persona_set: The persona set configuration
            topic: The discussion topic
        """
        self.persona_set = persona_set
        self.topic = topic
        self.formatter = ConversationFormatter()
        
        # Extract persona information
        self.host_name = persona_set['host']['name']
        self.guest_names = [guest['name'] for guest in persona_set['guests']]
        
        # Initialize conversation state
        self.state = ConversationState(
            topic=topic,
            persona_set_id=persona_set['set_id'],
            persona_set=persona_set,
            host_name=self.host_name,
            guest_names=self.guest_names
        )
        
        logger.info(f"Conversation service initialized for topic: {topic}")
    
    def start_conversation(self) -> bool:
        """Start the podcast conversation.
        
        Returns:
            True if conversation completed successfully, False otherwise
        """
        try:
            # Display welcome message
            print(self.formatter.format_welcome(
                self.topic,
                self.host_name,
                self.guest_names
            ))
            
            # Host introduction
            self._host_introduce()
            
            # Set status to active
            self.state.status = ConversationStatus.ACTIVE
            
            # Main conversation loop
            conversation_active = True
            while conversation_active and self.state.is_active():
                # Run a conversation exchange (host asks, guests respond)
                self._run_conversation_exchange()
                
                # Check if we should prompt user
                if self.state.should_prompt_user():
                    user_input = self._prompt_user_input()
                    
                    # Check for exit command
                    if self._is_exit_command(user_input):
                        conversation_active = False
                        break
                    
                    # Process user input if provided
                    if user_input and user_input.strip():
                        self._process_user_input(user_input)
                        self.state.user_has_participated = True
                    
                    # Reset counter after user prompt
                    self.state.reset_user_prompt_counter()
                
                # Safety limit: prevent infinite loops
                if self.state.current_turn > 50:
                    logger.warning("Reached maximum turn limit, ending conversation")
                    break
            
            # End the conversation gracefully
            self._host_close()
            self.state.status = ConversationStatus.COMPLETED
            
            # Display goodbye
            print(self.formatter.format_goodbye())
            
            logger.info(f"Conversation completed after {self.state.current_turn} turns")
            return True
            
        except KeyboardInterrupt:
            logger.info("Conversation interrupted by user")
            print("\n")
            print(self.formatter.format_system_message("Podcast interrupted. Ending gracefully..."))
            self._host_close()
            print(self.formatter.format_goodbye())
            return False
            
        except Exception as e:
            logger.error(f"Error during conversation: {e}", exc_info=True)
            print(self.formatter.format_error(f"An error occurred: {str(e)}"))
            return False
    
    def _host_introduce(self):
        """Host introduces the podcast and topic."""
        # Build introduction based on persona
        intro = self._generate_host_introduction()
        
        # Add message to state
        message = self.state.add_message(
            speaker=Speaker.HOST,
            persona_name=self.host_name,
            content=intro,
            speaker_id=self.persona_set['host']['id']
        )
        
        # Display the introduction
        print(self.formatter.format_message(message))
        
        time.sleep(0.5)  # Brief pause for readability
    
    def _generate_host_introduction(self) -> str:
        """Generate the host's introduction based on persona.
        
        Returns:
            Introduction text
        """
        guests_str = " and ".join(self.guest_names)
        
        # Use persona-specific introduction style
        intro = (
            f"Welcome to AI-Podcast! I'm your host, {self.host_name}, "
            f"and today we're diving into a fascinating topic: {self.topic}. "
            f"I'm joined by {guests_str}. "
            f"Let's explore this together!"
        )
        
        return intro
    
    def _run_conversation_exchange(self):
        """Run one exchange of conversation (host question + guest responses)."""
        # Host asks a question
        self._host_ask_question()
        
        # Allow user to chime in after host question
        user_input = self._quick_pause_for_user()
        if user_input:
            return  # User participated, skip rest of exchange
        
        # Guest 1 responds
        self._guest_respond(0)
        
        # Allow user to chime in after guest 1
        user_input = self._quick_pause_for_user()
        if user_input:
            return  # User participated, skip rest of exchange
        
        # Guest 2 responds (if exists)
        if len(self.guest_names) > 1:
            self._guest_respond(1)
            
            # Allow user to chime in after guest 2
            user_input = self._quick_pause_for_user()
            if user_input:
                return  # User participated, skip rest of exchange
        
        # Host provides a brief transition/follow-up
        self._host_followup()
        
        # Increment exchange counter
        self.state.increment_exchange_counter()
    
    def _host_ask_question(self):
        """Host asks a question based on conversation context."""
        context = self.state.get_context_summary()
        question = self._generate_host_question(context)
        
        message = self.state.add_message(
            speaker=Speaker.HOST,
            persona_name=self.host_name,
            content=question,
            speaker_id=self.persona_set['host']['id']
        )
        
        print(self.formatter.format_message(message))
        time.sleep(0.5)
    
    def _generate_host_question(self, context: str) -> str:
        """Generate a host question based on context.
        
        Args:
            context: Current conversation context
            
        Returns:
            Question text
        """
        # Simple question generation for MVP
        # In production, this would call the actual host agent
        turn = self.state.current_turn
        
        questions = [
            f"Let's dig deeper into {self.topic}. What are the key considerations we should be thinking about?",
            "That's a fascinating perspective. How do you see this playing out in practice?",
            "Building on that point, what challenges might we encounter?",
            "What opportunities does this present for innovation?",
            "How should we balance the different perspectives on this?",
            "What does the future look like in this space?",
        ]
        
        # Rotate through questions
        question_index = (turn // 4) % len(questions)
        return questions[question_index]
    
    def _guest_respond(self, guest_index: int):
        """Have a guest respond to the current discussion.
        
        Args:
            guest_index: Index of the guest (0 or 1)
        """
        if guest_index >= len(self.persona_set['guests']):
            return
        
        guest_config = self.persona_set['guests'][guest_index]
        guest_name = guest_config['name']
        guest_id = guest_config['id']
        
        # Determine speaker type
        speaker = Speaker.GUEST_1 if guest_index == 0 else Speaker.GUEST_2
        
        # Generate response
        response = self._generate_guest_response(guest_config)
        
        message = self.state.add_message(
            speaker=speaker,
            persona_name=guest_name,
            content=response,
            speaker_id=guest_id
        )
        
        print(self.formatter.format_message(message))
        time.sleep(0.5)
    
    def _generate_guest_response(self, guest_config: Dict) -> str:
        """Generate a guest response based on their persona.
        
        Args:
            guest_config: Guest persona configuration
            
        Returns:
            Response text
        """
        # Simple response generation for MVP
        # In production, this would call the actual guest agent
        
        persona_style = guest_config.get('speaking_style', '')
        example_phrases = guest_config.get('example_phrases', [])
        
        # Determine response style based on persona traits
        if 'analytical' in guest_config.get('personality_traits', []):
            # Academic/analytical response
            responses = [
                "From a research perspective, the data shows several interesting trends here.",
                "Studies indicate that this is a complex issue with multiple variables to consider.",
                "The theoretical framework suggests we need to examine this more closely.",
                "Based on the evidence, I think we're seeing a fundamental shift in how this works.",
            ]
        elif 'practical' in guest_config.get('personality_traits', []):
            # Practical/entrepreneurial response
            responses = [
                "In my experience, what actually works is focusing on measurable outcomes.",
                "We implemented something similar at my company, and the results were eye-opening.",
                "The practical reality is that execution matters more than perfect planning.",
                "Here's what I've learned from building this in the real world.",
            ]
        else:
            # Generic response
            responses = [
                "That's an important point to consider.",
                "I think there are several angles we should explore here.",
                "This connects to broader trends we're seeing.",
                "It's worth thinking about the implications of this.",
            ]
        
        # Rotate through responses
        turn = self.state.current_turn
        response_index = turn % len(responses)
        return responses[response_index]
    
    def _host_followup(self):
        """Host provides a brief follow-up or transition."""
        followups = [
            "Excellent points from both of you. Let's explore this further.",
            "That's fascinating. There's clearly a lot to unpack here.",
            "I love how you've framed that. Let's dig deeper.",
            "These are important perspectives. Let's continue.",
        ]
        
        turn = self.state.current_turn
        followup_index = turn % len(followups)
        followup = followups[followup_index]
        
        message = self.state.add_message(
            speaker=Speaker.HOST,
            persona_name=self.host_name,
            content=followup,
            speaker_id=self.persona_set['host']['id']
        )
        
        print(self.formatter.format_message(message))
        time.sleep(0.5)
    
    def _prompt_user_input(self) -> Optional[str]:
        """Prompt the user for input.
        
        Returns:
            User input string, or None if no input
        """
        print(self.formatter.format_user_prompt(self.state.exchanges_since_user_prompt))
        
        try:
            user_input = input("👉 ").strip()
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "stop"
    
    def _quick_pause_for_user(self) -> bool:
        """Provide a quick pause for user to chime in.
        
        Returns:
            True if user provided input, False if they continued listening
        """
        # Display quick prompt
        print(self.formatter.format_quick_pause())
        
        try:
            # Short timeout for input
            import select
            import sys
            
            # For non-Unix systems, use simpler input
            if sys.platform == 'win32':
                # Windows: just use regular input with prompt
                user_input = input("").strip()
            else:
                # Unix/Mac: Use select with timeout for non-blocking input
                # Wait up to 2 seconds for user input
                ready, _, _ = select.select([sys.stdin], [], [], 2.0)
                
                if ready:
                    user_input = sys.stdin.readline().strip()
                else:
                    # No input within timeout, continue
                    print("   [Continuing...]")
                    return False
            
            # Check if user wants to exit
            if self._is_exit_command(user_input):
                self.state.status = ConversationStatus.ENDING
                return True
            
            # If user provided input, process it
            if user_input:
                self._process_user_input(user_input)
                self.state.user_has_participated = True
                return True
            
            # User pressed Enter, continue
            return False
            
        except (EOFError, KeyboardInterrupt):
            self.state.status = ConversationStatus.ENDING
            return True
        except Exception as e:
            # If select doesn't work, fall back to simple behavior
            logger.debug(f"Quick pause timeout not available: {e}")
            return False
    
    def _is_exit_command(self, user_input: Optional[str]) -> bool:
        """Check if user input is an exit command.
        
        Args:
            user_input: The user's input
            
        Returns:
            True if input is an exit command
        """
        if not user_input:
            return False
        
        return user_input.lower() in self.EXIT_COMMANDS
    
    def _process_user_input(self, user_input: str):
        """Process user input and integrate it into the conversation.
        
        Args:
            user_input: The user's input text
        """
        # Add user message to history
        user_message = self.state.add_message(
            speaker=Speaker.USER,
            persona_name="You",
            content=user_input,
            speaker_id="user"
        )
        
        print(self.formatter.format_message(user_message))
        
        # Host acknowledges user input
        acknowledgment = self._generate_host_acknowledgment(user_input)
        host_message = self.state.add_message(
            speaker=Speaker.HOST,
            persona_name=self.host_name,
            content=acknowledgment,
            speaker_id=self.persona_set['host']['id']
        )
        
        print(self.formatter.format_message(host_message))
        time.sleep(0.5)
        
        # Have one or both guests respond to user input
        self._guest_respond(0)
        
        if len(self.guest_names) > 1:
            self._guest_respond(1)
    
    def _generate_host_acknowledgment(self, user_input: str) -> str:
        """Generate host acknowledgment of user input.
        
        Args:
            user_input: The user's input
            
        Returns:
            Acknowledgment text
        """
        # Check if it's a question
        is_question = '?' in user_input
        
        if is_question:
            acknowledgments = [
                "Great question from our listener! Let's hear what our guests think about this.",
                "That's an excellent question. This is exactly what we need to explore.",
                "I'm glad you asked that. Let's get our guests' perspectives on this.",
            ]
        else:
            acknowledgments = [
                "Thank you for that insight! Let's hear what our guests think about this perspective.",
                "That's a great point. Let's explore this further with our guests.",
                "Interesting observation! Let's see how this connects to what we've been discussing.",
            ]
        
        turn = self.state.current_turn
        ack_index = turn % len(acknowledgments)
        return acknowledgments[ack_index]
    
    def _host_close(self):
        """Host provides closing remarks."""
        closing = self._generate_host_closing()
        
        message = self.state.add_message(
            speaker=Speaker.HOST,
            persona_name=self.host_name,
            content=closing,
            speaker_id=self.persona_set['host']['id']
        )
        
        print(self.formatter.format_message(message))
    
    def _generate_host_closing(self) -> str:
        """Generate the host's closing remarks.
        
        Returns:
            Closing text
        """
        guests_str = " and ".join(self.guest_names)
        
        closing = (
            f"Thank you all for joining this fascinating discussion about {self.topic}! "
            f"Big thanks to {guests_str} for sharing their insights. "
            "And to you, our listener, for being part of this conversation. "
            "Until next time, keep exploring and stay curious!"
        )
        
        return closing
    
    def get_conversation_summary(self) -> Dict:
        """Get a summary of the conversation.
        
        Returns:
            Dictionary with conversation statistics
        """
        return {
            'topic': self.topic,
            'total_turns': self.state.current_turn,
            'total_messages': len(self.state.history),
            'user_participated': self.state.user_has_participated,
            'status': self.state.status.value,
            'host_name': self.host_name,
            'guest_names': self.guest_names
        }

