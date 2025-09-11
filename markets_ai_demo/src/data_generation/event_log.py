# src/data_generation/event_log.py
# Master event log generation for Frost Markets Intelligence Demo

import random
from datetime import datetime, timedelta
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from config import DemoConfig


def generate_master_event_log(session: Session) -> None:
    """
    Generate the master event log that drives all data correlations.
    This ensures realistic relationships between prices, news, and filings.
    """
    
    # Create the master event log table
    create_table_sql = """
    CREATE OR REPLACE TABLE MASTER_EVENT_LOG (
        EVENT_ID STRING,
        EVENT_DATE DATE,
        AFFECTED_TICKER VARCHAR(10),
        EVENT_TYPE VARCHAR(50),
        EVENT_DESCRIPTION VARCHAR(1000),
        EXPECTED_SENTIMENT FLOAT,  -- -1.0 (very negative) to 1.0 (very positive)
        EXPECTED_PRICE_IMPACT FLOAT  -- e.g., 0.05 for a 5% positive impact
    )
    """
    session.sql(create_table_sql).collect()
    print("   📊 Created MASTER_EVENT_LOG table")
    
    # Generate major market events
    events = []
    event_templates = _get_event_templates()
    
    # Generate events spread across the year
    start_date = datetime.strptime(DemoConfig.DATE_RANGE_START, "%Y-%m-%d")
    end_date = datetime.strptime(DemoConfig.DATE_RANGE_END, "%Y-%m-%d")
    
    for i in range(DemoConfig.NUM_MAJOR_EVENTS):
        # Pick random date and ticker
        random_days = random.randint(0, (end_date - start_date).days)
        event_date = start_date + timedelta(days=random_days)
        ticker = random.choice(DemoConfig.TICKER_LIST)
        
        # Select event template based on ticker/sector
        template = _select_event_template(ticker, event_templates)
        
        event = {
            "EVENT_ID": f"EVT_{i+1:03d}",
            "EVENT_DATE": event_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": ticker,
            "EVENT_TYPE": template["type"],
            "EVENT_DESCRIPTION": template["description"].format(ticker=ticker),
            "EXPECTED_SENTIMENT": template["sentiment"],
            "EXPECTED_PRICE_IMPACT": template["price_impact"]
        }
        events.append(event)
    
    # Create DataFrame and save to Snowflake
    events_df = session.create_dataframe(events)
    events_df.write.mode("overwrite").save_as_table("MASTER_EVENT_LOG")
    
    print(f"   ✅ Generated {len(events)} major market events")
    
    # Display sample events
    sample_events = session.table("MASTER_EVENT_LOG").limit(3).collect()
    print("   📋 Sample events:")
    for event in sample_events:
        print(f"      {event['EVENT_DATE']} - {event['AFFECTED_TICKER']}: {event['EVENT_DESCRIPTION'][:60]}...")


def _get_event_templates():
    """Define event templates for different scenarios"""
    return [
        {
            "type": "Technology Breakthrough",
            "description": "{ticker} announces breakthrough in quantum computing, potential to revolutionize data processing",
            "sentiment": 0.8,
            "price_impact": 0.12,
            "applicable_tickers": ["GOOGL", "IBM", "MSFT", "NVDA"]
        },
        {
            "type": "Regulatory Approval", 
            "description": "{ticker} receives FDA approval for groundbreaking GLP-1 drug for obesity treatment",
            "sentiment": 0.9,
            "price_impact": 0.15,
            "applicable_tickers": ["JNJ", "PFE", "ABBV"]
        },
        {
            "type": "Supply Chain Disruption",
            "description": "{ticker} faces production delays due to semiconductor shortage affecting Q4 guidance",
            "sentiment": -0.6,
            "price_impact": -0.08,
            "applicable_tickers": ["AAPL", "TSLA", "F", "GM"]
        },
        {
            "type": "Climate Initiative",
            "description": "{ticker} unveils $2B investment in direct air capture technology partnership",
            "sentiment": 0.7,
            "price_impact": 0.06,
            "applicable_tickers": ["XOM", "CVX", "MSFT", "GOOGL"]
        },
        {
            "type": "Cyber Security Incident",
            "description": "{ticker} reports data breach affecting customer payment information, immediate remediation underway",
            "sentiment": -0.8,
            "price_impact": -0.12,
            "applicable_tickers": ["META", "AMZN", "NFLX", "PYPL"]
        },
        {
            "type": "Market Expansion",
            "description": "{ticker} announces major expansion into Southeast Asian markets with $500M investment",
            "sentiment": 0.6,
            "price_impact": 0.08,
            "applicable_tickers": ["KO", "PG", "MCD", "SBUX"]
        },
        {
            "type": "Natural Disaster Impact",
            "description": "Major earthquake in Taiwan affects {ticker} manufacturing facilities, production halt expected",
            "sentiment": -0.7,
            "price_impact": -0.10,
            "applicable_tickers": ["AAPL", "NVDA", "AMD", "TSM"]
        },
        {
            "type": "Acquisition Announcement",
            "description": "{ticker} announces $3B acquisition of leading AI startup to accelerate automation capabilities",
            "sentiment": 0.5,
            "price_impact": 0.04,
            "applicable_tickers": ["MSFT", "GOOGL", "AMZN", "META"]
        },
        {
            "type": "Energy Transition",
            "description": "{ticker} commits to carbon neutrality by 2030, massive renewable energy investment announced",
            "sentiment": 0.6,
            "price_impact": 0.07,
            "applicable_tickers": ["XOM", "CVX", "BP", "TOT"]
        },
        {
            "type": "Earnings Surprise",
            "description": "{ticker} reports record quarterly results driven by strong demand for cloud services",
            "sentiment": 0.8,
            "price_impact": 0.10,
            "applicable_tickers": ["MSFT", "AMZN", "GOOGL", "CRM"]
        }
    ]


def _select_event_template(ticker, templates):
    """Select appropriate event template for the given ticker"""
    
    # Find templates applicable to this ticker
    applicable_templates = [
        template for template in templates 
        if ticker in template.get("applicable_tickers", DemoConfig.TICKER_LIST)
    ]
    
    # If no specific templates, use any template
    if not applicable_templates:
        applicable_templates = templates
    
    template = random.choice(applicable_templates)
    
    # Add some randomness to sentiment and price impact
    sentiment_variation = random.uniform(-0.1, 0.1)
    price_variation = random.uniform(0.8, 1.2)
    
    return {
        "type": template["type"],
        "description": template["description"],
        "sentiment": max(-1.0, min(1.0, template["sentiment"] + sentiment_variation)),
        "price_impact": template["price_impact"] * price_variation
    }
