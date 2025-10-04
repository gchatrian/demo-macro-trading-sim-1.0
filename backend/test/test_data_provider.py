#!/usr/bin/env python3
"""
Test Data Provider
"""

import sys
from pathlib import Path

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from model.database_manager import DatabaseManager
from model.data_provider import DataProvider, DataProviderError


def test_data_provider():
    """Test data provider functionality"""
    print("=" * 60)
    print("Data Provider Test")
    print("=" * 60)
    
    try:
        # Test 1: Initialize components
        print("\n1. Initializing Database Manager and Data Provider...")
        db = DatabaseManager()
        provider = DataProvider(db)
        print("   ✓ Components initialized")
        
        # Test 2: Get statistics
        print("\n2. Getting simulation statistics...")
        stats = provider.get_statistics()
        print(f"   Total releases: {stats['total_releases']}")
        print(f"   Future releases: {stats['future_releases']}")
        print(f"   Total events: {stats['total_events']}")
        print(f"   Future events: {stats['future_events']}")
        print(f"   History records: {stats['history_records']}")
        print(f"   Narratives: {stats['narratives_generated']}")
        print("   ✓ Statistics retrieved")
        
        # Test 3: Get next event
        print("\n3. Getting next event...")
        next_event = provider.get_next_event()
        if next_event:
            event_type, event_data = next_event
            if event_type == 'release':
                print(f"   Next event is a RELEASE:")
                print(f"   - Name: {event_data['name']}")
                print(f"   - Date: {event_data['release_date']}")
                print(f"   - Consensus: {event_data['consensus']}")
                print(f"   - Actual: {event_data['actual']}")
            elif event_type == 'event':
                print(f"   Next event is a MACRO EVENT:")
                print(f"   - Headline: {event_data['headline'][:60]}...")
                print(f"   - Date: {event_data['event_date']}")
            print("   ✓ Next event retrieved")
        else:
            print("   ⚠ No future events found")
        
        # Test 4: Get all future events
        print("\n4. Getting all future events (first 5)...")
        all_events = provider.get_all_future_events()
        print(f"   Found {len(all_events)} total future events")
        for i, (event_type, data) in enumerate(all_events[:5], 1):
            if event_type == 'release':
                date = data['release_date']
                name = data['name']
                print(f"   {i}. [{date}] RELEASE: {name}")
            else:
                date = data['event_date']
                headline = data['headline'][:40]
                print(f"   {i}. [{date}] EVENT: {headline}...")
        print("   ✓ All future events retrieved")
        
        # Test 5: Get release by ID
        if next_event and next_event[0] == 'release':
            print("\n5. Getting release details by ID...")
            release_id = next_event[1]['id']
            release = provider.get_release_by_id(release_id)
            print(f"   Retrieved: {release['name']}")
            
            # Get release type info
            release_type = provider.get_release_type_info(release['release_type_id'])
            print(f"   Type: {release_type['name']}")
            print(f"   Description: {release_type['description'][:50]}...")
            print("   ✓ Release details retrieved")
        else:
            print("\n5. Skipping release details test (no release available)")
        
        # Test 6: Get event by ID
        if next_event and next_event[0] == 'event':
            print("\n6. Getting event details by ID...")
            event_id = next_event[1]['id']
            event = provider.get_event_by_id(event_id)
            print(f"   Retrieved: {event['headline'][:50]}...")
            print("   ✓ Event details retrieved")
        else:
            # Get first event from all events
            events = [e for t, e in all_events if t == 'event']
            if events:
                print("\n6. Getting event details by ID...")
                event_id = events[0]['id']
                event = provider.get_event_by_id(event_id)
                print(f"   Retrieved: {event['headline'][:50]}...")
                print("   ✓ Event details retrieved")
            else:
                print("\n6. Skipping event details test (no event available)")
        
        # Test 7: Get macro history
        print("\n7. Getting macro variables history...")
        history = provider.get_macro_history(limit=5)
        print(f"   Found {len(history)} historical records")
        for i, record in enumerate(history[:3], 1):
            print(f"   {i}. {record['timestamp'][:19]} - "
                  f"G={record['growth']}, I={record['inflation']}, V={record['volatility']}")
        print("   ✓ Macro history retrieved")
        
        # Test 8: Get narratives (should be empty initially)
        print("\n8. Checking for existing narratives...")
        if next_event:
            event_type, event_data = next_event
            narratives = provider.get_narratives_for_reference(
                event_type,
                event_data['id']
            )
            print(f"   Found {len(narratives)} narratives for this event")
            print("   ✓ Narrative query works")
        
        print("\n" + "=" * 60)
        print("✓ All Data Provider tests passed!")
        print("=" * 60)
        print("\nNote: This test does NOT modify the database.")
        print("It only reads data to verify the provider works.")
        
        return True
        
    except DataProviderError as e:
        print(f"\n✗ Data Provider Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_data_provider()
    exit(0 if success else 1)
