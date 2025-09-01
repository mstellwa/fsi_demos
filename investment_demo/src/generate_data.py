#!/usr/bin/env python3
"""
Main data generation script for the Thematic Research Demo.
Generates both structured and unstructured data using Snowpark and Cortex Complete.
"""

import argparse
import sys
from datetime import datetime, timedelta
import random
import numpy as np
from typing import Dict, List, Optional
import logging

from snowflake.snowpark import Session
from snowflake.snowpark.types import *
from snowflake.snowpark.functions import col, lit, udf, call_function
import pandas as pd
from faker import Faker

from config import *
from structured_data_generator import StructuredDataGenerator
from unstructured_data_generator import UnstructuredDataGenerator
from data_validator import DataValidator
from cortex_objects_creator import CortexObjectsCreator
from warehouse_setup import WarehouseSetup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ThematicResearchDataGenerator:
    """Main orchestrator for generating demo data."""
    
    def __init__(self, session: Session):
        self.session = session
        self.faker = Faker(['en_US', 'sv_SE'])
        self.faker.seed_instance(RANDOM_SEED)
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)
        
        self.warehouse_setup = WarehouseSetup(session)
        self.structured_gen = StructuredDataGenerator(session)
        self.unstructured_gen = UnstructuredDataGenerator(session)
        self.validator = DataValidator(session)
        self.cortex_creator = CortexObjectsCreator(session)
        
    def setup_database(self):
        """Create warehouses, database and schemas if they don't exist."""
        
        # Create warehouses first
        logger.info("Setting up warehouses")
        self.warehouse_setup.create_warehouses()
        
        logger.info(f"Setting up database {DB_NAME}")
        
        # Create database
        self.session.sql(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}").collect()
        self.session.sql(f"USE DATABASE {DB_NAME}").collect()
        
        # Create schemas
        self.session.sql(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA}").collect()
        self.session.sql(f"CREATE SCHEMA IF NOT EXISTS {ANALYTICS_SCHEMA}").collect()
        
        # Set default schema
        self.session.sql(f"USE SCHEMA {RAW_SCHEMA}").collect()
        
        logger.info("Database setup complete")
        
    def generate_all_data(self, create_objects=True):
        """Generate all data for the demo and optionally create SQL objects.
        
        Args:
            create_objects: If True, also create Cortex Search services and Semantic View
        """
        try:
            # Setup database
            self.setup_database()
            
            # Generate structured data
            logger.info("Generating structured data...")
            companies_df = self.structured_gen.generate_companies()
            macro_df = self.structured_gen.generate_macroeconomic_data()
            financials_df = self.structured_gen.generate_financials(companies_df)
            
            # Generate unstructured data
            logger.info("Generating unstructured data...")
            self.unstructured_gen.generate_all(companies_df)
            
            # Validate data
            logger.info("Validating generated data...")
            validation_results = self.validator.validate_all()
            
            if validation_results['success']:
                logger.info("✅ All data generated and validated successfully!")
                self._print_summary(validation_results)
            else:
                logger.error("❌ Data validation failed!")
                self._print_validation_errors(validation_results)
                return False
            
            # Create SQL objects if requested
            if create_objects:
                logger.info("\n" + "="*60)
                logger.info("CREATING CORTEX INTELLIGENCE OBJECTS")
                logger.info("="*60)
                
                # Create Cortex Search services
                if self.cortex_creator.create_cortex_search_services():
                    logger.info("✅ Cortex Search services created")
                else:
                    logger.error("❌ Failed to create Cortex Search services")
                    return False
                
                # Create Semantic View
                if self.cortex_creator.create_semantic_view():
                    logger.info("✅ Semantic View created")
                else:
                    logger.error("❌ Failed to create Semantic View")
                    return False
                
                # Test the services
                logger.info("\nTesting created objects...")
                search_test = self.cortex_creator.test_search_services()
                semantic_test = self.cortex_creator.test_semantic_view()
                
                if search_test and semantic_test:
                    logger.info("✅ All objects tested successfully")
                else:
                    logger.warning("⚠️ Some tests failed - services may need time to index")
                
            return True
            
        except Exception as e:
            logger.error(f"Error during data generation: {str(e)}")
            raise
            
    def _print_summary(self, validation_results: Dict):
        """Print a summary of generated data."""
        print("\n" + "="*60)
        print("DATA GENERATION SUMMARY")
        print("="*60)
        
        print("\n📊 Structured Data:")
        print(f"  • Companies: {validation_results['companies_count']}")
        print(f"  • Financial quarters: {validation_results['quarters_count']}")
        print(f"  • Macro indicators: {validation_results['macro_months']}")
        
        print("\n📄 Unstructured Data:")
        print(f"  • News articles: {validation_results['news_count']}")
        print(f"    - Swedish articles: {validation_results['swedish_news_count']}")
        print(f"  • Expert transcripts: {validation_results['expert_count']}")
        print(f"  • Consultant reports: {validation_results['consultant_count']}")
        print(f"  • Earnings calls: {validation_results['earnings_count']}")
        print(f"  • Internal memos: {validation_results['memos_count']}")
        
        print("\n✅ Nordic Freight Systems Validation:")
        print(f"  • Earnings calls: {validation_results['nfs_earnings_count']} quarters")
        print(f"  • Has pricing power quotes: {validation_results['nfs_has_pricing_quotes']}")
        
        print("\n🎯 Demo Readiness:")
        for i, prompt_ready in enumerate(validation_results['demo_prompts_ready'], 1):
            status = "✅" if prompt_ready else "❌"
            print(f"  {status} Demo prompt {i} can be answered")
            
        print("="*60 + "\n")
        
    def _print_validation_errors(self, validation_results: Dict):
        """Print validation errors."""
        print("\n" + "="*60)
        print("VALIDATION ERRORS")
        print("="*60)
        
        for error in validation_results.get('errors', []):
            print(f"  ❌ {error}")
            
        print("="*60 + "\n")

def get_session(connection_name: str) -> Session:
    """Create and return a Snowpark session."""
    try:
        logger.info(f"Connecting to Snowflake using connection: {connection_name}")
        
        # Build session using connection name from connections.toml
        session = Session.builder.config("connection_name", connection_name).create()
        
        # Don't set warehouse here - it will be created and set in setup_database()
        # Just test the basic connection
        result = session.sql("SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()").collect()
        logger.info(f"Connected as: {result[0][0]}, Role: {result[0][1]}, Warehouse: {result[0][2]}")
        
        return session
        
    except Exception as e:
        logger.error(f"Failed to connect to Snowflake: {str(e)}")
        raise

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate synthetic data for the Thematic Research Demo"
    )
    parser.add_argument(
        "--connection",
        type=str,
        default=DEFAULT_CONNECTION,
        help=f"Connection name from connections.toml (default: {DEFAULT_CONNECTION})"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing data without generating new data"
    )
    parser.add_argument(
        "--skip-objects",
        action="store_true",
        help="Skip creating Cortex Search services and Semantic View"
    )
    
    args = parser.parse_args()
    
    try:
        # Get Snowflake session
        session = get_session(args.connection)
        
        # Create generator
        generator = ThematicResearchDataGenerator(session)
        
        if args.validate_only:
            # Just validate existing data
            logger.info("Running validation only...")
            validator = DataValidator(session)
            validation_results = validator.validate_all()
            generator._print_summary(validation_results)
            if not validation_results['success']:
                generator._print_validation_errors(validation_results)
                sys.exit(1)
        else:
            # Generate all data (and create objects unless skipped)
            create_objects = not args.skip_objects
            success = generator.generate_all_data(create_objects=create_objects)
            if not success:
                sys.exit(1)
                
        logger.info("\n" + "="*60)
        logger.info("SETUP COMPLETED SUCCESSFULLY!")
        logger.info("="*60)
        logger.info("\nNext steps:")
        logger.info("1. Configure the Agent in Snowflake Intelligence")
        logger.info("2. Follow instructions in docs/agent_setup_instructions.md")
        logger.info("3. Run the 4-step demo with the prompts from the documentation")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
        
    finally:
        if 'session' in locals():
            session.close()
            logger.info("Session closed")

if __name__ == "__main__":
    main()
