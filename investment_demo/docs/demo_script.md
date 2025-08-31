# Demo Script: Thematic Research Tool for Nordic Logistics Analysis

## Demo Overview
**Duration**: 10-12 minutes  
**Audience**: Investment firm executives and analysts  
**Scenario**: Investment associate "Anna" researching inflation impact on Nordic logistics companies  

---

## Opening Context & Narrative Setup (2 minutes)

### The Scenario
"Let me introduce you to Anna, an investment associate at our fictional investment firm 'Investor Listed.' She's been tasked with preparing a comprehensive report on the impact of rising inflation on Nordic industrial companies for an upcoming strategy offsite meeting tomorrow morning."

### The Traditional Challenge
"Traditionally, this kind of thematic research would take Anna several days:
- Manually searching through disconnected data sources
- Reading hundreds of pages of reports, news articles, and transcripts
- Copying and pasting information into spreadsheets
- Struggling to synthesize conflicting information from different sources
- Worrying about missing critical insights buried in the data

This is the 'data overload crisis' that every investment analyst faces today."

### The Solution Introduction
"Today, I'll show you how Snowflake Intelligence transforms Anna from a data gatherer into a strategic thinker. Our AI-powered Thematic Research Tool will help her complete this analysis in minutes instead of days, with full transparency and citations for every insight."

### Key Value Proposition
"What makes this different from a generic AI chatbot is that it:
1. Searches across ALL her firm's data sources simultaneously - both internal and external
2. Provides traceable citations for every claim - critical for investment decisions
3. Seamlessly combines quantitative financial analysis with qualitative insights
4. Maintains the context of her investigation throughout the conversation"

---

## Demo Flow: The 4-Step Investigation (8 minutes)

### Step 1: Opening with Broad Thematic Research (2 min)
**Context:** "Anna starts with a broad question to understand the overall landscape."

**Prompt 1:** 
```
Summarize the impact of rising inflation on Nordic logistics companies. Prefer recent sources.
```

**Narrative during response:** 
"Notice how the Agent is simultaneously searching across multiple sources - recent news from FactSet and SnowWire Nordics, our internal investment memos, and industry reports. It's not just keyword matching - it understands the semantic meaning of 'inflation impact' and 'Nordic logistics.'"

**Key points to highlight:**
- Multiple sources being queried in parallel (show the tool calls if visible)
- Citations appear inline: [Headline] (FactSet News, Date)
- The synthesis combines different perspectives into a coherent narrative
- Both English and Swedish sources are seamlessly integrated

**Expected Response Elements:**
- Rising fuel and labor costs impacting margins
- Supply chain disruptions exacerbating pressures
- Some companies showing resilience through pricing power
- References to recent news and internal analysis

---

### Step 2: Drilling into Quantitative Analysis (2 min)
**Context:** "Now Anna wants to see which companies have been most resilient. She needs hard numbers to support her analysis."

**Prompt 2:**
```
Which companies have been most successful in preserving their margins over the last year? Show me a chart.
```

**Narrative during response:**
"The Agent recognizes this is a quantitative question and automatically switches to Cortex Analyst. It's translating Anna's natural language into precise SQL queries against our Semantic View, which understands our business terminology - it knows what 'top 3' means, what constitutes a 'Nordic logistics firm,' and how to calculate gross margins."

**Key points to highlight:**
- Automatic tool selection based on query intent
- Visual chart generation directly in the interface
- The Agent identifies the top 3 by revenue (Nordic Freight Systems, Arctic Cargo AB, Snowline Transport ASA)
- Trend analysis showing margin compression or resilience

**Expected Response Elements:**
- Bar or line chart showing 6 quarters of data
- Nordic Freight Systems showing superior margin performance
- Clear ranking of top 3 companies
- Numerical values for comparison

---

### Step 3: Seeking Management Commentary (2 min)
**Context:** "Anna notices Nordic Freight Systems has maintained better margins than competitors. She wants to understand their strategy directly from management."

**Prompt 3:**
```
For "Nordic Freight Systems", what has management said about their pricing strategy?
```

**Narrative during response:**
"The Agent knows to search the earnings call transcripts for this specific company. It's not just finding any mention of pricing - it's identifying actual management commentary about pricing power and strategy."

**Key points to highlight:**
- Direct quotes from CEO/CFO with specific attribution
- The quote explains their dynamic pricing models and fuel surcharges
- Shows the ~90% cost pass-through achievement
- Demonstrates the value of having transcripts integrated into the analysis

**Expected Response Elements:**
- Direct quote from CEO or CFO
- Mention of dynamic pricing models
- Reference to fuel surcharges
- ~90% cost pass-through achievement
- Attribution to specific earnings call (Q3 2023, etc.)

---

### Step 4: Validating the Investment Thesis (2 min)
**Context:** "Before Anna finalizes her recommendation, she wants to validate if external experts and consultants agree with management's narrative."

**Prompt 4:**
```
Do recent consultant reports and expert interviews agree with that pricing narrative? Summarize briefly.
```

**Narrative during response:**
"This is where the real power of multi-source synthesis shines. The Agent is cross-referencing management's claims against independent third-party analysis from McBainCG consultants and industry experts from Guidepoint."

**Key points to highlight:**
- Triangulation across different source types
- Independent validation of management claims
- Identification of any conflicting views or caveats
- Synthesis into an actionable investment insight

**Expected Response Elements:**
- Confirmation from consultant reports about pricing power in consolidated markets
- Expert validation of dynamic pricing effectiveness
- Some skepticism about sustainability if inflation moderates
- Overall agreement with management's narrative

---

## Closing & Business Impact (2 minutes)

### The Transformation
"In less than 10 minutes, Anna has:
1. Understood the broad macroeconomic context
2. Identified the best-performing companies with data to prove it
3. Discovered the specific strategies driving outperformance
4. Validated these findings with independent sources

What traditionally took days of manual research is now completed in a single conversation."

### The Competitive Advantage
"For an investment firm, this means:
- **Faster decisions**: React to market events in hours, not days
- **Broader coverage**: Analysts can investigate more themes and companies
- **Better insights**: Never miss critical information buried in documents
- **Risk mitigation**: Every decision is backed by traceable, auditable sources
- **Alpha generation**: Find opportunities before competitors who are still doing manual research"

### Technical Differentiators
"This is only possible with Snowflake's unique architecture:
- **Unified data platform**: All sources in one place, no data movement
- **Cortex Intelligence**: Purpose-built AI for enterprise data
- **Semantic understanding**: The system truly understands your business context
- **Enterprise-grade security**: Your proprietary data never leaves your Snowflake account
- **Full governance**: Complete audit trail and access controls"

### Call to Action
"Imagine your analysts having this capability across all your portfolio companies, all your research themes, available 24/7. That's the transformation Snowflake Intelligence delivers."

---

## Demo Tips & Troubleshooting

### If Asked About Data Sources
"We're searching across:
- 50+ news articles including 10% Swedish content from SnowWire Nordics
- 12 expert interview transcripts from Guidepoint-style networks
- 8 strategic reports from McBainCG consultants
- 32 earnings call transcripts (6 quarters for Nordic Freight Systems)
- 12 internal investment memos from the firm's proprietary research"

### If Asked About Accuracy
"Every insight is traceable to its source. Click on any citation to see the original passage. This isn't a 'black box' AI - it's transparent and auditable, which is critical for investment decisions."

### If Results Seem Slow
"The system is searching across hundreds of documents in multiple languages simultaneously. In production, with proper indexing and caching, responses are typically sub-second."

### Expected Insights to Highlight
- Nordic Freight Systems' superior margin performance
- Their 90% cost pass-through achievement via dynamic pricing
- Validation from consultants about pricing power in consolidated markets
- Some expert skepticism about sustainability if inflation moderates

### Common Objections & Responses

**"How do we know the AI isn't hallucinating?"**
- Every fact has a citation you can click to verify
- The system only searches YOUR data, not the open internet
- Cortex Search uses semantic understanding, not generation

**"What about data security?"**
- All processing happens within your Snowflake account
- No data leaves your security perimeter
- Full audit trail of all queries and access

**"Can it handle our proprietary formats?"**
- Yes, the system adapts to any structured or unstructured format
- We've shown integration with diverse sources: JSON transcripts, markdown reports, etc.
- Custom connectors can be built for any data source

---

## Technical Setup Notes

### Pre-Demo Checklist
- [ ] Verify all 5 Cortex Search services are active
- [ ] Confirm Semantic View is functional
- [ ] Test each of the 4 demo prompts
- [ ] Ensure Nordic Freight Systems data is present
- [ ] Check that Swedish content is properly tagged

### Data Volumes
- 12 logistics companies (Nordic Freight Systems mandatory)
- 18 quarters of financial data
- 50 news articles (5 in Swedish)
- 12 expert transcripts
- 8 consultant reports
- 32 earnings calls
- 12 internal memos

### Key Companies to Reference
1. **Nordic Freight Systems** (star performer)
2. Arctic Cargo AB
3. Snowline Transport ASA
4. Lapland Freight Oy
5. Baltic Logistics Group

---

## Quick Reference Card

### The 4 Demo Prompts (Copy & Paste)
1. `Summarize the impact of rising inflation on Nordic logistics companies. Prefer recent sources.`
2. `Compare gross margins over the last 6 quarters for the top 3 Nordic logistics firms. Show a chart.`
3. `Quote what management said about pricing power for "Nordic Freight Systems".`
4. `Do recent consultant reports and expert interviews agree with that pricing narrative? Summarize briefly.`

### Key Messages
- **From data gatherer to strategic thinker**
- **Minutes not days**
- **Full transparency and citations**
- **Alpha generation at scale**

### Success Metrics to Mention
- 10x faster research cycle
- 3x more themes covered
- 100% source traceability
- 24/7 availability
