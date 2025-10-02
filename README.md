# AI-Podcast

An interactive, text-based conversational application that simulates a podcast experience with AI-powered hosts and guests using Google's Agent Development Kit (ADK).

## Quick Start

### Prerequisites

- Python 3.9+
- Google AI Studio API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd ai-podcast
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google AI Studio API key
   ```

5. **Test the basic orchestrator agent:**
   ```bash
   python test_agent.py
   ```

### Running the Agent

#### Option 1: Using ADK CLI
```bash
cd backend/agents
adk run orchestrator
```

#### Option 2: Using ADK Web Interface
```bash
cd backend/agents
adk web
# Open http://localhost:8000 in your browser
# Select "podcast_orchestrator" from the dropdown
```

## Project Structure

```
ai-podcast/
├── backend/
│   └── agents/
│       └── orchestrator/          # Orchestrator agent (Google ADK structure)
│           ├── __init__.py
│           └── agent.py           # Main agent implementation
├── documentation/                 # Project documentation
├── requirements.txt              # Python dependencies
├── test_agent.py                 # Basic agent test script
└── README.md                     # This file
```

## Current Features

- ✅ Basic orchestrator agent setup
- ✅ Google ADK integration
- ✅ Tool-based functionality (topic collection, podcast management)
- ✅ Environment configuration
- ✅ Basic testing framework

## Next Steps

This is the initial MVP setup. Future development will include:

1. **Multi-agent conversation system** - Add host and guest agents
2. **Persona configuration system** - Configurable AI personalities
3. **Conversation flow management** - Turn-taking and dialogue coordination
4. **Enhanced CLI interface** - Better user interaction
5. **Persona sets** - Technology, sports, business domain experts

## Documentation

- [Product Requirements Document](documentation/PRD.MD)
- [Technical Specifications](documentation/TECHNICAL_SPECS.MD)

## Troubleshooting

### Common Issues

1. **"Invalid API Key" Error**
   - Verify your API key in the `.env` file
   - Ensure no extra spaces or quotes
   - Get a new key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. **Agent Not Found**
   - Make sure you're running commands from the `backend/agents` directory
   - Verify the orchestrator folder structure exists

3. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

## Contributing

This project follows the Google ADK structure and patterns. Please refer to the [Technical Specifications](documentation/TECHNICAL_SPECS.MD) for detailed development guidelines.

## License

[Add your license here]
