-- ===================================================================
-- SAM Snowsight Intelligence Demo - Complete Structured Tables
-- All tables needed for the complete demo (Analyst, PM, and CRM agents)
-- ===================================================================

USE DATABASE FSI_DEMOS;
USE SCHEMA SAM_DEMO;

-- ===================================================================
-- CORE FINANCIAL AND MARKET DATA TABLES
-- ===================================================================

-- Company Financial Data (for R&D spend analysis and financial metrics)
CREATE OR REPLACE TABLE COMPANY_FINANCIALS (
    COMPANY_ID INTEGER,
    TICKER VARCHAR(10),
    COMPANY_NAME VARCHAR(255),
    REPORT_DATE DATE,
    QUARTER VARCHAR(10),
    REVENUE_USD_M DECIMAL(18,2),
    NET_INCOME_USD_M DECIMAL(18,2),
    RD_SPEND_USD_M DECIMAL(18,2),  -- Key field for analyst demo
    CASH_ON_HAND_USD_M DECIMAL(18,2),
    PRIMARY KEY (COMPANY_ID, REPORT_DATE)
);

-- Market Data (supporting data)
CREATE OR REPLACE TABLE MARKET_DATA (
    TICKER VARCHAR(10),
    TRADE_DATE DATE,
    OPEN_PRICE DECIMAL(10,2),
    HIGH_PRICE DECIMAL(10,2),
    LOW_PRICE DECIMAL(10,2),
    CLOSE_PRICE DECIMAL(10,2),
    VOLUME BIGINT,
    PRIMARY KEY (TICKER, TRADE_DATE)
);

-- ===================================================================
-- CLIENT AND PORTFOLIO MANAGEMENT TABLES
-- ===================================================================

-- Client CRM data for personalized communications
CREATE OR REPLACE TABLE CLIENT_CRM (
    CLIENT_ID VARCHAR(50) PRIMARY KEY,
    CLIENT_NAME VARCHAR(255),
    CLIENT_TYPE VARCHAR(50),
    AUM_USD_M DECIMAL(18,2),
    LAST_CONTACT_DATE DATE,
    STATED_INTERESTS VARCHAR(1000),
    MEETING_LOGS VARCHAR(5000)
);

-- Client Portfolio data linked to CRM
CREATE OR REPLACE TABLE CLIENT_PORTFOLIOS (
    PORTFOLIO_ID VARCHAR(50) PRIMARY KEY,
    CLIENT_ID VARCHAR(50),
    PERFORMANCE_YTD_PCT DECIMAL(5,2),
    INCEPTION_DATE DATE,
    FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT_CRM(CLIENT_ID)
);

-- Portfolio Holdings History for client portfolio analysis
CREATE OR REPLACE TABLE PORTFOLIO_HOLDINGS_HISTORY (
    TRANSACTION_ID VARCHAR(64) PRIMARY KEY,
    PORTFOLIO_ID VARCHAR(50),
    TRADE_DATE DATE,
    TICKER VARCHAR(10),
    ACTION VARCHAR(10),  -- BUY, SELL
    SHARES DECIMAL(18,4),
    PRICE_PER_SHARE DECIMAL(10,2),
    RESULTING_WEIGHT_PCT DECIMAL(5,2),
    FOREIGN KEY (PORTFOLIO_ID) REFERENCES CLIENT_PORTFOLIOS(PORTFOLIO_ID)
);

-- ===================================================================
-- PROMPT MANAGEMENT FOR SYNTHETIC DATA GENERATION
-- ===================================================================

-- Prompt Library for AI_COMPLETE template management
CREATE OR REPLACE TABLE PROMPT_LIBRARY (
    PROMPT_ID VARCHAR(64) PRIMARY KEY,
    PROMPT_TYPE VARCHAR(50),        -- ResearchNote, EarningsTranscript, HistoricalThesis, etc.
    TEMPLATE_TEXT STRING,           -- Template with placeholders
    DEFAULT_TONE VARCHAR(50),
    MIN_TOKENS INTEGER,
    MAX_TOKENS INTEGER,
    STYLE_GUIDE STRING,             -- SAM-specific guidance
    MODEL_TIER VARCHAR(10),         -- small, medium, large
    IS_ACTIVE BOOLEAN DEFAULT TRUE,
    METADATA_JSON VARIANT
);

-- Prompt Inputs for specific document generation instances
CREATE OR REPLACE TABLE PROMPT_INPUTS (
    RUN_ID VARCHAR(64),
    PROMPT_ID VARCHAR(64),
    COMPANY_NAME VARCHAR(255),
    DOC_DATE DATE,
    QUARTER VARCHAR(10),
    ATTENDEES STRING,
    TOPICS STRING,
    EVENT_ANCHOR STRING,
    DOC_VARIANT VARCHAR(50),
    OUTPUT_FORMAT VARCHAR(10),      -- TXT, PDF
    TARGET_COLLECTION VARCHAR(64),  -- Document type collection
    MODEL_NAME VARCHAR(100),        -- Specific model for AI_COMPLETE
    FOREIGN KEY (PROMPT_ID) REFERENCES PROMPT_LIBRARY(PROMPT_ID)
);

-- ===================================================================
-- DOCUMENT STORAGE AND MANAGEMENT
-- ===================================================================

-- Create internal stage for unstructured documents
CREATE OR REPLACE STAGE SAM_DOCS_STAGE;

-- Documents table for storing generated content (required for Cortex Search)
CREATE OR REPLACE TABLE DOCUMENTS (
    DOC_ID VARCHAR(64) PRIMARY KEY,
    FILE_URL STRING,
    COMPANY_NAME VARCHAR(255),
    DOCUMENT_TYPE VARCHAR(50),
    DOC_DATE DATE,
    QUARTER VARCHAR(10),
    AUTHOR VARCHAR(255),
    TAGS ARRAY,
    SOURCE_PROMPT_ID VARCHAR(64),
    MODEL_NAME VARCHAR(100),
    CONTENT VARCHAR(16777216),  -- Max VARCHAR for large documents
    LAST_MODIFIED TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Enable change tracking for Cortex Search compatibility
ALTER TABLE DOCUMENTS SET CHANGE_TRACKING = TRUE;

-- Rendered prompts table for bulk document generation optimization
CREATE OR REPLACE TABLE RENDERED_PROMPTS (
    PROMPT_RENDER_ID VARCHAR(64) PRIMARY KEY,
    DOC_ID VARCHAR(64),
    FILE_URL STRING,
    COMPANY_NAME VARCHAR(255),
    DOCUMENT_TYPE VARCHAR(50),
    DOC_DATE DATE,
    QUARTER VARCHAR(10),
    AUTHOR VARCHAR(255),
    TAGS ARRAY,
    SOURCE_PROMPT_ID VARCHAR(64),
    MODEL_NAME VARCHAR(100),
    FULL_PROMPT STRING,  -- Complete rendered prompt ready for AI_COMPLETE
    CREATION_TIMESTAMP TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
