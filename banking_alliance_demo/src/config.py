"""
Configuration management for SnowBank Intelligence Demo
Handles demo configuration stored in DEMO_CONFIG table and session management
"""

import logging
from typing import Dict, Any, Optional
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException

logger = logging.getLogger(__name__)


class DemoConfig:
    """Manages demo configuration and Snowpark session"""
    
    # Default configuration values
    DEFAULT_CONFIG = {
        'CONNECTION_NAME': 'sfseeurope-mstellwall-aws-us-west3',
        'SCHEMA_NAME': 'BANK_DEMO',
        'MODEL_CLASS': 'claude-4-sonnet',
        'CUSTOMER_COUNT': 5000,
        'LOAN_COUNT': 25000,
        'HISTORY_MONTHS': 24,
        'WAREHOUSE_FOR_BUILD': 'COMPUTE_WH',
        'RESET_STRATEGY': 'TRUNCATE_AND_RESEED',
        'SCENARIO_TOGGLES': 'ALL_ENABLED'
    }
    
    def __init__(self, connection_name: Optional[str] = None):
        """Initialize configuration with optional connection override"""
        self.connection_name = connection_name or self.DEFAULT_CONFIG['CONNECTION_NAME']
        self._session = None
        self._config_cache = {}
        
    @property
    def session(self) -> Session:
        """Get or create Snowpark session"""
        if self._session is None:
            self._session = self._create_session()
        return self._session
    
    def _create_session(self) -> Session:
        """Create Snowpark session using connections.toml"""
        try:
            session = Session.builder.config("connection_name", self.connection_name).create()
            logger.info(f"Created Snowpark session with connection: {self.connection_name}")
            
            # Set default context to our demo database/schema
            try:
                session.sql("USE DATABASE FSI_DEMOS").collect()
                session.sql("USE SCHEMA BANK_DEMO").collect()
                logger.info("Set session context to FSI_DEMOS.BANK_DEMO")
            except Exception as e:
                logger.warning(f"Could not set demo context (objects may not exist yet): {str(e)}")
            
            return session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            raise
    
    def get_config(self, key: str) -> Any:
        """Get configuration value from cache or database"""
        if key in self._config_cache:
            return self._config_cache[key]
            
        # Try to get from database, fallback to default
        try:
            result = self.session.sql(
                f"SELECT VALUE FROM DEMO_CONFIG WHERE KEY = '{key}'"
            ).collect()
            
            if result:
                value = result[0]['VALUE']
                # Convert numeric strings to proper types
                if key in ['CUSTOMER_COUNT', 'LOAN_COUNT', 'HISTORY_MONTHS']:
                    value = int(value)
                self._config_cache[key] = value
                return value
                
        except SnowparkSQLException:
            # Table doesn't exist yet, use default
            pass
            
        # Return default value
        default_value = self.DEFAULT_CONFIG.get(key)
        self._config_cache[key] = default_value
        return default_value
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value in database"""
        # Update cache
        self._config_cache[key] = value
        
        # Update database
        try:
            self.session.sql(f"""
                MERGE INTO DEMO_CONFIG AS target
                USING (SELECT '{key}' AS KEY, '{value}' AS VALUE) AS source
                ON target.KEY = source.KEY
                WHEN MATCHED THEN UPDATE SET VALUE = source.VALUE
                WHEN NOT MATCHED THEN INSERT (KEY, VALUE) VALUES (source.KEY, source.VALUE)
            """).collect()
            
        except SnowparkSQLException as e:
            logger.warning(f"Could not update config in database: {str(e)}")
    
    def initialize_config_table(self) -> None:
        """Initialize DEMO_CONFIG table with default values"""
        try:
            # Create config table if it doesn't exist
            self.session.sql("""
                CREATE TABLE IF NOT EXISTS DEMO_CONFIG (
                    KEY VARCHAR NOT NULL PRIMARY KEY,
                    VALUE VARCHAR NOT NULL
                )
            """).collect()
            
            # Insert default values
            for key, value in self.DEFAULT_CONFIG.items():
                self.session.sql(f"""
                    INSERT INTO DEMO_CONFIG (KEY, VALUE) 
                    SELECT '{key}', '{value}'
                    WHERE NOT EXISTS (SELECT 1 FROM DEMO_CONFIG WHERE KEY = '{key}')
                """).collect()
                
            logger.info("Initialized DEMO_CONFIG table with default values")
            
        except Exception as e:
            logger.error(f"Failed to initialize config table: {str(e)}")
            raise
    
    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values"""
        config = {}
        for key in self.DEFAULT_CONFIG.keys():
            config[key] = self.get_config(key)
        return config
    
    def close_session(self) -> None:
        """Close Snowpark session"""
        if self._session:
            self._session.close()
            self._session = None
            logger.info("Closed Snowpark session")
