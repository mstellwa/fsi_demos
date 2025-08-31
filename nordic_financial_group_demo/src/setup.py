#!/usr/bin/env python3
"""
Snowdrift Financials Multi-Phase Setup
Creates database foundation, schemas, and CONTROL framework for Insurance and Banking scenarios
"""

import yaml
import logging
from datetime import datetime
from typing import Dict, Any
from snowflake.snowpark import Session
from snowflake.snowpark.functions import current_timestamp
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, DateType, TimestampType, DoubleType, VariantType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SnowdriftSetup:
    """Snowdrift Financials Foundation Setup"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        """Initialize with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.connection_name = connection_name
        self.session = None
        
    def create_session(self) -> Session:
        """Create Snowpark session using ~/.snowflake/connections.toml"""
        logger.info(f"Creating Snowpark session with connection: {self.connection_name}")
        
        try:
            self.session = Session.builder.config("connection_name", self.connection_name).create()
            logger.info(f"Connected to: {self.session.get_current_account()}")
            return self.session
        except Exception as e:
            logger.error(f"Failed to create session: {str(e)}")
            logger.error("Ensure ~/.snowflake/connections.toml is configured properly")
            raise
    
    def setup_database_and_schemas(self):
        """Create database and schemas"""
        logger.info("Setting up database and schemas...")
        
        database = self.config['global']['database']
        
        # Create database if not exists
        self.session.sql(f"CREATE DATABASE IF NOT EXISTS {database}").collect()
        self.session.sql(f"USE DATABASE {database}").collect()
        logger.info(f"Database {database} created/confirmed")
        
        # Create schemas
        schemas = ['INSURANCE', 'INSURANCE_ANALYTICS', 'BANK', 'BANK_ANALYTICS', 'CONTROL']
        for schema in schemas:
            self.session.sql(f"CREATE OR REPLACE SCHEMA {schema}").collect()
            logger.info(f"Schema {schema} created/confirmed")
            
    def setup_control_framework(self):
        """Create CONTROL tables for configuration and prompt management"""
        logger.info("Setting up CONTROL framework...")
        
        self.session.sql("USE SCHEMA CONTROL").collect()
        
        # CONFIG table for configuration management
        config_schema = StructType([
            StructField("CONFIG_KEY", StringType(), nullable=False),
            StructField("CONFIG_VALUE", StringType(), nullable=True),
            StructField("SCOPE", StringType(), nullable=False),  # 'GLOBAL', 'INSURANCE', 'BANK', 'ASSET_MGMT'
            StructField("DESCRIPTION", StringType(), nullable=True),
            StructField("UPDATED_AT", TimestampType(), nullable=False)
        ])
        
        self.session.sql("""
            CREATE OR REPLACE TABLE CONFIG (
                CONFIG_KEY STRING NOT NULL,
                CONFIG_VALUE STRING,
                SCOPE STRING NOT NULL,
                DESCRIPTION STRING,
                UPDATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                PRIMARY KEY (CONFIG_KEY, SCOPE)
            )
        """).collect()
        
        # PROMPTS table for unstructured content generation
        self.session.sql("""
            CREATE OR REPLACE TABLE PROMPTS (
                PROMPT_ID STRING NOT NULL PRIMARY KEY,
                PROMPT_TYPE STRING NOT NULL,
                DOC_TYPE STRING,
                CLAIM_ID STRING,
                POLICY_ID STRING,
                MUNICIPALITY STRING,
                PROMPT_TEXT STRING NOT NULL,
                MODEL_TO_USE STRING NOT NULL,
                TEMPERATURE FLOAT,
                MAX_TOKENS INTEGER,
                SEED INTEGER,
                CREATED_AT NUMBER(16,0) NOT NULL,
                METADATA VARIANT
            )
        """).collect()
        
        # PROMPT_RUNS table for tracking generation lineage
        self.session.sql("""
            CREATE OR REPLACE TABLE PROMPT_RUNS (
                RUN_ID STRING NOT NULL PRIMARY KEY,
                PROMPT_ID STRING NOT NULL,
                MODEL_NAME STRING NOT NULL,
                TEMPERATURE FLOAT,
                MAX_TOKENS INTEGER,
                SEED INTEGER,
                INPUT_VARIABLES VARIANT,
                OUTPUT_IDS ARRAY,
                EXECUTION_TIME_SECONDS FLOAT,
                TOKENS_USED INTEGER,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (PROMPT_ID) REFERENCES PROMPTS(PROMPT_ID)
            )
        """).collect()
        
        logger.info("CONTROL framework tables created")
        
    def load_initial_config(self):
        """Load initial configuration from YAML into CONFIG table"""
        logger.info("Loading initial configuration...")
        
        self.session.sql("USE SCHEMA CONTROL").collect()
        
        # Prepare configuration records
        config_records = []
        
        # Global config
        global_config = self.config['global']
        for key, value in global_config.items():
            config_records.append((
                f"global.{key}",
                str(value),
                "GLOBAL",
                f"Global configuration: {key}",
                datetime.now()
            ))
        
        # Insurance config - flatten nested structure
        insurance_config = self.config['insurance']
        
        # Module settings
        config_records.append((
            "insurance.module_seed",
            str(insurance_config['module_seed']),
            "INSURANCE",
            "Insurance module seed for deterministic generation",
            datetime.now()
        ))
        
        # Structured data volumes
        structured = insurance_config['structured_data']
        for key, value in structured.items():
            config_records.append((
                f"insurance.structured_data.{key}",
                str(value),
                "INSURANCE",
                f"Structured data volume: {key}",
                datetime.now()
            ))
        
        # Unstructured data volumes
        unstructured = insurance_config['unstructured_data']
        for key, value in unstructured.items():
            config_records.append((
                f"insurance.unstructured_data.{key}",
                str(value),
                "INSURANCE",
                f"Unstructured data volume: {key}",
                datetime.now()
            ))
        
        # Content generation settings
        content_gen = insurance_config['content_generation']
        for key, value in content_gen.items():
            config_records.append((
                f"insurance.content_generation.{key}",
                str(value),
                "INSURANCE",
                f"Content generation setting: {key}",
                datetime.now()
            ))
        
        # Banking configuration (if available)
        banking_config = self.config.get('banking', {})
        if banking_config:
            # Banking module seed
            config_records.append((
                "banking.module_seed",
                str(banking_config.get('module_seed', 200)),
                "BANK",
                "Banking module seed for deterministic generation",
                datetime.now()
            ))
            
            # Banking structured data volumes
            structured_bank = banking_config.get('structured_data', {
                'customers_count': 25000,
                'accounts_per_customer': 4,
                'transactions_per_month': 150,
                'loans_count': 15000,
                'corporate_entities': 5000,
                'history_years': 3
            })
            for key, value in structured_bank.items():
                config_records.append((
                    f"banking.structured_data.{key}",
                    str(value),
                    "BANK",
                    f"Banking structured data volume: {key}",
                    datetime.now()
                ))
            
            # Banking unstructured data volumes
            unstructured_bank = banking_config.get('unstructured_data', {
                'economic_documents': 100,
                'compliance_documents': 75
            })
            for key, value in unstructured_bank.items():
                config_records.append((
                    f"banking.unstructured_data.{key}",
                    str(value),
                    "BANK",
                    f"Banking unstructured data volume: {key}",
                    datetime.now()
                ))
        
        # Create DataFrame and insert
        config_df = self.session.create_dataframe(
            config_records,
            schema=["CONFIG_KEY", "CONFIG_VALUE", "SCOPE", "DESCRIPTION", "UPDATED_AT"]
        )
        
        # Delete existing records and insert new ones
        self.session.sql("DELETE FROM CONFIG WHERE SCOPE IN ('GLOBAL', 'INSURANCE', 'BANK')").collect()
        
        # Use write_pandas as per our best practices
        config_pandas_df = config_df.to_pandas()
        result = self.session.write_pandas(
            config_pandas_df,
            "CONFIG",
            quote_identifiers=False,
            auto_create_table=False,
            overwrite=False
        )
        
        # Handle different return formats
        if isinstance(result, tuple) and len(result) >= 3:
            success = result[0]
            num_rows = result[2] if len(result) > 2 else len(config_pandas_df)
            if success:
                logger.info(f"✓ Loaded {num_rows} configuration records")
            else:
                logger.error(f"Failed to load configuration")
                raise Exception("Failed to load configuration")
        else:
            logger.info(f"✓ Configuration records loaded")
        
    def setup_insurance_tables(self):
        """Create Insurance schema structured tables"""
        logger.info("Setting up Insurance structured tables...")
        
        self.session.sql("USE SCHEMA INSURANCE").collect()
        
        # POLICIES table
        self.session.sql("""
            CREATE OR REPLACE TABLE POLICIES (
                POLICY_ID STRING NOT NULL PRIMARY KEY,
                CUSTOMER_ID STRING NOT NULL,
                POLICY_TYPE STRING NOT NULL DEFAULT 'PROPERTY',
                PREMIUM DECIMAL(12,2) NOT NULL,
                COVERAGE_AMOUNT DECIMAL(15,2) NOT NULL,
                EFFECTIVE_DATE DATE NOT NULL,
                EXPIRY_DATE DATE,
                STATUS STRING NOT NULL DEFAULT 'ACTIVE',
                ADDRESS_LINE1 STRING,
                CITY STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                COUNTRY STRING DEFAULT 'Norway',
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        # CLAIMS table  
        self.session.sql("""
            CREATE OR REPLACE TABLE CLAIMS (
                CLAIM_ID STRING NOT NULL PRIMARY KEY,
                POLICY_ID STRING NOT NULL,
                LOSS_DATE DATE NOT NULL,
                REPORTED_DATE DATE NOT NULL,
                DESCRIPTION STRING,
                STATUS STRING NOT NULL DEFAULT 'OPEN',
                CLAIM_AMOUNT DECIMAL(15,2),
                PAID_AMOUNT DECIMAL(15,2) DEFAULT 0,
                ADDRESS_LINE1 STRING,
                CITY STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                COUNTRY STRING DEFAULT 'Norway',
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (POLICY_ID) REFERENCES POLICIES(POLICY_ID)
            )
        """).collect()
        
        # GEO_RISK_SCORES table
        self.session.sql("""
            CREATE OR REPLACE TABLE GEO_RISK_SCORES (
                ADDRESS_KEY STRING NOT NULL PRIMARY KEY,
                ADDRESS_LINE1 STRING,
                CITY STRING,
                MUNICIPALITY STRING NOT NULL,
                POSTAL_CODE STRING NOT NULL,
                COUNTRY STRING DEFAULT 'Norway',
                FLOOD_RISK_SCORE INTEGER NOT NULL,
                RISK_FACTORS VARIANT,
                UPDATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        # BRREG_SNAPSHOT table (synthetic Norwegian business registry)
        self.session.sql("""
            CREATE OR REPLACE TABLE BRREG_SNAPSHOT (
                ORGANIZATION_NUMBER STRING NOT NULL PRIMARY KEY,
                COMPANY_NAME STRING NOT NULL,
                REGISTERED_ADDRESS STRING,
                CITY STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                BUSINESS_ACTIVITY_CODE STRING,
                BUSINESS_ACTIVITY_DESC STRING,
                REGISTRATION_DATE DATE,
                STATUS STRING DEFAULT 'ACTIVE',
                EMPLOYEE_COUNT INTEGER,
                ANNUAL_REVENUE DECIMAL(15,2),
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        logger.info("Insurance structured tables created")
    
    def setup_banking_tables(self):
        """Create Banking schema structured tables"""
        logger.info("Setting up Banking structured tables...")
        
        self.session.sql("USE SCHEMA BANK").collect()
        
        # CUSTOMERS table
        self.session.sql("""
            CREATE OR REPLACE TABLE CUSTOMERS (
                CUSTOMER_ID STRING NOT NULL PRIMARY KEY,
                FIRST_NAME STRING NOT NULL,
                LAST_NAME STRING NOT NULL,
                DOB DATE,
                NATIONAL_ID STRING UNIQUE,
                ADDRESS_LINE1 STRING,
                CITY STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                COUNTRY STRING DEFAULT 'Norway',
                PHONE STRING,
                EMAIL STRING,
                CUSTOMER_SINCE DATE NOT NULL,
                STATUS STRING NOT NULL DEFAULT 'ACTIVE',
                INSURANCE_POLICY_ID STRING,  -- Cross-reference to Insurance
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        # ACCOUNTS table
        self.session.sql("""
            CREATE OR REPLACE TABLE ACCOUNTS (
                ACCOUNT_ID STRING NOT NULL PRIMARY KEY,
                CUSTOMER_ID STRING NOT NULL,
                ACCOUNT_TYPE STRING NOT NULL DEFAULT 'CHECKING',  -- CHECKING, SAVINGS, MORTGAGE, LOAN
                BALANCE DECIMAL(15,2) NOT NULL DEFAULT 0,
                INTEREST_RATE DECIMAL(5,4) DEFAULT 0,
                OPENED_DATE DATE NOT NULL,
                STATUS STRING NOT NULL DEFAULT 'ACTIVE',
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID)
            )
        """).collect()
        
        # TRANSACTIONS table
        self.session.sql("""
            CREATE OR REPLACE TABLE TRANSACTIONS (
                TRANSACTION_ID STRING NOT NULL PRIMARY KEY,
                ACCOUNT_ID STRING NOT NULL,
                TRANSACTION_DATE DATE NOT NULL,
                AMOUNT DECIMAL(12,2) NOT NULL,
                TRANSACTION_TYPE STRING NOT NULL DEFAULT 'DEBIT',  -- DEBIT, CREDIT
                MERCHANT_NAME STRING,
                MERCHANT_CATEGORY STRING,  -- GROCERY, FUEL, UTILITIES, HEALTHCARE, etc.
                DESCRIPTION STRING,
                BALANCE_AFTER DECIMAL(15,2),
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (ACCOUNT_ID) REFERENCES ACCOUNTS(ACCOUNT_ID)
            )
        """).collect()
        
        # LOANS table
        self.session.sql("""
            CREATE OR REPLACE TABLE LOANS (
                LOAN_ID STRING NOT NULL PRIMARY KEY,
                CUSTOMER_ID STRING NOT NULL,
                LOAN_TYPE STRING NOT NULL DEFAULT 'MORTGAGE',  -- MORTGAGE, PERSONAL, AUTO
                PRINCIPAL_AMOUNT DECIMAL(15,2) NOT NULL,
                CURRENT_BALANCE DECIMAL(15,2) NOT NULL,
                INTEREST_RATE DECIMAL(5,4) NOT NULL,
                TERM_MONTHS INTEGER NOT NULL,
                ORIGINATED_DATE DATE NOT NULL,
                MATURITY_DATE DATE NOT NULL,
                STATUS STRING NOT NULL DEFAULT 'ACTIVE',
                PROPERTY_ADDRESS STRING,  -- For mortgages
                PROPERTY_MUNICIPALITY STRING,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID)
            )
        """).collect()
        
        # BRREG_CORPORATE table (Norwegian business registry for corporate customers)
        self.session.sql("""
            CREATE OR REPLACE TABLE BRREG_CORPORATE (
                ORGANIZATION_NUMBER STRING NOT NULL PRIMARY KEY,
                COMPANY_NAME STRING NOT NULL,
                REGISTERED_ADDRESS STRING,
                CITY STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                BUSINESS_ACTIVITY_CODE STRING,
                BUSINESS_ACTIVITY_DESC STRING,
                REGISTRATION_DATE DATE,
                STATUS STRING NOT NULL DEFAULT 'ACTIVE',
                EMPLOYEE_COUNT INTEGER,
                ANNUAL_REVENUE DECIMAL(15,2),
                BENEFICIAL_OWNERS VARIANT,  -- JSON array of beneficial ownership info
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        # ECONOMIC_DOCUMENTS table
        self.session.sql("""
            CREATE OR REPLACE TABLE ECONOMIC_DOCUMENTS (
                DOC_ID STRING NOT NULL PRIMARY KEY,
                TITLE STRING NOT NULL,
                DOC_TYPE STRING NOT NULL,  -- HOUSING_REPORT, EMPLOYMENT_DATA, MARKET_ANALYSIS
                MUNICIPALITY STRING,
                REGION STRING,
                CONTENT_MD STRING,  -- Markdown content
                KEYWORDS STRING,
                MODEL_USED STRING,
                GENERATION_TIMESTAMP TIMESTAMP_NTZ,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        # COMPLIANCE_DOCUMENTS table
        self.session.sql("""
            CREATE OR REPLACE TABLE COMPLIANCE_DOCUMENTS (
                DOC_ID STRING NOT NULL PRIMARY KEY,
                TITLE STRING NOT NULL,
                DOC_TYPE STRING NOT NULL,  -- KYC_REPORT, AML_ASSESSMENT, BENEFICIAL_OWNERSHIP
                ORGANIZATION_NUMBER STRING,
                COMPANY_NAME STRING,
                CONTENT_MD STRING,  -- Markdown content
                KEYWORDS STRING,
                MODEL_USED STRING,
                GENERATION_TIMESTAMP TIMESTAMP_NTZ,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        logger.info("Banking structured tables created")
        
    def setup_unstructured_tables(self):
        """Create tables for unstructured documents (Markdown storage)"""
        logger.info("Setting up unstructured document tables...")
        
        self.session.sql("USE SCHEMA INSURANCE").collect()
        
        # Claims documents table
        self.session.sql("""
            CREATE OR REPLACE TABLE CLAIMS_DOCUMENTS (
                ID STRING NOT NULL PRIMARY KEY,
                TITLE STRING NOT NULL,
                DOC_TYPE STRING NOT NULL, -- 'POLICE_REPORT', 'MEDICAL_REPORT', 'WITNESS_STATEMENT', 'PHOTO_REPORT'
                CLAIM_ID STRING NOT NULL,
                EVENT_DATE DATE,
                SOURCE STRING,
                LANGUAGE STRING DEFAULT 'English',
                CONTENT_MD STRING NOT NULL, -- Markdown content
                DOC_META VARIANT,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP(),
                FOREIGN KEY (CLAIM_ID) REFERENCES CLAIMS(CLAIM_ID)
            )
        """).collect()
        
        # Underwriting documents table
        self.session.sql("""
            CREATE OR REPLACE TABLE UNDERWRITING_DOCUMENTS (
                ID STRING NOT NULL PRIMARY KEY,
                TITLE STRING NOT NULL,
                DOC_TYPE STRING NOT NULL, -- 'RISK_BRIEF', 'FLOOD_ADVISORY', 'ENVIRONMENTAL_NEWS', 'INDUSTRY_REPORT'
                COMPANY_NAME STRING,
                ADDRESS_LINE1 STRING,
                MUNICIPALITY STRING,
                POSTAL_CODE STRING,
                REPORT_DATE DATE,
                SOURCE STRING,
                LANGUAGE STRING DEFAULT 'English',
                CONTENT_MD STRING NOT NULL, -- Markdown content
                DOC_META VARIANT,
                CREATED_AT TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
        logger.info("Unstructured document tables created")
        
    def run_setup(self):
        """Execute complete foundation setup"""
        logger.info("Starting Snowdrift Financials setup...")
        
        try:
            # Create session
            self.create_session()
            
            # Setup database and schemas
            self.setup_database_and_schemas()
            
            # Setup CONTROL framework
            self.setup_control_framework()
            
            # Load initial configuration
            self.load_initial_config()
            
            # Setup Insurance tables
            self.setup_insurance_tables()
            
            # Setup Banking tables
            self.setup_banking_tables()
            
            # Setup unstructured tables
            self.setup_unstructured_tables()
            
            logger.info("Foundation setup completed successfully!")
            logger.info("Ready for data generation")
            
        except Exception as e:
            logger.error(f"Setup failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Snowdrift Financials Setup")
    parser.add_argument("--connection", default="default", help="Connection name from ~/.snowflake/connections.toml")
    args = parser.parse_args()
    
    setup = SnowdriftSetup(connection_name=args.connection)
    setup.run_setup()

if __name__ == "__main__":
    main()
