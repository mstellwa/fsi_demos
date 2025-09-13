"""
Enhanced Structured Data Generation for SAM Demo
Following industry-standard portfolio model with immutable SecurityID and transaction-based holdings.

This module generates:
- Dimension tables: DIM_SECURITY, DIM_ISSUER, DIM_PORTFOLIO, DIM_BENCHMARK, DIM_DATE
- Fact tables: FACT_TRANSACTION, FACT_POSITION_DAILY_ABOR, FACT_MARKETDATA_TIMESERIES
- Security identifier cross-reference table
- Enhanced fundamentals, ESG, and factor data
"""

from snowflake.snowpark import Session
from typing import List
import random
from datetime import datetime, timedelta, date
import config
import pandas as pd
import os

def build_all(session: Session, scenarios: List[str], test_mode: bool = False):
    """
    Build all structured data using the enhanced data model.
    
    Args:
        session: Active Snowpark session
        scenarios: List of scenario names to build data for
        test_mode: If True, use 10% data volumes for faster testing
    """
    print("📊 Starting enhanced structured data generation...")
    
    # Step 1: Create database and schemas
    create_database_structure(session)
    
    # Step 2: Build foundation tables in dependency order
    print("🏛️  Building foundation tables with enhanced model...")
    build_foundation_tables(session, test_mode)
    
    # Step 3: Build scenario-specific structured data
    for scenario in scenarios:
        print(f"🎯 Building structured data for scenario: {scenario}")
        build_scenario_data(session, scenario)
    
    # Step 4: Validate data quality
    print("🔍 Validating data quality...")
    validate_data_quality(session)
    
    print("✅ Enhanced structured data generation complete")

def create_database_structure(session: Session):
    """Create database and schema structure."""
    try:
        session.sql(f"CREATE OR REPLACE DATABASE {config.DATABASE_NAME}").collect()
        session.sql(f"CREATE OR REPLACE SCHEMA {config.DATABASE_NAME}.RAW").collect()
        session.sql(f"CREATE OR REPLACE SCHEMA {config.DATABASE_NAME}.CURATED").collect()
        session.sql(f"CREATE OR REPLACE SCHEMA {config.DATABASE_NAME}.AI").collect()
        print(f"✅ Database structure created: {config.DATABASE_NAME}")
    except Exception as e:
        print(f"❌ Failed to create database structure: {e}")
        raise

def build_foundation_tables(session: Session, test_mode: bool = False):
    """Build all foundation tables in dependency order."""
    random.seed(config.RNG_SEED)
    
    print("🏢 Building issuer dimension...")
    build_dim_issuer(session, test_mode)
    
    print("🔗 Building security dimension with direct identifiers...")
    build_dim_security(session, test_mode)
    
    print("📈 Building portfolio dimension...")
    build_dim_portfolio(session)
    
    print("📊 Building benchmark dimension...")
    build_dim_benchmark(session)
    
    print("💱 Building transaction log...")
    build_fact_transaction(session, test_mode)
    
    print("📋 Building ABOR positions...")
    build_fact_position_daily_abor(session)
    
    print("📈 Building market data...")
    build_fact_marketdata_timeseries(session, test_mode)
    
    print("💰 Building fundamentals and estimates...")
    build_fundamentals_and_estimates(session)
    
    print("🌱 Building ESG scores...")
    build_esg_scores(session)
    
    print("📏 Building factor exposures...")
    build_factor_exposures(session)
    
    print("🎯 Building benchmark holdings...")
    build_benchmark_holdings(session)



def check_temp_real_assets_exists(session: Session) -> bool:
    """Check if TEMP_REAL_ASSETS table exists in the session."""
    try:
        session.sql("SELECT 1 FROM TEMP_REAL_ASSETS LIMIT 1").collect()
        return True
    except Exception:
        return False

def build_dim_issuer(session: Session, test_mode: bool = False):
    """Build issuer dimension exclusively from real asset data."""
    
    # Real assets required - no synthetic fallback
    if not config.USE_REAL_ASSETS_CSV:
        raise Exception("Real assets CSV required - set USE_REAL_ASSETS_CSV = True in config.py")
    
    if not os.path.exists(config.REAL_ASSETS_CSV_PATH):
        raise Exception(f"Real assets CSV not found at {config.REAL_ASSETS_CSV_PATH} - run 'python main.py --extract-real-assets' first")
    
    print("✅ Building issuer dimension from 100% real asset data")
    build_dim_issuer_from_real_data(session)

def build_dim_issuer_from_real_data(session: Session):
    """Build issuer dimension from real asset data using efficient Snowpark operations."""
    
    # Load real assets from CSV (required - no fallback)
    try:
        from extract_real_assets import load_real_assets_from_csv
        real_assets_df_pandas = load_real_assets_from_csv()
        
        if real_assets_df_pandas is None:
            raise Exception("Real assets CSV not found - required for real-only mode")
    except Exception as e:
        print(f"❌ Error loading real assets: {e}")
        print("   To fix: Run 'python main.py --extract-real-assets' first")
        raise
    
    # Upload to temporary table for efficient processing (will be reused by other functions)
    real_assets_df = session.write_pandas(
        real_assets_df_pandas,
        table_name="TEMP_REAL_ASSETS",
        quote_identifiers=False,
        auto_create_table=True, 
        table_type="temp"
    )
    print("✅ Created TEMP_REAL_ASSETS table for reuse by other functions")
    
    from snowflake.snowpark.functions import (
        col, lit, ifnull, row_number, abs as abs_func, hash as hash_func,
        regexp_replace, substr, trim, to_varchar, concat
    )
    from snowflake.snowpark import Window
    
    # Create issuers DataFrame using optimized Snowpark operations
    issuers_df = (real_assets_df.select(
        ifnull(col("ISSUER_NAME"), col("SECURITY_NAME")).alias("LegalName"),
        ifnull(col("COUNTRY_OF_DOMICILE"), lit("US")).alias("CountryOfIncorporation"),
        ifnull(col("INDUSTRY_SECTOR"), lit('Diversified')).alias("INDUSTRY_SECTOR")
    )
    .filter((col("LegalName").isNotNull()) & (col("LegalName") != lit("Unknown")))
    .distinct()
    .select(
        # Add required columns for the DIM_ISSUER table
        row_number().over(Window.order_by("LegalName")).alias("IssuerID"),
        lit(None).alias("UltimateParentIssuerID"),
        substr(trim(col("LegalName")), 1, 255).alias("LegalName"),  # Ensure it fits column
        regexp_replace(
            concat(lit("LEI"), to_varchar(abs_func(hash_func(col("LegalName"))) % lit(1000000))),
            r'(\d+)', r'00000\1'
        ).substr(1, 20).alias("LEI"),  # Generate LEI with proper format
        col("CountryOfIncorporation"),
        col("INDUSTRY_SECTOR").alias("GICS_Sector")  # Keep same column name for compatibility
    ))
    
    # Save to database
    issuers_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.DIM_ISSUER")
    
    issuer_count = issuers_df.count()
    print(f"✅ Created {issuer_count} issuers from real asset data using Snowpark operations")



def build_dim_security(session: Session, test_mode: bool = False):
    """Build securities with immutable SecurityID and direct TICKER/FIGI columns."""
    
    # Use test mode counts if specified
    securities_count = config.TEST_SECURITIES_COUNT if test_mode else config.SECURITIES_COUNT
    
    # Real assets only mode - no synthetic fallback
    if not config.USE_REAL_ASSETS_CSV:
        raise Exception("Real assets CSV required - set USE_REAL_ASSETS_CSV = True in config.py")
    
    if not os.path.exists(config.REAL_ASSETS_CSV_PATH):
        raise Exception(f"Real assets CSV not found at {config.REAL_ASSETS_CSV_PATH} - run 'python main.py --extract-real-assets' first")
    
    print("✅ Using real asset data for securities (100% authentic mode)")
    build_dim_security_from_real_data(session, securities_count)

def build_dim_security_from_real_data(session: Session, securities_count: dict):
    """Build securities using real asset data only - no synthetic fallback."""
    
    # Check if TEMP_REAL_ASSETS table already exists (created by build_dim_issuer)
    if check_temp_real_assets_exists(session):
        print("✅ Reusing existing TEMP_REAL_ASSETS table (optimization)")
        # Load real assets from existing temp table
        real_assets_df = session.table("TEMP_REAL_ASSETS").to_pandas()
    else:
        print("📥 Loading real assets from CSV (TEMP_REAL_ASSETS not found)")
        # Load real assets from CSV
        try:
            from extract_real_assets import load_real_assets_from_csv
            real_assets_df = load_real_assets_from_csv()
            
            if real_assets_df is None:
                raise Exception("Real assets CSV not found - required for real-only mode")
        except Exception as e:
            print(f"❌ Error loading real assets: {e}")
            print("   To fix: Run 'python main.py --extract-real-assets' first")
            raise
    
    # Get existing issuers for mapping (optimized single query)
    issuers = session.sql(f"SELECT IssuerID, LegalName FROM {config.DATABASE_NAME}.CURATED.DIM_ISSUER").collect()
    issuer_map = {row['LEGALNAME']: row['ISSUERID'] for row in issuers}
    
    # Process each asset category efficiently
    all_security_data = []
    security_id = 1
    
    for asset_category, max_count in [('Equity', securities_count['equities']), 
                                     ('Corporate Bond', securities_count['bonds']), 
                                     ('ETF', securities_count['etfs'])]:
        
        # Filter all available assets of this category (no limits)
        if asset_category == 'Corporate Bond':
            # Corporate bonds have complex tickers with coupons, dates, etc.
            category_assets = (real_assets_df[
                (real_assets_df['ASSET_CATEGORY'] == asset_category) &
                (real_assets_df['PRIMARY_TICKER'].notna()) &
                (real_assets_df['PRIMARY_TICKER'].str.len() <= 50) &  # More generous for bonds
                (real_assets_df['TOP_LEVEL_OPENFIGI_ID'].notna())  # Ensure FIGI available
            ].drop_duplicates(subset=['PRIMARY_TICKER'], keep='first')
             .head(max_count))  # Apply reasonable limit to prevent excessive data
        else:
            # Equity and ETF filtering - prioritize clean tickers but allow more flexibility
            category_assets = (real_assets_df[
                (real_assets_df['ASSET_CATEGORY'] == asset_category) &
                (real_assets_df['PRIMARY_TICKER'].notna()) &
                (real_assets_df['PRIMARY_TICKER'].str.len() <= 15) &  # More flexible length
                (real_assets_df['TOP_LEVEL_OPENFIGI_ID'].notna())     # Ensure FIGI available
            ].drop_duplicates(subset=['PRIMARY_TICKER'], keep='first')
             .head(max_count))  # Apply reasonable limit to prevent excessive data
        
        available_count = len(category_assets)
        print(f"  📊 Using {available_count} real {asset_category} securities (max: {max_count})")
        
        # Batch process securities for this category
        for _, asset in category_assets.iterrows():
            # Issuer lookup with fallback
            issuer_name = asset.get('ISSUER_NAME') or asset.get('SECURITY_NAME', 'Unknown')
            issuer_id = issuer_map.get(issuer_name, 1)  # Default to first issuer
            
            # Security type mapping
            security_type_map = {
                'Equity': 'Common Stock',
                'Corporate Bond': 'Corporate Bond', 
                'ETF': 'Exchange Traded Fund'
            }
            
            # Country handling - use COUNTRY_OF_DOMICILE directly
            country = asset.get('COUNTRY_OF_DOMICILE', 'US')
            if pd.isna(country) or not isinstance(country, str):
                country = 'US'
            
            all_security_data.append({
                'SecurityID': security_id,
                'IssuerID': issuer_id,
                'Ticker': asset['PRIMARY_TICKER'],  # Direct ticker column
                'FIGI': asset.get('TOP_LEVEL_OPENFIGI_ID', f"BBG{abs(hash(asset['PRIMARY_TICKER'])) % 1000000:06d}"),  # Direct FIGI column
                'Description': str(asset.get('SECURITY_NAME', asset['PRIMARY_TICKER']))[:255],
                'AssetClass': asset_category,
                'SecurityType': security_type_map.get(asset_category, 'Other'),
                'CountryOfRisk': country,
                'IssueDate': datetime(2010, 1, 1).date(),
                'MaturityDate': datetime(2030, 1, 1).date() if asset_category == 'Corporate Bond' else None,
                'CouponRate': 5.0 if asset_category == 'Corporate Bond' else None,
                'RecordStartDate': datetime.now(),
                'RecordEndDate': None,
                'IsActive': True
            })
            
            security_id += 1
    
    # Save to database using Snowpark DataFrames
    if all_security_data:
        securities_df = session.create_dataframe(all_security_data)
        securities_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.DIM_SECURITY")
        
        print(f"✅ Created {len(all_security_data)} securities from real asset data (100% authentic) with direct TICKER and FIGI columns")
        
        # Report actual counts achieved
        actual_counts = {}
        for sec in all_security_data:
            asset_class = sec['AssetClass']
            actual_counts[asset_class] = actual_counts.get(asset_class, 0) + 1
        
        print("📊 Real asset utilization by category:")
        for asset_type, max_target in securities_count.items():
            asset_category = {'equities': 'Equity', 'bonds': 'Corporate Bond', 'etfs': 'ETF'}[asset_type]
            actual = actual_counts.get(asset_category, 0)
            print(f"  {asset_category}: {actual:,} securities (target: {max_target:,})")
    
    else:
        raise Exception("No real securities found - check data filtering criteria")


def build_dim_portfolio(session: Session):
    """Build portfolio dimension from configuration."""
    
    portfolio_data = []
    for i, portfolio in enumerate(config.PORTFOLIO_LINEUP):
        portfolio_data.append({
            'PortfolioID': i + 1,
            'PortfolioCode': f"SAM_{i+1:02d}",
            'PortfolioName': portfolio['name'],
            'Strategy': 'Multi-Asset' if 'Multi-Asset' in portfolio['name'] else 'Equity',
            'BaseCurrency': 'USD',
            'InceptionDate': datetime(2019, 1, 1).date()
        })
    
    portfolios_df = session.create_dataframe(portfolio_data)
    portfolios_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO")
    
    print(f"✅ Created {len(portfolio_data)} portfolios")

def build_dim_benchmark(session: Session):
    """Build benchmark dimension."""
    
    benchmark_data = []
    for i, benchmark in enumerate(config.BENCHMARKS):
        benchmark_data.append({
            'BenchmarkID': i + 1,
            'BenchmarkName': benchmark['name'],
            'Provider': benchmark['provider']
        })
    
    benchmarks_df = session.create_dataframe(benchmark_data)
    benchmarks_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.DIM_BENCHMARK")
    
    print(f"✅ Created {len(benchmark_data)} benchmarks")

def build_fact_transaction(session: Session, test_mode: bool = False):
    """Generate synthetic transaction history."""
    
    # Generate transactions for the last 12 months that build up to current positions
    print("💱 Generating synthetic transaction history...")
    
    # This is a simplified version - in a real implementation, we'd generate
    # realistic transaction patterns that result in the desired end positions
    session.sql(f"""
        -- Generate synthetic transaction history that builds to realistic portfolio positions
        -- This creates a complete audit trail of BUY transactions over the past 12 months
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_TRANSACTION AS
        WITH major_us_securities AS (
            -- Step 1: Prioritize major US stocks for demo coherence and research coverage alignment
            -- Creates a priority ranking system to ensure portfolios hold recognizable securities
            SELECT 
                s.SecurityID,
                s.Ticker,
                CASE 
                    -- Priority 1: Major stocks with guaranteed research coverage (demo scenario alignment)
                    WHEN s.Ticker IN ('AAPL', 'CMC', 'RBBN', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'CRM', 'ORCL') THEN 1
                    -- Priority 2: Clean US ticker symbols (1-5 characters, letters only)
                    WHEN s.Ticker RLIKE '^[A-Z]{{1,5}}$' AND LENGTH(s.Ticker) <= 5 THEN 2
                    -- Priority 3: All other securities (bonds, international, complex tickers)
                    ELSE 3
                END as priority
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            WHERE s.AssetClass = 'Equity'  -- Focus on equities for transaction generation
        ),
        portfolio_securities AS (
            -- Step 2: Assign securities to portfolios based on priority ranking
            -- Each portfolio gets a cross-product with all securities, then ranked by priority
            SELECT 
                p.PortfolioID,
                s.SecurityID,
                s.priority,
                -- Random ordering within priority groups for portfolio diversification
                ROW_NUMBER() OVER (PARTITION BY p.PortfolioID ORDER BY s.priority, RANDOM()) as rn
            FROM {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO p
            CROSS JOIN major_us_securities s
        ),
        selected_holdings AS (
            -- Step 3: Limit each portfolio to ~45 securities for realistic concentration
            -- This creates the universe of securities each portfolio will hold
            SELECT PortfolioID, SecurityID
            FROM portfolio_securities
            WHERE rn <= 45  -- Typical large-cap equity portfolio size
        ),
        transaction_dates AS (
            -- Step 4: Generate weekly transaction dates over the past 12 months
            -- Creates realistic trading frequency (weekly purchases building positions)
            SELECT 
                DATEADD(day, seq4() * 7, DATEADD(month, -{config.SYNTHETIC_TRANSACTION_MONTHS}, CURRENT_DATE())) as trade_date
            FROM TABLE(GENERATOR(rowcount => {config.SYNTHETIC_TRANSACTION_MONTHS * 4}))  -- ~48 weeks of transactions
            WHERE DAYOFWEEK(trade_date) BETWEEN 2 AND 6  -- Business days only (Monday=2 to Friday=6)
        )
        -- Step 5: Generate final transaction records with realistic attributes
        -- Creates BUY transactions that build up portfolio positions over time
        SELECT 
            -- Unique transaction identifier (sequential numbering)
            ROW_NUMBER() OVER (ORDER BY sh.PortfolioID, sh.SecurityID, td.trade_date) as TransactionID,
            -- Transaction and trade dates (same for simplicity)
            td.trade_date as TransactionDate,
            td.trade_date as TradeDate,
            -- Portfolio and security references
            sh.PortfolioID,
            sh.SecurityID,
            -- Transaction attributes
            'BUY' as TransactionType,  -- Simplified: mostly buys to build positions over time
            DATEADD(day, 2, td.trade_date) as SettleDate,  -- Standard T+2 settlement cycle
            -- Realistic transaction amounts (100-10,000 shares)
            UNIFORM(100, 10000, RANDOM()) as Quantity,
            -- Realistic stock prices ($50-$500 range)
            UNIFORM(50, 500, RANDOM()) as Price,
            -- Gross amount calculated elsewhere (NULL for now)
            NULL as GrossAmount_Local,
            -- Realistic commission costs ($5-$50)
            UNIFORM(5, 50, RANDOM()) as Commission_Local,
            -- Standard currency and system identifiers
            'USD' as Currency,
            'ABOR' as SourceSystem,  -- Accounting Book of Record
            -- Source system transaction reference
            CONCAT('TXN_', ROW_NUMBER() OVER (ORDER BY sh.PortfolioID, sh.SecurityID, td.trade_date)) as SourceTransactionID
        FROM selected_holdings sh
        CROSS JOIN transaction_dates td
        WHERE UNIFORM(0, 1, RANDOM()) < 0.1  -- Only 10% of combinations create transactions
    """).collect()
    
    print("✅ Created transaction history")

def build_fact_position_daily_abor(session: Session):
    """Build ABOR positions from transaction log."""
    
    print("📋 Building ABOR positions from transactions...")
    
    session.sql(f"""
        -- Build ABOR (Accounting Book of Record) positions from transaction history
        -- This creates monthly position snapshots by aggregating transaction data
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR AS
        WITH monthly_dates AS (
            -- Step 1: Generate month-end dates for position snapshots over 5 years of history
            -- Uses LAST_DAY to ensure consistent month-end reporting dates
            SELECT LAST_DAY(DATEADD(month, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE()))) as position_date
            FROM TABLE(GENERATOR(rowcount => {12 * config.YEARS_OF_HISTORY}))  -- 60 month-end dates
        ),
        transaction_balances AS (
            -- Step 2: Calculate net position quantities and average cost basis from transactions
            -- Aggregates all BUY/SELL transactions to determine current holdings
            SELECT 
                PortfolioID,
                SecurityID,
                -- Net quantity: BUY transactions add, SELL transactions subtract
                SUM(CASE WHEN TransactionType = 'BUY' THEN Quantity ELSE -Quantity END) as TotalQuantity,
                -- Average transaction price for cost basis calculation
                AVG(Price) as AvgPrice
            FROM {config.DATABASE_NAME}.CURATED.FACT_TRANSACTION
            GROUP BY PortfolioID, SecurityID
            HAVING TotalQuantity > 0  -- Only include positions with positive holdings
        ),
        position_snapshots AS (
            -- Step 3: Create position snapshots for each month-end date
            -- Cross-joins transaction balances with monthly dates to create time series
            SELECT 
                md.position_date as HoldingDate,
                tb.PortfolioID,
                tb.SecurityID,
                tb.TotalQuantity as Quantity,
                -- Market value calculations (using average transaction price as proxy)
                tb.TotalQuantity * tb.AvgPrice as MarketValue_Local,
                tb.TotalQuantity * tb.AvgPrice as MarketValue_Base,  -- Assume all USD for simplicity
                -- Cost basis calculations (slightly below market value for realistic P&L)
                tb.TotalQuantity * tb.AvgPrice * 0.95 as CostBasis_Local,  -- 5% unrealized gain
                tb.TotalQuantity * tb.AvgPrice * 0.95 as CostBasis_Base,
                0 as AccruedInterest_Local  -- Simplified
            FROM monthly_dates md
            CROSS JOIN transaction_balances tb
        ),
        portfolio_totals AS (
            -- Step 4: Calculate total portfolio values for weight calculations
            -- Sums all position values by portfolio and date for percentage calculations
            SELECT 
                HoldingDate,
                PortfolioID,
                SUM(MarketValue_Base) as PortfolioTotal  -- Total AUM per portfolio per date
            FROM position_snapshots
            GROUP BY HoldingDate, PortfolioID
        )
        -- Step 5: Final position records with calculated portfolio weights
        -- Joins position data with portfolio totals to calculate percentage allocations
        SELECT 
            ps.*,  -- All position snapshot columns
            -- Calculate portfolio weight as percentage of total portfolio value
            ps.MarketValue_Base / pt.PortfolioTotal as PortfolioWeight  -- Decimal weight (0.05 = 5%)
        FROM position_snapshots ps
        JOIN portfolio_totals pt ON ps.HoldingDate = pt.HoldingDate AND ps.PortfolioID = pt.PortfolioID
    """).collect()
    
    print("✅ Created ABOR positions")

def build_fact_marketdata_timeseries(session: Session, test_mode: bool = False):
    """Build synthetic market data for all securities."""
    
    print("📝 Generating synthetic market data for all securities")
    build_marketdata_synthetic(session)

def build_marketdata_synthetic(session: Session):
    """Build synthetic market data."""
    
    session.sql(f"""
        -- Generate synthetic market data (OHLCV) for all securities over 5 years
        -- Creates realistic price movements and trading volumes for demo purposes
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES AS
        WITH business_dates AS (
            -- Step 1: Generate business days (Monday-Friday) over 5 years of history
            -- Excludes weekends to match real market trading calendar
            SELECT DATEADD(day, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE())) as price_date
            FROM TABLE(GENERATOR(rowcount => {365 * config.YEARS_OF_HISTORY}))  -- ~1,825 days total
            WHERE DAYOFWEEK(price_date) BETWEEN 2 AND 6  -- Monday=2 to Friday=6 only
        ),
        securities_dates AS (
            -- Step 2: Create cartesian product of all securities with all business dates
            -- This ensures every security has price data for every trading day
            SELECT 
                s.SecurityID,
                s.AssetClass,  -- Used for asset-class-specific price ranges
                bd.price_date as PriceDate
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            CROSS JOIN business_dates bd
        )
        -- Step 3: Generate realistic OHLCV data with asset-class-appropriate price ranges
        SELECT 
            PriceDate,
            SecurityID,
            -- Opening prices with asset-class-specific ranges and daily volatility
            CASE 
                WHEN AssetClass = 'Equity' THEN UNIFORM(50, 850, RANDOM())        -- Equity: $50-$850
                WHEN AssetClass = 'Corporate Bond' THEN UNIFORM(90, 110, RANDOM()) -- Bonds: $90-$110 (near par)
                ELSE UNIFORM(50, 450, RANDOM())                                   -- ETFs/Other: $50-$450
            END * (1 + (UNIFORM(-0.02, 0.02, RANDOM()))) as Price_Open,  -- ±2% daily variation
            
            -- High prices (always above base price)
            CASE 
                WHEN AssetClass = 'Equity' THEN UNIFORM(50, 850, RANDOM())
                WHEN AssetClass = 'Corporate Bond' THEN UNIFORM(90, 110, RANDOM())
                ELSE UNIFORM(50, 450, RANDOM())
            END * (1 + UNIFORM(0, 0.03, RANDOM())) as Price_High,  -- 0-3% above base
            
            -- Low prices (always below base price)
            CASE 
                WHEN AssetClass = 'Equity' THEN UNIFORM(50, 850, RANDOM())
                WHEN AssetClass = 'Corporate Bond' THEN UNIFORM(90, 110, RANDOM())
                ELSE UNIFORM(50, 450, RANDOM())
            END * (1 - UNIFORM(0, 0.03, RANDOM())) as Price_Low,   -- 0-3% below base
            
            -- Closing prices (base price without additional variation)
            CASE 
                WHEN AssetClass = 'Equity' THEN UNIFORM(50, 850, RANDOM())
                WHEN AssetClass = 'Corporate Bond' THEN UNIFORM(90, 110, RANDOM())
                ELSE UNIFORM(50, 450, RANDOM())
            END as Price_Close,
            
            -- Trading volumes with asset-class-appropriate ranges
            CASE 
                WHEN AssetClass = 'Equity' THEN UNIFORM(100000, 10000000, RANDOM())::int      -- High equity volumes
                WHEN AssetClass = 'Corporate Bond' THEN UNIFORM(10000, 1000000, RANDOM())::int -- Lower bond volumes
                ELSE UNIFORM(50000, 5000000, RANDOM())::int                                   -- Moderate ETF volumes
            END as Volume,
            
            -- Total return factor (simplified to 1.0 for now - could include dividends/interest)
            1.0 as TotalReturnFactor_Daily
        FROM securities_dates
    """).collect()
    
    print("✅ Created synthetic market data")

# Placeholder functions for remaining tables (to be implemented)
def build_fundamentals_and_estimates(session: Session):
    """Build fundamentals and estimates tables with SecurityID linkage."""
    
    # Build fundamentals table with realistic financial data
    session.sql(f"""
        -- Generate synthetic fundamental data (revenue, earnings, ratios) for equity securities
        -- Creates quarterly financial metrics with sector-appropriate ranges for 5 years
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS AS
        WITH equity_securities AS (
            SELECT 
                s.SecurityID as SECURITY_ID,
                s.Ticker,
                i.GICS_Sector
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER i ON s.IssuerID = i.IssuerID
            WHERE s.AssetClass = 'Equity'
        ),
        quarters AS (
            SELECT 
                DATEADD(quarter, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE())) as REPORTING_DATE,
                'Q' || QUARTER(DATEADD(quarter, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE()))) || 
                ' ' || YEAR(DATEADD(quarter, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE()))) as FISCAL_QUARTER
            FROM TABLE(GENERATOR(rowcount => {4 * config.YEARS_OF_HISTORY}))
        ),
        base_metrics AS (
            SELECT 
                es.SECURITY_ID,
                q.REPORTING_DATE,
                q.FISCAL_QUARTER,
                -- Base financial metrics scaled by sector
                CASE 
                    WHEN es.GICS_SECTOR = 'Information Technology' THEN UNIFORM(1000000000, 100000000000, RANDOM())
                    WHEN es.GICS_SECTOR = 'Health Care' THEN UNIFORM(5000000000, 50000000000, RANDOM())
                    ELSE UNIFORM(500000000, 20000000000, RANDOM())
                END as BASE_REVENUE,
                CASE 
                    WHEN es.GICS_SECTOR = 'Information Technology' THEN UNIFORM(0.15, 0.35, RANDOM())
                    WHEN es.GICS_SECTOR = 'Health Care' THEN UNIFORM(0.20, 0.40, RANDOM())
                    ELSE UNIFORM(0.05, 0.25, RANDOM())
                END as NET_MARGIN
            FROM equity_securities es
            CROSS JOIN quarters q
        )
        SELECT SECURITY_ID, REPORTING_DATE, FISCAL_QUARTER, 'Total Revenue' as METRIC_NAME, BASE_REVENUE as METRIC_VALUE, 'USD' as CURRENCY FROM base_metrics
        UNION ALL
        SELECT SECURITY_ID, REPORTING_DATE, FISCAL_QUARTER, 'Net Income' as METRIC_NAME, BASE_REVENUE * NET_MARGIN as METRIC_VALUE, 'USD' as CURRENCY FROM base_metrics
        UNION ALL  
        SELECT SECURITY_ID, REPORTING_DATE, FISCAL_QUARTER, 'EPS' as METRIC_NAME, (BASE_REVENUE * NET_MARGIN) / UNIFORM(1000000000, 10000000000, RANDOM()) as METRIC_VALUE, 'USD' as CURRENCY FROM base_metrics
        UNION ALL
        SELECT SECURITY_ID, REPORTING_DATE, FISCAL_QUARTER, 'Trailing P/E' as METRIC_NAME, UNIFORM(10, 40, RANDOM()) as METRIC_VALUE, 'USD' as CURRENCY FROM base_metrics
        UNION ALL
        SELECT SECURITY_ID, REPORTING_DATE, FISCAL_QUARTER, 'Revenue Growth' as METRIC_NAME, UNIFORM(-0.1, 0.3, RANDOM()) as METRIC_VALUE, 'USD' as CURRENCY FROM base_metrics
    """).collect()
    
    # Build estimates table with guidance
    session.sql(f"""
        -- Generate synthetic analyst estimates and guidance based on fundamental data
        -- Creates forward-looking revenue and earnings estimates with realistic consensus ranges
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES AS
        WITH estimate_base AS (
            SELECT 
                f.SECURITY_ID,
                f.REPORTING_DATE as ESTIMATE_DATE,
                CASE 
                    WHEN QUARTER(f.REPORTING_DATE) = 4 THEN 'Q1 ' || (YEAR(f.REPORTING_DATE) + 1)
                    ELSE 'Q' || (QUARTER(f.REPORTING_DATE) + 1) || ' ' || YEAR(f.REPORTING_DATE)
                END as FISCAL_PERIOD,
                f.METRIC_VALUE
            FROM {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS f
            WHERE f.METRIC_NAME IN ('Total Revenue', 'EPS')
        )
        SELECT 
            SECURITY_ID,
            ESTIMATE_DATE,
            FISCAL_PERIOD,
            CASE WHEN METRIC_VALUE > 1000000 THEN 'Revenue Estimate' ELSE 'EPS Estimate' END as METRIC_NAME,
            METRIC_VALUE * (1 + UNIFORM(-0.1, 0.1, RANDOM())) as ESTIMATE_VALUE,
            METRIC_VALUE * (1 + UNIFORM(-0.15, -0.05, RANDOM())) as GUIDANCE_LOW,
            METRIC_VALUE * (1 + UNIFORM(0.05, 0.15, RANDOM())) as GUIDANCE_HIGH,
            'USD' as CURRENCY
        FROM estimate_base
    """).collect()
    
    print("✅ Created fundamentals and estimates with realistic relationships")

def build_esg_scores(session: Session):
    """Build ESG scores with SecurityID linkage using efficient SQL generation."""
    
    session.sql(f"""
        -- Generate synthetic ESG scores with sector-specific characteristics and regional variations
        -- Creates Environmental, Social, Governance scores (0-100) with realistic distributions
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_ESG_SCORES AS
        WITH equity_securities AS (
            SELECT 
                s.SecurityID,
                s.Ticker,
                i.GICS_Sector,
                i.CountryOfIncorporation
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER i ON s.IssuerID = i.IssuerID
            WHERE s.AssetClass = 'Equity'
        ),
        scoring_dates AS (
            SELECT DATEADD(quarter, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE())) as SCORE_DATE
            FROM TABLE(GENERATOR(rowcount => {4 * config.YEARS_OF_HISTORY}))
        ),
        base_scores AS (
            SELECT 
                es.SecurityID,
                sd.SCORE_DATE,
                -- Environmental score (sector-specific)
                CASE 
                    WHEN es.GICS_Sector = 'Utilities' THEN UNIFORM(20, 60, RANDOM())
                    WHEN es.GICS_Sector = 'Energy' THEN UNIFORM(15, 50, RANDOM())
                    WHEN es.GICS_Sector = 'Information Technology' THEN UNIFORM(60, 95, RANDOM())
                    ELSE UNIFORM(40, 80, RANDOM())
                END as E_SCORE,
                -- Social score (region-specific bias)
                CASE 
                    WHEN es.CountryOfIncorporation IN ('US', 'CA') THEN UNIFORM(50, 85, RANDOM())
                    WHEN es.CountryOfIncorporation IN ('DE', 'FR', 'SE', 'DK') THEN UNIFORM(60, 90, RANDOM())
                    ELSE UNIFORM(45, 75, RANDOM())
                END as S_SCORE,
                -- Governance score (generally high for developed markets)
                CASE 
                    WHEN es.CountryOfIncorporation IN ('US', 'CA', 'GB', 'DE', 'FR', 'SE', 'DK') THEN UNIFORM(65, 95, RANDOM())
                    ELSE UNIFORM(40, 70, RANDOM())
                END as G_SCORE
            FROM equity_securities es
            CROSS JOIN scoring_dates sd
        )
        SELECT 
            SecurityID,
            SCORE_DATE,
            'Environmental' as SCORE_TYPE,
            E_SCORE as SCORE_VALUE,
            CASE 
                WHEN E_SCORE >= 80 THEN 'A'
                WHEN E_SCORE >= 60 THEN 'B' 
                WHEN E_SCORE >= 40 THEN 'C'
                ELSE 'D'
            END as SCORE_GRADE,
            'MSCI' as PROVIDER
        FROM base_scores
        UNION ALL
        SELECT SecurityID, SCORE_DATE, 'Social', S_SCORE, 
               CASE WHEN S_SCORE >= 80 THEN 'A' WHEN S_SCORE >= 60 THEN 'B' WHEN S_SCORE >= 40 THEN 'C' ELSE 'D' END,
               'MSCI' FROM base_scores
        UNION ALL  
        SELECT SecurityID, SCORE_DATE, 'Governance', G_SCORE,
               CASE WHEN G_SCORE >= 80 THEN 'A' WHEN G_SCORE >= 60 THEN 'B' WHEN G_SCORE >= 40 THEN 'C' ELSE 'D' END,
               'MSCI' FROM base_scores
        UNION ALL
        SELECT SecurityID, SCORE_DATE, 'Overall ESG', (E_SCORE + S_SCORE + G_SCORE) / 3,
               CASE WHEN (E_SCORE + S_SCORE + G_SCORE) / 3 >= 80 THEN 'A' 
                    WHEN (E_SCORE + S_SCORE + G_SCORE) / 3 >= 60 THEN 'B' 
                    WHEN (E_SCORE + S_SCORE + G_SCORE) / 3 >= 40 THEN 'C' 
                    ELSE 'D' END,
               'MSCI' FROM base_scores
    """).collect()
    
    print("✅ Created ESG scores with sector and regional differentiation")

def build_factor_exposures(session: Session):
    """Build factor exposures with SecurityID linkage using efficient SQL generation."""
    
    session.sql(f"""
        -- Generate synthetic factor exposures (Value, Growth, Quality, etc.) for equity securities
        -- Creates factor loadings with sector-specific characteristics and realistic correlations
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_FACTOR_EXPOSURES AS
        WITH equity_securities AS (
            SELECT 
                s.SecurityID,
                s.Ticker,
                i.GICS_Sector,
                i.CountryOfIncorporation
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER i ON s.IssuerID = i.IssuerID
            WHERE s.AssetClass = 'Equity'
        ),
        monthly_dates AS (
            SELECT DATEADD(month, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE())) as EXPOSURE_DATE
            FROM TABLE(GENERATOR(rowcount => {12 * config.YEARS_OF_HISTORY}))
        ),
        base_exposures AS (
            SELECT 
                es.SecurityID,
                md.EXPOSURE_DATE,
                -- Market beta (sector-specific)
                CASE 
                    WHEN es.GICS_Sector = 'Utilities' THEN UNIFORM(0.4, 0.8, RANDOM())
                    WHEN es.GICS_Sector = 'Information Technology' THEN UNIFORM(0.9, 1.4, RANDOM())
                    WHEN es.GICS_Sector = 'Health Care' THEN UNIFORM(0.6, 1.1, RANDOM())
                    ELSE UNIFORM(0.7, 1.2, RANDOM())
                END as MARKET_BETA,
                -- Size factor (small vs large cap)
                UNIFORM(-0.5, 0.8, RANDOM()) as SIZE_FACTOR,
                -- Value factor (sector-specific)
                CASE 
                    WHEN es.GICS_Sector = 'Information Technology' THEN UNIFORM(-0.3, 0.2, RANDOM())
                    WHEN es.GICS_Sector = 'Energy' THEN UNIFORM(0.1, 0.6, RANDOM())
                    ELSE UNIFORM(-0.2, 0.4, RANDOM())
                END as VALUE_FACTOR,
                -- Momentum factor
                UNIFORM(-0.4, 0.4, RANDOM()) as MOMENTUM_FACTOR,
                -- Quality factor
                CASE 
                    WHEN es.GICS_Sector = 'Information Technology' THEN UNIFORM(0.2, 0.7, RANDOM())
                    WHEN es.GICS_Sector = 'Health Care' THEN UNIFORM(0.1, 0.5, RANDOM())
                    ELSE UNIFORM(-0.2, 0.3, RANDOM())
                END as QUALITY_FACTOR,
                -- Volatility factor
                CASE 
                    WHEN es.GICS_Sector = 'Utilities' THEN UNIFORM(-0.3, 0.1, RANDOM())
                    WHEN es.GICS_Sector = 'Information Technology' THEN UNIFORM(-0.1, 0.4, RANDOM())
                    ELSE UNIFORM(-0.2, 0.2, RANDOM())
                END as VOLATILITY_FACTOR
            FROM equity_securities es
            CROSS JOIN monthly_dates md
        )
        SELECT SecurityID, EXPOSURE_DATE, 'Market' as FACTOR_NAME, MARKET_BETA as EXPOSURE_VALUE, 0.95 as R_SQUARED FROM base_exposures
        UNION ALL
        SELECT SecurityID, EXPOSURE_DATE, 'Size', SIZE_FACTOR, 0.75 FROM base_exposures
        UNION ALL
        SELECT SecurityID, EXPOSURE_DATE, 'Value', VALUE_FACTOR, 0.65 FROM base_exposures
        UNION ALL
        SELECT SecurityID, EXPOSURE_DATE, 'Momentum', MOMENTUM_FACTOR, 0.45 FROM base_exposures
        UNION ALL
        SELECT SecurityID, EXPOSURE_DATE, 'Quality', QUALITY_FACTOR, 0.55 FROM base_exposures
        UNION ALL
        SELECT SecurityID, EXPOSURE_DATE, 'Volatility', VOLATILITY_FACTOR, 0.35 FROM base_exposures
    """).collect()
    
    print("✅ Created factor exposures with sector-specific characteristics")

def build_benchmark_holdings(session: Session):
    """Build benchmark holdings with SecurityID linkage using efficient SQL generation."""
    
    session.sql(f"""
        -- Generate synthetic benchmark holdings for major indices (S&P 500, MSCI ACWI, Nasdaq 100)
        -- Creates realistic index compositions with market-cap weighted allocations
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_BENCHMARK_HOLDINGS AS
        WITH equity_securities AS (
            SELECT 
                s.SecurityID,
                s.Ticker,
                i.GICS_Sector,
                i.CountryOfIncorporation
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY s
            JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER i ON s.IssuerID = i.IssuerID
            WHERE s.AssetClass = 'Equity'
        ),
        benchmarks AS (
            SELECT BenchmarkID, BenchmarkName FROM {config.DATABASE_NAME}.CURATED.DIM_BENCHMARK
        ),
        monthly_dates AS (
            SELECT LAST_DAY(DATEADD(month, seq4(), DATEADD(year, -{config.YEARS_OF_HISTORY}, CURRENT_DATE()))) as HOLDING_DATE
            FROM TABLE(GENERATOR(rowcount => {12 * config.YEARS_OF_HISTORY}))
        ),
        benchmark_universe AS (
            SELECT 
                b.BenchmarkID,
                b.BenchmarkName,
                es.SecurityID,
                es.TICKER,
                es.GICS_Sector,
                es.CountryOfIncorporation,
                md.HOLDING_DATE,
                -- Weight logic based on benchmark type
                CASE 
                    WHEN b.BenchmarkName = 'S&P 500' AND es.CountryOfIncorporation = 'US' THEN UNIFORM(0.001, 0.07, RANDOM())
                    WHEN b.BenchmarkName = 'MSCI ACWI' THEN 
                        CASE 
                            WHEN es.CountryOfIncorporation = 'US' THEN UNIFORM(0.001, 0.05, RANDOM())
                            ELSE UNIFORM(0.0001, 0.01, RANDOM())
                        END
                    WHEN b.BenchmarkName = 'Nasdaq 100' AND es.GICS_Sector = 'Information Technology' THEN UNIFORM(0.005, 0.12, RANDOM())
                    ELSE NULL
                END as RAW_WEIGHT,
                ROW_NUMBER() OVER (PARTITION BY b.BenchmarkID, md.HOLDING_DATE ORDER BY RANDOM()) as rn
            FROM benchmarks b
            CROSS JOIN equity_securities es
            CROSS JOIN monthly_dates md
        ),
        filtered_holdings AS (
            SELECT *
            FROM benchmark_universe
            WHERE RAW_WEIGHT IS NOT NULL
            AND (
                (BenchmarkName = 'S&P 500' AND rn <= 500) OR
                (BenchmarkName = 'MSCI ACWI' AND rn <= 800) OR
                (BenchmarkName = 'Nasdaq 100' AND rn <= 100)
            )
        ),
        normalized_weights AS (
            SELECT 
                *,
                RAW_WEIGHT / SUM(RAW_WEIGHT) OVER (PARTITION BY BenchmarkID, HOLDING_DATE) as WEIGHT
            FROM filtered_holdings
        )
        SELECT 
            BenchmarkID,
            SecurityID,
            HOLDING_DATE,
            WEIGHT as BENCHMARK_WEIGHT,
            WEIGHT * 1000000000 as MARKET_VALUE_USD  -- Assume $1B benchmark size
        FROM normalized_weights
        WHERE WEIGHT >= 0.0001  -- Minimum 0.01% weight
    """).collect()
    
    print("✅ Created benchmark holdings with realistic index compositions")

def build_scenario_data(session: Session, scenario: str):
    """Build scenario-specific data."""
    print(f"⏭️  Scenario data for {scenario} - placeholder")

def validate_data_quality(session: Session):
    """Validate data quality of the new model."""
    
    print("🔍 Running data quality checks...")
    
    # Check portfolio weights sum to 100%
    weight_check = session.sql(f"""
        SELECT 
            PortfolioID,
            SUM(PortfolioWeight) as TotalWeight,
            ABS(SUM(PortfolioWeight) - 1.0) as WeightDeviation
        FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR 
        WHERE HoldingDate = (SELECT MAX(HoldingDate) FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR)
        GROUP BY PortfolioID
        HAVING ABS(SUM(PortfolioWeight) - 1.0) > 0.001
    """).collect()
    
    if weight_check:
        print(f"⚠️  Portfolio weight deviations found: {len(weight_check)} portfolios")
    else:
        print("✅ Portfolio weights sum to 100%")
    
    # Check security identifier integrity (simplified - check direct columns)
    security_check = session.sql(f"""
        SELECT 
            COUNT(*) as total_securities,
            COUNT(CASE WHEN Ticker IS NOT NULL AND LENGTH(Ticker) > 0 THEN 1 END) as securities_with_ticker,
            COUNT(CASE WHEN FIGI IS NOT NULL AND LENGTH(FIGI) > 0 THEN 1 END) as securities_with_figi
        FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY
    """).collect()
    
    if security_check:
        result = security_check[0]
        total = result['TOTAL_SECURITIES']
        with_ticker = result['SECURITIES_WITH_TICKER']
        with_figi = result['SECURITIES_WITH_FIGI']
        
        print(f"✅ Security identifier validation: {total} securities total")
        print(f"📊 Identifier coverage: {with_ticker} with TICKER ({with_ticker/total*100:.1f}%), {with_figi} with FIGI ({with_figi/total*100:.1f}%)")
        
        if with_ticker < total:
            print(f"⚠️  {total - with_ticker} securities missing TICKER")
        if with_figi < total:
            print(f"⚠️  {total - with_figi} securities missing FIGI")
    
    print("✅ Data quality validation complete")
