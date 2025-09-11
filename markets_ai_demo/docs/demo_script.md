# Demo Script: Frost Markets Intelligence - Snowflake AI Demo

This document provides complete scripts for delivering the Frost Markets Intelligence demo to clients, showcasing Snowflake AI capabilities for financial markets research.

## 🎯 Demo Overview

**Duration**: 45-60 minutes (15 minutes per scenario)  
**Format**: Modular - can demo individual scenarios or all three  
**Audience**: Financial services professionals, data teams, AI/ML practitioners  
**Goal**: Demonstrate intelligence augmentation for financial analysts using Snowflake AI

## 📋 Pre-Demo Checklist

### Technical Preparation
- [ ] Demo setup completed (`python setup.py --mode=full`)
- [ ] All three agents configured in Snowsight (see [agent_setup_instructions.md](agent_setup_instructions.md))
- [ ] Test queries verified for all scenarios
- [ ] Snowsight tabs pre-opened to Snowflake Intelligence
- [ ] Network connection stable

### Narrative Preparation
- [ ] Review client's specific use cases and pain points
- [ ] Customize talking points for their industry/role
- [ ] Prepare for potential questions about data sources, security, scalability
- [ ] Have backup demo environment ready if needed

---

## 🏦 Scenario 1: Global Research & Market Insights - Market Structure Reports (15 minutes)

### Business Context Setup (2 minutes)

**Persona**: Market Structure Analyst at Frost Markets Intelligence

**Business Challenge**: 
"Traditional market structure research is reactive and generic. By the time we publish quarterly reports, the content is already consensus. More critically, we can't easily identify which clients should be prioritized for strategic discussions on emerging regulatory changes like EMIR 3.0."

**Value Proposition**:
- **Hyper-Personalization**: Transform generic reports into client-specific insights
- **Engagement Analytics**: Measure which topics resonate with different client segments
- **Strategic Targeting**: Identify high-value clients for proactive outreach
- **Regulatory Intelligence**: Faster identification of regulatory impact by client trading patterns

**AI Tools in Use**:
- **CLIENT_MARKET_IMPACT_VIEW**: Client analytics combining trading, engagement, and discussion data
- **RESEARCH_REPORTS_SEARCH**: Market structure content discovery
- **NEWS_ARTICLES_SEARCH**: Latest regulatory developments
- **Cortex Complete**: Personalized content generation

---

### Demo Flow

#### Setup (30 seconds)

**Navigation**: Open Snowsight → Snowflake Intelligence → Select "Market Structure Reports Assistant"

**Scene Setting**: "Let's help Sarah, a Market Structure Analyst, author her quarterly FICC report while identifying clients who need proactive EMIR 3.0 discussions."

---

#### Query 1: Market Structure Theme Discovery (4 minutes)

**User Input:**
```
What have been the most significant developments in FICC market structure in EMEA over the past quarter?
```

**Expected Response:**
- Identification of EMIR 3.0 as the dominant theme in Q2 2025 FICC markets
- Discussion of "active account requirement" for Euro-denominated derivatives
- Additional themes: bond market transparency, MiFID II evolution, algorithmic trading adoption
- Specific regulatory timeline and implementation details for EMEA region
- Reference to Q2 2025 timeframe and European fixed income market developments

**Troubleshooting Note:** If the agent's response is generic or doesn't focus on FICC/EMEA/past quarter, it might be due to search service indexing. Wait a few minutes and try again. If it persists, try a more direct prompt like: "Show me our internal research on EMIR 3.0 and FICC regulatory developments" or "What does our Q2 2025 FICC market structure review say about EMEA developments?"

**Demo Talking Points:**
- **"The agent is searching our internal research reports and market intelligence"**
- **"This goes beyond generic market commentary - it's our firm's proprietary analysis"**
- **"Notice how it identifies the most impactful theme for our client base"**

**Key Features Highlighted:**
- Internal content discovery across research reports
- Regulatory expertise and interpretation
- Prioritization based on business impact
- Timeline-aware analysis

---

#### Query 2: Client Engagement Analytics (4 minutes)

**User Input:**
```
Which of these topics has generated the most engagement from our asset manager clients?
```

**Expected Response:**
- EMIR 3.0 has driven significantly higher engagement from asset managers
- Quantified metrics: "45% more engagement than other market structure themes"
- Specific engagement data: downloads, view time, client interaction patterns
- Comparison across client segments showing asset manager preference

**Demo Talking Points:**
- **"Now we're analyzing client behavior data - who's actually engaging with our content"**
- **"This isn't just page views - it's measuring true engagement depth and duration"**
- **"Asset managers clearly see EMIR 3.0 as most relevant to their business"**

**Key Features Highlighted:**
- Client behavior analytics integration
- Segmentation by client type and engagement patterns
- Quantified business intelligence
- Content performance measurement

---

#### Query 3: Strategic Client Targeting (4 minutes)

**User Input:**
```
Generate a list of asset manager clients who have shown high engagement on EMIR 3.0 but have not yet had a one-on-one discussion with us about it.
```

**Expected Response:**
- Prioritized list of target clients (e.g., "Maxwell-Reed Asset Management")
- Engagement metrics for each (number of downloads, view duration)
- Discussion gap analysis (high engagement + no recent regulatory discussions)
- Suggested talking points based on client trading patterns

**Demo Talking Points:**
- **"This is where AI becomes truly strategic - identifying business development opportunities"**
- **"We're combining content engagement with relationship management data"**
- **"Each client represents a potential high-value strategic discussion"**

**Key Features Highlighted:**
- Cross-system data integration (engagement + CRM)
- Opportunity identification and prioritization
- Relationship gap analysis
- Actionable business intelligence

---

#### Query 4: Personalized Content Generation (3 minutes)

**User Input:**
```
Draft the executive summary for my quarterly report, leading with the EMIR 3.0 theme and its specific implications for asset managers.
```

**Expected Response:**
- Professional executive summary starting with EMIR 3.0 impact
- Specific implications for asset manager segment
- Clear regulatory timeline and requirements
- Strategic recommendations for clearing relationships
- Business-ready content requiring minimal editing

**Demo Talking Points:**
- **"From analysis to publication-ready content in seconds"**
- **"Notice how it tailors the content specifically for asset managers"**
- **"This maintains our analytical rigor while dramatically accelerating delivery"**

**Key Features Highlighted:**
- Contextualized content generation
- Segment-specific customization
- Professional tone and structure
- Integration of previous analysis into narrative

---

### Scenario 1 Wrap-up (2 minutes)

**Business Impact Summary:**
- **Revenue Growth**: "Identify and prioritize high-value client opportunities proactively"
- **Operational Efficiency**: "Reduce report compilation time from days to hours"
- **Client Experience**: "Deliver hyper-personalized content that drives engagement"
- **Strategic Intelligence**: "Transform client interaction data into business development insights"

**Technical Differentiators:**
- Multi-system data integration (trading, engagement, CRM)
- Real-time client behavior analytics
- Automated opportunity identification
- Regulatory expertise automation

---

## 🎭 Scenario 2: Equity Research Analyst - Earnings Analysis (15 minutes)

### Business Context Setup (2 minutes)

**"Let me show you how Snowflake AI transforms the most time-critical workflow in equity research - earnings season analysis."**

**Pain Points to Address:**
- Analysts spend 3-5 hours per company during earnings season
- Manual data extraction from PDFs and transcripts
- Pressure to publish "First Take" notes within minutes of earnings release
- Need to synthesize quantitative results with qualitative management commentary

**Value Proposition:**
- Reduce analysis time by 50-75%
- Automated extraction from unstructured documents
- Instant cross-referencing between financial data and management comments
- Professional-grade outputs ready for client distribution

### Demo Flow

#### Setup (30 seconds)
- Open Snowsight → Snowflake Intelligence
- Select **"Earnings Analysis Assistant"**
- **Context**: "We're a research analyst at Frost Markets Intelligence covering Netflix. Earnings just came out after market close."

---

#### Query 1: Financial Results Summary (3 minutes)

**User Input:**
```
Give me a summary of Netflix's latest quarter results
```

**Expected Response:**
- Revenue, EPS, subscriber additions vs consensus estimates
- Beat/miss percentages clearly stated
- Key operational metrics

**Demo Talking Points:**
- **"Notice how the agent immediately pulls structured financial data"**
- **"Beat/miss calculations are automatic - no manual Excel work needed"**
- **"This would normally take 15-20 minutes of manual data gathering"**

**Key Features Highlighted:**
- Cortex Analyst querying semantic views
- Structured data analysis with instant calculations
- Professional financial terminology and formatting

---

#### Query 2: Management Commentary Analysis (4 minutes)

**User Input:**
```
What was management's tone during the Q&A session regarding future subscriber growth?
```

**Expected Response:**
- Specific quotes from the earnings call transcript
- Sentiment analysis of management commentary
- Context around analyst questions and management responses

**Demo Talking Points:**
- **"Now we're seamlessly moving from quantitative to qualitative analysis"**
- **"The agent is searching through the full earnings call transcript"**
- **"This eliminates the need to manually read through 50+ pages of transcript"**

**Key Features Highlighted:**
- Cortex Search on unstructured documents
- Semantic search capabilities (not just keyword matching)
- Integration of AI sentiment analysis

---

#### Query 3: Comparative Visualization (3 minutes)

**User Input:**
```
Generate a bar chart comparing reported revenue, EPS, and net adds against consensus for the last 4 quarters
```

**Expected Response:**
- Data table with historical beat/miss analysis
- Formatted for easy visualization
- Clear trend analysis

**Demo Talking Points:**
- **"The agent can instantly generate historical comparisons"**
- **"This data could feed directly into client presentations"**
- **"What used to require complex Excel formulas is now conversational"**

**Key Features Highlighted:**
- Historical data analysis across multiple metrics
- Data visualization capabilities
- Time series analysis with consensus comparisons

---

#### Query 4: Research Note Generation (3 minutes)

**User Input:**
```
Draft a 'First Take' summary for my note, including the headline numbers, the significant subscriber beat, and management's cautious tone on future growth
```

**Expected Response:**
- Professional research note format
- Synthesis of quantitative and qualitative insights
- Ready-to-publish language and structure

**Demo Talking Points:**
- **"This is where everything comes together - the agent synthesizes all our analysis"**
- **"Professional research note quality, generated in seconds"**
- **"From earnings release to publishable content in under 5 minutes"**

**Key Features Highlighted:**
- AI content generation with professional formatting
- Synthesis across multiple data sources
- Context-aware financial writing

---

### Scenario 2 Wrap-up (2 minutes)

**Business Impact Summary:**
- **Time Savings**: "5-minute analysis vs 3-hour manual process"
- **Quality Improvement**: "No more transcription errors or missed data points"
- **Scalability**: "Analysts can now cover more companies during earnings season"
- **Competitive Advantage**: "First to market with comprehensive analysis"

**Technical Differentiators:**
- Unified platform for structured and unstructured data
- Real-time semantic search across documents
- Professional-grade financial language generation

---

## 🔬 Scenario 3: Equity Research Analyst - Thematic Research (15 minutes)

### Business Context Setup (2 minutes)

**"Now let me show you how Snowflake AI helps analysts discover emerging investment themes before they become consensus."**

**Pain Points to Address:**
- Finding differentiated research angles in crowded markets
- Manual analysis of thousands of documents across different sources
- Connecting dots between scientific developments and investable companies
- Staying ahead of thematic trends

**Value Proposition:**
- Discover themes from alternative data sources
- Automated cross-sector analysis
- Link scientific/technical developments to public companies
- Generate actionable investment ideas with supporting data

### Demo Flow

#### Setup (30 seconds)
- Select **"Thematic Investment Research Assistant"**
- **Context**: "We're looking for emerging themes to generate differentiated research ideas."

---

#### Query 1: Theme Discovery (4 minutes)

**User Input:**
```
What are the emerging trends in carbon capture technology according to recent scientific papers and patent filings?
```

**Expected Response:**
- Identification of Direct Air Capture (DAC) trends
- Analysis of patent filings and scientific developments
- Technical details about solid sorbents and modular designs

**Demo Talking Points:**
- **"The agent is analyzing scientific literature and patent data"**
- **"This goes beyond traditional financial data sources"**
- **"Finding investable themes from technical innovation"**

**Key Features Highlighted:**
- Alternative data source integration
- Cross-document thematic analysis
- Technical content understanding and synthesis

---

#### Query 2: Company Exposure Analysis (4 minutes)

**User Input:**
```
Which publicly traded industrial companies are mentioned most frequently in relation to these new DAC technologies, either as developers or key suppliers?
```

**Expected Response:**
- List of public companies (Johnson Matthey, Linde, Siemens)
- Their specific roles in the carbon capture ecosystem
- Frequency of mentions and relevance analysis

**Demo Talking Points:**
- **"Now we're connecting themes to investable companies"**
- **"The agent identifies both direct players and supply chain beneficiaries"**
- **"This creates actionable investment universe from thematic research"**

**Key Features Highlighted:**
- Entity extraction and relationship mapping
- Public company identification from unstructured data
- Investment relevance scoring

---

#### Query 3: Performance Analysis (4 minutes)

**User Input:**
```
Show me the stock performance of those three companies over the last year. On the same chart, overlay any significant news announcements related to 'carbon capture' for each company
```

**Expected Response:**
- Stock price performance data for identified companies
- Timeline of carbon capture-related news events
- Performance correlation with news flow

**Demo Talking Points:**
- **"Seamlessly moving from thematic research to quantitative analysis"**
- **"Correlating news flow with stock performance"**
- **"Identifying which companies benefit most from theme momentum"**

**Key Features Highlighted:**
- Integration of market data with news analysis
- Event-driven performance analysis
- Multi-source data correlation

---

#### Query 4: Investment Thesis Development (3 minutes)

**User Input:**
```
It looks like Johnson Matthey has underperformed the other two. Summarize their specific involvement in the space and the general sentiment around their carbon capture efforts based on the available documents
```

**Expected Response:**
- Detailed analysis of Johnson Matthey's carbon capture exposure
- Sentiment analysis of their competitive position
- Balanced assessment of opportunities and risks

**Demo Talking Points:**
- **"The agent provides nuanced investment analysis"**
- **"Balancing technical potential against commercial viability"**
- **"This kind of company-specific thematic analysis is usually manual intensive research"**

**Key Features Highlighted:**
- Company-specific thematic analysis
- Sentiment analysis across multiple document types
- Balanced risk/opportunity assessment

---

### Scenario 3 Wrap-up (2 minutes)

**Business Impact Summary:**
- **Research Differentiation**: "Unique insights from alternative data sources"
- **Time to Market**: "Faster identification of emerging themes"
- **Coverage Expansion**: "Analysts can explore more themes systematically"
- **Alpha Generation**: "Earlier identification of investment opportunities"

**Technical Differentiators:**
- Multi-source document analysis and synthesis
- Thematic pattern recognition across data types
- Investment-focused entity extraction and mapping

---

## 💡 Advanced Demo Techniques

### Customization for Different Audiences

**For Data Teams:**
- Emphasize semantic view architecture and data modeling
- Show SQL queries behind agent responses
- Discuss search service configuration and optimization

**For Business Users:**
- Focus on workflow transformation and time savings
- Highlight professional output quality
- Demonstrate ease of use and natural language interaction

**For IT/Security Teams:**
- Discuss data governance and access controls
- Show audit trails and query logging
- Address model selection and customization options

### Handling Questions

**"How accurate is the AI-generated content?"**
- Show data sources and citations in responses
- Demonstrate validation capabilities with manual spot-checks
- Discuss confidence scoring and human review workflows

**"Can this work with our data?"**
- Explain semantic view flexibility for different data schemas
- Show how search services adapt to various document types
- Discuss integration patterns and data pipeline options

**"What about hallucinations or errors?"**
- Demonstrate source citations and traceability
- Show how responses are grounded in actual data
- Discuss validation workflows and human oversight

**"How does this scale?"**
- Explain warehouse separation and auto-scaling
- Show performance across different data volumes
- Discuss multi-user scenarios and resource management

### Demo Recovery Strategies

**If a query fails:**
1. **Acknowledge quickly**: "Let me try a different approach"
2. **Use backup queries**: Have 2-3 variations of each demo query ready
3. **Show manual validation**: Query the underlying tables directly
4. **Turn it into teaching**: "This shows the importance of data validation"

**If agent responds poorly:**
1. **Refine the query**: "Let me be more specific"
2. **Show iterative improvement**: Demonstrate query refinement
3. **Explain limitations**: "AI works best with specific, context-rich queries"

---

## 🎯 Key Messages to Reinforce

### Throughout Demo
1. **"Intelligence Augmentation, not Replacement"** - AI enhances human expertise
2. **"Unified Platform"** - One system for all data types and AI capabilities
3. **"Professional Grade"** - Ready for production financial workflows
4. **"Conversational Interface"** - No complex query languages needed

### Demo Conclusion
**"What you've seen is the future of financial analysis - where AI handles the repetitive work so analysts can focus on insight generation and client relationships. This isn't just faster data processing; it's a fundamental transformation of how financial research gets done."**

---

## 📊 Demo Metrics & ROI

### Quantifiable Benefits Demonstrated
- **75% reduction** in earnings analysis time (5 min vs 3+ hours)
- **10x faster** thematic research discovery
- **Unified workflow** across structured and unstructured data
- **Professional output quality** ready for client distribution

### Next Steps for Prospects
1. **Technical Deep Dive**: Architecture review and integration planning
2. **Pilot Program**: Limited scope implementation with specific use cases  
3. **Data Assessment**: Review of their existing data sources and quality
4. **ROI Modeling**: Quantified business case development

---

*For technical setup instructions, see [agent_setup_instructions.md](agent_setup_instructions.md).*  
*For troubleshooting, see [README.md](../README.md).*