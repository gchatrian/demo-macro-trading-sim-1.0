"""
Configuration package for the Macro Trading Simulator.
"""

from .settings import settings, get_settings, ConfigurationError

__all__ = ['settings', 'get_settings', 'ConfigurationError']
