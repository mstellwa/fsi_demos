# Snowcrest Asset Management (SAM) AI Demo

A comprehensive demonstration of Snowflake Intelligence capabilities for asset management customers, featuring realistic multi-asset portfolios, AI-powered analytics, and intelligent agents.

## Quick Start

### Prerequisites
1. **Snowflake Account**: With Cortex features enabled and cross-region access
2. **Python Environment**: Python 3.10+ with snowflake-snowpark-python
3. **Connection Configuration**: `~/.snowflake/connections.toml` properly configured
4. **Snowflake Intelligence Enabled**: https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence
5. **Optional**: Access to "Data Financials & Economics: Enterprise" dataset if going to use real data for assets and market prices.

### Install Dependencies
```bash
pip install snowflake-snowpark-python
```

### Configure Snowflake Connection
Ensure your `~/.snowflake/connections.toml` contains a valid connection profile:

```toml
[connections.sfseeurope-mstellwall-aws-us-west3]
account = "your-account"
user = "your-username" 
password = "your-password"
warehouse = "your-warehouse"
database = "SAM_DEMO"
schema = "CURATED"
```

### Build Demo Environment
```bash
# Build everything (all scenarios)
python python/main.py

# Test mode: Build all scenarios with 10% data for faster development testing
python python/main.py --test-mode

# Build specific scenarios only
python python/main.py --scenarios portfolio_copilot,esg_guardian

# Build only data layer
python python/main.py --scope data

# Extract real assets from Snowflake Marketplace (requires Marketplace access)
./data

# Use custom connection
python python/main.py --connection-name my_demo_connection
```

### Using Real Asset Data (Optional Enhancement)

The demo can use authentic financial instrument data from Snowflake Marketplace instead of generated tickers. This provides enhanced realism and authenticity for customer demonstrations.

**Benefits of Real Data**:
- ✅ **Authentic Tickers**: Global securities (AAPL, ASML, TSM, NESTLE, etc.)
- ✅ **Real Market Data**: Authentic OHLCV prices and volumes from major US exchanges
- ✅ **Geographic Distribution**: Proper coverage across USA/EU/APAC markets
- ✅ **Market Behavior**: Real volatility patterns and trading characteristics
- ✅ **Enhanced Credibility**: Customers see genuine market movements in portfolio performance
- ✅ **Competitive Advantage**: Most demos use purely synthetic data

**Requirements for Real Assets**:
- Snowflake Marketplace subscription to "Public Data Financials & Economics: Enterprise" dataset
- Access to `FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN` database
- Sufficient warehouse compute for OpenFIGI data extraction

**Step 1: Extract Real Assets** (requires Marketplace access)
```bash
python python/main.py --extract-real-assets
```

**Step 2: Extract Real Market Data** (optional, requires Marketplace access)
```bash
python python/main.py --extract-real-market-data
```

**Step 3: Enable Real Data Usage** (Already Enabled)
Both `USE_REAL_ASSETS_CSV = True` and `USE_REAL_MARKET_DATA = True` are now defaults in `python/config.py`

**Step 4: Build Demo**
```bash
python python/main.py --scenarios portfolio_copilot
```

## Demo Overview

### Company Profile: Snowcrest Asset Management (SAM)
- **Multi-asset investment firm** with 10 portfolios ($12.5B total AUM)
- **Enhanced Architecture**: Industry-standard data model with SecurityID and issuer hierarchies
- **Specializes in**: Thematic growth, ESG leadership, quantitative strategies
- **Geographic focus**: Global with emphasis on US (55%), Europe (30%), APAC/EM (15%)
- **Asset classes**: Equities (70%), Corporate Bonds (20%), ETFs (10%)

### Current Demo Status

✅ **Enhanced Implementation**: Industry-standard data model with transaction-based holdings

| Scenario | Agent | Status | Key Capabilities |
|----------|-------|--------|------------------|
| **Portfolio Insights** ✅ | `portfolio_copilot` | **READY** | Holdings analysis, issuer-level exposure, benchmark comparison |
| **Earnings Intelligence** ✅ | `research_copilot` | **READY** | Earnings analysis, transcript summaries, competitive insights |
| **Thematic Analysis** ✅ | `thematic_macro_advisor` | **READY** | Theme discovery, exposure analysis, macro scenario modeling |
| **ESG Monitoring** ✅ | `esg_guardian` | **READY** | Controversy scanning, policy compliance, engagement tracking |
| **Compliance** ✅ | `compliance_advisor` | **READY** | Mandate monitoring, breach detection, policy citation |
| **Client Reporting** ✅ | `sales_advisor` | **READY** | Performance reports, template formatting, philosophy integration |
| **Factor Analysis** ✅ | `quant_analyst` | **READY** | Factor screening, backtesting, performance attribution |

## Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Connection** | `sfseeurope-mstellwall-aws-us-west3` | Default Snowflake connection |
| **Model** | `llama3.1-70b` | LLM for content generation |
| **History** | 5 years | Historical data range |
| **Securities** | 500 total (test mode) | Enhanced SecurityID model with issuer hierarchies |
| **Language** | UK English | All generated content and agent responses |
| **Currency** | USD (fully hedged) | Base currency for all analytics |
| **Returns** | Monthly | Performance calculation frequency |
| **Providers** | NSD/PLM (50/50) | Simulated data provider mix |
| **Real Assets** | ✅ Enabled | Uses authentic tickers from Snowflake Marketplace |
| **Real Market Data** | ✅ Enabled | Uses authentic OHLCV prices from US exchanges |
| **Test Mode** | Available | 10% data volumes for faster development |
| **Warehouses** | Dedicated | Separate warehouses for execution and Cortex Search |

## Project Structure

```
/
├── .cursor/rules/              # Cursor AI development rules
├── docs/                       # Documentation (auto-generated)
│   ├── agents_setup.md         # Agent configuration instructions
│   ├── demo_scenarios.md       # Complete demo scripts
│   ├── data_model.md          # Schema and data documentation
│   └── runbooks.md            # Setup and execution procedures
├── python/                     # Python implementation
│   ├── config.py              # Configuration constants
│   ├── main.py                # CLI orchestrator
│   ├── generate_structured.py # Structured data generation
│   ├── generate_unstructured.py # Unstructured content generation
│   ├── build_ai.py            # AI components (semantic views, search)
│   └── extract_real_assets.py # Real asset data extraction
├── data/                       # Real asset data storage
│   └── real_assets.csv        # Authentic securities from Marketplace
└── README.md                  # This file
```

## Enhanced Data Architecture

### Database: `SAM_DEMO`
- **RAW Schema**: External provider simulation + raw documents
- **CURATED Schema**: Industry-standard dimension/fact model
- **AI Schema**: Enhanced semantic views and Cortex Search services

### Enhanced Data Model Features
- **Immutable SecurityID**: Corporate action resilience and temporal integrity
- **Transaction-Based Holdings**: ABOR positions built from canonical transaction log
- **Issuer Hierarchies**: Corporate structure and parent company analysis
- **Enhanced Document Integration**: Stable SecurityID/IssuerID linkage
- **Real Data Integration**: Authentic market data with synthetic fallback

### Data Providers (Simulated)
- **NorthStar Data (NSD)**: ESG ratings, equity factors, estimates, MSCI ACWI benchmark
- **PolarMetrics (PLM)**: Market prices, fundamentals, credit ratings, yield curves, S&P 500/Nasdaq benchmarks
- **Internal SAM**: Portfolio holdings, policies, templates, engagement notes

## Key Features

### 🎯 **Realistic Data**
- **Authentic Tickers**: 6,163 real securities from Snowflake Marketplace (AAPL, NVDA, ASML, TSM, NESTLE)
- **Real Market Data**: 10,000+ authentic OHLCV records from major US exchanges (NASDAQ, NYSE, ARCA)
- **Hybrid Pricing**: Real market movements for 21 securities, synthetic fallback for complete coverage
- **Correlated Relationships**: P/E ratios align with growth, sector-specific factor scores
- **Temporal Consistency**: Earnings dates align with transcripts, quarterly reporting cycles
- **Complex Analytics**: Bond mathematics, ESG ratings, factor exposures, compliance monitoring
- **Global Coverage**: Proper geographic distribution (55% US, 30% EU, 15% APAC/EM)

### 🤖 **Enhanced AI Components**
- **Semantic View**: Multi-table analytics with issuer hierarchy support
- **Search Services**: Enhanced with SecurityID/IssuerID attributes for stable document linkage
- **Intelligent Agents**: 7 role-specific agents with enhanced capabilities
- **Dedicated Warehouses**: `SAM_DEMO_EXECUTION_WH` and `SAM_DEMO_CORTEX_WH`
- **Industry-Standard Architecture**: Professional asset management data model

### 📊 **Investment Themes**
- **On-Device AI**: Semiconductor and software companies
- **Renewable Energy Transition**: Clean energy and infrastructure
- **Cybersecurity**: Security software and services

### ⚖️ **Compliance Monitoring**
- Concentration limits (7% max, 6.5% warning)
- Fixed income guardrails (75% IG minimum, duration tolerance)
- ESG requirements (BBB minimum rating, controversy exclusions)

## Troubleshooting

### Common Issues
- **Connection fails**: Verify `~/.snowflake/connections.toml` configuration
- **Module not found**: Ensure snowflake-snowpark-python is installed  
- **Permission denied**: Check Snowflake account has Cortex features enabled
- **Build fails**: Check warehouse has sufficient compute resources
- **Enhanced data model**: Uses SecurityID-based architecture with transaction audit trails
- **Agent terminology**: Agents now understand both 'fund' and 'portfolio' queries
- **Real assets missing**: Run `--extract-real-assets` to get authentic tickers

### Support
- Review cursor rules in `.cursor/rules/` for detailed specifications
- Check generated documentation in `docs/` for setup instructions
- Validate AI components with test queries in `docs/runbooks.md`

## Next Steps After Build

1. **Configure Agents**: Follow standardized format in `docs/agents_setup.md`
2. **Test Scenarios**: Use 'portfolio' terminology from `docs/demo_scenarios.md`  
3. **Validate Data**: Execute quality checks from `docs/runbooks.md`
4. **Demo Preparation**: All 7 scenarios ready with enhanced issuer-level capabilities

### Quick Agent Test
```
"What are my top 10 holdings by market value in the SAM Global Thematic Growth portfolio?"
```
**Expected**: Clean list with enhanced issuer information and stable SecurityID linkage

---

**Built with Snowflake Intelligence** | **Powered by Cortex** | **UK English Throughout**
