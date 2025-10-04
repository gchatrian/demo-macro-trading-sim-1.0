"""
Narrative Templates
Functions to build prompts for LLM narrative generation.
"""

from typing import Dict, Any, List


def build_pre_release_prompt(
    release_name: str,
    release_type: str,
    consensus: float,
    release_date: str,
    macro_state: Dict[str, float],
    recent_history: List[Dict[str, Any]]
) -> str:
    """
    Build a prompt for pre-release narrative.
    Generated the day before a release, based on consensus expectations.
    
    Args:
        release_name: Name of the release (e.g., "Non-Farm Payrolls January")
        release_type: Type of release (e.g., "NFP", "GDP", "CPI")
        consensus: Consensus forecast value
        release_date: When the release will occur
        macro_state: Current state of macro variables (growth, inflation, volatility)
        recent_history: Recent historical changes in macro variables
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Format recent history
    history_str = _format_history(recent_history)
    
    # Build regime description
    regime = _describe_regime(macro_state)
    
    prompt = f"""You are a financial market analyst writing a pre-release analysis for institutional investors.

CONTEXT:
- Release: {release_name} ({release_type})
- Scheduled for: {release_date}
- Consensus Forecast: {consensus}

CURRENT MACRO-ECONOMIC STATE:
- Growth: {macro_state['growth']:.2f}%
- Inflation: {macro_state['inflation']:.2f}%
- Market Volatility: {macro_state['volatility']:.2f}
- Regime: {regime}

{history_str}

TASK:
Write a market analysis discussing:
1. What the consensus forecast implies for the economy
2. How this release fits into the current macro environment
3. What market participants should watch for
4. Potential market reactions to beats or misses vs consensus

STYLE GUIDELINES:
- Professional, analytical tone appropriate for institutional investors
- Focus on economic implications and market dynamics
- Approximately 300-400 words
- Use market terminology naturally
- Be specific about numbers and magnitudes when relevant
- No bullet points or lists - write in flowing paragraphs

Write the analysis:"""
    
    return prompt


def build_post_release_prompt(
    release_name: str,
    release_type: str,
    consensus: float,
    actual: float,
    release_date: str,
    macro_state: Dict[str, float],
    new_macro_state: Dict[str, float],
    impact_summary: str
) -> str:
    """
    Build a prompt for post-release narrative.
    Generated immediately after a release, reacting to actual vs consensus.
    
    Args:
        release_name: Name of the release
        release_type: Type of release
        consensus: Consensus forecast
        actual: Actual released value
        release_date: When the release occurred
        macro_state: Macro state before the release
        new_macro_state: Macro state after applying the release impact
        impact_summary: Description of the impact on macro variables
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Calculate surprise
    surprise = actual - consensus
    surprise_pct = (surprise / consensus * 100) if consensus != 0 else 0
    beat_or_miss = "beat" if surprise > 0 else "missed" if surprise < 0 else "matched"
    
    # Calculate changes in macro variables
    growth_change = new_macro_state['growth'] - macro_state['growth']
    inflation_change = new_macro_state['inflation'] - macro_state['inflation']
    volatility_change = new_macro_state['volatility'] - macro_state['volatility']
    
    # Build new regime description
    new_regime = _describe_regime(new_macro_state)
    
    prompt = f"""You are a financial market analyst writing an immediate market reaction analysis.

RELEASE DETAILS:
- Release: {release_name} ({release_type})
- Consensus: {consensus}
- Actual: {actual}
- Surprise: {surprise:+.1f} ({surprise_pct:+.1f}%) - {beat_or_miss} expectations

MACRO-ECONOMIC IMPACT:
Previous State:
- Growth: {macro_state['growth']:.2f}%
- Inflation: {macro_state['inflation']:.2f}%
- Volatility: {macro_state['volatility']:.2f}

New State After Release:
- Growth: {new_macro_state['growth']:.2f}% (change: {growth_change:+.2f})
- Inflation: {new_macro_state['inflation']:.2f}% (change: {inflation_change:+.2f})
- Volatility: {new_macro_state['volatility']:.2f} (change: {volatility_change:+.2f})

Current Regime: {new_regime}

{impact_summary}

TASK:
Write a market reaction analysis covering:
1. Immediate interpretation of the data surprise
2. What this means for the economic narrative
3. Market implications and likely asset class reactions
4. Forward-looking considerations for investors

STYLE GUIDELINES:
- Urgent, immediate tone appropriate for breaking market news
- Professional analysis for institutional investors
- Approximately 300-400 words
- Use market terminology naturally
- Be specific about the magnitude of surprise and impacts
- No bullet points or lists - write in flowing paragraphs

Write the analysis:"""
    
    return prompt


def build_event_prompt(
    event_headline: str,
    event_date: str,
    macro_state: Dict[str, float],
    new_macro_state: Dict[str, float],
    impact_summary: str
) -> str:
    """
    Build a prompt for macro event narrative.
    Generated when a macro-economic or geopolitical event occurs.
    
    Args:
        event_headline: Headline of the macro event
        event_date: When the event occurred
        macro_state: Macro state before the event
        new_macro_state: Macro state after the event
        impact_summary: Description of the event's impact
        
    Returns:
        Formatted prompt string for LLM
    """
    
    # Calculate changes in macro variables
    growth_change = new_macro_state['growth'] - macro_state['growth']
    inflation_change = new_macro_state['inflation'] - macro_state['inflation']
    volatility_change = new_macro_state['volatility'] - macro_state['volatility']
    
    # Build new regime description
    new_regime = _describe_regime(new_macro_state)
    
    prompt = f"""You are a financial market analyst writing commentary on a major macro-economic or geopolitical event.

EVENT:
{event_headline}
Date: {event_date}

MACRO-ECONOMIC IMPACT:
Previous State:
- Growth: {macro_state['growth']:.2f}%
- Inflation: {macro_state['inflation']:.2f}%
- Volatility: {macro_state['volatility']:.2f}

New State After Event:
- Growth: {new_macro_state['growth']:.2f}% (change: {growth_change:+.2f})
- Inflation: {new_macro_state['inflation']:.2f}% (change: {inflation_change:+.2f})
- Volatility: {new_macro_state['volatility']:.2f} (change: {volatility_change:+.2f})

Current Regime: {new_regime}

{impact_summary}

TASK:
Write a market commentary covering:
1. Context and significance of this event
2. Economic and market implications
3. How this changes the macro outlook
4. What investors should watch next

STYLE GUIDELINES:
- Authoritative, analytical tone for institutional investors
- Connect the event to broader economic themes
- Approximately 300-400 words
- Use appropriate economic and market terminology
- Be specific about impacts and magnitudes
- No bullet points or lists - write in flowing paragraphs

Write the commentary:"""
    
    return prompt


def _format_history(history: List[Dict[str, Any]]) -> str:
    """
    Format recent history for inclusion in prompts.
    
    Args:
        history: List of recent macro variable states
        
    Returns:
        Formatted string describing recent history
    """
    if not history or len(history) < 2:
        return "RECENT HISTORY: Limited historical data available."
    
    # Take last few entries (most recent first)
    recent = history[:min(3, len(history))]
    
    history_lines = ["RECENT HISTORY:"]
    for i, record in enumerate(recent):
        cause = record.get('cause_type', 'unknown')
        timestamp = record.get('timestamp', 'unknown')[:10]  # Just date
        
        line = f"- {timestamp}: Growth={record['growth']:.2f}%, Inflation={record['inflation']:.2f}%, Volatility={record['volatility']:.2f}"
        
        if i == 0:
            line += " (current)"
        
        history_lines.append(line)
    
    return "\n".join(history_lines)


def _describe_regime(macro_state: Dict[str, float]) -> str:
    """
    Describe the current macro-economic regime.
    
    Args:
        macro_state: Dictionary with growth, inflation, volatility
        
    Returns:
        String description of the regime
    """
    growth = macro_state['growth']
    inflation = macro_state['inflation']
    volatility = macro_state['volatility']
    
    # Simple regime classification
    if growth > 4.0 and inflation > 4.0:
        return "Boom (high growth with elevated inflation)"
    elif growth > 3.0 and inflation < 3.0:
        return "Goldilocks (strong growth with moderate inflation)"
    elif growth > 3.0 and inflation > 3.0:
        return "Overheating (strong growth with rising inflation pressures)"
    elif growth < 1.0 and inflation < 2.0:
        return "Stagnation (low growth and subdued inflation)"
    elif growth < 1.0 and inflation > 3.0:
        return "Stagflation (low growth with high inflation)"
    elif growth < 0:
        return "Recession (negative growth)"
    else:
        return "Expansion (moderate growth)"


def format_impact_summary(
    impact_growth: float,
    impact_inflation: float,
    impact_volatility: float
) -> str:
    """
    Format a summary of impacts on macro variables.
    
    Args:
        impact_growth: Change in growth
        impact_inflation: Change in inflation
        impact_volatility: Change in volatility
        
    Returns:
        Formatted summary string
    """
    lines = ["IMPACT BREAKDOWN:"]
    
    if impact_growth != 0:
        direction = "boosted" if impact_growth > 0 else "reduced"
        lines.append(f"- Growth outlook {direction} by {abs(impact_growth):.2f}%")
    
    if impact_inflation != 0:
        direction = "increased" if impact_inflation > 0 else "decreased"
        lines.append(f"- Inflation pressure {direction} by {abs(impact_inflation):.2f}%")
    
    if impact_volatility != 0:
        direction = "rose" if impact_volatility > 0 else "fell"
        lines.append(f"- Market volatility {direction} by {abs(impact_volatility):.2f} points")
    
    return "\n".join(lines)
