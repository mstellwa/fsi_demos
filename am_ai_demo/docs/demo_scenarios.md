# SAM Demo - Scenario Scripts

Complete demo scenario for Portfolio Copilot with step-by-step conversations, expected responses, and data flows.

## Current Implementation Status

✅ **Phase 1 & 2 Complete**: 3 scenarios fully operational for demonstration
- **Portfolio Copilot**: ✅ Portfolio analytics and benchmarking (Phase 1)
- **Research Copilot**: ✅ Document research and analysis (Phase 2)
- **Thematic Macro Advisor**: ✅ Thematic investment strategy (Phase 2)

🔄 **Phase 3 Ready for Implementation**: ESG & Compliance scenarios
- **ESG Guardian**: ESG risk monitoring and policy compliance
- **Compliance Advisor**: Mandate monitoring and breach detection

🔄 **Phase 4 Future Implementation**: Client & Quantitative scenarios
- **Sales Advisor**: Client reporting and template formatting
- **Quant Analyst**: Factor analysis and performance attribution

## Scenario 1: Portfolio Copilot - Portfolio Insights & Benchmarking

**Business Context**: Portfolio managers need instant access to portfolio analytics, holdings information, and supporting research to make informed investment decisions.

**Persona**: Anna, Senior Portfolio Manager  
**Agent**: `portfolio_copilot`  
**Data Available**: 10 portfolios, 5,000 securities, 2,800 research documents

### 4-Step Demo Conversation

#### Step 1: Top Holdings Overview
**User Prompt**: 
```
"What are my top 10 holdings by market value in the SAM Technology & Infrastructure portfolio?"
```

**Expected Response**:
- Table showing: Ticker, Company Name, Weight %, Market Value USD
- Flag any positions >6.5% (concentration warning)
- Total exposure percentage of top 10

**Tools Used**: `quantitative_analyzer` (Cortex Analyst)  
**Data Accessed**: `FACT_POSITION_DAILY_ABOR`, `DIM_SECURITY`, `DIM_ISSUER` via semantic view  
**Demo Points**: Show instant portfolio analytics, no SQL required

#### Step 2: Latest Research for Holdings  
**User Prompt**: 
```
"What is the latest broker research saying about Apple, Commercial Metals, and Ribbon Communications?"
```

**Expected Response**:
- Bullet list: Company → Recent report titles with dates (AAPL, CMC, RBBN)
- Brief summaries of key investment themes
- Ratings distribution (Buy/Hold/Sell)

**Note**: Uses actual holdings from the portfolio for demo continuity

**Tools Used**: `search_broker_research` (Cortex Search)  
**Data Accessed**: `BROKER_RESEARCH_CORPUS` with SecurityID linkage  
**Demo Points**: Show AI-powered document search, automatic citation

#### Step 3: Benchmark Comparison
**User Prompt**: 
```
"Show me the sector allocation for the SAM Technology & Infrastructure portfolio and compare it to technology sector averages."
```

**Expected Response**:
- Portfolio sector allocation breakdown
- Technology sector concentration analysis
- Comparison to benchmark sector weights
- Concentration warnings for positions >6.5%

**Tools Used**: `quantitative_analyzer` (Cortex Analyst)  
**Data Accessed**: `FACT_POSITION_DAILY_ABOR`, `BENCHMARK_HOLDINGS` via semantic view  
**Demo Points**: Show complex multi-table analytics, benchmark integration

#### Step 4: Risk Assessment
**User Prompt**: 
```
"Which of my top holdings have negative recent research or emerging risks?"
```

**Expected Response**:
- List of flagged securities with specific concerns
- Source citations (document type, date, analyst)
- Recommended actions (review, monitor, consider reduction)

**Tools Used**: `search_broker_research`, `search_press_releases`  
**Data Accessed**: Filter for negative ratings or risk keywords in recent documents  
**Demo Points**: Show AI risk monitoring, multi-source intelligence

## Demo Execution Guidelines

### Pre-Demo Checklist
- [ ] Run `python main.py --scenarios portfolio_copilot` successfully
- [ ] Verify semantic view: `DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_ANALYST_VIEW`
- [ ] Test search services: Use `SNOWFLAKE.CORTEX.SEARCH_PREVIEW()` on each service
- [ ] Configure `portfolio_copilot` agent in Snowflake Intelligence
- [ ] Test agent with validation queries

### Demo Flow Best Practices
1. **Start Simple**: Begin with Step 1 (top holdings) to show basic functionality
2. **Show Integration**: Emphasize how Steps 1→2 flow from quantitative to qualitative
3. **Highlight AI**: Point out document search and automatic citations in Step 2
4. **Show Complexity**: Step 3 demonstrates multi-table benchmark analysis
5. **End with Value**: Step 4 shows proactive risk monitoring

### Current Data Highlights
- **Realistic Portfolios**: SAM Technology & Infrastructure ($90B), SAM ESG Leaders ($108B), SAM Flagship ($150B)
- **Real Tickers**: AAPL, MSFT, NVDA, GOOGL, etc. with proper sector classifications
- **Generated Research**: 1,200 broker reports, 800 earnings transcripts, 800 press releases
- **UK English**: All content generated in professional UK English

### Success Metrics
- ✅ **Speed**: Instant responses to complex portfolio queries
- ✅ **Integration**: Seamless combination of structured and unstructured data
- ✅ **Citations**: Proper source attribution for all document references
- ✅ **Realism**: Authentic-looking financial data and research content

## Scenario 2: Research Copilot - Document Research & Analysis ✅ PHASE 2

**Business Context**: Research analysts need comprehensive document analysis across multiple sources to synthesize investment insights and market intelligence efficiently.

**Persona**: David, Research Analyst  
**Agent**: `research_copilot`  
**Data Available**: 100 broker reports, 75 earnings transcripts, 75 press releases

### 4-Step Demo Conversation

#### Step 1: Multi-Source Research Synthesis
**User Prompt**: 
```
"What is the latest research saying about technology sector opportunities?"
```

**Expected Response**:
- Key investment themes from broker research
- Management commentary from earnings transcripts
- Corporate developments from press releases
- Synthesized investment insights with proper citations

**Tools Used**: `search_broker_research`, `search_earnings_transcripts`, `search_press_releases`  
**Data Accessed**: All three document corpus tables with search synthesis  
**Demo Points**: Show multi-source document analysis and research synthesis

#### Step 2: Company-Specific Intelligence
**User Prompt**: 
```
"Find all available research on Apple's recent performance and outlook"
```

**Expected Response**:
- Broker research opinions and ratings
- Earnings call highlights and guidance
- Press release announcements and developments
- Comprehensive company analysis with timeline

**Tools Used**: `search_broker_research`, `search_earnings_transcripts`, `search_press_releases`  
**Data Accessed**: All document types filtered by company/ticker  
**Demo Points**: Show company-specific research aggregation and analysis

#### Step 3: Thematic Research Discovery
**User Prompt**: 
```
"What trends are emerging in ESG and sustainability research?"
```

**Expected Response**:
- ESG investment themes from broker research
- Sustainability initiatives from press releases
- Management ESG commitments from earnings calls
- Emerging regulatory and market trends

**Tools Used**: `search_broker_research`, `search_earnings_transcripts`, `search_press_releases`  
**Data Accessed**: Documents filtered by ESG/sustainability keywords  
**Demo Points**: Show thematic research discovery and trend identification

#### Step 4: Cross-Source Validation
**User Prompt**: 
```
"Compare what management is saying versus analyst research about renewable energy trends"
```

**Expected Response**:
- Management outlook from earnings transcripts
- Analyst perspectives from broker research
- Corporate strategy from press releases
- Identification of consensus and divergent views

**Tools Used**: `search_broker_research`, `search_earnings_transcripts`, `search_press_releases`  
**Data Accessed**: Documents filtered by renewable energy themes across all sources  
**Demo Points**: Show cross-source validation and perspective comparison

### Pre-Demo Checklist
- [ ] Run `python main.py --scenarios research_copilot` successfully
- [ ] Verify semantic view: `DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_RESEARCH_VIEW`
- [ ] Test search services: Use `SNOWFLAKE.CORTEX.SEARCH_PREVIEW()` on earnings and research services
- [ ] Configure `research_copilot` agent in Snowflake Intelligence with `financial_analyzer` tool
- [ ] Test agent with validation queries for earnings data

### Demo Flow Best Practices
1. **Start with Earnings**: Begin with Step 1 to show financial analysis capabilities
2. **Show Time Series**: Use Step 2 to demonstrate longitudinal analysis
3. **Visualize Data**: Step 3 highlights chart generation from financial data
4. **Competitive Intelligence**: Step 4 shows sector-wide analysis capabilities

## Scenario 3: Thematic Macro Advisor - Investment Theme Analysis ✅ PHASE 2

**Business Context**: Portfolio managers need to combine quantitative portfolio analysis with thematic research to identify and validate investment opportunities across macro trends.

**Persona**: Anna, Portfolio Manager (Thematic Focus)  
**Agent**: `thematic_macro_advisor`  
**Data Available**: Portfolio holdings data + 100 broker reports, 75 press releases, 75 earnings transcripts

### 4-Step Demo Conversation

#### Step 1: Current Thematic Positioning
**User Prompt**: 
```
"Analyze our current exposure to AI and technology themes across portfolios"
```

**Expected Response**:
- Technology sector allocation by portfolio
- AI-related company holdings and weights
- Thematic concentration analysis
- Benchmark comparison where available

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Current portfolio holdings with sector/thematic classification  
**Demo Points**: Show quantitative thematic exposure analysis

#### Step 2: Thematic Research Discovery  
**User Prompt**: 
```
"What are the key thematic investment opportunities for 2024 according to research?"
```

**Expected Response**:
- Emerging investment themes from broker research
- Corporate strategic initiatives from press releases
- Management outlook on themes from earnings calls
- Synthesis of macro trends and opportunities

**Tools Used**: `search_broker_research`, `search_press_releases`, `search_earnings_transcripts`  
**Data Accessed**: Documents filtered by thematic and macro trend keywords  
**Demo Points**: Show thematic research synthesis and opportunity identification

#### Step 3: Strategic Positioning Analysis
**User Prompt**: 
```
"How should we position for the energy transition theme based on current research and our holdings?"
```

**Expected Response**:
- Current renewable energy exposure in portfolios
- Energy transition research themes and opportunities
- Corporate positioning strategies from press releases
- Strategic positioning recommendations

**Tools Used**: `quantitative_analyzer`, `search_broker_research`, `search_press_releases`  
**Data Accessed**: Holdings analysis + thematic research synthesis  
**Demo Points**: Show combination of quantitative positioning with thematic research

#### Step 4: Cross-Theme Validation
**User Prompt**: 
```
"Analyze ESG themes versus technology themes - are there overlap opportunities in our portfolios?"
```

**Expected Response**:
- ESG and technology theme intersection analysis
- Companies positioned in both themes from holdings
- Research validation of sustainable technology trends
- Portfolio optimization recommendations

**Tools Used**: `quantitative_analyzer`, `search_broker_research`, `search_earnings_transcripts`  
**Data Accessed**: Holdings analysis + cross-thematic research synthesis  
**Demo Points**: Show complex thematic intersection analysis and validation

## Scenario 4: ESG Guardian - ESG Risk Monitoring

**Business Context**: ESG officers need proactive monitoring of sustainability risks, policy compliance, and engagement tracking to maintain ESG leadership and avoid reputational damage.

**Persona**: Sofia, ESG & Risk Officer  
**Agent**: `esg_guardian`  
**Data Available**: 500 NGO reports, 150 engagement notes, 8 policy documents

### 4-Step Demo Conversation

#### Step 1: Proactive Controversy Scanning
**User Prompt**: 
```
"Scan for any new ESG controversies affecting our portfolio companies in the last 30 days."
```

**Expected Response**:
- List of flagged controversies with severity levels (High/Medium/Low)
- Affected portfolio companies and exposure amounts
- Source citations with NGO names and publication dates

**Tools Used**: `quantitative_analyzer`, `search_ngo_reports`  
**Data Accessed**: Current holdings + recent NGO reports with controversy keywords  
**Demo Points**: Show proactive ESG risk monitoring and automatic flagging

#### Step 2: Internal Context Retrieval
**User Prompt**: 
```
"Do we have any engagement history with Nike regarding supply chain issues?"
```

**Expected Response**:
- Summary of previous engagement meetings and topics
- Key commitments made by management
- Follow-up actions and timelines from engagement logs

**Tools Used**: `search_engagement_notes`  
**Data Accessed**: Engagement logs filtered by company and topic  
**Demo Points**: Show internal knowledge retrieval and engagement tracking

#### Step 3: Policy Compliance Assessment
**User Prompt**: 
```
"What does our ESG policy say about human rights violations and what's our total exposure to Nike?"
```

**Expected Response**:
- Relevant policy clause with exact text and section reference
- Current total AUM exposure across all funds
- Policy-mandated actions (review, exclusion, engagement requirements)

**Tools Used**: `quantitative_analyzer`, `search_policy_docs`  
**Data Accessed**: Holdings aggregation + policy documents  
**Demo Points**: Show policy integration and compliance checking

#### Step 4: Committee Reporting
**User Prompt**: 
```
"Draft a summary for the ESG committee on this Nike situation."
```

**Expected Response**:
- Executive summary of the controversy and engagement history
- Portfolio impact assessment with exposure calculations
- Recommended actions with timeline and policy references

**Tools Used**: All tools synthesized  
**Data Accessed**: Combined information from previous queries  
**Demo Points**: Show comprehensive ESG governance and reporting

## Scenario 5: Compliance Advisor - Mandate Monitoring

**Business Context**: Compliance officers need automated monitoring of investment mandates, breach detection, and policy adherence to ensure regulatory compliance and fiduciary responsibility.

**Persona**: Compliance Officer  
**Agent**: `compliance_advisor`  
**Data Available**: 8 policy documents, 150 engagement logs, portfolio holdings

### 4-Step Demo Conversation

#### Step 1: Compliance Breach Detection
**User Prompt**: 
```
"Check all portfolios for active compliance breaches as of today."
```

**Expected Response**:
- List of breaches by portfolio and rule type
- Severity assessment (breach vs warning thresholds)
- Affected positions with amounts and percentages

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Current holdings vs compliance thresholds from config  
**Demo Points**: Show automated compliance monitoring and breach detection

#### Step 2: Rule Documentation
**User Prompt**: 
```
"Show me the exact IMA clause for the 7% single issuer concentration limit."
```

**Expected Response**:
- Exact policy text with section reference
- Applicable portfolios and any exceptions
- Historical context and rationale if available

**Tools Used**: `search_policy_docs`  
**Data Accessed**: IMA documents and policy manuals  
**Demo Points**: Show policy search and exact clause retrieval

#### Step 3: Remediation Planning
**User Prompt**: 
```
"What are our options for addressing the Microsoft overweight in the US Core portfolio?"
```

**Expected Response**:
- Calculation of excess exposure amount above limits
- Reduction scenarios with market impact considerations
- Timeline recommendations for compliance restoration

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Holdings data with liquidity and market impact analysis  
**Demo Points**: Show remediation planning and impact assessment

#### Step 4: Audit Trail Documentation
**User Prompt**: 
```
"Generate a compliance incident report for this concentration breach."
```

**Expected Response**:
- Formal incident documentation with timeline
- Policy references and breach calculations
- Remediation plan with milestones and responsibilities

**Tools Used**: `quantitative_analyzer`, `search_policy_docs`  
**Data Accessed**: Holdings data + compliance procedures and templates  
**Demo Points**: Show audit trail creation and formal reporting

## Scenario 6: Sales Advisor - Client Reporting

**Business Context**: Client relationship managers need to generate professional client reports, integrate investment philosophy, and maintain consistent messaging while ensuring compliance with regulatory requirements.

**Persona**: Client Relationship Manager  
**Agent**: `sales_advisor`  
**Data Available**: 2 sales templates, 3 philosophy documents, 8 policy documents

### 4-Step Demo Conversation

#### Step 1: Performance Report Generation
**User Prompt**: 
```
"Generate a monthly performance report for the ESG Leaders Global Equity portfolio."
```

**Expected Response**:
- Performance summary vs benchmark with key metrics
- Top contributors and detractors to performance
- Sector allocation and ESG score summary
- Professional formatting with appropriate disclaimers

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Performance data, holdings, ESG scores for ESG Leaders portfolio  
**Demo Points**: Show automated performance reporting and data synthesis

#### Step 2: Template Integration
**User Prompt**: 
```
"Format this report using our standard monthly client template."
```

**Expected Response**:
- Report restructured following template format
- Professional sections (Executive Summary, Performance, Holdings, Outlook)
- Consistent branding and compliance language
- Client-appropriate tone and structure

**Tools Used**: `search_sales_templates`  
**Data Accessed**: Monthly report template and formatting guidelines  
**Demo Points**: Show template-based formatting and professional presentation

#### Step 3: Philosophy Integration
**User Prompt**: 
```
"Add our ESG investment philosophy and approach to this report."
```

**Expected Response**:
- Integration of approved ESG messaging and philosophy
- Alignment of performance narrative with investment approach
- Strategic positioning and value proposition
- Consistent brand voice and messaging

**Tools Used**: `search_philosophy_docs`  
**Data Accessed**: ESG philosophy and brand messaging documents  
**Demo Points**: Show philosophy integration and consistent messaging

#### Step 4: Compliance Review
**User Prompt**: 
```
"Ensure this report includes all required compliance disclosures and disclaimers."
```

**Expected Response**:
- Addition of mandatory regulatory disclosures
- Risk warnings and performance disclaimers
- Fiduciary language and limitations
- Compliance-ready final document

**Tools Used**: `search_policy_docs`  
**Data Accessed**: Compliance requirements and disclosure templates  
**Demo Points**: Show compliance integration and regulatory adherence

## Scenario 7: Quant Analyst - Factor Analysis

**Business Context**: Quantitative analysts need advanced factor analysis, performance attribution, and systematic strategy development tools to identify patterns, screen securities, and develop data-driven investment approaches.

**Persona**: Quantitative Analyst  
**Agent**: `quant_analyst`  
**Data Available**: 1,200 broker reports, 800 earnings transcripts, factor exposure data

### 4-Step Demo Conversation

#### Step 1: Factor Screening
**User Prompt**: 
```
"Screen for stocks with improving momentum and quality factors over the last 6 months."
```

**Expected Response**:
- Filtered list of securities meeting factor criteria
- Factor score trends and statistical significance
- Current portfolio exposure to screened securities
- Factor ranking and percentile information

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Factor exposures, factor scores, portfolio holdings  
**Demo Points**: Show systematic factor screening and quantitative analysis

#### Step 2: Factor Comparison Analysis
**User Prompt**: 
```
"Compare factor loadings between our Value and Growth portfolios."
```

**Expected Response**:
- Side-by-side factor loading comparison table
- Statistical significance of differences
- Factor tilt analysis and style drift assessment
- Risk-adjusted performance implications

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Factor exposures for Value and Growth portfolios  
**Demo Points**: Show portfolio factor analysis and style comparison

#### Step 3: Backtesting Analysis
**User Prompt**: 
```
"Backtest a low volatility strategy over the last 3 years vs MSCI ACWI benchmark."
```

**Expected Response**:
- Simulated strategy performance vs benchmark
- Risk metrics (Sharpe ratio, maximum drawdown, volatility)
- Factor attribution of outperformance/underperformance
- Statistical analysis of results

**Tools Used**: `quantitative_analyzer`  
**Data Accessed**: Historical performance, factor data, benchmark returns  
**Demo Points**: Show backtesting capabilities and performance attribution

#### Step 4: Fundamental Context Integration
**User Prompt**: 
```
"What fundamental themes support the performance of our top-performing low volatility stocks?"
```

**Expected Response**:
- Analysis of fundamental characteristics of top performers
- Earnings trends and analyst sentiment for these securities
- Thematic and sector drivers of performance
- Integration of quantitative and qualitative insights

**Tools Used**: `quantitative_analyzer`, `search_broker_research`, `search_earnings_transcripts`  
**Data Accessed**: Performance data + research reports + earnings transcripts  
**Demo Points**: Show integration of quantitative analysis with fundamental research
