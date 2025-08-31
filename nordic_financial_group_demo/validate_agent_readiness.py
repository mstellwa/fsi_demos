#!/usr/bin/env python3
"""
Agent Readiness Validation Script
Verifies that all infrastructure is ready for Snowflake Intelligence agent configuration.
"""

import logging
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from setup import SnowdriftSetup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def validate_infrastructure(connection_name: str = "sfseeurope-mstellwall-aws-us-west3"):
    """Validate all infrastructure components for agent configuration"""
    
    logger.info("🔍 Validating Snowdrift Financials Infrastructure for Agent Configuration...")
    
    try:
        # Create session
        setup = SnowdriftSetup(connection_name=connection_name)
        session = setup.create_session()
        session.sql("USE DATABASE SNOWDRIFT_FINANCIALS").collect()
        
        validation_results = []
        
        # 1. Check Semantic View
        logger.info("📊 Checking Semantic View...")
        try:
            result = session.sql("SELECT * FROM SEMANTIC_VIEW(INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW METRICS policies.policy_count) LIMIT 1").collect()
            if result and result[0]['POLICY_COUNT'] > 0:
                validation_results.append("✅ NORWEGIAN_INSURANCE_SEMANTIC_VIEW: Working with data")
                logger.info(f"✅ Semantic view operational with {result[0]['POLICY_COUNT']} policies")
            else:
                validation_results.append("❌ NORWEGIAN_INSURANCE_SEMANTIC_VIEW: No data")
        except Exception as e:
            validation_results.append(f"❌ NORWEGIAN_INSURANCE_SEMANTIC_VIEW: Error - {str(e)}")
        
        # 1b. Check Banking Semantic View
        logger.info("🏦 Checking Banking Semantic View...")
        try:
            result = session.sql("SELECT * FROM SEMANTIC_VIEW(BANK_ANALYTICS.CUSTOMER_360_VIEW METRICS customers.customer_count) LIMIT 1").collect()
            if result and result[0]['CUSTOMER_COUNT'] > 0:
                validation_results.append("✅ CUSTOMER_360_VIEW: Working with data")
                logger.info(f"✅ Banking semantic view operational with {result[0]['CUSTOMER_COUNT']} customers")
            else:
                validation_results.append("❌ CUSTOMER_360_VIEW: No data")
        except Exception as e:
            validation_results.append(f"❌ CUSTOMER_360_VIEW: Error - {str(e)}")
        
        # 2. Check Search Services
        logger.info("🔍 Checking Search Services...")
        try:
            session.sql("USE SCHEMA INSURANCE").collect()
            result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            service_names = [row['name'] for row in result]
            
            if 'CLAIMS_SEARCH_SERVICE' in service_names:
                validation_results.append("✅ CLAIMS_SEARCH_SERVICE: Available")
            else:
                validation_results.append("❌ CLAIMS_SEARCH_SERVICE: Missing")
                
            if 'UNDERWRITING_SEARCH_SERVICE' in service_names:
                validation_results.append("✅ UNDERWRITING_SEARCH_SERVICE: Available")
            else:
                validation_results.append("❌ UNDERWRITING_SEARCH_SERVICE: Missing")
                
        except Exception as e:
            validation_results.append(f"❌ Insurance Search Services: Error - {str(e)}")
        
        # 2b. Check Banking Search Services
        logger.info("🏦 Checking Banking Search Services...")
        try:
            result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            service_names = [row['name'] for row in result]
            
            if 'ECONOMIC_SEARCH_SERVICE' in service_names:
                validation_results.append("✅ ECONOMIC_SEARCH_SERVICE: Available")
            else:
                validation_results.append("❌ ECONOMIC_SEARCH_SERVICE: Missing")
                
            if 'COMPLIANCE_SEARCH_SERVICE' in service_names:
                validation_results.append("✅ COMPLIANCE_SEARCH_SERVICE: Available")
            else:
                validation_results.append("❌ COMPLIANCE_SEARCH_SERVICE: Missing")
                
        except Exception as e:
            validation_results.append(f"❌ Banking Search Services: Error - {str(e)}")
        
        # 3. Check Document Content
        logger.info("📄 Checking Document Content...")
        try:
            session.sql("USE SCHEMA INSURANCE").collect()
            
            # Claims documents
            claims_result = session.sql("SELECT COUNT(*) as cnt FROM CLAIMS_DOCUMENTS").collect()
            claims_count = claims_result[0]['CNT']
            if claims_count >= 150:
                validation_results.append(f"✅ Claims Documents: {claims_count} documents")
            else:
                validation_results.append(f"⚠️ Claims Documents: Only {claims_count} documents (expected ~150)")
            
            # Underwriting documents
            underwriting_result = session.sql("SELECT COUNT(*) as cnt FROM UNDERWRITING_DOCUMENTS").collect()
            underwriting_count = underwriting_result[0]['CNT']
            if underwriting_count >= 120:
                validation_results.append(f"✅ Underwriting Documents: {underwriting_count} documents")
            else:
                validation_results.append(f"⚠️ Underwriting Documents: Only {underwriting_count} documents (expected ~120)")
                
        except Exception as e:
            validation_results.append(f"❌ Insurance Document Content: Error - {str(e)}")
        
        # 3b. Check Banking Document Content
        logger.info("🏦 Checking Banking Document Content...")
        try:
            session.sql("USE SCHEMA BANK").collect()
            
            # Economic documents
            economic_result = session.sql("SELECT COUNT(*) as cnt FROM ECONOMIC_DOCUMENTS").collect()
            economic_count = economic_result[0]['CNT']
            if economic_count >= 100:
                validation_results.append(f"✅ Economic Documents: {economic_count} documents")
            else:
                validation_results.append(f"⚠️ Economic Documents: Only {economic_count} documents (expected ~100)")
            
            # Compliance documents
            compliance_result = session.sql("SELECT COUNT(*) as cnt FROM COMPLIANCE_DOCUMENTS").collect()
            compliance_count = compliance_result[0]['CNT']
            if compliance_count >= 75:
                validation_results.append(f"✅ Compliance Documents: {compliance_count} documents")
            else:
                validation_results.append(f"⚠️ Compliance Documents: Only {compliance_count} documents (expected ~75)")
                
        except Exception as e:
            validation_results.append(f"❌ Banking Document Content: Error - {str(e)}")
        
        # 4. Check Structured Data
        logger.info("🏢 Checking Structured Data...")
        try:
            session.sql("USE SCHEMA INSURANCE").collect()
            
            # Policies
            policies_result = session.sql("SELECT COUNT(*) as cnt FROM POLICIES").collect()
            policies_count = policies_result[0]['CNT']
            if policies_count >= 20000:
                validation_results.append(f"✅ Policies: {policies_count:,} records")
            else:
                validation_results.append(f"⚠️ Policies: Only {policies_count:,} records (expected ~20,000)")
            
            # Claims
            claims_result = session.sql("SELECT COUNT(*) as cnt FROM CLAIMS").collect()
            claims_count = claims_result[0]['CNT']
            if claims_count >= 30000:
                validation_results.append(f"✅ Claims: {claims_count:,} records")
            else:
                validation_results.append(f"⚠️ Claims: Only {claims_count:,} records (expected ~30,000)")
                
        except Exception as e:
            validation_results.append(f"❌ Insurance Structured Data: Error - {str(e)}")
        
        # 4b. Check Banking Structured Data
        logger.info("🏦 Checking Banking Structured Data...")
        try:
            session.sql("USE SCHEMA BANK").collect()
            
            # Customers
            customers_result = session.sql("SELECT COUNT(*) as cnt FROM CUSTOMERS").collect()
            customers_count = customers_result[0]['CNT']
            if customers_count >= 25000:
                validation_results.append(f"✅ Banking Customers: {customers_count:,} records")
            else:
                validation_results.append(f"⚠️ Banking Customers: Only {customers_count:,} records (expected ~25,000)")
            
            # Accounts
            accounts_result = session.sql("SELECT COUNT(*) as cnt FROM ACCOUNTS").collect()
            accounts_count = accounts_result[0]['CNT']
            if accounts_count >= 60000:
                validation_results.append(f"✅ Banking Accounts: {accounts_count:,} records")
            else:
                validation_results.append(f"⚠️ Banking Accounts: Only {accounts_count:,} records (expected ~65,000)")
            
            # Transactions
            transactions_result = session.sql("SELECT COUNT(*) as cnt FROM TRANSACTIONS").collect()
            transactions_count = transactions_result[0]['CNT']
            if transactions_count >= 4000000:
                validation_results.append(f"✅ Banking Transactions: {transactions_count:,} records")
            else:
                validation_results.append(f"⚠️ Banking Transactions: Only {transactions_count:,} records (expected ~5,000,000)")
            
            # Loans
            loans_result = session.sql("SELECT COUNT(*) as cnt FROM LOANS").collect()
            loans_count = loans_result[0]['CNT']
            if loans_count >= 15000:
                validation_results.append(f"✅ Banking Loans: {loans_count:,} records")
            else:
                validation_results.append(f"⚠️ Banking Loans: Only {loans_count:,} records (expected ~15,000)")
            
            # Cross-division integration check
            cross_div_result = session.sql("SELECT COUNT(*) as cnt FROM CUSTOMERS WHERE INSURANCE_POLICY_ID IS NOT NULL").collect()
            cross_div_count = cross_div_result[0]['CNT']
            cross_div_percentage = (cross_div_count / customers_count) * 100 if customers_count > 0 else 0
            if cross_div_percentage >= 15:
                validation_results.append(f"✅ Cross-Division Integration: {cross_div_count:,} customers ({cross_div_percentage:.1f}%)")
            else:
                validation_results.append(f"⚠️ Cross-Division Integration: Only {cross_div_count:,} customers ({cross_div_percentage:.1f}%) have insurance")
                
        except Exception as e:
            validation_results.append(f"❌ Banking Structured Data: Error - {str(e)}")
        
        # 5. Test Search Functionality (optional - may not be available in all environments)
        logger.info("🧪 Testing Search Functionality...")
        try:
            # Test claims search
            claims_search_result = session.sql(
                "SELECT CORTEX_SEARCH('CLAIMS_SEARCH_SERVICE', 'flood damage') LIMIT 1"
            ).collect()
            if claims_search_result:
                validation_results.append("✅ Claims Search: Functional")
            else:
                validation_results.append("⚠️ Claims Search: No results")
                
            # Test underwriting search
            underwriting_search_result = session.sql(
                "SELECT CORTEX_SEARCH('UNDERWRITING_SEARCH_SERVICE', 'flood risk') LIMIT 1"
            ).collect()
            if underwriting_search_result:
                validation_results.append("✅ Underwriting Search: Functional")
            else:
                validation_results.append("⚠️ Underwriting Search: No results")
                
        except Exception as e:
            # Search functionality may not be available in all environments
            if "Unknown function CORTEX_SEARCH" in str(e):
                validation_results.append("ℹ️ Insurance Search Functionality: CORTEX_SEARCH not available (agents will still work in Snowsight)")
            else:
                validation_results.append(f"⚠️ Insurance Search Functionality: {str(e)}")
        
        # 5b. Test Banking Search Functionality (optional)
        logger.info("🏦 Testing Banking Search Functionality...")
        try:
            # Test economic search
            economic_search_result = session.sql(
                "SELECT CORTEX_SEARCH('ECONOMIC_SEARCH_SERVICE', 'housing market Oslo') LIMIT 1"
            ).collect()
            if economic_search_result:
                validation_results.append("✅ Economic Search: Functional")
            else:
                validation_results.append("⚠️ Economic Search: No results")
                
            # Test compliance search
            compliance_search_result = session.sql(
                "SELECT CORTEX_SEARCH('COMPLIANCE_SEARCH_SERVICE', 'AML assessment') LIMIT 1"
            ).collect()
            if compliance_search_result:
                validation_results.append("✅ Compliance Search: Functional")
            else:
                validation_results.append("⚠️ Compliance Search: No results")
                
        except Exception as e:
            # Search functionality may not be available in all environments
            if "Unknown function CORTEX_SEARCH" in str(e):
                validation_results.append("ℹ️ Banking Search Functionality: CORTEX_SEARCH not available (agents will still work in Snowsight)")
            else:
                validation_results.append(f"⚠️ Banking Search Functionality: {str(e)}")
        
        session.close()
        
        # Print Results
        print("\n" + "="*60)
        print("🎯 AGENT CONFIGURATION READINESS REPORT")
        print("="*60)
        
        success_count = sum(1 for result in validation_results if result.startswith("✅"))
        warning_count = sum(1 for result in validation_results if result.startswith("⚠️"))
        error_count = sum(1 for result in validation_results if result.startswith("❌"))
        info_count = sum(1 for result in validation_results if result.startswith("ℹ️"))
        
        for result in validation_results:
            print(result)
        
        print("\n" + "-"*60)
        print(f"📊 SUMMARY: {success_count} ✅ | {warning_count} ⚠️ | {error_count} ❌ | {info_count} ℹ️")
        
        if error_count == 0:
            print("\n🎉 READY FOR AGENT CONFIGURATION!")
            print("👉 Proceed to Snowsight → AI → Agents to configure your assistants")
            print("📖 Follow AGENT_SETUP_GUIDE.md for detailed instructions")
            if info_count > 0:
                print("ℹ️  Note: Search functionality will be available in Snowsight even if not testable here")
            return True
        else:
            print("\n🚧 INFRASTRUCTURE ISSUES DETECTED")
            print("🔧 Run 'python main.py --step all --connection [CONNECTION_NAME]' to fix issues")
            return False
            
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        print(f"\n❌ VALIDATION FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Agent Readiness")
    parser.add_argument(
        "--connection", 
        default="sfseeurope-mstellwall-aws-us-west3",
        help="Snowflake connection name"
    )
    
    args = parser.parse_args()
    
    success = validate_infrastructure(args.connection)
    sys.exit(0 if success else 1)
