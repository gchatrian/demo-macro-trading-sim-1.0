"""
Configuration module for the Macro Trading Simulator.
Loads environment variables and defines system constants.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class ConfigurationError(Exception):
    """Raised when required configuration is missing or invalid"""
    pass


class Settings:
    """
    Application settings loaded from environment variables.
    """
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    
    # Simulation Configuration
    DEMO_DAY_DURATION: int  # Duration of 1 simulated day in real seconds
    
    # System Configuration
    NARRATIVE_MAX_TOKENS: int = 600  # ~400 words
    NARRATIVE_TEMPERATURE: float = 0.7
    MODEL_NAME: str = "gpt-4o-mini"
    
    def __init__(self):
        """Initialize settings by loading and validating environment variables"""
        self._load_and_validate()
    
    def _load_and_validate(self):
        """Load environment variables and validate they are present"""
        
        # Load Supabase configuration
        self.SUPABASE_URL = self._get_required_env('SUPABASE_URL')
        self.SUPABASE_SERVICE_ROLE_KEY = self._get_required_env('SUPABASE_SERVICE_ROLE_KEY')
        
        # Load OpenAI configuration
        self.OPENAI_API_KEY = self._get_required_env('OPENAI_API_KEY')
        
        # Load simulation configuration
        demo_duration_str = self._get_required_env('DEMO_DAY_DURATION')
        try:
            self.DEMO_DAY_DURATION = int(demo_duration_str)
            if self.DEMO_DAY_DURATION <= 0:
                raise ValueError("DEMO_DAY_DURATION must be positive")
        except ValueError as e:
            raise ConfigurationError(
                f"Invalid DEMO_DAY_DURATION value '{demo_duration_str}': {e}"
            )
        
        # Validate URLs
        if not self.SUPABASE_URL.startswith('https://'):
            raise ConfigurationError(
                f"SUPABASE_URL must start with 'https://': {self.SUPABASE_URL}"
            )
        
        # Validate API keys format (basic check)
        if len(self.SUPABASE_SERVICE_ROLE_KEY) < 20:
            raise ConfigurationError(
                "SUPABASE_SERVICE_ROLE_KEY appears to be invalid (too short)"
            )
        
        if not self.OPENAI_API_KEY.startswith('sk-'):
            raise ConfigurationError(
                "OPENAI_API_KEY appears to be invalid (should start with 'sk-')"
            )
    
    def _get_required_env(self, key: str) -> str:
        """
        Get required environment variable or raise error.
        
        Args:
            key: Environment variable name
            
        Returns:
            Value of the environment variable
            
        Raises:
            ConfigurationError: If variable is not set or is empty
        """
        value = os.getenv(key)
        
        if value is None or value.strip() == '':
            raise ConfigurationError(
                f"Required environment variable '{key}' is not set. "
                f"Please check your .env file."
            )
        
        # Check for placeholder values
        placeholder_indicators = ['your_', '_here', 'placeholder']
        if any(indicator in value.lower() for indicator in placeholder_indicators):
            raise ConfigurationError(
                f"Environment variable '{key}' appears to contain a placeholder value. "
                f"Please set the actual value in your .env file."
            )
        
        return value.strip()
    
    def get_simulation_config(self) -> dict:
        """
        Get simulation-specific configuration as a dictionary.
        
        Returns:
            Dictionary with simulation parameters
        """
        return {
            'demo_day_duration': self.DEMO_DAY_DURATION,
            'narrative_max_tokens': self.NARRATIVE_MAX_TOKENS,
            'narrative_temperature': self.NARRATIVE_TEMPERATURE,
            'model_name': self.MODEL_NAME
        }
    
    def __repr__(self) -> str:
        """String representation (hides sensitive data)"""
        return (
            f"Settings("
            f"SUPABASE_URL='{self.SUPABASE_URL}', "
            f"DEMO_DAY_DURATION={self.DEMO_DAY_DURATION}, "
            f"MODEL_NAME='{self.MODEL_NAME}'"
            f")"
        )


# Global settings instance
settings = Settings()


# Convenience function for importing
def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings instance with loaded configuration
    """
    return settings
