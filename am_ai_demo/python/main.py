#!/usr/bin/env python3
"""
Snowcrest Asset Management (SAM) Demo - Main CLI Orchestrator

This script orchestrates the creation of the complete SAM demo environment,
including structured data generation, unstructured content creation, and AI component setup.

Usage:
    python main.py [--connection-name CONNECTION] [--scenarios SCENARIO_LIST] [--scope SCOPE]

Examples:
    python main.py                                    # Build everything with defaults
    python main.py --scenarios portfolio_copilot     # Build foundation + portfolio scenario
    python main.py --scope data                      # Build only data layer
    python main.py --connection-name my_demo         # Use specific connection
"""

import argparse
import sys
from typing import List, Optional

# Import configuration
from config import (
    DEFAULT_CONNECTION_NAME, 
    AVAILABLE_SCENARIOS,
    SCENARIO_DATA_REQUIREMENTS,
    DATABASE_NAME
)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Build Snowcrest Asset Management (SAM) AI Demo Environment'
    )
    
    parser.add_argument(
        '--connection-name',
        type=str,
        default=DEFAULT_CONNECTION_NAME,
        help=f'Snowflake connection name from ~/.snowflake/connections.toml (default: {DEFAULT_CONNECTION_NAME})'
    )
    
    parser.add_argument(
        '--scenarios',
        type=str,
        default='all',
        help='Comma-separated list of scenarios to build, or "all" for all scenarios (default: all)'
    )
    
    parser.add_argument(
        '--scope',
        type=str,
        choices=['all', 'data', 'semantic', 'search'],
        default='all',
        help='Scope of build: all=everything, data=structured+unstructured, semantic=views only, search=services only'
    )
    
    parser.add_argument(
        '--extract-real-assets',
        action='store_true',
        help='Extract real asset data from Snowflake Marketplace and save to CSV (requires marketplace access)'
    )
    parser.add_argument(
        '--extract-real-market-data',
        action='store_true',
        help='Extract real market data (OHLCV) from Snowflake Marketplace for US securities (requires marketplace access)'
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Use test mode with 10 percent of data for faster development testing (500 securities vs 5,000)'
    )
    
    return parser.parse_args()

def validate_scenarios(scenario_list: List[str]) -> List[str]:
    """Validate and return list of valid scenarios."""
    invalid_scenarios = [s for s in scenario_list if s not in AVAILABLE_SCENARIOS]
    if invalid_scenarios:
        print(f"❌ Invalid scenarios: {invalid_scenarios}")
        print(f"Available scenarios: {AVAILABLE_SCENARIOS}")
        sys.exit(1)
    
    return scenario_list

def get_required_document_types(scenarios: List[str]) -> List[str]:
    """Get unique list of document types required for the specified scenarios."""
    required_types = set()
    for scenario in scenarios:
        if scenario in SCENARIO_DATA_REQUIREMENTS:
            required_types.update(SCENARIO_DATA_REQUIREMENTS[scenario])
    return list(required_types)

def create_snowpark_session(connection_name: str):
    """Create and validate Snowpark session."""
    try:
        from snowflake.snowpark import Session
        
        print(f"🔗 Connecting to Snowflake using connection: {connection_name}")
        session = Session.builder.config("connection_name", connection_name).create()
        
        # Test connection
        result = session.sql("SELECT CURRENT_VERSION()").collect()
        print(f"✅ Connected successfully to Snowflake version: {result[0][0]}")
        
        # Create dedicated warehouses for the demo
        create_demo_warehouses(session)
        
        return session
        
    except ImportError:
        print("❌ Error: snowflake-snowpark-python not installed")
        print("Install with: pip install snowflake-snowpark-python")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print(f"Ensure ~/.snowflake/connections.toml is configured with connection '{connection_name}'")
        sys.exit(1)

def create_demo_warehouses(session):
    """Create dedicated warehouses for demo execution and Cortex Search services."""
    from config import EXECUTION_WAREHOUSE, CORTEX_SEARCH_WAREHOUSE, WAREHOUSE_SIZE
    
    try:
        print("🏗️ Creating demo warehouses...")
        
        # Create execution warehouse for data generation and code execution
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {EXECUTION_WAREHOUSE}
            WITH WAREHOUSE_SIZE = {WAREHOUSE_SIZE}
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            COMMENT = 'Warehouse for SAM demo data generation and execution'
        """).collect()
        print(f"✅ Created execution warehouse: {EXECUTION_WAREHOUSE}")
        
        # Create Cortex Search warehouse for search services
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {CORTEX_SEARCH_WAREHOUSE}
            WITH WAREHOUSE_SIZE = {WAREHOUSE_SIZE}
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            COMMENT = 'Warehouse for SAM demo Cortex Search services'
        """).collect()
        print(f"✅ Created Cortex Search warehouse: {CORTEX_SEARCH_WAREHOUSE}")
        
        # Set session to use execution warehouse by default
        session.use_warehouse(EXECUTION_WAREHOUSE)
        print(f"✅ Session configured to use: {EXECUTION_WAREHOUSE}")
        
    except Exception as e:
        print(f"⚠️ Warning: Failed to create warehouses: {e}")
        print("Continuing with existing warehouse from connection...")

def main():
    """Main execution function."""
    print("🏔️  Snowcrest Asset Management (SAM) Demo Builder")
    print("=" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    # Parse and validate scenarios
    if args.scenarios.lower() == 'all':
        scenario_list = AVAILABLE_SCENARIOS
    else:
        scenario_list = [s.strip() for s in args.scenarios.split(',')]
    validated_scenarios = validate_scenarios(scenario_list)
    
    print(f"📋 Building scenarios: {validated_scenarios}")
    print(f"🎯 Scope: {args.scope}")
    print(f"🔗 Connection: {args.connection_name}")
    if args.test_mode:
        print(f"🧪 Test Mode: Using 10% data volumes for faster development testing")
    print()
    
    # Create Snowpark session
    session = create_snowpark_session(args.connection_name)
    
    # Handle real asset extraction if requested
    if args.extract_real_assets:
        print("🌍 Extracting real asset data from Snowflake Marketplace...")
        import extract_real_assets
        success = extract_real_assets.extract_real_assets_to_csv(session)
        if success:
            print("✅ Real asset data extracted successfully")
            print("💡 To use real assets in future builds, set USE_REAL_ASSETS_CSV = True in config.py")
        else:
            print("❌ Real asset extraction failed - continuing with generated data")
        print()
        return  # Exit after extraction
    
    # Handle real market data extraction if requested
    if args.extract_real_market_data:
        print("📈 Extracting real market data from Snowflake Marketplace...")
        import extract_real_assets
        success = extract_real_assets.extract_real_market_data(session)
        if success:
            print("✅ Real market data extracted successfully")
            print("💡 Market data will be used automatically when USE_REAL_MARKET_DATA = True in config.py")
        else:
            print("❌ Real market data extraction failed - continuing with synthetic data")
        print()
        return  # Exit after extraction
    
    # Determine what to build based on scope
    build_data = args.scope in ['all', 'data']
    build_semantic = args.scope in ['all', 'semantic'] 
    build_search = args.scope in ['all', 'search']
    
    try:
        # Step 1: Build structured data (foundation + scenario-specific)
        if build_data:
            print("📊 Building structured data...")
            # Import and run structured data generation
            import generate_structured
            generate_structured.build_all(session, validated_scenarios, args.test_mode)
            
            print("📝 Building unstructured data...")
            # Import and run unstructured data generation
            import generate_unstructured
            required_doc_types = get_required_document_types(validated_scenarios)
            generate_unstructured.build_all(session, required_doc_types, args.test_mode)
        
        # Step 2: Build AI components
        if build_semantic or build_search:
            print("🤖 Building AI components...")
            import build_ai
            build_ai.build_all(session, validated_scenarios, build_semantic, build_search)
        
        print()
        print("🎉 SAM Demo Environment Build Complete!")
        print(f"📍 Database: {DATABASE_NAME}")
        print(f"🎭 Scenarios: {validated_scenarios}")
        print()
        print("Next steps:")
        print("1. Configure agents in Snowflake Intelligence (see docs/agents_setup.md)")
        print("2. Test demo scenarios (see docs/demo_scenarios.md)")
        print("3. Run validation checks (see docs/runbooks.md)")
        
    except ImportError as e:
        print(f"❌ Missing module: {e}")
        print("Ensure all required Python modules are created:")
        print("- python/generate_structured.py")
        print("- python/generate_unstructured.py") 
        print("- python/build_ai.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Build failed: {str(e)}")
        sys.exit(1)
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
