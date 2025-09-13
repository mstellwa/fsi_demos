# SAM Demo - Data Model Documentation (100% Real Assets)

Complete documentation of the data architecture using 14,000+ authentic securities from Snowflake Marketplace OpenFIGI dataset following industry-standard asset management practices.

## Database Architecture

**Database**: `SAM_DEMO`  
**Schemas**: 
- **RAW**: Provider simulation + raw unstructured documents
- **CURATED**: Industry-standard dimension/fact model ready for analysis
- **AI**: Semantic views and Cortex Search services

## Implementation Status (100% Real Assets)

✅ **14,000+ Real Securities**: All from authentic OpenFIGI dataset (no synthetic securities)  
✅ **3,303 Real Issuers**: Corporate hierarchies from real companies  
✅ **Authentic Identifiers**: TICKER + real Bloomberg FIGI identifiers only  
✅ **Transaction-Based Holdings**: 27,000+ holdings using real securities  
✅ **Synthetic Market Data**: 4M+ records with realistic volatility patterns  
✅ **AI Components**: All semantic views and search services operational at scale  

## Enhanced Data Model (Industry Standard)

### Core Dimension Tables (CURATED Schema)
```sql
-- Master security dimension with immutable SecurityID (100% Real)
DIM_SECURITY               -- 14,000 real securities from OpenFIGI dataset
DIM_ISSUER                 -- 3,303 real issuers with corporate hierarchies
DIM_SECURITY_IDENTIFIER_XREF -- Security identifier cross-reference (TICKER, FIGI)
DIM_PORTFOLIO              -- 10 portfolios with enhanced information
DIM_BENCHMARK              -- 3 benchmarks (S&P 500, MSCI ACWI, Nasdaq 100)
```

### Core Fact Tables (CURATED Schema)
```sql
-- Transaction-based model (source of truth)
FACT_TRANSACTION           -- Canonical transaction log with 12 months history
FACT_POSITION_DAILY_ABOR   -- ABOR positions built from transactions
FACT_MARKETDATA_TIMESERIES -- Synthetic market data with realistic volatility patterns

-- Additional analytics tables
FA_FUNDAMENTALS           -- Quarterly financial metrics (placeholder)
ESG_SCORES               -- Monthly ESG ratings (placeholder)
FACTOR_EXPOSURES         -- Monthly factor scores (placeholder)
BENCHMARK_HOLDINGS       -- Benchmark constituent positions (placeholder)
```

### Enhanced Document Integration (CURATED Schema)
```sql
-- Document corpus tables with SecurityID/IssuerID linkage
BROKER_RESEARCH_CORPUS     -- 40 analyst reports with SecurityID linkage
EARNINGS_TRANSCRIPTS_CORPUS -- 35 earnings call summaries with SecurityID linkage
PRESS_RELEASES_CORPUS      -- 35 corporate press releases with SecurityID linkage
```

## Key Architecture Benefits

### Industry-Standard Capabilities
- **Immutable SecurityID**: Corporate action resilience and temporal integrity
- **Transaction Audit Trail**: Complete history for compliance and reconciliation
- **Issuer Hierarchy**: Corporate structure and parent company analysis
- **Enhanced Document Integration**: Stable SecurityID/IssuerID linkage
- **Real Data Integration**: Authentic market data with synthetic fallback

### Enhanced Analytics Support
- **Issuer-Level Risk Analysis**: Total exposure across all securities of an issuer
- **Corporate Action Handling**: Maintain analytical continuity through ticker changes
- **Transaction-Level Analytics**: Complete audit trail for compliance
- **Temporal Consistency**: Proper handling of identifier changes over time

## AI Components (AI Schema)

### Semantic View: `SAM_ANALYST_VIEW`
**Enhanced Capabilities**:
- Portfolio analytics with issuer hierarchy support
- Multi-table relationships (Holdings → Securities → Issuers)
- Enhanced dimensions and metrics for comprehensive analysis
- Direct date column support (no DIM_DATE complexity)

**Key Metrics**:
- `TOTAL_MARKET_VALUE`: Sum of position values in base currency
- `HOLDING_COUNT`: Count of portfolio positions
- `ISSUER_EXPOSURE`: Total exposure to issuer across all securities
- `PORTFOLIO_WEIGHT_PCT`: Portfolio weight as percentage

**Key Dimensions**:
- `PORTFOLIONAME`, `DESCRIPTION`, `PRIMARYTICKER`, `LEGALNAME`, `GICS_SECTOR`

### Enhanced Search Services
- `SAM_BROKER_RESEARCH`: Search analyst reports with SecurityID/IssuerID attributes
- `SAM_EARNINGS_TRANSCRIPTS`: Search earnings summaries with SecurityID/IssuerID attributes
- `SAM_PRESS_RELEASES`: Search corporate announcements with SecurityID/IssuerID attributes

### Real Market Data Integration
**Status**: ✅ Implemented and operational

**Data Source**: `FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.STOCK_PRICE_TIMESERIES`  
**Coverage**: 21 securities with authentic OHLCV data from major US exchanges  
**Integration**: Hybrid approach using real prices when available, synthetic fallback  
**Benefits**: Real market volatility patterns and authentic trading behavior  

## Data Quality Standards (Verified)

### Validation Results
✅ **Portfolio Weights**: Sum to 100% (±0.1% tolerance)  
✅ **Transaction Integrity**: Transaction log balances to ABOR positions  
✅ **Identifier Cross-Reference**: Security identifier relationships validated  
✅ **Price Data**: No negative prices, realistic ranges by asset class  
✅ **Date Consistency**: Business days only, proper date ranges  
✅ **Foreign Key Relationships**: All relationships valid and tested  

### Enhanced Validation Capabilities
✅ **Transaction Balancing**: FACT_TRANSACTION sums to FACT_POSITION_DAILY_ABOR  
✅ **Issuer Hierarchy**: Corporate relationships properly established  
✅ **SecurityID Integrity**: Cross-reference table properly populated  
✅ **Document Linkage**: Stable SecurityID/IssuerID linkage validated  

## Sample Data Highlights

### Enhanced Portfolio Examples
- SAM Global Flagship Multi-Asset: $2.5B AUM with multi-asset holdings
- SAM ESG Leaders Global Equity: $1.8B AUM with ESG-focused positions  
- SAM Global Thematic Growth: $1.5B AUM with technology concentration

### Enhanced Securities Examples
- **Real Tickers**: AAPL, MSFT, NVDA, GOOGL, AMZN, META with proper issuer linkage
- **Immutable SecurityID**: Each security has stable identifier surviving corporate actions
- **Issuer Hierarchies**: Corporate structure relationships established
- **Global Coverage**: US (55%), Europe (30%), APAC/EM (15%) with authentic issuers

### Enhanced Content Quality
- **SecurityID Integration**: All documents linked via stable identifiers
- **Issuer-Level Documents**: NGO reports and engagement notes apply to issuer level
- **Professional UK English**: Consistent throughout all generated content
- **Realistic Financial Context**: Sector-specific content with authentic metrics

## Migration Benefits Achieved

### From Simple Model To Industry Standard
- **Before**: Flat security table with TICKER primary key
- **After**: Immutable SecurityID with full symbology spine
- **Before**: Direct position snapshots
- **After**: Transaction-based holdings with audit trail
- **Before**: String-based document linkage
- **After**: Stable SecurityID/IssuerID document relationships

### Enhanced Capabilities Enabled
- **Issuer-level analysis**: "What's our total exposure to Apple across all securities?"
- **Corporate hierarchy queries**: "Show me all holdings in technology conglomerates"
- **Enhanced document search**: "Find ESG reports for all our technology holdings"
- **Transaction analytics**: Complete audit trail for compliance and analysis

The SAM demo now implements a professional, industry-standard asset management data model that provides enhanced analytics capabilities while maintaining all existing functionality.