# src/data_generation/structured_data.py
# Structured data generation for Frost Markets Intelligence Demo

import random
import math
import sys
import os
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Add the src directory to the path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DemoConfig
from utils.date_utils import get_historical_quarters, get_dynamic_date_range

fake = Faker()


def generate_all_structured_data(session: Session) -> None:
    """Generate all structured data tables for the demo"""
    
    print("   🏢 Generating companies data...")
    generate_companies(session)
    
    print("   📈 Generating historical stock prices...")
    generate_historical_stock_prices(session)
    
    print("   📊 Generating consensus estimates...")
    generate_consensus_estimates(session)
    
    print("   👥 Generating client data...")
    generate_client_data(session)
    
    print("   💼 Generating portfolio and trading data...")
    generate_portfolio_data(session)
    
    print("   🌍 Generating third-party vendor data...")
    generate_vendor_data(session)
    
    print("   ✅ All structured data generated")


def generate_companies(session: Session) -> None:
    """Generate the companies table with real tickers"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE COMPANIES (
        TICKER VARCHAR(10) PRIMARY KEY,
        COMPANY_NAME VARCHAR(100),
        SECTOR VARCHAR(100),
        INDUSTRY VARCHAR(100),
        MARKET_CAP_BILLIONS FLOAT
    )
    """
    session.sql(create_table_sql).collect()
    
    # Company mappings with realistic data
    company_data = [
        {"TICKER": "AAPL", "COMPANY_NAME": "Apple Inc.", "SECTOR": "Technology", "INDUSTRY": "Consumer Electronics", "MARKET_CAP_BILLIONS": 3000},
        {"TICKER": "MSFT", "COMPANY_NAME": "Microsoft Corporation", "SECTOR": "Technology", "INDUSTRY": "Software", "MARKET_CAP_BILLIONS": 2800},
        {"TICKER": "GOOGL", "COMPANY_NAME": "Alphabet Inc.", "SECTOR": "Technology", "INDUSTRY": "Internet Services", "MARKET_CAP_BILLIONS": 1700},
        {"TICKER": "AMZN", "COMPANY_NAME": "Amazon.com Inc.", "SECTOR": "Consumer Discretionary", "INDUSTRY": "E-commerce", "MARKET_CAP_BILLIONS": 1600},
        {"TICKER": "NVDA", "COMPANY_NAME": "NVIDIA Corporation", "SECTOR": "Technology", "INDUSTRY": "Semiconductors", "MARKET_CAP_BILLIONS": 1200},
        {"TICKER": "TSLA", "COMPANY_NAME": "Tesla Inc.", "SECTOR": "Consumer Discretionary", "INDUSTRY": "Electric Vehicles", "MARKET_CAP_BILLIONS": 800},
        {"TICKER": "META", "COMPANY_NAME": "Meta Platforms Inc.", "SECTOR": "Technology", "INDUSTRY": "Social Media", "MARKET_CAP_BILLIONS": 900},
        {"TICKER": "NFLX", "COMPANY_NAME": "Netflix Inc.", "SECTOR": "Consumer Discretionary", "INDUSTRY": "Streaming Media", "MARKET_CAP_BILLIONS": 200},
        {"TICKER": "JNJ", "COMPANY_NAME": "Johnson & Johnson", "SECTOR": "Healthcare", "INDUSTRY": "Pharmaceuticals", "MARKET_CAP_BILLIONS": 450},
        {"TICKER": "PG", "COMPANY_NAME": "Procter & Gamble Co.", "SECTOR": "Consumer Staples", "INDUSTRY": "Personal Care", "MARKET_CAP_BILLIONS": 380},
        {"TICKER": "KO", "COMPANY_NAME": "The Coca-Cola Company", "SECTOR": "Consumer Staples", "INDUSTRY": "Beverages", "MARKET_CAP_BILLIONS": 260},
        {"TICKER": "XOM", "COMPANY_NAME": "Exxon Mobil Corporation", "SECTOR": "Energy", "INDUSTRY": "Oil & Gas", "MARKET_CAP_BILLIONS": 400},
        {"TICKER": "JPM", "COMPANY_NAME": "JPMorgan Chase & Co.", "SECTOR": "Financial Services", "INDUSTRY": "Banking", "MARKET_CAP_BILLIONS": 500},
        {"TICKER": "BAC", "COMPANY_NAME": "Bank of America Corp.", "SECTOR": "Financial Services", "INDUSTRY": "Banking", "MARKET_CAP_BILLIONS": 320},
        {"TICKER": "WMT", "COMPANY_NAME": "Walmart Inc.", "SECTOR": "Consumer Staples", "INDUSTRY": "Retail", "MARKET_CAP_BILLIONS": 600}
    ]
    
    companies_df = session.create_dataframe(company_data)
    companies_df.write.mode("overwrite").save_as_table("COMPANIES")


def generate_historical_stock_prices(session: Session) -> None:
    """Generate historical stock prices with event-driven volatility"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE HISTORICAL_STOCK_PRICES (
        TICKER VARCHAR(10),
        PRICE_DATE DATE,
        OPEN NUMBER(18, 4),
        HIGH NUMBER(18, 4),
        LOW NUMBER(18, 4),
        CLOSE NUMBER(18, 4),
        VOLUME NUMBER(18, 0),
        PRIMARY KEY (TICKER, PRICE_DATE)
    )
    """
    session.sql(create_table_sql).collect()
    
    # Get events for price impact calculation
    events_df = session.table("MASTER_EVENT_LOG").collect()
    events_by_ticker = {}
    for event in events_df:
        ticker = event['AFFECTED_TICKER']
        if ticker not in events_by_ticker:
            events_by_ticker[ticker] = []
        events_by_ticker[ticker].append({
            'date': event['EVENT_DATE'],
            'impact': event['EXPECTED_PRICE_IMPACT']
        })
    
    # Generate price data for each ticker
    all_price_data = []
    # Use dynamic date range covering all historical quarters
    start_date, end_date = get_dynamic_date_range()
    
    for ticker in DemoConfig.TICKER_LIST:
        print(f"     📊 Generating prices for {ticker}...")
        
        # Starting price based on market cap
        companies_data = session.table("COMPANIES").filter(col("TICKER") == ticker).collect()
        if companies_data:
            market_cap = companies_data[0]['MARKET_CAP_BILLIONS']
            base_price = max(50, min(500, market_cap / 6))  # Rough approximation
        else:
            base_price = 150
        
        current_price = base_price
        current_date = start_date
        
        while current_date <= end_date:
            # Check for events on this date
            price_shock = 0
            if ticker in events_by_ticker:
                for event in events_by_ticker[ticker]:
                    if event['date'] == current_date.date():
                        price_shock = event['impact']
                        break
            
            # Generate daily price movement (geometric Brownian motion + events)
            daily_return = random.normalvariate(0.0005, 0.02) + price_shock  # 0.05% drift, 2% volatility
            current_price *= (1 + daily_return)
            
            # Generate OHLC data
            open_price = current_price * random.uniform(0.995, 1.005)
            close_price = current_price
            high_price = max(open_price, close_price) * random.uniform(1.0, 1.02)
            low_price = min(open_price, close_price) * random.uniform(0.98, 1.0)
            
            # Volume spike on event days
            base_volume = random.randint(1000000, 5000000)
            if abs(price_shock) > 0.03:  # Significant event
                volume = base_volume * random.uniform(2.0, 4.0)
            else:
                volume = base_volume
            
            price_record = {
                "TICKER": ticker,
                "PRICE_DATE": current_date.strftime("%Y-%m-%d"),
                "OPEN": round(open_price, 2),
                "HIGH": round(high_price, 2), 
                "LOW": round(low_price, 2),
                "CLOSE": round(close_price, 2),
                "VOLUME": int(volume)
            }
            all_price_data.append(price_record)
            
            current_date += timedelta(days=1)
    
    # Save to Snowflake in batches
    batch_size = 1000
    for i in range(0, len(all_price_data), batch_size):
        batch = all_price_data[i:i + batch_size]
        batch_df = session.create_dataframe(batch)
        
        if i == 0:
            batch_df.write.mode("overwrite").save_as_table("HISTORICAL_STOCK_PRICES")
        else:
            batch_df.write.mode("append").save_as_table("HISTORICAL_STOCK_PRICES")


def generate_consensus_estimates(session: Session) -> None:
    """Generate consensus estimates from fictional providers"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE CONSENSUS_ESTIMATES (
        TICKER VARCHAR(10),
        FISCAL_QUARTER VARCHAR(7),
        METRIC_NAME VARCHAR(50),
        ESTIMATE_VALUE NUMBER(20, 4),
        PROVIDER VARCHAR(20)
    )
    """
    session.sql(create_table_sql).collect()
    
    estimates_data = []
    # Use all historical quarters for estimates (8 quarters by default)
    quarters = get_historical_quarters()
    metrics = ["Revenue", "EPS", "Net Income"]
    providers = ["FactSet", "Bloomberg", "Refinitiv"]
    
    for ticker in DemoConfig.TICKER_LIST:
        # Get company info for scaling estimates
        companies_data = session.table("COMPANIES").filter(col("TICKER") == ticker).collect()
        market_cap = companies_data[0]['MARKET_CAP_BILLIONS'] if companies_data else 100
        
        for quarter in quarters:
            for metric in metrics:
                for provider in providers:
                    if metric == "Revenue":
                        base_value = market_cap * random.uniform(0.1, 0.3) * 1000  # Revenue in millions
                    elif metric == "EPS":
                        base_value = random.uniform(1.0, 8.0)  # EPS in dollars
                    else:  # Net Income
                        base_value = market_cap * random.uniform(0.02, 0.08) * 1000  # Net income in millions
                    
                    # Add provider variation
                    provider_variation = random.uniform(0.95, 1.05)
                    estimate_value = base_value * provider_variation
                    
                    estimates_data.append({
                        "TICKER": ticker,
                        "FISCAL_QUARTER": quarter,
                        "METRIC_NAME": metric,
                        "ESTIMATE_VALUE": round(estimate_value, 4),
                        "PROVIDER": provider
                    })
    
    estimates_df = session.create_dataframe(estimates_data)
    estimates_df.write.mode("overwrite").save_as_table("CONSENSUS_ESTIMATES")


def generate_client_data(session: Session) -> None:
    """Generate client profiles and trading activity"""
    
    # Client profiles table
    create_clients_sql = """
    CREATE OR REPLACE TABLE CLIENT_PROFILES (
        CLIENT_ID STRING PRIMARY KEY,
        CLIENT_NAME VARCHAR(100),
        CLIENT_TYPE VARCHAR(50),
        AUM_BILLIONS FLOAT,
        REGION VARCHAR(50)
    )
    """
    session.sql(create_clients_sql).collect()
    
    clients_data = []
    
    # Strategic: Ensure we have asset managers at specific positions for targeting scenario
    # Force CLI_003, CLI_007, CLI_011, CLI_015, CLI_019, CLI_023 to be Asset Managers for targeting
    target_positions = [3, 7, 11, 15, 19, 23]  # These will be % 4 == 3, perfect for targeting
    
    for i in range(DemoConfig.NUM_CLIENTS):
        client_num = i + 1
        
        # Strategic assignment of client types
        if client_num in target_positions:
            client_type = "Asset Manager"  # Ensure targeting opportunities
        else:
            client_type = random.choice(DemoConfig.CLIENT_TYPES)
        
        # Generate realistic client names
        if client_type == "Asset Manager":
            name = f"{fake.company()} Asset Management"
        elif client_type == "Hedge Fund":
            name = f"{fake.last_name()} Capital Partners"
        elif client_type == "Pension Fund":
            name = f"{fake.state()} State Pension Fund"
        else:
            name = f"{fake.company()} {client_type}"
        
        # AUM based on client type
        if client_type in ["Pension Fund", "Sovereign Wealth Fund"]:
            aum = random.uniform(50, 500)
        elif client_type == "Asset Manager":
            aum = random.uniform(10, 200)
        else:
            aum = random.uniform(1, 50)
        
        clients_data.append({
            "CLIENT_ID": f"CLI_{client_num:03d}",
            "CLIENT_NAME": name,
            "CLIENT_TYPE": client_type,
            "AUM_BILLIONS": round(aum, 1),
            "REGION": random.choice(["North America", "Europe", "Asia Pacific"])
        })
    
    clients_df = session.create_dataframe(clients_data)
    clients_df.write.mode("overwrite").save_as_table("CLIENT_PROFILES")
    
    # Client trading activity (focused on derivatives for EMIR 3.0 scenario)
    create_trading_sql = """
    CREATE OR REPLACE TABLE CLIENT_TRADING_ACTIVITY (
        CLIENT_ID STRING,
        TRADE_DATE DATE,
        NOTIONAL_VALUE NUMBER(20, 2),
        ASSET_CLASS VARCHAR(50),
        DERIVATIVE_TYPE VARCHAR(50),
        CLEARING_CCP VARCHAR(50),
        TRADE_ID STRING
    )
    """
    session.sql(create_trading_sql).collect()
    
    trading_data = []
    # Use dynamic date range covering all historical quarters  
    start_date, end_date = get_dynamic_date_range()
    
    for client in clients_data:
        client_id = client["CLIENT_ID"]
        
        # Generate 20-50 trades per client throughout the year
        num_trades = random.randint(20, 50)
        
        for _ in range(num_trades):
            trade_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            
            # Bias toward EUR/USD swaps for EMIR 3.0 scenario
            if random.random() < 0.4:  # 40% chance of EUR/USD swap
                derivative_type = "EUR/USD Swap"
                asset_class = "FX Derivatives"
                # Some clients heavily use non-EU CCPs (for EMIR 3.0 risk)
                clearing_ccp = random.choice(["NON_EU_CCP", "EU_CCP"]) if random.random() < 0.7 else "EU_CCP"
            else:
                derivative_type = random.choice(["Interest Rate Swap", "Credit Default Swap", "Equity Option"])
                asset_class = random.choice(["Interest Rate Derivatives", "Credit Derivatives", "Equity Derivatives"])
                clearing_ccp = random.choice(["LCH", "CME", "ICE", "EUREX"])
            
            notional = random.uniform(1000000, 100000000)  # $1M to $100M
            
            trading_data.append({
                "CLIENT_ID": client_id,
                "TRADE_DATE": trade_date.strftime("%Y-%m-%d"),
                "NOTIONAL_VALUE": round(notional, 2),
                "ASSET_CLASS": asset_class,
                "DERIVATIVE_TYPE": derivative_type,
                "CLEARING_CCP": clearing_ccp,
                "TRADE_ID": f"TRD_{len(trading_data)+1:06d}"
            })
    
    trading_df = session.create_dataframe(trading_data)
    trading_df.write.mode("overwrite").save_as_table("CLIENT_TRADING_ACTIVITY")
    
    # Generate CLIENT_ENGAGEMENT data for Market Structure Reports scenario
    generate_client_engagement(session, clients_data)
    
    # Generate CLIENT_DISCUSSIONS data for tracking one-on-one meetings
    generate_client_discussions(session, clients_data)
    
    print(f"   ✅ Client data generated: {len(clients_data)} clients, {len(trading_data)} trades")


def generate_portfolio_data(session: Session) -> None:
    """Generate firm portfolio holdings and trades"""
    
    # Portfolio holdings
    create_holdings_sql = """
    CREATE OR REPLACE TABLE PORTFOLIO_HOLDINGS (
        PORTFOLIO_ID VARCHAR(50),
        TICKER VARCHAR(10),
        QUANTITY NUMBER(18, 0),
        MARKET_VALUE NUMBER(20, 4),
        AS_OF_DATE DATE
    )
    """
    session.sql(create_holdings_sql).collect()
    
    portfolios = [
        {"id": "GLOBAL_EQUITY_FUND", "focus": "diversified"},
        {"id": "TMT_TRADING_BOOK", "focus": "technology"},
        {"id": "RISK_ARBITRAGE_FUND", "focus": "event_driven"}
    ]
    
    holdings_data = []
    latest_prices = {}
    
    # Get latest prices for market value calculation
    for ticker in DemoConfig.TICKER_LIST:
        price_data = session.table("HISTORICAL_STOCK_PRICES").filter(col("TICKER") == ticker).sort(col("PRICE_DATE").desc()).limit(1).collect()
        if price_data:
            latest_prices[ticker] = price_data[0]['CLOSE']
        else:
            latest_prices[ticker] = 100  # Default price
    
    for portfolio in portfolios:
        portfolio_id = portfolio["id"]
        focus = portfolio["focus"]
        
        # Select tickers based on portfolio focus
        if focus == "technology":
            ticker_pool = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "NFLX"]
        elif focus == "event_driven":
            ticker_pool = random.sample(DemoConfig.TICKER_LIST, 8)
        else:
            ticker_pool = DemoConfig.TICKER_LIST
        
        for ticker in ticker_pool:
            if random.random() < 0.7:  # 70% chance to hold each stock
                quantity = random.randint(10000, 500000)
                market_value = quantity * latest_prices[ticker]
                
                holdings_data.append({
                    "PORTFOLIO_ID": portfolio_id,
                    "TICKER": ticker,
                    "QUANTITY": quantity,
                    "MARKET_VALUE": round(market_value, 2),
                    "AS_OF_DATE": get_dynamic_date_range()[1].strftime("%Y-%m-%d")  # Use end of dynamic range
                })
    
    holdings_df = session.create_dataframe(holdings_data)
    holdings_df.write.mode("overwrite").save_as_table("PORTFOLIO_HOLDINGS")


def generate_vendor_data(session: Session) -> None:
    """Generate third-party vendor data (FactSet, S&P)"""
    
    # FactSet Geographic Revenue data
    create_geo_revenue_sql = """
    CREATE OR REPLACE TABLE FACTSET_GEO_REVENUE (
        TICKER VARCHAR(10),
        COUNTRY VARCHAR(50),
        REVENUE_PERCENTAGE FLOAT
    )
    """
    session.sql(create_geo_revenue_sql).collect()
    
    geo_revenue_data = []
    countries = ["United States", "China", "Germany", "Japan", "United Kingdom", "France", "Canada", "South Korea", "India", "Rest of World"]
    
    for ticker in DemoConfig.TICKER_LIST:
        # Generate revenue distribution that sums to 100%
        percentages = [random.uniform(0, 1) for _ in countries]
        total = sum(percentages)
        normalized_percentages = [p / total for p in percentages]
        
        # Bias some companies toward China exposure (for Taiwan earthquake scenario)
        if ticker in ["AAPL", "NVDA", "AMD", "QCOM"]:
            china_index = countries.index("China")
            normalized_percentages[china_index] = max(0.15, normalized_percentages[china_index])
            # Renormalize
            total = sum(normalized_percentages)
            normalized_percentages = [p / total for p in normalized_percentages]
        
        for country, percentage in zip(countries, normalized_percentages):
            if percentage > 0.01:  # Only include meaningful exposures
                geo_revenue_data.append({
                    "TICKER": ticker,
                    "COUNTRY": country,
                    "REVENUE_PERCENTAGE": round(percentage, 4)
                })
    
    geo_revenue_df = session.create_dataframe(geo_revenue_data)
    geo_revenue_df.write.mode("overwrite").save_as_table("FACTSET_GEO_REVENUE")
    
    # S&P Credit Ratings
    create_ratings_sql = """
    CREATE OR REPLACE TABLE SP_CREDIT_RATINGS (
        TICKER VARCHAR(10),
        RATING VARCHAR(10),
        RATING_DATE DATE,
        OUTLOOK VARCHAR(20)
    )
    """
    session.sql(create_ratings_sql).collect()
    
    ratings_data = []
    credit_ratings = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-"]
    outlooks = ["Positive", "Stable", "Negative"]
    
    for ticker in DemoConfig.TICKER_LIST:
        # Assign ratings based on company size/stability
        companies_data = session.table("COMPANIES").filter(col("TICKER") == ticker).collect()
        if companies_data:
            market_cap = companies_data[0]['MARKET_CAP_BILLIONS']
            sector = companies_data[0]['SECTOR']
            
            # Larger, more stable companies get better ratings
            if market_cap > 1000:
                rating = random.choice(["AAA", "AA+", "AA", "AA-"])
            elif market_cap > 500:
                rating = random.choice(["AA-", "A+", "A", "A-"])
            else:
                rating = random.choice(["A-", "BBB+", "BBB", "BBB-"])
            
            # Tech companies might have more volatile outlooks
            if sector == "Technology":
                outlook = random.choice(outlooks)
            else:
                outlook = random.choice(["Stable", "Stable", "Positive"])  # Bias toward stable
        else:
            rating = random.choice(credit_ratings)
            outlook = random.choice(outlooks)
        
        ratings_data.append({
            "TICKER": ticker,
            "RATING": rating,
            "RATING_DATE": "2024-01-01",
            "OUTLOOK": outlook
        })
    
    ratings_df = session.create_dataframe(ratings_data)
    ratings_df.write.mode("overwrite").save_as_table("SP_CREDIT_RATINGS")


def generate_client_engagement(session: Session, clients_data: list) -> None:
    """Generate client engagement data for Market Structure Reports scenario"""
    
    # Create CLIENT_ENGAGEMENT table
    create_engagement_sql = """
    CREATE OR REPLACE TABLE CLIENT_ENGAGEMENT (
        CLIENT_ID STRING,
        CONTENT_ID STRING,
        ENGAGEMENT_TYPE VARCHAR(20),
        ENGAGEMENT_TIMESTAMP TIMESTAMP_NTZ,
        ENGAGEMENT_DURATION_MINUTES INTEGER
    )
    """
    session.sql(create_engagement_sql).collect()
    
    engagement_data = []
    
    # Get research report IDs for content engagement
    research_reports = [
        "RPT_001",  # EMIR 3.0 report
        "RPT_002",  # Carbon Capture
        "RPT_003",  # Semiconductors
        "RPT_004"   # ESG
    ]
    
    # Generate engagement for the last 90 days
    start_date = datetime.now() - timedelta(days=90)
    end_date = datetime.now()
    
    for client in clients_data:
        client_id = client["CLIENT_ID"]
        client_type = client["CLIENT_TYPE"]
        
        # Asset managers have higher engagement with EMIR 3.0 content
        # Use deterministic randomization for consistent demo results
        client_hash = hash(client_id) % 100
        
        if client_type == "Asset Manager":
            # Ensure multiple high-engagement asset managers for demo
            # Use client ID position to ensure good distribution
            client_num = int(client_id.split('_')[1]) if '_' in client_id else hash(client_id) % 100
            
            # Ensure ALL asset managers have high engagement for compelling demo
            # This creates multiple high-engagement clients for targeting analysis
            # Always give asset managers high engagement (2-5 interactions)
            # All asset managers get high engagement (remove the if condition)
            # Multiple engagements with EMIR 3.0 report
            for _ in range(random.randint(2, 5)):
                    engagement_time = start_date + timedelta(
                        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
                    )
                    engagement_data.append({
                        "CLIENT_ID": client_id,
                        "CONTENT_ID": "RPT_001",  # EMIR 3.0 report
                        "ENGAGEMENT_TYPE": random.choice(["Download", "View", "Share"]),
                        "ENGAGEMENT_TIMESTAMP": engagement_time,
                        "ENGAGEMENT_DURATION_MINUTES": random.randint(5, 45)
                    })
            
            # Lower engagement with other topics
            for report_id in research_reports[1:]:
                if random.random() < 0.3:  # 30% engagement with other topics
                    engagement_time = start_date + timedelta(
                        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
                    )
                    engagement_data.append({
                        "CLIENT_ID": client_id,
                        "CONTENT_ID": report_id,
                        "ENGAGEMENT_TYPE": random.choice(["Download", "View"]),
                        "ENGAGEMENT_TIMESTAMP": engagement_time,
                        "ENGAGEMENT_DURATION_MINUTES": random.randint(3, 20)
                    })
        else:
            # Other client types have lower overall engagement
            for report_id in research_reports:
                if random.random() < 0.2:  # 20% engagement rate
                    engagement_time = start_date + timedelta(
                        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
                    )
                    engagement_data.append({
                        "CLIENT_ID": client_id,
                        "CONTENT_ID": report_id,
                        "ENGAGEMENT_TYPE": random.choice(["Download", "View"]),
                        "ENGAGEMENT_TIMESTAMP": engagement_time,
                        "ENGAGEMENT_DURATION_MINUTES": random.randint(2, 15)
                    })
    
    if engagement_data:
        engagement_df = session.create_dataframe(engagement_data)
        engagement_df.write.mode("overwrite").save_as_table("CLIENT_ENGAGEMENT")
    
    print(f"   📈 Client engagement data: {len(engagement_data)} interactions")


def generate_client_discussions(session: Session, clients_data: list) -> None:
    """Generate client discussions data to track one-on-one meetings"""
    
    # Create CLIENT_DISCUSSIONS table
    create_discussions_sql = """
    CREATE OR REPLACE TABLE CLIENT_DISCUSSIONS (
        CLIENT_ID STRING,
        DISCUSSION_DATE DATE,
        DISCUSSION_TYPE VARCHAR(50),
        TOPICS_DISCUSSED VARCHAR(500),
        RELATIONSHIP_MANAGER VARCHAR(100),
        FOLLOW_UP_SCHEDULED BOOLEAN
    )
    """
    session.sql(create_discussions_sql).collect()
    
    discussion_data = []
    
    # Generate discussions for last 6 months
    start_date = datetime.now() - timedelta(days=180)
    end_date = datetime.now()
    
    relationship_managers = [
        "Sarah Johnson", "Michael Chen", "Emily Rodriguez", 
        "David Thompson", "Lisa Wang", "James Miller"
    ]
    
    # Specific discussion topics including regulatory themes
    general_topics = [
        "Portfolio Review and Strategy",
        "Market Outlook Discussion", 
        "ESG Integration Strategy",
        "Technology Investment Review",
        "Risk Management Framework",
        "Performance Review and Analysis"
    ]
    
    regulatory_topics = [
        "EMIR 3.0 Implementation and Impact",
        "Derivatives Clearing Strategy", 
        "Regulatory Impact Assessment",
        "MiFID II Compliance Review",
        "Bond Market Transparency Requirements",
        "European Regulatory Changes"
    ]
    
    for client in clients_data:
        client_id = client["CLIENT_ID"]
        client_type = client["CLIENT_TYPE"]
        
        # Larger clients have more frequent discussions
        if client_type in ["Asset Manager", "Pension Fund"]:
            base_discussions = random.randint(2, 4)  # 2-4 discussions in 6 months
        else:
            base_discussions = random.randint(0, 2)  # 0-2 discussions in 6 months
        
        # Strategic assignment of discussion topics
        # Some asset managers with high EMIR engagement should NOT have EMIR discussions
        client_hash = hash(client_id) % 100  # Deterministic randomization
        
        # For asset managers, create strategic targeting opportunities
        if client_type == "Asset Manager":
            # Use client number to ensure some high-engagement clients don't have EMIR discussions
            client_num = int(client_id.split('_')[1]) if '_' in client_id else hash(client_id) % 100
            # Strategic: Create targeting scenario where some asset managers with high EMIR engagement
            # have NO recent discussions (within last 3 months) to enable outreach targeting
            has_recent_discussion = (client_num % 4 != 3)  # 75% have discussions, 25% don't (clients ending in 3 have no recent discussions)
            has_emir_discussion = (client_num % 3 == 0) and has_recent_discussion  # Only clients with recent discussions get EMIR topics
            # For asset managers without recent discussions, still generate some old discussions for realism
            num_discussions = base_discussions if has_recent_discussion else random.randint(1, 2)
        else:
            has_recent_discussion = True  # All others have normal discussion patterns
            has_emir_discussion = client_hash < 60  # 60% chance for others
            num_discussions = base_discussions
        
        for i in range(num_discussions):
            # If this is an asset manager without recent discussions, ensure discussions are older than 3 months
            if client_type == "Asset Manager" and not has_recent_discussion:
                # Generate discussions older than 3 months (90 days ago from now)
                cutoff_date = datetime.now() - timedelta(days=90)
                discussion_date = start_date + timedelta(
                    days=random.randint(0, (cutoff_date - start_date).days)
                )
            else:
                # Normal discussion date generation
                discussion_date = start_date + timedelta(
                    days=random.randint(0, (end_date - start_date).days)
                )
            
            # Choose topic strategically
            if client_type == "Asset Manager" and i == 0 and has_emir_discussion:
                # First discussion for some asset managers is regulatory
                topic = random.choice(regulatory_topics)
            elif random.random() < 0.3:  # 30% chance of regulatory topic for others
                topic = random.choice(regulatory_topics)
            else:
                topic = random.choice(general_topics)
            
            discussion_data.append({
                "CLIENT_ID": client_id,
                "DISCUSSION_DATE": discussion_date.date(),
                "DISCUSSION_TYPE": random.choice(["Strategic Review", "Quarterly Check-in", "Ad-hoc Consultation"]),
                "TOPICS_DISCUSSED": topic,
                "RELATIONSHIP_MANAGER": random.choice(relationship_managers),
                "FOLLOW_UP_SCHEDULED": random.choice([True, False])
            })
    
    if discussion_data:
        discussions_df = session.create_dataframe(discussion_data)
        discussions_df.write.mode("overwrite").save_as_table("CLIENT_DISCUSSIONS")
    
    print(f"   💬 Client discussions data: {len(discussion_data)} meetings")
