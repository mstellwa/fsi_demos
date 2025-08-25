"""
SnowBank Intelligence Demo - Complete Setup Script

This script sets up the complete demo environment including:
- Database schema creation (IF NOT EXISTS)
- Synthetic data generation (REPLACE tables)
- Document generation using Cortex Complete (REPLACE tables)
- Cortex Search services (CREATE OR REPLACE)
- Dual semantic model architecture (CREATE OR REPLACE)
- Comprehensive validation

Usage:
    python main.py [--connection CONNECTION_NAME]
    
The script always performs a complete demo setup with full dataset.
"""

import logging
import time
from datetime import datetime

from src.config import DemoConfig
from src.database import DatabaseManager
from src.data_generators import StructuredDataGenerator
from src.document_generator import DocumentGenerator
from src.search_services import SearchServiceManager
from src.semantic_model import SemanticModelManager
from src.validation import ValidationFramework

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('snowbank_demo.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DemoSetupManager:
    """Manages complete demo setup with robust error handling and validation"""
    
    def __init__(self, connection_name='sfseeurope-mstellwall-aws-us-west3'):
        self.config = DemoConfig(connection_name=connection_name)
        self.db_manager = DatabaseManager(self.config)
        self.data_generator = StructuredDataGenerator(self.config)
        self.doc_generator = DocumentGenerator(self.config)
        self.search_manager = SearchServiceManager(self.config)
        self.semantic_manager = SemanticModelManager(self.config)
        self.validator = ValidationFramework(self.config)
        
    def setup_complete_demo(self) -> dict:
        """Execute complete demo setup with full dataset"""
        start_time = time.time()
        results = {
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'steps': {},
            'total_time_minutes': 0,
            'errors': []
        }
        
        try:
            logger.info("🚀 Starting complete SnowBank Intelligence Demo setup...")
            logger.info("📋 Setup Strategy: IF NOT EXISTS (database) + REPLACE (all objects)")
            
            # Step 1: Database schema (IF NOT EXISTS)
            results['steps']['1_database_schema'] = self._setup_database_schema()
            
            # Step 2: Structured data (REPLACE tables)
            results['steps']['2_structured_data'] = self._generate_structured_data()
            
            # Step 3: Documents (REPLACE tables)
            results['steps']['3_documents'] = self._generate_documents()
            
            # Step 4: Search services (CREATE OR REPLACE)
            results['steps']['4_search_services'] = self._create_search_services()
            
            # Step 5: Dual semantic model (CREATE OR REPLACE)
            results['steps']['5_semantic_model'] = self._create_semantic_model()
            
            # Step 6: Comprehensive validation
            results['steps']['6_validation'] = self._validate_setup()
            
            # Calculate total time
            total_time = (time.time() - start_time) / 60
            results['total_time_minutes'] = round(total_time, 1)
            
            # Check overall success
            all_successful = all(step.get('success', False) for step in results['steps'].values())
            results['success'] = all_successful
            
            if all_successful:
                logger.info(f"✅ Demo setup completed successfully in {results['total_time_minutes']} minutes")
                logger.info("🎯 Ready for Scenario 1: 'Holistic Client 360°' testing!")
            else:
                logger.error("❌ Demo setup had failures")
                
        except Exception as e:
            logger.error(f"💥 Fatal error during demo setup: {str(e)}")
            results['errors'].append(f"Fatal error: {str(e)}")
            
        finally:
            self.config.session.close()
            
        return results
    
    def _setup_database_schema(self) -> dict:
        """Setup database schema using IF NOT EXISTS strategy"""
        step_result = {'success': False, 'details': {}}
        start_time = time.time()
        
        try:
            logger.info("📋 Setting up database schema (IF NOT EXISTS)...")
            
            # Create database schema with IF NOT EXISTS
            self.db_manager.create_database_schema()
            
            step_result['success'] = True
            step_result['details'] = {
                'schema_created': True,
                'strategy': 'IF NOT EXISTS'
            }
            
            logger.info(f"✅ Database schema setup completed in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Database schema setup failed: {str(e)}")
            
        return step_result
    
    def _generate_structured_data(self) -> dict:
        """Generate all structured data with REPLACE strategy"""
        step_result = {'success': False, 'details': {}}
        start_time = time.time()
        
        try:
            logger.info("📊 Generating structured data (REPLACE tables)...")
            
            # Generate all structured data (uses OVERWRITE mode)
            self.data_generator.generate_all_data()
            
            # Count generated records for validation
            record_counts = {}
            tables = ['MEMBER_BANKS', 'CUSTOMERS', 'LOANS', 'FINANCIALS', 'ALLIANCE_PERFORMANCE', 'MARKET_DATA']
            
            for table in tables:
                try:
                    count_result = self.config.session.sql(f"SELECT COUNT(*) as count FROM {table}").collect()
                    record_counts[table] = count_result[0]['COUNT'] if count_result else 0
                except Exception as e:
                    record_counts[table] = f"Error: {str(e)}"
            
            # Verify demo companies exist
            helio_check = self.config.session.sql(
                "SELECT customer_name FROM CUSTOMERS WHERE customer_name = 'Helio Salmon AS'"
            ).collect()
            demo_companies_exist = len(helio_check) > 0
            
            step_result['success'] = demo_companies_exist and record_counts.get('CUSTOMERS', 0) >= 5000
            step_result['details'] = {
                'record_counts': record_counts,
                'demo_companies_included': demo_companies_exist,
                'strategy': 'REPLACE tables',
                'helio_salmon_in_banking_data': demo_companies_exist
            }
            
            logger.info(f"✅ Structured data generation completed in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Structured data generation failed: {str(e)}")
            
        return step_result
    
    def _generate_documents(self) -> dict:
        """Generate documents using REPLACE strategy"""
        step_result = {'success': False, 'details': {}}
        start_time = time.time()
        
        try:
            logger.info("📄 Generating documents (REPLACE tables)...")
            
            # Generate documents using optimized Snowpark approach
            self.doc_generator.generate_all_documents()
            
            # Count generated documents
            doc_count_result = self.config.session.sql("SELECT COUNT(*) as count FROM DOCUMENTS").collect()
            doc_count = doc_count_result[0]['COUNT'] if doc_count_result else 0
            
            step_result['success'] = doc_count > 0
            step_result['details'] = {
                'documents_generated': doc_count,
                'generation_method': 'snowpark_dataframe_optimized',
                'strategy': 'REPLACE tables'
            }
            
            logger.info(f"✅ Document generation completed in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Document generation failed: {str(e)}")
            
        return step_result
    
    def _create_search_services(self) -> dict:
        """Create Cortex Search services using CREATE OR REPLACE strategy"""
        step_result = {'success': False, 'details': {}}
        start_time = time.time()
        
        try:
            logger.info("🔍 Creating search services (CREATE OR REPLACE)...")
            
            # Create all search services
            self.search_manager.create_all_services()
            
            # Test services
            service_status = self.search_manager.test_all_services()
            
            step_result['success'] = all(service_status.values())
            step_result['details'] = {
                'services_created': list(service_status.keys()),
                'services_status': service_status,
                'strategy': 'CREATE OR REPLACE'
            }
            
            logger.info(f"✅ Search services creation completed in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Search services creation failed: {str(e)}")
            
        return step_result
    
    def _create_semantic_model(self) -> dict:
        """Create dual semantic model using CREATE OR REPLACE strategy"""
        step_result = {'success': False, 'details': {}}
        start_time = time.time()
        
        try:
            logger.info("🧠 Creating dual semantic model (CREATE OR REPLACE)...")
            
            # Create both semantic views (banking + market)
            self.semantic_manager.create_semantic_view()
            
            # Validate both semantic views
            validation_results = self.semantic_manager.validate_semantic_model()
            
            banking_exists = validation_results.get('SNOWBANK_DEMO_SV', False)
            market_exists = validation_results.get('MARKET_PEER_ANALYSIS_SV', False)
            
            step_result['success'] = banking_exists and market_exists
            step_result['details'] = {
                'banking_semantic_view_created': banking_exists,
                'market_semantic_view_created': market_exists,
                'both_views_working': banking_exists and market_exists,
                'validation_results': validation_results,
                'strategy': 'CREATE OR REPLACE'
            }
            
            logger.info(f"✅ Semantic model creation completed in {time.time() - start_time:.1f} seconds")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Semantic model creation failed: {str(e)}")
            
        return step_result
    
    def _validate_setup(self) -> dict:
        """Comprehensive validation of complete setup"""
        step_result = {'success': False, 'details': {}}
        
        try:
            logger.info("✅ Running comprehensive validation...")
            
            validation_checks = {}
            
            # Check demo companies exist in banking data
            helio_banking = self.config.session.sql(
                "SELECT customer_name FROM CUSTOMERS WHERE customer_name = 'Helio Salmon AS'"
            ).collect()
            validation_checks['helio_in_banking'] = len(helio_banking) > 0
            
            # Check demo companies exist in market data
            helio_market = self.config.session.sql(
                "SELECT company_name FROM MARKET_DATA WHERE company_name = 'Helio Salmon AS'"
            ).collect()
            validation_checks['helio_in_market'] = len(helio_market) > 0
            
            # Check LTM fee data exists (using actual record types)
            fee_check = self.config.session.sql("""
                SELECT COUNT(*) as count FROM FINANCIALS 
                WHERE record_type IN ('FEE_REVENUE', 'COMMISSION')
                AND record_date >= DATEADD(month, -12, CURRENT_DATE())
            """).collect()
            validation_checks['ltm_fees_exist'] = fee_check[0]['COUNT'] > 0 if fee_check else False
            
            # Check Helio Salmon AS has realistic LTM fees
            helio_ltm_check = self.config.session.sql("""
                SELECT * FROM SEMANTIC_VIEW(
                    SNOWBANK_DEMO_SV
                    DIMENSIONS customers.customer_name
                    METRICS financials.ltm_fee_income
                )
                WHERE customer_name = 'Helio Salmon AS'
            """).collect()
            helio_ltm_amount = helio_ltm_check[0]['LTM_FEE_INCOME'] if helio_ltm_check else 0
            validation_checks['helio_has_ltm_fees'] = helio_ltm_amount > 0
            
            # Check both semantic views exist
            try:
                sv_check = self.config.session.sql("SHOW SEMANTIC VIEWS").collect()
                banking_view_exists = any('SNOWBANK_DEMO_SV' in str(row) for row in sv_check)
                market_view_exists = any('MARKET_PEER_ANALYSIS_SV' in str(row) for row in sv_check)
                validation_checks['banking_semantic_view'] = banking_view_exists
                validation_checks['market_semantic_view'] = market_view_exists
            except:
                validation_checks['banking_semantic_view'] = False
                validation_checks['market_semantic_view'] = False
            
            # Check search services respond
            try:
                search_test = self.config.session.sql(
                    "SELECT SEARCH_PREVIEW('CLIENT_AND_MARKET_INTEL_SVC', 'aquaculture', 1)"
                ).collect()
                validation_checks['search_services_working'] = len(search_test) > 0
            except:
                validation_checks['search_services_working'] = False
            
            # Check data volumes
            customer_check = self.config.session.sql("SELECT COUNT(*) as count FROM CUSTOMERS").collect()
            validation_checks['sufficient_customers'] = customer_check[0]['COUNT'] >= 5000 if customer_check else False
            
            step_result['success'] = all(validation_checks.values())
            step_result['details'] = validation_checks
            
            if step_result['success']:
                logger.info("✅ All validation checks passed - demo ready!")
            else:
                failed_checks = [k for k, v in validation_checks.items() if not v]
                logger.warning(f"⚠️ Validation issues: {failed_checks}")
            
        except Exception as e:
            step_result['details']['error'] = str(e)
            logger.error(f"❌ Validation failed: {str(e)}")
            
        return step_result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='SnowBank Intelligence Demo - Complete Setup')
    parser.add_argument('--connection', default='sfseeurope-mstellwall-aws-us-west3', 
                       help='Connection name from connections.toml')
    
    args = parser.parse_args()
    
    # Execute complete demo setup
    setup_manager = DemoSetupManager(connection_name=args.connection)
    results = setup_manager.setup_complete_demo()
    
    # Print results summary
    print("\n" + "="*70)
    print("🚀 SNOWBANK INTELLIGENCE DEMO SETUP RESULTS")
    print("="*70)
    print(f"Success: {'✅ YES' if results['success'] else '❌ NO'}")
    print(f"Total Time: {results['total_time_minutes']} minutes")
    print(f"Timestamp: {results['timestamp']}")
    
    if results.get('errors'):
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"   - {error}")
    
    print(f"\n📋 Setup Steps:")
    for step_name, step_result in results['steps'].items():
        status = '✅' if step_result.get('success', False) else '❌'
        print(f"   {status} {step_name}")
    
    if results['success']:
        print(f"\n🎯 DEMO READY FOR TESTING!")
        print(f"   ✅ Banking data: Helio Salmon AS available")
        print(f"   ✅ Market data: Helio Salmon AS available for peer analysis")
        print(f"   ✅ Dual semantic views: Banking + Market")
        print(f"   ✅ Search services: 3 services operational")
        print(f"   ✅ Scenario 1 ready: 'Holistic Client 360°'")
    
    print("\n" + "="*70)
    
    return 0 if results['success'] else 1


if __name__ == "__main__":
    exit(main())
