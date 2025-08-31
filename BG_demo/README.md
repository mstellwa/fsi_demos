# SAM Snowsight Intelligence Demo

Complete demonstration of Snowflake Intelligence for asset management, featuring **Snowcap Asset Management** (SAM) - a fictional investment firm showcasing AI-powered research, portfolio management, and client services.

## 🎯 Demo Overview

This demo showcases three AI agents built on Snowflake Intelligence:

1. **Curiosity Co-Pilot** (Research Analyst) - Hybrid synthesis of quantitative data + qualitative insights with 10-Question Framework
2. **Conviction Engine** (Portfolio Manager) - Historical thesis evolution and systematic pre-mortem analysis using Corporate Memory
3. **Personalization & Narrative Suite** (Client Manager) - Personalized communications and meeting preparation with SAM philosophy

### Key Features
- **10-Question Investment Framework**: Structured research methodology for exceptional growth companies
- **Corporate Memory**: 20+ year simulated archive for institutional decision-making advantage
- **SAM Philosophy Integration**: "Patient capital," "unusual thinking," and "Actual Investor" approach
- **Hybrid Intelligence**: Seamlessly combines SQL analytics with document search
- **Realistic Data**: AI-generated synthetic documents with proper investment terminology

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Snowflake account with Cortex features enabled
- Python 3.8+ 
- Appropriate permissions for database/schema/table creation

### Step 1: Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure connection (update with your credentials)
cp connections.toml.template connections.toml
# Edit connections.toml with your Snowflake account details
```

### Step 2: Complete Setup (One Command)
```bash
# Run the unified orchestrator setup script
python setup/unified_setup.py
```

This unified orchestrator will:
- ✅ Execute modular SQL components in sequence (4 SQL files)
- ✅ Generate comprehensive synthetic data (6 companies, 3 clients, 40+ document templates)
- ✅ **Optimized bulk document generation** - 30 AI-generated documents in ~90 seconds (10x faster)
- ✅ Build semantic views with RELATIONSHIPS syntax
- ✅ Automatically create 3 specialized Cortex Search services
- ✅ Run end-to-end verification and validation

### Step 3: Configure Agents in Snowsight
After the setup completes, follow the enhanced configuration guide:
- `setup/AGENT_SETUP_INSTRUCTIONS.md` - Complete agent setup with 10-Question Framework and SAM philosophy

## 📊 Data Universe

### Companies (6 total)
- **Tempus AI** - Medical AI (8 quarters of data)
- **NorthernCell Energy** - Solid-state batteries (6 quarters)
- **Arkadia Commerce** - E-commerce platform (6 quarters) 
- **Voltaic Dynamics** - EV supply chain (6 quarters)
- **Helios Semiconductors** - AI chips (5 quarters)
- **TerraLink Logistics** - Global logistics (4 quarters)

### Clients (3 total)
- **Scottish Pension Trust** - £2.45B AUM, energy transition focus
- **Edinburgh University Endowment** - £890M AUM, tech innovation focus
- **Highland Family Office** - £326M AUM, private company focus

### Document Types
- Research notes and investment theses
- Historical documents (2019 vs 2022 comparisons)
- Internal meeting notes with management
- Client meeting notes and communications
- Earnings call transcripts and analysis

## 🎭 Enhanced Demo Scenarios

### Scenario 1: Research Analyst (10-Question Framework)
```
Query: "I'm new to Tempus AI and need to build conviction quickly. Use our 10-Question Framework to scaffold a preliminary analysis. Start with Questions 3-5: Scale of opportunity, competitive advantage, and management quality. For the competitive advantage section, I specifically need R&D spending trends over the last 8 quarters combined with sentiment analysis from their latest earnings Q&A about AI model performance. Include 2-3 direct quotes that support your assessment."

Expected: Framework-structured analysis + R&D trends + sentiment analysis + citations
```

### Scenario 2: Portfolio Manager (Thesis Evolution + Pre-mortem)
```
Query: "I'm reviewing our Arkadia Commerce position amid current market volatility. Show me the evolution of our investment thesis: side-by-side comparison of our 2019 initial investment view versus our 2022 updated position. Highlight what fundamental assumptions changed about their competitive moat against Amazon, and explain why these changes matter for our 5-10 year outlook. Then, run a pre-mortem: what are the top 3 ways this investment could fail, grounded in our firm's historical experience with similar platform companies?"

Expected: Side-by-side thesis evolution + pre-mortem analysis + corporate memory insights
```

### Scenario 3: Client Manager (Comprehensive Meeting Notes)
```
Query: "Generate comprehensive meeting notes for tomorrow's Scottish Pension Trust quarterly review. Include: meeting agenda, attendees, portfolio performance summary, detailed narratives for their top-3 holdings (with supporting quotes from our research), key risks being monitored, client ESG concerns, and specific follow-up actions. Ensure the tone reflects our 'patient capital' philosophy and their sustainability focus."

Expected: Professional 600-900 word meeting minutes + holdings narratives + SAM philosophy integration
```

## 🔧 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Structured    │    │   Unstructured   │    │  Snowsight      │
│   Data (SQL)    │    │   Documents      │    │  Intelligence   │
│                 │    │                  │    │                 │
│ • Financials    │    │ • Research Notes │    │ • 3 Agents      │
│ • Market Data   │───▶│ • Meeting Notes  │───▶│ • Search Tools  │
│ • Portfolios    │    │ • Client Comms   │    │ • Semantic Views│
│ • Client Data   │    │ • Historical     │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure (Unified Orchestrator)

```
├── connections.toml               # Snowflake connection config
├── requirements.txt              # Python dependencies
│
├── setup/                        # 🔥 Unified Orchestrator Setup
│   ├── unified_setup.py          # 🔥 Master setup script (run this!)
│   ├── AGENT_SETUP_INSTRUCTIONS.md   # Enhanced agent configuration
│   ├── demo_validation_checklist.md  # Testing and validation guide
│   ├── final_verification.py         # Infrastructure verification
│   └── semantic_views_reference.sql  # Reference for semantic view syntax
│
├── sql/                          # 🔥 Modular SQL Components (executed by unified_setup.py)
│   ├── 01_create_database_schema.sql      # Database and schema creation
│   ├── 02_create_structured_tables.sql    # All tables with foreign keys
│   ├── 03_populate_sample_data.sql        # Enhanced data + 40+ prompt templates
│   └── 04_create_services_and_views.sql   # Semantic views with RELATIONSHIPS
│
├── python/                       # 🔥 Document Generation Module (imported by unified_setup.py)
│   └── generate_synthetic_data.py         # Professional content generation (25+ docs)
│
└── .cursor/rules/                # Implementation architecture and requirements
    ├── unified-orchestrator-architecture.mdc  # 🔥 Master architecture specification
    ├── sam-demo-technical-requirements.mdc    # Technical implementation details
    ├── sam-demo-project-plan.mdc              # Implementation phases and timeline
    └── demo-enhancements.mdc                  # P0-P2 enhancement tracking
```

## 🆘 Troubleshooting

### Common Issues

**"Database FSI_DEMOS does not exist"**
```bash
# Ensure you have proper permissions
python -c "
import snowflake.snowpark as snowpark
session = snowpark.Session.builder.config('connection_name', 'your-connection').create()
session.sql('CREATE DATABASE FSI_DEMOS').collect()
"
```

**"AI_COMPLETE function not available"**
- Verify your account has Snowflake Cortex features enabled
- Check model availability in your region (us-west-2 recommended)
- Confirm role permissions for AI functions

**"Search services not ready"** 
```sql
-- Verify documents were created
SELECT COUNT(*) FROM FSI_DEMOS.SAM_DEMO.DOCUMENTS;

-- Check Cortex Search service status in Snowsight
-- Services take 2-3 minutes to index after creation
```

**🚨 MOST COMMON ISSUE: "Document indexing appears to be misconfigured"**
- **Problem**: Agent reports search system errors or indexing issues
- **Cause**: Missing ID Column and Title Column configuration in Cortex Search Service tools
- **Root Cause**: Search services must include `DOC_ID` and `FILE_URL` in ATTRIBUTES section:
  ```sql
  CREATE CORTEX SEARCH SERVICE service_name
  ON CONTENT
  ATTRIBUTES DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
  ```
- **Solution**: For ALL search service tools in agents, configure:
  - **ID Column**: `DOC_ID`
  - **Title Column**: `FILE_URL`
- **Verification**: `SELECT DOC_ID, FILE_URL FROM FSI_DEMOS.SAM_DEMO.DOCUMENTS LIMIT 3`

**"Agents not finding tools"**
- Ensure you're in the correct database (FSI_DEMOS) and schema (SAM_DEMO)
- Verify search services are created and indexed
- Check semantic views with: `SHOW SEMANTIC VIEWS IN SCHEMA SAM_DEMO`
- Confirm all search service tools have ID and Title columns properly configured

## 🎊 Success Metrics

Setup is successful when:
- ✅ 6 companies with financial data created (Tempus AI with 8 quarters)
- ✅ 3 clients with portfolio holdings created (Scottish Pension Trust, etc.)
- ✅ 30 realistic documents generated with SAM philosophy (10x faster than before)
- ✅ 10-Question Framework integrated in Research Analyst responses
- ✅ Thesis evolution analysis working for Portfolio Manager
- ✅ Client personalization with ESG alignment working
- ✅ All citations are accurate and grounded in source documents

## ⚡ Performance Optimizations

The demo features **SQL-based bulk document generation** for dramatically improved performance:

### **Before Optimization:**
- Sequential Python `AI_COMPLETE` calls
- ~15+ minutes for 30 documents
- Row-by-row processing

### **After Optimization:**
- **90 seconds for 30 documents** (10x improvement)
- Leverages Snowflake parallel processing
- Model-by-model bulk SQL generation
- Robust fallback handling

### **Technical Implementation:**
1. **RENDERED_PROMPTS Table** - Pre-rendered prompts stored for bulk processing
2. **Bulk SQL Generation** - `SNOWFLAKE.CORTEX.COMPLETE` with model grouping
3. **Optimized Workflow** - Separates prompt rendering from AI generation
4. **Error Handling** - Graceful fallback to individual processing if needed

### **Key Benefits:**
- ✅ **Much faster iteration** during development and testing
- ✅ **Scalable architecture** for larger document sets
- ✅ **Production-ready performance** for demos and real usage
- ✅ **Maintains data integrity** with proper array handling

## 📚 Additional Resources

- [Snowflake Intelligence Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence)
- [Cortex Search Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview)
- [Snowpark Python Guide](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)

---

**Ready to wow your asset management prospects with AI-powered intelligence! 🚀**
