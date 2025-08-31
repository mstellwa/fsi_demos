-- ===================================================================
-- SAM Demo - Semantic Views Reference with Correct Syntax
-- This file contains the exact working syntax patterns for semantic views
-- ===================================================================

USE DATABASE FSI_DEMOS;
USE SCHEMA SAM_DEMO;

-- ===================================================================
-- FINANCIAL_DATA_ANALYST - Single Table Semantic View
-- Enhanced with SYNONYMS and COMMENTS for natural language queries
-- ===================================================================

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

-- ===================================================================
-- CLIENT_DATA_ANALYST - Multi-Table Semantic View with RELATIONSHIPS
-- Demonstrates proper RELATIONSHIPS syntax for table joins
-- ===================================================================

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
-- RELATIONSHIPS SYNTAX PATTERN REFERENCE
-- ===================================================================

/*
CORRECT RELATIONSHIPS SYNTAX:

RELATIONSHIPS (
  relationship_name AS 
    child_table (foreign_key_column) REFERENCES parent_table
)

EXAMPLE:
RELATIONSHIPS (
  client_crm_to_client_portfolios AS 
    client_portfolios (client_id) REFERENCES client_crm
)

KEY POINTS:
1. Use relationship_name AS for clarity
2. Child table with foreign key references parent table
3. Foreign key column name in parentheses after child table
4. Parent table name only (no column specification needed)

WRONG SYNTAX (DO NOT USE):
- parent.column = child.column
- child REFERENCES parent.column
- child.fk_column REFERENCES parent.pk_column
*/

-- ===================================================================
-- VERIFICATION QUERIES
-- ===================================================================

-- Check semantic views exist
SHOW SEMANTIC VIEWS;

-- Describe semantic view structure
DESCRIBE SEMANTIC VIEW FINANCIAL_DATA_ANALYST;
DESCRIBE SEMANTIC VIEW CLIENT_DATA_ANALYST;

-- Test data access through tables
SELECT COUNT(*) FROM COMPANY_FINANCIALS;
SELECT COUNT(*) FROM CLIENT_CRM;
SELECT COUNT(*) FROM CLIENT_PORTFOLIOS;

-- Test table relationships
SELECT c.CLIENT_NAME, p.PERFORMANCE_YTD_PCT 
FROM CLIENT_CRM c 
JOIN CLIENT_PORTFOLIOS p ON c.CLIENT_ID = p.CLIENT_ID 
LIMIT 3;
