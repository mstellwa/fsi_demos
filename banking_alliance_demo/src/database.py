"""
Database schema management for SnowBank Intelligence Demo
Creates and manages all required tables and database objects
"""

import logging
from typing import List, Dict
from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException

from .config import DemoConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database schema creation and maintenance"""
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
    
    def create_schema(self) -> None:
        """Create complete database schema"""
        logger.info("Creating database schema...")
        
        # Set up warehouse if available
        try:
            warehouse = self.config.get_config('WAREHOUSE_FOR_BUILD')
            self.session.sql(f"USE WAREHOUSE {warehouse}").collect()
            logger.info(f"Using warehouse: {warehouse}")
        except Exception as e:
            logger.warning(f"Could not set warehouse: {str(e)}")
        
        # Create database and schema
        try:
            self.session.sql("CREATE DATABASE IF NOT EXISTS FSI_DEMOS").collect()
            self.session.sql("USE DATABASE FSI_DEMOS").collect()
            logger.info("Using database: FSI_DEMOS")
        except Exception as e:
            logger.warning(f"Could not create/use database FSI_DEMOS: {str(e)}")
        
        # Create or replace schema
        self.session.sql("CREATE SCHEMA IF NOT EXISTS BANK_DEMO").collect()
        self.session.sql("USE SCHEMA BANK_DEMO").collect()
        logger.info("Using schema: BANK_DEMO")
        
        # Create all tables
        self._create_member_banks_table()
        self._create_customers_table()
        self._create_loans_table()
        self._create_financials_table()
        self._create_alliance_performance_table()
        self._create_market_data_table()
        self._create_document_prompts_table()
        self._create_documents_table()
        self._create_demo_config_table()
        self._create_run_registry_table()
        
        logger.info("Database schema created successfully")
    
    def _create_member_banks_table(self) -> None:
        """Create MEMBER_BANKS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE MEMBER_BANKS (
                MEMBER_BANK_ID VARCHAR NOT NULL PRIMARY KEY,
                BANK_NAME VARCHAR NOT NULL,
                REGION VARCHAR NOT NULL,
                TOTAL_ASSETS NUMBER(38,2) NOT NULL
            )
        """).collect()
        
    def _create_customers_table(self) -> None:
        """Create CUSTOMERS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE CUSTOMERS (
                CUSTOMER_ID VARCHAR NOT NULL PRIMARY KEY,
                MEMBER_BANK_ID VARCHAR NOT NULL,
                CUSTOMER_NAME VARCHAR NOT NULL,
                CUSTOMER_TYPE VARCHAR NOT NULL,
                INDUSTRY_SECTOR VARCHAR NOT NULL,
                GEOGRAPHIC_REGION VARCHAR NOT NULL,
                CREDIT_SCORE_ORIGINATION INT NOT NULL,
                FOREIGN KEY (MEMBER_BANK_ID) REFERENCES MEMBER_BANKS(MEMBER_BANK_ID)
            )
        """).collect()
        
    def _create_loans_table(self) -> None:
        """Create LOANS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE LOANS (
                LOAN_ID VARCHAR NOT NULL PRIMARY KEY,
                CUSTOMER_ID VARCHAR NOT NULL,
                MEMBER_BANK_ID VARCHAR NOT NULL,
                LOAN_TYPE VARCHAR NOT NULL,
                OUTSTANDING_BALANCE NUMBER(38,2) NOT NULL,
                INTEREST_RATE FLOAT NOT NULL,
                ORIGINATION_DATE DATE NOT NULL,
                MATURITY_DATE DATE NOT NULL,
                PROPERTY_VALUE_ORIGINATION NUMBER(38,2),
                CURRENT_PROPERTY_VALUE NUMBER(38,2),
                LOAN_TO_VALUE_RATIO FLOAT,
                GREEN_BOND_FRAMEWORK_TAG BOOLEAN DEFAULT FALSE,
                GREEN_PROJECT_CATEGORY VARCHAR,
                LAST_CREDIT_REVIEW_DATE DATE,
                FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID),
                FOREIGN KEY (MEMBER_BANK_ID) REFERENCES MEMBER_BANKS(MEMBER_BANK_ID)
            )
        """).collect()
        
    def _create_financials_table(self) -> None:
        """Create FINANCIALS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE FINANCIALS (
                RECORD_ID VARCHAR NOT NULL PRIMARY KEY,
                CUSTOMER_ID VARCHAR NOT NULL,
                MEMBER_BANK_ID VARCHAR NOT NULL,
                RECORD_TYPE VARCHAR NOT NULL,
                RECORD_DATE DATE NOT NULL,
                AMOUNT NUMBER(38,2) NOT NULL,
                FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMERS(CUSTOMER_ID),
                FOREIGN KEY (MEMBER_BANK_ID) REFERENCES MEMBER_BANKS(MEMBER_BANK_ID)
            )
        """).collect()
        
    def _create_alliance_performance_table(self) -> None:
        """Create ALLIANCE_PERFORMANCE table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE ALLIANCE_PERFORMANCE (
                REPORTING_YEAR INT NOT NULL,
                MEMBER_BANK_ID VARCHAR NOT NULL,
                SMB_LENDING_GROWTH_PCT FLOAT NOT NULL,
                COST_INCOME_RATIO FLOAT NOT NULL,
                PRIMARY KEY (REPORTING_YEAR, MEMBER_BANK_ID),
                FOREIGN KEY (MEMBER_BANK_ID) REFERENCES MEMBER_BANKS(MEMBER_BANK_ID)
            )
        """).collect()
        
    def _create_market_data_table(self) -> None:
        """Create MARKET_DATA table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE MARKET_DATA (
                TICKER VARCHAR NOT NULL,
                TRADE_DATE DATE NOT NULL,
                CLOSE_PRICE NUMBER(38,2) NOT NULL,
                COMPANY_NAME VARCHAR NOT NULL,
                PEER_GROUP VARCHAR NOT NULL,
                PRIMARY KEY (TICKER, TRADE_DATE)
            )
        """).collect()
        
    def _create_document_prompts_table(self) -> None:
        """Create DOCUMENT_PROMPTS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE DOCUMENT_PROMPTS (
                DOC_ID VARCHAR NOT NULL PRIMARY KEY,
                SCENARIO VARCHAR NOT NULL,
                DOC_TYPE VARCHAR NOT NULL,
                TARGET_ENTITY VARCHAR NOT NULL,
                PROMPT_TEXT VARCHAR NOT NULL,
                MODEL_CLASS VARCHAR NOT NULL,
                TEMPERATURE FLOAT NOT NULL,
                CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                STATUS VARCHAR DEFAULT 'PENDING'
            )
        """).collect()
        
    def _create_documents_table(self) -> None:
        """Create DOCUMENTS table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE DOCUMENTS (
                DOC_ID VARCHAR NOT NULL PRIMARY KEY,
                SCENARIO VARCHAR NOT NULL,
                DOC_TYPE VARCHAR NOT NULL,
                TITLE VARCHAR NOT NULL,
                TARGET_ENTITY VARCHAR NOT NULL,
                CONTENT_MD VARCHAR NOT NULL,
                MODEL_CLASS VARCHAR NOT NULL,
                CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """).collect()
        
    def _create_demo_config_table(self) -> None:
        """Create DEMO_CONFIG table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE DEMO_CONFIG (
                KEY VARCHAR NOT NULL PRIMARY KEY,
                VALUE VARCHAR NOT NULL
            )
        """).collect()
        
    def _create_run_registry_table(self) -> None:
        """Create RUN_REGISTRY table"""
        self.session.sql("""
            CREATE OR REPLACE TABLE RUN_REGISTRY (
                RUN_ID VARCHAR NOT NULL,
                STEP VARCHAR NOT NULL,
                PARAMS VARIANT,
                ROWS_WRITTEN NUMBER,
                STARTED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                ENDED_AT TIMESTAMP_NTZ,
                STATUS VARCHAR DEFAULT 'RUNNING',
                PRIMARY KEY (RUN_ID, STEP)
            )
        """).collect()
    
    def reset_demo_data(self) -> None:
        """Reset all demo data by truncating tables"""
        logger.info("Resetting demo data...")
        
        # Tables to truncate (in reverse dependency order)
        tables_to_truncate = [
            'RUN_REGISTRY',
            'DOCUMENTS', 
            'DOCUMENT_PROMPTS',
            'MARKET_DATA',
            'ALLIANCE_PERFORMANCE',
            'FINANCIALS',
            'LOANS',
            'CUSTOMERS',
            'MEMBER_BANKS'
        ]
        
        for table in tables_to_truncate:
            try:
                self.session.sql(f"TRUNCATE TABLE {table}").collect()
                logger.info(f"Truncated table: {table}")
            except SnowparkSQLException as e:
                logger.warning(f"Could not truncate {table}: {str(e)}")
        
        logger.info("Demo data reset completed")
    
    def get_table_counts(self) -> Dict[str, int]:
        """Get row counts for all tables"""
        tables = [
            'MEMBER_BANKS', 'CUSTOMERS', 'LOANS', 'FINANCIALS',
            'ALLIANCE_PERFORMANCE', 'MARKET_DATA', 'DOCUMENT_PROMPTS',
            'DOCUMENTS', 'DEMO_CONFIG', 'RUN_REGISTRY'
        ]
        
        counts = {}
        for table in tables:
            try:
                result = self.session.sql(f"SELECT COUNT(*) AS cnt FROM {table}").collect()
                counts[table] = result[0]['CNT'] if result else 0
            except SnowparkSQLException:
                counts[table] = 0
                
        return counts
