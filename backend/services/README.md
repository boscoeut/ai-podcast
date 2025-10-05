# Conversation Service

## Overview

The Conversation Service is the core engine that orchestrates podcast conversations between the AI host, guest agents, and human users. It manages the conversation flow, turn-taking, user interaction, and session lifecycle.

## Architecture

```
ConversationService
├── ConversationState (tracks current state)
├── ConversationFormatter (formats output)
└── Conversation Loop
    ├── Host Introduction
    ├── Conversation Exchanges
    │   ├── Host asks question
    │   ├── Guest 1 responds
    │   ├── Guest 2 responds
    │   └── Host follows up
    ├── User Participation Prompts
    │   ├── Prompt every 3 exchanges
    │   ├── Process user input
    │   └── Check for exit commands
    └── Host Closing
```

## Key Components

### ConversationService

Main service class that orchestrates the entire conversation flow.

**Key Methods:**
- `start_conversation()` - Begins the podcast session
- `_run_conversation_exchange()` - Executes one full exchange cycle
- `_prompt_user_input()` - Prompts user for participation
- `_process_user_input()` - Integrates user input into conversation
- `get_conversation_summary()` - Returns conversation statistics

### ConversationState

Tracks the state of an ongoing conversation.

**Attributes:**
- `topic` - Discussion topic
- `status` - Current status (initializing, active, ending, completed)
- `current_turn` - Current turn number
- `history` - List of all messages
- `exchanges_since_user_prompt` - Counter for prompting user

**Key Methods:**
- `add_message()` - Add a message to history
- `get_recent_history()` - Get last N messages
- `should_prompt_user()` - Determine if user should be prompted
- `get_context_summary()` - Generate context for agents

### ConversationFormatter

Formats conversation output for CLI display.

**Key Methods:**
- `format_message()` - Format a single message with speaker icons
- `format_welcome()` - Format welcome message at start
- `format_user_prompt()` - Format user input prompt
- `format_goodbye()` - Format closing message
- `format_error()` - Format error messages

## Conversation Flow

### 1. Initialization
```python
conversation_service = ConversationService(
    persona_set=selected_persona_set,
    topic="Your topic here"
)
```

### 2. Start Conversation
```python
success = conversation_service.start_conversation()
```

The conversation includes natural pause points after each speaker, allowing users to chime in at any time.

The conversation follows this sequence:

1. **Welcome Message** - Display formatted welcome
2. **Host Introduction** - Host introduces podcast and topic
3. **Main Loop** - Repeat until exit:
   - Run conversation exchange with pauses after each agent:
     - Host asks question → **PAUSE**
     - Guest 1 responds → **PAUSE**
     - Guest 2 responds → **PAUSE**
     - Host follows up
   - Check if we should show full prompt (every 3 exchanges)
   - Process user input if provided at any pause
   - Check for exit commands
4. **Host Closing** - Host provides closing remarks
5. **Goodbye Message** - Display formatted goodbye

### 3. Conversation Exchange

Each exchange consists of:
1. Host asks a question → User can chime in
2. Guest 1 responds → User can chime in
3. Guest 2 responds → User can chime in
4. Host provides follow-up/transition

After each step, a brief pause allows the user to interrupt naturally.

### 4. User Participation

Users can participate at any pause point after each speaker, plus receive full prompts every 3 exchanges with options to:
- Enter a comment or question
- Press Enter to continue listening
- Type exit commands ('stop', 'exit', 'quit', 'end', 'bye')

When user provides input:
1. User message is displayed
2. Host acknowledges the input
3. Guests respond to user's point
4. Conversation continues

## User Participation

The conversation service provides natural pause points after each agent speaks:

- **Quick Pauses**: After every agent response, users can chime in
- **Auto-Continue**: On macOS/Linux, pauses auto-continue after 2 seconds if no input
- **Manual Continue**: Press Enter to immediately continue
- **Exit Anytime**: Type 'stop', 'exit', 'quit' at any pause to end gracefully

## Configuration

The service uses configuration from the persona set:

```python
{
    'set_id': 'technology',
    'set_name': 'Technology Experts',
    'host': {...},  # Host persona config
    'guests': [     # Guest persona configs
        {...},
        {...}
    ]
}
```

## Example Usage

```python
from persona.manager import PersonaConfigManager
from services.conversation_service import ConversationService

# Load persona set
persona_manager = PersonaConfigManager()
persona_set = persona_manager.get_persona_set('technology')

# Initialize conversation (pauses are always enabled)
conversation = ConversationService(
    persona_set=persona_set,
    topic="The future of AI in healthcare"
)

# Start the conversation
# Users will see pauses after each speaker
success = conversation.start_conversation()

# Get summary
if success:
    summary = conversation.get_conversation_summary()
    print(f"Conversation completed in {summary['total_turns']} turns")
```

## Error Handling

The service handles:
- **Keyboard Interrupts (Ctrl+C)** - Graceful exit with closing
- **API Errors** - Logged and displayed to user
- **Invalid Input** - Handled appropriately
- **Infinite Loops** - Safety limit of 50 turns

## Future Enhancements

For Phase 2 and beyond, the conversation service can be enhanced with:

1. **Real Agent Integration** - Call actual ADK agents instead of simulated responses
2. **Advanced Turn-Taking** - Dynamic turn allocation based on relevance
3. **Context Management** - Smarter context passing to agents
4. **Configurable Pause Timeout** - Allow users to set custom timeout durations
5. **Conversation History** - Persist conversations across sessions
6. **Voice Integration** - Text-to-speech and speech-to-text
7. **Multi-User Support** - Multiple human participants

## Testing

Run the test suite:
```bash
python test_conversation.py
```

This tests:
- Conversation service initialization
- State management
- Message history tracking
- User prompt logic
- CLI formatting

## Logging

The service uses Python's logging module:

```python
import logging
logger = logging.getLogger(__name__)

# Set log level in .env
LOG_LEVEL=INFO
```

Logged events:
- Conversation initialization
- Turn progression
- User input processing
- Errors and exceptions
- Conversation completion

## Performance

Current implementation uses simulated agent responses for MVP speed:
- Response generation: < 100ms
- No API calls during MVP testing
- 50 turn safety limit prevents infinite loops

When integrated with real ADK agents:
- Expected response time: 2-5 seconds per agent
- API rate limits apply
- Context window management needed

