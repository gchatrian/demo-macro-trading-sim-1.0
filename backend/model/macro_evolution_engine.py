"""
Macro Evolution Engine
Manages the evolution of the three macro variables: Growth, Inflation, Volatility
"""

from typing import Dict, Any, Optional
from datetime import datetime
from .database_manager import DatabaseManager, DatabaseError


class MacroEvolutionError(Exception):
    """Raised when macro evolution operations fail"""
    pass


class MacroEvolutionEngine:
    """
    Manages the evolution of macro-economic variables.
    Applies impacts from releases and events, maintains history.
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the Macro Evolution Engine.
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager
        self._current_state = None
    
    def get_current_state(self) -> Dict[str, float]:
        """
        Get the current state of the three macro variables.
        
        Returns:
            Dictionary with 'growth', 'inflation', 'volatility' keys
            
        Raises:
            MacroEvolutionError: If unable to retrieve state
            
        Example:
            state = engine.get_current_state()
            print(f"Growth: {state['growth']}, Inflation: {state['inflation']}")
        """
        try:
            # Query the most recent entry in macro_variables_history
            history = self.db.query_with_order(
                'macro_variables_history',
                order_by='timestamp',
                ascending=False,
                limit=1
            )
            
            if not history:
                raise MacroEvolutionError(
                    "No macro variables state found in database. "
                    "Database may not be initialized."
                )
            
            latest = history[0]
            self._current_state = {
                'growth': float(latest['growth']),
                'inflation': float(latest['inflation']),
                'volatility': float(latest['volatility']),
                'timestamp': latest['timestamp']
            }
            
            return self._current_state
            
        except DatabaseError as e:
            raise MacroEvolutionError(f"Failed to get current state: {e}")
    
    def apply_release_impact(
        self, 
        release_id: str, 
        timestamp: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Apply the impact of an economic release on macro variables.
        
        Args:
            release_id: UUID of the economic release
            timestamp: Timestamp for the new state (default: now)
            
        Returns:
            New state of macro variables
            
        Raises:
            MacroEvolutionError: If application fails
            
        Example:
            new_state = engine.apply_release_impact(release_id)
        """
        try:
            # Get the release data
            release = self.db.get_by_id('economic_releases', release_id)
            if not release:
                raise MacroEvolutionError(
                    f"Release with ID {release_id} not found"
                )
            
            # Get current state
            current = self.get_current_state()
            
            # Calculate new values
            new_growth = current['growth'] + float(release['impact_growth'])
            new_inflation = current['inflation'] + float(release['impact_inflation'])
            new_volatility = current['volatility'] + float(release['impact_volatility'])
            
            # Ensure volatility doesn't go negative
            new_volatility = max(0.0, new_volatility)
            
            # Set timestamp
            if timestamp is None:
                timestamp = datetime.utcnow().isoformat() + '+00'
            
            # Insert new state into history
            new_state = self.db.insert('macro_variables_history', {
                'timestamp': timestamp,
                'growth': new_growth,
                'inflation': new_inflation,
                'volatility': new_volatility,
                'cause_type': 'release',
                'cause_id': release_id
            })
            
            print(f"✓ Applied release impact: "
                  f"Growth {current['growth']:.2f} → {new_growth:.2f}, "
                  f"Inflation {current['inflation']:.2f} → {new_inflation:.2f}, "
                  f"Volatility {current['volatility']:.2f} → {new_volatility:.2f}")
            
            return {
                'growth': float(new_state['growth']),
                'inflation': float(new_state['inflation']),
                'volatility': float(new_state['volatility']),
                'timestamp': new_state['timestamp']
            }
            
        except DatabaseError as e:
            raise MacroEvolutionError(f"Failed to apply release impact: {e}")
    
    def apply_event_impact(
        self, 
        event_id: str,
        timestamp: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Apply the impact of a macro event on macro variables.
        
        Args:
            event_id: UUID of the macro event
            timestamp: Timestamp for the new state (default: now)
            
        Returns:
            New state of macro variables
            
        Raises:
            MacroEvolutionError: If application fails
            
        Example:
            new_state = engine.apply_event_impact(event_id)
        """
        try:
            # Get the event data
            event = self.db.get_by_id('macro_events', event_id)
            if not event:
                raise MacroEvolutionError(
                    f"Event with ID {event_id} not found"
                )
            
            # Get current state
            current = self.get_current_state()
            
            # Calculate new values
            new_growth = current['growth'] + float(event['impact_growth'])
            new_inflation = current['inflation'] + float(event['impact_inflation'])
            new_volatility = current['volatility'] + float(event['impact_volatility'])
            
            # Ensure volatility doesn't go negative
            new_volatility = max(0.0, new_volatility)
            
            # Set timestamp
            if timestamp is None:
                timestamp = datetime.utcnow().isoformat() + '+00'
            
            # Insert new state into history
            new_state = self.db.insert('macro_variables_history', {
                'timestamp': timestamp,
                'growth': new_growth,
                'inflation': new_inflation,
                'volatility': new_volatility,
                'cause_type': 'event',
                'cause_id': event_id
            })
            
            print(f"✓ Applied event impact: "
                  f"Growth {current['growth']:.2f} → {new_growth:.2f}, "
                  f"Inflation {current['inflation']:.2f} → {new_inflation:.2f}, "
                  f"Volatility {current['volatility']:.2f} → {new_volatility:.2f}")
            
            return {
                'growth': float(new_state['growth']),
                'inflation': float(new_state['inflation']),
                'volatility': float(new_state['volatility']),
                'timestamp': new_state['timestamp']
            }
            
        except DatabaseError as e:
            raise MacroEvolutionError(f"Failed to apply event impact: {e}")
    
    def get_history(
        self, 
        limit: int = 10,
        ascending: bool = False
    ) -> list[Dict[str, Any]]:
        """
        Get recent history of macro variables.
        
        Args:
            limit: Number of records to return
            ascending: Order (default False = most recent first)
            
        Returns:
            List of historical states
            
        Example:
            history = engine.get_history(limit=5)
            for state in history:
                print(f"{state['timestamp']}: Growth={state['growth']}")
        """
        try:
            history = self.db.query_with_order(
                'macro_variables_history',
                order_by='timestamp',
                ascending=ascending,
                limit=limit
            )
            return history
            
        except DatabaseError as e:
            raise MacroEvolutionError(f"Failed to get history: {e}")
    
    def describe_regime(self, state: Optional[Dict[str, float]] = None) -> str:
        """
        Describe the current macro-economic regime based on variables.
        
        Args:
            state: Optional state dict (default: current state)
            
        Returns:
            String description of the regime
            
        Example:
            regime = engine.describe_regime()
            print(regime)  # "Boom: High growth, elevated inflation"
        """
        if state is None:
            state = self.get_current_state()
        
        growth = state['growth']
        inflation = state['inflation']
        volatility = state['volatility']
        
        # Simple regime classification
        if growth > 4.0 and inflation > 4.0:
            return "Boom: High growth with elevated inflation"
        elif growth > 3.0 and inflation < 3.0:
            return "Goldilocks: Strong growth with moderate inflation"
        elif growth > 3.0 and inflation > 3.0:
            return "Overheating: Strong growth with rising inflation pressures"
        elif growth < 1.0 and inflation < 2.0:
            return "Stagnation: Low growth and subdued inflation"
        elif growth < 1.0 and inflation > 3.0:
            return "Stagflation: Low growth with high inflation"
        elif growth < 0:
            return "Recession: Negative growth"
        else:
            return "Expansion: Moderate growth"
