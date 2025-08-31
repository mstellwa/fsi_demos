# Snowdrift Financials - Phase 1: Insurance

Demo-ready Snowflake Intelligence experience for the Insurance division, featuring Property P&C claims processing and Commercial Property underwriting scenarios.

## Quick Start

### Prerequisites
- Python 3.8+
- Snowflake account with appropriate permissions
- Snowflake connection configured in `~/.snowflake/connections.toml`

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Snowflake connection:**
   Set up your connection in `~/.snowflake/connections.toml` following the [official Snowflake documentation](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect#label-python-connection-toml).
   
   Example configuration:
   ```toml
   [default]
   account = "your-account-identifier"
   user = "your-username"
   password = "your-password"
   warehouse = "COMPUTE_WH"
   database = "SNOWDRIFT_FINANCIALS"
   schema = "INSURANCE"
   authenticator = "externalbrowser"  # or other auth method
   ```

3. **Run complete setup:**
   ```bash
   python main.py --step all
   ```
   
   **Or run individual steps:**
   ```bash
   python main.py --step data            # Generate all data (structured + unstructured)
   python main.py --step semantic        # Create semantic views
   python main.py --step search          # Create search services
   ```

   **Using a specific connection:**
   ```bash
   python main.py --connection myconnection
   ```

4. **Validate infrastructure:**
   ```bash
   python validate_agent_readiness.py
   ```

5. **Generate demo package:**
   ```bash
   python demo_validation.py
   ```

This will create:
- `SNOWDRIFT_FINANCIALS` database
- Schemas: `INSURANCE`, `INSURANCE_ANALYTICS`, `CONTROL`
- All required tables with realistic Norwegian insurance data
- ~56,000 total records across all tables
- `INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW` ready for Cortex Analyst

## Project Structure

```
nordic_financial_group_demo/
├── src/
│   ├── setup.py                      # Foundation setup (database, schemas, tables)
│   ├── generate_data.py              # Norwegian insurance structured data generation
│   ├── create_semantic_view.py       # SEMANTIC VIEW creation for Cortex Analyst
│   ├── generate_documents.py         # Unstructured content generation via Cortex Complete
│   ├── create_search_services.py     # Cortex Search services creation and testing
│   └── __init__.py
├── .cursor/rules/                    # Consolidated cursor rules (FRD, TRD, Plan)
├── main.py                           # Main entry point with simplified CLI
├── validate_agent_readiness.py      # Infrastructure validation for agent setup
├── demo_validation.py               # Demo package generation with real data
├── config.yaml                      # Project configuration
├── requirements.txt                  # Python dependencies
├── AGENT_SETUP_GUIDE.md             # Complete agent configuration guide
├── DEMO_PACKAGE.json                # Generated demo scripts and validation queries
└── README.md                        # This file
```

## Implementation Status

### 🎉 **PROJECT COMPLETE** - All Milestones Achieved

- ✅ **Foundation Setup**
  - Database and schema creation (`SNOWDRIFT_FINANCIALS`)
  - CONTROL framework with configuration management
  - All required table structures

- ✅ **Structured Data Generation**
  - Realistic Norwegian insurance data (~56k records)
  - Geographic risk scores with flood risk modeling
  - Business registry (BRREG) simulation
  - Insurance policies with risk-based pricing
  - Claims with realistic patterns and correlations

- ✅ **Semantic View Creation**
  - `INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW` with proper SEMANTIC VIEW syntax
  - TABLES, RELATIONSHIPS, FACTS, DIMENSIONS, METRICS with comments and synonyms
  - Business terminology for natural language queries
  - Comprehensive business metrics ready for Cortex Analyst

- ✅ **Unstructured Content Generation**
  - 150 claims documents (police reports, medical reports, witness statements, etc.)
  - 120 underwriting documents (risk assessments, flood advisories, market analysis)
  - Generated via Cortex Complete with configurable models (claude-4-sonnet → llama3.1-8b)
  - Proper PROMPTS table workflow implementation

- ✅ **Cortex Search Services**
  - CLAIMS_SEARCH_SERVICE and UNDERWRITING_SEARCH_SERVICE
  - Automated creation and validation
  - Document indexing with proper attributes and metadata

- ✅ **Agent Configuration**
  - Complete agent setup guide with Response/Planning instruction split
  - Claims Intake Assistant and Underwriting Co-Pilot ready for Snowsight
  - Infrastructure validation tools (`validate_agent_readiness.py`)
  - Tool binding: Cortex Analyst + Cortex Search

- ✅ **Demo Preparation**
  - Complete demo package with real data scenarios (`DEMO_PACKAGE.json`)
  - End-to-end validation scripts (`demo_validation.py`)
  - Performance-optimized demo flows (10-15 minutes each)
  - Ready-to-use demo scripts with high-value sample claim (CLM-014741: 12.1M NOK)

## Demo Scenarios

### 1. Claims Intake Assistant
**Persona:** Senior Claims Adjuster  
**Goal:** Rapidly understand new claims, extract medical details, detect inconsistencies

**Expected outcomes:**
- Incident summary (3-5 sentences) with citations
- Medical diagnoses/treatments in table format
- Inconsistency flagging across documents
- "How I answered" explanation

### 2. Underwriting Co-Pilot  
**Persona:** Commercial P&C Underwriter  
**Goal:** Enrich applications with internal history, flood risk, adverse media

**Expected outcomes:**
- Prior policy/claims history retrieval
- Flood risk summary (1-10 scale) with rationale
- Adverse environmental/flood media items
- Decision recommendations with citations

## Generated Data

### Structured Data
- **~1,000 geographic locations** with flood risk scores (1-10 scale)
- **~5,000 business registry entries** (synthetic Norwegian BRREG data)
- **~20,000 insurance policies** with risk-based pricing
- **~30,000 insurance claims** with realistic loss patterns
- **Total: ~56,000 records** across all tables

### Data Features
- **Norwegian focus**: Realistic municipalities, postal codes, business names
- **Flood risk modeling**: Coastal cities have higher base risk (Bergen, Stavanger, etc.)
- **Correlation patterns**: Claims frequency correlates with geographic flood risk
- **Deterministic generation**: Reproducible results using configured seeds
- **Realistic pricing**: Premium calculations based on coverage amount and risk factors

### Semantic View Capabilities
- **Business terminology**: Natural language support with comprehensive column comments
- **Risk categorization**: Automatic flood risk categorization (Low/Medium/High)
- **Claims analytics**: Loss ratios, outstanding amounts, claims status breakdowns
- **Golden questions**: 10 validated business questions for testing Cortex Analyst
- **Cross-referencing**: Policies linked with geographic risk and claims history

## Next Steps

After completing Phase 1:
- **Phase 2**: Banking integration (Customer 360, Mortgage Risk, Compliance)
- **Phase 3**: Asset Management (Thematic Research, ESG Monitoring, Due Diligence)

---

*Part of the complete Snowdrift Financials ecosystem demonstrating enterprise Snowflake Intelligence across Insurance, Banking, and Asset Management divisions.*
