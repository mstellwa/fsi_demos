"""
Real Asset Data Extraction for SAM Demo

This module extracts real financial instrument data from Snowflake Marketplace
using the OpenFIGI standard to get authentic tickers for equities, corporate bonds, and ETFs.
"""

from snowflake.snowpark import Session
import os
import config

def extract_real_assets_to_csv(session: Session):
    """
    Extract real asset data from Snowflake Marketplace and save to CSV.
    
    Uses the comprehensive SQL query from asset_masterdata_guide.md to get
    real tickers for USA, EU, and APAC/EM markets across all asset classes.
    
    Args:
        session: Active Snowpark session with access to Marketplace data
    """
    
    print("🌍 Extracting ALL real asset data from Snowflake Marketplace (no limit)...")
    
    # The enhanced SQL query for better real asset coverage
    real_assets_query = f"""
WITH Enriched_Securities AS (
    -- This CTE joins the main security index with geography, company characteristics, and aggregated exchange codes.
    SELECT
        osi.TOP_LEVEL_OPENFIGI_ID,
        osi.SECURITY_NAME,
        osi.ASSET_CLASS,
        osi.SECURITY_TYPE,
        osi.SECURITY_SUBTYPE,
        osi.PRIMARY_TICKER,
        ci.PRIMARY_EXCHANGE_CODE,
        ci.PRIMARY_EXCHANGE_NAME,
        osi.EXCHANGE_CODES,
        ci.COMPANY_NAME AS ISSUER_NAME,
        -- Extract Country of Domicile from company characteristics
        MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'business_address_country' THEN char.VALUE END) AS COUNTRY_OF_DOMICILE,
        -- Use SIC Description as a proxy for industry, as GICS is not in this base dataset
        MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'sic_description' THEN char.VALUE END) AS INDUSTRY_SECTOR
    FROM
        {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.OPENFIGI_SECURITY_INDEX AS osi
    LEFT JOIN
        {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_SECURITY_RELATIONSHIPS AS rship 
            ON osi.TOP_LEVEL_OPENFIGI_ID = rship.SECURITY_ID AND osi.TOP_LEVEL_OPENFIGI_ID_TYPE = rship.security_id_type
    LEFT JOIN
        {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_INDEX AS ci ON rship.COMPANY_ID = ci.COMPANY_ID
    LEFT JOIN
        {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_CHARACTERISTICS AS char ON rship.COMPANY_ID = char.COMPANY_ID
    WHERE
        NOT (ARRAY_CONTAINS('CEDEAR'::variant, osi.SECURITY_TYPE) 
            OR ARRAY_CONTAINS('PRIV PLACEMENT'::variant, osi.SECURITY_TYPE)
            OR ARRAY_CONTAINS('Crypto'::variant, osi.SECURITY_TYPE))
    GROUP BY
        osi.TOP_LEVEL_OPENFIGI_ID,
        osi.SECURITY_NAME,
        osi.ASSET_CLASS,
        osi.SECURITY_TYPE,
        osi.SECURITY_SUBTYPE,
        osi.PRIMARY_TICKER,
        ci.PRIMARY_EXCHANGE_CODE,
        ci.PRIMARY_EXCHANGE_NAME,
        osi.EXCHANGE_CODES,
        ci.COMPANY_NAME
),
Categorized_Securities AS (
    -- This CTE applies the asset class and market region logic to each security.
    SELECT
        es.TOP_LEVEL_OPENFIGI_ID,
        es.SECURITY_NAME,
        es.ISSUER_NAME,
        es.PRIMARY_TICKER,
        es.PRIMARY_EXCHANGE_CODE,
        IFNULL(es.PRIMARY_EXCHANGE_NAME, es.EXCHANGE_CODES[0]::varchar) AS PRIMARY_EXCHANGE_NAME,
        es.EXCHANGE_CODES,
        es.INDUSTRY_SECTOR,
        es.COUNTRY_OF_DOMICILE,
        -- Asset Category Classification Logic (Expanded to include more bond types)
        CASE
            WHEN es.ASSET_CLASS = 'Corp' THEN 'Corporate Bond'
            WHEN es.ASSET_CLASS = 'Govt' THEN 'Government Bond'
            WHEN es.ASSET_CLASS = 'Muni' THEN 'Municipal Bond'
            WHEN es.ASSET_CLASS = 'Mtge' THEN 'Mortgage-Backed Security'
            WHEN es.ASSET_CLASS = 'Equity' AND (
                ARRAY_CONTAINS('ETF'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Exchange Traded Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('ETN'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('ETP'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Unit Trust'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('UIT'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Closed-End Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Open-End Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Fund of Funds'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Mutual Fund'::variant, es.SECURITY_SUBTYPE)
            ) THEN 'ETF'
            WHEN es.ASSET_CLASS = 'Equity' THEN 'Equity'
            ELSE NULL
        END AS ASSET_CATEGORY,
        -- Market Region Classification Logic
        CASE
            WHEN es.COUNTRY_OF_DOMICILE = 'US' THEN 'USA'
            WHEN es.COUNTRY_OF_DOMICILE IN (
                'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
                'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                'SI', 'ES', 'SE'
            ) THEN 'EU'
            WHEN es.COUNTRY_OF_DOMICILE IN (
                'AF', 'AU', 'BD', 'BT', 'BR', 'BN', 'KH', 'CL', 'CN', 'CO', 'CK', 'CZ',
                'KP', 'EG', 'FJ', 'GR', 'HK', 'HU', 'IN', 'ID', 'JP', 'KI', 'KW', 'LA',
                'MY', 'MV', 'MH', 'MX', 'FM', 'MN', 'MM', 'NR', 'NP', 'NZ', 'PK', 'PW',
                'PG', 'PE', 'PH', 'PL', 'QA', 'KR', 'WS', 'SA', 'SG', 'SB', 'ZA', 'LK',
                'TW', 'TH', 'TL', 'TO', 'TR', 'TV', 'AE', 'VU', 'VN'
            ) THEN 'APAC/EM'
            ELSE 'Other'
        END AS MARKET_REGION
    FROM
        Enriched_Securities AS es
)
-- Final SELECT Statement
-- This query selects the categorized and filtered data, returning the final list with all requested columns.
SELECT
    cs.MARKET_REGION,
    cs.ASSET_CATEGORY,
    cs.ISSUER_NAME,
    cs.INDUSTRY_SECTOR,
    cs.TOP_LEVEL_OPENFIGI_ID,
    cs.SECURITY_NAME,
    cs.PRIMARY_TICKER,
    cs.PRIMARY_EXCHANGE_CODE,
    cs.PRIMARY_EXCHANGE_NAME,
    cs.COUNTRY_OF_DOMICILE,
    cs.EXCHANGE_CODES
FROM
    Categorized_Securities cs
WHERE
    cs.ASSET_CATEGORY IS NOT NULL
ORDER BY
    cs.MARKET_REGION,
    cs.ASSET_CATEGORY,
    cs.ISSUER_NAME,
    cs.SECURITY_NAME
-- No LIMIT - capture all assets including USA
    """
    
    try:
        # Execute the query to get real asset data
        print("🔍 Querying Snowflake Marketplace for real asset data...")
        result_df = session.sql(real_assets_query)
        
        # Convert to pandas for CSV export
        pandas_df = result_df.to_pandas()
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(config.REAL_ASSETS_CSV_PATH), exist_ok=True)
        
        # Save to CSV
        pandas_df.to_csv(config.REAL_ASSETS_CSV_PATH, index=False)
        
        print(f"✅ Extracted {len(pandas_df)} real assets to {config.REAL_ASSETS_CSV_PATH}")
        
        # Show distribution summary
        distribution = pandas_df.groupby(['MARKET_REGION', 'ASSET_CATEGORY']).size().reset_index(name='COUNT')
        print("\n📊 Real Asset Distribution:")
        for _, row in distribution.iterrows():
            print(f"  {row['MARKET_REGION']} {row['ASSET_CATEGORY']}: {row['COUNT']:,}")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to extract real assets: {e}")
        print("Note: This requires access to FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN database")
        print("Falling back to generated ticker symbols")
        return False

def load_real_assets_from_csv():
    """
    Load real asset data from existing CSV file.
    
    Returns:
        pandas.DataFrame: Real asset data or None if file doesn't exist
    """
    
    try:
        import pandas as pd
        
        if os.path.exists(config.REAL_ASSETS_CSV_PATH):
            df = pd.read_csv(config.REAL_ASSETS_CSV_PATH)
            print(f"✅ Loaded {len(df)} real assets from {config.REAL_ASSETS_CSV_PATH}")
            return df
        else:
            print(f"❌ Real assets CSV not found at {config.REAL_ASSETS_CSV_PATH}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to load real assets CSV: {e}")
        return None

def get_real_tickers_by_region_and_class(real_assets_df, target_counts):
    """
    Extract real tickers from the CSV data according to target distributions.
    
    Args:
        real_assets_df: pandas DataFrame with real asset data
        target_counts: dict with target counts per region/asset class
        
    Returns:
        dict: Organized real tickers by region and asset class
    """
    
    if real_assets_df is None:
        return None
    
    organized_tickers = {
        'USA': {'Equity': [], 'Corporate Bond': [], 'ETF': []},
        'EU': {'Equity': [], 'Corporate Bond': [], 'ETF': []},
        'APAC/EM': {'Equity': [], 'Corporate Bond': [], 'ETF': []}
    }
    
    # Extract tickers for each region/asset class combination
    for region in ['USA', 'EU', 'APAC/EM']:
        for asset_class in ['Equity', 'Corporate Bond', 'ETF']:
            filtered_data = real_assets_df[
                (real_assets_df['MARKET_REGION'] == region) & 
                (real_assets_df['ASSET_CATEGORY'] == asset_class) &
                (real_assets_df['PRIMARY_TICKER'].notna())
            ]
            
            # Get target count for this combination
            target_key = f"{region}_{asset_class}".replace('/', '_').replace(' ', '_')
            target_count = target_counts.get(target_key, 100)  # Default to 100
            
            # Sample tickers up to target count
            sampled_tickers = filtered_data['PRIMARY_TICKER'].head(target_count).tolist()
            organized_tickers[region][asset_class] = sampled_tickers
            
            print(f"📊 {region} {asset_class}: {len(sampled_tickers)} real tickers")
    
    return organized_tickers

def extract_real_market_data(session: Session) -> bool:
    """
    Extract real daily OHLCV data for US securities from Snowflake Marketplace.
    
    Uses STOCK_PRICE_TIMESERIES table to get authentic market data for major US exchanges.
    Saves data to CSV for reuse without requiring Marketplace access.
    
    Args:
        session: Active Snowpark session with access to Marketplace data
        
    Returns:
        bool: True if extraction successful, False otherwise
    """
    
    print("📈 Extracting real market data from Snowflake Marketplace...")
    
    # First, load real assets to get the tickers we need market data for
    real_assets_df = load_real_assets_from_csv()
    if real_assets_df is None:
        print("❌ Need real assets CSV first. Run --extract-real-assets first.")
        return False
    
    # Get equity tickers for market data extraction (filter for valid ticker format)
    equity_data = real_assets_df[
        (real_assets_df['ASSET_CATEGORY'] == 'Equity') &
        (real_assets_df['PRIMARY_TICKER'].notna()) &
        (real_assets_df['PRIMARY_TICKER'].str.len() <= 6) &  # Reasonable ticker length
        (~real_assets_df['PRIMARY_TICKER'].str.contains(' ', na=False)) &  # No spaces (company names)
        (~real_assets_df['PRIMARY_TICKER'].str.startswith('BBG', na=False))  # No BBG IDs
    ]
    
    all_equities = equity_data['PRIMARY_TICKER'].head(100).tolist()  # Start with 100 for testing
    
    print(f"📊 Sample tickers to query: {all_equities[:10]}")  # Debug output
    
    if not all_equities:
        print("❌ No equity tickers found in real assets data")
        return False
    
    print(f"🎯 Extracting market data for {len(all_equities)} equity securities")
    
    # Create ticker list for SQL IN clause
    ticker_list = "'" + "','".join(all_equities) + "'"
    
    # Query to extract real market data (simplified for testing)
    market_data_query = f"""
    SELECT 
        TICKER,
        DATE,
        PRIMARY_EXCHANGE_CODE,
        PRIMARY_EXCHANGE_NAME,
        MAX(CASE WHEN VARIABLE = 'pre-market_open' THEN VALUE END) as OPEN_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_high' THEN VALUE END) as HIGH_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_low' THEN VALUE END) as LOW_PRICE,
        MAX(CASE WHEN VARIABLE = 'post-market_close' THEN VALUE END) as CLOSE_PRICE,
        MAX(CASE WHEN VARIABLE = 'nasdaq_volume' THEN VALUE END) as VOLUME
    FROM {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.STOCK_PRICE_TIMESERIES
    WHERE TICKER IN ({ticker_list})
      AND DATE >= DATEADD(year, -2, CURRENT_DATE())  -- Reduced to 2 years for testing
    GROUP BY TICKER, DATE, PRIMARY_EXCHANGE_CODE, PRIMARY_EXCHANGE_NAME
    HAVING 
        CLOSE_PRICE IS NOT NULL  -- Only require close price
    ORDER BY TICKER, DATE
    LIMIT 10000  -- Limit results for testing
    """
    
    try:
        # Execute the query to get real market data
        print("🔍 Querying STOCK_PRICE_TIMESERIES for real market data...")
        result_df = session.sql(market_data_query)
        
        # Convert to pandas for CSV export
        pandas_df = result_df.to_pandas()
        
        if len(pandas_df) == 0:
            print("⚠️ No market data found for the specified tickers and date range")
            return False
        
        # Create data directory if it doesn't exist
        market_data_path = config.REAL_MARKET_DATA_CSV_PATH
        os.makedirs(os.path.dirname(market_data_path), exist_ok=True)
        
        # Save to CSV
        pandas_df.to_csv(market_data_path, index=False)
        
        print(f"✅ Extracted {len(pandas_df):,} market data records to {market_data_path}")
        
        # Show summary statistics
        unique_tickers = pandas_df['TICKER'].nunique()
        date_range = f"{pandas_df['DATE'].min()} to {pandas_df['DATE'].max()}"
        exchanges = pandas_df['PRIMARY_EXCHANGE_NAME'].unique()
        
        print(f"\n📊 Real Market Data Summary:")
        print(f"  📈 Securities: {unique_tickers:,} unique tickers")
        print(f"  📅 Date Range: {date_range}")
        print(f"  🏛️ Exchanges: {', '.join(sorted(exchanges))}")
        
        # Show distribution by exchange
        exchange_dist = pandas_df.groupby('PRIMARY_EXCHANGE_NAME')['TICKER'].nunique().sort_values(ascending=False)
        print(f"\n📊 Securities by Exchange:")
        for exchange, count in exchange_dist.items():
            print(f"  {exchange}: {count:,} securities")
            
        return True
        
    except Exception as e:
        print(f"❌ Failed to extract real market data: {e}")
        print("Note: This requires access to FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.STOCK_PRICE_TIMESERIES")
        print("Ensure your account has the required Marketplace subscription")
        return False

def load_real_market_data_from_csv():
    """
    Load real market data from existing CSV file.
    
    Returns:
        pandas.DataFrame: Real market data or None if file doesn't exist
    """
    
    try:
        import pandas as pd
        
        if os.path.exists(config.REAL_MARKET_DATA_CSV_PATH):
            df = pd.read_csv(config.REAL_MARKET_DATA_CSV_PATH)
            df['DATE'] = pd.to_datetime(df['DATE'])  # Ensure proper date format
            print(f"✅ Loaded {len(df):,} real market data records from {config.REAL_MARKET_DATA_CSV_PATH}")
            
            # Show summary
            unique_tickers = df['TICKER'].nunique()
            date_range = f"{df['DATE'].min().date()} to {df['DATE'].max().date()}"
            print(f"  📈 {unique_tickers:,} securities, 📅 {date_range}")
            
            return df
        else:
            print(f"❌ Real market data CSV not found at {config.REAL_MARKET_DATA_CSV_PATH}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to load real market data CSV: {e}")
        return None
