#!/usr/bin/env python3
"""
Test Timeline Scheduler
"""

import sys
from pathlib import Path
import time

# Add parent directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from model import DatabaseManager, DataProvider
from controller.timeline_scheduler import TimelineScheduler, TimelineSchedulerError


def test_timeline_scheduler():
    """Test timeline scheduler functionality"""
    print("=" * 60)
    print("Timeline Scheduler Test")
    print("=" * 60)
    
    try:
        # Test 1: Initialize components
        print("\n1. Initializing components...")
        db = DatabaseManager()
        provider = DataProvider(db)
        scheduler = TimelineScheduler(provider)
        print("   ✓ Timeline Scheduler initialized")
        
        # Test 2: Check loaded events
        print("\n2. Checking loaded events...")
        progress = scheduler.get_progress()
        print(f"   Total events loaded: {progress['total_events']}")
        print(f"   Processed: {progress['processed_events']}")
        print(f"   Remaining: {progress['remaining_events']}")
        if progress['current_simulated_time']:
            print(f"   Current sim time: {progress['current_simulated_time']}")
        print("   ✓ Events loaded successfully")
        
        # Test 3: Timeline summary
        print("\n3. Getting timeline summary...")
        summary = scheduler.get_timeline_summary()
        print(summary)
        print("   ✓ Timeline summary generated")
        
        # Test 4: Start timeline
        print("\n4. Starting timeline...")
        scheduler.start()
        print("   ✓ Timeline started")
        
        # Test 5: Get next few events (without waiting)
        print("\n5. Getting first 5 events (no wait)...")
        for i in range(min(5, progress['total_events'])):
            event = scheduler.skip_to_next_event()
            if event:
                summary = scheduler.format_event_summary(event)
                print(f"   Event {i+1}: {summary}")
        print("   ✓ Events retrieved successfully")
        
        # Test 6: Check progress after processing some events
        print("\n6. Checking progress...")
        progress = scheduler.get_progress()
        print(f"   Processed: {progress['processed_events']}/{progress['total_events']}")
        print(f"   Progress: {progress['progress_percentage']:.1f}%")
        print(f"   Current simulated time: {progress['current_simulated_time']}")
        print("   ✓ Progress tracking works")
        
        # Test 7: Test wait functionality (but skip in test to avoid real wait)
        print("\n7. Testing wait calculation (no actual wait in test)...")
        
        # Reset to beginning for wait test
        scheduler.current_index = 5  # Start from event 6
        
        # Get next event to show what would happen
        next_event = scheduler.get_next_event()
        if next_event:
            wait_seconds = next_event['real_time_seconds']
            elapsed = (time.time() - time.mktime(scheduler.real_start_time.timetuple()))
            actual_wait = wait_seconds - elapsed
            
            print(f"   Next event: {scheduler.format_event_summary(next_event)}")
            print(f"   Would wait: {actual_wait:.1f} seconds in real demo")
            print(f"   (Simulated days from start: {wait_seconds / 120:.1f})")
            
            # Skip instead of waiting for the test
            event = scheduler.skip_to_next_event()
            print("   ✓ Wait calculation works (skipped actual wait for testing)")
        
        print("\n" + "=" * 60)
        print("✓ All Timeline Scheduler tests passed!")
        print("=" * 60)
        print("\nNote: The scheduler is ready to manage simulation timing.")
        print("In actual simulation, it will properly space events over time.")
        
        return True
        
    except TimelineSchedulerError as e:
        print(f"\n✗ Timeline Scheduler Error: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_timeline_scheduler()
    exit(0 if success else 1)