#!/usr/bin/env python3
"""
AI-Podcast Main Entry Point.

This is the main entry point for the AI-Podcast application.
It provides a command-line interface for starting podcast conversations
with configurable AI personas.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path for imports
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from persona.manager import PersonaConfigManager
from services.conversation_service import ConversationService


def load_environment():
    """Load environment variables from .env file."""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        print(f"✅ Loaded environment from {env_file}")
    else:
        print("⚠️  No .env file found. Using default configuration.")
        print("   Create .env from .env.example template if needed.")


def setup_logging():
    """Setup logging configuration."""
    import logging
    
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured at {log_level} level")


def validate_api_key():
    """Validate that API key is configured."""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("❌ Error: GOOGLE_API_KEY not configured!")
        print("   Please set your API key in the .env file.")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("✅ API key configured")
    return True


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="AI-Podcast: Interactive AI-powered podcast conversations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive persona selection
  python main.py --persona-set technology          # Use technology personas
  python main.py --persona-set technology --topic "AI ethics"  # Start with topic
        """
    )
    
    parser.add_argument(
        '--persona-set', 
        type=str,
        help='Persona set to use (e.g., technology, sports, business)'
    )
    
    parser.add_argument(
        '--topic',
        type=str,
        help='Initial discussion topic'
    )
    
    parser.add_argument(
        '--list-personas',
        action='store_true',
        help='List available persona sets and exit'
    )
    
    parser.add_argument(
        '--info',
        type=str,
        help='Show information about a specific persona set'
    )
    
    args = parser.parse_args()
    
    # Load environment and setup
    load_environment()
    setup_logging()
    
    try:
        # Initialize persona manager with absolute path
        print("🤖 Initializing AI-Podcast...")
        # Calculate path to personas directory (at project root)
        project_root = Path(__file__).parent.parent
        personas_path = project_root / "personas"
        persona_manager = PersonaConfigManager(config_dir=str(personas_path))
        
        # Handle list command
        if args.list_personas:
            print("\n📋 Available Persona Sets:")
            for set_id in persona_manager.list_available_sets():
                info = persona_manager.get_persona_set_info(set_id)
                print(f"\n  {info['set_name']} ({set_id})")
                print(f"    Description: {info['description']}")
                print(f"    Host: {info['host_name']} - {info['host_title']}")
                print(f"    Guests: {', '.join(info['guest_names'])}")
            return
        
        # Handle info command
        if args.info:
            try:
                info = persona_manager.get_persona_set_info(args.info)
                print(f"\n📊 Persona Set: {info['set_name']}")
                print(f"   ID: {info['set_id']}")
                print(f"   Description: {info['description']}")
                print(f"   Domains: {', '.join(info['domains'])}")
                print(f"   Host: {info['host_name']} - {info['host_title']}")
                print(f"   Guests ({info['guest_count']}):")
                for name, title in zip(info['guest_names'], info['guest_titles']):
                    print(f"     - {name} - {title}")
            except ValueError as e:
                print(f"❌ Error: {e}")
            return
        
        # Validate API key
        if not validate_api_key():
            sys.exit(1)
        
        # Select persona set
        if args.persona_set:
            try:
                selected_persona_set = persona_manager.get_persona_set(args.persona_set)
                print(f"✅ Using persona set: {selected_persona_set['set_name']}")
            except ValueError as e:
                print(f"❌ Error: {e}")
                sys.exit(1)
        else:
            try:
                selected_persona_set = persona_manager.select_persona_set()
                print(f"✅ Selected: {selected_persona_set['set_name']}")
            except (ValueError, KeyboardInterrupt) as e:
                print(f"❌ Error: {e}")
                sys.exit(1)
        
        # Get topic
        if args.topic:
            topic = args.topic
            print(f"📝 Topic: {topic}")
        else:
            topic = input("\n🎯 What topic would you like to discuss today? ").strip()
            if not topic:
                print("❌ Error: Please provide a topic for discussion.")
                sys.exit(1)
        
        # Get guest count from user
        guest_pool = persona_manager.get_guest_personas(selected_persona_set['set_id'])
        default_guest_count = selected_persona_set.get('default_guest_count', 2)
        max_guests = len(guest_pool)
        
        print(f"\n👥 How many guests would you like for this podcast? (1-{max_guests})")
        print(f"   Available guests: {', '.join([g['name'] for g in guest_pool])}")
        
        guest_count = None
        while guest_count is None:
            try:
                guest_input = input(f"   Guest count [default: {default_guest_count}]: ").strip()
                
                if not guest_input:
                    # Use default
                    guest_count = default_guest_count
                else:
                    guest_count = int(guest_input)
                    
                    # Validate range
                    if guest_count < 1 or guest_count > max_guests:
                        print(f"   ⚠️  Please enter a number between 1 and {max_guests}")
                        guest_count = None
                        continue
                        
            except ValueError:
                print("   ⚠️  Please enter a valid number")
                continue
        
        # Select guests from pool
        try:
            selected_guests = persona_manager.select_guests(selected_persona_set, guest_count)
            print(f"✅ Selected {guest_count} guest(s): {', '.join([g['name'] for g in selected_guests])}")
            
            # Create a modified persona set with selected guests
            persona_set_with_selected_guests = selected_persona_set.copy()
            persona_set_with_selected_guests['guests'] = selected_guests
            
        except ValueError as e:
            print(f"❌ Error selecting guests: {e}")
            sys.exit(1)
        
        # Start podcast session with conversation service
        print(f"\n🎙️  Starting AI-Podcast session...")
        print(f"   Topic: {topic}")
        print(f"   Host: {persona_set_with_selected_guests['host']['name']}")
        print(f"   Guests: {', '.join([guest['name'] for guest in persona_set_with_selected_guests['guests']])}")
        print("\n   Press Ctrl+C at any time to exit gracefully")
        
        # Initialize conversation service with selected guests
        conversation_service = ConversationService(
            persona_set=persona_set_with_selected_guests,
            topic=topic
        )
        
        print("   💭 You can chime in after each speaker during the conversation")
        
        # Start the conversation
        success = conversation_service.start_conversation()
        
        # Display conversation summary
        if success:
            summary = conversation_service.get_conversation_summary()
            print(f"\n📊 Conversation Summary:")
            print(f"   Total turns: {summary['total_turns']}")
            print(f"   User participated: {'Yes' if summary['user_participated'] else 'No'}")
            print(f"\n✅ Thank you for using AI-Podcast!")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"❌ Error initializing AI-Podcast: {e}")
        if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
