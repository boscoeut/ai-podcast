"""Persona Configuration Validator.

This module validates persona configuration structures and data.
"""

from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PersonaValidator:
    """Validates persona configuration structures and data."""
    
    # Required fields for persona set
    REQUIRED_SET_FIELDS = {
        'set_id': str,
        'set_name': str,
        'description': str,
        'host': dict,
        'guests': list
    }
    
    # Required fields for persona configuration
    REQUIRED_PERSONA_FIELDS = {
        'id': str,
        'name': str,
        'role': str,
        'title': str,
        'personality_traits': list,
        'speaking_style': str,
        'expertise_area': list,
        'background': str,
        'system_instruction': str,
        'model_parameters': dict
    }
    
    # Required model parameters
    REQUIRED_MODEL_PARAMS = {
        'temperature': (float, int),
        'top_p': (float, int),
        'top_k': int,
        'max_output_tokens': int
    }
    
    # Valid roles
    VALID_ROLES = ['host', 'guest']
    
    def validate_persona_set(self, persona_set: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a complete persona set configuration.
        
        Args:
            persona_set: Persona set configuration to validate
            
        Returns:
            dict: Validation result with status and any errors
            
        Raises:
            ValueError: If validation fails
        """
        errors = []
        warnings = []
        
        # Validate set-level fields
        for field, field_type in self.REQUIRED_SET_FIELDS.items():
            if field not in persona_set:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(persona_set[field], field_type):
                errors.append(f"Field '{field}' must be of type {field_type.__name__}")
        
        if errors:
            raise ValueError(f"Persona set validation failed: {'; '.join(errors)}")
        
        # Validate host persona
        try:
            host_result = self.validate_persona_config(persona_set['host'], 'host')
            if host_result['status'] == 'error':
                errors.extend(host_result['errors'])
        except ValueError as e:
            errors.append(f"Host validation failed: {str(e)}")
        
        # Validate guest personas
        if not isinstance(persona_set['guests'], list) or len(persona_set['guests']) == 0:
            errors.append("At least one guest persona is required")
        else:
            for i, guest in enumerate(persona_set['guests']):
                try:
                    guest_result = self.validate_persona_config(guest, 'guest')
                    if guest_result['status'] == 'error':
                        errors.extend([f"Guest {i+1}: {err}" for err in guest_result['errors']])
                except ValueError as e:
                    errors.append(f"Guest {i+1} validation failed: {str(e)}")
        
        # Check for duplicate IDs
        all_ids = [persona_set['host']['id']]
        all_ids.extend([guest['id'] for guest in persona_set['guests']])
        if len(all_ids) != len(set(all_ids)):
            errors.append("Duplicate persona IDs found")
        
        if errors:
            return {
                'status': 'error',
                'errors': errors,
                'warnings': warnings
            }
        
        return {
            'status': 'success',
            'warnings': warnings
        }
    
    def validate_persona_config(self, persona_config: Dict[str, Any], expected_role: str = None) -> Dict[str, Any]:
        """
        Validate a single persona configuration.
        
        Args:
            persona_config: Persona configuration to validate
            expected_role: Expected role ('host' or 'guest')
            
        Returns:
            dict: Validation result with status and any errors
        """
        errors = []
        warnings = []
        
        # Validate required fields
        for field, field_type in self.REQUIRED_PERSONA_FIELDS.items():
            if field not in persona_config:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(persona_config[field], field_type):
                errors.append(f"Field '{field}' must be of type {field_type.__name__}")
        
        if errors:
            return {
                'status': 'error',
                'errors': errors,
                'warnings': warnings
            }
        
        # Validate role
        role = persona_config.get('role')
        if role not in self.VALID_ROLES:
            errors.append(f"Invalid role '{role}'. Must be one of: {self.VALID_ROLES}")
        
        if expected_role and role != expected_role:
            errors.append(f"Expected role '{expected_role}' but found '{role}'")
        
        # Validate model parameters
        model_params = persona_config.get('model_parameters', {})
        for param, param_type in self.REQUIRED_MODEL_PARAMS.items():
            if param not in model_params:
                errors.append(f"Missing model parameter: {param}")
            elif not isinstance(model_params[param], param_type):
                if isinstance(param_type, tuple):
                    type_names = [t.__name__ for t in param_type]
                    errors.append(f"Model parameter '{param}' must be one of: {type_names}")
                else:
                    errors.append(f"Model parameter '{param}' must be of type {param_type.__name__}")
        
        # Validate parameter ranges
        if 'temperature' in model_params:
            temp = model_params['temperature']
            if not (0.0 <= temp <= 1.0):
                errors.append("Temperature must be between 0.0 and 1.0")
        
        if 'top_p' in model_params:
            top_p = model_params['top_p']
            if not (0.0 <= top_p <= 1.0):
                errors.append("top_p must be between 0.0 and 1.0")
        
        if 'top_k' in model_params:
            top_k = model_params['top_k']
            if top_k < 1:
                errors.append("top_k must be at least 1")
        
        if 'max_output_tokens' in model_params:
            max_tokens = model_params['max_output_tokens']
            if max_tokens < 1:
                errors.append("max_output_tokens must be at least 1")
        
        # Validate lists are not empty
        if 'personality_traits' in persona_config:
            traits = persona_config['personality_traits']
            if not isinstance(traits, list) or len(traits) == 0:
                errors.append("personality_traits must be a non-empty list")
        
        if 'expertise_area' in persona_config:
            expertise = persona_config['expertise_area']
            if not isinstance(expertise, list) or len(expertise) == 0:
                errors.append("expertise_area must be a non-empty list")
        
        # Check for optional fields
        if 'example_phrases' in persona_config:
            phrases = persona_config['example_phrases']
            if not isinstance(phrases, list):
                warnings.append("example_phrases should be a list")
        
        if errors:
            return {
                'status': 'error',
                'errors': errors,
                'warnings': warnings
            }
        
        return {
            'status': 'success',
            'warnings': warnings
        }
