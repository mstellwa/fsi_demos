# src/ai_components/semantic_views.py
# Semantic view creation for Cortex Analyst in Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def create_all_semantic_views(session: Session) -> None:
    """Create REAL semantic views for Cortex Analyst"""
    
    print("   🔍 Creating REAL semantic views for Cortex Analyst...")
    
    # Create EARNINGS_ACTUALS table first
    create_actuals_sql = """
    CREATE OR REPLACE TABLE ENRICHED_DATA.EARNINGS_ACTUALS AS
    SELECT 
        TICKER,
        FISCAL_QUARTER,
        METRIC_NAME,
        ESTIMATE_VALUE * (1 + UNIFORM(-0.1, 0.1, RANDOM())) AS ACTUAL_VALUE
    FROM RAW_DATA.CONSENSUS_ESTIMATES 
    WHERE PROVIDER = 'FactSet'
    """
    session.sql(create_actuals_sql).collect()
    print("   ✅ EARNINGS_ACTUALS table created")
    
    # First verify column names in our tables
    print("   🔍 Verifying column names in source tables...")
    verify_table_columns(session)
    
    # Now create the semantic views
    print("   🔍 Creating EARNINGS_ANALYSIS_VIEW semantic view...")
    create_earnings_analysis_semantic_view(session)
    
    print("   🔍 Creating THEMATIC_RESEARCH_VIEW semantic view...")
    create_thematic_research_semantic_view(session)
    
    print("   🔍 Creating CLIENT_MARKET_IMPACT_VIEW semantic view...")
    create_client_market_impact_semantic_view(session)


def verify_table_columns(session: Session) -> None:
    """Verify actual column names in source tables before creating semantic view"""
    
    tables_to_check = [
        "RAW_DATA.COMPANIES",
        "RAW_DATA.CONSENSUS_ESTIMATES", 
        "ENRICHED_DATA.EARNINGS_ACTUALS"
    ]
    
    for table in tables_to_check:
        try:
            print(f"   📊 Columns in {table}:")
            result = session.sql(f"DESCRIBE TABLE {table}").collect()
            for row in result[:5]:  # Show first 5 columns
                print(f"      - {row['name']} ({row['type']})")
        except Exception as e:
            print(f"      ❌ Error describing {table}: {str(e)}")


def create_earnings_analysis_semantic_view(session: Session) -> None:
    """
    Create SEMANTIC VIEW for earnings analysis - required for Cortex Analyst
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW ANALYTICS.EARNINGS_ANALYSIS_VIEW
	TABLES (
		ACTUALS AS ENRICHED_DATA.EARNINGS_ACTUALS
			PRIMARY KEY (TICKER, FISCAL_QUARTER, METRIC_NAME)
			WITH SYNONYMS=('earnings_results','financial_results','quarterly_results')
			COMMENT='Actual quarterly earnings results for companies',
		ESTIMATES AS RAW_DATA.CONSENSUS_ESTIMATES  
			PRIMARY KEY (TICKER, FISCAL_QUARTER, METRIC_NAME, PROVIDER)
			WITH SYNONYMS=('consensus_estimates','analyst_estimates','forecasts')
			COMMENT='Consensus estimates from financial data providers',
		COMPANIES AS RAW_DATA.COMPANIES
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info')
			COMMENT='Company master data including sector and industry'
	)
	RELATIONSHIPS (
		ACTUALS_TO_COMPANIES AS ACTUALS(TICKER) REFERENCES COMPANIES(TICKER),
		ESTIMATES_TO_COMPANIES AS ESTIMATES(TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		COMPANIES.COMPANY_TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol') COMMENT='Company stock ticker symbol',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation') COMMENT='Full company name',
		COMPANIES.COMPANY_SECTOR AS SECTOR WITH SYNONYMS=('industry_sector','business_sector') COMMENT='Business sector classification',
		COMPANIES.COMPANY_INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line') COMMENT='Industry classification',
		ACTUALS.REPORTING_QUARTER AS FISCAL_QUARTER WITH SYNONYMS=('reporting_period','fiscal_period','period') COMMENT='Fiscal quarter (e.g., 2024-Q1)',
		ACTUALS.FINANCIAL_METRIC AS METRIC_NAME WITH SYNONYMS=('financial_metric','kpi','measure') COMMENT='Financial metric name (Revenue, EPS, Net Income)',
		ESTIMATES.DATA_PROVIDER AS PROVIDER WITH SYNONYMS=('data_provider','research_provider','source') COMMENT='Source of the estimate (FactSet, Bloomberg, etc.)'
	)
	METRICS (
		ACTUALS.TOTAL_ACTUAL AS SUM(ACTUAL_VALUE) WITH SYNONYMS=('total_actual','sum_actual','actual_total') COMMENT='Sum of actual reported financial results',
		ESTIMATES.AVG_ESTIMATE AS AVG(ESTIMATE_VALUE) WITH SYNONYMS=('avg_estimate','mean_consensus','consensus_avg') COMMENT='Average consensus analyst estimate'
	)
	COMMENT='Earnings analysis semantic view for comparing actual results vs consensus estimates';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ EARNINGS_ANALYSIS_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create semantic view: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_thematic_research_semantic_view(session: Session) -> None:
    """
    Create THEMATIC_RESEARCH_VIEW semantic view for thematic investment research
    Supports Global Research & Market Insights scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW ANALYTICS.THEMATIC_RESEARCH_VIEW
	TABLES (
		REPORTS AS RAW_DATA.RESEARCH_REPORTS
			PRIMARY KEY (REPORT_ID)
			WITH SYNONYMS=('research_reports','thematic_reports','analysis')
			COMMENT='Internal research reports with thematic analysis',
		COMPANIES AS RAW_DATA.COMPANIES
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info','firms')
			COMMENT='Company master data with sector and industry classification',
		PRICES AS RAW_DATA.HISTORICAL_STOCK_PRICES
			PRIMARY KEY (TICKER, PRICE_DATE)
			WITH SYNONYMS=('stock_prices','market_data','price_history')
			COMMENT='Historical stock price data for performance analysis',
		NEWS AS RAW_DATA.NEWS_ARTICLES
			PRIMARY KEY (ARTICLE_ID)
			WITH SYNONYMS=('news_articles','market_news','events')
			COMMENT='News articles and market event coverage'
	)
	RELATIONSHIPS (
		PRICES_TO_COMPANIES AS PRICES(TICKER) REFERENCES COMPANIES(TICKER),
		NEWS_TO_COMPANIES AS NEWS(AFFECTED_TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		COMPANIES.COMPANY_TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol') COMMENT='Company stock ticker symbol',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation') COMMENT='Company name',
		COMPANIES.COMPANY_SECTOR AS SECTOR WITH SYNONYMS=('industry_sector','business_sector') COMMENT='Business sector classification',
		COMPANIES.COMPANY_INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line') COMMENT='Industry classification',
		REPORTS.REPORT_TYPE AS REPORT_TYPE WITH SYNONYMS=('analysis_type','research_type') COMMENT='Type of research report',
		REPORTS.THEMES AS THEMATIC_TAGS WITH SYNONYMS=('thematic_tags','investment_themes','topics') COMMENT='Thematic investment tags and topics',
		REPORTS.AUTHOR AS AUTHOR WITH SYNONYMS=('analyst','research_author','writer') COMMENT='Report author name',
		REPORTS.PUBLISHED_DATE AS PUBLISHED_DATE WITH SYNONYMS=('publication_date','report_date') COMMENT='Report publication date',
		PRICES.PRICE_DATE AS PRICE_DATE WITH SYNONYMS=('trade_date','market_date','date') COMMENT='Stock price date',
		NEWS.SOURCE AS SOURCE WITH SYNONYMS=('source','publication','media') COMMENT='News article source'
	)
	METRICS (
		PRICES.AVG_PRICE AS AVG(CLOSE) WITH SYNONYMS=('average_price','mean_price','avg_close') COMMENT='Average stock closing price',
		PRICES.MAX_PRICE AS MAX(CLOSE) WITH SYNONYMS=('highest_price','peak_price','max_close') COMMENT='Maximum stock closing price',
		PRICES.MIN_PRICE AS MIN(CLOSE) WITH SYNONYMS=('lowest_price','bottom_price','min_close') COMMENT='Minimum stock closing price',
		PRICES.TOTAL_VOLUME AS SUM(VOLUME) WITH SYNONYMS=('total_trading_volume','sum_volume','cumulative_volume') COMMENT='Total trading volume',
		COMPANIES.TOTAL_MARKET_CAP AS SUM(MARKET_CAP_BILLIONS) WITH SYNONYMS=('total_market_cap','sum_market_cap','aggregate_cap') COMMENT='Total market capitalization'
	)
	COMMENT='Thematic investment research semantic view for analyzing trends, themes, and cross-sector opportunities';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ THEMATIC_RESEARCH_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create THEMATIC_RESEARCH_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_client_market_impact_semantic_view(session: Session) -> None:
    """
    Create CLIENT_MARKET_IMPACT_VIEW semantic view for client analytics
    Supports Market Structure Reports scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW ANALYTICS.CLIENT_MARKET_IMPACT_VIEW
	TABLES (
		CLIENTS AS RAW_DATA.CLIENT_PROFILES
			PRIMARY KEY (CLIENT_ID)
			WITH SYNONYMS=('client_info','customer_profiles','institutional_clients')
			COMMENT='Client profile information and assets under management',
		TRADING AS RAW_DATA.CLIENT_TRADING_ACTIVITY
			PRIMARY KEY (TRADE_ID)
			WITH SYNONYMS=('client_trades','trading_activity','derivative_trades')
			COMMENT='Client derivative trading activity and clearing details',
		ENGAGEMENT AS RAW_DATA.CLIENT_ENGAGEMENT
			PRIMARY KEY (CLIENT_ID, CONTENT_ID, ENGAGEMENT_TIMESTAMP)
			WITH SYNONYMS=('content_engagement','research_downloads','client_interactions')
			COMMENT='Client engagement with research content and reports',
		DISCUSSIONS AS RAW_DATA.CLIENT_DISCUSSIONS
			PRIMARY KEY (CLIENT_ID, DISCUSSION_DATE)
			WITH SYNONYMS=('client_meetings','strategic_discussions','relationship_management')
			COMMENT='Client discussion and meeting tracking'
	)
	RELATIONSHIPS (
		TRADING_TO_CLIENTS AS TRADING(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID),
		ENGAGEMENT_TO_CLIENTS AS ENGAGEMENT(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID),
		DISCUSSIONS_TO_CLIENTS AS DISCUSSIONS(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID)
	)
	DIMENSIONS (
		CLIENTS.CLIENT_ID AS CLIENT_ID WITH SYNONYMS=('client','customer_id','account_id') COMMENT='Unique client identifier',
		CLIENTS.CLIENT_NAME AS CLIENT_NAME WITH SYNONYMS=('client','customer_name','institution_name') COMMENT='Client organization name',
		CLIENTS.CLIENT_TYPE AS CLIENT_TYPE WITH SYNONYMS=('customer_type','institution_type','client_segment') COMMENT='Type of institutional client',
		CLIENTS.REGION AS REGION WITH SYNONYMS=('geography','location','client_region') COMMENT='Client geographic region',
		TRADING.TRADE_DATE AS TRADE_DATE WITH SYNONYMS=('transaction_date','trading_date') COMMENT='Date of trading activity',
		TRADING.ASSET_CLASS AS ASSET_CLASS WITH SYNONYMS=('product_type','instrument_class') COMMENT='Asset class of derivative trade',
		TRADING.DERIVATIVE_TYPE AS DERIVATIVE_TYPE WITH SYNONYMS=('product','instrument_type','trade_type') COMMENT='Specific derivative instrument type',
		TRADING.CLEARING_CCP AS CLEARING_CCP WITH SYNONYMS=('ccp','clearing_house','central_counterparty') COMMENT='Central counterparty for clearing',
		ENGAGEMENT.ENGAGEMENT_TYPE AS ENGAGEMENT_TYPE WITH SYNONYMS=('interaction_type','content_action') COMMENT='Type of content engagement',
		ENGAGEMENT.CONTENT_ID AS CONTENT_ID WITH SYNONYMS=('report_id','research_id','document_id') COMMENT='Research content identifier',
		DISCUSSIONS.DISCUSSION_TYPE AS DISCUSSION_TYPE WITH SYNONYMS=('meeting_type','interaction_type') COMMENT='Type of client discussion',
		DISCUSSIONS.RELATIONSHIP_MANAGER AS RELATIONSHIP_MANAGER WITH SYNONYMS=('account_manager','rm','contact') COMMENT='Relationship manager name'
	)
	METRICS (
		CLIENTS.TOTAL_AUM AS SUM(AUM_BILLIONS) WITH SYNONYMS=('total_assets','sum_aum','aggregate_assets') COMMENT='Total assets under management',
		TRADING.TOTAL_NOTIONAL AS SUM(NOTIONAL_VALUE) WITH SYNONYMS=('total_trading_volume','sum_notional','aggregate_volume') COMMENT='Total notional trading volume',
		TRADING.TRADE_COUNT AS COUNT(TRADE_ID) WITH SYNONYMS=('number_of_trades','trading_frequency','transaction_count') COMMENT='Count of derivative trades',
		ENGAGEMENT.ENGAGEMENT_COUNT AS COUNT(ENGAGEMENT_TIMESTAMP) WITH SYNONYMS=('content_interactions','download_count','interaction_count') COMMENT='Count of research content engagements',
		DISCUSSIONS.DISCUSSION_COUNT AS COUNT(DISCUSSION_DATE) WITH SYNONYMS=('meeting_count','interaction_frequency') COMMENT='Count of client discussions and meetings'
	)
	COMMENT='Client market impact analysis for personalized research and EMIR 3.0 risk assessment';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ CLIENT_MARKET_IMPACT_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create CLIENT_MARKET_IMPACT_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise