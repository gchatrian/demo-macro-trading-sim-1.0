#!/usr/bin/env python3
"""
Test database manager module
"""

import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from model.database_manager import DatabaseManager, DatabaseError


def test_database_manager():
    """Test database manager functionality"""
    print("=" * 60)
    print("Database Manager Test")
    print("=" * 60)
    
    try:
        # Test 1: Initialize database manager
        print("\n1. Initializing Database Manager...")
        db = DatabaseManager()
        print("   ✓ Database Manager initialized")
        
        # Test 2: Test connection
        print("\n2. Testing connection...")
        db.test_connection()
        
        # Test 3: Query release_types
        print("\n3. Querying release_types table...")
        release_types = db.query('release_types')
        print(f"   Found {len(release_types)} release types:")
        for rt in release_types:
            print(f"   - {rt['name']}: {rt['description']}")
        print("   ✓ Query successful")
        
        # Test 4: Query economic_releases with filter
        print("\n4. Querying economic_releases (not happened yet)...")
        future_releases = db.query('economic_releases', has_happened=False)
        print(f"   Found {len(future_releases)} future releases")
        if future_releases:
            print(f"   First release: {future_releases[0]['name']} on {future_releases[0]['release_date']}")
        print("   ✓ Filtered query successful")
        
        # Test 5: Query with ordering
        print("\n5. Querying next 3 macro_events ordered by date...")
        next_events = db.query_with_order(
            'macro_events',
            order_by='event_date',
            ascending=True,
            limit=3,
            has_happened=False
        )
        print(f"   Found {len(next_events)} upcoming events:")
        for event in next_events:
            print(f"   - {event['event_date']}: {event['headline'][:50]}...")
        print("   ✓ Ordered query successful")
        
        # Test 6: Query macro_variables_history
        print("\n6. Querying macro_variables_history (initial state)...")
        initial_state = db.query('macro_variables_history', cause_type='initial')
        if initial_state:
            state = initial_state[0]
            print(f"   Initial state:")
            print(f"   - Growth: {state['growth']}")
            print(f"   - Inflation: {state['inflation']}")
            print(f"   - Volatility: {state['volatility']}")
            print("   ✓ Historical query successful")
        else:
            print("   ⚠ No initial state found (database might not be seeded)")
        
        # Test 7: Get by ID (use first release_type)
        print("\n7. Testing get_by_id...")
        if release_types:
            rt_id = release_types[0]['id']
            rt = db.get_by_id('release_types', rt_id)
            print(f"   Retrieved: {rt['name']}")
            print("   ✓ Get by ID successful")
        
        print("\n" + "=" * 60)
        print("✓ All database tests passed!")
        print("=" * 60)
        
        return True
        
    except DatabaseError as e:
        print(f"\n✗ Database Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_database_manager()
    exit(0 if success else 1)
