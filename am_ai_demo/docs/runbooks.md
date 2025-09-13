# SAM Demo - Runbooks and Procedures

Setup procedures, validation checks, and operational guidance for the SAM demo.

## Prerequisites

### Required Setup
1. **Snowflake Account**: With Cortex features enabled and cross-region access
2. **Connection Configuration**: `~/.snowflake/connections.toml` properly configured
3. **Python Environment**: `snowflake-snowpark-python` installed

### Connection Configuration
Ensure your `~/.snowflake/connections.toml` contains a valid connection:

```toml
[connections.sfseeurope-mstellwall-aws-us-west3]
account = "your-account"
user = "your-username"
password = "your-password"  
warehouse = "your-warehouse"
database = "SAM_DEMO"
schema = "CURATED"
```

## Build Procedures

### Quick Start (Portfolio Copilot Demo)
```bash
# Install dependencies
pip install snowflake-snowpark-python

# Build complete demo environment
python python/main.py --scenarios portfolio_copilot

# Build with test mode for faster development
python python/main.py --test-mode

# Extract real market data (optional, requires Marketplace access)
python python/main.py --extract-real-market-data

# Expected output: ✅ All components created successfully
```

### Build Validation
```sql
-- 1. Verify semantic view
DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_ANALYST_VIEW;

-- 2. Test semantic view functionality  
SELECT * FROM SEMANTIC_VIEW(
    SAM_DEMO.AI.SAM_ANALYST_VIEW
    METRICS TOTAL_MARKET_VALUE
    DIMENSIONS PORTFOLIONAME
) LIMIT 5;

-- 3. Test search services
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'SAM_DEMO.AI.SAM_BROKER_RESEARCH',
    '{"query": "technology investment", "limit": 2}'
);

-- 4. Verify data volumes
SELECT 'ABOR Holdings' as table_name, COUNT(*) as record_count FROM SAM_DEMO.CURATED.FACT_POSITION_DAILY_ABOR
UNION ALL
SELECT 'Broker Research', COUNT(*) FROM SAM_DEMO.CURATED.BROKER_RESEARCH_CORPUS
UNION ALL  
SELECT 'Securities', COUNT(*) FROM SAM_DEMO.CURATED.DIM_SECURITY
UNION ALL
SELECT 'Market Data', COUNT(*) FROM SAM_DEMO.CURATED.FACT_MARKETDATA_TIMESERIES
UNION ALL
SELECT 'Transactions', COUNT(*) FROM SAM_DEMO.CURATED.FACT_TRANSACTION;

-- 5. Check real market data integration (if enabled)
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT s.Ticker) as total_securities
FROM SAM_DEMO.CURATED.FACT_MARKETDATA_TIMESERIES m
JOIN SAM_DEMO.CURATED.DIM_SECURITY s ON m.SecurityID = s.SecurityID;
```

### Partial Builds
```bash
# Build only data layer (skip AI components)
python python/main.py --scenarios portfolio_copilot --scope data

# Build only semantic views
python python/main.py --scenarios portfolio_copilot --scope semantic

# Build only search services  
python python/main.py --scenarios portfolio_copilot --scope search

# Build multiple scenarios
python python/main.py --scenarios portfolio_copilot,research_copilot
```

## Agent Configuration

### Step 1: Access Snowflake Intelligence
1. Log into Snowsight
2. Navigate to Snowflake Intelligence
3. Create new agent: `portfolio_copilot`

### Step 2: Configure Tools
Follow the exact configuration in `docs/agents_setup.md`:
- **quantitative_analyzer**: Cortex Analyst with `SAM_DEMO.AI.SAM_ANALYST_VIEW`
- **search_broker_research**: Cortex Search with `SAM_DEMO.AI.SAM_BROKER_RESEARCH`
- **search_earnings_transcripts**: Cortex Search with `SAM_DEMO.AI.SAM_EARNINGS_TRANSCRIPTS`
- **search_press_releases**: Cortex Search with `SAM_DEMO.AI.SAM_PRESS_RELEASES`

### Step 3: Add Instructions
Copy the Planning and Response instructions from `docs/agents_setup.md`

## Demo Readiness Checklist

### Technical Validation
- [ ] ✅ Database `SAM_DEMO` exists with RAW, CURATED, AI schemas
- [ ] ✅ Enhanced foundation tables created (DIM_SECURITY, FACT_TRANSACTION, FACT_POSITION_DAILY_ABOR)
- [ ] ✅ Document corpus tables created with SecurityID/IssuerID linkage
- [ ] ✅ Semantic view `SAM_ANALYST_VIEW` created with issuer hierarchy support
- [ ] ✅ Enhanced search services created with SecurityID/IssuerID attributes
- [ ] ✅ Agent `portfolio_copilot` configured in Snowflake Intelligence

### Business Validation
- [ ] Portfolio data shows realistic diversification and weights
- [ ] Generated documents contain authentic financial content
- [ ] Search services return relevant results for investment queries
- [ ] Agent responds appropriately to test queries from `docs/demo_scenarios.md`

## Troubleshooting Guide

### Common Issues and Solutions

**Build Fails with Connection Error**:
- Verify `~/.snowflake/connections.toml` is configured
- Check warehouse has sufficient compute resources
- Ensure Cortex features are enabled in your account

**Semantic View Creation Fails**:
- Check for existing views: `DROP VIEW IF EXISTS SAM_DEMO.AI.SAM_ANALYST_VIEW`
- Verify all referenced tables exist in CURATED schema
- Use exact syntax from cursor rules (tabs, not spaces)

**Search Services Fail**:
- Verify WAREHOUSE parameter matches your connection
- Check ATTRIBUTES match SELECT column aliases exactly
- Ensure corpus tables have DOCUMENT_TEXT column

**Agent Not Responding**:
- Verify agent has access to semantic view and search services
- Check tool configurations match exact service names
- Test individual components before agent configuration

### Performance Notes
- **Build Time**: ~10-15 minutes for complete portfolio_copilot scenario
- **Data Volume**: 6.5M structured records + 2,800 generated documents
- **Warehouse**: Uses warehouse from connection profile (recommend Medium or larger)

### Verified Environment
- ✅ **Snowflake Version**: 9.25.1
- ✅ **Region**: AWS_US_WEST_2  
- ✅ **Cortex Complete**: Working with `llama3.1-70b`
- ✅ **Semantic Views**: Working with correct syntax
- ✅ **Cortex Search**: Working with AS SELECT pattern
