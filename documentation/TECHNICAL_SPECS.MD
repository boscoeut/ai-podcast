# Technical Specifications: AI-Podcast

> **Note**: This document contains technical architecture, implementation details, and development guidelines. For product vision, functional requirements, and user stories, see the [Product Requirements Document (PRD)](./PRD.MD).

## Overview

This document contains the technical specifications, architecture, and implementation details for the AI-Podcast application. It is designed for developers, architects, and technical stakeholders who will be implementing the system.

---

## Table of Contents

1. [Technical Requirements](#technical-requirements)
2. [Non-Functional Requirements](#non-functional-requirements)
3. [System Architecture](#system-architecture)
4. [Data Models](#data-models)
5. [API Specifications](#api-specifications)
6. [Technology Stack](#technology-stack)
7. [Implementation Phases](#implementation-phases)
8. [Testing Strategy](#testing-strategy)

---

## Technical Requirements

### TR1: Framework & Platform
- **TR1.1**: Application shall be built using Google's Agent Development Kit (ADK) v1.4.2+
- **TR1.2**: Application shall use Python 3.9+
- **TR1.3**: Application shall use Gemini models (gemini-2.5-flash or gemini-2.0-flash-exp)
- **TR1.4**: Application shall support both Google AI Studio and Vertex AI platforms

### TR2: Architecture
- **TR2.1**: System shall implement multi-agent architecture using ADK Agent class
- **TR2.2**: Each AI persona (host + guests) shall be implemented as a separate Agent
- **TR2.3**: System shall use a root orchestrator agent to manage conversation flow
- **TR2.4**: Agents shall communicate through ADK's agent orchestration mechanisms

### TR3: Agent Configuration
- **TR3.1**: Each agent shall have distinct system instructions defining their persona
- **TR3.2**: Agents shall use appropriate model parameters (temperature, top_p) for persona consistency
- **TR3.3**: Host agent shall have elevated orchestration capabilities
- **TR3.4**: Agents shall maintain conversation history/context

### TR4: Conversation Engine
- **TR4.1**: System shall implement turn-based conversation logic
- **TR4.2**: System shall track conversation state (topic, participants, turn order)
- **TR4.3**: System shall implement automatic dialogue generation without user intervention
- **TR4.4**: System shall integrate user input into conversation context

### TR5: Command Interface
- **TR5.1**: Application shall run via command-line interface (CLI)
- **TR5.2**: Application shall use `adk run` command for execution
- **TR5.3**: System shall accept standard input for user interaction
- **TR5.4**: System shall output to standard output (stdout)

### TR6: Configuration Management
- **TR6.1**: System shall use `.env` file for API key and configuration management
- **TR6.2**: Configuration shall include:
  - API authentication (Google AI Studio or Vertex AI)
  - Model selection
  - Conversation parameters (turn count, pause duration, etc.)
  - Persona configurations

### TR7: Error Handling
- **TR7.1**: System shall handle API errors gracefully
- **TR7.2**: System shall handle invalid user input appropriately
- **TR7.3**: System shall implement retry logic for transient failures
- **TR7.4**: System shall log errors for debugging

### TR8: Persona Configuration System
- **TR8.1**: System shall implement a persona configuration manager to load and manage persona sets
- **TR8.2**: Personas shall be defined in YAML or JSON configuration files
- **TR8.3**: System shall support multiple persona profiles organized by domain/category
- **TR8.4**: Persona configuration shall include: name, role, expertise, personality traits, speaking style, and system instructions
- **TR8.5**: System shall allow persona selection via:
  - Command-line argument (e.g., `--persona-set sports`)
  - Interactive prompt at startup
  - Configuration file default
- **TR8.6**: System shall validate persona configurations on load
- **TR8.7**: System shall provide at least 3 pre-configured persona sets (technology, sports, business)
- **TR8.8**: System shall support custom user-created persona configurations

---

## Non-Functional Requirements

### NFR1: Performance
- **NFR1.1**: System shall generate agent responses within 5 seconds under normal conditions
- **NFR1.2**: System shall handle sessions of at least 30 minutes duration
- **NFR1.3**: System shall maintain context for at least 50 conversation turns

### NFR2: Usability
- **NFR2.1**: User commands shall be intuitive and clearly documented
- **NFR2.2**: System prompts shall clearly indicate when user input is expected
- **NFR2.3**: Error messages shall be user-friendly and actionable

### NFR3: Reliability
- **NFR3.1**: System shall gracefully handle network interruptions
- **NFR3.2**: System shall not crash on unexpected user input
- **NFR3.3**: System shall maintain conversation coherence across session

### NFR4: Maintainability
- **NFR4.1**: Code shall follow Python PEP 8 style guidelines
- **NFR4.2**: Functions and classes shall be well-documented
- **NFR4.3**: Agent personas shall be easily configurable/modifiable
- **NFR4.4**: System shall be modular to allow easy addition of new guest personas

### NFR5: Scalability (Future)
- **NFR5.1**: Architecture shall support addition of more guest personas
- **NFR5.2**: System shall be designed to accommodate voice integration in future versions

---

## System Architecture

### High-Level Component Design

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (CLI)                      │
│                    (Standard Input/Output)                    │
└───────────────────────────────┬─────────────────────────────┘
                                │
                    ┌───────────▼────────────┐
                    │  Persona Configuration │
                    │       Manager          │
                    │  - Load persona sets   │
                    │  - Select by domain    │
                    │  - Validate configs    │
                    └───────────┬────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────┐
│                  Podcast Orchestrator Agent                   │
│  - Manages conversation flow                                  │
│  - Tracks turn order                                          │
│  - Integrates user input                                      │
│  - Controls session lifecycle                                 │
│  - Initializes agents with selected personas                  │
└─────────────┬─────────────────────────────────┬──────────────┘
              │                                 │
    ┌─────────▼──────────┐         ┌───────────▼──────────────┐
    │   Host Agent       │         │   Guest Agents Pool      │
    │  (Dynamic Persona) │         │   (Dynamic Personas)     │
    │                    │         │                          │
    │  Examples:         │◄────────┤  Examples:               │
    │  - Alex Rivera     │         │  - Dr. Maya Chen         │
    │  - Sam Rodriguez   │         │  - Jordan Blake          │
    │  - Dana Morgan     │         │  - Coach Turner          │
    │                    │         │  - Chris Bennett         │
    │  Configurable:     │         │  - Robert Chen           │
    │  - Facilitates     │         │                          │
    │  - Introduces      │         │  Each with domain-       │
    │  - Summarizes      │         │  specific:               │
    │  - Transitions     │         │  - Persona               │
    └────────────────────┘         │  - Instructions          │
                                   │  - Expertise             │
                                   │  - Response style        │
                                   └──────────────────────────┘
              │                                 │
              └─────────────┬───────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│              ADK Framework & Gemini API                       │
│  - Agent orchestration                                        │
│  - LLM inference                                              │
│  - Context management                                         │
└───────────────────────────────────────────────────────────────┘
```

### Key Components

#### 1. Persona Configuration Manager
- **Responsibility**: Load and manage persona configurations for different domains
- **Implementation**: Python module that reads and validates persona configuration files
- **Key Functions**:
  - Load persona sets from YAML/JSON files
  - Validate persona configuration structure
  - Select appropriate persona set based on domain or user choice
  - Provide default persona sets
  - Support custom persona creation
  - Map persona configurations to agent parameters

#### 2. Podcast Orchestrator Agent
- **Responsibility**: Main controller that manages the entire podcast flow
- **Implementation**: Root agent that delegates to host and guest agents
- **Key Functions**:
  - Initialize podcast with user topic and selected persona set
  - Dynamically create agents with configured personas
  - Manage conversation rounds
  - Coordinate turn-taking between agents
  - Handle user input integration
  - Detect and execute exit commands

#### 3. Host Agent (Dynamic Persona)
- **Responsibility**: Podcast host that facilitates discussion
- **Implementation**: ADK Agent with domain-specific host instructions loaded from configuration
- **Persona Examples**:
  - Alex Rivera (Technology) - Tech journalist
  - Sam Rodriguez (Sports) - Sports analyst
  - Dana Morgan (Business) - Business anchor
- **Key Functions**:
  - Open and close podcast
  - Ask questions to guests
  - Facilitate balanced participation
  - Summarize key points
  - Transition between topics

#### 4. Guest Agents (Dynamic Personas)
- **Responsibility**: Provide diverse perspectives on topic
- **Implementation**: Separate ADK Agents with domain-specific instructions loaded from configuration
- **Persona Examples by Domain**:
  - Technology: Dr. Maya Chen (researcher), Jordan Blake (entrepreneur)
  - Sports: Coach Michelle Turner (strategy), Chris Bennett (journalist)
  - Business: Robert Chen (investor), Lisa Park (CEO)
- **Key Functions**:
  - Share viewpoints on topic
  - Respond to host questions
  - Engage with other guests' ideas
  - React to user input

#### 5. Conversation State Manager
- **Responsibility**: Maintain conversation context and state
- **Implementation**: Python class/module
- **State Includes**:
  - Current topic
  - Active persona set
  - Conversation history
  - Current turn/speaker
  - User participation points
  - Session status (active/ending)

#### 6. CLI Interface
- **Responsibility**: Handle user input/output
- **Implementation**: Python command-line interface
- **Key Functions**:
  - Display formatted agent dialogue
  - Capture user input
  - Display prompts and instructions
  - Handle interrupt signals
  - Allow persona set selection

---

## Data Models

### Persona Set Configuration
```python
{
    "set_id": str,  # e.g., "technology", "sports", "business"
    "set_name": str,  # e.g., "Technology Experts"
    "description": str,
    "domains": List[str],  # e.g., ["AI", "tech", "software"]
    "host": PersonaConfig,
    "guests": List[PersonaConfig]  # 2-3 guests
}
```

### Persona Configuration
```python
{
    "id": str,  # e.g., "alex_rivera"
    "name": str,  # Display name: "Alex Rivera"
    "role": "host" | "guest",
    "title": str,  # e.g., "Tech Journalist & Host"
    "personality_traits": List[str],  # e.g., ["enthusiastic", "curious", "articulate"]
    "speaking_style": str,  # Description of how they speak
    "expertise_area": List[str],  # Areas of knowledge
    "background": str,  # Short bio
    "system_instruction": str,  # Full instruction for the LLM
    "model_parameters": {
        "temperature": float,  # 0.0-1.0
        "top_p": float,  # 0.0-1.0
        "top_k": int,
        "max_output_tokens": int
    },
    "example_phrases": List[str]  # Optional: characteristic phrases
}
```

### Conversation State
```python
{
    "topic": str,
    "persona_set_id": str,  # Active persona set
    "status": "initializing" | "active" | "ending" | "completed",
    "current_turn": int,
    "speakers": List[str],
    "active_personas": {
        "host": PersonaConfig,
        "guests": List[PersonaConfig]
    },
    "history": List[Message],
    "user_engaged": bool
}
```

### Message
```python
{
    "speaker": str,  # "host", "guest_1", "guest_2", "user"
    "persona_id": str,  # e.g., "alex_rivera", "maya_chen"
    "persona_name": str,  # Display name: "Alex Rivera"
    "content": str,
    "timestamp": datetime,
    "turn_number": int
}
```

---

## API Specifications

### Agent Configuration

#### Host Agent Configuration
```python
host_agent = Agent(
    name="host_agent",
    model="gemini-2.5-flash",
    instruction="""You are Alex Rivera, an enthusiastic podcast host.
    Your role is to facilitate engaging discussions by:
    - Asking thoughtful questions
    - Ensuring all guests contribute
    - Keeping conversation on topic
    - Creating smooth transitions
    - Summarizing key insights
    
    Be warm, curious, and articulate. Make guests and listeners feel welcome.""",
    description="Podcast host facilitating the discussion"
)
```

#### Guest Agent Configuration Example
```python
guest_agent_maya = Agent(
    name="guest_maya",
    model="gemini-2.5-flash",
    instruction="""You are Dr. Maya Chen, an academic researcher.
    Your perspective is analytical and evidence-based. You:
    - Reference research and data when relevant
    - Think theoretically about problems
    - Ask clarifying questions
    - Value precision and accuracy
    
    Speak thoughtfully and back up claims with reasoning.""",
    description="Academic guest providing research-based insights"
)
```

#### Guest Agent Configuration Example - Jordan Blake
```python
guest_agent_jordan = Agent(
    name="guest_jordan",
    model="gemini-2.5-flash",
    instruction="""You are Jordan Blake, a serial entrepreneur.
    Your perspective is practical and action-oriented. You:
    - Share concrete examples from your business experience
    - Focus on implementation and real-world application
    - Use business analogies and metaphors
    - Value results and measurable outcomes
    
    Be direct, decisive, and pragmatic in your responses.""",
    description="Entrepreneurial guest providing practical insights"
)
```

### Model Configuration Parameters

#### Recommended Parameters by Persona

**Host Agent (Alex Rivera)**
```python
{
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 500
}
```
*Higher temperature for more varied facilitation styles and natural conversation flow*

**Guest Agent - Academic (Dr. Maya Chen)**
```python
{
    "temperature": 0.6,
    "top_p": 0.85,
    "top_k": 30,
    "max_output_tokens": 600
}
```
*Lower temperature for more consistent, thoughtful academic responses*

**Guest Agent - Entrepreneur (Jordan Blake)**
```python
{
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 35,
    "max_output_tokens": 500
}
```
*Moderate temperature for practical yet creative business insights*

---

## Persona Configuration Files

### Configuration File Format (YAML)

#### personas/technology.yaml
```yaml
set_id: technology
set_name: "Technology Experts"
description: "AI and technology discussion experts"
domains:
  - technology
  - AI
  - software
  - innovation

host:
  id: alex_rivera
  name: "Alex Rivera"
  role: host
  title: "Tech Journalist & Podcast Host"
  personality_traits:
    - enthusiastic
    - curious
    - articulate
    - engaging
  speaking_style: "Warm and welcoming with natural transitions. Uses thoughtful questions to drive discussion."
  expertise_area:
    - technology trends
    - AI and machine learning
    - digital transformation
    - innovation
  background: "Experienced podcast host with a background in technology journalism. Passionate about making complex tech topics accessible."
  system_instruction: |
    You are Alex Rivera, an enthusiastic tech podcast host with a journalism background.
    
    Your role is to:
    - Welcome listeners and introduce the topic warmly
    - Ask probing questions that reveal insights
    - Ensure all guests contribute meaningfully
    - Create smooth transitions between topics
    - Summarize key points periodically
    - Keep conversation accessible yet substantive
    
    Your style:
    - Warm, curious, and articulate
    - Use phrases like "That's fascinating...", "Let's dig deeper...", "Building on that..."
    - Make guests and listeners feel welcome
    - Bridge between technical and accessible language
    
    Keep responses conversational and concise (2-4 sentences typically).
  model_parameters:
    temperature: 0.8
    top_p: 0.9
    top_k: 40
    max_output_tokens: 500
  example_phrases:
    - "That's a fascinating perspective..."
    - "Let's dig deeper into that..."
    - "I love how you framed that..."
    - "To our listeners wondering about..."

guests:
  - id: maya_chen
    name: "Dr. Maya Chen"
    role: guest
    title: "AI Researcher & Academic"
    personality_traits:
      - analytical
      - thoughtful
      - evidence-based
      - precise
    speaking_style: "Thoughtful and measured. References research and data. Values accuracy and nuance."
    expertise_area:
      - AI ethics
      - machine learning research
      - technology adoption
      - social impacts of AI
    background: "PhD in Computer Science. University researcher specializing in AI ethics and social impacts of technology."
    system_instruction: |
      You are Dr. Maya Chen, an academic AI researcher with expertise in ethics and social impacts.
      
      Your perspective is:
      - Analytical and evidence-based
      - Grounded in research and data
      - Theoretical and frameworks-oriented
      - Nuanced and precise
      
      Your style:
      - Reference studies when relevant: "Research from MIT shows...", "Studies indicate..."
      - Think in frameworks and models
      - Ask clarifying questions
      - Value precision: "Based on the data...", "The research is clear that..."
      - Consider multiple variables and complexity
      
      Keep responses substantive but conversational (2-5 sentences).
    model_parameters:
      temperature: 0.6
      top_p: 0.85
      top_k: 30
      max_output_tokens: 600
    example_phrases:
      - "Studies from MIT have shown..."
      - "From a theoretical standpoint..."
      - "The research is quite clear that..."
      - "We need to consider multiple variables..."
  
  - id: jordan_blake
    name: "Jordan Blake"
    role: guest
    title: "Tech Entrepreneur & Founder"
    personality_traits:
      - practical
      - action-oriented
      - decisive
      - experienced
    speaking_style: "Direct and pragmatic. Shares concrete examples from experience. Focuses on implementation."
    expertise_area:
      - startup building
      - product development
      - AI implementation
      - business strategy
    background: "Serial entrepreneur with multiple successful tech companies. Expert in practical AI implementation."
    system_instruction: |
      You are Jordan Blake, a serial tech entrepreneur with hands-on AI implementation experience.
      
      Your perspective is:
      - Practical and action-oriented
      - Focused on real-world application
      - Results and outcomes driven
      - Implementation-focused
      
      Your style:
      - Share concrete examples: "In my experience...", "We implemented this..."
      - Use business metaphors and analogies
      - Direct and decisive
      - Focus on "what actually works"
      - Value measurable results
      
      Keep responses practical and concise (2-4 sentences typically).
    model_parameters:
      temperature: 0.7
      top_p: 0.9
      top_k: 35
      max_output_tokens: 500
    example_phrases:
      - "In my experience..."
      - "Here's what actually works..."
      - "We implemented this at my company..."
      - "The practical reality is..."
```

#### personas/sports.yaml
```yaml
set_id: sports
set_name: "Sports Analysts"
description: "Sports discussion and analysis experts"
domains:
  - sports
  - athletics
  - competition

host:
  id: sam_rodriguez
  name: "Sam Rodriguez"
  role: host
  title: "Sports Analyst & Commentator"
  personality_traits:
    - passionate
    - knowledgeable
    - energetic
    - insightful
  speaking_style: "Energetic and passionate. Deep sports knowledge. Makes analysis accessible."
  expertise_area:
    - sports analysis
    - game strategy
    - athlete performance
    - sports history
  background: "Former sports journalist turned podcast host. Deep knowledge across major sports leagues."
  system_instruction: |
    You are Sam "The Analyst" Rodriguez, a passionate sports commentator and podcast host.
    
    Your role is to:
    - Bring energy and enthusiasm to sports discussions
    - Ask insightful questions about strategy and performance
    - Connect current events to sports history
    - Make complex strategy accessible
    - Ensure balanced coverage of different viewpoints
    
    Your style:
    - Passionate and knowledgeable
    - Use sports metaphors and vivid language
    - Reference memorable games and moments
    - Balance statistics with storytelling
    
    Keep responses energetic yet concise (2-4 sentences).
  model_parameters:
    temperature: 0.8
    top_p: 0.9
    top_k: 40
    max_output_tokens: 500

guests:
  - id: michelle_turner
    name: "Coach Michelle Turner"
    role: guest
    title: "Former Athlete & Strategy Expert"
    personality_traits:
      - strategic
      - experienced
      - disciplined
      - insightful
    speaking_style: "Strategic and experience-driven. Focuses on fundamentals and preparation."
    expertise_area:
      - coaching strategy
      - team dynamics
      - athletic performance
      - mental game
    background: "Former professional athlete turned coach. Expert in game strategy and team performance."
    system_instruction: |
      You are Coach Michelle Turner, a former professional athlete and respected coach.
      
      Your perspective is:
      - Strategic and tactical
      - Focused on fundamentals and preparation
      - Experience-based from years of competition
      - Understanding of team dynamics and mental game
      
      Your style:
      - Share insights from coaching experience
      - Emphasize fundamentals and discipline
      - Discuss strategy and game planning
      - Consider psychological aspects
      
      Keep responses strategic and insightful (2-5 sentences).
    model_parameters:
      temperature: 0.7
      top_p: 0.9
      top_k: 35
      max_output_tokens: 550

  - id: chris_bennett
    name: "Chris Bennett"
    role: guest
    title: "Sports Journalist"
    personality_traits:
      - observant
      - analytical
      - well-connected
      - storyteller
    speaking_style: "Journalistic and narrative-driven. Connects stories to broader trends."
    expertise_area:
      - sports journalism
      - league dynamics
      - player stories
      - sports business
    background: "Award-winning sports journalist covering major leagues. Expert storyteller and industry insider."
    system_instruction: |
      You are Chris Bennett, an experienced sports journalist with deep industry connections.
      
      Your perspective is:
      - Journalistic and investigative
      - Story-driven and narrative-focused
      - Understanding of business and media aspects
      - Connected to latest news and trends
      
      Your style:
      - Tell compelling stories about athletes and teams
      - Connect individual stories to broader trends
      - Discuss media and business aspects
      - Provide insider perspective
      
      Keep responses narrative and engaging (2-4 sentences).
    model_parameters:
      temperature: 0.75
      top_p: 0.9
      top_k: 38
      max_output_tokens: 550
```

#### personas/business.yaml
```yaml
set_id: business
set_name: "Business Leaders"
description: "Business and finance discussion experts"
domains:
  - business
  - finance
  - entrepreneurship
  - economics

host:
  id: dana_morgan
  name: "Dana Morgan"
  role: host
  title: "Business News Anchor"
  personality_traits:
    - professional
    - incisive
    - articulate
    - authoritative
  speaking_style: "Professional and polished. Asks sharp questions about strategy and markets."
  expertise_area:
    - business news
    - market analysis
    - corporate strategy
    - economic trends
  background: "Veteran business news anchor. Expert in making complex financial topics understandable."
  system_instruction: |
    You are Dana Morgan, a professional business news anchor and podcast host.
    
    Your role is to:
    - Ask incisive questions about business strategy and markets
    - Connect business decisions to broader economic trends
    - Ensure discussions are substantive yet accessible
    - Challenge assumptions with follow-up questions
    - Summarize key business insights
    
    Your style:
    - Professional and authoritative
    - Sharp and direct questions
    - Focus on strategy, trends, and outcomes
    - Balance optimism with realism
    
    Keep responses professional and focused (2-4 sentences).
  model_parameters:
    temperature: 0.75
    top_p: 0.9
    top_k: 38
    max_output_tokens: 500

guests:
  - id: robert_chen
    name: "Robert Chen"
    role: guest
    title: "Investment Strategist"
    personality_traits:
      - analytical
      - data-driven
      - cautious
      - strategic
    speaking_style: "Analytical and market-focused. Data-driven perspective on investment trends."
    expertise_area:
      - investment strategy
      - market analysis
      - portfolio management
      - risk assessment
    background: "Senior investment strategist with decades of experience. Expert in market dynamics and risk."
    system_instruction: |
      You are Robert Chen, a seasoned investment strategist and market analyst.
      
      Your perspective is:
      - Analytical and data-driven
      - Focused on markets, valuations, and trends
      - Risk-aware and measured
      - Long-term strategic thinking
      
      Your style:
      - Reference market data and trends
      - Discuss risk and opportunity
      - Consider macroeconomic factors
      - Balance bullish and bearish perspectives
      
      Keep responses analytical yet accessible (2-5 sentences).
    model_parameters:
      temperature: 0.65
      top_p: 0.85
      top_k: 32
      max_output_tokens: 600

  - id: lisa_park
    name: "Lisa Park"
    role: guest
    title: "Startup Founder & CEO"
    personality_traits:
      - innovative
      - bold
      - resilient
      - visionary
    speaking_style: "Entrepreneurial and growth-focused. Shares startup building experiences."
    expertise_area:
      - entrepreneurship
      - startup growth
      - fundraising
      - team building
    background: "Serial entrepreneur and CEO. Built and scaled multiple successful startups."
    system_instruction: |
      You are Lisa Park, a successful startup founder and CEO.
      
      Your perspective is:
      - Entrepreneurial and growth-oriented
      - Focused on building and scaling
      - Experience-based from startup journey
      - Innovative and forward-thinking
      
      Your style:
      - Share real startup experiences
      - Discuss growth challenges and solutions
      - Focus on people, culture, and execution
      - Balance vision with practical reality
      
      Keep responses entrepreneurial and engaging (2-4 sentences).
    model_parameters:
      temperature: 0.75
      top_p: 0.9
      top_k: 38
      max_output_tokens: 550
```

### Loading Personas Programmatically

This class will be implemented in `backend/persona/manager.py`:

```python
# backend/persona/manager.py
import yaml
from pathlib import Path
from typing import Dict, List

class PersonaConfigManager:
    """
    Manages persona configurations and creates ADK agents dynamically.
    
    This manager loads persona YAML files and creates agents following
    Google ADK's structure (each agent in its own folder with agent.py).
    """
    
    def __init__(self, config_dir: str = "personas"):
        """
        Initialize the PersonaConfigManager.
        
        Args:
            config_dir: Path to persona configuration directory.
                       Default is "personas" at project root.
        """
        self.config_dir = Path(config_dir)
        self.persona_sets: Dict[str, Dict] = {}
        self.load_all_personas()
    
    def load_all_personas(self):
        """Load all persona configuration files from the config directory"""
        for config_file in self.config_dir.glob("*.yaml"):
            with open(config_file, 'r') as f:
                persona_set = yaml.safe_load(f)
                self.persona_sets[persona_set['set_id']] = persona_set
    
    def get_persona_set(self, set_id: str) -> Dict:
        """Get a specific persona set by ID"""
        if set_id not in self.persona_sets:
            raise ValueError(f"Persona set '{set_id}' not found")
        return self.persona_sets[set_id]
    
    def list_available_sets(self) -> List[str]:
        """List all available persona sets"""
        return list(self.persona_sets.keys())
    
    def select_persona_set(self, domain: str = None) -> Dict:
        """Select appropriate persona set based on domain or user choice"""
        if domain and domain in self.persona_sets:
            return self.persona_sets[domain]
        
        # Interactive selection
        print("Available persona sets:")
        for i, (set_id, persona_set) in enumerate(self.persona_sets.items(), 1):
            print(f"{i}. {persona_set['set_name']} - {persona_set['description']}")
        
        choice = int(input("Select a persona set (number): ")) - 1
        set_id = list(self.persona_sets.keys())[choice]
        return self.persona_sets[set_id]
    
    def create_agent_from_persona(self, persona_config: Dict, model: str = "gemini-2.5-flash"):
        """
        Create an ADK Agent from persona configuration.
        
        Note: In the actual implementation, agents are defined in their own folders
        (backend/agents/host_agent/agent.py, etc.) following Google ADK structure.
        This method provides the configuration that will be used by those agent files.
        
        Args:
            persona_config: Dictionary containing persona configuration
            model: The Gemini model to use (default: gemini-2.5-flash)
            
        Returns:
            Agent instance configured with persona settings
        """
        from google.adk.agents import Agent
        
        return Agent(
            name=persona_config['id'],
            model=model,
            instruction=persona_config['system_instruction'],
            description=f"{persona_config['name']} - {persona_config['title']}",
            temperature=persona_config['model_parameters']['temperature'],
            top_p=persona_config['model_parameters']['top_p'],
            top_k=persona_config['model_parameters']['top_k'],
            max_output_tokens=persona_config['model_parameters']['max_output_tokens'],
        )
```

### Using PersonaConfigManager with Google ADK Agent Structure

Each agent file (e.g., `backend/agents/host_agent/agent.py`) will use the PersonaConfigManager:

```python
# backend/agents/host_agent/agent.py
# Following Google ADK structure: https://google.github.io/adk-docs/get-started/quickstart/

import sys
from pathlib import Path

# Add backend to path to import modules
backend_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_path))

from persona.manager import PersonaConfigManager
from google.adk.agents import Agent

# Initialize persona manager
persona_manager = PersonaConfigManager(config_dir="../../../personas")

# Get the currently selected persona set (could be from config or environment variable)
# For now, default to technology
persona_set = persona_manager.get_persona_set("technology")

# Get the host persona configuration
host_config = persona_set['host']

# Create the host agent using the persona configuration
root_agent = Agent(
    name=host_config['id'],
    model="gemini-2.5-flash",
    description=f"{host_config['name']} - {host_config['title']}",
    instruction=host_config['system_instruction'],
    temperature=host_config['model_parameters']['temperature'],
    top_p=host_config['model_parameters']['top_p'],
)

# Export for ADK to discover
__all__ = ['root_agent']
```

---

## Technology Stack

### Core Framework
- **Google Agent Development Kit (ADK)**: v1.4.2+
- **Python**: 3.9+

### LLM Platform
- **Primary**: Google Gemini 2.5 Flash (via Google AI Studio or Vertex AI)
- **Alternative**: Gemini 2.0 Flash Exp

### Development Tools
- **Environment Management**: python-dotenv for .env configuration
- **CLI**: Built-in Python argparse/input()
- **Testing**: pytest (for unit tests)
- **Version Control**: Git
- **Code Formatting**: black, flake8
- **Type Checking**: mypy (optional)

### Required Dependencies
```
google-adk>=1.4.2
python-dotenv>=1.0.0
pyyaml>=6.0
```

### Development Dependencies
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

### Python Package Requirements (requirements.txt)
```
google-adk>=1.4.2
python-dotenv>=1.0.0
pyyaml>=6.0
```

### Development Requirements (requirements-dev.txt)
```
-r requirements.txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
```

---

## Implementation Phases

### Phase 1: MVP (Minimum Viable Product) - Week 1-2
**Goal**: Basic working podcast with configurable personas

**Tasks**:
- Set up ADK project structure
  - Initialize ADK project with `adk init` in the root directory
  - Configure `.env` with API credentials
  - Create project directory structure (backend/, database/, ui/, personas/)
  - Create `backend/`, `database/`, `ui/`, and `personas/` directories
- **Implement Persona Configuration System**
  - Create persona configuration manager (`backend/persona/manager.py`)
  - Implement YAML loader for persona files (`backend/persona/loader.py`)
  - Create validation logic for persona configs (`backend/persona/validator.py`)
  - Create default persona sets:
    - `personas/technology.yaml`
    - `personas/sports.yaml` (optional for Phase 1)
- **Implement ADK agents following Google structure**
  - Create orchestrator agent folder: `backend/agents/orchestrator/`
    - `backend/agents/orchestrator/__init__.py`
    - `backend/agents/orchestrator/agent.py`
  - Create host agent folder: `backend/agents/host_agent/`
    - `backend/agents/host_agent/__init__.py`
    - `backend/agents/host_agent/agent.py`
  - Create guest agents folder: `backend/agents/guest_agents/`
    - `backend/agents/guest_agents/__init__.py`
    - `backend/agents/guest_agents/agent.py`
- Implement dynamic agent creation
  - Create agents from loaded persona configurations
  - Map persona configs to ADK Agent parameters
  - Test individual agent creation with different personas
- Create conversation orchestrator
  - Implement conversation flow logic in orchestrator agent
  - Basic turn rotation between host and guests
  - Simple state tracking with persona set info
- Implement CLI interface
  - Create main entry point (`backend/main.py`)
  - **Add persona set selection (interactive or CLI arg)**
  - Add topic input prompt
  - Format and display agent responses with persona names
- Add basic stop command
  - Detect exit keywords
  - Graceful shutdown
- Test with multiple persona sets
  - Technology topics with tech personas
  - Test persona switching between sessions

**Deliverables**:
- Working Python application using ADK
- Persona configuration system
- At least 2 persona sets (technology + 1 more)
- Basic conversation flow (5-10 turns)
- README with setup instructions
- `.env.example` template

**Success Criteria**:
- Application runs without crashes
- Users can select between persona sets
- All agents respond with distinct voices appropriate to domain
- Persona configurations are loaded correctly
- User can start and stop conversations
- Conversation stays loosely on topic

---

### Phase 2: Enhanced Conversation - Week 3
**Goal**: Improve conversation quality and user interaction

**Tasks**:
- Refine agent personas and system instructions
  - A/B test different instruction formats
  - Add more specific personality traits
  - Include example phrases in instructions
- Implement user participation prompts
  - Add prompts every 3-5 turns
  - Accept user input gracefully
  - Handle empty/skip responses
- Add conversation state management
  - Track conversation history
  - Maintain topic context
  - Store turn count and participants
- Improve turn-taking logic for natural flow
  - Implement dynamic turn allocation
  - Add natural transitions
  - Prevent repetitive patterns
- Add conversation history context
  - Pass relevant history to agents
  - Implement context window management
  - Reference previous points in conversation
- Implement graceful error handling
  - Try/catch for API errors
  - Retry logic with exponential backoff
  - User-friendly error messages
  - Logging for debugging

**Deliverables**:
- Enhanced agent instructions with clearer personas
- User participation features working smoothly
- Improved conversation coherence and natural flow
- Error handling and logging system

**Success Criteria**:
- Agents consistently maintain distinct personas
- Conversations feel natural and engaging
- User can seamlessly join conversations
- Errors are handled without crashes
- Conversations stay on topic for 20+ turns

---

### Phase 3: Polish & Optimization - Week 4
**Goal**: Production-ready application

**Tasks**:
- **Expand persona library**
  - Complete all 3 default persona sets (technology, sports, business)
  - Add optional 3rd guest to persona sets
  - Create template for custom persona creation
  - Document persona creation guide
- Optimize model parameters for each persona
  - Fine-tune temperature, top_p values across all domains
  - Test response quality for each persona
  - Balance creativity vs. consistency
  - Ensure domain-appropriate responses
- Improve CLI formatting and user experience
  - Add color/formatting to output
  - Clear speaker labels with emojis/icons
  - Visual separators between sections
  - Better prompts and instructions
  - Improve persona selection UI
- Add configuration file for easy customization
  - Allow customization of:
    - Default persona set
    - Number of guests (2 or 3)
    - Turn count before user prompt
    - Model parameters
    - Conversation behavior
- Comprehensive testing with various topics
  - Test all persona sets with appropriate topics
  - Test persona switching
  - Test custom persona creation
  - Test edge cases
  - Test with different conversation lengths
  - Test error scenarios
  - Performance testing
- Documentation and examples
  - Complete README with examples from all persona sets
  - Persona creation guide
  - API documentation for extensibility
  - Troubleshooting guide
  - Example conversation transcripts for each domain

**Deliverables**:
- Polished, production-ready application
- 3+ complete persona sets
- Persona creation template and guide
- Configuration documentation
- User guide with example interactions from all domains
- Complete test suite
- Release v1.0

**Success Criteria**:
- Application is stable and reliable
- All persona sets work seamlessly
- Users can easily create custom personas
- Documentation is comprehensive
- Easy for new users to set up and run
- Configurable without code changes
- Test coverage >80%
- Persona distinctiveness verified across all sets

---

## Testing Strategy

### Test Categories

#### Unit Tests
- **Agent initialization and configuration**
  - Test Agent creation with various parameters
  - Verify system instructions are properly set
  - Test persona configuration loading
- **Persona instruction loading**
  - Test loading from configuration files
  - Validate instruction format
  - Test instruction variable substitution
- **Turn-taking logic**
  - Test turn rotation algorithms
  - Verify fair distribution of speaking turns
  - Test edge cases (1 guest, 5 guests, etc.)
- **User input parsing**
  - Test various input formats
  - Validate command detection
  - Test special characters and edge cases
- **Exit command detection**
  - Test all exit command variations
  - Verify case-insensitive matching
  - Test exit at various conversation stages

#### Integration Tests
- **Multi-agent conversation flow**
  - Test complete conversation lifecycle
  - Verify agents interact correctly
  - Test conversation state transitions
- **User input integration into conversation**
  - Test user input at various conversation points
  - Verify agents respond to user appropriately
  - Test context incorporation
- **Session lifecycle (start to end)**
  - Test initialization
  - Test active conversation
  - Test graceful shutdown
  - Test cleanup
- **Error handling scenarios**
  - Test API timeout handling
  - Test network interruption recovery
  - Test invalid API key handling
  - Test rate limit handling

#### User Acceptance Testing
- **Conversation quality with various topics**
  - Test with 10+ diverse topics
  - Rate conversation relevance
  - Evaluate persona consistency
- **Persona distinctiveness and consistency**
  - Blind test: can users identify speakers?
  - Evaluate personality trait manifestation
  - Check for persona drift over long conversations
- **User interaction responsiveness**
  - Test response to user questions
  - Measure acknowledgment quality
  - Evaluate conversation redirection
- **Natural conversation flow**
  - Rate naturalness on 1-10 scale
  - Evaluate transition quality
  - Check for repetitive patterns

### Test Scenarios

#### 1. Happy Path
**Description**: User provides topic, listens to conversation, asks question, stops podcast

**Steps**:
1. Launch application
2. Enter topic: "The future of education"
3. Read 3 conversation rounds (9 turns)
4. At prompt, enter question: "What about rural areas?"
5. Read 2 more conversation rounds
6. Enter "stop" command
7. Read closing message

**Expected Result**: Smooth flow, relevant conversation, appropriate response to user question, graceful exit

---

#### 2. Minimal Participation
**Description**: User provides topic, never participates, stops after several rounds

**Steps**:
1. Launch application
2. Enter topic: "Climate change solutions"
3. At each prompt, press Enter (continue without commenting)
4. Continue for 6 rounds (18 turns)
5. Enter "stop" command

**Expected Result**: Conversation continues naturally without user input, stays on topic, agents maintain engagement

---

#### 3. Heavy Participation
**Description**: User comments after every prompt

**Steps**:
1. Launch application
2. Enter topic: "Artificial intelligence ethics"
3. After each round, enter a comment or question
4. Continue for 5 rounds with 5 user inputs
5. Enter "stop" command

**Expected Result**: Agents consistently acknowledge and incorporate user input, conversation adapts to user's interests

---

#### 4. Edge Cases
**Description**: Test boundary conditions

**Test Cases**:
- **Empty topic**: Press Enter without entering topic
  - Expected: Prompt user again with error message
- **Very long topic**: Enter 500+ character topic description
  - Expected: Accept and summarize appropriately
- **Stop command during introduction**: Enter "stop" during host's opening
  - Expected: Gracefully exit with brief closing
- **Special characters in topic**: "AI & ML: The Future?"
  - Expected: Handle gracefully without errors
- **Multi-line topic**: Enter topic with newlines
  - Expected: Accept and process appropriately

---

#### 5. Error Scenarios
**Description**: Test error handling and recovery

**Test Cases**:
- **Invalid API key**: Set invalid key in `.env`
  - Expected: Clear error message, guidance to fix
- **Network interruption**: Disconnect network during conversation
  - Expected: Error message, retry option, graceful degradation
- **API rate limit**: Trigger rate limit (if possible in test environment)
  - Expected: Pause and retry with exponential backoff
- **Malformed input**: Enter very long string (10,000+ chars)
  - Expected: Truncate or reject with message
- **Interrupted session**: CTRL+C during conversation
  - Expected: Catch interrupt, brief closing, clean exit

---

### Testing Tools & Frameworks

#### Test Execution
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

#### Mock Configuration for Testing
```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_gemini_api():
    """Mock Gemini API for testing without API calls"""
    mock = Mock()
    mock.generate_content.return_value = Mock(
        text="Test response from agent"
    )
    return mock

@pytest.fixture
def sample_conversation_state():
    """Fixture providing sample conversation state"""
    return {
        "topic": "Test Topic",
        "status": "active",
        "current_turn": 3,
        "speakers": ["host", "guest_1", "guest_2"],
        "history": [],
        "user_engaged": False
    }
```

---

### Performance Testing

#### Metrics to Measure
- **Response Time**: Time from API call to response display
  - Target: <5 seconds per agent response
  - Measure: 95th percentile across 100 requests
- **Memory Usage**: Memory footprint during long conversations
  - Target: <500MB for 30-minute session
  - Measure: Peak memory usage
- **Context Window Management**: Handling of long conversation histories
  - Target: Maintain coherence for 50+ turns
  - Measure: Token usage, context truncation behavior

#### Performance Test Scripts
```python
# tests/performance/test_response_time.py
import time
import statistics

def test_agent_response_time():
    """Test agent response time over multiple calls"""
    response_times = []
    
    for i in range(100):
        start = time.time()
        # Make agent call
        agent.respond("Test prompt")
        end = time.time()
        response_times.append(end - start)
    
    avg_time = statistics.mean(response_times)
    p95_time = statistics.quantiles(response_times, n=20)[18]
    
    assert avg_time < 3.0, f"Average response time {avg_time}s exceeds 3s"
    assert p95_time < 5.0, f"P95 response time {p95_time}s exceeds 5s"
```

---

## File Structure

Following Google ADK best practices ([reference](https://google.github.io/adk-docs/get-started/quickstart/)), the project is organized into backend, database, and UI folders:

```
ai-podcast/
├── .env                          # Environment variables (not in git)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore file
├── README.md                     # Main documentation
├── requirements.txt              # Python dependencies (backend)
├── requirements-dev.txt          # Development dependencies
├── pytest.ini                    # Pytest configuration
├── setup.py                      # Package setup
│
├── documentation/
│   ├── PRD.MD                    # Product Requirements Document
│   ├── TECHNICAL_SPECS.MD        # This document
│   ├── USER_GUIDE.md             # User guide
│   └── API.md                    # API documentation
│
├── personas/                     # Persona configuration files
│   ├── technology.yaml           # Tech domain personas
│   ├── sports.yaml               # Sports domain personas
│   ├── business.yaml             # Business domain personas
│   └── custom/                   # User-created custom personas
│       └── example.yaml
│
├── backend/                      # Backend application (ADK agents)
│   ├── __init__.py
│   ├── main.py                   # Main entry point
│   ├── config.py                 # Configuration management
│   │
│   ├── agents/                   # ADK agents (following Google ADK structure)
│   │   ├── __init__.py
│   │   │
│   │   ├── orchestrator/         # Orchestrator agent (Google ADK structure)
│   │   │   ├── __init__.py
│   │   │   └── agent.py          # Orchestrator agent implementation
│   │   │
│   │   ├── host_agent/           # Host agent (Google ADK structure)
│   │   │   ├── __init__.py
│   │   │   └── agent.py          # Host agent implementation
│   │   │
│   │   └── guest_agents/         # Guest agents (Google ADK structure)
│   │       ├── __init__.py
│   │       └── agent.py          # Guest agents implementation
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py       # Conversation state model
│   │   ├── message.py            # Message model
│   │   └── persona.py            # Persona configuration model
│   │
│   ├── persona/
│   │   ├── __init__.py
│   │   ├── manager.py            # Persona configuration manager
│   │   ├── loader.py             # YAML/JSON loader
│   │   └── validator.py          # Configuration validator
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── conversation_service.py  # Conversation management service
│   │   └── state_service.py      # State management service
│   │
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── interface.py          # CLI interface
│   │   └── formatter.py          # Output formatting
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py             # Logging configuration
│       └── error_handler.py      # Error handling utilities
│
├── database/                     # Database related files
│   ├── migrations/               # Database migration scripts
│   ├── schemas/                  # Database schemas
│   └── seeds/                    # Seed data (optional)
│
├── ui/                           # Frontend (future implementation)
│   └── README.md                 # Placeholder for future UI
│
└── tests/
    ├── __init__.py
    ├── conftest.py               # Pytest fixtures
    │
    ├── unit/
    │   ├── test_agents.py
    │   ├── test_models.py
    │   ├── test_persona.py       # Test persona loading
    │   ├── test_services.py
    │   ├── test_cli.py
    │   └── test_utils.py
    │
    ├── integration/
    │   ├── test_conversation_flow.py
    │   ├── test_user_interaction.py
    │   ├── test_persona_switching.py  # Test persona selection
    │   └── test_error_handling.py
    │
    └── performance/
        └── test_response_time.py
```

### Key Structure Notes

1. **Backend/agents structure**: Follows Google ADK best practices where each agent is in its own folder with `__init__.py` and `agent.py` files (as recommended in the [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/))

2. **Backend folder**: Contains all backend Python code including agents, models, services, and utilities

3. **Database folder**: Centralized location for database-related files (migrations, schemas, seeds)

4. **UI folder**: Placeholder for future frontend implementation

5. **Personas folder**: Remains at root level for easy access and configuration

---

## Environment Configuration

### .env File Structure
```bash
# API Configuration
GOOGLE_API_KEY=your_api_key_here
# OR for Vertex AI:
# GOOGLE_CLOUD_PROJECT=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

# Model Configuration
MODEL_NAME=gemini-2.5-flash
# Alternative: gemini-2.0-flash-exp

# Application Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false

# Conversation Configuration
TURNS_BEFORE_USER_PROMPT=3
MAX_CONVERSATION_TURNS=50
ENABLE_THIRD_GUEST=false
```

### .env.example Template
```bash
# API Configuration
# Get your API key from https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_api_key_here

# Model Configuration (default: gemini-2.5-flash)
MODEL_NAME=gemini-2.5-flash

# Application Configuration
LOG_LEVEL=INFO
DEBUG_MODE=false

# Conversation Configuration
TURNS_BEFORE_USER_PROMPT=3
MAX_CONVERSATION_TURNS=50
ENABLE_THIRD_GUEST=false
```

---

## Security Considerations

### API Key Management
- Store API keys in `.env` file only
- Never commit `.env` to version control
- Use `.env.example` for documentation
- Validate API key on application start
- Rotate keys regularly

### Input Validation
- Sanitize user input to prevent injection
- Limit input length to prevent abuse
- Validate commands against whitelist
- Escape special characters in output

### Data Privacy
- Do not log user input verbatim
- Clear conversation history on exit
- Do not persist any user data
- Comply with data privacy regulations

---

## Deployment

### Local Development Setup

**CRITICAL**: This project already has a virtual environment set up at `.venv`. **DO NOT CREATE A NEW ONE**. Always use the existing `.venv` virtual environment.

```bash
# Clone repository
git clone <repository-url>
cd ai-podcast

# IMPORTANT: Virtual environment already exists at .venv
# DO NOT run: python3 -m venv .venv (this will overwrite existing setup)

# Activate the existing virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Verify you're in the correct environment
which python  # Should show path to .venv/bin/python

# Install dependencies (if needed)
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Edit .env with your API key

# Run tests
pytest

# Run application with ADK
# Note: adk run expects agents in individual folders per Google ADK structure
# Navigate to parent of agent folders (backend/agents/)
cd backend/agents
adk run orchestrator  # Run the orchestrator agent

# Or run from project root using main.py
cd ../..
python backend/main.py
```

### Running with ADK Dev UI

According to the [Google ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/), you can use the ADK web interface:

```bash
# From the backend/agents directory (parent of agent folders)
cd backend/agents
adk web

# This will start the dev UI at http://localhost:8000
# You can then select agents from the dropdown menu
```

### Production Considerations
- Use production API keys with appropriate quotas
- Enable error logging and monitoring
- Set up alerting for failures
- Document known issues and workarounds
- Plan for API quota management

---

## Maintenance & Extensibility

### Adding New Guest Personas
1. Create persona configuration in `src/ai_podcast/agents/guest_agents.py`
2. Define system instruction with personality traits
3. Set appropriate model parameters
4. Add persona to orchestrator rotation
5. Test persona distinctiveness
6. Update documentation

### Modifying Conversation Flow
1. Edit orchestrator logic in `src/ai_podcast/agents/orchestrator.py`
2. Update turn-taking algorithm
3. Adjust user prompt frequency
4. Test with various scenarios
5. Update integration tests

### Upgrading ADK Version
1. Review ADK changelog for breaking changes
2. Update `requirements.txt` with new version
3. Update agent initialization code if needed
4. Run full test suite
5. Update documentation with any API changes

---

## Troubleshooting

### Common Issues

#### Issue: "Invalid API Key" Error
**Symptoms**: Application fails to start with authentication error  
**Solution**:
- Verify API key in `.env` file
- Check for extra spaces or quotes
- Ensure API key has necessary permissions
- Generate new key if needed

#### Issue: Slow Response Times
**Symptoms**: Agent responses take >10 seconds  
**Solution**:
- Check network connectivity
- Verify API quota hasn't been exceeded
- Consider using faster model (gemini-2.5-flash)
- Reduce max_output_tokens if very long responses

#### Issue: Agents Sound Similar
**Symptoms**: Can't distinguish between guest personas  
**Solution**:
- Review and enhance system instructions
- Increase temperature differences between agents
- Add more specific personality traits
- Include example phrases in instructions

#### Issue: Conversation Loses Context
**Symptoms**: Agents forget earlier discussion points  
**Solution**:
- Verify conversation history is being passed to agents
- Check context window isn't being truncated too aggressively
- Increase max_conversation_turns if needed
- Implement better context summarization

---

## Monitoring & Logging

### Log Levels
- **DEBUG**: Detailed information for debugging
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical errors requiring immediate attention

### Key Metrics to Monitor
- API call success rate
- Average response time
- Error rate by type
- User session duration
- Turn count per session
- API quota usage

### Logging Example
```python
import logging

logger = logging.getLogger(__name__)

# Log conversation events
logger.info(f"Starting podcast on topic: {topic}")
logger.debug(f"Agent {agent_name} generated response: {response[:50]}...")
logger.warning(f"User prompt timeout after {timeout}s")
logger.error(f"API call failed: {error_message}")
```

---

## API Rate Limiting & Quotas

### Google AI Studio Quotas
- Free tier: 60 requests per minute
- Paid tier: Higher limits based on plan

### Quota Management Strategies
1. **Request Throttling**: Implement rate limiting in application
2. **Exponential Backoff**: Retry failed requests with increasing delays
3. **Quota Monitoring**: Track API usage and alert when approaching limits
4. **Graceful Degradation**: Provide informative messages when quota exceeded

### Example Rate Limiting Implementation
```python
import time
from functools import wraps

class RateLimiter:
    def __init__(self, max_calls=60, time_window=60):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls outside time window
            self.calls = [c for c in self.calls if now - c < self.time_window]
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.time_window - (now - self.calls[0])
                time.sleep(sleep_time)
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-02 | Initial technical specifications |
| 1.1 | 2025-10-02 | Added configurable persona system for domain-specific hosts and guests |
| 1.2 | 2025-10-02 | Reorganized file structure: backend/, database/, ui/; adopted Google ADK agent structure |
| 1.3 | 2025-10-02 | Renamed docs/ folder to documentation/ for better clarity |

---

*End of Technical Specifications Document*

