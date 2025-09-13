"""
AI Components Builder for SAM Demo

This module creates AI components including:
- Semantic views for Cortex Analyst
- Cortex Search services for document types
- Validation and testing of AI components
"""

from snowflake.snowpark import Session
from typing import List
import config

def build_all(session: Session, scenarios: List[str], build_semantic: bool = True, build_search: bool = True):
    """
    Build AI components for the specified scenarios.
    
    Args:
        session: Active Snowpark session
        scenarios: List of scenario names
        build_semantic: Whether to build semantic views
        build_search: Whether to build search services
    """
    print("🤖 Starting AI components build...")
    
    if build_semantic:
        print("🧠 Building semantic views...")
        create_semantic_views(session)
    
    if build_search:
        print("🔍 Building Cortex Search services...")
        create_search_services(session, scenarios)
    
    # Validate components
    print("✅ Validating AI components...")
    validate_components(session, build_semantic, build_search)
    
    print("✅ AI components build complete")

def create_semantic_views(session: Session):
    """Create the master semantic view for Cortex Analyst using correct Snowflake syntax."""
    
    try:
        # Create proper semantic view with correct syntax patterns
        session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Daily portfolio holdings and positions. Each portfolio holding has multiple rows. When no time period is provided always get the latest value by date.',
		PORTFOLIOS AS {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Investment portfolios and fund information',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate hierarchy data'
	)
	RELATIONSHIPS (
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID)
	)
	DIMENSIONS (
		-- Portfolio dimensions
		PORTFOLIOS.PORTFOLIONAME AS PortfolioName WITH SYNONYMS=('fund_name','strategy_name','portfolio_name') COMMENT='Portfolio or fund name',
		PORTFOLIOS.STRATEGY AS Strategy WITH SYNONYMS=('investment_strategy','portfolio_strategy') COMMENT='Investment strategy type',
		
		-- Security dimensions  
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','security_name','description') COMMENT='Security description or company name',
		SECURITIES.PRIMARYTICKER AS Ticker WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker') COMMENT='Primary trading symbol',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('instrument_type','security_type','asset_class') COMMENT='Asset class: Equity, Corporate Bond, ETF',
		
		-- Issuer dimensions (for enhanced analysis)
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer_name','legal_name','company_name') COMMENT='Legal issuer name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics_sector') COMMENT='GICS Level 1 sector classification',
		ISSUERS.COUNTRYOFINCORPORATION AS CountryOfIncorporation WITH SYNONYMS=('domicile','country_of_risk','country') COMMENT='Country of incorporation',
		
		-- Time dimensions
		HOLDINGS.HOLDINGDATE AS HoldingDate WITH SYNONYMS=('position_date','as_of_date','date') COMMENT='Holdings as-of date'
	)
	METRICS (
		-- Core position metrics
		HOLDINGS.TOTAL_MARKET_VALUE AS SUM(MarketValue_Base) WITH SYNONYMS=('exposure','total_exposure','aum','market_value','position_value') COMMENT='Total market value in base currency',
		HOLDINGS.HOLDING_COUNT AS COUNT(SecurityID) WITH SYNONYMS=('position_count','number_of_holdings','holding_count','count') COMMENT='Count of portfolio positions',
		
		-- Portfolio weight metrics  
		HOLDINGS.PORTFOLIO_WEIGHT AS SUM(PortfolioWeight) WITH SYNONYMS=('weight','allocation','portfolio_weight') COMMENT='Portfolio weight as decimal',
		HOLDINGS.PORTFOLIO_WEIGHT_PCT AS SUM(PortfolioWeight) * 100 WITH SYNONYMS=('weight_percent','allocation_percent','percentage_weight') COMMENT='Portfolio weight as percentage',
		
		-- Issuer-level metrics (enhanced capability)
		HOLDINGS.ISSUER_EXPOSURE AS SUM(MarketValue_Base) WITH SYNONYMS=('issuer_total','issuer_value','issuer_exposure') COMMENT='Total exposure to issuer across all securities',
		
		-- Concentration metrics
		HOLDINGS.MAX_POSITION_WEIGHT AS MAX(PortfolioWeight) WITH SYNONYMS=('largest_position','max_weight','concentration') COMMENT='Largest single position weight'
	)
	COMMENT='Multi-asset semantic view for portfolio analytics with issuer hierarchy support';
        """).collect()
        
        print("✅ Created semantic view: SAM_ANALYST_VIEW")
        
    except Exception as e:
        print(f"❌ Failed to create semantic view: {e}")
        raise
    
    # Create additional semantic view for research with fundamentals data
    try:
        print("📊 Creating research semantic view with fundamentals...")
        create_research_semantic_view(session)
    except Exception as e:
        print(f"⚠️  Warning: Could not create research semantic view: {e}")
        # Don't raise - this is optional enhancement

def create_research_semantic_view(session: Session):
    """Create semantic view for research with fundamentals and estimates data."""
    
    # First check if the fundamentals tables exist
    try:
        session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS LIMIT 1").collect()
        session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES LIMIT 1").collect()
    except:
        print("⚠️  Fundamentals tables not found, skipping research view creation")
        return
    
    # Create the research-focused semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_RESEARCH_VIEW
	TABLES (
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','equities','securities') 
			COMMENT='Security master data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate data',
		FUNDAMENTALS AS {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS
			PRIMARY KEY (SECURITY_ID, REPORTING_DATE, METRIC_NAME)
			WITH SYNONYMS=('financials','earnings','results','fundamentals')
			COMMENT='Company financial fundamentals',
		ESTIMATES AS {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES
			PRIMARY KEY (SECURITY_ID, ESTIMATE_DATE, FISCAL_PERIOD, METRIC_NAME) 
			WITH SYNONYMS=('forecasts','estimates','guidance','consensus') 
			COMMENT='Analyst estimates and guidance'
	)
	RELATIONSHIPS (
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID),
		FUNDAMENTALS_TO_SECURITIES AS FUNDAMENTALS(SECURITY_ID) REFERENCES SECURITIES(SECURITYID),
		ESTIMATES_TO_SECURITIES AS ESTIMATES(SECURITY_ID) REFERENCES SECURITIES(SECURITYID)
	)
	DIMENSIONS (
		-- Security dimensions  
		SECURITIES.PRIMARYTICKER AS Ticker WITH SYNONYMS=('ticker','symbol','ticker_symbol') COMMENT='Trading ticker symbol',
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','name','security_name') COMMENT='Company name',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('type','security_type','asset_class') COMMENT='Asset class',
		
		-- Issuer dimensions
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer','legal_name','entity_name') COMMENT='Legal entity name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics') COMMENT='GICS sector',
		ISSUERS.COUNTRYOFINCORPORATION AS CountryOfIncorporation WITH SYNONYMS=('domicile','country','headquarters') COMMENT='Country of incorporation',
		
		-- Fundamentals dimensions
		FUNDAMENTALS.REPORTING_DATE AS REPORTING_DATE WITH SYNONYMS=('report_date','earnings_date','date') COMMENT='Financial reporting date',
		FUNDAMENTALS.FISCAL_QUARTER AS FISCAL_QUARTER WITH SYNONYMS=('quarter','period','fiscal_period') COMMENT='Fiscal quarter',
		FUNDAMENTALS.METRIC_NAME AS METRIC_NAME WITH SYNONYMS=('metric','measure','financial_metric') COMMENT='Financial metric name',
		
		-- Estimates dimensions
		ESTIMATES.FISCAL_PERIOD AS FISCAL_PERIOD WITH SYNONYMS=('forecast_period','estimate_quarter') COMMENT='Estimate fiscal period'
	)
	METRICS (
		-- Actual financial metrics
		FUNDAMENTALS.ACTUAL_VALUE AS SUM(METRIC_VALUE) WITH SYNONYMS=('actual','reported','result') COMMENT='Actual reported value',
		
		-- Estimate metrics
		ESTIMATES.ESTIMATE_VALUE AS SUM(ESTIMATE_VALUE) WITH SYNONYMS=('estimate','forecast','consensus') COMMENT='Consensus estimate value',
		ESTIMATES.GUIDANCE_LOW AS MIN(GUIDANCE_LOW) WITH SYNONYMS=('guidance_low','low_guidance') COMMENT='Low end of guidance',
		ESTIMATES.GUIDANCE_HIGH AS MAX(GUIDANCE_HIGH) WITH SYNONYMS=('guidance_high','high_guidance') COMMENT='High end of guidance',
		
		-- Count metrics
		FUNDAMENTALS.METRIC_COUNT AS COUNT(DISTINCT FUNDAMENTALS.METRIC_NAME) WITH SYNONYMS=('metric_count','measures_count') COMMENT='Count of financial metrics',
		ESTIMATES.ESTIMATE_COUNT AS COUNT(DISTINCT ESTIMATES.METRIC_NAME) WITH SYNONYMS=('estimate_count','forecasts_count') COMMENT='Count of estimate metrics'
	)
	COMMENT='Research semantic view with fundamentals and estimates for earnings analysis';
    """).collect()
    
    print("✅ Created semantic view: SAM_RESEARCH_VIEW")

def create_search_services(session: Session, scenarios: List[str]):
    """Create Cortex Search services for required document types."""
    
    # Determine required document types from scenarios
    required_doc_types = set()
    for scenario in scenarios:
        if scenario in config.SCENARIO_DATA_REQUIREMENTS:
            required_doc_types.update(config.SCENARIO_DATA_REQUIREMENTS[scenario])
    
    print(f"Creating search services for: {list(required_doc_types)}")
    
    # Create search service for each required document type
    for doc_type in required_doc_types:
        if doc_type in config.DOCUMENT_TYPES:
            corpus_table = f"{config.DATABASE_NAME}.CURATED.{config.DOCUMENT_TYPES[doc_type]['corpus_name']}"
            service_name = config.DOCUMENT_TYPES[doc_type]['search_service']
            
            try:
                # Use dedicated Cortex Search warehouse
                from config import CORTEX_SEARCH_WAREHOUSE, CORTEX_SEARCH_TARGET_LAG
                search_warehouse = CORTEX_SEARCH_WAREHOUSE
                
                # Create enhanced Cortex Search service with SecurityID and IssuerID attributes
                # Using configurable TARGET_LAG for demo environments to see changes quickly
                session.sql(f"""
                    CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.{service_name}
                        ON DOCUMENT_TEXT
                        ATTRIBUTES DOCUMENT_TITLE, SecurityID, IssuerID, DOCUMENT_TYPE, PUBLISH_DATE, LANGUAGE
                        WAREHOUSE = {search_warehouse}
                        TARGET_LAG = '{CORTEX_SEARCH_TARGET_LAG}'
                        AS 
                        SELECT 
                            DOCUMENT_ID,
                            DOCUMENT_TITLE,
                            DOCUMENT_TEXT,
                            SecurityID,
                            IssuerID,
                            DOCUMENT_TYPE,
                            PUBLISH_DATE,
                            LANGUAGE
                        FROM {corpus_table}
                """).collect()
                
                print(f"✅ Created search service: {service_name}")
                
            except Exception as e:
                print(f"❌ Failed to create search service {service_name}: {e}")
                continue

def validate_components(session: Session, semantic_built: bool, search_built: bool):
    """Validate that AI components are working correctly."""
    
    if semantic_built:
        print("🔍 Testing semantic view...")
        try:
            # Test semantic view using proper SEMANTIC_VIEW() function with correct metric names
            test_query = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE
                    DIMENSIONS PORTFOLIONAME
                )
                LIMIT 5
            """
            result = session.sql(test_query).collect()
            print(f"✅ Semantic view query test passed: {len(result)} results")
            
            # Test DESCRIBE SEMANTIC VIEW
            describe_result = session.sql(f"DESCRIBE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW").collect()
            print(f"✅ Semantic view structure validated: {len(describe_result)} components")
            
            # Test with multiple metrics and dimensions
            advanced_test = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE, HOLDING_COUNT
                    DIMENSIONS DESCRIPTION, GICS_SECTOR
                )
                LIMIT 10
            """
            advanced_result = session.sql(advanced_test).collect()
            print(f"✅ Advanced semantic view test passed: {len(advanced_result)} records")
            
        except Exception as e:
            print(f"❌ Semantic view validation failed: {e}")
            # Don't raise - continue with search services
    
    if search_built:
        print("🔍 Testing search services...")
        try:
            # Get list of search services using correct SHOW command
            ai_objects = session.sql(f'SHOW CORTEX SEARCH SERVICES IN {config.DATABASE_NAME}.AI').collect()
            
            print(f"Found {len(ai_objects)} search services to test")
            
            # Test each search service using your example syntax (without schema prefix in OVER clause)
            for service in ai_objects:
                service_name = service['name']
                try:
                    test_result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                            '{config.DATABASE_NAME}.AI.{service_name}',
                            '{{"query": "technology investment", "limit": 2}}'
                        ) 
                    """).collect()
                    print(f"✅ Search service test passed: {service_name}")
                except Exception as e:
                    print(f"❌ Search service test failed for {service_name}: {e}")
                    
        except Exception as e:
            print(f"❌ Search services validation failed: {e}")
    
    print("✅ AI component validation complete")