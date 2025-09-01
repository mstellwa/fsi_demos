"""
Configuration settings for the Thematic Research Demo
"""

# Database Configuration
DB_NAME = "THEMES_RESEARCH_DEMO"
RAW_SCHEMA = "RAW_DATA"
ANALYTICS_SCHEMA = "ANALYTICS"
WAREHOUSE = "TRD_COMPUTE_WH"
CORTEX_SEARCH_WAREHOUSE = "TRD_CORTEX_SEARCH_WH"

# Default connection name
DEFAULT_CONNECTION = "sfseeurope-mstellwall-aws-us-west3"

# Data Generation Settings
RANDOM_SEED = 42  # Fixed seed for deterministic generation
NUM_COMPANIES = 12  # 10-12 companies as per requirements
NUM_QUARTERS = 18  # 18 quarters of financial history
NUM_MACRO_MONTHS = 48  # 48 months of macro data

# Required Anchor Company
ANCHOR_COMPANY = "Nordic Freight Systems"
ANCHOR_COMPANIES = [
    "Nordic Freight Systems",  # MANDATORY - must exist with complete data
    "Arctic Cargo AB",
    "Snowline Transport ASA", 
    "Lapland Freight Oy",
    "Baltic Logistics Group"
]

# Other logistics companies to generate
ADDITIONAL_COMPANIES = [
    "Fjord Express Lines",
    "Northern Routes Ltd",
    "Scandinavian Haulers AS",
    "Polar Transport Solutions",
    "Viking Freight Services",
    "Aurora Logistics AB",
    "Midnight Sun Carriers"
]

# Unstructured Data Volumes
NUM_NEWS_ARTICLES = 50  # 40-60 as per requirements
NUM_EXPERT_TRANSCRIPTS = 12  # 10-12
NUM_CONSULTANT_REPORTS = 8  # 6-8
NUM_INTERNAL_MEMOS = 12  # 10-12

# Earnings Calls Configuration
EARNINGS_CALLS_CONFIG = {
    "Nordic Freight Systems": 6,  # Minimum 6 quarters (mandatory)
    "Arctic Cargo AB": 4,
    "Snowline Transport ASA": 4,
    "Lapland Freight Oy": 4,
    "Baltic Logistics Group": 4,
    # Others get 2 quarters each
}

# Language Settings
SWEDISH_NEWS_FRACTION = 0.10  # 10% Swedish news
SWEDISH_PROVIDER = "SnowWire Nordics"

# Model Settings
DEFAULT_LLM_MODEL = "llama3.1-8b"
AGENT_MODEL = "claude-4.0"  # For documentation only

# Cortex Search Settings
SEARCH_REFRESH_MINUTES = 10

# Regions
PRIMARY_REGION = "Nordics"
REGIONS = ["Sweden", "Norway", "Denmark", "Finland", "Iceland", "EU", "Baltic"]

# Industrial Sectors (all logistics-focused)
SECTORS = [
    "Road Freight",
    "Maritime Logistics", 
    "Air Cargo",
    "Rail Transport",
    "Intermodal Logistics",
    "Cold Chain Logistics",
    "Last-Mile Delivery"
]
