# src/utils/snowpark_session.py
# Snowpark session management for the Frost Markets Intelligence demo

import argparse
from snowflake.snowpark import Session
from config import DemoConfig


def get_snowpark_session(connection_name: str = None) -> Session:
    """
    Creates and returns a Snowpark session using connections.toml.
    
    Args:
        connection_name: Connection name from connections.toml. 
                        If None, uses command-line arg or config default.
    
    Returns:
        Snowpark Session object
    """
    if not connection_name:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--connection_name", 
            type=str, 
            default=DemoConfig.SNOWFLAKE_CONNECTION_NAME,
            help="Connection name from connections.toml file"
        )
        args, _ = parser.parse_known_args()
        connection_name = args.connection_name
    
    try:
        session = Session.builder.config("connection_name", connection_name).create()
        
        # Verify connection and set context
        current_db = session.get_current_database()
        current_schema = session.get_current_schema()
        
        print(f"✅ Snowpark session created successfully")
        print(f"   Connection: {connection_name}")
        print(f"   Database: {current_db}")
        print(f"   Schema: {current_schema}")
        
        return session
        
    except Exception as e:
        print(f"❌ Failed to create Snowpark session: {str(e)}")
        print(f"   Check that connections.toml exists and '{connection_name}' is configured")
        raise


def create_demo_warehouses(session: Session) -> None:
    """
    Creates the demo warehouses for compute and search operations.
    
    Args:
        session: Active Snowpark session
    """
    try:
        print("🏗️  Creating demo warehouses...")
        
        # Create compute warehouse for general operations
        compute_wh_sql = f"""
        CREATE WAREHOUSE IF NOT EXISTS {DemoConfig.COMPUTE_WAREHOUSE}
        WITH WAREHOUSE_SIZE = 'MEDIUM'
        AUTO_SUSPEND = 300
        AUTO_RESUME = TRUE
        COMMENT = 'Frost Markets Intelligence - Compute warehouse for data processing and analysis'
        """
        session.sql(compute_wh_sql).collect()
        print(f"   ✅ Created compute warehouse: {DemoConfig.COMPUTE_WAREHOUSE}")
        
        # Create search warehouse for Cortex Search services
        search_wh_sql = f"""
        CREATE WAREHOUSE IF NOT EXISTS {DemoConfig.SEARCH_WAREHOUSE}
        WITH WAREHOUSE_SIZE = 'MEDIUM'
        AUTO_SUSPEND = 300
        AUTO_RESUME = TRUE
        COMMENT = 'Frost Markets Intelligence - Search warehouse for Cortex Search services'
        """
        session.sql(search_wh_sql).collect()
        print(f"   ✅ Created search warehouse: {DemoConfig.SEARCH_WAREHOUSE}")
        
    except Exception as e:
        print(f"❌ Error creating warehouses: {str(e)}")
        raise


def set_demo_context(session: Session) -> None:
    """
    Sets the database and schema context for the demo.
    
    Args:
        session: Active Snowpark session
    """
    try:
        # Set database context
        session.sql(f"USE DATABASE {DemoConfig.DATABASE_NAME}").collect()
        session.sql(f"USE SCHEMA {DemoConfig.SCHEMAS['RAW_DATA']}").collect()
        session.sql(f"USE WAREHOUSE {DemoConfig.COMPUTE_WAREHOUSE}").collect()
        
        print(f"✅ Demo context set:")
        print(f"   Database: {DemoConfig.DATABASE_NAME}")
        print(f"   Schema: {DemoConfig.SCHEMAS['RAW_DATA']}")
        print(f"   Warehouse: {DemoConfig.COMPUTE_WAREHOUSE}")
        
    except Exception as e:
        print(f"⚠️  Could not set demo context: {str(e)}")
        print("   This is expected if running setup for the first time")


def close_session(session: Session) -> None:
    """
    Safely closes a Snowpark session.
    
    Args:
        session: Snowpark session to close
    """
    try:
        session.close()
        print("✅ Snowpark session closed successfully")
    except Exception as e:
        print(f"⚠️  Error closing session: {str(e)}")
