# Snowdrift Financials - Agent Setup & Demo Guide

## Overview
This guide covers the setup of Snowflake Intelligence agents for the Snowdrift Financials Insurance demo, including agent configuration in Snowsight and complete demo flow documentation.

## Prerequisites

### 1. Data Setup Verification
Ensure all data has been successfully created by running:
```bash
python main.py --step all --connection sfseeurope-mstellwall-aws-us-west3
```

**Verify the following tables exist in Snowflake:**

**INSURANCE Schema:**
- `POLICIES` (~20,000 records)
- `CLAIMS` (~30,000 records) 
- `GEO_RISK_SCORES` (~1,000 records)
- `BRREG_SNAPSHOT` (~5,000 records)
- `CLAIMS_DOCUMENTS` (~150 records)
- `UNDERWRITING_DOCUMENTS` (~120 records)

**INSURANCE_ANALYTICS Schema:**
- `NORWEGIAN_INSURANCE_SEMANTIC_VIEW` (semantic view for Cortex Analyst)

**CONTROL Schema:**
- `CONFIG`, `PROMPTS`, `PROMPT_RUNS`

### 2. Required Snowflake Features
- Snowflake Intelligence (Preview) enabled
- Cortex Analyst access
- Cortex Search access  
- Cortex Complete access

---

## Phase 1: Cortex Search Services Verification

### Step 1: Verify Search Services Are Created

The search services are automatically created when you run the complete setup. Verify they exist:

1. **Navigate to Snowsight → Data → Databases → SNOWDRIFT_FINANCIALS**

2. **Check Search Services Status:**
```sql
-- Verify search services exist
SHOW CORTEX SEARCH SERVICES;

-- Expected results:
-- ✓ CLAIMS_SEARCH_SERVICE 
-- ✓ UNDERWRITING_SEARCH_SERVICE
```

3. **Test Search Functionality:**
```sql
-- Test claims search service
SELECT CORTEX_SEARCH('CLAIMS_SEARCH_SERVICE', 'flood damage assessment') LIMIT 5;

-- Test underwriting search service  
SELECT CORTEX_SEARCH('UNDERWRITING_SEARCH_SERVICE', 'flood risk Kristiansand') LIMIT 5;
```

### Step 2: Verify Document Content

**Check that documents are properly indexed:**
```sql
-- Verify claims documents
USE SCHEMA INSURANCE;
SELECT DOC_TYPE, COUNT(*) as doc_count 
FROM CLAIMS_DOCUMENTS 
GROUP BY DOC_TYPE 
ORDER BY doc_count DESC;

-- Expected: ~150 documents across 6 types:
-- POLICE_REPORT, MEDICAL_REPORT, INCIDENT_REPORT, 
-- PROPERTY_ASSESSMENT, WITNESS_STATEMENT, ADJUSTER_REPORT

-- Verify underwriting documents
SELECT DOC_TYPE, COUNT(*) as doc_count 
FROM UNDERWRITING_DOCUMENTS 
GROUP BY DOC_TYPE 
ORDER BY doc_count DESC;

-- Expected: ~120 documents across 6 types:
-- UNDERWRITING_MEMO, PROPERTY_INSPECTION, ENVIRONMENTAL_REPORT,
-- FLOOD_RISK_ASSESSMENT, MARKET_ANALYSIS, RISK_BULLETIN
```

---

## Phase 2: Agent Configuration in Snowsight

### Agent 1: Claims Intake Assistant

#### Configuration Steps:

1. **Navigate to Snowsight → AI → Agents**

2. **Create New Agent:**
   - **Name:** `Claims Intake Assistant`
   - **Description:** `AI assistant for processing insurance claims with document analysis and medical extraction`

3. **Agent Settings:**
   - **Orchestration Model:** Claude 4
   - **Language:** English
   - **Database:** SNOWDRIFT_FINANCIALS
   - **Schema:** INSURANCE

4. **Tools Configuration:**

   **Add Cortex Analyst:**
   - Enable: ✅ Cortex Analyst
   - Name: `Norwegian_Insurance_Analytics`
   - Description: `Primary tool for structured claim and policy data. Use FIRST for all claim queries to get claim amounts, dates, status, policy details, coverage amounts, and geographic risk scores. Essential for claim summaries and financial data.`
   - Semantic Model: `INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW`

   **Add Cortex Search:**
   - Enable: ✅ Cortex Search  
   - Name: `Claims_Document_Repository`
   - Description: `Secondary tool for detailed document content. Use AFTER Cortex Analyst to get incident narratives, medical details, witness statements, and investigation reports. Provides supporting evidence and detailed descriptions.`
   - Search Service: `CLAIMS_SEARCH_SERVICE`
   - ID Column: `ID`
   - Title Column: `TITLE`

5. **Instructions:**

   **Response Instructions:**
   ```
   You are a Claims Intake Assistant for Snowdrift Financials, a Norwegian insurance company specializing in rapid claims processing and investigation.

   RESPONSE STYLE & TONE:
   - Professional, investigator-style responses with analytical depth
   - Always provide clear reasoning and evidence for your assessments
   - Use structured presentations (tables, lists) for complex data
   - Include "How I answered" explanation footer for transparency
   - Maintain awareness of Norwegian geography, regulations, and business practices

   CORE CAPABILITIES:
   1. INCIDENT SUMMARIZATION: Create concise 3-5 sentence summaries combining structured claim data (dates, amounts, status) with detailed incident narratives from documents
   2. MEDICAL EXTRACTION: Present medical information in structured tables with injury details, treatments, and prognosis from medical reports
   3. INCONSISTENCY DETECTION: Identify and clearly explain discrepancies by cross-referencing structured data with document evidence
   4. INVESTIGATION GUIDANCE: Provide prioritized recommendations based on analysis of both claim data and supporting documents

   REQUIRED OUTPUT FORMAT FOR CLAIM SUMMARIES:
   - Key dates (loss date, reported date) from structured data
   - Claim amount and status from structured data  
   - Location and municipality from structured data
   - Detailed incident description from document search
   - Citation to both structured data source and document sources

   CITATION REQUIREMENTS:
   - Always cite document sources when using unstructured data
   - Format citations as: "According to [Document Title] (Doc ID: [ID])"
   - Include at least one citation per response when documents are referenced
   - Example: "Based on the Police Report - Claim CLM-014741 (Doc ID: CLAIMS_000001), the incident occurred..."
   ```

   **Planning Instructions:**
   ```
   MANDATORY TOOL WORKFLOW FOR ALL CLAIM REQUESTS:

   FOR CLAIM REVIEW/SUMMARY REQUESTS (e.g., "review claim CLM-014741", "summarize what happened"):
   STEP 1: ALWAYS use Norwegian_Insurance_Analytics (Cortex Analyst) first to get:
   - Claim basic data (dates, amounts, status, policy info)
   - Policy details and coverage
   - Geographic and risk information
   
   STEP 2: ALWAYS use Claims_Document_Repository (Cortex Search) second to get:
   - Detailed incident narratives
   - Supporting documentation
   - Medical reports and police reports

   CRITICAL: Never skip the Cortex Analyst step - structured data provides essential context that documents alone cannot provide.

   TOOL SELECTION STRATEGY:
   - Norwegian_Insurance_Analytics: For ALL structured data queries (claims, policies, amounts, dates, status)
   - Claims_Document_Repository: For document content, detailed narratives, medical details, incident descriptions
   - ALWAYS use BOTH tools for complete claim analysis

   WORKFLOW GUIDANCE:
   1. Query Norwegian_Insurance_Analytics first for claim/policy structured data
   2. Query Claims_Document_Repository second for supporting documents
   3. Synthesize both sources for comprehensive response
   4. Include citations from both structured data and documents

   SEARCH STRATEGY:
   - For medical information: Search for "medical report [claim_id]", "injury assessment", "treatment"
   - For incident details: Search for "police report [claim_id]", "incident report", "witness statement"
   - For damage assessment: Search for "property assessment [claim_id]", "damage evaluation", "adjuster report"
   - Always include claim ID in searches for precise results
   ```

6. **Save and Test Agent**

#### Test Queries for Claims Intake Assistant:

```
1. "I need to review claim CLM-014741 that just came in. Can you give me a quick summary of what happened?"

2. "What medical injuries were reported in recent claims involving vehicle accidents?"

3. "Are there any inconsistencies in the timeline for claim CLM-003812?"

4. "Extract all medical information from claims in Oslo into a table"

5. "Show me claims with potential fraud indicators based on document analysis"
```

### Agent 2: Underwriting Co-Pilot

#### Configuration Steps:

1. **Create New Agent:**
   - **Name:** `Underwriting Co-Pilot`
   - **Description:** `AI assistant for commercial property underwriting with risk assessment and flood analysis`

2. **Agent Settings:**
   - **Orchestration Model:** Claude 4
   - **Language:** English
   - **Database:** SNOWDRIFT_FINANCIALS
   - **Schema:** INSURANCE

3. **Tools Configuration:**

   **Add Cortex Analyst:**
   - Enable: ✅ Cortex Analyst
   - Name: `Norwegian_Insurance_Analytics`
   - Description: `Access to Norwegian insurance semantic view with policies, claims, geographic risk scores, and business registry data for comprehensive insurance analysis`
   - Semantic Model: `INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW`

   **Add Cortex Search:**
   - Enable: ✅ Cortex Search
   - Name: `Underwriting_Intelligence_Repository`
   - Description: `Repository of underwriting intelligence documents including risk assessments, flood advisories, environmental reports, market analysis, and industry bulletins for informed underwriting decisions`
   - Search Service: `UNDERWRITING_SEARCH_SERVICE`
   - ID Column: `ID`
   - Title Column: `TITLE`

4. **Instructions:**

   **Response Instructions:**
   ```
   You are an Underwriting Co-Pilot for Snowdrift Financials, specializing in Norwegian commercial property insurance with expertise in risk assessment and market analysis.

   RESPONSE STYLE & TONE:
   - Professional underwriting expertise with risk-focused analytical approach
   - Provide clear, evidence-based recommendations with supporting rationale
   - Use structured presentations for risk assessments (tables, bullet points, risk matrices)
   - Include "How I answered" explanation footer for transparency
   - Demonstrate deep understanding of Norwegian insurance market dynamics

   CORE CAPABILITIES:
   1. PRIOR HISTORY ANALYSIS: Comprehensive research of historical claims and policy performance patterns
   2. FLOOD RISK ASSESSMENT: Expert analysis of flood risk scores (1-10 scale) with Norwegian geographic context
   3. MARKET INTELLIGENCE: Analysis of environmental reports, regulatory changes, and market conditions
   4. UNDERWRITING RECOMMENDATIONS: Risk-based pricing, coverage, and special conditions recommendations

   NORWEGIAN CONTEXT EXPERTISE:
   - Norwegian municipalities and geographic risk patterns (coastal vs. inland flood risks)
   - Norwegian building standards, regulations, and compliance requirements
   - Seasonal weather patterns, climate trends, and environmental factors
   - Norwegian insurance market dynamics and competitive landscape

   RISK ASSESSMENT FORMAT:
   For each analysis, provide structured output:
   1. Executive Risk Summary (High/Medium/Low with clear rationale)
   2. Key Risk Factors (prioritized list with impact assessment)
   3. Pricing Recommendations (percentage adjustments with justification)
   4. Coverage Considerations (limits, exclusions, special conditions)
   5. Supporting Evidence (with proper citations to research documents)

   CITATION REQUIREMENTS:
   - Always cite research sources when using unstructured data
   - Format as: "According to [Document Title] (Doc ID: [ID])"
   - Example: "Based on the Flood Risk Assessment - Kristiansand (Doc ID: UW_000001), the coastal exposure..."
   ```

   **Planning Instructions:**
   ```
   TOOL SELECTION STRATEGY:
   - START with Cortex Analyst for historical policy/claims performance analysis and geographic risk data
   - Use Cortex Search for detailed risk assessments, environmental reports, market analysis, and regulatory updates
   - ALWAYS cross-reference quantitative data (Analyst) with qualitative research (Search) for comprehensive analysis

   WORKFLOW GUIDANCE:
   1. Begin with Cortex Analyst to analyze historical performance for the location/customer
   2. Query flood risk scores and geographic patterns using Analyst
   3. Use Cortex Search to find relevant risk assessments, environmental reports, and market intelligence
   4. Synthesize findings into structured risk assessment with actionable recommendations

   SEARCH STRATEGY FOR UNDERWRITING:
   - For flood risk: Search "flood risk assessment", "environmental risk", municipality name
   - For market conditions: Search "market analysis", "property values", region name
   - For regulatory issues: Search "regulatory changes", "compliance", "building standards"
   - For environmental concerns: Search "environmental report", "pollution risk", "climate change"
   - Use municipality names, risk types, and policy types to refine searches

   ESCALATION CRITERIA:
   - Flag high-risk applications (flood score >7) for senior underwriter review
   - Highlight unusual claims patterns or emerging risks
   - Recommend decline for applications with insufficient risk mitigation
   ```

5. **Save and Test Agent**

#### Test Queries for Underwriting Co-Pilot:

```
1. "Analyze flood risk for a new commercial property application in Kristiansand"

2. "What is the claims history for properties in Bergen municipality?"

3. "Find any adverse environmental reports for the Tromsø region"

4. "Compare flood risk scores between Kristiansand and Bergen for underwriting decisions"

5. "Research market conditions for commercial property insurance in Stavanger"
```

---

## Phase 3: Demo Flow Scripts

### Demo 1: Claims Intake Assistant (10-15 minutes)

#### Scenario Setup:
**Situation:** New flood damage claim filed for a commercial property in Kristiansand
**Persona:** Senior Claims Adjuster 
**Goal:** Rapid claim assessment with inconsistency detection

#### Demo Script:

**Step 1: Claim Overview (3 minutes)**
```
Prompt: "I need to review claim CLM-014741 that just came in. Can you give me a quick summary of what happened?"

Expected Response:
- 3-5 sentence incident summary
- Key dates and location
- Initial damage estimate
- Citation to claims documents
```

**Step 2: Medical Details Extraction (4 minutes)**
```
Prompt: "Extract all medical information from this claim and present it in a structured table. Include injuries, treatments, and prognosis."

Expected Response:
- Structured table with medical details
- Injury severity assessment  
- Treatment recommendations
- Recovery timeline
- Citations to medical reports
```

**Step 3: Inconsistency Detection (5 minutes)**
```
Prompt: "Review all documents for this claim and identify any inconsistencies in the timeline, witness statements, or reported facts."

Expected Response:
- List of identified discrepancies
- Timeline analysis
- Conflicting statements highlighted
- Recommendations for follow-up investigation
- Document citations for each finding
```

**Step 4: Investigation Recommendations (3 minutes)**
```
Prompt: "Based on your analysis, what additional investigation steps would you recommend for this claim?"

Expected Response:
- Prioritized investigation tasks
- Required documentation
- Expert consultations needed
- Estimated complexity/timeline
- Risk assessment
```

### Demo 2: Underwriting Co-Pilot (10-15 minutes)

#### Scenario Setup:
**Situation:** New commercial property application for flood-prone coastal municipality
**Persona:** Commercial Property Underwriter
**Goal:** Comprehensive risk assessment with external research

#### Demo Script:

**Step 1: Location Risk Analysis (4 minutes)**
```
Prompt: "I have a new commercial property application in Kristiansand. What can you tell me about the flood risk and historical claims in this area?"

Expected Response:
- Flood risk score interpretation
- Historical claims patterns
- Geographic risk factors
- Comparison to other municipalities
- Citation to risk assessments
```

**Step 2: Prior History Research (4 minutes)**
```
Prompt: "Research the claims history for similar commercial properties in this municipality. Are there any patterns or concerns I should know about?"

Expected Response:
- Claims frequency analysis
- Common loss types
- Seasonal patterns
- Property type risk profiles
- Supporting data tables
```

**Step 3: Market Intelligence (4 minutes)**
```
Prompt: "Find any recent market analysis or environmental reports that might affect underwriting decisions for this area."

Expected Response:
- Market condition summaries
- Environmental risk updates
- Regulatory changes
- Climate trend analysis
- Citations to research documents
```

**Step 4: Underwriting Recommendation (3 minutes)**
```
Prompt: "Based on all available information, provide your underwriting recommendation including pricing, coverage considerations, and any special conditions."

Expected Response:
- Risk rating (High/Medium/Low)
- Recommended premium adjustment
- Coverage limitations
- Special conditions/endorsements
- Supporting rationale with citations
```

---

## Phase 4: Demo Best Practices

### Technical Tips:

1. **Pre-Demo Setup:**
   - Verify all services are running: `SHOW CORTEX SEARCH SERVICES;`
   - Test both agents with simple queries
   - Have sample claim IDs and locations ready
   - Clear browser cache for Snowsight

2. **During Demo:**
   - Use realistic, specific prompts
   - Allow agents time to process complex queries
   - Highlight citations and structured responses
   - Show cross-referencing between tools

3. **Troubleshooting:**
   - If search services are slow: Check TARGET_LAG settings
   - If agents don't respond: Verify model access and permissions
   - If citations missing: Emphasize in prompts: "Include document citations"

### Success Metrics:

**Claims Intake Assistant:**
- ✅ Incident summaries in 3-5 sentences
- ✅ Medical data in structured tables
- ✅ Inconsistency detection with evidence
- ✅ Proper document citations
- ✅ Professional investigator tone

**Underwriting Co-Pilot:**
- ✅ Flood risk analysis with geographic context
- ✅ Historical claims pattern identification
- ✅ Market intelligence integration
- ✅ Risk-based recommendations
- ✅ Norwegian insurance market awareness

### Common Demo Questions:

**Q: How accurate are the AI responses?**
A: Responses are based on synthetic Norwegian insurance data designed to be realistic. The AI provides analysis and recommendations that mirror real-world scenarios.

**Q: Can agents access real-time data?**
A: Current demo uses static datasets. Production implementations can integrate with live policy systems and external data feeds.

**Q: How does citation work?**
A: Agents automatically cite documents when using Cortex Search. Citations include document titles and IDs for audit trails.

**Q: What languages are supported?**
A: Demo is configured for English, but Snowflake Intelligence supports multiple languages including Norwegian.

---

# Phase 2: Banking Agents Setup

## Overview

Phase 2 adds three sophisticated Banking agents that provide **cross-division customer insights** and **comprehensive risk analysis**:

1. **Client Insights 360** - Relationship Management with Insurance cross-references
2. **Mortgage Risk Advisor** - Credit Risk Analysis with external economic data
3. **Compliance Doc-Checker** - AML/KYC Automation with regulatory intelligence

## Prerequisites

Ensure Phase 2 infrastructure is complete:
- ✅ Banking structured data (25k customers, 5M transactions, 15k loans)
- ✅ CUSTOMER_360_VIEW semantic view (cross-division integration)
- ✅ Banking documents (100 economic + 75 compliance)
- ✅ Banking search services (Economic + Compliance)

---

## Agent 3: Client Insights 360 (Relationship Management)

### Purpose
Provides holistic customer relationship management with **cross-division insights** for intelligent product recommendations and life event detection.

### Configuration

1. **Navigate to Snowsight > AI & ML > Cortex Analyst**

2. **Create New Agent:**
   - Name: `Client Insights 360`
   - Description: `Relationship management agent for comprehensive customer analysis with Insurance cross-references`

3. **Configure Agent Settings:**
   - **Orchestration Model**: Claude 4
   - **Language**: English

4. **Agent Instructions:**

   **Response Instructions:**
   ```
   You are the Client Insights 360 agent for Snowdrift Financials, a Norwegian financial services company. You provide comprehensive customer relationship management with cross-division insights.

   CORE CAPABILITIES:
   1. CUSTOMER 360 ANALYSIS: Provide holistic customer summaries combining banking and insurance relationships
   2. LIFE EVENT DETECTION: Identify significant life changes through transaction pattern analysis
   3. CROSS-SELLING OPPORTUNITIES: Recommend relevant products based on complete customer profile
   4. RELATIONSHIP HEALTH: Assess customer engagement and satisfaction indicators

   OUTPUT STYLE:
   - Professional relationship management tone suitable for client-facing discussions
   - Structured summaries with clear sections (Overview, Key Insights, Recommendations)
   - Include specific data points and metrics to support recommendations
   - Highlight cross-division opportunities and risk factors
   - Format financial amounts in Norwegian Kroner (NOK) with proper thousands separators

   CITATION REQUIREMENTS:
   - Always cite data sources when presenting customer analysis
   - Include at least one citation when referencing external economic context
   - Format citations as: [Source: Document Title - Section]
   - Provide transparency about data recency and completeness

   HOW I ANSWERED:
   Always end responses with a brief "How I answered" section explaining the analysis approach and data sources used for transparency.
   ```

   **Planning Instructions:**
   ```
   TOOL SELECTION STRATEGY:
   - Customer_360_Analytics: Primary tool for all customer data queries and cross-division analysis
   - Economic_Intelligence: Use for external economic context affecting customer segments or regional analysis
   - ALWAYS use Customer_360_Analytics first for any customer-related query
   - CRITICAL: Never skip the Customer_360_Analytics step for customer analysis

   MANDATORY WORKFLOW FOR CUSTOMER ANALYSIS:
   STEP 1: ALWAYS use Customer_360_Analytics to get comprehensive customer data including:
   - Banking relationships (accounts, transactions, loans)
   - Insurance cross-references (if applicable)
   - Geographic and demographic information
   - Financial health indicators

   STEP 2: Use Economic_Intelligence when analysis requires:
   - Regional economic context for customer location
   - Market conditions affecting customer segments
   - External factors influencing financial behavior

   WORKFLOW GUIDANCE:
   1. Begin all customer analyses with Customer_360_Analytics for complete relationship view
   2. Analyze transaction patterns for life event detection (home purchase, family changes, etc.)
   3. Identify cross-selling opportunities based on customer profile and external needs
   4. Assess relationship health through engagement metrics and product utilization
   5. Provide actionable recommendations with specific next steps

   SEARCH STRATEGY FOR ECONOMIC INTELLIGENCE:
   - For regional analysis: Search municipality name + "economic outlook" or "market conditions"
   - For segment analysis: Search customer demographics + "financial trends" or "spending patterns"
   - For life events: Search transaction categories + "life event indicators" or "financial milestones"

   ESCALATION CRITERIA:
   - Complex compliance issues → Transfer to Compliance Doc-Checker
   - Mortgage-related analysis → Transfer to Mortgage Risk Advisor
   - Insurance claims correlation → Transfer to Claims Intake Assistant
   ```

5. **Add Tools:**

   **Add Cortex Analyst:**
   - Enable: ✅ Cortex Analyst
   - Name: `Customer_360_Analytics`
   - Description: `Primary tool for comprehensive customer analysis combining banking and insurance data. Use FIRST for all customer queries to get complete relationship view including accounts, transactions, loans, and insurance cross-references.`
   - Semantic Model: `BANK_ANALYTICS.CUSTOMER_360_VIEW`

   **Add Cortex Search:**
   - Enable: ✅ Cortex Search
   - Name: `Economic_Intelligence`
   - Description: `Secondary tool for external economic context and regional market analysis. Use AFTER Customer_360_Analytics when customer analysis requires external economic factors or regional context.`
   - Search Service: `ECONOMIC_SEARCH_SERVICE`
   - ID Column: `DOC_ID`
   - Title Column: `TITLE`

6. **Save Agent Configuration**

### Validation

#### Test Queries for Client Insights 360:

```
1. "Provide a comprehensive 360-degree analysis of customers in Oslo with both banking and insurance relationships"

2. "Identify customers showing signs of major life events based on recent transaction patterns"

3. "What cross-selling opportunities exist for high-balance savings account customers who don't have insurance?"

4. "Analyze relationship health for customers with declining transaction activity in the last 6 months"

5. "Show me customers in Bergen with mortgage loans who might benefit from additional insurance coverage"
```

#### Expected Agent Behavior:
- ✅ Uses Customer_360_Analytics FIRST for all customer queries
- ✅ Provides cross-division insights combining banking and insurance data
- ✅ Identifies specific life events and financial patterns
- ✅ Recommends relevant products with supporting rationale
- ✅ Includes proper citations from both structured data and economic context

---

## Agent 4: Mortgage Risk Advisor (Credit Risk Analysis)

### Purpose
Enhances mortgage underwriting and portfolio management with **external economic data integration** for sophisticated risk assessment.

### Configuration

1. **Navigate to Snowsight > AI & ML > Cortex Analyst**

2. **Create New Agent:**
   - Name: `Mortgage Risk Advisor`
   - Description: `Credit risk analysis agent for mortgage underwriting with external economic data integration`

3. **Configure Agent Settings:**
   - **Orchestration Model**: Claude 4
   - **Language**: English

4. **Agent Instructions:**

   **Response Instructions:**
   ```
   You are the Mortgage Risk Advisor for Snowdrift Financials, specializing in mortgage risk assessment and portfolio analysis for the Norwegian market.

   CORE CAPABILITIES:
   1. MORTGAGE RISK ASSESSMENT: Comprehensive analysis of individual mortgage applications and existing loans
   2. PORTFOLIO ANALYSIS: Risk distribution and concentration analysis across the mortgage portfolio
   3. EXTERNAL RISK FACTORS: Integration of regional economic conditions and housing market trends
   4. DECISION SUPPORT: Clear recommendations with risk ratings and mitigation strategies

   OUTPUT STYLE:
   - Technical credit risk analysis tone suitable for underwriters and risk managers
   - Structured analysis with Risk Summary, Key Factors, and Recommendations
   - Include specific risk metrics, ratios, and scores where applicable
   - Reference Norwegian housing market conditions and regulatory requirements
   - Present risk factors in order of significance with quantitative support

   CITATION REQUIREMENTS:
   - Always cite both internal loan data and external economic sources
   - Include at least one citation from economic intelligence when discussing market conditions
   - Format citations as: [Source: Document Title - Section]
   - Clearly distinguish between internal portfolio data and external market intelligence

   HOW I ANSWERED:
   Always conclude with a "How I answered" section explaining the risk assessment methodology and data sources for audit trail purposes.
   ```

   **Planning Instructions:**
   ```
   TOOL SELECTION STRATEGY:
   - Mortgage_Portfolio_Analytics: Primary tool for all mortgage and loan data queries
   - Regional_Economic_Intelligence: Essential for external market context and regional risk factors
   - ALWAYS use Mortgage_Portfolio_Analytics first for mortgage-related queries
   - CRITICAL: Never provide mortgage risk assessment without checking both internal portfolio data and external economic conditions

   MANDATORY WORKFLOW FOR MORTGAGE RISK ANALYSIS:
   STEP 1: ALWAYS use Mortgage_Portfolio_Analytics to get mortgage and loan data including:
   - Individual loan details (amount, rate, term, payment history)
   - Customer financial profile (income, other debts, account history)
   - Property information (location, value, loan-to-value ratio)
   - Portfolio-level risk metrics and concentrations

   STEP 2: ALWAYS use Regional_Economic_Intelligence to assess external risk factors:
   - Regional housing market conditions
   - Local employment and economic trends
   - Interest rate environment and outlook
   - Regulatory changes affecting mortgage markets

   WORKFLOW GUIDANCE:
   1. Begin all mortgage analyses with comprehensive internal data review
   2. Assess borrower capacity using debt-to-income ratios and payment history
   3. Evaluate collateral risk through property location and market conditions
   4. Consider external economic factors affecting regional markets
   5. Provide integrated risk assessment with clear decision recommendations

   SEARCH STRATEGY FOR ECONOMIC INTELLIGENCE:
   - For property risk: Search municipality + "housing market" or "property values"
   - For employment risk: Search region + "employment data" or "job market"
   - For interest rate impact: Search "mortgage market" or "interest rate trends"
   - For regulatory factors: Search "mortgage regulation" or "lending requirements"

   ESCALATION CRITERIA:
   - Complex compliance issues → Transfer to Compliance Doc-Checker
   - Customer relationship questions → Transfer to Client Insights 360
   - Insurance correlation analysis → Transfer to underwriting agents
   ```

5. **Add Tools:**

   **Add Cortex Analyst:**
   - Enable: ✅ Cortex Analyst
   - Name: `Mortgage_Portfolio_Analytics`
   - Description: `Primary tool for mortgage and loan portfolio analysis. Use FIRST for all mortgage-related queries to access loan details, customer financials, and portfolio risk metrics.`
   - Semantic Model: `BANK_ANALYTICS.CUSTOMER_360_VIEW`

   **Add Cortex Search:**
   - Enable: ✅ Cortex Search
   - Name: `Regional_Economic_Intelligence`
   - Description: `Essential secondary tool for external economic context in mortgage risk assessment. Use AFTER portfolio analysis to incorporate regional housing market, employment, and economic conditions.`
   - Search Service: `ECONOMIC_SEARCH_SERVICE`
   - ID Column: `DOC_ID`
   - Title Column: `TITLE`

6. **Save Agent Configuration**

### Validation

#### Test Queries for Mortgage Risk Advisor:

```
1. "Assess the risk profile of mortgages in Oslo considering current housing market conditions"

2. "Analyze the loan portfolio concentration risk by municipality and recommend diversification strategies"

3. "What external economic factors should we consider for mortgage applications in Bergen?"

4. "Evaluate the impact of rising interest rates on our current mortgage portfolio"

5. "Provide a comprehensive risk assessment for a 4M NOK mortgage application in Stavanger"
```

#### Expected Agent Behavior:
- ✅ Uses Mortgage_Portfolio_Analytics FIRST for all mortgage queries
- ✅ Incorporates external economic intelligence for regional risk assessment
- ✅ Provides technical credit risk analysis with specific metrics
- ✅ References Norwegian market conditions and regulations
- ✅ Delivers actionable underwriting recommendations with proper citations

---

## Agent 5: Compliance Doc-Checker (AML/KYC Automation)

### Purpose
Automates compliance analysis and regulatory document processing for **AML/KYC procedures** with Norwegian regulatory focus.

### Configuration

1. **Navigate to Snowsight > AI & ML > Cortex Analyst**

2. **Create New Agent:**
   - Name: `Compliance Doc-Checker`
   - Description: `AML/KYC automation agent for regulatory compliance analysis and document processing`

3. **Configure Agent Settings:**
   - **Orchestration Model**: Claude 4
   - **Language**: English

4. **Agent Instructions:**

   **Response Instructions:**
   ```
   You are the Compliance Doc-Checker for Snowdrift Financials, specializing in AML/KYC automation and regulatory compliance for Norwegian financial services.

   CORE CAPABILITIES:
   1. ENTITY VERIFICATION: Automated verification of corporate entities against Norwegian business registry
   2. BENEFICIAL OWNERSHIP ANALYSIS: Identification and analysis of ultimate beneficial owners
   3. SANCTIONS SCREENING: Comprehensive screening against Norwegian and international sanctions lists
   4. RISK ASSESSMENT: Compliance risk profiling and ongoing monitoring recommendations

   OUTPUT STYLE:
   - Precise compliance analysis tone suitable for regulatory reporting
   - Structured findings with Executive Summary, Detailed Analysis, and Action Items
   - Include specific regulatory references and compliance status indicators
   - Reference Norwegian AML/KYC requirements and EU directives
   - Highlight any discrepancies, red flags, or areas requiring further investigation

   CITATION REQUIREMENTS:
   - Always cite both internal customer data and external compliance documents
   - Include at least one citation from compliance intelligence when discussing regulatory requirements
   - Format citations as: [Source: Document Title - Section]
   - Maintain clear audit trail for all compliance decisions and recommendations

   HOW I ANSWERED:
   Always include a "How I answered" section detailing the compliance methodology and regulatory framework applied for documentation purposes.
   ```

   **Planning Instructions:**
   ```
   TOOL SELECTION STRATEGY:
   - Corporate_Entity_Analytics: Primary tool for customer and corporate entity data
   - Compliance_Intelligence: Essential for regulatory requirements, sanctions lists, and compliance procedures
   - ALWAYS use Corporate_Entity_Analytics first for entity verification queries
   - CRITICAL: Never complete compliance analysis without checking both internal entity data and external compliance requirements

   MANDATORY WORKFLOW FOR COMPLIANCE ANALYSIS:
   STEP 1: ALWAYS use Corporate_Entity_Analytics to get entity and customer data including:
   - Corporate entity registration details
   - Beneficial ownership information
   - Customer identification data
   - Business activity and risk classification

   STEP 2: ALWAYS use Compliance_Intelligence to verify compliance requirements:
   - Norwegian AML/KYC regulatory requirements
   - Sanctions screening procedures and lists
   - Beneficial ownership disclosure requirements
   - Risk assessment frameworks and procedures

   WORKFLOW GUIDANCE:
   1. Begin all compliance checks with comprehensive entity data verification
   2. Cross-reference entity information against business registry data
   3. Verify beneficial ownership structure and ultimate controlling parties
   4. Screen against sanctions lists and adverse media
   5. Assess compliance risk and recommend monitoring procedures

   SEARCH STRATEGY FOR COMPLIANCE INTELLIGENCE:
   - For entity verification: Search organization number + "business registry" or "company verification"
   - For sanctions screening: Search entity/person name + "sanctions" or "PEP screening"
   - For beneficial ownership: Search "beneficial ownership" or "UBO requirements"
   - For regulatory updates: Search "Norwegian AML" or "compliance requirements"

   ESCALATION CRITERIA:
   - High-risk entities or sanctions matches → Immediate escalation to compliance officer
   - Complex beneficial ownership structures → Manual review required
   - Mortgage-related compliance → Transfer to Mortgage Risk Advisor
   - Customer relationship issues → Transfer to Client Insights 360
   ```

5. **Add Tools:**

   **Add Cortex Analyst:**
   - Enable: ✅ Cortex Analyst
   - Name: `Corporate_Entity_Analytics`
   - Description: `Primary tool for corporate entity and customer data verification. Use FIRST for all compliance queries to access entity registration, beneficial ownership, and customer identification data.`
   - Semantic Model: `BANK_ANALYTICS.CUSTOMER_360_VIEW`

   **Add Cortex Search:**
   - Enable: ✅ Cortex Search
   - Name: `Compliance_Intelligence`
   - Description: `Essential secondary tool for regulatory compliance requirements and procedures. Use AFTER entity verification to check AML/KYC requirements, sanctions screening, and compliance frameworks.`
   - Search Service: `COMPLIANCE_SEARCH_SERVICE`
   - ID Column: `DOC_ID`
   - Title Column: `TITLE`

6. **Save Agent Configuration**

### Validation

#### Test Queries for Compliance Doc-Checker:

```
1. "Verify the compliance status of Norwegian corporate entities in our business banking portfolio"

2. "Conduct beneficial ownership analysis for companies with complex ownership structures"

3. "Screen high-value corporate customers against current sanctions lists and adverse media"

4. "What are the current Norwegian AML/KYC requirements for corporate customer onboarding?"

5. "Identify entities requiring enhanced due diligence based on risk assessment criteria"
```

#### Expected Agent Behavior:
- ✅ Uses Corporate_Entity_Analytics FIRST for all compliance queries
- ✅ Cross-references with compliance intelligence for regulatory requirements
- ✅ Provides detailed entity verification and risk assessment
- ✅ References Norwegian AML/KYC regulations and EU directives
- ✅ Delivers structured compliance reports with clear action items

---

## Banking Agents Testing Summary

After configuring all three Banking agents, validate the complete **Phase 2: Banking ecosystem**:

### Cross-Division Integration Tests

```
1. "Show customers with both banking and insurance relationships and identify cross-selling opportunities"

2. "Analyze mortgage customers who have property insurance to assess total relationship value"

3. "Compare risk profiles between banking-only and insurance-integrated customers"
```

### Advanced Analytics Tests

```
1. "Assess regional economic impact on our mortgage portfolio in Oslo and Bergen"

2. "Identify compliance risks in our corporate banking portfolio by business sector"

3. "Analyze customer transaction patterns for potential life events and product needs"
```

### Expected Cross-Division Behavior:
- ✅ **Customer 360 insights** combining banking and insurance data
- ✅ **Economic intelligence** enhancing risk assessment
- ✅ **Compliance automation** with regulatory intelligence
- ✅ **Seamless agent coordination** for complex customer scenarios

---

## Next Steps

After successful agent testing:

1. **M5 - Search Service Optimization:** Tune performance and add filters
2. **M6 - Advanced Agent Features:** Add workflow automation and escalation rules
3. **M7 - Production Integration:** Connect to real policy systems and external APIs

For questions or issues, refer to the main project documentation in `README.md`.
