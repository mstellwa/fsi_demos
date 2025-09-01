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
│   ├── warehouse_setup.py          # Warehouse creation and management
│   ├── structured_data_generator.py # Companies, financials, macro data
│   ├── unstructured_data_generator.py # Content generation via Cortex Complete
│   ├── data_validator.py           # Validation checks
│   └── cortex_objects_creator.py   # Creates Cortex Search services & Semantic Views
├── docs/
│   ├── agent_setup_instructions.md # Detailed agent configuration
│   └── demo_script.md              # Complete demo execution script
├── demo_research/                  # Design documentation
│   ├── Snowflake AI Research Tool Demo.md # Original design doc
│   └── gpt_review.md               # Design review and refinements
└── .cursor/rules/                  # Cursor AI assistant rules
    ├── agent-and-demo-flow.mdc     # Agent behavior rules
    ├── cortex-search-and-semantic-view.mdc # Search service specs
    ├── data-generation.mdc         # Data generation rules
    ├── demo-prompts.mdc            # Demo script reference
    ├── models-and-refresh.mdc      # Model configuration
    ├── naming-and-branding.mdc     # Naming conventions
    └── overview-and-setup.mdc      # Project overview
```

## Prerequisites

### 1. Snowflake Account Requirements

**Features Required**:
- Cortex Complete enabled (llama3.1-8b model)
- Cortex Search enabled
- Cortex Analyst enabled
- Snowflake Intelligence access
- Claude 4.0 model (for Agent configuration)

**Role Permissions Required**:
The Snowflake role you use must have the following privileges:

```sql
-- Database operations
CREATE DATABASE
USE DATABASE

-- Schema operations  
CREATE SCHEMA
USE SCHEMA

-- Warehouse operations
CREATE WAREHOUSE
USE WAREHOUSE
OPERATE WAREHOUSE

-- Table operations
CREATE TABLE
SELECT, INSERT, UPDATE, DELETE on tables

-- Cortex operations
CREATE CORTEX SEARCH SERVICE
CREATE SEMANTIC VIEW

-- Function access
USAGE on FUNCTION SNOWFLAKE.CORTEX.COMPLETE
```

**Recommended Setup**:
```sql
-- Grant necessary privileges to your role (replace YOUR_ROLE with actual role name)
GRANT CREATE DATABASE ON ACCOUNT TO ROLE YOUR_ROLE;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE YOUR_ROLE;
```

### 2. Local Environment

**Python Requirements**:
- Python 3.8 or higher
- pip package manager

**Snowflake Connection**:
Configure your connection in `~/.snowflake/connections.toml`:

```toml
[your_connection_name]
account = "your_account_identifier"
user = "your_username"
password = "your_password"  # Or use authenticator for SSO
role = "YOUR_ROLE"  # Role with required permissions
warehouse = "COMPUTE_WH"  # Will be created if doesn't exist
database = "THEMES_RESEARCH_DEMO"  # Will be created by setup
schema = "RAW_DATA"  # Will be created by setup
```

### 3. Network Requirements

- Stable internet connection (setup takes 10-15 minutes)
- Access to Snowflake endpoints (no firewall blocking)
- If using corporate network, ensure proxy settings are configured

## Quick Setup (Recommended)

### Step 1: Install Dependencies

```bash
# Clone the repository (if not already done)
git clone <repository_url>
cd investment_demo

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Run Complete Setup

```bash
# Run with default connection (edit config.py to change default)
python setup_demo.py

# Or specify your connection name
python setup_demo.py --connection your_connection_name
```

**What the setup script does**:
1. **Creates warehouses**: 
   - `TRD_COMPUTE_WH` for general compute operations
   - `TRD_CORTEX_SEARCH_WH` for Cortex Search services
2. **Creates database**: `THEMES_RESEARCH_DEMO` with schemas:
   - `RAW_DATA` for source tables
   - `ANALYTICS` for Cortex objects
3. **Generates synthetic data** using Cortex Complete:
   - 12 companies (including Nordic Freight Systems)
   - 18 quarters of financial data
   - 50 news articles (10% in Swedish)
   - 12 expert transcripts
   - 8 consultant reports
   - 32 earnings calls
   - 12 internal memos
4. **Creates Cortex Search services** (5 total, one per source)
5. **Creates Semantic View** for quantitative analysis
6. **Validates** all components are working

**Expected runtime**: 10-15 minutes (depending on Cortex Complete speed)

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

### Common Setup Issues

**"Warehouse COMPUTE_WH is missing" error**:
- The setup script now creates `TRD_COMPUTE_WH` and `TRD_CORTEX_SEARCH_WH` automatically
- If you see this error, ensure your role has `CREATE WAREHOUSE` privilege
- Check existing warehouses: `SHOW WAREHOUSES`

**"Invalid identifier 'SOURCE'" error**:
- This is a Snowflake reserved keyword issue (now fixed in the code)
- The code uses `NEWS_SOURCE` and `DATA_SOURCE` instead
- If you see this, drop and recreate the affected table

**"Quoted identifiers" error in Cortex Search**:
- Drop the existing service first: `DROP CORTEX SEARCH SERVICE IF EXISTS service_name`
- The setup now always drops services before recreating them

**Network timeout errors**:
- The setup is resilient to network issues
- Simply rerun `python setup_demo.py` - it will resume where it left off
- For unstable connections, run in steps:
  ```bash
  python setup_demo.py --skip-objects  # Data only
  python setup_demo.py --validate-only # Then validate
  ```

### Data Generation Issues

**Cortex Complete not working**:
```sql
-- Test Cortex Complete access
SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-8b', 'test');

-- If error, check model availability
SHOW FUNCTIONS LIKE 'COMPLETE' IN SCHEMA SNOWFLAKE.CORTEX;
```

**Missing Nordic Freight Systems**:
- This company is mandatory and created deterministically
- If missing, check `RANDOM_SEED = 42` in `src/config.py`
- Regenerate data: `python setup_demo.py`

### Cortex Search Issues

**Services not returning results**:
```sql
-- Check services exist
SHOW CORTEX SEARCH SERVICES IN SCHEMA ANALYTICS;

-- Wait for indexing (up to 10 minutes)
-- Force refresh if needed
ALTER CORTEX SEARCH SERVICE service_name REFRESH;
```

### Agent Configuration Issues

**Agent not finding the right tools**:
- Tool names must match exactly (use underscores, not hyphens)
- Check `docs/agent_setup_instructions.md` for exact tool configurations
- Verify all 6 tools are configured (1 Analyst + 5 Search)

**Agent not citing sources properly**:
- Every Cortex Search service must have a TITLE column
- Citations format: `[Title] (SourceType, Date)`
- Check that all services have proper TITLE mappings

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
