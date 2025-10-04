"""
Timeline Scheduler
Manages the timing of events in the simulation, converting simulated time to real time.
"""

import time
from typing import Optional, Dict, Any, Tuple, List
from datetime import datetime, timedelta
from config import get_settings
from model import DataProvider


class TimelineSchedulerError(Exception):
    """Raised when timeline scheduler operations fail"""
    pass


class TimelineScheduler:
    """
    Manages the timeline of the simulation.
    In DEMO mode: 1 simulated day = DEMO_DAY_DURATION seconds (default 120s = 2 minutes)
    """
    
    def __init__(self, data_provider: DataProvider):
        """
        Initialize the Timeline Scheduler.
        
        Args:
            data_provider: DataProvider instance to access events
        """
        self.data_provider = data_provider
        self.settings = get_settings()
        
        # Load all future events at initialization
        self.events = []
        self.current_index = 0
        self.simulation_start_time = None
        self.real_start_time = None
        
        self._load_events()
    
    def _load_events(self):
        """Load all future events from the database and sort by date"""
        try:
            all_events = self.data_provider.get_all_future_events()
            
            # Convert to scheduler format with parsed dates
            self.events = []
            for event_type, event_data in all_events:
                if event_type == 'release':
                    date_field = 'release_date'
                else:
                    date_field = 'event_date'
                
                date_str = event_data[date_field]
                event_datetime = datetime.fromisoformat(date_str.replace('+00', '+00:00'))
                
                self.events.append({
                    'type': event_type,
                    'data': event_data,
                    'sim_datetime': event_datetime
                })
            
            # Sort by datetime (should already be sorted, but ensure it)
            self.events.sort(key=lambda x: x['sim_datetime'])
            
            print(f"✓ Loaded {len(self.events)} events into timeline")
            
            if self.events:
                first = self.events[0]['sim_datetime']
                last = self.events[-1]['sim_datetime']
                print(f"  Timeline spans from {first} to {last}")
            
        except Exception as e:
            raise TimelineSchedulerError(f"Failed to load events: {e}")
    
    def start(self):
        """
        Start the simulation clock.
        Sets the reference points for time conversion.
        """
        if not self.events:
            raise TimelineSchedulerError("No events loaded. Cannot start timeline.")
        
        self.simulation_start_time = self.events[0]['sim_datetime']
        self.real_start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print(f"Timeline Started")
        print(f"{'='*60}")
        print(f"Simulation start: {self.simulation_start_time}")
        print(f"Real start: {self.real_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Time compression: 1 day = {self.settings.DEMO_DAY_DURATION} seconds")
        print(f"{'='*60}\n")
    
    def _simulated_time_to_real_time(self, sim_datetime: datetime) -> float:
        """
        Convert a simulated datetime to real seconds from start.
        
        Args:
            sim_datetime: Simulated datetime
            
        Returns:
            Seconds from real_start_time
        """
        if self.simulation_start_time is None:
            raise TimelineSchedulerError("Timeline not started. Call start() first.")
        
        # Calculate simulated time delta from start
        sim_delta = sim_datetime - self.simulation_start_time
        sim_days = sim_delta.total_seconds() / (24 * 3600)
        
        # Convert to real time
        real_seconds = sim_days * self.settings.DEMO_DAY_DURATION
        
        return real_seconds
    
    def _get_current_simulated_time(self) -> datetime:
        """
        Get current simulated time based on elapsed real time.
        
        Returns:
            Current simulated datetime
        """
        if self.real_start_time is None:
            raise TimelineSchedulerError("Timeline not started. Call start() first.")
        
        # Calculate real elapsed time
        real_elapsed = (datetime.now() - self.real_start_time).total_seconds()
        
        # Convert to simulated days
        sim_days = real_elapsed / self.settings.DEMO_DAY_DURATION
        
        # Calculate simulated time
        sim_time = self.simulation_start_time + timedelta(days=sim_days)
        
        return sim_time
    
    def get_next_event(self) -> Optional[Dict[str, Any]]:
        """
        Get the next event to process.
        
        Returns:
            Event dictionary or None if no more events
            Format: {
                'type': 'release' or 'event',
                'data': event data from database,
                'sim_datetime': datetime object,
                'real_time_seconds': seconds from start when event should occur
            }
        """
        if self.current_index >= len(self.events):
            return None
        
        event = self.events[self.current_index]
        
        # Calculate when this event should occur in real time
        real_time_seconds = self._simulated_time_to_real_time(event['sim_datetime'])
        
        return {
            'type': event['type'],
            'data': event['data'],
            'sim_datetime': event['sim_datetime'],
            'real_time_seconds': real_time_seconds
        }
    
    def wait_until_next_event(self) -> Optional[Dict[str, Any]]:
        """
        Wait until the next event should occur, then return it.
        Sleeps if necessary to maintain proper timing.
        
        Returns:
            Next event or None if no more events
        """
        event = self.get_next_event()
        
        if event is None:
            return None
        
        # Calculate how long to wait
        elapsed = (datetime.now() - self.real_start_time).total_seconds()
        wait_time = event['real_time_seconds'] - elapsed
        
        if wait_time > 0:
            # Show countdown for longer waits
            if wait_time > 5:
                print(f"\n⏳ Waiting {wait_time:.1f} seconds until next event...")
                # Sleep in chunks to allow interruption
                while wait_time > 0:
                    sleep_chunk = min(1.0, wait_time)
                    time.sleep(sleep_chunk)
                    wait_time -= sleep_chunk
            else:
                time.sleep(wait_time)
        
        # Move to next event
        self.current_index += 1
        
        return event
    
    def skip_to_next_event(self) -> Optional[Dict[str, Any]]:
        """
        Skip waiting and immediately return the next event.
        Useful for testing or fast-forward mode.
        
        Returns:
            Next event or None if no more events
        """
        event = self.get_next_event()
        
        if event is not None:
            self.current_index += 1
        
        return event
    
    def get_progress(self) -> Dict[str, Any]:
        """
        Get current progress through the timeline.
        
        Returns:
            Dictionary with progress information
        """
        total_events = len(self.events)
        processed_events = self.current_index
        remaining_events = total_events - processed_events
        
        progress_pct = (processed_events / total_events * 100) if total_events > 0 else 0
        
        # Only calculate current simulated time if timeline has started
        if self.real_start_time is not None:
            current_sim_time = self._get_current_simulated_time()
        else:
            current_sim_time = None
        
        return {
            'total_events': total_events,
            'processed_events': processed_events,
            'remaining_events': remaining_events,
            'progress_percentage': progress_pct,
            'current_simulated_time': current_sim_time
        }
    
    def format_event_summary(self, event: Dict[str, Any]) -> str:
        """
        Format an event for display.
        
        Args:
            event: Event dictionary from get_next_event()
            
        Returns:
            Formatted string
        """
        sim_time = event['sim_datetime'].strftime('%Y-%m-%d %H:%M')
        
        if event['type'] == 'release':
            data = event['data']
            return (f"[{sim_time}] ECONOMIC RELEASE: {data['name']} "
                   f"(Consensus: {data['consensus']}, Actual: {data['actual']})")
        else:
            data = event['data']
            return f"[{sim_time}] MACRO EVENT: {data['headline']}"
    
    def get_timeline_summary(self) -> str:
        """
        Get a summary of the entire timeline.
        
        Returns:
            Formatted string with timeline info
        """
        if not self.events:
            return "Timeline is empty"
        
        first_event = self.events[0]['sim_datetime']
        last_event = self.events[-1]['sim_datetime']
        sim_duration = last_event - first_event
        
        # Calculate real duration
        if self.simulation_start_time is not None:
            total_real_seconds = self._simulated_time_to_real_time(last_event)
            real_duration_minutes = total_real_seconds / 60
        else:
            # Calculate without needing start time
            sim_days = sim_duration.total_seconds() / (24 * 3600)
            total_real_seconds = sim_days * self.settings.DEMO_DAY_DURATION
            real_duration_minutes = total_real_seconds / 60
        
        releases = sum(1 for e in self.events if e['type'] == 'release')
        events = sum(1 for e in self.events if e['type'] == 'event')
        
        summary = f"""
Timeline Summary:
  Simulated period: {first_event} to {last_event}
  Simulated duration: {sim_duration.days} days
  Real duration: {real_duration_minutes:.1f} minutes
  Total events: {len(self.events)} ({releases} releases, {events} macro events)
  Time compression: 1 day = {self.settings.DEMO_DAY_DURATION} seconds
"""
        return summary