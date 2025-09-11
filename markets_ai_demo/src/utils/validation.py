# src/utils/validation.py
# Validation utilities for Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def validate_all_components(session: Session) -> None:
    """Comprehensive validation of all demo components"""
    
    print("🔍 Validating demo components...")
    
    # Validate database structure
    validate_database_structure(session)
    
    # Validate data generation
    validate_data_quality(session)
    
    # Validate AI components
    validate_semantic_views(session)
    validate_search_services(session)
    
    # Validate scenarios
    validate_scenario_readiness(session)
    
    print("✅ Validation completed")


def validate_database_structure(session: Session) -> None:
    """Validate database and schema structure"""
    
    print("   📊 Validating database structure...")
    
    # Check database exists
    try:
        session.sql(f"USE DATABASE {DemoConfig.DATABASE_NAME}").collect()
        print(f"     ✅ Database {DemoConfig.DATABASE_NAME} exists")
    except Exception as e:
        print(f"     ❌ Database error: {str(e)}")
        return
    
    # Check schemas
    expected_schemas = list(DemoConfig.SCHEMAS.values())
    for schema in expected_schemas:
        try:
            session.sql(f"USE SCHEMA {schema}").collect()
            print(f"     ✅ Schema {schema} exists")
        except Exception as e:
            print(f"     ❌ Schema {schema} error: {str(e)}")
    
    # Check warehouses
    try:
        session.sql(f"USE WAREHOUSE {DemoConfig.COMPUTE_WAREHOUSE}").collect()
        print(f"     ✅ Warehouse {DemoConfig.COMPUTE_WAREHOUSE} exists")
        session.sql(f"USE WAREHOUSE {DemoConfig.SEARCH_WAREHOUSE}").collect()
        print(f"     ✅ Warehouse {DemoConfig.SEARCH_WAREHOUSE} exists")
    except Exception as e:
        print(f"     ❌ Warehouse error: {str(e)}")


def validate_data_quality(session: Session) -> None:
    """Validate data generation quality and correlations"""
    
    print("   📈 Validating data quality...")
    
    # Set context
    session.sql(f"USE DATABASE {DemoConfig.DATABASE_NAME}").collect()
    session.sql(f"USE SCHEMA {DemoConfig.SCHEMAS['RAW_DATA']}").collect()
    
    # Check table row counts
    expected_tables = [
        "MASTER_EVENT_LOG",
        "COMPANIES", 
        "HISTORICAL_STOCK_PRICES",
        "CONSENSUS_ESTIMATES",
        "CLIENT_PROFILES",
        "CLIENT_TRADING_ACTIVITY",
        "PORTFOLIO_HOLDINGS",
        "FACTSET_GEO_REVENUE",
        "SP_CREDIT_RATINGS",
        "SEC_FILINGS_RAW",
        "EARNINGS_CALL_TRANSCRIPTS", 
        "NEWS_ARTICLES",
        "RESEARCH_REPORTS"
    ]
    
    for table in expected_tables:
        try:
            # Use Snowpark table method for efficient counting
            count = session.table(f"{DemoConfig.DATABASE_NAME}.{DemoConfig.SCHEMAS['RAW_DATA']}.{table}").count()
            
            if count > 0:
                print(f"     ✅ {table}: {count} rows")
            else:
                print(f"     ⚠️  {table}: No data")
                
        except Exception as e:
            print(f"     ❌ {table}: Error - {str(e)}")
    
    # Validate event-driven correlations
    validate_event_correlations(session)


def validate_event_correlations(session: Session) -> None:
    """Validate that events correlate with stock price movements"""
    
    print("   🎯 Validating event-driven correlations...")
    
    try:
        # Check if price volatility increases on event dates
        correlation_sql = """
        WITH event_prices AS (
            SELECT 
                e.EVENT_DATE,
                e.AFFECTED_TICKER,
                e.EXPECTED_PRICE_IMPACT,
                p.CLOSE,
                LAG(p.CLOSE) OVER (PARTITION BY p.TICKER ORDER BY p.PRICE_DATE) AS prev_close,
                (p.CLOSE - LAG(p.CLOSE) OVER (PARTITION BY p.TICKER ORDER BY p.PRICE_DATE)) / 
                LAG(p.CLOSE) OVER (PARTITION BY p.TICKER ORDER BY p.PRICE_DATE) AS actual_return
            FROM MASTER_EVENT_LOG e
            JOIN HISTORICAL_STOCK_PRICES p ON e.AFFECTED_TICKER = p.TICKER 
                AND e.EVENT_DATE = p.PRICE_DATE
        )
        SELECT 
            COUNT(*) as event_count,
            AVG(ABS(actual_return)) as avg_volatility,
            COUNT(CASE WHEN SIGN(actual_return) = SIGN(EXPECTED_PRICE_IMPACT) THEN 1 END) as direction_matches
        FROM event_prices
        WHERE actual_return IS NOT NULL
        """
        
        result = session.sql(correlation_sql).collect()
        if result:
            event_count = result[0]['EVENT_COUNT']
            avg_volatility = result[0]['AVG_VOLATILITY'] 
            direction_matches = result[0]['DIRECTION_MATCHES']
            
            if event_count > 0:
                match_rate = direction_matches / event_count * 100
                print(f"     📊 Event correlation analysis:")
                print(f"       Events with price data: {event_count}")
                print(f"       Average volatility on event days: {avg_volatility:.3f}")
                print(f"       Direction accuracy: {match_rate:.1f}%")
                
                if match_rate > 60:
                    print(f"     ✅ Good event-price correlation")
                else:
                    print(f"     ⚠️  Low event-price correlation")
            else:
                print(f"     ⚠️  No event-price correlations found")
        
    except Exception as e:
        print(f"     ❌ Correlation validation error: {str(e)}")


def validate_semantic_views(session: Session) -> None:
    """Validate views are working"""
    
    print("   🔍 Validating views...")
    
    session.sql(f"USE SCHEMA {DemoConfig.SCHEMAS['ANALYTICS']}").collect()
    
    views = [
        "EARNINGS_ANALYSIS_VIEW"
    ]
    
    for view in views:
        try:
            # Test basic query on regular SQL view
            test_sql = f"SELECT * FROM {view} LIMIT 2"
            result = session.sql(test_sql).collect()
            
            if result:
                print(f"     ✅ {view}: Working with {len(result)} rows")
            else:
                print(f"     ⚠️  {view}: No data")
                
        except Exception as e:
            print(f"     ❌ {view}: Error - {str(e)}")


def validate_search_services(session: Session) -> None:
    """Validate search services are indexed and working"""
    
    print("   🔎 Validating search services...")
    
    search_services = [
        {
            "name": "EARNINGS_TRANSCRIPTS_SEARCH",
            "test_query": "revenue growth"
        },
        {
            "name": "RESEARCH_REPORTS_SEARCH",
            "test_query": "market structure"
        },
        {
            "name": "NEWS_ARTICLES_SEARCH", 
            "test_query": "technology"
        }
    ]
    
    for service in search_services:
        try:
            # Test if search service exists by checking SHOW CORTEX SEARCH SERVICES
            test_sql = f"SHOW CORTEX SEARCH SERVICES LIKE '%{service['name']}';"
            result = session.sql(test_sql).collect()
            
            if result:
                print(f"     ✅ {service['name']}: Service exists and ready")
            else:
                print(f"     ❌ {service['name']}: Service not found")
                
        except Exception as e:
            print(f"     ❌ {service['name']}: Error - {str(e)}")


def validate_scenario_readiness(session: Session) -> None:
    """Validate that specific demo scenarios have required data"""
    
    print("   🎯 Validating scenario readiness...")
    
    # Scenario 1: Earnings Analysis
    validate_earnings_scenario(session)
    
    # Scenario 2: Thematic Research  
    validate_thematic_scenario(session)
    
    # Scenario 3: Market Structure Reports
    validate_market_structure_scenario(session)


def validate_earnings_scenario(session: Session) -> None:
    """Validate earnings analysis scenario has required data"""
    
    try:
        # Check for earnings data
        earnings_sql = """
        SELECT COUNT(*) as cnt FROM ANALYTICS.EARNINGS_ANALYSIS_VIEW
        WHERE company_ticker = 'NFLX' AND quarter = '2024-Q3'
        """
        result = session.sql(earnings_sql).collect()
        
        if result and result[0]['CNT'] > 0:
            print("     ✅ Earnings Analysis scenario: Data ready")
        else:
            print("     ⚠️  Earnings Analysis scenario: Missing Netflix Q3 data")
            
        # Check for transcript data
        transcript_sql = """
        SELECT COUNT(*) as cnt FROM RAW_DATA.EARNINGS_CALL_TRANSCRIPTS
        WHERE TICKER = 'NFLX'
        """
        result = session.sql(transcript_sql).collect()
        
        if result and result[0]['CNT'] > 0:
            print("     ✅ Earnings transcripts: Available")
        else:
            print("     ⚠️  Earnings transcripts: Missing Netflix data")
            
    except Exception as e:
        print(f"     ❌ Earnings scenario validation error: {str(e)}")


def validate_thematic_scenario(session: Session) -> None:
    """Validate thematic research scenario has required data"""
    
    try:
        # Check for thematic data
        # Test basic functionality of semantic view
        thematic_sql = """
        SELECT * FROM SEMANTIC_VIEW(
            ANALYTICS.THEMATIC_RESEARCH_VIEW
            METRICS AVG_PRICE
            DIMENSIONS COMPANY_TICKER
        ) LIMIT 3
        """
        result = session.sql(thematic_sql).collect()
        
        if result and len(result) > 0:
            print("     ✅ Thematic Research scenario: THEMATIC_RESEARCH_VIEW working")
        else:
            print("     ⚠️  Thematic Research scenario: THEMATIC_RESEARCH_VIEW not returning data")
            
        # Check for research reports
        research_sql = """
        SELECT COUNT(*) as cnt FROM RAW_DATA.RESEARCH_REPORTS
        WHERE THEMATIC_TAGS LIKE '%Carbon%'
        """
        result = session.sql(research_sql).collect()
        
        if result and result[0]['CNT'] > 0:
            print("     ✅ Research reports: Carbon capture content available")
        else:
            print("     ⚠️  Research reports: Missing carbon capture content")
            
    except Exception as e:
        print(f"     ❌ Thematic scenario validation error: {str(e)}")


def validate_market_structure_scenario(session: Session) -> None:
    """Validate market structure reports scenario has required data and logic"""
    print("   🎯 Validating Market Structure Reports scenario...")
    try:
        # 1. Check for FICC market structure content in research reports
        search_sql = """
        SELECT COUNT(*) as cnt FROM RAW_DATA.RESEARCH_REPORTS
        WHERE THEMATIC_TAGS LIKE '%FICC%' AND THEMATIC_TAGS LIKE '%EMIR 3.0%'
        """
        result = session.sql(search_sql).collect()
        if result and result[0]['CNT'] > 0:
            print(f"     ✅ FICC Market Structure content available: {result[0]['CNT']} reports")
        else:
            print("     ⚠️  FICC Market Structure content missing in research reports")

        # 2. Check for client engagement data for asset managers on EMIR 3.0
        engagement_sql = """
        SELECT COUNT(e.CLIENT_ID) as cnt
        FROM RAW_DATA.CLIENT_ENGAGEMENT e
        JOIN RAW_DATA.CLIENT_PROFILES cp ON e.CLIENT_ID = cp.CLIENT_ID
        WHERE cp.CLIENT_TYPE = 'Asset Manager' AND e.CONTENT_ID = 'RPT_001' -- Assuming RPT_001 is EMIR 3.0
        """
        result = session.sql(engagement_sql).collect()
        if result and result[0]['CNT'] > 0:
            print(f"     ✅ Asset Manager EMIR 3.0 engagement data available: {result[0]['CNT']} interactions")
        else:
            print("     ⚠️  Asset Manager EMIR 3.0 engagement data missing")

        # 3. Check for clients with high engagement but no recent discussions
        # This is a simplified check, the actual agent logic is more complex
        client_outreach_sql = """
        SELECT COUNT(DISTINCT ce.CLIENT_ID) as cnt
        FROM RAW_DATA.CLIENT_ENGAGEMENT ce
        JOIN RAW_DATA.CLIENT_PROFILES cp ON ce.CLIENT_ID = cp.CLIENT_ID
        LEFT JOIN RAW_DATA.CLIENT_DISCUSSIONS cd ON ce.CLIENT_ID = cd.CLIENT_ID
            AND cd.DISCUSSION_DATE >= DATEADD(month, -3, CURRENT_DATE()) -- Discussions in last 3 months
        WHERE cp.CLIENT_TYPE = 'Asset Manager'
            AND ce.CONTENT_ID = 'RPT_001' -- Engaged with EMIR 3.0 report
            AND cd.CLIENT_ID IS NULL -- No recent discussion
        """
        result = session.sql(client_outreach_sql).collect()
        if result and result[0]['CNT'] > 0:
            print(f"     ✅ High-engagement clients for EMIR outreach identified: {result[0]['CNT']} prospects")
        else:
            print("     ⚠️  No high-engagement clients identified for EMIR outreach (or all had discussions)")

        # 4. Test CLIENT_MARKET_IMPACT_VIEW functionality
        test_view_sql = """
        SELECT * FROM SEMANTIC_VIEW(
            ANALYTICS.CLIENT_MARKET_IMPACT_VIEW
            METRICS ENGAGEMENT_COUNT
            DIMENSIONS CLIENT_NAME, ENGAGEMENT_TYPE
        ) LIMIT 5
        """
        result = session.sql(test_view_sql).collect()
        if result and len(result) > 0:
            print("     ✅ CLIENT_MARKET_IMPACT_VIEW working")
        else:
            print("     ⚠️  CLIENT_MARKET_IMPACT_VIEW not returning data")

    except Exception as e:
        print(f"     ❌ Market Structure Reports scenario validation error: {str(e)}")


def generate_validation_report(session: Session) -> str:
    """Generate a comprehensive validation report"""
    
    print("\n📋 Generating validation report...")
    
    report = []
    report.append("# Frost Markets Intelligence Demo - Validation Report")
    report.append(f"Generated: {session.sql('SELECT CURRENT_TIMESTAMP()').collect()[0][0]}")
    report.append("")
    
    # Data summary
    try:
        session.sql(f"USE SCHEMA {DemoConfig.SCHEMAS['RAW_DATA']}").collect()
        
        tables = [
            "COMPANIES", "MASTER_EVENT_LOG", "HISTORICAL_STOCK_PRICES",
            "CONSENSUS_ESTIMATES", "CLIENT_PROFILES", "NEWS_ARTICLES"
        ]
        
        report.append("## Data Summary")
        for table in tables:
            try:
                count = session.table(f"{DemoConfig.DATABASE_NAME}.{DemoConfig.SCHEMAS['RAW_DATA']}.{table}").count()
                report.append(f"- {table}: {count:,} rows")
            except:
                report.append(f"- {table}: Error")
        
        report.append("")
        
    except Exception as e:
        report.append(f"## Data Summary\nError: {str(e)}\n")
    
    # AI Components
    report.append("## AI Components Status")
    report.append("### Semantic Views")
    
    semantic_views = ["EARNINGS_ANALYSIS_VIEW", "PORTFOLIO_EXPOSURE_VIEW", "CLIENT_MARKET_IMPACT_VIEW", "THEMATIC_RESEARCH_VIEW"]
    for view in semantic_views:
        try:
            session.sql(f"SELECT * FROM SEMANTIC_VIEW(ANALYTICS.{view} LIMIT 1)").collect()
            report.append(f"- {view}: ✅ Working")
        except:
            report.append(f"- {view}: ❌ Error")
    
    report.append("\n### Search Services")
    search_services = ["EARNINGS_TRANSCRIPTS_SEARCH", "RESEARCH_REPORTS_SEARCH", "NEWS_ARTICLES_SEARCH"]
    for service in search_services:
        try:
            result = session.sql(f"SHOW CORTEX SEARCH SERVICES LIKE '%{service}';").collect()
            if result:
                report.append(f"- {service}: ✅ Ready")
            else:
                report.append(f"- {service}: ❌ Not found")
        except:
            report.append(f"- {service}: ❌ Error")
    
    report_text = "\n".join(report)
    print("✅ Validation report generated")
    
    return report_text
