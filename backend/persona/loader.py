"""Persona Configuration Loader.

This module handles loading persona configurations from YAML files.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class PersonaLoader:
    """Handles loading persona configurations from YAML files."""
    
    def __init__(self, config_dir: str = "personas"):
        """
        Initialize the PersonaLoader.
        
        Args:
            config_dir: Path to persona configuration directory.
                       Default is "personas" at project root.
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(f"Persona config directory not found: {config_dir}")
    
    def load_persona_set(self, set_id: str) -> Dict:
        """
        Load a specific persona set by ID.
        
        Args:
            set_id: The persona set identifier (e.g., "technology", "sports")
            
        Returns:
            dict: Loaded persona set configuration
            
        Raises:
            FileNotFoundError: If persona set file doesn't exist
            yaml.YAMLError: If YAML file is malformed
        """
        config_file = self.config_dir / f"{set_id}.yaml"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Persona set file not found: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                persona_set = yaml.safe_load(f)
                
            logger.info(f"Successfully loaded persona set: {set_id}")
            return persona_set
            
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML file {config_file}: {e}")
            raise yaml.YAMLError(f"Invalid YAML format in {config_file}: {e}")
    
    def load_all_persona_sets(self) -> Dict[str, Dict]:
        """
        Load all persona set files from the config directory.
        
        Returns:
            dict: Dictionary mapping set_id to persona set configuration
            
        Raises:
            yaml.YAMLError: If any YAML file is malformed
        """
        persona_sets = {}
        
        for config_file in self.config_dir.glob("*.yaml"):
            set_id = config_file.stem
            
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    persona_set = yaml.safe_load(f)
                    persona_sets[set_id] = persona_set
                    
                logger.info(f"Loaded persona set: {set_id}")
                
            except yaml.YAMLError as e:
                logger.error(f"Error loading {config_file}: {e}")
                raise yaml.YAMLError(f"Invalid YAML format in {config_file}: {e}")
        
        return persona_sets
    
    def list_available_sets(self) -> List[str]:
        """
        List all available persona set IDs.
        
        Returns:
            list: List of available persona set identifiers
        """
        return [f.stem for f in self.config_dir.glob("*.yaml")]
