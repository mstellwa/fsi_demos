"""
Snowcrest Asset Management (SAM) Demo Configuration
All configuration constants for the SAM AI demo using CAPS naming convention.
"""

# Connection and execution
DEFAULT_CONNECTION_NAME = 'sfseeurope-mstellwall-aws-us-west3'
RNG_SEED = 42

# Warehouse configuration
EXECUTION_WAREHOUSE = 'SAM_DEMO_EXECUTION_WH'  # For data generation and code execution
CORTEX_SEARCH_WAREHOUSE = 'SAM_DEMO_CORTEX_WH'  # For Cortex Search services
WAREHOUSE_SIZE = 'MEDIUM'  # Warehouse size for both

# Cortex Search configuration
CORTEX_SEARCH_TARGET_LAG = '5 minutes'  # How often search indexes refresh (use shorter for demos)

# Data generation parameters
YEARS_OF_HISTORY = 5
MODEL_NAME = 'llama3.1-70b'  # Configurable, single model for all generation

# Enhanced data model settings
USE_TRANSACTION_BASED_MODEL = True
GENERATE_CORPORATE_HIERARCHIES = True
ISSUER_HIERARCHY_DEPTH = 2  # Keep simple for demo

# Transaction generation settings
SYNTHETIC_TRANSACTION_MONTHS = 12  # Generate 12 months of history
TRANSACTION_TYPES = ['BUY', 'SELL', 'DIVIDEND', 'CORPORATE_ACTION']
AVERAGE_MONTHLY_TRANSACTIONS_PER_SECURITY = 2.5

# Provider configuration
PROVIDERS = ['NSD', 'PLM']  # NorthStar Data, PolarMetrics
PROVIDER_MIX = {'NSD': 0.5, 'PLM': 0.5}

# Data volumes (real assets only) - based on available real data capacity
SECURITIES_COUNT = {'equities': 10000, 'bonds': 3000, 'etfs': 1000}  # All real assets from OpenFIGI dataset

# Test mode configuration (10% of full data for faster development testing)
TEST_MODE_MULTIPLIER = 0.1
TEST_SECURITIES_COUNT = {
    'equities': int(SECURITIES_COUNT['equities'] * TEST_MODE_MULTIPLIER),    # 1000
    'bonds': int(SECURITIES_COUNT['bonds'] * TEST_MODE_MULTIPLIER),          # 300  
    'etfs': int(SECURITIES_COUNT['etfs'] * TEST_MODE_MULTIPLIER)             # 100
}
UNSTRUCTURED_COUNTS = {
    'broker_research': 3,      # Per equity
    'earnings_transcripts': 2, # Per equity (summary + Q&A)
    'press_releases': 1,       # Per equity
    'ngo_reports': 2,         # Per issuer
    'engagement_notes': 1,     # Per issuer
    'policy_docs': 8,         # Fixed set
    'sales_templates': 2,     # Fixed set
    'philosophy_docs': 3      # Fixed set
}

# Test mode unstructured counts (reduced for faster testing)
TEST_UNSTRUCTURED_COUNTS = {
    'broker_research': 1,      # 1 per equity (vs 3)
    'earnings_transcripts': 1, # 1 per equity (vs 2)
    'press_releases': 1,       # 1 per equity (same)
    'ngo_reports': 1,         # 1 per issuer (vs 2)
    'engagement_notes': 1,     # 1 per issuer (same)
    'policy_docs': 3,         # 3 docs (vs 8)
    'sales_templates': 1,     # 1 template (vs 2)
    'philosophy_docs': 1      # 1 doc (vs 3)
}

# Portfolio configuration
PORTFOLIO_LINEUP = [
    {'name': 'SAM Global Flagship Multi-Asset', 'benchmark': 'MSCI ACWI', 'aum_usd': 2.5e9},
    {'name': 'SAM ESG Leaders Global Equity', 'benchmark': 'MSCI ACWI', 'aum_usd': 1.8e9},
    {'name': 'SAM Global Thematic Growth', 'benchmark': 'Nasdaq 100', 'aum_usd': 1.5e9},
    {'name': 'SAM US Core Equity', 'benchmark': 'S&P 500', 'aum_usd': 1.2e9},
    {'name': 'SAM Renewable & Climate Solutions', 'benchmark': 'Nasdaq 100', 'aum_usd': 1.0e9},
    {'name': 'SAM AI & Digital Innovation', 'benchmark': 'Nasdaq 100', 'aum_usd': 0.9e9},
    {'name': 'SAM Global Balanced 60/40', 'benchmark': 'MSCI ACWI', 'aum_usd': 0.8e9},
    {'name': 'SAM Tech Disruptors Equity', 'benchmark': 'Nasdaq 100', 'aum_usd': 0.7e9},
    {'name': 'SAM US Value Equity', 'benchmark': 'S&P 500', 'aum_usd': 0.6e9},
    {'name': 'SAM Multi-Asset Income', 'benchmark': 'S&P 500', 'aum_usd': 0.5e9}
]

# Thematic focuses
THEMES = ['On-Device AI', 'Renewable Energy Transition', 'Cybersecurity']

# Data distribution
DATA_DISTRIBUTION = {
    'regions': {'US': 0.55, 'Europe': 0.30, 'APAC_EM': 0.15},
    'asset_classes': {'equities': 0.70, 'bonds': 0.20, 'etfs': 0.10},
    'bond_ratings': {'IG': 0.75, 'HY': 0.25},
    'bond_maturity': {'1-3y': 0.25, '3-7y': 0.45, '7-12y': 0.25, '12y+': 0.05}
}

# Compliance rules (configurable with defaults)
COMPLIANCE_RULES = {
    'concentration': {
        'max_single_issuer': 0.07,     # 7%
        'warning_threshold': 0.065     # 6.5%
    },
    'fi_guardrails': {
        'min_investment_grade': 0.75,  # 75%
        'max_ccc_below': 0.05,         # 5%
        'duration_tolerance': 1.0      # ±1.0 years vs benchmark
    },
    'esg_rules': {
        'min_overall_rating': 'BBB',
        'exclude_high_controversy': True,
        'applicable_portfolios': ['SAM ESG Leaders Global Equity', 'SAM Renewable & Climate Solutions']
    }
}

# ESG Controversy Keywords (globally defined)
ESG_CONTROVERSY_KEYWORDS = {
    'environmental': {
        'high': ['toxic spill', 'environmental disaster', 'illegal dumping', 'major pollution'],
        'medium': ['environmental violation', 'emissions breach', 'waste management'],
        'low': ['environmental concern', 'sustainability question']
    },
    'social': {
        'high': ['forced labor', 'child labor', 'human rights violation', 'workplace fatality'],
        'medium': ['labor dispute', 'workplace injury', 'discrimination allegation'],
        'low': ['employee concern', 'workplace issue']
    },
    'governance': {
        'high': ['fraud investigation', 'criminal charges', 'regulatory sanction'],
        'medium': ['accounting irregularity', 'governance breach', 'compliance violation'],
        'low': ['governance concern', 'board dispute']
    }
}

# Benchmark configuration
BENCHMARKS = [
    {'id': 'SP500', 'name': 'S&P 500', 'currency': 'USD', 'provider': 'PLM'},
    {'id': 'MSCI_ACWI', 'name': 'MSCI ACWI', 'currency': 'USD', 'provider': 'NSD'},
    {'id': 'NASDAQ100', 'name': 'Nasdaq 100', 'currency': 'USD', 'provider': 'PLM'}
]

# Factor definitions
EQUITY_FACTORS = ['Value', 'Quality', 'Momentum', 'Size', 'Low_Volatility', 'Growth']
FI_FACTORS = ['Duration', 'Credit_Spread', 'Carry']

# Currency configuration
BASE_CURRENCY = 'USD'
SUPPORTED_CURRENCIES = ['USD', 'EUR', 'GBP']
FX_HEDGING = 'FULLY_HEDGED'  # All returns fully hedged to USD

# Trading calendar
TRADING_CALENDAR = 'UTC_BUSINESS_DAYS'  # Mon-Fri UTC
RETURNS_FREQUENCY = 'MONTHLY'  # Monthly returns for 5-year comparisons

# Language and locale
CONTENT_LANGUAGE = 'en'  # UK English for all generated content
CONTENT_LOCALE = 'UK'

# Database and schema names
DATABASE_NAME = 'SAM_DEMO'
SCHEMAS = {
    'RAW': 'RAW',
    'CURATED': 'CURATED', 
    'AI': 'AI'
}

# Get the directory where this config.py file is located
import os
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root (parent of python/ directory)
PROJECT_ROOT = os.path.dirname(CONFIG_DIR)

# Real asset data extraction settings
EXTRACT_REAL_ASSETS = False  # Set to True to extract real assets from Snowflake Marketplace
REAL_ASSETS_CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'real_assets.csv')  # Always in project/data/
USE_REAL_ASSETS_CSV = True  # Set to True to use existing CSV instead of generating fake data

# Real market data settings
USE_REAL_MARKET_DATA = True  # Use real OHLCV data when available
REAL_MARKET_DATA_CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'real_market_data.csv')  # Always in project/data/
EXTRACT_REAL_MARKET_DATA = True  # Set to True to extract from Marketplace

# Enhanced real asset to issuer mapping
REAL_ASSET_ISSUER_MAPPING = {
    'AAPL': {'legal_name': 'Apple Inc.', 'country': 'US', 'sector': 'Information Technology'},
    'MSFT': {'legal_name': 'Microsoft Corporation', 'country': 'US', 'sector': 'Information Technology'},
    'NVDA': {'legal_name': 'NVIDIA Corporation', 'country': 'US', 'sector': 'Information Technology'},
    'GOOGL': {'legal_name': 'Alphabet Inc.', 'country': 'US', 'sector': 'Communication Services'},
    'AMZN': {'legal_name': 'Amazon.com Inc.', 'country': 'US', 'sector': 'Consumer Discretionary'},
    'META': {'legal_name': 'Meta Platforms Inc.', 'country': 'US', 'sector': 'Communication Services'},
    'TSLA': {'legal_name': 'Tesla Inc.', 'country': 'US', 'sector': 'Consumer Discretionary'},
    'ASML': {'legal_name': 'ASML Holding N.V.', 'country': 'NL', 'sector': 'Information Technology'},
    'SAP': {'legal_name': 'SAP SE', 'country': 'DE', 'sector': 'Information Technology'},
    'TSM': {'legal_name': 'Taiwan Semiconductor Manufacturing Company Limited', 'country': 'TW', 'sector': 'Information Technology'},
    'NESTLE': {'legal_name': 'Nestlé S.A.', 'country': 'CH', 'sector': 'Consumer Staples'}
}

# Market data extraction settings
MARKET_DATA_YEARS_HISTORY = 5  # Years of historical data to extract
MARKET_DATA_EXCHANGES = [  # Target exchanges for data extraction
    'NASDAQ', 'NEW YORK STOCK EXCHANGE', 'NYSE ARCA', 'NYSE MKT LLC', 'BATS Z-EXCHANGE'
]

# Marketplace data source (requires subscription)
MARKETPLACE_DATABASE = 'FINANCIALS_ECONOMICS_ENTERPRISE'
OPENFIGI_SCHEMA = 'CYBERSYN'

# Available scenarios
AVAILABLE_SCENARIOS = [
    'portfolio_copilot',
    'research_copilot', 
    'thematic_macro_advisor',
    'esg_guardian',
    'sales_advisor',
    'quant_analyst',
    'compliance_advisor'
]

# Scenario-specific data requirements
SCENARIO_DATA_REQUIREMENTS = {
    'portfolio_copilot': ['broker_research', 'earnings_transcripts', 'press_releases'],
    'research_copilot': ['broker_research', 'earnings_transcripts'],
    'thematic_macro_advisor': ['broker_research', 'press_releases'],
    'esg_guardian': ['ngo_reports', 'engagement_notes', 'policy_docs'],
    'sales_advisor': ['sales_templates', 'philosophy_docs', 'policy_docs'],
    'quant_analyst': ['broker_research', 'earnings_transcripts'],
    'compliance_advisor': ['policy_docs', 'engagement_notes']
}

# Document type specifications
DOCUMENT_TYPES = {
    'broker_research': {
        'table_name': 'BROKER_RESEARCH_RAW',
        'corpus_name': 'BROKER_RESEARCH_CORPUS',
        'search_service': 'SAM_BROKER_RESEARCH',
        'word_count_range': (700, 1200),
        'applies_to': 'securities',              # Changed from 'equities'
        'linkage_level': 'security'              # New: security-level linkage
    },
    'earnings_transcripts': {
        'table_name': 'EARNINGS_TRANSCRIPTS_RAW', 
        'corpus_name': 'EARNINGS_TRANSCRIPTS_CORPUS',
        'search_service': 'SAM_EARNINGS_TRANSCRIPTS',
        'word_count_range': (6000, 10000),  # Full transcripts
        'applies_to': 'securities',
        'linkage_level': 'security'
    },
    'press_releases': {
        'table_name': 'PRESS_RELEASES_RAW',
        'corpus_name': 'PRESS_RELEASES_CORPUS', 
        'search_service': 'SAM_PRESS_RELEASES',
        'word_count_range': (250, 400),
        'applies_to': 'securities',
        'linkage_level': 'security'
    },
    'ngo_reports': {
        'table_name': 'NGO_REPORTS_RAW',
        'corpus_name': 'NGO_REPORTS_CORPUS',
        'search_service': 'SAM_NGO_REPORTS', 
        'word_count_range': (400, 800),
        'applies_to': 'issuers',                 # Issuer-level documents
        'linkage_level': 'issuer'                # New: issuer-level linkage
    },
    'engagement_notes': {
        'table_name': 'ENGAGEMENT_NOTES_RAW',
        'corpus_name': 'ENGAGEMENT_NOTES_CORPUS',
        'search_service': 'SAM_ENGAGEMENT_NOTES',
        'word_count_range': (150, 300),
        'applies_to': 'issuers',
        'linkage_level': 'issuer'
    },
    'policy_docs': {
        'table_name': 'POLICY_DOCS_RAW',
        'corpus_name': 'POLICY_DOCS_CORPUS',
        'search_service': 'SAM_POLICY_DOCS',
        'word_count_range': (800, 1500),
        'applies_to': None,                      # Global documents
        'linkage_level': 'global'                # New: no linkage
    },
    'sales_templates': {
        'table_name': 'SALES_TEMPLATES_RAW',
        'corpus_name': 'SALES_TEMPLATES_CORPUS',
        'search_service': 'SAM_SALES_TEMPLATES',
        'word_count_range': (800, 1500),
        'applies_to': None,
        'linkage_level': 'global'
    },
    'philosophy_docs': {
        'table_name': 'PHILOSOPHY_DOCS_RAW',
        'corpus_name': 'PHILOSOPHY_DOCS_CORPUS',
        'search_service': 'SAM_PHILOSOPHY_DOCS',
        'word_count_range': (800, 1500),
        'applies_to': None,
        'linkage_level': 'global'
    }
}

# Market data configuration (synthetic only)
USE_REAL_MARKET_DATA = False  # Disabled: Generate synthetic market data for all securities
REAL_MARKET_DATA_CSV_PATH = None  # Not used in synthetic-only mode
