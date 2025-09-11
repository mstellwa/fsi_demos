#!/usr/bin/env python3
# setup.py
# Main setup script for Frost Markets Intelligence Demo

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.snowpark_session import get_snowpark_session, create_demo_warehouses, set_demo_context, close_session
from config import DemoConfig


def create_database_schema(session):
    """Execute schema creation SQL"""
    print("\n🏗️  Creating database schemas...")
    
    try:
        # Create database first
        print("   📊 Creating database...")
        session.sql("CREATE DATABASE IF NOT EXISTS MARKETS_AI_DEMO COMMENT = 'Frost Markets Intelligence - Snowflake AI Demo Database'").collect()
        
        # Set database context
        print("   🏗️  Setting database context...")
        session.sql("USE DATABASE MARKETS_AI_DEMO").collect()
        
        # Create schemas
        print("   📁 Creating schemas...")
        session.sql("CREATE SCHEMA IF NOT EXISTS RAW_DATA COMMENT = 'Raw structured and unstructured data for demo scenarios'").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS ENRICHED_DATA COMMENT = 'AI-enriched data from Document AI and Cortex functions'").collect()
        session.sql("CREATE SCHEMA IF NOT EXISTS ANALYTICS COMMENT = 'Semantic views, search services, and analytical objects'").collect()
        
        # Set default context
        print("   🎯 Setting default context...")
        session.sql("USE SCHEMA RAW_DATA").collect()
        session.sql(f"USE WAREHOUSE {DemoConfig.COMPUTE_WAREHOUSE}").collect()
        
        print("✅ Database schemas created successfully")
        
    except Exception as e:
        print(f"❌ Error creating schemas: {str(e)}")
        # Try to show what went wrong
        try:
            current_db = session.get_current_database()
            print(f"   Current database: {current_db}")
        except:
            print("   Could not determine current database")
        raise


def generate_data(session, mode):
    """Generate all demo data"""
    print(f"\n📊 Generating demo data (mode: {mode})...")
    
    try:
        # Import data generation modules
        from data_generation.event_log import generate_master_event_log
        from data_generation.structured_data import generate_all_structured_data
        from data_generation.unstructured_data import generate_all_unstructured_data
        
        # Generate master event log first (drives all correlations)
        print("  🎯 Generating master event log...")
        generate_master_event_log(session)
        
        # Generate structured data
        print("  📈 Generating structured data...")
        generate_all_structured_data(session)
        
        # Generate unstructured data using Cortex
        print("  📄 Generating unstructured data with Cortex...")
        generate_all_unstructured_data(session)
        
        print("✅ Demo data generated successfully")
        
    except Exception as e:
        print(f"❌ Error generating data: {str(e)}")
        raise


def create_ai_components(session, mode):
    """Create Snowflake AI components"""
    print(f"\n🤖 Creating AI components (mode: {mode})...")
    
    try:
        from ai_components.semantic_views import create_all_semantic_views
        from ai_components.search_services import create_all_search_services
        
        # Create semantic views
        print("  🔍 Creating semantic views...")
        create_all_semantic_views(session)
        
        # Create search services
        print("  🔎 Creating search services...")
        create_all_search_services(session)
        
        print("✅ AI components created successfully")
        
    except Exception as e:
        print(f"❌ Error creating AI components: {str(e)}")
        raise


def validate_setup(session):
    """Basic validation of the demo setup"""
    print("\n✅ Validating demo setup...")
    
    try:
        from utils.validation import validate_all_components
        validate_all_components(session)
        print("✅ Demo validation completed successfully")
        
    except Exception as e:
        print(f"⚠️  Validation warnings: {str(e)}")


def main():
    """Main setup function with mode options"""
    parser = argparse.ArgumentParser(description="Frost Markets Intelligence Demo Setup")
    parser.add_argument(
        "--mode", 
        choices=["full", "data-only", "ai-only", "scenario-specific"],
        default="full",
        help="Setup mode: full setup, data only, AI components only, or specific scenario"
    )
    parser.add_argument(
        "--scenario",
        choices=DemoConfig.PHASE_1_SCENARIOS + DemoConfig.PHASE_2_SCENARIOS,
        help="Specific scenario to setup (requires --mode=scenario-specific)"
    )
    parser.add_argument(
        "--connection_name",
        default=DemoConfig.SNOWFLAKE_CONNECTION_NAME,
        help="Connection name from connections.toml"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation step"
    )
    
    args = parser.parse_args()
    
    print("🏔️  Frost Markets Intelligence Demo Setup")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    if args.scenario:
        print(f"Scenario: {args.scenario}")
    print(f"Connection: {args.connection_name}")
    print()
    
    session = None
    try:
        # Create Snowpark session
        session = get_snowpark_session(args.connection_name)
        
        # Create warehouses first (required for all operations)
        create_demo_warehouses(session)
        
        # Execute setup based on mode
        if args.mode in ["full", "data-only"]:
            create_database_schema(session)
            set_demo_context(session)
            generate_data(session, args.mode)
            
        if args.mode in ["full", "ai-only"]:
            if args.mode == "ai-only":
                set_demo_context(session)
            create_ai_components(session, args.mode)
            
        if args.mode == "scenario-specific":
            if not args.scenario:
                print("❌ --scenario required when using --mode=scenario-specific")
                sys.exit(1)
            # TODO: Implement scenario-specific setup
            print(f"🎯 Setting up scenario: {args.scenario}")
            
        # Validation
        if not args.skip_validation:
            from utils.validation import validate_all_components
            validate_all_components(session)
            
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Open Snowsight and navigate to Snowflake Intelligence")
        print("   2. Configure agents using templates in src/ai_components/agents.py")
        print("   3. Test demo scenarios")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)
        
    finally:
        if session:
            close_session(session)


if __name__ == "__main__":
    main()
