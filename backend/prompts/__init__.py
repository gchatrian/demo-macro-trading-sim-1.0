"""
Prompts package for the Macro Trading Simulator.
Contains LLM prompt templates and generation logic.
"""

from .narrative_templates import (
    build_pre_release_prompt,
    build_post_release_prompt,
    build_event_prompt,
    format_impact_summary
)

__all__ = [
    'build_pre_release_prompt',
    'build_post_release_prompt',
    'build_event_prompt',
    'format_impact_summary'
]
