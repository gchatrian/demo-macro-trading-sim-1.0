"""
Controller package for the Macro Trading Simulator.
Orchestrates simulation flow and coordinates components.
"""

from .timeline_scheduler import TimelineScheduler, TimelineSchedulerError

__all__ = ['TimelineScheduler', 'TimelineSchedulerError']
