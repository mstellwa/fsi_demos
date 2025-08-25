# SnowBank Intelligence Demo - Agent Configuration Instructions

This document provides step-by-step instructions for configuring the 4 agents in Snowsight after running the data setup.

> **🆕 Important Update**: This demo now uses **proper semantic views** created with `CREATE SEMANTIC VIEW` syntax instead of standard SQL views. This provides enhanced Cortex Analyst capabilities with embedded business logic, predefined metrics, and optimized natural language query processing.

## Prerequisites

**For complete functional and technical requirements**, see:
- [Functional Requirements](./.cursor/rukes/functional_requirements.mdc) - Agent specifications and configuration details
- [Technical Requirements](./.cursor/rukes/technical_requirements.mdc) - Environment setup and prerequisites

**Quick prerequisites check**:
- ✅ Demo setup completed: `python main.py`
- ✅ Access to Snowsight with Snowflake Intelligence enabled
- ✅ Cortex Analyst and Cortex Search permissions
- ✅ **Proper semantic views created**: `SNOWBANK_DEMO_SV` + `MARKET_PEER_ANALYSIS_SV`

## Agent Configuration Overview

Create 4 agents in Snowsight, each with:
- **Cortex Analyst** tool connected to `SNOWBANK_DEMO_SV` (proper semantic view)
- **One Cortex Search** service per agent
- **Claude 4.0** as orchestration model
- **Specific planning and response instructions**

### Semantic View Details
**Dual Semantic View Architecture** - Clean separation of banking and market data:

#### Banking Semantic View (`SNOWBANK_DEMO_SV`)
- **4 Core Tables**: `MEMBER_BANKS`, `CUSTOMERS`, `LOANS`, `FINANCIALS` with defined relationships
- **Banking Focus**: Customer portfolios, loan exposures, LTM fees, green bonds, alliance performance
- **No Multi-Path Issues**: Clean relationship design without market data conflicts

#### Market Semantic View (`MARKET_PEER_ANALYSIS_SV`) 
- **1 Focused Table**: `MARKET_DATA` for dedicated peer analysis
- **Market Focus**: Stock performance, peer comparisons, price volatility, industry benchmarking
- **Query Example**: "Stock performance vs top 3 aquaculture competitors"

Both views use proper `CREATE SEMANTIC VIEW` syntax with comprehensive metadata and are Cortex Analyst ready.

---

## Agent 1: Relationship Manager (Client 360°)

### Basic Configuration
- **Name**: `Relationship_Manager_Agent`
- **Description**: "Holistic Client 360° analysis combining structured metrics with market intelligence"
- **Orchestration Model**: Claude 4.0

### Tools Configuration

#### Tool 1: Cortex Analyst (Banking Data)
- **Tool Type**: Cortex Analyst
- **Name**: `SnowBank_Portfolio_Analyst`
- **Semantic View**: `FSI_DEMOS.BANK_DEMO.SNOWBANK_DEMO_SV`
- **Description**: "Access to Nordic Banking Alliance semantic view containing customer portfolios, loan exposures, and financial data. Query by customer names, industry sectors (Aquaculture, Maritime, etc.), geographic regions (Helgeland, Vestlandet, etc.), loan types, and exposure amounts. Provides metrics like total exposure, loan counts, LTM fee income, and credit scores across the alliance network."

#### Tool 2: Cortex Analyst (Market Data)
- **Tool Type**: Cortex Analyst
- **Name**: `Market_Peer_Analysis`
- **Semantic View**: `FSI_DEMOS.BANK_DEMO.MARKET_PEER_ANALYSIS_SV`
- **Description**: "Access to Norwegian/Nordic stock market data for peer analysis. Query by company names, stock tickers, peer groups (Aquaculture, Banking, Maritime, etc.), and trading dates. Provides metrics like average stock prices, price volatility, max/min prices for competitive benchmarking and industry sector performance analysis."

#### Tool 3: Cortex Search
- **Tool Type**: Cortex Search
- **Name**: `Client_Market_Intelligence_Search`
- **Service**: `FSI_DEMOS.BANK_DEMO.CLIENT_AND_MARKET_INTEL_SVC`
- **ID Column**: `DOC_ID`
- **Title Column**: `TITLE`
- **Description**: "Search service for CRM meeting notes and Norwegian industry news articles covering aquaculture operations, regulatory changes, market conditions, and customer relationship insights"

### Instructions

#### Planning Instructions
```
For client exposure, balances, revenues, or loan data, use the SnowBank_Portfolio_Analyst tool. For peer stock performance or market comparisons, use the Market_Peer_Analysis tool. For qualitative risks, news, or CRM notes, use Cortex Search. Synthesize results from multiple tools into a comprehensive 360° analysis.
```

#### Response Instructions
```
Be concise. Provide a small metrics table (exposure, LTM fee revenue) and a single chart when time-series is requested. Include 2–4 sentence narrative. Cite document titles for any unstructured facts. End responses with a brief "what I did" summary for transparency.
```

### Sample Test Query
```
Briefing on 'Helio Salmon AS': total exposure, LTM fees, peer stock performance vs top 3 aquaculture competitors, and recent risk signals.
```

**Expected Tool Usage**:
1. **Banking Tool**: Customer exposure and LTM fees for Helio Salmon AS
2. **Market Tool**: Aquaculture peer stock performance (LSG.OL, MOWI.OL, SalMar.OL)
3. **Search Tool**: Recent CRM notes and risk signals

---

## Agent 2: Risk Analyst (Stress Testing)

### Basic Configuration
- **Name**: `Risk_Analyst_Agent`
- **Description**: "Dynamic Portfolio Stress Testing with policy-aware risk mitigation"
- **Orchestration Model**: Claude 4.0

### Tools Configuration

#### Tool 1: Cortex Analyst
- **Tool Type**: Cortex Analyst
- **Name**: `SnowBank_Risk_Analytics`
- **Semantic View**: `FSI_DEMOS.BANK_DEMO.SNOWBANK_DEMO_SV`
- **Description**: "Access to SnowBank semantic view for portfolio stress testing and risk analysis with LTV calculations, property valuations, customer segmentation, and loan performance metrics across Norwegian regions"

#### Tool 2: Cortex Search
- **Tool Type**: Cortex Search
- **Name**: `Internal_Policy_Search`
- **Service**: `FSI_DEMOS.BANK_DEMO.INTERNAL_POLICY_SEARCH_SVC`
- **ID Column**: `DOC_ID`
- **Title Column**: `TITLE`
- **Description**: "Search service for internal credit policies including forbearance procedures, LTV breach management, restructuring options, payment holiday eligibility, and risk mitigation frameworks"

### Instructions

#### Planning Instructions
```
For LTV shocks and cohort identification, use Cortex Analyst. Once a high-risk cohort is identified, query the policy search service to retrieve applicable mitigation clauses (e.g., payment holiday, restructuring). Synthesize the quantitative cohort with verbatim policy excerpts.
```

#### Response Instructions
```
Return a compact table with key fields (LOAN_ID, OUTSTANDING_BALANCE, POST_STRESS_LTV). Below, list quoted policy clauses with titles and sections. Keep total response brief. End responses with a brief "what I did" summary for transparency.
```

### Sample Test Query
```
Impact of 5% property decline and +75bps; loans breaching 85% LTV; relevant forbearance options.
```

---

## Agent 3: ESG Officer (Green Bond Reporting)

### Basic Configuration
- **Name**: `ESG_Officer_Agent`
- **Description**: "Automated Green Bond Reporting with environmental impact tracking"
- **Orchestration Model**: Claude 4.0

### Tools Configuration

#### Tool 1: Cortex Analyst
- **Tool Type**: Cortex Analyst
- **Name**: `SnowBank_ESG_Analytics`
- **Semantic View**: `FSI_DEMOS.BANK_DEMO.SNOWBANK_DEMO_SV`
- **Description**: "Access to SnowBank semantic view for green bond portfolio analysis including green project categorization, sustainable lending metrics, renewable energy financing, and environmental impact tracking"

#### Tool 2: Cortex Search
- **Tool Type**: Cortex Search
- **Name**: `ESG_Compliance_Search`
- **Service**: `FSI_DEMOS.BANK_DEMO.REPORTING_AND_COMPLIANCE_SVC`
- **ID Column**: `DOC_ID`
- **Title Column**: `TITLE`
- **Description**: "Search service for green bond documentation, annual ESG reports, third-party sustainability assessments, renewable energy project details, LEED/BREEAM certifications, and CO2 reduction targets"

### Instructions

#### Planning Instructions
```
Use Cortex Analyst to aggregate green lending amounts by category for the requested period. For top loans, query the reporting & compliance search service to extract project descriptions and environmental targets; also retrieve eligibility criteria. Provide citations.
```

#### Response Instructions
```
Start with a category totals table. Then list top projects with 1–2 sentence descriptions and extracted CO2 targets. Include a short eligibility confirmation with citations. End responses with a brief "what I did" summary for transparency.
```

### Sample Test Query
```
Generate 2024 Green Bond allocation by category; describe top 5 renewable projects; confirm eligibility.
```

---

## Agent 4: Executive Leadership (Strategic Inquiry)

### Basic Configuration
- **Name**: `Executive_Leadership_Agent`
- **Description**: "Cross-Alliance Strategic Inquiry for performance benchmarking"
- **Orchestration Model**: Claude 4.0

### Tools Configuration

#### Tool 1: Cortex Analyst
- **Tool Type**: Cortex Analyst
- **Name**: `SnowBank_Alliance_Analytics`
- **Semantic View**: `FSI_DEMOS.BANK_DEMO.SNOWBANK_DEMO_SV`
- **Description**: "Access to SnowBank semantic view for cross-alliance performance analysis including SMB lending growth, cost-income ratios, member bank comparisons, and strategic KPI benchmarking across the Nordic Banking federation"

#### Tool 2: Cortex Search
- **Tool Type**: Cortex Search
- **Name**: `Strategic_Reports_Search`
- **Service**: `FSI_DEMOS.BANK_DEMO.REPORTING_AND_COMPLIANCE_SVC`
- **ID Column**: `DOC_ID`
- **Title Column**: `TITLE`
- **Description**: "Search service for annual reports, strategic initiatives documentation, SMB digital transformation programs, alliance performance updates, and cross-member collaboration insights"

### Instructions

#### Planning Instructions
```
Rank banks by SMB growth and compute alliance average C/I using Cortex Analyst. Then search annual reports for SMB initiatives and summarize specific actions with citations. Present a brief executive note.
```

#### Response Instructions
```
Provide a ranked list with SMB growth and C/I vs alliance avg, followed by bullet summaries of initiatives (1–2 bullets per bank) with citations. Keep it crisp. End responses with a brief "what I did" summary for transparency.
```

### Sample Test Query
```
Top 3 SMB growth banks in 2024; summarize their SMB initiatives; compare C/I vs alliance avg.
```

---

## Demo Execution

For complete demo scenarios, presentation scripts, timing guidelines, and expected results, see **[DEMO_SCRIPT.md](./DEMO_SCRIPT.md)**.

The demo script includes:
- ✅ **4 Complete Scenarios**: Holistic Client 360°, Dynamic Stress Testing, Green Bond Reporting, Cross-Alliance Strategic Analysis
- ✅ **Narrative Flow**: Opening (Alliance Dilemma) → 4 Scenarios → Closing (Alliance Advantage)  
- ✅ **Expected Results**: Sample outputs and metrics for each scenario step
- ✅ **Timing Guidelines**: 15-20 minute total execution with 4-minute scenario segments
- ✅ **Execution Notes**: Technical setup, success metrics, and backup strategies

---

## Troubleshooting Agent Setup

### Common Issues

1. **Agent Creation Failed**
   - Verify Snowflake Intelligence is enabled
   - Check user permissions for agent creation
   - Ensure Claude 4.0 model is available

2. **Cortex Analyst Tool Issues**
   - Verify `SNOWBANK_DEMO_SV` semantic view exists: `SHOW SEMANTIC VIEWS`
   - Check semantic view structure: `DESCRIBE SEMANTIC VIEW SNOWBANK_DEMO_SV`
   - Verify semantic view permissions (SELECT on underlying tables)
   - Ensure semantic view has proper TABLES, RELATIONSHIPS, FACTS, DIMENSIONS, and METRICS clauses
   - Note: Direct SELECT from semantic views is not supported - Cortex Analyst handles the querying

3. **Cortex Search Tool Issues**
   - Verify search services are created and active
   - Test search services with sample queries
   - Check document content exists

4. **Agent Responses Empty/Error**
   - Verify both tools are properly configured
   - Check warehouse is running and sized appropriately
   - Review agent execution logs in Snowsight

### Validation Queries

Test each service manually before agent configuration:

```sql
-- Verify semantic view exists and has proper structure
SHOW SEMANTIC VIEWS;

-- Verify semantic view has dimensions and metrics
DESCRIBE SEMANTIC VIEW SNOWBANK_DEMO_SV;

-- Test semantic view data (Note: Direct SELECT from semantic views is not yet supported)
-- Instead, test underlying data:
SELECT COUNT(*) FROM FSI_DEMOS.BANK_DEMO.LOANS;
SELECT COUNT(*) FROM FSI_DEMOS.BANK_DEMO.CUSTOMERS;
SELECT COUNT(*) FROM FSI_DEMOS.BANK_DEMO.MEMBER_BANKS;

-- Test search services
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'FSI_DEMOS.BANK_DEMO.CLIENT_AND_MARKET_INTEL_SVC',
    '{"query": "algae bloom", "limit": 5}'
);

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'FSI_DEMOS.BANK_DEMO.INTERNAL_POLICY_SEARCH_SVC',
    '{"query": "forbearance", "limit": 5}'
);

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'FSI_DEMOS.BANK_DEMO.REPORTING_AND_COMPLIANCE_SVC',
    '{"query": "renewable energy", "limit": 5}'
);
```

**Expected Results:**
- ✅ `SHOW SEMANTIC VIEWS` should list `SNOWBANK_DEMO_SV`
- ✅ `DESCRIBE SEMANTIC VIEW` should show 44 dimensions and 52 metrics  
- ✅ All table counts should be > 0 (5 banks, 5000 customers, 25000 loans)
- ✅ All search services should return relevant document excerpts with proper JSON format

All queries should return results before proceeding with agent configuration.
