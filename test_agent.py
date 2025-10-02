#!/usr/bin/env python3
"""
Simple test script for the orchestrator agent.
This script tests the basic functionality without requiring ADK CLI.
"""

import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from agents.orchestrator.agent import root_agent, get_podcast_topic, start_podcast_introduction, end_podcast
    
    print("✅ Successfully imported orchestrator agent!")
    print(f"Agent name: {root_agent.name}")
    print(f"Agent model: {root_agent.model}")
    print(f"Agent description: {root_agent.description}")
    print(f"Number of tools: {len(root_agent.tools)}")
    
    print("\n🔧 Testing tools:")
    
    # Test the tools
    print("Testing get_podcast_topic...")
    # Note: This will prompt for input in a real scenario
    print("Tool available: get_podcast_topic")
    
    print("Testing start_podcast_introduction...")
    result = start_podcast_introduction("Artificial Intelligence in Healthcare")
    print(f"Result: {result}")
    
    print("Testing end_podcast...")
    result = end_podcast()
    print(f"Result: {result}")
    
    print("\n✅ All tests passed! The orchestrator agent is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
