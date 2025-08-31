#!/usr/bin/env python3
"""
Primary orchestration script for setting up the complete Thematic Research Demo.
This is the main entry point that handles the entire demo setup process.
"""

import argparse
import sys
import time
import logging
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from generate_data import ThematicResearchDataGenerator, get_session
from config import DEFAULT_CONNECTION, DB_NAME

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_banner():
    """Print a welcome banner."""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║     SNOWFLAKE INTELLIGENCE - THEMATIC RESEARCH DEMO SETUP       ║
║                                                                  ║
║     Investment Research Assistant for Nordic Logistics          ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_step(step_num, total_steps, description):
    """Print a formatted step indicator."""
    print(f"\n[Step {step_num}/{total_steps}] {description}")
    print("-" * 60)

def main():
    """Main orchestration function."""
    parser = argparse.ArgumentParser(
        description="Complete setup for Thematic Research Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Setup with default connection
  python setup_demo.py
  
  # Setup with specific connection
  python setup_demo.py --connection my_connection
  
  # Quick mode (skip confirmations)
  python setup_demo.py --quick
  
  # Validate existing setup
  python setup_demo.py --validate-only
        """
    )
    
    parser.add_argument(
        "--connection",
        type=str,
        default=DEFAULT_CONNECTION,
        help=f"Snowflake connection name (default: {DEFAULT_CONNECTION})"
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip confirmation prompts and run immediately"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing setup without creating new data"
    )
    
    parser.add_argument(
        "--skip-objects",
        action="store_true",
        help="Skip creating Cortex Search and Semantic View (data only)"
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Show configuration
    print("\n📋 Configuration:")
    print(f"  • Connection: {args.connection}")
    print(f"  • Database: {DB_NAME}")
    print(f"  • Mode: {'Validation Only' if args.validate_only else 'Full Setup'}")
    
    if not args.quick and not args.validate_only:
        print("\n⚠️  This process will:")
        print("  1. Create/replace database and schemas")
        print("  2. Generate synthetic data using Cortex Complete")
        print("  3. Create Cortex Search services")
        print("  4. Create Semantic View for Cortex Analyst")
        print("  5. Validate the complete setup")
        print("\n  Estimated time: 10-15 minutes")
        
        response = input("\nDo you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Setup cancelled.")
            sys.exit(0)
    
    total_steps = 5 if not args.validate_only else 1
    current_step = 0
    
    try:
        # Connect to Snowflake
        current_step += 1
        if not args.validate_only:
            print_step(current_step, total_steps, "Connecting to Snowflake")
        
        session = get_session(args.connection)
        generator = ThematicResearchDataGenerator(session)
        
        if args.validate_only:
            # Validation only mode
            print_step(1, 1, "Validating Existing Setup")
            
            from data_validator import DataValidator
            from cortex_objects_creator import CortexObjectsCreator
            
            validator = DataValidator(session)
            cortex_creator = CortexObjectsCreator(session)
            
            # Validate data
            validation_results = validator.validate_all()
            generator._print_summary(validation_results)
            
            if not validation_results['success']:
                generator._print_validation_errors(validation_results)
                print("\n❌ Data validation failed")
            else:
                print("\n✅ Data validation passed")
            
            # Test SQL objects
            print("\nTesting Cortex Intelligence objects...")
            search_ok = cortex_creator.test_search_services()
            semantic_ok = cortex_creator.test_semantic_view()
            
            if search_ok and semantic_ok:
                print("✅ All SQL objects are functional")
            else:
                print("⚠️ Some SQL objects may need attention")
            
            sys.exit(0 if validation_results['success'] else 1)
        
        # Full setup mode
        current_step += 1
        print_step(current_step, total_steps, "Setting up Database")
        generator.setup_database()
        
        current_step += 1
        print_step(current_step, total_steps, "Generating Data")
        print("This will use Cortex Complete to generate realistic content...")
        
        # Generate structured data
        print("\n📊 Generating structured data...")
        companies_df = generator.structured_gen.generate_companies()
        macro_df = generator.structured_gen.generate_macroeconomic_data()
        financials_df = generator.structured_gen.generate_financials(companies_df)
        
        # Generate unstructured data
        print("\n📄 Generating unstructured data with Cortex Complete...")
        print("  • News articles (including Swedish content)")
        print("  • Expert interview transcripts")
        print("  • Consultant reports")
        print("  • Earnings call transcripts")
        print("  • Internal investment memos")
        generator.unstructured_gen.generate_all(companies_df)
        
        current_step += 1
        print_step(current_step, total_steps, "Creating Cortex Intelligence Objects")
        
        if not args.skip_objects:
            # Create Cortex Search services
            print("\n🔍 Creating Cortex Search services...")
            if not generator.cortex_creator.create_cortex_search_services():
                raise Exception("Failed to create Cortex Search services")
            
            # Create Semantic View
            print("\n📈 Creating Semantic View...")
            if not generator.cortex_creator.create_semantic_view():
                raise Exception("Failed to create Semantic View")
            
            print("\n⏳ Waiting for services to initialize...")
            time.sleep(5)
        else:
            print("Skipping SQL object creation (--skip-objects flag)")
        
        current_step += 1
        print_step(current_step, total_steps, "Validating Setup")
        
        # Run validation
        validation_results = generator.validator.validate_all()
        generator._print_summary(validation_results)
        
        if not validation_results['success']:
            generator._print_validation_errors(validation_results)
            raise Exception("Validation failed")
        
        # Test SQL objects if created
        if not args.skip_objects:
            print("\n🧪 Testing Cortex Intelligence objects...")
            search_test = generator.cortex_creator.test_search_services()
            semantic_test = generator.cortex_creator.test_semantic_view()
            
            if not (search_test and semantic_test):
                print("\n⚠️ Note: Some search services may need a few minutes to fully index")
                print("    You can re-run validation with: python setup_demo.py --validate-only")
        
        # Success!
        print("\n" + "="*70)
        print("🎉 DEMO SETUP COMPLETED SUCCESSFULLY!")
        print("="*70)
        
        print("\n📚 Next Steps:")
        print("\n1. Configure the Agent in Snowflake Intelligence:")
        print("   • Navigate to AI & ML → Snowflake Intelligence")
        print("   • Create new agent: THEMATIC_RESEARCH_AGENT")
        print("   • Follow: docs/agent_setup_instructions.md")
        
        print("\n2. Run the 4-step demo:")
        print("   Step 1: 'Summarize the impact of rising inflation on Nordic logistics companies.'")
        print("   Step 2: 'Compare gross margins over the last 6 quarters for the top 3 firms.'")
        print("   Step 3: 'Quote what management said about pricing power for Nordic Freight Systems.'")
        print("   Step 4: 'Do consultant reports and expert interviews agree with that narrative?'")
        
        print("\n3. Resources:")
        print("   • Agent setup: docs/agent_setup_instructions.md")
        print("   • Demo script: See README.md")
        print("   • Validation: python setup_demo.py --validate-only")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n❌ Setup failed: {str(e)}")
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
        
    finally:
        if 'session' in locals():
            session.close()
            logger.info("Session closed")

if __name__ == "__main__":
    main()
