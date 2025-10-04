"""Persona Configuration Manager.

This module manages persona configurations and creates ADK agents dynamically.
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging

from .loader import PersonaLoader
from .validator import PersonaValidator

logger = logging.getLogger(__name__)


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
        self.loader = PersonaLoader(str(self.config_dir))
        self.validator = PersonaValidator()
        self.load_all_personas()
    
    def load_all_personas(self):
        """Load all persona configuration files from the config directory."""
        try:
            self.persona_sets = self.loader.load_all_persona_sets()
            
            # Validate all loaded persona sets
            for set_id, persona_set in self.persona_sets.items():
                try:
                    validation_result = self.validator.validate_persona_set(persona_set)
                    if validation_result['status'] == 'error':
                        logger.error(f"Validation failed for persona set '{set_id}': {validation_result['errors']}")
                        # Remove invalid persona set
                        del self.persona_sets[set_id]
                    else:
                        if validation_result['warnings']:
                            logger.warning(f"Validation warnings for '{set_id}': {validation_result['warnings']}")
                        logger.info(f"Successfully validated persona set: {set_id}")
                        
                except ValueError as e:
                    logger.error(f"Validation error for persona set '{set_id}': {e}")
                    # Remove invalid persona set
                    if set_id in self.persona_sets:
                        del self.persona_sets[set_id]
                        
        except Exception as e:
            logger.error(f"Error loading persona sets: {e}")
            raise
    
    def get_persona_set(self, set_id: str) -> Dict:
        """
        Get a specific persona set by ID.
        
        Args:
            set_id: The persona set identifier
            
        Returns:
            dict: Persona set configuration
            
        Raises:
            ValueError: If persona set not found
        """
        if set_id not in self.persona_sets:
            available = list(self.persona_sets.keys())
            raise ValueError(f"Persona set '{set_id}' not found. Available sets: {available}")
        
        return self.persona_sets[set_id]
    
    def list_available_sets(self) -> List[str]:
        """
        List all available persona sets.
        
        Returns:
            list: List of available persona set identifiers
        """
        return list(self.persona_sets.keys())
    
    def select_persona_set(self, domain: str = None) -> Dict:
        """
        Select appropriate persona set based on domain or user choice.
        
        Args:
            domain: Optional domain to match against persona sets
            
        Returns:
            dict: Selected persona set configuration
            
        Raises:
            ValueError: If no persona sets available
        """
        if not self.persona_sets:
            raise ValueError("No persona sets available")
        
        # Try to match domain first
        if domain and domain in self.persona_sets:
            return self.persona_sets[domain]
        
        # Interactive selection
        print("Available persona sets:")
        for i, (set_id, persona_set) in enumerate(self.persona_sets.items(), 1):
            print(f"{i}. {persona_set['set_name']} - {persona_set['description']}")
        
        try:
            choice = int(input("Select a persona set (number): ")) - 1
            set_ids = list(self.persona_sets.keys())
            
            if 0 <= choice < len(set_ids):
                selected_id = set_ids[choice]
                return self.persona_sets[selected_id]
            else:
                raise ValueError(f"Invalid selection. Please choose 1-{len(set_ids)}")
                
        except (ValueError, KeyboardInterrupt) as e:
            raise ValueError(f"Invalid selection: {e}")
    
    def get_host_persona(self, set_id: str) -> Dict:
        """
        Get the host persona configuration for a specific set.
        
        Args:
            set_id: The persona set identifier
            
        Returns:
            dict: Host persona configuration
        """
        persona_set = self.get_persona_set(set_id)
        return persona_set['host']
    
    def get_guest_personas(self, set_id: str) -> List[Dict]:
        """
        Get the guest persona configurations for a specific set.
        
        Args:
            set_id: The persona set identifier
            
        Returns:
            list: List of guest persona configurations
        """
        persona_set = self.get_persona_set(set_id)
        return persona_set['guests']
    
    def get_persona_by_id(self, set_id: str, persona_id: str) -> Optional[Dict]:
        """
        Get a specific persona configuration by ID within a set.
        
        Args:
            set_id: The persona set identifier
            persona_id: The persona identifier
            
        Returns:
            dict: Persona configuration, or None if not found
        """
        persona_set = self.get_persona_set(set_id)
        
        # Check host
        if persona_set['host']['id'] == persona_id:
            return persona_set['host']
        
        # Check guests
        for guest in persona_set['guests']:
            if guest['id'] == persona_id:
                return guest
        
        return None
    
    def reload_persona_set(self, set_id: str):
        """
        Reload a specific persona set from disk.
        
        Args:
            set_id: The persona set identifier to reload
        """
        try:
            persona_set = self.loader.load_persona_set(set_id)
            validation_result = self.validator.validate_persona_set(persona_set)
            
            if validation_result['status'] == 'success':
                self.persona_sets[set_id] = persona_set
                logger.info(f"Successfully reloaded persona set: {set_id}")
            else:
                logger.error(f"Failed to reload persona set '{set_id}': {validation_result['errors']}")
                raise ValueError(f"Validation failed: {validation_result['errors']}")
                
        except Exception as e:
            logger.error(f"Error reloading persona set '{set_id}': {e}")
            raise
    
    def get_persona_set_info(self, set_id: str) -> Dict:
        """
        Get summary information about a persona set.
        
        Args:
            set_id: The persona set identifier
            
        Returns:
            dict: Summary information about the persona set
        """
        persona_set = self.get_persona_set(set_id)
        
        return {
            'set_id': persona_set['set_id'],
            'set_name': persona_set['set_name'],
            'description': persona_set['description'],
            'domains': persona_set.get('domains', []),
            'host_name': persona_set['host']['name'],
            'host_title': persona_set['host']['title'],
            'guest_count': len(persona_set['guests']),
            'guest_names': [guest['name'] for guest in persona_set['guests']],
            'guest_titles': [guest['title'] for guest in persona_set['guests']]
        }
