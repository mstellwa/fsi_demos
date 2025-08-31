"""
Creator for Cortex Intelligence objects (Search services and Semantic Views).
"""

import logging
from snowflake.snowpark import Session
from config import DB_NAME, RAW_SCHEMA, ANALYTICS_SCHEMA, WAREHOUSE

logger = logging.getLogger(__name__)

class CortexObjectsCreator:
    """Creates and manages Cortex Search services and Semantic Views."""
    
    def __init__(self, session: Session):
        self.session = session
        
    def create_cortex_search_services(self):
        """Create all Cortex Search services."""
        logger.info("Creating Cortex Search services...")
        
        # Switch to ANALYTICS schema
        self.session.sql(f"USE DATABASE {DB_NAME}").collect()
        self.session.sql(f"USE SCHEMA {ANALYTICS_SCHEMA}").collect()
        
        # 1. Factset News Search Service
        logger.info("Creating FACTSET_NEWS_SEARCH service...")
        try:
            self.session.sql(f"""
                CREATE OR REPLACE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.FACTSET_NEWS_SEARCH
                    ON ARTICLE_BODY
                    ATTRIBUTES HEADLINE, PUBLISH_TIMESTAMP, SOURCE, COMPANY_ID, LANG
                    WAREHOUSE = {WAREHOUSE}
                    TARGET_LAG = '10 minutes'
                    AS 
                    SELECT 
                        ARTICLE_ID,
                        HEADLINE AS TITLE,
                        ARTICLE_BODY AS CONTENT,
                        PUBLISH_TIMESTAMP,
                        SOURCE,
                        COMPANY_ID,
                        LANG
                    FROM {DB_NAME}.{RAW_SCHEMA}.FACTSET_NEWS_FEED
            """).collect()
        except Exception as e:
            logger.warning(f"Failed to create FACTSET_NEWS_SEARCH: {e}")
            # Try alternative approach - drop first if exists
            try:
                self.session.sql(f"DROP CORTEX SEARCH SERVICE IF EXISTS {DB_NAME}.{ANALYTICS_SCHEMA}.FACTSET_NEWS_SEARCH").collect()
                self.session.sql(f"""
                    CREATE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.FACTSET_NEWS_SEARCH
                        ON ARTICLE_BODY
                        WAREHOUSE = {WAREHOUSE}
                        TARGET_LAG = '10 minutes'
                        AS 
                        SELECT 
                            ARTICLE_ID,
                            HEADLINE,
                            ARTICLE_BODY,
                            PUBLISH_TIMESTAMP,
                            SOURCE,
                            COMPANY_ID,
                            LANG
                        FROM {DB_NAME}.{RAW_SCHEMA}.FACTSET_NEWS_FEED
                """).collect()
            except Exception as e2:
                logger.error(f"Failed to create FACTSET_NEWS_SEARCH even after drop: {e2}")
                raise
        
        # 2. Guidepoint Expert Transcripts Search Service
        logger.info("Creating GUIDEPOINT_TRANSCRIPTS_SEARCH service...")
        self.session.sql(f"""
            CREATE OR REPLACE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.GUIDEPOINT_TRANSCRIPTS_SEARCH
                ON TRANSCRIPT_TEXT
                ATTRIBUTES TITLE, INTERVIEW_DATE, EXPERT_PROFILE, COMPANY_ID
                WAREHOUSE = {WAREHOUSE}
                TARGET_LAG = '10 minutes'
                AS 
                SELECT 
                    TRANSCRIPT_ID,
                    TITLE,
                    TRANSCRIPT_TEXT AS CONTENT,
                    INTERVIEW_DATE,
                    EXPERT_PROFILE,
                    COMPANY_ID
                FROM {DB_NAME}.{RAW_SCHEMA}.GUIDEPOINT_EXPERT_TRANSCRIPTS
        """).collect()
        
        # 3. McBainCG Consultant Reports Search Service
        logger.info("Creating MCBAINCG_REPORTS_SEARCH service...")
        self.session.sql(f"""
            CREATE OR REPLACE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.MCBAINCG_REPORTS_SEARCH
                ON REPORT_BODY
                ATTRIBUTES TITLE, PUBLISH_DATE, EXECUTIVE_SUMMARY
                WAREHOUSE = {WAREHOUSE}
                TARGET_LAG = '10 minutes'
                AS 
                SELECT 
                    REPORT_ID,
                    TITLE,
                    REPORT_BODY AS CONTENT,
                    PUBLISH_DATE,
                    EXECUTIVE_SUMMARY,
                    NULL AS COMPANY_ID
                FROM {DB_NAME}.{RAW_SCHEMA}.MCBAINCG_CONSULTANT_REPORTS
        """).collect()
        
        # 4. Quartr Earnings Calls Search Service
        logger.info("Creating QUARTR_EARNINGS_CALLS_SEARCH service...")
        self.session.sql(f"""
            CREATE OR REPLACE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.QUARTR_EARNINGS_CALLS_SEARCH
                ON TRANSCRIPT_JSON
                ATTRIBUTES TITLE, COMPANY_ID, CALL_TIMESTAMP, REPORTING_PERIOD
                WAREHOUSE = {WAREHOUSE}
                TARGET_LAG = '10 minutes'
                AS 
                SELECT 
                    CALL_ID,
                    TITLE,
                    TRANSCRIPT_JSON AS CONTENT,
                    COMPANY_ID,
                    CALL_TIMESTAMP,
                    REPORTING_PERIOD
                FROM {DB_NAME}.{RAW_SCHEMA}.QUARTR_EARNINGS_CALLS
        """).collect()
        
        # 5. Internal Memos Search Service
        logger.info("Creating INTERNAL_MEMOS_SEARCH service...")
        self.session.sql(f"""
            CREATE OR REPLACE CORTEX SEARCH SERVICE {DB_NAME}.{ANALYTICS_SCHEMA}.INTERNAL_MEMOS_SEARCH
                ON MEMO_BODY
                ATTRIBUTES SUBJECT, CREATION_DATE, AUTHOR, SUBJECT_COMPANIES
                WAREHOUSE = {WAREHOUSE}
                TARGET_LAG = '10 minutes'
                AS 
                SELECT 
                    MEMO_ID,
                    SUBJECT AS TITLE,
                    MEMO_BODY AS CONTENT,
                    CREATION_DATE,
                    AUTHOR,
                    SUBJECT_COMPANIES
                FROM {DB_NAME}.{RAW_SCHEMA}.INTERNAL_INVESTMENT_MEMOS
        """).collect()
        
        logger.info("✅ All Cortex Search services created successfully")
        
        # Validate services were created
        services = self.session.sql("SHOW CORTEX SEARCH SERVICES IN SCHEMA ANALYTICS").collect()
        service_names = [row['name'] for row in services]
        logger.info(f"Created services: {service_names}")
        
        return True
        
    def create_semantic_view(self):
        """Create the Semantic View for Cortex Analyst."""
        logger.info("Creating Semantic View...")
        
        # Switch to ANALYTICS schema
        self.session.sql(f"USE DATABASE {DB_NAME}").collect()
        self.session.sql(f"USE SCHEMA {ANALYTICS_SCHEMA}").collect()
        
        # Create the semantic view
        semantic_view_sql = """
        CREATE OR REPLACE SEMANTIC VIEW INDUSTRIAL_ANALYSIS_SV
            -- Define logical tables
            TABLES (
                companies AS THEMES_RESEARCH_DEMO.RAW_DATA.COMPANIES
                    PRIMARY KEY (COMPANY_ID)
                    WITH SYNONYMS ('company', 'firm', 'corporation', 'logistics company')
                    COMMENT = 'Master table of Nordic logistics companies in the portfolio',
                
                financials AS THEMES_RESEARCH_DEMO.RAW_DATA.COMPANY_FINANCIALS
                    PRIMARY KEY (FINANCIAL_ID)
                    WITH SYNONYMS ('financial data', 'quarterly results', 'earnings')
                    COMMENT = 'Quarterly financial statement data for each company',
                
                macro_indicators AS THEMES_RESEARCH_DEMO.RAW_DATA.MACROECONOMIC_INDICATORS
                    PRIMARY KEY (INDICATOR_ID)
                    WITH SYNONYMS ('economic data', 'inflation metrics', 'macro data')
                    COMMENT = 'Time-series macroeconomic indicators including inflation indices'
            )
            
            -- Define relationships
            RELATIONSHIPS (
                financials_to_companies AS 
                    financials (COMPANY_ID) REFERENCES companies
            )
            
            -- Define dimensions
            DIMENSIONS (
                -- Company dimensions
                companies.company_name AS companies.COMPANY_NAME
                    WITH SYNONYMS ('name', 'company', 'firm name')
                    COMMENT = 'Legal name of the logistics company',
                
                companies.ticker AS companies.TICKER_SYMBOL
                    WITH SYNONYMS ('ticker', 'symbol', 'stock symbol')
                    COMMENT = 'Stock ticker symbol',
                
                companies.sector AS companies.SECTOR
                    WITH SYNONYMS ('industry', 'segment', 'business segment', 'sub-sector')
                    COMMENT = 'Logistics sub-sector (e.g., Road Freight, Maritime)',
                
                companies.headquarters AS companies.HEADQUARTERS
                    WITH SYNONYMS ('HQ', 'location', 'base')
                    COMMENT = 'Company headquarters location',
                
                -- Financial dimensions
                financials.reporting_period AS financials.REPORTING_PERIOD
                    WITH SYNONYMS ('quarter', 'period', 'fiscal quarter')
                    COMMENT = 'Financial reporting period (e.g., 2024-Q3)',
                
                financials.fiscal_year AS financials.FISCAL_YEAR
                    WITH SYNONYMS ('year', 'FY')
                    COMMENT = 'Fiscal year',
                
                financials.fiscal_quarter AS financials.FISCAL_QUARTER
                    WITH SYNONYMS ('quarter number', 'Q')
                    COMMENT = 'Quarter number (1-4)',
                
                -- Macro dimensions
                macro_indicators.indicator_name AS macro_indicators.INDICATOR_NAME
                    WITH SYNONYMS ('metric', 'indicator', 'economic indicator')
                    COMMENT = 'Name of the macroeconomic indicator',
                
                macro_indicators.region AS macro_indicators.REGION
                    WITH SYNONYMS ('geography', 'country', 'area')
                    COMMENT = 'Geographic region for the indicator'
            )
            
            -- Define metrics
            METRICS (
                -- Revenue metrics
                financials.total_revenue AS SUM(financials.REVENUE)
                    WITH SYNONYMS ('revenue', 'sales', 'turnover', 'top line')
                    COMMENT = 'Total revenue for the period',
                
                financials.avg_revenue AS AVG(financials.REVENUE)
                    WITH SYNONYMS ('average revenue', 'mean revenue')
                    COMMENT = 'Average revenue across periods',
                
                -- Cost and margin metrics
                financials.total_cogs AS SUM(financials.COST_OF_GOODS_SOLD)
                    WITH SYNONYMS ('COGS', 'cost of sales', 'direct costs')
                    COMMENT = 'Total cost of goods sold',
                
                financials.gross_profit AS SUM(financials.GROSS_PROFIT)
                    WITH SYNONYMS ('gross income')
                    COMMENT = 'Gross profit (Revenue - COGS)',
                
                financials.avg_gross_margin AS 
                    AVG(financials.GROSS_MARGIN) * 100
                    WITH SYNONYMS ('gross margin percentage', 'GM%', 'gross margin percent', 'average gross margin')
                    COMMENT = 'Average gross profit margin as percentage of revenue',
                
                -- Profitability metrics
                financials.operating_income AS SUM(financials.OPERATING_INCOME)
                    WITH SYNONYMS ('EBIT', 'operating profit')
                    COMMENT = 'Operating income before interest and taxes',
                
                financials.net_income AS SUM(financials.NET_INCOME)
                    WITH SYNONYMS ('net profit', 'bottom line', 'earnings')
                    COMMENT = 'Net income after all expenses',
                
                -- Company metrics
                companies.company_count AS COUNT(DISTINCT companies.COMPANY_ID)
                    WITH SYNONYMS ('number of companies', 'firm count')
                    COMMENT = 'Count of unique companies',
                
                -- Macro metrics
                macro_indicators.average_indicator_value AS AVG(macro_indicators.VALUE)
                    WITH SYNONYMS ('avg value', 'mean value')
                    COMMENT = 'Average value of macroeconomic indicator'
            )
            COMMENT = 'Semantic view for analyzing Nordic logistics companies financial performance and macroeconomic trends'
        """
        
        self.session.sql(semantic_view_sql).collect()
        
        logger.info("✅ Semantic View created successfully")
        
        # Validate semantic view
        views = self.session.sql("SHOW SEMANTIC VIEWS LIKE 'INDUSTRIAL_ANALYSIS_SV' IN SCHEMA ANALYTICS").collect()
        if views:
            logger.info(f"Semantic view validated: {views[0]['name']}")
        
        return True
        
    def test_search_services(self):
        """Run basic tests on search services."""
        logger.info("Testing Cortex Search services...")
        
        self.session.sql(f"USE DATABASE {DB_NAME}").collect()
        self.session.sql(f"USE SCHEMA {ANALYTICS_SCHEMA}").collect()
        
        tests_passed = True
        
        # Test each service
        test_queries = [
            ("FACTSET_NEWS_SEARCH", "inflation logistics"),
            ("GUIDEPOINT_TRANSCRIPTS_SEARCH", "pricing strategies"),
            ("MCBAINCG_REPORTS_SEARCH", "Nordic market"),
            ("QUARTR_EARNINGS_CALLS_SEARCH", "Nordic Freight Systems"),
            ("INTERNAL_MEMOS_SEARCH", "investment thesis")
        ]
        
        for service_name, query in test_queries:
            try:
                result = self.session.sql(f"""
                    SELECT SEARCH_PREVIEW(
                        '{query}',
                        {{'columns': ['TITLE'], 'limit': 1}}
                    ) OVER {service_name}
                """).collect()
                
                if result and len(result) > 0:
                    logger.info(f"✅ {service_name} test passed")
                else:
                    logger.warning(f"⚠️ {service_name} returned no results for '{query}'")
                    
            except Exception as e:
                logger.error(f"❌ {service_name} test failed: {str(e)}")
                tests_passed = False
        
        return tests_passed
        
    def test_semantic_view(self):
        """Test the semantic view with basic queries."""
        logger.info("Testing Semantic View...")
        
        self.session.sql(f"USE DATABASE {DB_NAME}").collect()
        self.session.sql(f"USE SCHEMA {ANALYTICS_SCHEMA}").collect()
        
        try:
            # Test basic query
            result = self.session.sql("""
                SELECT * FROM INDUSTRIAL_ANALYSIS_SV
                WHERE METRICS.last_quarter_revenue IS NOT NULL
                ORDER BY METRICS.last_quarter_revenue DESC
                LIMIT 3
            """).collect()
            
            if result and len(result) > 0:
                logger.info(f"✅ Semantic View test passed - found {len(result)} top companies")
                return True
            else:
                logger.warning("⚠️ Semantic View returned no results")
                return False
                
        except Exception as e:
            logger.error(f"❌ Semantic View test failed: {str(e)}")
            return False
