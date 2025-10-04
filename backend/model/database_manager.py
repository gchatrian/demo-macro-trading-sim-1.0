"""
Database Manager for Supabase interactions.
Handles all database operations and connection management.
"""

from typing import List, Dict, Any, Optional
try:
    from supabase import create_client, Client
except ImportError:
    # Fallback for different supabase versions
    from supabase.client import Client, create_client

from config import get_settings


class DatabaseError(Exception):
    """Raised when database operations fail"""
    pass


class DatabaseManager:
    """
    Manages all interactions with Supabase database.
    Provides methods for querying, inserting, and updating data.
    """
    
    def __init__(self):
        """Initialize database connection"""
        self._client: Optional[Client] = None
        self._connect()
    
    def _connect(self):
        """
        Establish connection to Supabase.
        
        Raises:
            DatabaseError: If connection fails
        """
        try:
            settings = get_settings()
            # Create client with minimal options for compatibility
            self._client = create_client(
                supabase_url=settings.SUPABASE_URL,
                supabase_key=settings.SUPABASE_SERVICE_ROLE_KEY
            )
            print("✓ Database connection established")
        except Exception as e:
            raise DatabaseError(f"Failed to connect to Supabase: {e}")
    
    @property
    def client(self) -> Client:
        """
        Get Supabase client instance.
        
        Returns:
            Supabase client
            
        Raises:
            DatabaseError: If client is not initialized
        """
        if self._client is None:
            raise DatabaseError("Database client not initialized")
        return self._client
    
    def query(self, table: str, **filters) -> List[Dict[str, Any]]:
        """
        Query data from a table with optional filters.
        
        Args:
            table: Table name
            **filters: Optional filters (e.g., has_happened=False)
            
        Returns:
            List of records as dictionaries
            
        Raises:
            DatabaseError: If query fails
            
        Example:
            records = db.query('economic_releases', has_happened=False)
        """
        try:
            query = self.client.table(table).select("*")
            
            # Apply filters
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            raise DatabaseError(f"Query failed on table '{table}': {e}")
    
    def query_with_order(
        self, 
        table: str, 
        order_by: str, 
        ascending: bool = True,
        limit: Optional[int] = None,
        **filters
    ) -> List[Dict[str, Any]]:
        """
        Query data with ordering and optional limit.
        
        Args:
            table: Table name
            order_by: Column to order by
            ascending: Sort order (default True)
            limit: Maximum number of records to return
            **filters: Optional filters
            
        Returns:
            List of records as dictionaries
            
        Raises:
            DatabaseError: If query fails
            
        Example:
            # Get next 5 events ordered by date
            events = db.query_with_order(
                'macro_events', 
                order_by='event_date', 
                ascending=True,
                limit=5,
                has_happened=False
            )
        """
        try:
            query = self.client.table(table).select("*")
            
            # Apply filters
            for key, value in filters.items():
                query = query.eq(key, value)
            
            # Apply ordering
            query = query.order(order_by, desc=not ascending)
            
            # Apply limit
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            raise DatabaseError(
                f"Ordered query failed on table '{table}': {e}"
            )
    
    def get_by_id(self, table: str, record_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single record by ID.
        
        Args:
            table: Table name
            record_id: UUID of the record
            
        Returns:
            Record as dictionary or None if not found
            
        Raises:
            DatabaseError: If query fails
        """
        try:
            response = self.client.table(table).select("*").eq("id", record_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            raise DatabaseError(f"Get by ID failed on table '{table}': {e}")
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new record.
        
        Args:
            table: Table name
            data: Dictionary with column names and values
            
        Returns:
            Inserted record with generated ID
            
        Raises:
            DatabaseError: If insert fails
            
        Example:
            new_record = db.insert('narratives', {
                'timestamp': '2025-01-10 10:00:00+00',
                'narrative_type': 'pre_release',
                'content': 'Market expects...',
                'reference_type': 'release',
                'reference_id': release_id
            })
        """
        try:
            response = self.client.table(table).insert(data).execute()
            
            if response.data:
                return response.data[0]
            
            raise DatabaseError("Insert succeeded but no data returned")
            
        except Exception as e:
            raise DatabaseError(f"Insert failed on table '{table}': {e}")
    
    def update(
        self, 
        table: str, 
        record_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing record by ID.
        
        Args:
            table: Table name
            record_id: UUID of the record to update
            data: Dictionary with column names and new values
            
        Returns:
            Updated record
            
        Raises:
            DatabaseError: If update fails
            
        Example:
            updated = db.update(
                'economic_releases',
                release_id,
                {'has_happened': True}
            )
        """
        try:
            response = (
                self.client.table(table)
                .update(data)
                .eq("id", record_id)
                .execute()
            )
            
            if response.data:
                return response.data[0]
            
            raise DatabaseError("Update succeeded but no data returned")
            
        except Exception as e:
            raise DatabaseError(f"Update failed on table '{table}': {e}")
    
    def update_where(
        self, 
        table: str, 
        data: Dict[str, Any],
        **filters
    ) -> List[Dict[str, Any]]:
        """
        Update multiple records matching filters.
        
        Args:
            table: Table name
            data: Dictionary with column names and new values
            **filters: Conditions for update
            
        Returns:
            List of updated records
            
        Raises:
            DatabaseError: If update fails
            
        Example:
            # Mark all events before a date as happened
            updated = db.update_where(
                'macro_events',
                {'has_happened': True},
                event_date__lt='2025-02-01'
            )
        """
        try:
            query = self.client.table(table).update(data)
            
            # Apply filters
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            return response.data
            
        except Exception as e:
            raise DatabaseError(
                f"Update where failed on table '{table}': {e}"
            )
    
    def execute_rpc(self, function_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute a stored procedure or custom function.
        
        Args:
            function_name: Name of the function
            params: Function parameters
            
        Returns:
            Function result
            
        Raises:
            DatabaseError: If execution fails
        """
        try:
            response = self.client.rpc(function_name, params).execute()
            return response.data
            
        except Exception as e:
            raise DatabaseError(
                f"RPC call failed for function '{function_name}': {e}"
            )
    
    def test_connection(self) -> bool:
        """
        Test database connection by querying release_types.
        
        Returns:
            True if connection works
            
        Raises:
            DatabaseError: If connection test fails
        """
        try:
            # Simple query to test connection
            response = self.client.table('release_types').select("count").execute()
            print("✓ Database connection test successful")
            return True
            
        except Exception as e:
            raise DatabaseError(f"Connection test failed: {e}")
