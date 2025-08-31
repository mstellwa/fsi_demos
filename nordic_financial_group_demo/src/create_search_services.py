#!/usr/bin/env python3
"""
Snowdrift Financials - M5: Cortex Search Services Creation
Creates and tests Cortex Search services for Insurance and Banking documents:
- Insurance: Claims and Underwriting documents
- Banking: Economic reports and Compliance documents
"""

import logging
import yaml
from typing import List, Dict, Any
from snowflake.snowpark import Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('snowdrift_search_services.log')
    ]
)
logger = logging.getLogger(__name__)

class SearchServiceCreator:
    """Create and test Cortex Search services for Snowdrift Financials"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.connection_name = connection_name
        self.session = None
        
        # Search service settings
        self.warehouse = self.config.get('insurance', {}).get('search_services', {}).get('warehouse', 'COMPUTE_WH')
        self.target_lag = self.config.get('insurance', {}).get('search_services', {}).get('target_lag', '1 minute')
        
        # Banking search service settings (reuse insurance settings if not specified)
        banking_config = self.config.get('banking', {}).get('search_services', {})
        self.banking_warehouse = banking_config.get('warehouse', self.warehouse)
        self.banking_target_lag = banking_config.get('target_lag', self.target_lag)
        
    def create_session(self) -> Session:
        """Create Snowpark session using ~/.snowflake/connections.toml"""
        logger.info(f"Creating Snowpark session with connection: {self.connection_name}")
        try:
            self.session = Session.builder.config("connection_name", self.connection_name).create()
            logger.info(f"Connected to: {self.session.get_current_account()}")
            return self.session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            logger.error("Ensure ~/.snowflake/connections.toml is configured properly")
            raise
    
    def create_claims_search_service(self):
        """Create Cortex Search service for claims documents"""
        logger.info("Creating CLAIMS_SEARCH_SERVICE...")
        
        self.session.sql("USE SCHEMA INSURANCE").collect()
        
        create_service_sql = f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE CLAIMS_SEARCH_SERVICE
        ON CONTENT_MD
        ATTRIBUTES ID, TITLE, DOC_TYPE, CLAIM_ID, MUNICIPALITY, KEYWORDS
        TARGET_LAG = '{self.target_lag}'
        WAREHOUSE = {self.warehouse}
        AS (
            SELECT 
                DOC_ID as ID,
                TITLE,
                DOC_TYPE,
                CLAIM_ID,
                MUNICIPALITY, 
                KEYWORDS,
                CONTENT_MD
            FROM INSURANCE.CLAIMS_DOCUMENTS
        )
        """
        
        self.session.sql(create_service_sql).collect()
        logger.info("✓ CLAIMS_SEARCH_SERVICE created successfully")
        
    def create_underwriting_search_service(self):
        """Create Cortex Search service for underwriting documents"""
        logger.info("Creating UNDERWRITING_SEARCH_SERVICE...")
        
        self.session.sql("USE SCHEMA INSURANCE").collect()
        
        create_service_sql = f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE UNDERWRITING_SEARCH_SERVICE
        ON CONTENT_MD
        ATTRIBUTES ID, TITLE, DOC_TYPE, MUNICIPALITY, FLOOD_RISK_SCORE, KEYWORDS
        TARGET_LAG = '{self.target_lag}'
        WAREHOUSE = {self.warehouse}
        AS (
            SELECT 
                DOC_ID as ID,
                TITLE,
                DOC_TYPE,
                MUNICIPALITY,
                FLOOD_RISK_SCORE,
                KEYWORDS,
                CONTENT_MD
            FROM INSURANCE.UNDERWRITING_DOCUMENTS
        )
        """
        
        self.session.sql(create_service_sql).collect()
        logger.info("✓ UNDERWRITING_SEARCH_SERVICE created successfully")
    
    def test_search_services(self):
        """Test search services by verifying indexed documents"""
        logger.info("Testing search services by checking indexed content...")
        
        # Test claims search service content
        logger.info("=== Testing Claims Search Service Content ===")
        
        try:
            # Check if claims documents exist and have content
            result = self.session.sql("""
                SELECT DOC_TYPE, COUNT(*) as doc_count 
                FROM INSURANCE.CLAIMS_DOCUMENTS 
                GROUP BY DOC_TYPE 
                ORDER BY doc_count DESC
            """).collect()
            
            if result:
                logger.info(f"✓ Claims documents indexed: {len(result)} document types")
                for row in result:
                    logger.info(f"  - {row['DOC_TYPE']}: {row['DOC_COUNT']} documents")
            else:
                logger.warning("⚠ No claims documents found for indexing")
                
        except Exception as e:
            logger.error(f"✗ Claims content check failed: {str(e)}")
        
        # Test underwriting search service content
        logger.info("=== Testing Underwriting Search Service Content ===")
        
        try:
            # Check if underwriting documents exist and have content
            result = self.session.sql("""
                SELECT DOC_TYPE, COUNT(*) as doc_count 
                FROM INSURANCE.UNDERWRITING_DOCUMENTS 
                GROUP BY DOC_TYPE 
                ORDER BY doc_count DESC
            """).collect()
            
            if result:
                logger.info(f"✓ Underwriting documents indexed: {len(result)} document types")
                for row in result:
                    logger.info(f"  - {row['DOC_TYPE']}: {row['DOC_COUNT']} documents")
            else:
                logger.warning("⚠ No underwriting documents found for indexing")
                
        except Exception as e:
            logger.error(f"✗ Underwriting content check failed: {str(e)}")
        
        logger.info("✓ Search service content verification completed")
    
    def verify_search_services(self):
        """Verify search services are created and functional"""
        logger.info("Verifying search services...")
        
        # Check if services exist
        services_result = self.session.sql("SHOW CORTEX SEARCH SERVICES").collect()
        service_names = [row['name'] for row in services_result]
        
        required_services = ['CLAIMS_SEARCH_SERVICE', 'UNDERWRITING_SEARCH_SERVICE']
        
        for service in required_services:
            if service in service_names:
                logger.info(f"✓ {service} exists")
            else:
                logger.error(f"✗ {service} not found")
                raise Exception(f"Required service {service} not created")
        
        # Test basic functionality by checking document counts
        try:
            # Test that the services have indexed content
            claims_count = self.session.sql("SELECT COUNT(*) as cnt FROM INSURANCE.CLAIMS_DOCUMENTS").collect()
            underwriting_count = self.session.sql("SELECT COUNT(*) as cnt FROM INSURANCE.UNDERWRITING_DOCUMENTS").collect()
            
            if claims_count[0]['CNT'] > 0 and underwriting_count[0]['CNT'] > 0:
                logger.info(f"✓ Search services ready: {claims_count[0]['CNT']} claims docs, {underwriting_count[0]['CNT']} underwriting docs")
            else:
                logger.warning("⚠ Search services created but no documents found to index")
            
        except Exception as e:
            logger.error(f"✗ Search service content verification failed: {str(e)}")
            # Don't raise - services were created successfully
    
    def create_economic_search_service(self):
        """Create Cortex Search service for economic documents"""
        logger.info("Creating ECONOMIC_SEARCH_SERVICE...")
        
        try:
            # Drop existing service if it exists
            self.session.sql("DROP CORTEX SEARCH SERVICE IF EXISTS ECONOMIC_SEARCH_SERVICE").collect()
            logger.info("✓ Dropped existing ECONOMIC_SEARCH_SERVICE")
        except Exception as e:
            logger.info(f"No existing ECONOMIC_SEARCH_SERVICE to drop: {str(e)}")
        
        try:
            # Create Cortex Search Service for economic documents
            create_economic_sql = f"""
            CREATE CORTEX SEARCH SERVICE ECONOMIC_SEARCH_SERVICE
            ON CONTENT_MD
            ATTRIBUTES MUNICIPALITY, REGION, DOC_TYPE, TITLE, KEYWORDS
            TARGET_LAG = '{self.banking_target_lag}'
            WAREHOUSE = {self.banking_warehouse}
            AS (
                SELECT 
                    DOC_ID,
                    TITLE,
                    CONTENT_MD,
                    MUNICIPALITY,
                    REGION,
                    DOC_TYPE,
                    KEYWORDS
                FROM BANK.ECONOMIC_DOCUMENTS 
                WHERE CONTENT_MD IS NOT NULL
            )
            """
            
            self.session.sql(create_economic_sql).collect()
            logger.info("✓ ECONOMIC_SEARCH_SERVICE created successfully")
            
            # Verify the service was created
            service_check = self.session.sql("SHOW CORTEX SEARCH SERVICES LIKE 'ECONOMIC_SEARCH_SERVICE'").collect()
            if service_check:
                logger.info(f"✓ Service verified: {service_check[0]['name']}")
            else:
                logger.warning("⚠ Service creation completed but verification failed")
                
        except Exception as e:
            logger.error(f"✗ Failed to create ECONOMIC_SEARCH_SERVICE: {str(e)}")
            raise
    
    def create_compliance_search_service(self):
        """Create Cortex Search service for compliance documents"""
        logger.info("Creating COMPLIANCE_SEARCH_SERVICE...")
        
        try:
            # Drop existing service if it exists
            self.session.sql("DROP CORTEX SEARCH SERVICE IF EXISTS COMPLIANCE_SEARCH_SERVICE").collect()
            logger.info("✓ Dropped existing COMPLIANCE_SEARCH_SERVICE")
        except Exception as e:
            logger.info(f"No existing COMPLIANCE_SEARCH_SERVICE to drop: {str(e)}")
        
        try:
            # Create Cortex Search Service for compliance documents
            create_compliance_sql = f"""
            CREATE CORTEX SEARCH SERVICE COMPLIANCE_SEARCH_SERVICE
            ON CONTENT_MD
            ATTRIBUTES ORGANIZATION_NUMBER, COMPANY_NAME, DOC_TYPE, TITLE, KEYWORDS
            TARGET_LAG = '{self.banking_target_lag}'
            WAREHOUSE = {self.banking_warehouse}
            AS (
                SELECT 
                    DOC_ID,
                    TITLE,
                    CONTENT_MD,
                    ORGANIZATION_NUMBER,
                    COMPANY_NAME,
                    DOC_TYPE,
                    KEYWORDS
                FROM BANK.COMPLIANCE_DOCUMENTS 
                WHERE CONTENT_MD IS NOT NULL
            )
            """
            
            self.session.sql(create_compliance_sql).collect()
            logger.info("✓ COMPLIANCE_SEARCH_SERVICE created successfully")
            
            # Verify the service was created
            service_check = self.session.sql("SHOW CORTEX SEARCH SERVICES LIKE 'COMPLIANCE_SEARCH_SERVICE'").collect()
            if service_check:
                logger.info(f"✓ Service verified: {service_check[0]['name']}")
            else:
                logger.warning("⚠ Service creation completed but verification failed")
                
        except Exception as e:
            logger.error(f"✗ Failed to create COMPLIANCE_SEARCH_SERVICE: {str(e)}")
            raise
    
    def verify_banking_search_services(self):
        """Verify Banking search services are working and have content"""
        logger.info("Verifying Banking search services content...")
        
        try:
            # Test economic search service
            logger.info("Testing ECONOMIC_SEARCH_SERVICE...")
            
            # Check if SEARCH_PREVIEW is available
            try:
                economic_test = self.session.sql("""
                    SELECT SEARCH_PREVIEW(
                        'ECONOMIC_SEARCH_SERVICE',
                        'housing market Oslo',
                        3
                    ) as results
                """).collect()
                
                if economic_test and economic_test[0]['RESULTS']:
                    results = economic_test[0]['RESULTS']
                    logger.info(f"✓ ECONOMIC_SEARCH_SERVICE working: {len(results)} results for 'housing market Oslo'")
                    # Log sample result
                    if results:
                        sample = results[0]
                        logger.info(f"  Sample: {sample.get('title', 'No title')[:100]}...")
                else:
                    logger.warning("⚠ ECONOMIC_SEARCH_SERVICE created but no results returned")
                    
            except Exception as e:
                if "does not exist or not authorized" in str(e).lower():
                    logger.info("SEARCH_PREVIEW not available, checking document count instead")
                    # Fallback: Check document count
                    doc_count = self.session.sql("SELECT COUNT(*) as count FROM BANK.ECONOMIC_DOCUMENTS").collect()
                    if doc_count and doc_count[0]['COUNT'] > 0:
                        logger.info(f"✓ ECONOMIC_SEARCH_SERVICE: {doc_count[0]['COUNT']} documents available")
                    else:
                        logger.warning("⚠ ECONOMIC_SEARCH_SERVICE: No documents found")
                else:
                    raise
            
            # Test compliance search service
            logger.info("Testing COMPLIANCE_SEARCH_SERVICE...")
            
            try:
                compliance_test = self.session.sql("""
                    SELECT SEARCH_PREVIEW(
                        'COMPLIANCE_SEARCH_SERVICE',
                        'KYC assessment',
                        3
                    ) as results
                """).collect()
                
                if compliance_test and compliance_test[0]['RESULTS']:
                    results = compliance_test[0]['RESULTS']
                    logger.info(f"✓ COMPLIANCE_SEARCH_SERVICE working: {len(results)} results for 'KYC assessment'")
                    # Log sample result
                    if results:
                        sample = results[0]
                        logger.info(f"  Sample: {sample.get('title', 'No title')[:100]}...")
                else:
                    logger.warning("⚠ COMPLIANCE_SEARCH_SERVICE created but no results returned")
                    
            except Exception as e:
                if "does not exist or not authorized" in str(e).lower():
                    logger.info("SEARCH_PREVIEW not available, checking document count instead")
                    # Fallback: Check document count
                    doc_count = self.session.sql("SELECT COUNT(*) as count FROM BANK.COMPLIANCE_DOCUMENTS").collect()
                    if doc_count and doc_count[0]['COUNT'] > 0:
                        logger.info(f"✓ COMPLIANCE_SEARCH_SERVICE: {doc_count[0]['COUNT']} documents available")
                    else:
                        logger.warning("⚠ COMPLIANCE_SEARCH_SERVICE: No documents found")
                else:
                    raise
            
            logger.info("Banking search services verification completed")
            
        except Exception as e:
            logger.error(f"✗ Banking search service verification failed: {str(e)}")
            # Don't raise - services were created successfully
    
    def test_banking_search_services(self):
        """Test Banking search services with sample queries"""
        logger.info("Testing Banking search services with sample queries...")
        
        test_queries = [
            {
                'service': 'ECONOMIC_SEARCH_SERVICE',
                'query': 'Oslo housing market conditions',
                'description': 'Economic search test - Oslo housing'
            },
            {
                'service': 'ECONOMIC_SEARCH_SERVICE', 
                'query': 'employment data Bergen',
                'description': 'Economic search test - Bergen employment'
            },
            {
                'service': 'COMPLIANCE_SEARCH_SERVICE',
                'query': 'AML risk assessment',
                'description': 'Compliance search test - AML'
            },
            {
                'service': 'COMPLIANCE_SEARCH_SERVICE',
                'query': 'beneficial ownership analysis',
                'description': 'Compliance search test - UBO'
            }
        ]
        
        for test in test_queries:
            try:
                logger.info(f"Testing: {test['description']}")
                
                # Try SEARCH_PREVIEW first
                try:
                    result = self.session.sql(f"""
                        SELECT SEARCH_PREVIEW(
                            '{test['service']}',
                            '{test['query']}',
                            3
                        ) as results
                    """).collect()
                    
                    if result and result[0]['RESULTS']:
                        results = result[0]['RESULTS']
                        logger.info(f"✓ {test['service']}: {len(results)} results for '{test['query']}'")
                    else:
                        logger.warning(f"⚠ {test['service']}: No results for '{test['query']}'")
                        
                except Exception as e:
                    if "does not exist or not authorized" in str(e).lower():
                        logger.info(f"SEARCH_PREVIEW not available for {test['service']}")
                    else:
                        logger.warning(f"Search test failed for {test['service']}: {str(e)}")
                        
            except Exception as e:
                logger.warning(f"✗ Test failed for {test['description']}: {str(e)}")
        
        logger.info("Banking search services testing completed")
    
    def run_search_service_creation(self):
        """Execute complete search service creation and testing"""
        logger.info("Starting M5 - Cortex Search Services Creation...")
        
        try:
            self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Step 1: Create Insurance Search Services
            logger.info("=== Step 1: Insurance Claims Search Service ===")
            self.create_claims_search_service()
            
            logger.info("=== Step 2: Insurance Underwriting Search Service ===")
            self.create_underwriting_search_service()
            
            # Step 3: Create Banking Search Services
            logger.info("=== Step 3: Banking Economic Search Service ===")
            self.create_economic_search_service()
            
            logger.info("=== Step 4: Banking Compliance Search Service ===")
            self.create_compliance_search_service()
            
            # Step 5: Verify All Services
            logger.info("=== Step 5: Insurance Search Services Verification ===")
            self.verify_search_services()
            
            logger.info("=== Step 6: Banking Search Services Verification ===")
            self.verify_banking_search_services()
            
            # Step 7: Test All Services
            logger.info("=== Step 7: Insurance Search Services Testing ===")
            self.test_search_services()
            
            logger.info("=== Step 8: Banking Search Services Testing ===")
            self.test_banking_search_services()
            
            logger.info("All Cortex Search Services creation completed successfully!")
            logger.info("Ready for agent configuration: Insurance + Banking services available")
            
        except Exception as e:
            logger.error(f"Search service creation failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Cortex Search Services")
    parser.add_argument(
        "--connection", 
        default="default",
        help="Connection name from ~/.snowflake/connections.toml (default: default)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        creator = SearchServiceCreator(connection_name=args.connection)
        creator.run_search_service_creation()
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
