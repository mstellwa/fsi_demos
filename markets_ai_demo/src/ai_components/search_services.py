# src/ai_components/search_services.py
# Cortex Search service creation for Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def create_all_search_services(session: Session) -> None:
    """Create all Cortex Search services for the demo scenarios"""
    
    print("   🔎 Creating earnings_transcripts search service...")
    create_earnings_transcripts_search(session)
    
    print("   🔎 Creating research_reports search service...")
    create_research_reports_search(session)
    
    print("   🔎 Creating news_articles search service...")  
    create_news_articles_search(session)
    
    print("   ✅ All search services created")


def create_earnings_transcripts_search(session: Session) -> None:
    """
    Create search service for earnings call transcripts
    Supports: Equity Research Analyst scenarios
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE ANALYTICS.EARNINGS_TRANSCRIPTS_SEARCH
    ON FULL_TEXT
    ATTRIBUTES TRANSCRIPT_ID, TITLE, TICKER, FISCAL_QUARTER
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        TRANSCRIPT_ID,
        TITLE,
        TICKER,
        FISCAL_QUARTER,
        FULL_TEXT
    FROM RAW_DATA.EARNINGS_CALL_TRANSCRIPTS
    """
    
    session.sql(search_service_sql).collect()
    print("     📞 Earnings transcripts search service created")


def create_research_reports_search(session: Session) -> None:
    """
    Create search service for internal research reports
    Supports: Global Research & Market Insights scenarios
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE ANALYTICS.RESEARCH_REPORTS_SEARCH
    ON FULL_TEXT
    ATTRIBUTES REPORT_ID, TITLE, REPORT_TYPE, THEMATIC_TAGS, AUTHOR, PUBLISHED_DATE
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        REPORT_ID,
        TITLE,
        REPORT_TYPE, 
        THEMATIC_TAGS,
        AUTHOR,
        PUBLISHED_DATE,
        FULL_TEXT
    FROM RAW_DATA.RESEARCH_REPORTS
    """
    
    session.sql(search_service_sql).collect()
    print("     📊 Research reports search service created")


def create_news_articles_search(session: Session) -> None:
    """
    Create search service for news articles
    Supports: Cross-scenario news and market event analysis
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE ANALYTICS.NEWS_ARTICLES_SEARCH
    ON BODY
    ATTRIBUTES ARTICLE_ID, HEADLINE, SOURCE, AFFECTED_TICKER, PUBLISHED_AT
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        ARTICLE_ID,
        HEADLINE,
        SOURCE,
        AFFECTED_TICKER, 
        PUBLISHED_AT,
        BODY
    FROM RAW_DATA.NEWS_ARTICLES
    """
    
    session.sql(search_service_sql).collect() 
    print("     📰 News articles search service created")