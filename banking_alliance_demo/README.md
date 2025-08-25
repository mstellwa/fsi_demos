# SnowBank Intelligence Demo

A comprehensive Snowflake Intelligence demonstration for Norwegian banking alliance scenarios, featuring Cortex Analyst, Cortex Search, and synthetic Norwegian industry data.

## Overview

This demo showcases Snowflake Intelligence capabilities across four banking personas:
- **Relationship Manager**: Holistic Client 360° view
- **Risk Analyst**: Dynamic Portfolio Stress Testing  
- **ESG Officer**: Automated Green Bond Reporting
- **Executive Leadership**: Cross-Alliance Strategic Inquiry

## Key Features

- **Norwegian Industry Focus**: Authentic Norwegian company names, regions, and industry sectors
- **Synthetic Data Generation**: 5K customers, 25K loans with 24 months of history
- **Cortex Complete Integration**: AI-generated documents with Norwegian context
- **3 Cortex Search Services**: Policy, Market Intelligence, and Compliance content
- **🆕 Dual Semantic Views**: Separated banking and market data for clean agent architecture
- **Validation Framework**: Automated testing and verification

## Setup Requirements

**For complete setup requirements**, see [Technical Requirements](./.cursor/rukes/technical_requirements.mdc) in the cursor rules.

### Quick Start

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Configure Connection**: Ensure `~/.snowflake/connections.toml` is configured
3. **Run Setup**: `python main.py`

**Note**: All detailed prerequisites, environment setup, and technical constraints are documented in the cursor rules files for comprehensive development guidance.

### Setup Steps

The setup process includes:

1. **Database Schema Creation**
   - Creates `FSI_DEMOS.BANK_DEMO` schema
   - 10 core tables with proper relationships
   - Configuration and run registry tables

2. **Synthetic Data Generation**
   - Norwegian member banks (5 banks across regions)
   - Customers with realistic industry/geographic distribution
   - Loans including green bonds and property valuations
   - Financial records and market data
   - Alliance performance metrics

3. **Document Generation** ⚡ OPTIMIZED
   - Norwegian industry-specific content using Cortex Complete
   - **NEW**: Snowpark dataframe batch processing with `save_as_table()`
   - **Performance**: ~31 documents in ~3 seconds (vs ~8 minutes individually)
   - CRM notes, news articles, policy documents
   - Annual reports and loan documentation
   - Third-party assessments and compliance content

4. **Cortex Search Services**
   - `INTERNAL_POLICY_SEARCH_SVC`: Credit policies and procedures
   - `CLIENT_AND_MARKET_INTEL_SVC`: CRM notes and market news
   - `REPORTING_AND_COMPLIANCE_SVC`: Reports and loan documentation

5. **Dual Semantic View Architecture** 🆕🔄
   - **Banking View**: `SNOWBANK_DEMO_SV` for customer portfolios, loans, financials
   - **Market View**: `MARKET_PEER_ANALYSIS_SV` for peer analysis and stock performance
   - **Clean Separation**: Eliminates multi-path relationship issues
   - **Enhanced Agent Intelligence**: Multiple Cortex Analyst tools per agent
   - **Cortex Analyst optimized** with proper `CREATE SEMANTIC VIEW` syntax

## Usage

### Single Setup Command

```bash
# Complete demo setup (default connection)
python main.py

# Specify custom connection
python main.py --connection your-connection-name
```

**Setup Strategy:**
- **Database**: Uses `IF NOT EXISTS` (preserves existing databases)
- **All Objects**: Uses `CREATE OR REPLACE` (ensures clean state)
- **Data**: Always generates complete dataset with demo companies
- **Validation**: Built-in comprehensive validation

## Agent Configuration Best Practices

### Tool Description Strategy
When configuring agents in Snowsight, use **specific tool descriptions** that provide building blocks without hardcoding solutions:

**✅ Good Tool Description:**
```
"Access to Nordic Banking Alliance semantic view containing customer portfolios, loan exposures, and financial data. Query by customer names, industry sectors (Aquaculture, Maritime, etc.), geographic regions (Helgeland, Vestlandet, etc.), loan types, and exposure amounts."
```

**❌ Poor Tool Description:**
```
"Access to semantic view for customer analysis"
```

**Key Principle**: Provide specific capabilities and example dimensions, but never hardcode scenario solutions or query patterns.

### Demo Scenarios

#### 1. Holistic Client 360° (Aquaculture Focus)
**Persona**: Relationship Manager  
**Tools**: Cortex Analyst + Client & Market Intelligence Search

Sample queries:
- "Provide a 360-degree briefing on 'Helio Salmon AS': total exposure, LTM fees, peer stock performance vs top 3 aquaculture competitors"
- "Scan last 6 months of CRM notes and news for operational risks like algae blooms, ISA, or new regulations"

#### 2. Dynamic Portfolio Stress Testing (Property Market)
**Persona**: Risk Analyst  
**Tools**: Cortex Analyst + Internal Policy Search

Sample queries:
- "Model 5% Helgeland property decline + 75bps rate increase on residential mortgage portfolio"
- "Identify loans breaching 85% LTV and cross-reference policy manual for forbearance options"

#### 3. Automated Green Bond Reporting (Renewable Focus)
**Persona**: ESG Officer  
**Tools**: Cortex Analyst + Reporting & Compliance Search

Sample queries:
- "Generate 2024 Green Bond allocation by category"
- "For top 5 renewable energy loans, extract project descriptions and CO2 targets from loan documents"

#### 4. Cross-Alliance Strategic Inquiry
**Persona**: Executive Leadership  
**Tools**: Cortex Analyst + Reporting & Compliance Search

Sample queries:
- "Rank all member banks by 2024 SMB lending growth"
- "For top 3 performers, summarize their SMB initiatives from annual reports"

## Configuration

Configuration is stored in the `DEMO_CONFIG` table and can be modified:

```python
from src.config import DemoConfig

config = DemoConfig()
config.set_config('CUSTOMER_COUNT', 7500)  # Increase customer count
config.set_config('MODEL_CLASS', 'MEDIUM')  # Change AI model class
```

### Available Configuration Options

| Key | Default | Description |
|-----|---------|-------------|
| CONNECTION_NAME | sfseeurope-mstellwall-aws-us-west3 | Snowflake connection name |
| CUSTOMER_COUNT | 5000 | Number of synthetic customers |
| LOAN_COUNT | 25000 | Number of synthetic loans |
| HISTORY_MONTHS | 24 | Months of historical data |
| MODEL_CLASS | LARGE | Cortex model class for document generation |
| WAREHOUSE_FOR_BUILD | MEDIUM | Warehouse size for data generation |

## Document Generation Technical Details

### Snowpark DataFrame Approach

The demo uses an optimized snowpark dataframe approach for document generation:

1. **Prompt Storage**: All prompts are stored in `DOCUMENT_PROMPTS` table
2. **Batch Processing**: Process all prompts for each model class in a single dataframe operation
3. **Direct Storage**: Use `save_as_table()` directly from the generated dataframe

### Implementation Notes

For detailed technical requirements including `cortex.complete()` constraints, performance optimization patterns, and implementation guidelines, see [Technical Requirements](./.cursor/rukes/technical_requirements.mdc).

## Data Model

### Core Tables
- `MEMBER_BANKS`: 5 Norwegian regional banks
- `CUSTOMERS`: Individual and corporate customers
- `LOANS`: Loan portfolio including green bonds
- `FINANCIALS`: Fee revenue and financial records
- `ALLIANCE_PERFORMANCE`: SMB growth and efficiency metrics
- `MARKET_DATA`: Norwegian/Nordic stock market data

### Document Tables
- `DOCUMENT_PROMPTS`: AI generation prompts
- `DOCUMENTS`: Generated content for search services

### System Tables
- `DEMO_CONFIG`: Configuration key-value pairs
- `RUN_REGISTRY`: Data generation run metadata

## Norwegian Industry Context

### Geographic Regions
- **Helgeland**: Aquaculture concentration
- **Østlandet**: Technology services hub
- **Trøndelag**: Mixed technology and maritime
- **Vestlandet**: Maritime industry focus
- **Nord-Norge**: Oil & gas services

### Industry Sectors
- Aquaculture (salmon farming, sea lice regulations)
- Renewable Energy (offshore wind, CO2 targets)
- Maritime (shipping, offshore services)
- Real Estate Development (BREEAM/LEED certification)
- Technology Services (digital transformation)
- Tourism & Hospitality
- Oil & Gas Services

## Validation

The demo includes comprehensive validation:

```bash
python validate_demo.py --output summary
```

### Validation Categories
- **Data Volumes**: Row counts within ±10% tolerance
- **Data Integrity**: Referential integrity checks
- **Data Distribution**: Geographic and industry realism
- **Green Lending**: 15-25% green bond portfolio
- **Document Corpus**: Answerable phrases for demo queries
- **Search Services**: Service creation and functionality
- **Semantic Model**: View accessibility and data
- **Agent Readiness**: Tool availability verification

## Troubleshooting

### Common Issues

1. **Connection Errors**
   - Verify `connections.toml` credentials
   - Check warehouse and database permissions
   - Ensure Cortex features are enabled

2. **Cortex Complete Failures**
   - Verify model class availability in your region
   - Check warehouse size (MEDIUM minimum recommended)
   - Review error logs for specific issues

3. **Search Service Creation Failures**
   - Ensure sufficient document content exists
   - Verify warehouse permissions for Cortex Search
   - Check for existing services with same names

4. **Validation Failures**
   - Review specific validation output
   - Check data generation logs
   - Verify all setup steps completed

### Log Files
- `snowbank_demo.log`: Complete execution log
- Run registry table: Data generation metadata

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Cortex        │    │   Cortex        │    │   Cortex        │
│   Analyst       │    │   Search        │    │   Complete      │
│                 │    │   Services (3)  │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SnowBank Demo Platform                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│  Semantic Model │   Search Index  │      Document Corpus        │
│  (Analyst Tool) │  (Search Tool)  │   (Generated Content)       │
└─────────────────┴─────────────────┴─────────────────────────────┘
```

## Contributing

When extending the demo:

1. **Adding New Scenarios**: Update document generators and search prompts
2. **New Industries**: Extend Norwegian company naming and geographic logic
3. **Additional Measures**: Update semantic model definitions
4. **New Validations**: Add checks to validation framework

## License

This demo is designed for Snowflake customer demonstrations and training purposes.
