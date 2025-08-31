-- ===================================================================
-- SAM Snowsight Intelligence Demo - Complete Services and Views Setup
-- Creates all semantic views and search services for Analyst, PM, and CRM agents
-- ===================================================================

USE DATABASE FSI_DEMOS;
USE SCHEMA SAM_DEMO;

-- ===================================================================
-- SEMANTIC VIEWS FOR AGENT TOOLS
-- ===================================================================

-- FINANCIAL_DATA_ANALYST semantic view for Research Analyst agent
-- Provides structured access to financial and R&D data for hybrid analysis
CREATE OR REPLACE SEMANTIC VIEW FINANCIAL_DATA_ANALYST
  TABLES (
    company_financials AS COMPANY_FINANCIALS PRIMARY KEY (COMPANY_ID, REPORT_DATE)
    WITH SYNONYMS ('financial data', 'company metrics', 'earnings', 'revenue data', 'R&D spending')
    COMMENT = 'Company financial metrics including revenue, R&D spend, and cash positions for investment analysis'
  )
  FACTS (
    company_financials.company_id AS company_id
    WITH SYNONYMS ('company ID', 'company identifier')
    COMMENT = 'Unique identifier for each company',
    company_financials.revenue_usd_m AS revenue_usd_m
    WITH SYNONYMS ('revenue', 'sales', 'top line', 'quarterly revenue')
    COMMENT = 'Quarterly revenue in USD millions',
    company_financials.rd_spend_usd_m AS rd_spend_usd_m
    WITH SYNONYMS ('R&D spending', 'research and development', 'innovation investment', 'R&D expenditure')
    COMMENT = 'Quarterly R&D expenditure in USD millions - key metric for tech companies',
    company_financials.cash_on_hand_usd_m AS cash_on_hand_usd_m
    WITH SYNONYMS ('cash', 'cash position', 'liquidity', 'cash reserves')
    COMMENT = 'Cash and cash equivalents in USD millions'
  )
  DIMENSIONS (
    company_financials.company_name AS company_name
    WITH SYNONYMS ('company', 'company name', 'firm', 'business', 'portfolio holding')
    COMMENT = 'Full company name for portfolio holdings identification',
    company_financials.ticker AS ticker
    WITH SYNONYMS ('symbol', 'stock symbol', 'ticker symbol', 'trading symbol')
    COMMENT = 'Trading ticker symbol for company identification',
    company_financials.quarter AS quarter
    WITH SYNONYMS ('quarter', 'reporting period', 'Q1', 'Q2', 'Q3', 'Q4', 'fiscal quarter')
    COMMENT = 'Reporting quarter in YYYYQN format',
    company_financials.report_date AS report_date
    WITH SYNONYMS ('date', 'reporting date', 'quarter end', 'fiscal period end')
    COMMENT = 'Quarter end date for financial reporting'
  )
  METRICS (
    company_financials.total_revenue AS SUM(revenue_usd_m)
    WITH SYNONYMS ('total revenue', 'cumulative revenue', 'revenue sum', 'aggregate sales')
    COMMENT = 'Total revenue across all reporting periods',
    company_financials.total_rd_spend AS SUM(rd_spend_usd_m)
    WITH SYNONYMS ('total R&D', 'cumulative R&D spending', 'total innovation investment', 'aggregate R&D')
    COMMENT = 'Total R&D spending across all periods - indicates innovation commitment',
    company_financials.rd_intensity AS AVG(rd_spend_usd_m / NULLIF(revenue_usd_m, 0) * 100)
    WITH SYNONYMS ('R&D intensity', 'R&D as percent of revenue', 'innovation ratio', 'R&D percentage')
    COMMENT = 'R&D spending as percentage of revenue - key innovation and growth metric'
  );

-- CLIENT_DATA_ANALYST semantic view for CRM agent
-- Provides structured access to client and portfolio data for personalized communications
CREATE OR REPLACE SEMANTIC VIEW CLIENT_DATA_ANALYST
  TABLES (
    client_crm AS CLIENT_CRM PRIMARY KEY (CLIENT_ID)
    WITH SYNONYMS ('clients', 'client data', 'CRM', 'customer information', 'relationship management')
    COMMENT = 'Client relationship management data including AUM, interests, and contact history',
    client_portfolios AS CLIENT_PORTFOLIOS PRIMARY KEY (PORTFOLIO_ID)
    WITH SYNONYMS ('portfolios', 'client portfolios', 'portfolio performance', 'investment accounts')
    COMMENT = 'Client portfolio data with performance metrics and inception dates'
  )
  RELATIONSHIPS (
    client_crm_to_client_portfolios AS 
      client_portfolios (client_id) REFERENCES client_crm
  )
  FACTS (
    client_crm.aum_usd_m AS aum_usd_m
    WITH SYNONYMS ('AUM', 'assets under management', 'client assets', 'managed assets')
    COMMENT = 'Client assets under management in USD millions',
    client_portfolios.performance_ytd_pct AS performance_ytd_pct
    WITH SYNONYMS ('performance', 'YTD performance', 'portfolio return', 'returns', 'investment performance')
    COMMENT = 'Year-to-date portfolio performance as percentage'
  )
  DIMENSIONS (
    client_crm.client_name AS client_name
    WITH SYNONYMS ('client', 'client name', 'customer name', 'investor name')
    COMMENT = 'Full client name for relationship management and communications',
    client_crm.client_type AS client_type
    WITH SYNONYMS ('client type', 'customer type', 'investor type', 'institution type')
    COMMENT = 'Type of client: Pension Fund, Endowment, Family Office, etc.',
    client_crm.stated_interests AS stated_interests
    WITH SYNONYMS ('interests', 'investment interests', 'client preferences', 'investment focus', 'themes')
    COMMENT = 'Client investment interests and preferences for personalized communications',
    client_crm.last_contact_date AS last_contact_date
    WITH SYNONYMS ('last contact', 'recent contact', 'last meeting', 'latest interaction')
    COMMENT = 'Date of most recent client contact for relationship tracking',
    client_portfolios.portfolio_id AS portfolio_id
    WITH SYNONYMS ('portfolio', 'portfolio ID', 'portfolio identifier', 'account ID')
    COMMENT = 'Unique portfolio identifier for account management',
    client_portfolios.inception_date AS inception_date
    WITH SYNONYMS ('inception', 'start date', 'portfolio start', 'account opening')
    COMMENT = 'Portfolio inception date for performance tracking'
  )
  METRICS (
    client_crm.total_aum AS SUM(aum_usd_m)
    WITH SYNONYMS ('total AUM', 'total assets', 'aggregate AUM', 'firm AUM')
    COMMENT = 'Total assets under management across all clients',
    client_portfolios.avg_performance AS AVG(performance_ytd_pct)
    WITH SYNONYMS ('average performance', 'mean returns', 'average YTD', 'typical performance')
    COMMENT = 'Average portfolio performance across all clients'
  );

-- ===================================================================
-- DATA VERIFICATION AND TESTING
-- ===================================================================

-- Verify semantic views were created successfully
SELECT '=== SEMANTIC VIEW VERIFICATION ===' as status;
SHOW SEMANTIC VIEWS;

-- Verify we have the expected data for all scenarios
SELECT '=== DATA VERIFICATION ===' as status;

SELECT 'Total Companies:' as metric, COUNT(DISTINCT COMPANY_NAME) as value FROM COMPANY_FINANCIALS
UNION ALL
SELECT 'Total Financial Records:', COUNT(*) FROM COMPANY_FINANCIALS
UNION ALL  
SELECT 'Total Clients:', COUNT(*) FROM CLIENT_CRM
UNION ALL
SELECT 'Total Portfolios:', COUNT(*) FROM CLIENT_PORTFOLIOS
UNION ALL
SELECT 'Total Holdings:', COUNT(*) FROM PORTFOLIO_HOLDINGS_HISTORY
UNION ALL
SELECT 'Prompt Templates:', COUNT(*) FROM PROMPT_LIBRARY
UNION ALL
SELECT 'Prompt Inputs for Generation:', COUNT(*) FROM PROMPT_INPUTS
UNION ALL  
SELECT 'Documents Ready:', COUNT(*) FROM DOCUMENTS;

-- Show company list for reference in demos
SELECT '=== COMPANIES AVAILABLE FOR ANALYSIS ===' as info;
SELECT 
    COMPANY_NAME, 
    TICKER, 
    COUNT(*) as quarters_of_data,
    MIN(QUARTER) as earliest_quarter,
    MAX(QUARTER) as latest_quarter,
    MAX(RD_SPEND_USD_M) as latest_rd_spend_usd_m
FROM COMPANY_FINANCIALS 
GROUP BY COMPANY_NAME, TICKER
ORDER BY COMPANY_NAME;

-- Show client summary for CRM scenarios
SELECT '=== CLIENTS AVAILABLE FOR CRM SCENARIOS ===' as info;
SELECT 
    c.CLIENT_NAME, 
    c.CLIENT_TYPE, 
    c.AUM_USD_M,
    c.STATED_INTERESTS, 
    p.PERFORMANCE_YTD_PCT,
    p.INCEPTION_DATE
FROM CLIENT_CRM c
JOIN CLIENT_PORTFOLIOS p ON c.CLIENT_ID = p.CLIENT_ID
ORDER BY c.AUM_USD_M DESC;

-- Show portfolio holdings for client context
SELECT '=== CLIENT PORTFOLIO HOLDINGS ===' as info;
SELECT 
    c.CLIENT_NAME,
    ph.TICKER,
    cf.COMPANY_NAME,
    ph.SHARES,
    ph.RESULTING_WEIGHT_PCT,
    ph.TRADE_DATE
FROM CLIENT_CRM c
JOIN CLIENT_PORTFOLIOS cp ON c.CLIENT_ID = cp.CLIENT_ID  
JOIN PORTFOLIO_HOLDINGS_HISTORY ph ON cp.PORTFOLIO_ID = ph.PORTFOLIO_ID
LEFT JOIN COMPANY_FINANCIALS cf ON ph.TICKER = cf.TICKER
WHERE ph.ACTION = 'BUY'
ORDER BY c.CLIENT_NAME, ph.RESULTING_WEIGHT_PCT DESC;

-- Show prompt inputs ready for document generation
SELECT '=== PROMPT INPUTS FOR DOCUMENT GENERATION ===' as info;
SELECT 
    PROMPT_TYPE,
    COUNT(*) as input_count,
    COUNT(DISTINCT COMPANY_NAME) as companies_covered,
    COUNT(DISTINCT QUARTER) as quarters_covered
FROM PROMPT_INPUTS pi
JOIN PROMPT_LIBRARY pl ON pi.PROMPT_ID = pl.PROMPT_ID
GROUP BY PROMPT_TYPE
ORDER BY PROMPT_TYPE;

-- ===================================================================
-- NEXT STEPS FOR COMPLETE SETUP
-- ===================================================================

SELECT '=== SETUP STATUS ===' as status;
SELECT 'Core database schema: ✅ COMPLETE' as step
UNION ALL
SELECT 'Structured data population: ✅ COMPLETE' 
UNION ALL
SELECT 'Semantic views: ✅ COMPLETE'
UNION ALL
SELECT 'Prompt templates: ✅ COMPLETE'
UNION ALL
SELECT 'Document generation inputs: ✅ COMPLETE'
UNION ALL
SELECT 'NEXT: Run document generation script to populate DOCUMENTS table'
UNION ALL
SELECT 'NEXT: Create Cortex Search services over document collections'
UNION ALL
SELECT 'NEXT: Configure three agents in Snowsight Intelligence UI';

SELECT '=== DEMO READINESS CHECKLIST ===' as checklist;
SELECT '□ Generate synthetic documents using AI_COMPLETE' as task
UNION ALL
SELECT '□ Create research_service (Cortex Search over research documents)'
UNION ALL  
SELECT '□ Create corporate_memory_service (Cortex Search over historical documents)'
UNION ALL
SELECT '□ Configure Curiosity Co-Pilot agent (Analyst)'
UNION ALL
SELECT '□ Configure Conviction Engine agent (PM)'
UNION ALL
SELECT '□ Configure Personalization & Narrative Suite agent (CRM)'
UNION ALL
SELECT '□ Test demo scenarios with scripted prompts';

-- Note: The following services are created automatically by unified_setup.py:
-- 
-- CREATE CORTEX SEARCH SERVICE research_service 
-- ON CONTENT
-- ATTRIBUTES DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
-- WAREHOUSE = COMPUTE_WH
-- TARGET_LAG = '1 hour'
-- AS (
--   SELECT CONTENT, DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
--   FROM DOCUMENTS 
--   WHERE DOCUMENT_TYPE IN ('ResearchNote', 'EarningsTranscript', 'FrameworkAnalysis', 'ExpertNetworkInterview', 'PatentAnalysis')
-- );
--
-- CREATE CORTEX SEARCH SERVICE corporate_memory_service
-- ON CONTENT
-- ATTRIBUTES DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
-- WAREHOUSE = COMPUTE_WH  
-- TARGET_LAG = '1 hour'
-- AS (
--   SELECT CONTENT, DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
--   FROM DOCUMENTS
--   WHERE DOCUMENT_TYPE IN ('HistoricalThesis', 'MeetingNotes', 'InternalDebateSummary')
-- );
--
-- 🚨 CRITICAL: For agent tools to work properly, configure:
-- - ID Column: DOC_ID
-- - Title Column: FILE_URL
