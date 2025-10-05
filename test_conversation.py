#!/usr/bin/env python3
"""
Test script for conversation loop functionality.
This tests the conversation service without requiring user interaction.
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from persona.manager import PersonaConfigManager
from services.conversation_service import ConversationService
from models.conversation import ConversationStatus

def test_conversation_initialization():
    """Test that conversation service can be initialized."""
    print("🧪 Testing conversation service initialization...")
    
    try:
        # Load persona manager
        persona_manager = PersonaConfigManager()
        print(f"✅ Loaded {len(persona_manager.list_available_sets())} persona sets")
        
        # Get technology persona set
        persona_set = persona_manager.get_persona_set('technology')
        print(f"✅ Loaded technology persona set")
        
        # Select guests from pool (same as main.py does)
        selected_guests = persona_manager.select_guests(persona_set, 2)  # Use 2 guests for test
        print(f"✅ Selected 2 guests: {', '.join([g['name'] for g in selected_guests])}")
        
        # Create a modified persona set with selected guests (same as main.py)
        persona_set_with_selected_guests = persona_set.copy()
        persona_set_with_selected_guests['guests'] = selected_guests
        
        # Initialize conversation service
        topic = "The future of artificial intelligence"
        conversation_service = ConversationService(
            persona_set=persona_set_with_selected_guests,
            topic=topic
        )
        print(f"✅ Initialized conversation service with topic: {topic}")
        
        # Check initial state
        assert conversation_service.state.status == ConversationStatus.INITIALIZING
        assert conversation_service.state.topic == topic
        assert conversation_service.state.current_turn == 0
        assert len(conversation_service.state.history) == 0
        print(f"✅ Initial state is correct")
        
        # Test conversation summary
        summary = conversation_service.get_conversation_summary()
        assert summary['topic'] == topic
        assert summary['total_turns'] == 0
        print(f"✅ Conversation summary works")
        
        print("\n✅ All initialization tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_state():
    """Test conversation state management."""
    print("\n🧪 Testing conversation state management...")
    
    try:
        from models.conversation import ConversationState, Speaker
        
        # Create a test conversation state
        state = ConversationState(
            topic="Test topic",
            persona_set_id="technology",
            persona_set={'set_id': 'technology', 'set_name': 'Tech'},
            host_name="Test Host",
            guest_names=["Guest 1", "Guest 2"]
        )
        
        print(f"✅ Created conversation state")
        
        # Test adding messages
        msg1 = state.add_message(Speaker.HOST, "Test Host", "Hello world", "host_1")
        assert state.current_turn == 1
        assert len(state.history) == 1
        print(f"✅ Added message, turn counter works")
        
        msg2 = state.add_message(Speaker.GUEST_1, "Guest 1", "Response", "guest_1")
        assert state.current_turn == 2
        assert len(state.history) == 2
        print(f"✅ Multiple messages work")
        
        # Test recent history
        recent = state.get_recent_history(5)
        assert len(recent) == 2
        print(f"✅ Recent history retrieval works")
        
        # Test context summary
        context = state.get_context_summary()
        assert "Test topic" in context
        print(f"✅ Context summary generation works")
        
        # Test user prompt logic
        state.status = ConversationStatus.ACTIVE
        state.exchanges_since_user_prompt = 3
        state.max_exchanges_before_prompt = 3
        assert state.should_prompt_user() == True
        print(f"✅ User prompt logic works")
        
        state.reset_user_prompt_counter()
        assert state.exchanges_since_user_prompt == 0
        print(f"✅ Counter reset works")
        
        print("\n✅ All state management tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_formatter():
    """Test CLI formatter."""
    print("\n🧪 Testing CLI formatter...")
    
    try:
        from cli.formatter import ConversationFormatter
        from models.conversation import Message, Speaker
        
        formatter = ConversationFormatter()
        print(f"✅ Created formatter")
        
        # Test message formatting
        msg = Message(
            speaker=Speaker.HOST,
            persona_name="Test Host",
            content="This is a test message",
            turn_number=1,
            speaker_id="host_1"
        )
        
        formatted = formatter.format_message(msg)
        assert "TEST HOST" in formatted  # Formatter converts to uppercase
        assert "This is a test message" in formatted
        print(f"✅ Message formatting works")
        
        # Test welcome formatting
        welcome = formatter.format_welcome(
            topic="Test Topic",
            host_name="Test Host",
            guest_names=["Guest 1", "Guest 2"]
        )
        assert "Test Topic" in welcome
        assert "Test Host" in welcome
        print(f"✅ Welcome formatting works")
        
        # Test user prompt formatting
        prompt = formatter.format_user_prompt(3)
        assert "YOUR TURN" in prompt
        print(f"✅ User prompt formatting works")
        
        print("\n✅ All formatter tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 CONVERSATION LOOP ENGINE TESTS")
    print("=" * 60)
    print()
    
    tests = [
        test_conversation_initialization,
        test_conversation_state,
        test_formatter,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED! The conversation loop engine is working correctly.")
        print("\n🎉 You can now run the full application:")
        print("   python backend/main.py --persona-set technology --topic 'AI ethics'")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

