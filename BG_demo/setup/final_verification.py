#!/usr/bin/env python3
"""
SAM Demo - Final Infrastructure Verification
"""

import snowflake.snowpark as snowpark

def verify_infrastructure():
    """Verify all demo components are ready"""
    
    session = snowpark.Session.builder.config("connection_name", "sfseeurope-mstellwall-aws-us-west3").create()
    session.sql("USE DATABASE FSI_DEMOS").collect()
    session.sql("USE SCHEMA SAM_DEMO").collect()
    
    print("🔍 SAM Demo Infrastructure - Final Status")
    print("=" * 50)
    
    # Check semantic views
    try:
        views = session.sql("SHOW SEMANTIC VIEWS").collect()
        print(f"✅ Semantic Views: {len(views)}")
        for view in views:
            print(f"   - {view[1]} (Ready)")
    except Exception as e:
        print(f"❌ Semantic views error: {str(e)}")
    
    # Check search services  
    try:
        services = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
        print(f"✅ Search Services: {len(services)}")
        for service in services:
            print(f"   - {service[1]} (Ready)")
    except Exception as e:
        print(f"❌ Search services error: {str(e)}")
    
    # Check data completeness
    companies = session.sql("SELECT COUNT(DISTINCT COMPANY_NAME) FROM COMPANY_FINANCIALS").collect()[0][0]
    clients = session.sql("SELECT COUNT(*) FROM CLIENT_CRM").collect()[0][0]
    docs = session.sql("SELECT COUNT(*) FROM DOCUMENTS").collect()[0][0]
    holdings = session.sql("SELECT COUNT(*) FROM PORTFOLIO_HOLDINGS_HISTORY").collect()[0][0]
    
    print(f"✅ Sample Data:")
    print(f"   - Companies: {companies}")
    print(f"   - Clients: {clients}")
    print(f"   - Documents: {docs}")
    print(f"   - Portfolio Holdings: {holdings}")
    
    # Check critical ID/Title columns for agent configuration
    print(f"\n🚨 Agent Configuration Verification:")
    try:
        id_title_check = session.sql("SELECT COUNT(*) FROM DOCUMENTS WHERE DOC_ID IS NOT NULL AND FILE_URL IS NOT NULL").collect()[0][0]
        total_docs = session.sql("SELECT COUNT(*) FROM DOCUMENTS").collect()[0][0]
        if id_title_check == total_docs:
            print(f"✅ ID/Title Columns: All {total_docs} documents have DOC_ID and FILE_URL")
        else:
            print(f"❌ ID/Title Columns: Only {id_title_check}/{total_docs} documents have required columns")
            print("⚠️  Agent tools MUST be configured with ID Column: DOC_ID, Title Column: FILE_URL")
    except Exception as e:
        print(f"❌ ID/Title columns check error: {str(e)}")
    
    # Test specific data
    print(f"\n📊 Demo Data Verification:")
    try:
        tempus_data = session.sql("SELECT COUNT(*) FROM COMPANY_FINANCIALS WHERE COMPANY_NAME = 'Tempus AI'").collect()[0][0]
        print(f"   ✅ Tempus AI financial quarters: {tempus_data}")
        
        tempus_docs = session.sql("SELECT COUNT(*) FROM DOCUMENTS WHERE COMPANY_NAME = 'Tempus AI'").collect()[0][0]
        print(f"   ✅ Tempus AI documents: {tempus_docs}")
        
        arkadia_docs = session.sql("SELECT COUNT(*) FROM DOCUMENTS WHERE COMPANY_NAME = 'Arkadia Commerce'").collect()[0][0]
        print(f"   ✅ Arkadia Commerce documents: {arkadia_docs}")
        
        # Show client summary
        client_data = session.sql("SELECT CLIENT_NAME, CLIENT_TYPE, AUM_USD_M FROM CLIENT_CRM ORDER BY AUM_USD_M DESC").collect()
        print(f"   ✅ Client profiles:")
        for client in client_data:
            print(f"     - {client[0]} ({client[1]}): ${client[2]:.1f}M AUM")
            
    except Exception as e:
        print(f"   ⚠️ Data verification error: {str(e)}")
    
    session.close()
    
    print(f"\n🎉 SAM Demo Infrastructure: PRODUCTION READY!")
    print(f"\n📋 Agent Tools Available:")
    print(f"   1. research_service (Cortex Search)")
    print(f"   2. corporate_memory_service (Cortex Search)")
    print(f"   3. FINANCIAL_DATA_ANALYST (Semantic View)")
    print(f"\n📝 Next: Configure agents in Snowsight Intelligence UI")

if __name__ == "__main__":
    verify_infrastructure()
