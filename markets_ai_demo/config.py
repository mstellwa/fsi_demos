# config.py
# Master configuration for the Frost Markets Intelligence Demo

class DemoConfig:
    """Configuration settings for the Frost Markets Intelligence demo"""
    
    # --- Data Volume and Scope ---
    NUM_COMPANIES = 15
    NUM_CLIENTS = 25
    
    # --- Time Series Configuration ---
    # Number of historical quarters to generate (configurable)
    NUM_HISTORICAL_QUARTERS = 8
    # Number of years of data to generate (calculated from quarters, but can be overridden)
    NUM_HISTORICAL_YEARS = 2
    # Generate data dynamically based on current date when setup runs
    
    # --- Company & Market Data Configuration ---
    TICKER_LIST = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX",
        "JNJ", "PG", "KO", "XOM", "JPM", "BAC", "WMT"
    ]
    
    SECTOR_LIST = [
        "Technology", "Healthcare", "Financial Services", 
        "Consumer Discretionary", "Energy", "Consumer Staples"
    ]
    
    # --- Thematic & Risk Configuration ---
    THEMATIC_TAGS = [
        "Carbon Capture", "Direct Air Capture", "AI/ML", "Cloud Computing",
        "Electric Vehicles", "Renewable Energy", "Biotechnology",
        "Supply Chain Disruption", "Geopolitical Risk"
    ]
    
    RISK_EVENT_TYPES = [
        "Regulatory Change", "Natural Disaster", "Geopolitical Event",
        "Technology Breakthrough", "Market Disruption", "Credit Event",
        "Supply Chain Issue", "Cyber Security", "Climate Event"
    ]
    
    # --- Event Configuration ---
    NUM_MAJOR_EVENTS = 8
    
    # --- Client Configuration ---
    CLIENT_TYPES = [
        "Asset Manager", "Hedge Fund", "Pension Fund", 
        "Corporate Treasurer", "Insurance Company", "Sovereign Wealth Fund"
    ]
    
    # --- Snowflake AI Configuration ---
    CORTEX_MODEL_NAME = "llama3.1-70b"
    
    # --- Snowflake Connection Configuration ---
    # This value can be overridden by command-line argument
    SNOWFLAKE_CONNECTION_NAME = "sfseeurope-mstellwall-aws-us-west3"
    
    # --- Database Configuration ---
    DATABASE_NAME = "MARKETS_AI_DEMO"
    SCHEMAS = {
        "RAW_DATA": "RAW_DATA",
        "ENRICHED_DATA": "ENRICHED_DATA", 
        "ANALYTICS": "ANALYTICS"
    }
    
    # --- Warehouse Configuration ---
    COMPUTE_WAREHOUSE = "MARKETS_AI_DEMO_COMPUTE_WH"
    SEARCH_WAREHOUSE = "MARKETS_AI_DEMO_SEARCH_WH"
    
    # --- Demo Scenario Configuration ---
    PHASE_1_SCENARIOS = [
        "equity_research_earnings",
        "equity_research_thematic"
    ]
    
    PHASE_2_SCENARIOS = [
        "global_research_reports",
        "global_research_client_strategy"
    ]
