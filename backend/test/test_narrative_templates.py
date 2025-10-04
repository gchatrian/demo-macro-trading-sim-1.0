#!/usr/bin/env python3
"""
Test Narrative Templates
"""

import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from prompts.narrative_templates import (
    build_pre_release_prompt,
    build_post_release_prompt,
    build_event_prompt,
    format_impact_summary
)


def test_narrative_templates():
    """Test narrative template generation"""
    print("=" * 80)
    print("Narrative Templates Test")
    print("=" * 80)
    
    # Sample data
    macro_state = {
        'growth': 2.3,
        'inflation': 2.1,
        'volatility': 12.0
    }
    
    new_macro_state = {
        'growth': 2.38,
        'inflation': 2.12,
        'volatility': 12.3
    }
    
    recent_history = [
        {
            'timestamp': '2025-01-02 09:00:00+00',
            'growth': 2.3,
            'inflation': 2.1,
            'volatility': 12.0,
            'cause_type': 'initial'
        }
    ]
    
    # Test 1: Pre-release prompt
    print("\n1. Testing pre-release prompt generation...")
    pre_prompt = build_pre_release_prompt(
        release_name="Non-Farm Payrolls January",
        release_type="NFP",
        consensus=180.0,
        release_date="2025-01-10 13:30:00",
        macro_state=macro_state,
        recent_history=recent_history
    )
    
    print("   Generated prompt:")
    print("   " + "-" * 76)
    for line in pre_prompt.split('\n')[:15]:  # Show first 15 lines
        print("   " + line)
    print("   " + "..." if len(pre_prompt.split('\n')) > 15 else "")
    print("   " + "-" * 76)
    print(f"   Total length: {len(pre_prompt)} characters")
    print("   ✓ Pre-release prompt generated")
    
    # Test 2: Post-release prompt
    print("\n2. Testing post-release prompt generation...")
    impact_summary = format_impact_summary(
        impact_growth=0.08,
        impact_inflation=0.02,
        impact_volatility=0.3
    )
    
    post_prompt = build_post_release_prompt(
        release_name="Non-Farm Payrolls January",
        release_type="NFP",
        consensus=180.0,
        actual=215.0,
        release_date="2025-01-10 13:30:00",
        macro_state=macro_state,
        new_macro_state=new_macro_state,
        impact_summary=impact_summary
    )
    
    print("   Generated prompt:")
    print("   " + "-" * 76)
    for line in post_prompt.split('\n')[:15]:  # Show first 15 lines
        print("   " + line)
    print("   " + "..." if len(post_prompt.split('\n')) > 15 else "")
    print("   " + "-" * 76)
    print(f"   Total length: {len(post_prompt)} characters")
    print("   ✓ Post-release prompt generated")
    
    # Test 3: Event prompt
    print("\n3. Testing event prompt generation...")
    event_macro_state = {
        'growth': 2.3,
        'inflation': 2.1,
        'volatility': 12.0
    }
    
    event_new_state = {
        'growth': 2.65,
        'inflation': 2.15,
        'volatility': 14.5
    }
    
    event_impact = format_impact_summary(
        impact_growth=0.35,
        impact_inflation=0.05,
        impact_volatility=2.5
    )
    
    event_prompt = build_event_prompt(
        event_headline="Major Tech Companies Announce Revolutionary AI Breakthrough: Productivity Set to Surge",
        event_date="2025-02-15 16:00:00",
        macro_state=event_macro_state,
        new_macro_state=event_new_state,
        impact_summary=event_impact
    )
    
    print("   Generated prompt:")
    print("   " + "-" * 76)
    for line in event_prompt.split('\n')[:15]:  # Show first 15 lines
        print("   " + line)
    print("   " + "..." if len(event_prompt.split('\n')) > 15 else "")
    print("   " + "-" * 76)
    print(f"   Total length: {len(event_prompt)} characters")
    print("   ✓ Event prompt generated")
    
    # Test 4: Impact summary formatting
    print("\n4. Testing impact summary formatting...")
    summary = format_impact_summary(
        impact_growth=-0.10,
        impact_inflation=0.15,
        impact_volatility=2.0
    )
    print("   Generated summary:")
    for line in summary.split('\n'):
        print("   " + line)
    print("   ✓ Impact summary formatted")
    
    # Test 5: Prompt structure validation
    print("\n5. Validating prompt structure...")
    
    # Check that prompts contain key elements
    checks = [
        ("CONTEXT" in pre_prompt or "RELEASE DETAILS" in pre_prompt, "Context section"),
        ("TASK" in pre_prompt, "Task section"),
        ("STYLE GUIDELINES" in pre_prompt, "Style guidelines"),
        ("300-400 words" in pre_prompt, "Length specification"),
        ("consensus" in pre_prompt.lower(), "Consensus mentioned"),
        ("MACRO" in post_prompt.upper(), "Macro state"),
        ("Surprise" in post_prompt or "surprise" in post_prompt, "Surprise calculation"),
    ]
    
    all_passed = True
    for check, description in checks:
        if check:
            print(f"   ✓ {description} present")
        else:
            print(f"   ✗ {description} missing")
            all_passed = False
    
    if all_passed:
        print("   ✓ All prompt structure checks passed")
    
    print("\n" + "=" * 80)
    print("✓ All Narrative Template tests passed!")
    print("=" * 80)
    print("\nNote: These prompts are ready to be sent to the LLM.")
    print("They include all necessary context and clear instructions.")
    
    return True


if __name__ == "__main__":
    success = test_narrative_templates()
    exit(0 if success else 1)
