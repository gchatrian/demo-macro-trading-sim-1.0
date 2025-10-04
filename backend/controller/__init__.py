"""
Controller package for the Macro Trading Simulator.
Orchestrates simulation flow and coordinates components.
"""

from .timeline_scheduler import TimelineScheduler, TimelineSchedulerError
from .terminal_output_manager import TerminalOutputManager

__all__ = [
    'TimelineScheduler', 
    'TimelineSchedulerError',
    'TerminalOutputManager'
]