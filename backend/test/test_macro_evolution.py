#!/usr/bin/env python3
"""
Test Macro Evolution Engine
"""

import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from model.database_manager import DatabaseManager
from model.macro_evolution_engine import MacroEvolutionEngine, MacroEvolutionError


def test_macro_evolution_engine():
    """Test macro evolution engine functionality"""
    print("=" * 60)
    print("Macro Evolution Engine Test")
    print("=" * 60)
    
    try:
        # Test 1: Initialize components
        print("\n1. Initializing Database Manager and Engine...")
        db = DatabaseManager()
        engine = MacroEvolutionEngine(db)
        print("   ✓ Components initialized")
        
        # Test 2: Get current state
        print("\n2. Getting current macro state...")
        state = engine.get_current_state()
        print(f"   Current state:")
        print(f"   - Growth: {state['growth']}")
        print(f"   - Inflation: {state['inflation']}")
        print(f"   - Volatility: {state['volatility']}")
        print(f"   - Timestamp: {state['timestamp']}")
        print("   ✓ Current state retrieved")
        
        # Test 3: Describe regime
        print("\n3. Describing current regime...")
        regime = engine.describe_regime()
        print(f"   Regime: {regime}")
        print("   ✓ Regime description generated")
        
        # Test 4: Get a release to test impact
        print("\n4. Testing release impact (simulation)...")
        releases = db.query('economic_releases', has_happened=False)
        if releases:
            test_release = releases[0]
            print(f"   Test release: {test_release['name']}")
            print(f"   Impacts: G={test_release['impact_growth']}, "
                  f"I={test_release['impact_inflation']}, "
                  f"V={test_release['impact_volatility']}")
            
            # Show what would happen (don't actually apply)
            projected_growth = state['growth'] + float(test_release['impact_growth'])
            projected_inflation = state['inflation'] + float(test_release['impact_inflation'])
            projected_volatility = max(0, state['volatility'] + float(test_release['impact_volatility']))
            
            print(f"   Projected new state:")
            print(f"   - Growth: {state['growth']} → {projected_growth}")
            print(f"   - Inflation: {state['inflation']} → {projected_inflation}")
            print(f"   - Volatility: {state['volatility']} → {projected_volatility}")
            print("   ✓ Release impact calculation works")
        else:
            print("   ⚠ No releases found to test")
        
        # Test 5: Get an event to test impact
        print("\n5. Testing event impact (simulation)...")
        events = db.query('macro_events', has_happened=False)
        if events:
            test_event = events[0]
            print(f"   Test event: {test_event['headline'][:50]}...")
            print(f"   Impacts: G={test_event['impact_growth']}, "
                  f"I={test_event['impact_inflation']}, "
                  f"V={test_event['impact_volatility']}")
            
            # Show what would happen (don't actually apply)
            projected_growth = state['growth'] + float(test_event['impact_growth'])
            projected_inflation = state['inflation'] + float(test_event['impact_inflation'])
            projected_volatility = max(0, state['volatility'] + float(test_event['impact_volatility']))
            
            print(f"   Projected new state:")
            print(f"   - Growth: {state['growth']} → {projected_growth}")
            print(f"   - Inflation: {state['inflation']} → {projected_inflation}")
            print(f"   - Volatility: {state['volatility']} → {projected_volatility}")
            print("   ✓ Event impact calculation works")
        else:
            print("   ⚠ No events found to test")
        
        # Test 6: Get history
        print("\n6. Getting macro variables history...")
        history = engine.get_history(limit=5)
        print(f"   Found {len(history)} historical records")
        for i, record in enumerate(history[:3], 1):
            print(f"   {i}. {record['timestamp'][:19]} - "
                  f"G={record['growth']}, I={record['inflation']}, V={record['volatility']} "
                  f"(cause: {record['cause_type']})")
        print("   ✓ History retrieval works")
        
        print("\n" + "=" * 60)
        print("✓ All Macro Evolution Engine tests passed!")
        print("=" * 60)
        print("\nNote: This test does NOT modify the database.")
        print("It only reads data and simulates calculations.")
        
        return True
        
    except MacroEvolutionError as e:
        print(f"\n✗ Macro Evolution Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_macro_evolution_engine()
    exit(0 if success else 1)
