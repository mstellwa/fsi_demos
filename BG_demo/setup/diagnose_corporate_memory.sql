-- ===================================================================
-- CORPORATE MEMORY SERVICE DIAGNOSTIC QUERIES
-- Run these to diagnose Portfolio Manager demo issues
-- ===================================================================

USE DATABASE FSI_DEMOS;
USE SCHEMA SAM_DEMO;

-- 1. Check if documents were generated
SELECT '=== DOCUMENTS TABLE VERIFICATION ===' as check_type;
SELECT COUNT(*) as total_documents FROM DOCUMENTS;

-- 2. Check Arkadia Commerce documents specifically  
SELECT '=== ARKADIA COMMERCE DOCUMENTS ===' as check_type;
SELECT 
    DOC_ID,
    COMPANY_NAME,
    DOCUMENT_TYPE,
    DOC_DATE,
    AUTHOR,
    SUBSTRING(CONTENT, 1, 100) as content_preview
FROM DOCUMENTS 
WHERE COMPANY_NAME = 'Arkadia Commerce'
ORDER BY DOC_DATE;

-- 3. Check corporate memory document types
SELECT '=== CORPORATE MEMORY DOCUMENT TYPES ===' as check_type;
SELECT 
    DOCUMENT_TYPE,
    COUNT(*) as document_count,
    COUNT(DISTINCT COMPANY_NAME) as companies_covered
FROM DOCUMENTS 
WHERE DOCUMENT_TYPE IN ('HistoricalThesis', 'MeetingNotes', 'InternalDebateSummary')
GROUP BY DOCUMENT_TYPE
ORDER BY DOCUMENT_TYPE;

-- 4. Check 2019 Arkadia Commerce documents specifically
SELECT '=== 2019 ARKADIA COMMERCE DOCUMENTS ===' as check_type;
SELECT 
    DOC_ID,
    DOCUMENT_TYPE,
    DOC_DATE,
    SUBSTRING(CONTENT, 1, 200) as content_preview
FROM DOCUMENTS 
WHERE COMPANY_NAME = 'Arkadia Commerce' 
AND YEAR(DOC_DATE) = 2019
ORDER BY DOC_DATE;

-- 5. Check if search services exist with proper ATTRIBUTES
SELECT '=== CORTEX SEARCH SERVICES ===' as check_type;
SHOW CORTEX SEARCH SERVICES;

-- Verify that search services include DOC_ID and FILE_URL in ATTRIBUTES
-- Look for attribute_columns containing both DOC_ID and FILE_URL
SELECT '=== SEARCH SERVICE ATTRIBUTES VERIFICATION ===' as check_type;

-- 6. Test corporate_memory_service using SEARCH_PREVIEW
SELECT '=== CORPORATE MEMORY SERVICE TEST ===' as check_type;

-- Test the exact Portfolio Manager demo query
SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'CORPORATE_MEMORY_SERVICE',
      '{
         "query": "Show me our original investment thesis for Arkadia Commerce when we first invested in 2019. What were the key risks identified by the team in the initial debate?",
         "limit": 5
      }'
  )
)['results'] as search_results;

-- Test a simpler query to verify service works
SELECT '=== SIMPLE SEARCH TEST ===' as check_type;

SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'CORPORATE_MEMORY_SERVICE', 
      '{
         "query": "Arkadia Commerce 2019",
         "limit": 3
      }'
  )
)['results'] as simple_search;

-- 7. Test all three Portfolio Manager demo queries
SELECT '=== PM DEMO QUERY 1 TEST ===' as check_type;

SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'CORPORATE_MEMORY_SERVICE',
      '{
         "query": "Show me our original investment thesis for Arkadia Commerce when we first invested in 2019. What were the key risks identified by the team in the initial debate?",
         "limit": 3
      }'
  )
)['results'] as pm_query_1;

SELECT '=== PM DEMO QUERY 2 TEST ===' as check_type;

SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'CORPORATE_MEMORY_SERVICE',
      '{
         "query": "Track the evolution of our thinking on Arkadia Commerce competitive moat against Amazon. Summarize the key points from our management meeting notes with their CEO in 2019 and 2022.",
         "limit": 3
      }'
  )
)['results'] as pm_query_2;

SELECT '=== PM DEMO QUERY 3 TEST ===' as check_type;

SELECT PARSE_JSON(
  SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
      'CORPORATE_MEMORY_SERVICE',
      '{
         "query": "Generate a pre-mortem analysis. Based on our firm historical investment mistakes documented in the archive, what are the top 3 ways our Arkadia Commerce investment could fail, grounded in our firm historical experience with similar platform companies?",
         "limit": 3
      }'
  )
)['results'] as pm_query_3;

-- 8. Verify ID and Title columns for agent configuration
SELECT '=== ID AND TITLE COLUMN VERIFICATION ===' as check_type;

SELECT 
    DOC_ID,
    FILE_URL,
    COMPANY_NAME,
    DOCUMENT_TYPE,
    DOC_DATE
FROM DOCUMENTS 
WHERE COMPANY_NAME = 'Arkadia Commerce'
LIMIT 5;

-- 9. Check content status for debugging
SELECT '=== CONTENT STATUS CHECK ===' as check_type;
SELECT 
    DOC_ID,
    DOCUMENT_TYPE, 
    COMPANY_NAME,
    DOC_DATE,
    CASE 
        WHEN CONTENT IS NULL THEN 'NULL CONTENT'
        WHEN LENGTH(CONTENT) = 0 THEN 'EMPTY CONTENT'
        WHEN LENGTH(CONTENT) < 100 THEN 'VERY SHORT CONTENT'
        ELSE 'CONTENT OK'
    END as content_status,
    LENGTH(CONTENT) as content_length
FROM DOCUMENTS 
WHERE COMPANY_NAME = 'Arkadia Commerce'
ORDER BY DOC_DATE;
