"""
Structured data generators for SnowBank Intelligence Demo
Generates synthetic Norwegian banking data using Snowpark DataFrames
"""

import logging
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random

from faker import Faker
from snowflake.snowpark import DataFrame
from snowflake.snowpark.functions import col, lit, current_timestamp
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, BooleanType, DecimalType

from .config import DemoConfig

logger = logging.getLogger(__name__)

# Norwegian-specific data
NORWEGIAN_REGIONS = ['Helgeland', 'Østlandet', 'Trøndelag', 'Vestlandet', 'Nord-Norge']
INDUSTRY_SECTORS = ['Aquaculture', 'Renewable Energy', 'Maritime', 'Real Estate Development', 'Technology Services', 'Tourism & Hospitality', 'Oil & Gas Services']
NORWEGIAN_COMPANY_PREFIXES = ['Helio', 'Nordlys', 'Bergen', 'Trondheim', 'Stavanger', 'Lofoten', 'Sunnmøre', 'Finnmark']
COMPANY_SUFFIXES = ['AS', 'ASA', 'Holding AS', 'Services AS', 'Technology AS']

# Key demo companies that must exist in structured data (matching document prompts)
DEMO_SEED_COMPANIES = [
    {"name": "Helio Salmon AS", "type": "Corporate", "industry": "Aquaculture", "region": "Helgeland"},
    {"name": "Bergen Maritime Services AS", "type": "Corporate", "industry": "Maritime", "region": "Vestlandet"},
    {"name": "Nordlys Renewable Energy ASA", "type": "Corporate", "industry": "Renewable Energy", "region": "Trøndelag"},
    {"name": "Trondheim Tech Solutions AS", "type": "Corporate", "industry": "Technology Services", "region": "Trøndelag"},
    {"name": "Lofoten Tourism Holdings AS", "type": "Corporate", "industry": "Tourism & Hospitality", "region": "Nordland"},
    {"name": "Stavanger Oil Services AS", "type": "Corporate", "industry": "Oil & Gas Services", "region": "Vestlandet"},
    {"name": "Finnmark Aquaculture AS", "type": "Corporate", "industry": "Aquaculture", "region": "Nord-Norge"},
    {"name": "Sunnmøre Shipping AS", "type": "Corporate", "industry": "Maritime", "region": "Vestlandet"},
    # Additional Helgeland aquaculture companies for realistic peer comparison
    {"name": "Helgeland Marine Farms AS", "type": "Corporate", "industry": "Aquaculture", "region": "Helgeland"},
    {"name": "Arctic Salmon Holdings AS", "type": "Corporate", "industry": "Aquaculture", "region": "Helgeland"},
    {"name": "Nordkyst Aquaculture AS", "type": "Corporate", "industry": "Aquaculture", "region": "Helgeland"},
    {"name": "Helgeland Fish Company AS", "type": "Corporate", "industry": "Aquaculture", "region": "Helgeland"},
]
LOAN_TYPES = ['Residential Mortgage', 'Commercial Real Estate', 'Corporate Term Loan', 'Working Capital', 'Equipment Finance', 'Green Bond']
GREEN_PROJECT_CATEGORIES = ['Renewable Energy', 'Green Buildings', 'Clean Transportation', 'Sustainable Aquaculture', 'Energy Efficiency']


class StructuredDataGenerator:
    """Generates synthetic structured data for all demo tables"""
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
        self.fake = Faker('no_NO')  # Norwegian locale
        self.fake.seed_instance(42)  # For reproducible data
        random.seed(42)
        
    def generate_all_data(self) -> None:
        """Generate all structured data"""
        logger.info("Starting structured data generation...")
        
        run_id = str(uuid.uuid4())
        
        # Generate data in dependency order
        self._log_run_start(run_id, "member_banks")
        member_banks = self.generate_member_banks()
        self._log_run_end(run_id, "member_banks", member_banks.count())
        
        self._log_run_start(run_id, "customers")
        customers = self.generate_customers(member_banks)
        self._log_run_end(run_id, "customers", customers.count())
        
        self._log_run_start(run_id, "loans")
        loans = self.generate_loans(customers)
        self._log_run_end(run_id, "loans", loans.count())
        
        self._log_run_start(run_id, "financials")
        financials = self.generate_financials(customers)
        self._log_run_end(run_id, "financials", financials.count())
        
        self._log_run_start(run_id, "alliance_performance")
        alliance_perf = self.generate_alliance_performance(member_banks)
        self._log_run_end(run_id, "alliance_performance", alliance_perf.count())
        
        self._log_run_start(run_id, "market_data")
        market_data = self.generate_market_data()
        self._log_run_end(run_id, "market_data", market_data.count())
        
        # Initialize config
        self.config.initialize_config_table()
        
        logger.info("Structured data generation completed")
    
    def generate_member_banks(self) -> DataFrame:
        """Generate member banks data"""
        logger.info("Generating member banks...")
        
        banks_data = []
        for i in range(1, 6):  # 5 member banks
            bank_id = f"BANK_{i:03d}"
            region = NORWEGIAN_REGIONS[i-1]
            bank_name = f"Nordic Bank {region}"
            total_assets = random.uniform(50_000_000_000, 200_000_000_000)  # 50B to 200B NOK
            
            banks_data.append((bank_id, bank_name, region, total_assets))
        
        # Create DataFrame
        schema = StructType([
            StructField("MEMBER_BANK_ID", StringType()),
            StructField("BANK_NAME", StringType()),
            StructField("REGION", StringType()),
            StructField("TOTAL_ASSETS", DecimalType(38, 2))
        ])
        
        df = self.session.create_dataframe(banks_data, schema)
        df.write.mode("overwrite").save_as_table("MEMBER_BANKS")
        
        logger.info(f"Generated {len(banks_data)} member banks")
        return df
    
    def generate_customers(self, member_banks_df: DataFrame) -> DataFrame:
        """Generate customers data with Norwegian characteristics"""
        logger.info("Generating customers...")
        
        customer_count = self.config.get_config('CUSTOMER_COUNT')
        customers_data = []
        
        # Get member bank IDs
        bank_ids = [row['MEMBER_BANK_ID'] for row in member_banks_df.collect()]
        bank_regions = {row['MEMBER_BANK_ID']: row['REGION'] for row in member_banks_df.collect()}
        
        # First, add demo seed companies (guaranteed to exist for demo scenarios)
        logger.info(f"Adding {len(DEMO_SEED_COMPANIES)} demo seed companies...")
        for i, seed_company in enumerate(DEMO_SEED_COMPANIES, 1):
            customer_id = f"DEMO_{i:06d}"
            
            # Find a bank in the appropriate region, fallback to random
            matching_banks = [bid for bid, region in bank_regions.items() if region == seed_company["region"]]
            member_bank_id = random.choice(matching_banks) if matching_banks else random.choice(bank_ids)
            
            customers_data.append((
                customer_id, member_bank_id, seed_company["name"], seed_company["type"],
                seed_company["industry"], seed_company["region"], 
                random.randint(650, 850)  # High credit score for demo companies
            ))
        
        # Then generate random customers
        logger.info(f"Generating {customer_count} random customers...")
        for i in range(1, customer_count + 1):
            customer_id = f"CUST_{i:06d}"
            member_bank_id = random.choice(bank_ids)
            customer_region = bank_regions[member_bank_id]
            
            # Generate Norwegian-style company name
            if random.random() < 0.3:  # 30% individual customers
                customer_name = self.fake.name()
                customer_type = "Individual"
                industry_sector = "Personal Banking"
            else:  # 70% corporate customers
                prefix = random.choice(NORWEGIAN_COMPANY_PREFIXES)
                industry = random.choice(INDUSTRY_SECTORS)
                suffix = random.choice(COMPANY_SUFFIXES)
                customer_name = f"{prefix} {industry} {suffix}"
                customer_type = "Corporate"
                industry_sector = industry
            
            # Geographic concentration logic
            if industry_sector == "Aquaculture" and customer_region != "Helgeland":
                if random.random() < 0.7:  # 70% chance to move to Helgeland
                    customer_region = "Helgeland"
            elif industry_sector == "Technology Services" and customer_region not in ["Østlandet", "Trøndelag"]:
                if random.random() < 0.6:  # 60% chance to move to tech regions
                    customer_region = random.choice(["Østlandet", "Trøndelag"])
            elif industry_sector == "Maritime" and customer_region != "Vestlandet":
                if random.random() < 0.6:  # 60% chance to move to Vestlandet
                    customer_region = "Vestlandet"
            
            credit_score = random.randint(300, 850)
            
            customers_data.append((
                customer_id, member_bank_id, customer_name, customer_type,
                industry_sector, customer_region, credit_score
            ))
        
        # Create DataFrame
        schema = StructType([
            StructField("CUSTOMER_ID", StringType()),
            StructField("MEMBER_BANK_ID", StringType()),
            StructField("CUSTOMER_NAME", StringType()),
            StructField("CUSTOMER_TYPE", StringType()),
            StructField("INDUSTRY_SECTOR", StringType()),
            StructField("GEOGRAPHIC_REGION", StringType()),
            StructField("CREDIT_SCORE_ORIGINATION", IntegerType())
        ])
        
        df = self.session.create_dataframe(customers_data, schema)
        df.write.mode("overwrite").save_as_table("CUSTOMERS")
        
        logger.info(f"Generated {len(customers_data)} customers")
        return df
    
    def _generate_loan_data(self, loan_id, customer_id, member_bank_id, industry_sector, customer_type, start_date, end_date):
        """Helper method to generate a single loan record"""
        # Loan type based on customer type and industry
        if customer_type == "Individual":
            loan_type = "Residential Mortgage"
        else:
            if industry_sector in ["Real Estate Development"]:
                loan_type = "Commercial Real Estate"
            elif industry_sector in ["Renewable Energy", "Aquaculture"]:
                loan_type = random.choice(["Corporate Term Loan", "Green Bond"])
            else:
                loan_type = random.choice(["Corporate Term Loan", "Working Capital", "Equipment Finance"])
        
        # Loan amount based on type and industry
        # Special handling for Helgeland aquaculture demo companies to ensure similar exposure levels
        # Based on DEMO_SEED_COMPANIES order: DEMO_000001=Helio, DEMO_000009-000012=new Helgeland aquaculture
        helgeland_aquaculture_demo_ids = ["DEMO_000001", "DEMO_000009", "DEMO_000010", "DEMO_000011", "DEMO_000012"]
        
        if (customer_id in helgeland_aquaculture_demo_ids and industry_sector == "Aquaculture"):
            # Create similar exposure levels to Helio Salmon AS (target: 400M-900M NOK total)
            if loan_type in ["Commercial Real Estate", "Green Bond"]:
                outstanding_balance = random.uniform(150_000_000, 450_000_000)  # 150M-450M NOK per loan
            else:
                outstanding_balance = random.uniform(80_000_000, 200_000_000)  # 80M-200M NOK per loan
        elif loan_type == "Residential Mortgage":
            outstanding_balance = random.uniform(1_000_000, 8_000_000)  # 1-8M NOK
        elif loan_type in ["Commercial Real Estate", "Green Bond"]:
            outstanding_balance = random.uniform(10_000_000, 500_000_000)  # 10M-500M NOK
        else:
            outstanding_balance = random.uniform(2_000_000, 100_000_000)  # 2M-100M NOK
        
        # Interest rate
        base_rate = 3.5  # Norwegian base rate approximation
        credit_spread = random.uniform(0.5, 4.0)
        interest_rate = base_rate + credit_spread
        
        # Dates
        origination_date = self.fake.date_between(start_date=start_date, end_date=end_date)
        maturity_years = random.choice([5, 7, 10, 15, 20, 25, 30])
        maturity_date = origination_date + timedelta(days=maturity_years * 365)
        
        # Property values (for real estate loans)
        property_value_origination = None
        current_property_value = None
        loan_to_value_ratio = None
        
        if loan_type in ["Residential Mortgage", "Commercial Real Estate"]:
            property_value_origination = outstanding_balance / random.uniform(0.6, 0.9)
            # Property appreciation/depreciation
            appreciation_rate = random.uniform(-0.1, 0.15)  # -10% to +15%
            current_property_value = property_value_origination * (1 + appreciation_rate)
            loan_to_value_ratio = outstanding_balance / current_property_value
        
        # Green bond framework
        green_bond_framework_tag = False
        green_project_category = None
        
        if (loan_type == "Green Bond" or 
            (industry_sector in ["Renewable Energy", "Aquaculture"] and random.random() < 0.25)):
            green_bond_framework_tag = True
            if industry_sector == "Renewable Energy":
                green_project_category = "Renewable Energy"
            elif industry_sector == "Aquaculture":
                green_project_category = "Sustainable Aquaculture"
            else:
                green_project_category = random.choice(GREEN_PROJECT_CATEGORIES)
        
        # Last credit review
        last_review_date = self.fake.date_between(
            start_date=origination_date,
            end_date=min(end_date, origination_date + timedelta(days=365))
        )
        
        return (
            loan_id, customer_id, member_bank_id, loan_type,
            outstanding_balance, interest_rate, origination_date, maturity_date,
            property_value_origination, current_property_value, loan_to_value_ratio,
            green_bond_framework_tag, green_project_category, last_review_date
        )
    
    def generate_loans(self, customers_df: DataFrame) -> DataFrame:
        """Generate loans data with green bonds and Norwegian market characteristics"""
        logger.info("Generating loans...")
        
        loan_count = self.config.get_config('LOAN_COUNT')
        history_months = self.config.get_config('HISTORY_MONTHS')
        loans_data = []
        
        # Get customer data
        customers = customers_df.collect()
        demo_customers = [c for c in customers if c['CUSTOMER_ID'].startswith('DEMO_')]
        regular_customers = [c for c in customers if not c['CUSTOMER_ID'].startswith('DEMO_')]
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=history_months * 30)
        
        loan_counter = 1
        
        # First, ensure each demo company gets 2-3 loans for realistic exposure
        logger.info(f"Generating guaranteed loans for {len(demo_customers)} demo companies...")
        for demo_customer in demo_customers:
            num_loans = random.randint(2, 3)  # Each demo company gets 2-3 loans
            for _ in range(num_loans):
                loan_id = f"LOAN_{loan_counter:08d}"
                customer = demo_customer
                customer_id = customer['CUSTOMER_ID']
                member_bank_id = customer['MEMBER_BANK_ID']
                industry_sector = customer['INDUSTRY_SECTOR']
                customer_type = customer['CUSTOMER_TYPE']
                
                # Generate loan for this demo customer
                loan_data = self._generate_loan_data(
                    loan_id, customer_id, member_bank_id, industry_sector, 
                    customer_type, start_date, end_date
                )
                loans_data.append(loan_data)
                loan_counter += 1
        
        # Then generate remaining loans randomly
        remaining_loans = loan_count - len(loans_data)
        logger.info(f"Generating {remaining_loans} additional random loans...")
        for i in range(remaining_loans):
            loan_id = f"LOAN_{loan_counter:08d}"
            customer = random.choice(customers)
            customer_id = customer['CUSTOMER_ID']
            member_bank_id = customer['MEMBER_BANK_ID']
            industry_sector = customer['INDUSTRY_SECTOR']
            customer_type = customer['CUSTOMER_TYPE']
            
            # Generate loan using helper method
            loan_data = self._generate_loan_data(
                loan_id, customer_id, member_bank_id, industry_sector, 
                customer_type, start_date, end_date
            )
            loans_data.append(loan_data)
            loan_counter += 1
        
        # Create DataFrame
        schema = StructType([
            StructField("LOAN_ID", StringType()),
            StructField("CUSTOMER_ID", StringType()),
            StructField("MEMBER_BANK_ID", StringType()),
            StructField("LOAN_TYPE", StringType()),
            StructField("OUTSTANDING_BALANCE", DecimalType(38, 2)),
            StructField("INTEREST_RATE", FloatType()),
            StructField("ORIGINATION_DATE", DateType()),
            StructField("MATURITY_DATE", DateType()),
            StructField("PROPERTY_VALUE_ORIGINATION", DecimalType(38, 2)),
            StructField("CURRENT_PROPERTY_VALUE", DecimalType(38, 2)),
            StructField("LOAN_TO_VALUE_RATIO", FloatType()),
            StructField("GREEN_BOND_FRAMEWORK_TAG", BooleanType()),
            StructField("GREEN_PROJECT_CATEGORY", StringType()),
            StructField("LAST_CREDIT_REVIEW_DATE", DateType())
        ])
        
        df = self.session.create_dataframe(loans_data, schema)
        df.write.mode("overwrite").save_as_table("LOANS")
        
        logger.info(f"Generated {len(loans_data)} loans")
        return df
    
    def generate_financials(self, customers_df: DataFrame) -> DataFrame:
        """Generate financial records (fees, revenues, etc.)"""
        logger.info("Generating financials...")
        
        customers = customers_df.collect()
        history_months = self.config.get_config('HISTORY_MONTHS')
        financials_data = []
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=history_months * 30)
        
        record_types = ['FEE_REVENUE', 'INTEREST_INCOME', 'COMMISSION', 'TRADING_INCOME']
        
        for customer in customers:
            customer_id = customer['CUSTOMER_ID']
            member_bank_id = customer['MEMBER_BANK_ID']
            customer_type = customer['CUSTOMER_TYPE']
            
            # Generate monthly records
            current_date = start_date
            while current_date <= end_date:
                for record_type in record_types:
                    if random.random() < 0.7:  # 70% chance of having this record type
                        record_id = str(uuid.uuid4())
                        
                        # Amount based on customer type and record type
                        if customer_type == "Individual":
                            if record_type == "FEE_REVENUE":
                                amount = random.uniform(100, 2000)
                            elif record_type == "INTEREST_INCOME":
                                amount = random.uniform(5000, 25000)
                            else:
                                amount = random.uniform(50, 1000)
                        else:  # Corporate
                            if record_type == "FEE_REVENUE":
                                amount = random.uniform(5000, 50000)
                            elif record_type == "INTEREST_INCOME":
                                amount = random.uniform(50000, 500000)
                            else:
                                amount = random.uniform(1000, 25000)
                        
                        financials_data.append((
                            record_id, customer_id, member_bank_id,
                            record_type, current_date, amount
                        ))
                
                # Next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
        
        # Create DataFrame
        schema = StructType([
            StructField("RECORD_ID", StringType()),
            StructField("CUSTOMER_ID", StringType()),
            StructField("MEMBER_BANK_ID", StringType()),
            StructField("RECORD_TYPE", StringType()),
            StructField("RECORD_DATE", DateType()),
            StructField("AMOUNT", DecimalType(38, 2))
        ])
        
        df = self.session.create_dataframe(financials_data, schema)
        df.write.mode("overwrite").save_as_table("FINANCIALS")
        
        logger.info(f"Generated {len(financials_data)} financial records")
        return df
    
    def generate_alliance_performance(self, member_banks_df: DataFrame) -> DataFrame:
        """Generate alliance performance metrics"""
        logger.info("Generating alliance performance...")
        
        member_banks = member_banks_df.collect()
        performance_data = []
        
        # Generate for last 3 years
        current_year = datetime.now().year
        for year in range(current_year - 2, current_year + 1):
            for bank in member_banks:
                member_bank_id = bank['MEMBER_BANK_ID']
                
                # SMB lending growth (varying performance)
                if member_bank_id == "BANK_001":  # Top performer
                    smb_growth = random.uniform(15, 25)
                elif member_bank_id == "BANK_002":  # Second best
                    smb_growth = random.uniform(10, 18)
                else:  # Others
                    smb_growth = random.uniform(2, 12)
                
                # Cost/Income ratio (lower is better)
                cost_income_ratio = random.uniform(0.45, 0.75)
                
                performance_data.append((
                    year, member_bank_id, smb_growth, cost_income_ratio
                ))
        
        # Create DataFrame
        schema = StructType([
            StructField("REPORTING_YEAR", IntegerType()),
            StructField("MEMBER_BANK_ID", StringType()),
            StructField("SMB_LENDING_GROWTH_PCT", FloatType()),
            StructField("COST_INCOME_RATIO", FloatType())
        ])
        
        df = self.session.create_dataframe(performance_data, schema)
        df.write.mode("overwrite").save_as_table("ALLIANCE_PERFORMANCE")
        
        logger.info(f"Generated {len(performance_data)} performance records")
        return df
    
    def generate_market_data(self) -> DataFrame:
        """Generate market data for Norwegian/Nordic companies"""
        logger.info("Generating market data...")
        
        # Norwegian/Nordic companies with realistic tickers
        companies = [
            ("EQNR.OL", "Equinor ASA", "Oil & Gas"),
            ("DNB.OL", "DNB Bank ASA", "Banking"),
            ("TEL.OL", "Telenor ASA", "Telecommunications"),
            ("NHY.OL", "Norsk Hydro ASA", "Materials"),
            ("MOWI.OL", "Mowi ASA", "Aquaculture"),
            ("SalMar.OL", "SalMar ASA", "Aquaculture"),
            ("LSG.OL", "Lerøy Seafood Group ASA", "Aquaculture"),
            ("ORK.OL", "Orkla ASA", "Consumer Goods"),
            ("YAR.OL", "Yara International ASA", "Chemicals"),
            ("NEL.OL", "Nel ASA", "Renewable Energy"),
            # Demo companies for peer analysis (must match DEMO_SEED_COMPANIES)
            ("HELIO.OL", "Helio Salmon AS", "Aquaculture"),
            ("BERG.OL", "Bergen Maritime Services AS", "Maritime"),
            ("NORD.OL", "Nordlys Renewable Energy ASA", "Renewable Energy"),
            ("TROND.OL", "Trondheim Tech Solutions AS", "Technology"),
            ("LOF.OL", "Lofoten Tourism Holdings AS", "Tourism"),
            ("STAV.OL", "Stavanger Oil Services AS", "Oil & Gas"),
            ("FINN.OL", "Finnmark Aquaculture AS", "Aquaculture"),
            ("SUNN.OL", "Sunnmøre Shipping AS", "Maritime"),
            # Additional Helgeland aquaculture companies for peer comparison
            ("HELMAR.OL", "Helgeland Marine Farms AS", "Aquaculture"),
            ("ARCTIC.OL", "Arctic Salmon Holdings AS", "Aquaculture"),
            ("NORDKYST.OL", "Nordkyst Aquaculture AS", "Aquaculture"),
            ("HELFISH.OL", "Helgeland Fish Company AS", "Aquaculture")
        ]
        
        market_data = []
        history_months = self.config.get_config('HISTORY_MONTHS')
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=history_months * 30)
        
        for ticker, company_name, peer_group in companies:
            current_date = start_date
            base_price = random.uniform(50, 500)  # Starting price in NOK
            
            while current_date <= end_date:
                # Random walk for stock price
                price_change = random.uniform(-0.05, 0.05)  # ±5% daily change
                base_price = max(base_price * (1 + price_change), 1.0)  # Minimum 1 NOK
                
                market_data.append((
                    ticker, current_date, base_price, company_name, peer_group
                ))
                
                current_date += timedelta(days=1)
        
        # Create DataFrame
        schema = StructType([
            StructField("TICKER", StringType()),
            StructField("TRADE_DATE", DateType()),
            StructField("CLOSE_PRICE", DecimalType(38, 2)),
            StructField("COMPANY_NAME", StringType()),
            StructField("PEER_GROUP", StringType())
        ])
        
        df = self.session.create_dataframe(market_data, schema)
        df.write.mode("overwrite").save_as_table("MARKET_DATA")
        
        logger.info(f"Generated {len(market_data)} market data records")
        return df
    
    def _log_run_start(self, run_id: str, step: str) -> None:
        """Log run start in registry"""
        try:
            self.session.sql(f"""
                INSERT INTO RUN_REGISTRY (RUN_ID, STEP, STARTED_AT, STATUS)
                VALUES ('{run_id}', '{step}', CURRENT_TIMESTAMP(), 'RUNNING')
            """).collect()
        except Exception:
            pass  # Registry might not exist yet
    
    def _log_run_end(self, run_id: str, step: str, rows_written: int) -> None:
        """Log run completion in registry"""
        try:
            self.session.sql(f"""
                UPDATE RUN_REGISTRY 
                SET ENDED_AT = CURRENT_TIMESTAMP(), 
                    STATUS = 'COMPLETED',
                    ROWS_WRITTEN = {rows_written}
                WHERE RUN_ID = '{run_id}' AND STEP = '{step}'
            """).collect()
        except Exception:
            pass  # Registry might not exist yet
