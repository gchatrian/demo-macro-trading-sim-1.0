"""
Data Provider
Provides a clean interface for the Controller to access data
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from .database_manager import DatabaseManager, DatabaseError


class DataProviderError(Exception):
    """Raised when data provider operations fail"""
    pass


class DataProvider:
    """
    Provides high-level data access methods for the simulation.
    Abstracts database complexity from the Controller.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the Data Provider.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager
    
    def get_next_event(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """
        Get the next event (release or macro event) that hasn't happened yet.
        Returns the earliest event by date.
        
        Returns:
            Tuple of (event_type, event_data) where event_type is 'release' or 'event'
            Returns None if no future events exist
            
        Raises:
            DataProviderError: If query fails
            
        Example:
            event_type, event_data = provider.get_next_event()
            if event_type == 'release':
                print(f"Next release: {event_data['name']}")
            elif event_type == 'event':
                print(f"Next event: {event_data['headline']}")
        """
        try:
            # Get next economic release
            next_release = self.db.query_with_order(
                'economic_releases',
                order_by='release_date',
                ascending=True,
                limit=1,
                has_happened=False
            )
            
            # Get next macro event
            next_event = self.db.query_with_order(
                'macro_events',
                order_by='event_date',
                ascending=True,
                limit=1,
                has_happened=False
            )
            
            # Compare dates and return earliest
            release_date = None
            event_date = None
            
            if next_release:
                release_date = datetime.fromisoformat(next_release[0]['release_date'].replace('+00', '+00:00'))
            
            if next_event:
                event_date = datetime.fromisoformat(next_event[0]['event_date'].replace('+00', '+00:00'))
            
            # Determine which comes first
            if release_date and event_date:
                if release_date <= event_date:
                    return ('release', next_release[0])
                else:
                    return ('event', next_event[0])
            elif release_date:
                return ('release', next_release[0])
            elif event_date:
                return ('event', next_event[0])
            else:
                return None
                
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get next event: {e}")
    
    def get_all_future_events(self) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Get all future events (releases and macro events) sorted by date.
        
        Returns:
            List of tuples (event_type, event_data) sorted by date
            
        Raises:
            DataProviderError: If query fails
        """
        try:
            # Get all future releases
            releases = self.db.query_with_order(
                'economic_releases',
                order_by='release_date',
                ascending=True,
                has_happened=False
            )
            
            # Get all future events
            events = self.db.query_with_order(
                'macro_events',
                order_by='event_date',
                ascending=True,
                has_happened=False
            )
            
            # Combine and sort by date
            all_events = []
            
            for release in releases:
                date = datetime.fromisoformat(release['release_date'].replace('+00', '+00:00'))
                all_events.append((date, 'release', release))
            
            for event in events:
                date = datetime.fromisoformat(event['event_date'].replace('+00', '+00:00'))
                all_events.append((date, 'event', event))
            
            # Sort by date
            all_events.sort(key=lambda x: x[0])
            
            # Return without the date (just type and data)
            return [(event_type, data) for _, event_type, data in all_events]
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get all future events: {e}")
    
    def get_release_by_id(self, release_id: str) -> Dict[str, Any]:
        """
        Get economic release details by ID.
        
        Args:
            release_id: UUID of the release
            
        Returns:
            Release data dictionary
            
        Raises:
            DataProviderError: If release not found or query fails
        """
        try:
            release = self.db.get_by_id('economic_releases', release_id)
            if not release:
                raise DataProviderError(f"Release with ID {release_id} not found")
            return release
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get release: {e}")
    
    def get_event_by_id(self, event_id: str) -> Dict[str, Any]:
        """
        Get macro event details by ID.
        
        Args:
            event_id: UUID of the event
            
        Returns:
            Event data dictionary
            
        Raises:
            DataProviderError: If event not found or query fails
        """
        try:
            event = self.db.get_by_id('macro_events', event_id)
            if not event:
                raise DataProviderError(f"Event with ID {event_id} not found")
            return event
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get event: {e}")
    
    def get_release_type_info(self, release_type_id: str) -> Dict[str, Any]:
        """
        Get release type information (GDP, NFP, PMI, etc.)
        
        Args:
            release_type_id: UUID of the release type
            
        Returns:
            Release type data
            
        Raises:
            DataProviderError: If not found or query fails
        """
        try:
            release_type = self.db.get_by_id('release_types', release_type_id)
            if not release_type:
                raise DataProviderError(f"Release type with ID {release_type_id} not found")
            return release_type
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get release type: {e}")
    
    def mark_release_as_happened(self, release_id: str) -> Dict[str, Any]:
        """
        Mark an economic release as happened.
        
        Args:
            release_id: UUID of the release
            
        Returns:
            Updated release data
            
        Raises:
            DataProviderError: If update fails
        """
        try:
            updated = self.db.update(
                'economic_releases',
                release_id,
                {'has_happened': True}
            )
            return updated
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to mark release as happened: {e}")
    
    def mark_event_as_happened(self, event_id: str) -> Dict[str, Any]:
        """
        Mark a macro event as happened.
        
        Args:
            event_id: UUID of the event
            
        Returns:
            Updated event data
            
        Raises:
            DataProviderError: If update fails
        """
        try:
            updated = self.db.update(
                'macro_events',
                event_id,
                {'has_happened': True}
            )
            return updated
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to mark event as happened: {e}")
    
    def get_macro_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent history of macro variables.
        
        Args:
            limit: Number of records to return (default 10)
            
        Returns:
            List of historical states (most recent first)
            
        Raises:
            DataProviderError: If query fails
        """
        try:
            history = self.db.query_with_order(
                'macro_variables_history',
                order_by='timestamp',
                ascending=False,
                limit=limit
            )
            return history
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get macro history: {e}")
    
    def save_narrative(
        self,
        timestamp: str,
        narrative_type: str,
        content: str,
        reference_type: str,
        reference_id: str
    ) -> Dict[str, Any]:
        """
        Save a generated narrative to the database.
        
        Args:
            timestamp: When the narrative was generated
            narrative_type: 'pre_release', 'post_release', or 'event'
            content: The narrative text
            reference_type: 'release' or 'event'
            reference_id: UUID of the referenced release or event
            
        Returns:
            Saved narrative record
            
        Raises:
            DataProviderError: If save fails
        """
        try:
            narrative = self.db.insert('narratives', {
                'timestamp': timestamp,
                'narrative_type': narrative_type,
                'content': content,
                'reference_type': reference_type,
                'reference_id': reference_id
            })
            return narrative
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to save narrative: {e}")
    
    def get_narratives_for_reference(
        self,
        reference_type: str,
        reference_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all narratives associated with a specific release or event.
        
        Args:
            reference_type: 'release' or 'event'
            reference_id: UUID of the release or event
            
        Returns:
            List of narrative records
            
        Raises:
            DataProviderError: If query fails
        """
        try:
            narratives = self.db.query(
                'narratives',
                reference_type=reference_type,
                reference_id=reference_id
            )
            return narratives
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get narratives: {e}")
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about the simulation data.
        
        Returns:
            Dictionary with counts of various entities
            
        Example:
            stats = provider.get_statistics()
            print(f"Total releases: {stats['total_releases']}")
        """
        try:
            stats = {
                'total_releases': len(self.db.query('economic_releases')),
                'future_releases': len(self.db.query('economic_releases', has_happened=False)),
                'total_events': len(self.db.query('macro_events')),
                'future_events': len(self.db.query('macro_events', has_happened=False)),
                'history_records': len(self.db.query('macro_variables_history')),
                'narratives_generated': len(self.db.query('narratives'))
            }
            return stats
            
        except DatabaseError as e:
            raise DataProviderError(f"Failed to get statistics: {e}")
