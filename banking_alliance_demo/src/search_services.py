"""
Cortex Search Services management for SnowBank Intelligence Demo
Creates and manages the three required search services for different document types
"""

import logging
from typing import List, Dict
from snowflake.snowpark.exceptions import SnowparkSQLException

from .config import DemoConfig

logger = logging.getLogger(__name__)


class SearchServiceManager:
    """Manages Cortex Search services creation and configuration"""
    
    # Search service definitions
    SEARCH_SERVICES = {
        'INTERNAL_POLICY_SEARCH_SVC': {
            'source_query': "SELECT DOC_ID, TITLE, CONTENT_MD FROM DOCUMENTS WHERE DOC_TYPE = 'POLICY'",
            'search_column': 'CONTENT_MD',
            'id_column': 'DOC_ID',
            'title_column': 'TITLE',
            'description': 'Indexed credit policy content for mitigation options'
        },
        'CLIENT_AND_MARKET_INTEL_SVC': {
            'source_query': "SELECT DOC_ID, TITLE, CONTENT_MD FROM DOCUMENTS WHERE DOC_TYPE IN ('CRM_NOTE','NEWS')",
            'search_column': 'CONTENT_MD',
            'id_column': 'DOC_ID', 
            'title_column': 'TITLE',
            'description': 'CRM notes and market news for risk signals and context'
        },
        'REPORTING_AND_COMPLIANCE_SVC': {
            'source_query': "SELECT DOC_ID, TITLE, CONTENT_MD FROM DOCUMENTS WHERE DOC_TYPE IN ('ANNUAL_REPORT','LOAN_DOC','THIRD_PARTY')",
            'search_column': 'CONTENT_MD',
            'id_column': 'DOC_ID',
            'title_column': 'TITLE', 
            'description': 'Loan documents and third-party opinions for project descriptions and eligibility'
        }
    }
    
    # Pre-warming queries for each service
    PREWARMING_QUERIES = {
        'INTERNAL_POLICY_SEARCH_SVC': [
            "forbearance",
            "payment holiday", 
            "restructuring",
            "LTV breach"
        ],
        'CLIENT_AND_MARKET_INTEL_SVC': [
            "algae bloom",
            "ISA",
            "sea lice", 
            "aquaculture regulation"
        ],
        'REPORTING_AND_COMPLIANCE_SVC': [
            "renewable energy",
            "CO2 reduction",
            "BREEAM",
            "LEED",
            "SMB initiative"
        ]
    }
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
    
    def create_all_services(self) -> None:
        """Create all Cortex Search services"""
        logger.info("Creating Cortex Search services...")
        
        for service_name, service_config in self.SEARCH_SERVICES.items():
            try:
                self.create_search_service(service_name, service_config)
                logger.info(f"Created search service: {service_name}")
            except Exception as e:
                logger.error(f"Failed to create search service {service_name}: {str(e)}")
        
        # Pre-warm all services
        self.prewarm_all_services()
        
        logger.info("All Cortex Search services created and pre-warmed")
    
    def create_search_service(self, service_name: str, config: Dict) -> None:
        """Create a single Cortex Search service"""
        
        # Drop existing service if it exists
        try:
            self.session.sql(f"DROP CORTEX SEARCH SERVICE IF EXISTS {service_name}").collect()
        except SnowparkSQLException:
            pass  # Service might not exist
        
        # Create the search service
        create_sql = f"""
        CREATE CORTEX SEARCH SERVICE {service_name}
        ON {config['search_column']}
        ATTRIBUTES {config['id_column']}, {config['title_column']}
        WAREHOUSE = {self.config.get_config('WAREHOUSE_FOR_BUILD')}
        TARGET_LAG = '1 hour'
        AS (
            {config['source_query']}
        )
        """
        
        try:
            self.session.sql(create_sql).collect()
            logger.info(f"Successfully created search service: {service_name}")
        except Exception as e:
            logger.error(f"Failed to create search service {service_name}: {str(e)}")
            raise
    
    def prewarm_all_services(self) -> None:
        """Pre-warm all search services to reduce first-hit latency"""
        logger.info("Pre-warming search services...")
        
        for service_name, queries in self.PREWARMING_QUERIES.items():
            self.prewarm_service(service_name, queries)
    
    def prewarm_service(self, service_name: str, queries: List[str]) -> None:
        """Pre-warm a specific search service"""
        logger.info(f"Pre-warming service: {service_name}")
        
        for query in queries:
            try:
                # Execute search query to warm up the service
                search_sql = f"""
                SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    '{service_name}',
                    '{{"query": "{query}", "limit": 10}}'
                ) as search_results
                """
                
                result = self.session.sql(search_sql).collect()
                logger.debug(f"Pre-warmed {service_name} with query: '{query}'")
                
            except Exception as e:
                logger.warning(f"Pre-warming failed for {service_name} with query '{query}': {str(e)}")
    
    def test_all_services(self) -> Dict[str, bool]:
        """Test all search services with sample queries"""
        logger.info("Testing all search services...")
        
        results = {}
        
        for service_name, queries in self.PREWARMING_QUERIES.items():
            results[service_name] = self.test_service(service_name, queries[0])
        
        return results
    
    def test_service(self, service_name: str, test_query: str) -> bool:
        """Test a specific search service"""
        try:
            search_sql = f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{service_name}',
                '{{"query": "{test_query}", "limit": 5}}'
            ) as search_results
            """
            
            result = self.session.sql(search_sql).collect()
            
            if result and result[0]['SEARCH_RESULTS']:
                logger.info(f"Search service {service_name} test successful")
                return True
            else:
                logger.warning(f"Search service {service_name} returned no results")
                return False
                
        except Exception as e:
            logger.error(f"Search service {service_name} test failed: {str(e)}")
            return False
    
    def get_service_status(self) -> Dict[str, str]:
        """Get status of all search services"""
        status = {}
        
        for service_name in self.SEARCH_SERVICES.keys():
            try:
                # Check if service exists and is ready
                check_sql = f"""
                SHOW CORTEX SEARCH SERVICES LIKE '{service_name}'
                """
                
                result = self.session.sql(check_sql).collect()
                
                if result:
                    status[service_name] = "EXISTS"
                else:
                    status[service_name] = "NOT_FOUND"
                    
            except Exception as e:
                status[service_name] = f"ERROR: {str(e)}"
        
        return status
    
    def drop_all_services(self) -> None:
        """Drop all search services (for reset)"""
        logger.info("Dropping all search services...")
        
        for service_name in self.SEARCH_SERVICES.keys():
            try:
                self.session.sql(f"DROP CORTEX SEARCH SERVICE IF EXISTS {service_name}").collect()
                logger.info(f"Dropped search service: {service_name}")
            except Exception as e:
                logger.warning(f"Failed to drop search service {service_name}: {str(e)}")

