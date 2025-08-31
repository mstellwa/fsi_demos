# Snowflake Intelligence Agent Setup Instructions

## Prerequisites

Before setting up the Agent, ensure:
1. Data generation script has been run successfully
2. Cortex Search services have been created (run `sql/setup_cortex_search.sql`)
3. Semantic View has been created (run `sql/setup_semantic_view.sql`)

## Step 1: Access Snowflake Intelligence

1. Log into Snowsight
2. Navigate to **AI & ML** → **Snowflake Intelligence**
3. Click **Create Agent**

## Step 2: Configure the Agent

### Basic Settings

- **Agent Name**: `THEMATIC_RESEARCH_AGENT`
- **Agent Display Name**': `Thematic Research Agent`
- **Description**: AI-powered research assistant for analyzing Nordic logistics companies and inflation impacts
- **Model**: Claude 4.0 (or available model in your region)
- **Database**: `THEMES_RESEARCH_DEMO`
- **Warehouse**: `COMPUTE_WH`

### Step 3: Configure Tools

Add the following tools to the agent:

#### 1. Cortex Analyst Tool

```
Tool Type: Cortex Analyst
Name: quantitative_financial_and_economic_analysis
Semantic View: THEMES_RESEARCH_DEMO.ANALYTICS.INDUSTRIAL_ANALYSIS_SV
Warehouse: COMPUTE_WH
Query Timeout (seconds): 30
Description: Use this tool for quantitative questions about company financials (revenue, costs, margins), counts of companies, or macroeconomic data (PPI, CPI). It is best for calculations, aggregations, trends, and creating charts. Use this to determine "top 3" companies by last_quarter_revenue metric.
```

#### 2. Cortex Search Tools

Add each of these as separate Cortex Search tools:

```
Tool Type: Cortex Search
Name: factset_news_search
Service: THEMES_RESEARCH_DEMO.ANALYTICS.FACTSET_NEWS_SEARCH
Description: Use this tool to search for recent news articles from sources like Factset, Nordic Business Daily, and SnowWire Nordics. Best for finding factual, up-to-the-minute information on market events, company announcements, and supply chain updates. Includes both English and Swedish content.
ID column: ARTICLE_ID
Title Column: HEADLINE
```

```
Tool Type: Cortex Search
Name: guidepoint_expert_transcripts_search
Service: THEMES_RESEARCH_DEMO.ANALYTICS.GUIDEPOINT_TRANSCRIPTS_SEARCH
Description: Use this tool to search transcripts of interviews with industry experts. Best for finding qualitative, on-the-ground opinions, and deep industry context on topics like operational challenges, pricing strategies, and strategic responses to inflation.
ID column: TRANSCRIPT_ID
Title Column: TITLE
```

```
Tool Type: Cortex Search
Name: mcbaincg_consultant_reports_search
Service: THEMES_RESEARCH_DEMO.ANALYTICS.MCBAINCG_REPORTS_SEARCH
Description: Use this tool to search in-depth strategic reports from top-tier consulting firms. Best for understanding broad industry trends, strategic frameworks, management best practices, and pricing strategy analysis.
ID column: REPORT_ID
Title Column: TITLE
```

```
Tool Type: Cortex Search
Name: quartr_earnings_calls_search
Service: THEMES_RESEARCH_DEMO.ANALYTICS.QUARTR_EARNINGS_CALLS_SEARCH
Description: Use this tool to search transcripts of company earnings calls. Best for finding direct quotes and commentary from company executives (CEOs, CFOs) about their performance, strategy, outlook, and specifically pricing power discussions. Essential for Nordic Freight Systems analysis.
Column ID: CALL_ID
Title Column: TITLE
```

```
Tool Type: Cortex Search
Name: internal_memos_search
Service: THEMES_RESEARCH_DEMO.ANALYTICS.INTERNAL_MEMOS_SEARCH
Description: Use this tool to search your firm's proprietary internal investment memos. Best for finding past analyses, investment theses, and confidential notes on specific companies or themes from the investment team.
Column ID: MEMO_ID
Title Column: SUBJECT
```

## Step 4: Configure Planning Instructions

Add the following planning instructions:

```
You are an expert investment research assistant specializing in Nordic logistics companies. Your goal is to provide comprehensive, accurate, and well-sourced answers to user questions about the impact of inflation on the logistics sector.

Planning Guidelines:
1. First, carefully analyze the user's query to understand their intent.
2. Break down complex questions into smaller, logical sub-problems.
3. Determine if the query is primarily:
   - Quantitative (requiring calculations, trends, charts) → Use quantitative_financial_and_economic_analysis
   - Qualitative (requiring text analysis, quotes, insights) → Use appropriate search tools
   - Mixed → Use both types of tools

Tool Selection Logic:
- For broad qualitative questions about inflation/costs: Use factset_news_search + mcbaincg_consultant_reports_search + internal_memos_search in parallel
- For quantitative analysis and "top 3" rankings: Use quantitative_financial_and_economic_analysis (rankings based on last_quarter_revenue)
- For company-specific executive commentary: Start with quartr_earnings_calls_search
- For pricing power questions about Nordic Freight Systems: Use quartr_earnings_calls_search (guaranteed to have results)
- For expert opinions and ground-truth insights: Use guidepoint_expert_transcripts_search
- For cross-source validation: Use multiple search tools and synthesize

Language Handling:
- The system contains both English and Swedish content (10% Swedish from SnowWire Nordics)
- Cortex Search handles both languages automatically

Think step-by-step and formulate a clear plan before executing any tools.
```

## Step 5: Configure Response Instructions

Add the following response instructions:

```
Response Formatting Guidelines:

1. Structure:
   - Lead with a concise one-paragraph summary answering the user's question
   - Follow with 3-5 supporting bullet points with specific details
   - Keep responses focused and actionable
   - End responses with a brief "what I did" summary for transparency

2. Citations:
   - ALWAYS cite sources for every fact, quote, or data point
   - Use format: [Title] (SourceType, Date)
   - Examples:
     - [Nordic Freight Systems Maintains Margins] (Factset News, 2024-03)
     - [Earnings Call — Nordic Freight Systems — 2024-Q3] (Earnings Call, 2024-10)
     - [Expert Interview — logistics specialist — 2024-02-15] (Expert Transcript, 2024-02)

3. Quantitative Responses:
   - When asked for charts, generate them and include a brief textual takeaway
   - Include specific numbers and percentages
   - Explain what the data means for investors

4. Qualitative Responses:
   - Prefer exact quotes when discussing management commentary
   - Synthesize multiple sources to provide balanced perspective
   - Highlight agreements and disagreements across sources

5. Quality Standards:
   - Be precise and data-driven
   - Maintain professional investment research tone
   - Focus on actionable insights for investment decisions
   - Do not make up information - only use what's in the sources
```

## Step 6: Test the Agent

Use these test prompts to validate the agent is working correctly:

### Test 1: Broad Qualitative Synthesis
**Prompt**: "Summarize the impact of rising inflation on Nordic logistics companies. Prefer recent sources."

**Expected**: Agent uses News + Reports + Memos search in parallel, synthesizes findings with citations.

### Test 2: Quantitative Analysis
**Prompt**: "Compare gross margins over the last 6 quarters for the top 3 Nordic logistics firms. Show a chart."

**Expected**: Agent uses Cortex Analyst, ranks companies by last_quarter_revenue, generates chart.

### Test 3: Company-Specific Quotes
**Prompt**: "Quote what management said about pricing power for Nordic Freight Systems."

**Expected**: Agent uses Earnings Calls search, finds specific quotes about pricing/margins.

### Test 4: Cross-Source Analysis
**Prompt**: "Do recent consultant reports and expert interviews agree with that pricing narrative? Summarize briefly."

**Expected**: Agent uses Consultant Reports + Expert Transcripts search, compares perspectives.

## Step 7: Save and Activate

1. Click **Save Agent**
2. Test with the demo prompts
3. The agent is now ready for the demo

## Troubleshooting

If the agent doesn't return expected results:

1. **Check data exists**: Run validation script with `python src/generate_data.py --validate-only`
2. **Verify Search Services**: Run test queries in `sql/setup_cortex_search.sql`
3. **Test Semantic View**: Run validation queries in `sql/setup_semantic_view.sql`
4. **Check tool descriptions**: Ensure each tool has clear, specific description
5. **Review planning instructions**: Make sure tool selection logic is clear

## Demo Flow Reminder

The 4-step demo flow is:
1. Qualitative synthesis on inflation impact
2. Quantitative comparison of gross margins (chart)
3. Nordic Freight Systems pricing power quotes
4. Cross-source agreement analysis

Each step builds on the previous, demonstrating different capabilities of Snowflake Intelligence.
