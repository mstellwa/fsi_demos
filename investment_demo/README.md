# Thematic Research Tool Demo for Snowflake Intelligence

## Overview

This demo showcases Snowflake Intelligence capabilities for investment research, demonstrating how AI can help analysts quickly synthesize information from multiple sources to understand the impact of inflation on Nordic logistics companies.

## Demo Scenario

An investment associate at "Investor Listed" needs to research how rising inflation affects industrial companies for an upcoming strategy meeting. Using Snowflake Intelligence, they can query both structured financial data and unstructured text sources (news, reports, transcripts) in natural language, getting synthesized insights with citations in minutes instead of days.

## Key Features

- **Multi-source synthesis**: Combines news, expert interviews, consultant reports, earnings calls, and internal memos
- **Quantitative analysis**: Financial metrics, trends, and comparisons via Cortex Analyst
- **Qualitative insights**: Semantic search across unstructured documents via Cortex Search
- **Intelligent orchestration**: Agent automatically selects appropriate tools based on query intent
- **Full citations**: Every fact is traceable to its source with `[Title] (SourceType, Date)` format
- **Multilingual**: Includes 10% Swedish content from SnowWire Nordics

## Project Structure

```
investment_demo/
├── setup_demo.py                    # Main orchestration script (run this!)
├── requirements.txt                 # Python dependencies
├── README.md                       # This file
├── src/                            # Core implementation modules
│   ├── config.py                   # Configuration settings
│   ├── generate_data.py            # Data generation orchestrator
│   ├── structured_data_generator.py # Companies, financials, macro data
│   ├── unstructured_data_generator.py # Content generation via Cortex Complete
│   ├── data_validator.py           # Validation checks
│   └── cortex_objects_creator.py   # Creates Cortex Search services & Semantic Views
├── docs/
│   └── agent_setup_instructions.md # Detailed agent configuration
└── demo_research/                  # Design documentation
    ├── Snowflake AI Research Tool Demo.md # Original design doc
    └── gpt_review.md               # Design review and refinements
```

## Prerequisites

1. **Snowflake Account** with:
   - Cortex Complete enabled (llama3.1-8b model)
   - Cortex Search enabled
   - Cortex Analyst enabled
   - Snowflake Intelligence access
   - Claude 4.0 model (for Agent)

2. **Local Environment**:
   - Python 3.8+
   - Snowflake connection configured in `~/.snowflake/connections.toml`

## Quick Setup (Recommended)

### One-Command Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete setup (data + SQL objects)
python setup_demo.py
```

This single command will:
1. Connect to Snowflake (using default connection: `sfseeurope-mstellwall-aws-us-west3`)
2. Create database and schemas
3. Generate all synthetic data using Cortex Complete
4. Create Cortex Search services
5. Create Semantic View
6. Validate everything is working

**Expected runtime: 10-15 minutes**

### Alternative Setup Options

```bash
# Use a different connection
python setup_demo.py --connection your_connection_name

# Skip confirmation prompts
python setup_demo.py --quick

# Validate existing setup
python setup_demo.py --validate-only

# Generate data only (skip SQL objects)
python setup_demo.py --skip-objects
```

## Detailed Setup (Manual Steps)

If you prefer to understand each component:

### Step 1: Configure Snowflake Connection

Ensure your `~/.snowflake/connections.toml` has the connection configured:

```toml
[sfseeurope-mstellwall-aws-us-west3]
account = "your_account"
user = "your_user"
password = "your_password"
warehouse = "COMPUTE_WH"
database = "THEMES_RESEARCH_DEMO"
schema = "RAW_DATA"
```

### Step 2: Understand the Setup Process

The `setup_demo.py` script orchestrates:

1. **Database Setup** - Creates THEMES_RESEARCH_DEMO database with RAW_DATA and ANALYTICS schemas
2. **Data Generation** - Uses Cortex Complete to generate:
   - Structured data (companies, financials, macro indicators)
   - Unstructured content (news, transcripts, reports, memos)
3. **Cortex Objects Creation** - Programmatically creates:
   - 5 Cortex Search services (one per unstructured source)
   - 1 Semantic View for Cortex Analyst
4. **Validation** - Verifies all components are working

All SQL is generated programmatically by `src/cortex_objects_creator.py` - no manual SQL files needed.

### Step 3: Configure the Agent

Follow the detailed instructions in `docs/agent_setup_instructions.md` to:
1. Create the agent in Snowflake Intelligence
2. Configure all 6 tools (1 Analyst + 5 Search)
3. Set planning and response instructions
4. Test with validation queries

## Running the Demo

For the complete demo script with narrative, storytelling, and detailed instructions, see:

### 📖 **[Demo Script: docs/demo_script.md](docs/demo_script.md)**

The demo script includes:
- **Opening context** with "Anna" persona introduction (2 min)
- **4-step progressive investigation** with exact prompts (8 min)
- **Narrative talking points** for each step
- **Expected responses** and key highlights
- **Closing business impact** discussion (2 min)
- **Troubleshooting tips** and objection handling
- **Quick reference card** with copy-paste prompts

### Quick Reference: The 4 Demo Prompts

1. **Broad thematic research**: 
   > "Summarize the impact of rising inflation on Nordic logistics companies. Prefer recent sources."

2. **Quantitative analysis**: 
   > "Compare gross margins over the last 6 quarters for the top 3 Nordic logistics firms. Show a chart."

3. **Management commentary**: 
   > "Quote what management said about pricing power for Nordic Freight Systems."

4. **Cross-source validation**: 
   > "Do recent consultant reports and expert interviews agree with that pricing narrative? Summarize briefly."

## Troubleshooting

### If data generation fails:
- Check Snowflake connection: `SELECT CURRENT_USER()`
- Verify Cortex Complete is enabled: `SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-8b', 'test')`
- Check warehouse is running: `SHOW WAREHOUSES`

### If searches return no results:
- Verify services are created: `SHOW CORTEX SEARCH SERVICES IN SCHEMA ANALYTICS`
- Wait for indexing (up to 10 minutes after creation)
- Test with `SEARCH_PREVIEW` function

### If Agent doesn't work as expected:
- Run validation: `python src/generate_data.py --validate-only`
- Check tool descriptions match exactly
- Verify Nordic Freight Systems exists in data
- Review planning instructions for clarity

## Customization Options

Modify `src/config.py` to adjust:
- Number of companies
- Data volumes
- Time periods
- Language mix
- Company names

## Important Notes

- **Deterministic**: Uses fixed seed to ensure "Nordic Freight Systems" always exists
- **Demo-ready**: All 4 demo prompts guaranteed to work
- **Citations**: Every source has a TITLE column for proper citations
- **Realistic**: Content generated by LLM mimics real financial sources

## Support

For issues or questions about this demo, refer to:
- **Demo execution**: `docs/demo_script.md`
- **Agent setup**: `docs/agent_setup_instructions.md`
- **Technical design**: `demo_research/Snowflake AI Research Tool Demo.md`
- **Configuration rules**: `.cursor/rules/`
