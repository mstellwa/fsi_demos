# Frost Markets Intelligence - Snowflake AI Demo

A comprehensive demonstration of Snowflake AI capabilities for financial markets research, showcasing intelligence augmentation for equity research analysts and market insights professionals.

## 🏔️ Overview

This demo creates a fictional financial markets research firm "Frost Markets Intelligence" to demonstrate:

- **Snowflake Intelligence** with conversational AI agents
- **Cortex Analyst** for semantic data analysis
- **Cortex Search** for unstructured document retrieval  

## 🎯 Demo Scenarios

### Phase 1 (Current)
1. **Global Research & Market Insights - Market Structure Reports**
   - Hyper-personalizing quarterly market structure reports
   - Client engagement analytics and strategic targeting
   - EMIR 3.0 regulatory impact assessment for asset managers

2. **Equity Research Analyst - Earnings Analysis**
   - Accelerating quarterly earnings season analysis
   - Beat/miss analysis and management commentary extraction

3. **Equity Research Analyst - Thematic Research**
   - Discovering investment themes from alternative data
   - Cross-sector trend analysis and company exposure mapping

### Phase 2 (Future)
4. **Global Research - Client Strategy Preparation**

## 🚀 Quick Start

### Prerequisites
- Snowflake account with Cortex features enabled
- Python 3.11+ with pip
- A `connections.toml` file configured (see [Snowflake docs](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session#connect-by-using-the-connections-toml-file))

### Installation

```bash
# Clone/download the demo files
cd markets_ai_demo

# Install Python dependencies
pip install -r requirements.txt

# Configure connection (optional - defaults to 'markets_demo')
# Edit config.py to change SNOWFLAKE_CONNECTION_NAME if needed
```
**Snowflake Connection**:
Configure your connection in `~/.snowflake/connections.toml`:

```toml
[your_connection_name]
account = "your_account_identifier"
user = "your_username"
password = "your_password"  # Or use authenticator for SSO
role = "YOUR_ROLE"  # Role with required permissions
```

### Setup Demo Environment

```bash
# Full setup (using SNOWFLAKE_CONNECTION_NAME inconfig.py )
python setup.py --mode=full

# Or specify connection name
python setup.py --mode=full --connection_name your_connection_name

# Other setup modes:
python setup.py --mode=data-only      # Just generate data
python setup.py --mode=ai-only        # Just create AI components  
python setup.py --mode=scenario-specific --scenario=equity_research_earnings
```

The setup process will:
1. ✅ Create database schemas and warehouse
2. ✅ Generate master event log for data correlations
3. ✅ Generate structured data (companies, prices, clients)
4. ✅ Generate unstructured data using Cortex Complete
5. ✅ Create semantic views for Cortex Analyst
6. ✅ Create Cortex Search services
7. ✅ Validate all components

## 🤖 Agent Configuration

After setup completes, configure agents in Snowsight:

1. Open **Snowsight** → **AI & ML** → **Snowflake Intelligence**
2. Click **Create Agent**
3. Follow detailed instructions in **[📖 Agent Setup Guide](docs/agent_setup_instructions.md)**

## 🎭 Demo Delivery

For complete demo scripts, talking points, and delivery guidance:

👉 **[📋 Complete Demo Script](docs/demo_script.md)**

### Quick Demo Overview

**Scenario 1: Market Structure Reports (15 minutes)**
- Personalized market structure report creation
- Client engagement analytics and targeting
- EMIR 3.0 regulatory impact assessment

**Scenario 2: Earnings Analysis (15 minutes)**
- Accelerated quarterly earnings analysis
- Beat/miss calculations and management commentary
- Professional research note generation

**Scenario 3: Thematic Research (15 minutes)**  
- Emerging theme discovery from alternative data
- Company exposure analysis and investment implications
- Cross-sector trend identification

## 📊 Data Architecture

### Database Structure
```
MARKETS_AI_DEMO/
├── RAW_DATA/           # Source data tables
│   ├── COMPANIES
│   ├── HISTORICAL_STOCK_PRICES  
│   ├── CONSENSUS_ESTIMATES
│   ├── CLIENT_PROFILES
│   ├── CLIENT_TRADING_ACTIVITY
│   ├── CLIENT_ENGAGEMENT
│   ├── CLIENT_DISCUSSIONS
│   ├── SEC_FILINGS_RAW
│   ├── EARNINGS_CALL_TRANSCRIPTS
│   ├── NEWS_ARTICLES
│   └── ...
├── ENRICHED_DATA/      # AI-processed data
│   ├── EARNINGS_ACTUALS
│   └── THEMATIC_INTELLIGENCE
└── ANALYTICS/          # Semantic views & search services
    ├── EARNINGS_ANALYSIS_VIEW
    ├── THEMATIC_RESEARCH_VIEW
    ├── CLIENT_MARKET_IMPACT_VIEW
    ├── EARNINGS_TRANSCRIPTS_SEARCH
    ├── RESEARCH_REPORTS_SEARCH
    └── NEWS_ARTICLES_SEARCH
```

### Key Design Principles
- **Event-Driven Correlations**: Master event log drives realistic relationships between prices, news, and earnings
- **Real Tickers, Synthetic Data**: Uses actual stock symbols (AAPL, MSFT) with generated financial data
- **Modular Scenarios**: Each demo segment is completely self-contained
- **AI-Generated Content**: Unstructured documents created using Cortex Complete for realism

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Data volume
NUM_COMPANIES = 15               # Number of companies to generate
NUM_CLIENTS = 25                 # Number of client profiles
NUM_HISTORICAL_QUARTERS = 8     # Number of quarters to generate (dynamic)
NUM_HISTORICAL_YEARS = 2        # Number of years of data (calculated from quarters)

# AI model
CORTEX_MODEL_NAME = "llama3.1-70b"

# Connection
SNOWFLAKE_CONNECTION_NAME = "sfseeurope-mstellwall-aws-us-west3"

# Warehouses
COMPUTE_WAREHOUSE = "MARKETS_AI_DEMO_COMPUTE_WH"  # For data processing
SEARCH_WAREHOUSE = "MARKETS_AI_DEMO_SEARCH_WH"    # For Cortex Search
```

## 🧪 Testing & Validation

```bash
# Run validation manually
python -c "
from src.utils.snowpark_session import get_snowpark_session
from src.utils.validation import validate_all_components
session = get_snowpark_session()
validate_all_components(session)
session.close()
"

# Check search service indexing status
python -c "
from src.utils.snowpark_session import get_snowpark_session
from src.ai_components.search_services import get_search_service_status
session = get_snowpark_session()
get_search_service_status(session)
session.close()
"
```

## 🔄 Cleanup & Reset

```bash
# Reset entire demo environment
python sql/cleanup.sql

# Or use SQL directly in Snowsight:
DROP DATABASE IF EXISTS MARKETS_AI_DEMO CASCADE;
```

## 📚 Scenario Extensions

### Adding New Companies
1. Add ticker to `TICKER_LIST` in `config.py`
2. Run `python setup.py --mode=data-only`

### Adding New Themes  
1. Add themes to `THEMATIC_TAGS` in `config.py`
2. Update event templates in `src/data_generation/event_log.py`
3. Regenerate data

### Creating Custom Agents
1. Add configuration to `src/ai_components/agents.py`
2. Create corresponding semantic views if needed
3. Test with sample queries

## 🎯 Business Value Demonstrated

- **50-75% reduction** in earnings analysis time
- **Real-time risk assessment** capabilities
- **Cross-sector theme discovery** from unstructured data
- **Hyper-personalized client insights** at scale
- **Unified intelligence** across all data types

## 🛠️ Troubleshooting

### Common Issues

**"Connection failed"**
- Verify `connections.toml` exists and has correct connection name
- Check network connectivity to Snowflake

**"Search service not ready"**  
- Search services need 5-10 minutes to index after creation
- Check status with `get_search_service_status()`

**"No data in semantic view"**
- Ensure data generation completed successfully
- Check table row counts in validation

**"Agent not finding results"**
- Verify semantic views work with manual SQL queries
- Check search services are indexed and returning results

### Getting Help

1. Run validation: `python setup.py --mode=full --skip-validation=false`
2. Check logs for specific error messages
3. Verify each component individually using test functions

## 📋 Demo Checklist

Before presenting:
- [ ] Run full setup successfully (`python setup.py --mode=full`)
- [ ] Validate all components pass tests
- [ ] Configure both agents in Snowsight ([Agent Setup Guide](docs/agent_setup_instructions.md))
- [ ] Test sample queries for each scenario  
- [ ] Verify search services are indexed (check search_service_status)
- [ ] Practice demo script timing ([Demo Script](docs/demo_script.md))
- [ ] Review client-specific talking points

---
