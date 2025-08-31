#!/usr/bin/env python3
"""
Snowdrift Financials - Main Entry Point
Complete setup and data generation for multi-division financial services demo
Supports scenario-based generation: insurance, bank, asset_management, or all
"""

import argparse
import sys
import logging
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from setup import SnowdriftSetup
from generate_data import NorwegianDataGenerator
from create_semantic_view import SemanticViewCreator
from generate_documents import DocumentGenerator
from create_search_services import SearchServiceCreator

# Import Banking generators
try:
    from generate_banking_data import NorwegianBankingDataGenerator
    from generate_banking_documents import BankingDocumentGenerator
    BANKING_AVAILABLE = True
except ImportError:
    BANKING_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Scenario definitions
SCENARIOS = {
    'insurance': {
        'name': 'Insurance (Phase 1)',
        'description': 'Property P&C and Commercial Property insurance with claims and underwriting',
        'dependencies': []
    },
    'bank': {
        'name': 'Banking (Phase 2)', 
        'description': 'Retail and Corporate Banking with customer 360 and cross-division integration',
        'dependencies': ['insurance']  # Banking needs insurance data for cross-references
    },
    'asset_management': {
        'name': 'Asset Management (Phase 3)',
        'description': 'Investment and ESG management with portfolio analytics',
        'dependencies': ['insurance', 'bank']  # Asset mgmt needs high-net-worth banking customers
    },
    'all': {
        'name': 'All Scenarios',
        'description': 'Complete multi-division financial services ecosystem',
        'dependencies': []
    }
}

def check_scenario_dependencies(scenario: str, connection_name: str) -> bool:
    """Check if scenario dependencies are met"""
    if scenario == 'all' or not SCENARIOS[scenario]['dependencies']:
        return True
    
    logger.info(f"Checking dependencies for {scenario}...")
    
    try:
        from setup import SnowdriftSetup
        setup = SnowdriftSetup(connection_name=connection_name)
        session = setup.create_session()
        session.sql("USE DATABASE SNOWDRIFT_FINANCIALS").collect()
        
        for dep in SCENARIOS[scenario]['dependencies']:
            if dep == 'insurance':
                # Check if insurance data exists
                result = session.sql("SELECT COUNT(*) as cnt FROM INSURANCE.POLICIES").collect()
                if result[0]['CNT'] == 0:
                    logger.error(f"❌ Dependency check failed: {scenario} requires insurance data")
                    logger.error("   Run: python main.py --scenario insurance --step all")
                    return False
                logger.info(f"✓ Insurance dependency satisfied ({result[0]['CNT']} policies)")
                
            elif dep == 'bank':
                # Check if banking data exists
                result = session.sql("SELECT COUNT(*) as cnt FROM BANK.CUSTOMERS").collect()
                if result[0]['CNT'] == 0:
                    logger.error(f"❌ Dependency check failed: {scenario} requires banking data")
                    logger.error("   Run: python main.py --scenario bank --step all")
                    return False
                logger.info(f"✓ Banking dependency satisfied ({result[0]['CNT']} customers)")
        
        session.close()
        return True
        
    except Exception as e:
        logger.warning(f"⚠ Could not verify dependencies for {scenario}: {str(e)}")
        return True  # Proceed anyway

def run_setup(scenarios: list, connection_name: str = "default"):
    """Run foundation setup for specified scenarios"""
    logger.info(f"=== Foundation Setup for scenarios: {', '.join(scenarios)} ===")
    
    # Setup always runs for all requested scenarios together
    setup = SnowdriftSetup(connection_name=connection_name)
    setup.run_setup()
    logger.info("Foundation setup completed successfully!")

def run_data_generation(scenarios: list, connection_name: str = "default"):
    """Run data generation for specified scenarios"""
    logger.info(f"=== Data Generation for scenarios: {', '.join(scenarios)} ===")
    
    for scenario in scenarios:
        if scenario == 'insurance':
            logger.info("Generating Insurance data...")
            
            # Step 1: Generate structured insurance data
            logger.info("Step 1: Generating insurance structured data...")
            generator = NorwegianDataGenerator(connection_name=connection_name)
            generator.run_data_generation()
            
            # Step 2: Generate insurance documents
            logger.info("Step 2: Generating insurance documents...")
            doc_generator = DocumentGenerator(connection_name=connection_name)
            doc_generator.run_document_generation()
            
        elif scenario == 'bank':
            if not BANKING_AVAILABLE:
                logger.error("❌ Banking generators not available - missing generate_banking_data.py or generate_banking_documents.py")
                continue
                
            logger.info("Generating Banking data...")
            
            # Check dependencies
            if not check_scenario_dependencies('bank', connection_name):
                logger.error("❌ Banking data generation requires insurance data")
                continue
            
            # Step 1: Generate structured banking data
            logger.info("Step 1: Generating banking structured data...")
            banking_generator = NorwegianBankingDataGenerator(connection_name=connection_name)
            banking_generator.run_banking_data_generation()
            
            # Step 2: Generate banking documents
            logger.info("Step 2: Generating banking documents...")
            banking_doc_generator = BankingDocumentGenerator(connection_name=connection_name)
            banking_doc_generator.run_banking_document_generation()
            
        elif scenario == 'asset_management':
            logger.info("Asset Management data generation not yet implemented")
            logger.info("This will be implemented in Phase 3")
            
    logger.info("Data generation completed successfully!")

def run_semantic_view(scenarios: list, connection_name: str = "default"):
    """Run semantic view creation for specified scenarios"""
    logger.info(f"=== Semantic View Creation for scenarios: {', '.join(scenarios)} ===")
    
    # Use the enhanced semantic view creator that handles both Insurance and Banking
    creator = SemanticViewCreator(connection_name=connection_name)
    creator.run_semantic_view_creation()
    logger.info("Semantic view creation completed successfully!")

def run_documents(scenarios: list, connection_name: str = "default"):
    """Run document generation for specified scenarios"""
    logger.info(f"=== Document Generation for scenarios: {', '.join(scenarios)} ===")
    
    for scenario in scenarios:
        if scenario == 'insurance':
            logger.info("Generating Insurance documents...")
            doc_generator = DocumentGenerator(connection_name=connection_name)
            doc_generator.run_document_generation()
            
        elif scenario == 'bank':
            if not BANKING_AVAILABLE:
                logger.error("❌ Banking document generator not available")
                continue
                
            logger.info("Generating Banking documents...")
            banking_doc_generator = BankingDocumentGenerator(connection_name=connection_name)
            banking_doc_generator.run_banking_document_generation()
            
        elif scenario == 'asset_management':
            logger.info("Asset Management document generation not yet implemented")
            
    logger.info("Document generation completed successfully!")

def run_search_services(scenarios: list, connection_name: str = "default"):
    """Run Cortex Search services creation for specified scenarios"""
    logger.info(f"=== Search Services Creation for scenarios: {', '.join(scenarios)} ===")
    
    # Use the enhanced search service creator that handles all scenarios
    creator = SearchServiceCreator(connection_name=connection_name)
    creator.run_search_service_creation()
    logger.info("Search services creation completed successfully!")

def run_scenario_setup(scenarios: list, steps: list, connection_name: str = "default"):
    """Run complete setup for specified scenarios and steps"""
    scenario_names = [SCENARIOS[s]['name'] for s in scenarios]
    logger.info(f"=== Running Snowdrift Financials Setup ===")
    logger.info(f"Scenarios: {', '.join(scenario_names)}")
    logger.info(f"Steps: {', '.join(steps)}")
    
    try:
        # Step 1: Foundation setup (if requested)
        if 'setup' in steps:
            logger.info("Starting M1 - Foundation Setup...")
            run_setup(scenarios, connection_name)
        
        # Step 2: Data generation (if requested)
        if 'data' in steps:
            logger.info("Starting M2/M4 - Data Generation...")
            run_data_generation(scenarios, connection_name)
        
        # Step 3: Semantic view creation (if requested)
        if 'semantic' in steps:
            logger.info("Starting M3 - Semantic View Creation...")
            run_semantic_view(scenarios, connection_name)
        
        # Step 4: Document generation (if requested and not done in data step)
        if 'documents' in steps:
            logger.info("Starting M4 - Document Generation...")
            run_documents(scenarios, connection_name)
        
        # Step 5: Search services creation (if requested)
        if 'search' in steps:
            logger.info("Starting M5 - Search Services Creation...")
            run_search_services(scenarios, connection_name)
        
        logger.info("🎉 Snowdrift Financials setup completed successfully!")
        logger.info(f"✓ Scenarios completed: {', '.join(scenario_names)}")
        logger.info(f"✓ Steps completed: {', '.join(steps)}")
        logger.info("👉 Next: Configure agents in Snowsight using AGENT_SETUP_GUIDE.md")
        
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        raise

def main():
    """Main entry point with scenario-based command line interface"""
    parser = argparse.ArgumentParser(
        description="Snowdrift Financials - Multi-Division Financial Services Demo Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scenario-Based Examples:
  python main.py --scenario all --step all                    # Complete setup (all divisions)
  python main.py --scenario insurance --step all              # Insurance only (Phase 1)
  python main.py --scenario bank --step all                   # Banking only (Phase 2) 
  python main.py --scenario asset_management --step all       # Asset Management only (Phase 3)
  
  python main.py --scenario bank --step data                  # Banking data only
  python main.py --scenario insurance --step search           # Insurance search services only
  python main.py --scenario all --step semantic               # All semantic views
  
  python main.py --scenario bank --connection myconn          # Use specific connection

Available Scenarios:
  insurance        - Property P&C and Commercial Property insurance (Phase 1)
  bank            - Retail and Corporate Banking with cross-division integration (Phase 2)
  asset_management - Investment and ESG management (Phase 3 - not yet implemented)
  all             - Complete multi-division ecosystem
        """
    )
    parser.add_argument(
        "--scenario", 
        choices=["insurance", "bank", "asset_management", "all"], 
        default="all",
        help="Scenario to setup: insurance, bank, asset_management, or all (default: all)"
    )
    parser.add_argument(
        "--step", 
        choices=["setup", "data", "semantic", "documents", "search", "all"], 
        default="all",
        help="Setup step to run: setup, data, semantic, documents, search, or all (default: all)"
    )
    parser.add_argument(
        "--connection", 
        default="default",
        help="Connection name from ~/.snowflake/connections.toml (default: default)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Determine scenarios to run
    if args.scenario == 'all':
        scenarios = ['insurance', 'bank', 'asset_management']
    else:
        scenarios = [args.scenario]
    
    # Determine steps to run
    if args.step == 'all':
        steps = ['setup', 'data', 'semantic', 'search']
    else:
        steps = [args.step]
    
    # Validate scenario availability
    for scenario in scenarios:
        if scenario == 'bank' and not BANKING_AVAILABLE:
            logger.error("❌ Banking scenario not available - missing banking generators")
            logger.error("   Ensure generate_banking_data.py and generate_banking_documents.py exist")
            sys.exit(1)
        elif scenario == 'asset_management':
            logger.warning("⚠ Asset Management scenario not yet implemented (Phase 3)")
            if len(scenarios) == 1:  # Only asset_management requested
                logger.info("Asset Management will be implemented in Phase 3")
                sys.exit(0)
            else:  # Remove from scenarios list if part of 'all'
                scenarios.remove('asset_management')
    
    # Show scenario information
    logger.info(f"Starting Snowdrift Financials setup:")
    logger.info(f"  Scenarios: {', '.join(scenarios)}")
    logger.info(f"  Steps: {', '.join(steps)}")
    logger.info(f"  Connection: {args.connection}")
    
    for scenario in scenarios:
        info = SCENARIOS[scenario]
        logger.info(f"  {scenario}: {info['description']}")
        if info['dependencies']:
            logger.info(f"    Dependencies: {', '.join(info['dependencies'])}")
    
    try:
        run_scenario_setup(scenarios, steps, args.connection)
        
        # Provide helpful next steps based on what was run
        logger.info("\n🎯 NEXT STEPS:")
        
        if 'all' in steps or 'search' in steps:
            logger.info("1. Run validation: python validate_agent_readiness.py")
            logger.info("2. Configure agents in Snowsight using AGENT_SETUP_GUIDE.md")
        elif 'setup' in steps:
            logger.info(f"Run data generation: python main.py --scenario {args.scenario} --step data")
        elif 'data' in steps:
            logger.info(f"Run semantic views: python main.py --scenario {args.scenario} --step semantic")
        elif 'semantic' in steps:
            logger.info(f"Run search services: python main.py --scenario {args.scenario} --step search")
        elif 'documents' in steps:
            logger.info(f"Run search services: python main.py --scenario {args.scenario} --step search")
            
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()