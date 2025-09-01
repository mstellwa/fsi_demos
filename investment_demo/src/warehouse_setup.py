"""
Warehouse setup for the Thematic Research Demo
"""

import logging
from snowflake.snowpark import Session
from config import WAREHOUSE, CORTEX_SEARCH_WAREHOUSE

logger = logging.getLogger(__name__)

class WarehouseSetup:
    """Creates and manages warehouses for the demo."""
    
    def __init__(self, session: Session):
        self.session = session
        
    def create_warehouses(self):
        """Create all required warehouses for the demo."""
        logger.info("Creating warehouses for the demo...")
        
        warehouses = [
            {
                "name": WAREHOUSE,
                "size": "MEDIUM",
                "purpose": "general compute"
            },
            {
                "name": CORTEX_SEARCH_WAREHOUSE,
                "size": "MEDIUM", 
                "purpose": "Cortex Search services"
            }
        ]
        
        for wh in warehouses:
            try:
                # Create warehouse if it doesn't exist
                logger.info(f"Creating warehouse {wh['name']} (size: {wh['size']}) for {wh['purpose']}...")
                
                self.session.sql(f"""
                    CREATE WAREHOUSE IF NOT EXISTS {wh['name']}
                    WITH 
                        WAREHOUSE_SIZE = '{wh['size']}'
                        AUTO_SUSPEND = 60
                        AUTO_RESUME = TRUE
                        INITIALLY_SUSPENDED = FALSE
                """).collect()
                
                # Grant usage to current role
                current_role = self.session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
                self.session.sql(f"GRANT USAGE ON WAREHOUSE {wh['name']} TO ROLE {current_role}").collect()
                
                logger.info(f"✅ Warehouse {wh['name']} created and ready")
                
            except Exception as e:
                logger.warning(f"Could not create warehouse {wh['name']}: {e}")
                # Try to resume if it exists but is suspended
                try:
                    self.session.sql(f"ALTER WAREHOUSE {wh['name']} RESUME").collect()
                    logger.info(f"✅ Warehouse {wh['name']} resumed")
                except:
                    pass
        
        # Switch to the main compute warehouse
        self.session.sql(f"USE WAREHOUSE {WAREHOUSE}").collect()
        logger.info(f"Using warehouse {WAREHOUSE} for session")
        
        return True
    
    def validate_warehouses(self):
        """Validate that all required warehouses exist and are accessible."""
        logger.info("Validating warehouses...")
        
        required_warehouses = [WAREHOUSE, CORTEX_SEARCH_WAREHOUSE]
        all_valid = True
        
        # Get list of available warehouses
        warehouses = self.session.sql("SHOW WAREHOUSES").collect()
        available_wh = {wh['name']: wh for wh in warehouses}
        
        for wh_name in required_warehouses:
            if wh_name in available_wh:
                wh_info = available_wh[wh_name]
                logger.info(f"✅ {wh_name}: size={wh_info['size']}, state={wh_info['state']}")
            else:
                logger.error(f"❌ {wh_name}: NOT FOUND")
                all_valid = False
        
        return all_valid
