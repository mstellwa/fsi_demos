#!/usr/bin/env python3
"""
Snowdrift Financials Phase 2 - Banking Data Generation
Generates synthetic Norwegian banking data with realistic patterns and Insurance cross-references
"""

import yaml
import logging
import random
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Tuple
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NorwegianBankingDataGenerator:
    """Generates realistic Norwegian banking data with Insurance integration"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        """Initialize with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.connection_name = connection_name
        self.session = None
        
        # Set up random seeds for deterministic generation
        self.global_seed = self.config['global']['global_seed']
        self.module_seed = self.config.get('banking', {}).get('module_seed', 200)
        random.seed(self.global_seed + self.module_seed)
        np.random.seed(self.global_seed + self.module_seed)
        
        # Load Norwegian data (same as Insurance for consistency)
        self.municipalities = self.config['insurance']['data_generation']['norwegian_municipalities']
        
        # Norwegian first and last names (consistent with Insurance)
        self.norwegian_first_names = [
            "Lars", "Anna", "Ole", "Kari", "Nils", "Ingrid", "Erik", "Astrid", "Magnus", "Solveig",
            "Bjørn", "Liv", "Tor", "Maja", "Ove", "Sigrid", "Rune", "Thea", "Svein", "Ida",
            "Gunnar", "Ellen", "Stein", "Marit", "Oddvar", "Randi", "Terje", "Anne", "Kjell", "Eva",
            "Hans", "Grete", "Per", "Inger", "Dag", "Tone", "Arild", "Kristin", "Geir", "Brit",
            "Jan", "Lise", "Morten", "Hilde", "Espen", "Cathrine", "Thomas", "Maria", "Andreas", "Emma",
            "Henrik", "Sofie", "Jonas", "Camilla", "Martin", "Julie", "Markus", "Sara", "Kristian", "Linda"
        ]
        
        self.norwegian_last_names = [
            "Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Kristiansen",
            "Jensen", "Karlsen", "Johnsen", "Pettersen", "Eriksen", "Berg", "Haugen", "Hagen",
            "Johannessen", "Andreassen", "Jacobsen", "Dahl", "Jørgensen", "Halvorsen", "Lund", "Strand",
            "Solberg", "Moen", "Lie", "Fossum", "Bakken", "Amundsen", "Knudsen", "Knutsen",
            "Mathisen", "Evensen", "Svendsen", "Rasmussen", "Bjerke", "Fredriksen", "Nygård", "Løken"
        ]
        
        # Norwegian merchant categories for transactions
        self.merchant_categories = {
            "GROCERY": ["Rema 1000", "ICA", "Coop", "Bunnpris", "Kiwi", "Meny", "Joker"],
            "FUEL": ["Shell", "Esso", "Circle K", "YX", "Best", "Uno-X"],
            "UTILITIES": ["Hafslund", "BKK", "Lyse", "Agder Energi", "TrønderEnergi"],
            "HEALTHCARE": ["Apotek1", "Vitusapotek", "Ditt Apotek", "Boots", "Legekontor"],
            "EDUCATION": ["Barnehage", "Skole", "Universitet", "Høyskole"],
            "TRANSPORT": ["NSB", "Ruter", "Kolumbus", "AtB", "Skyss"],
            "ENTERTAINMENT": ["Cinemateket", "Teater", "Museum", "Konserthus"],
            "RETAIL": ["H&M", "Cubus", "KappAhl", "Eurosko", "Elkjøp", "Jernia"],
            "RESTAURANT": ["McDonald's", "Burger King", "Dølemo", "Peppes Pizza", "Egon"],
            "SERVICES": ["Frisør", "Renseri", "Verksted", "Rørlegger", "Elektriker"]
        }
        
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
    
    def get_insurance_customers(self) -> List[Dict]:
        """Get existing insurance customers for cross-references"""
        logger.info("Fetching existing insurance customers for cross-references...")
        
        insurance_customers = self.session.sql("""
            SELECT DISTINCT
                CUSTOMER_ID,
                POLICY_ID,
                MUNICIPALITY,
                POSTAL_CODE,
                ADDRESS_LINE1,
                CITY
            FROM INSURANCE.POLICIES 
            WHERE STATUS = 'ACTIVE'
            ORDER BY RANDOM()
        """).to_pandas()
        
        logger.info(f"Found {len(insurance_customers)} insurance customers")
        return insurance_customers.to_dict('records')
    
    def generate_customers(self) -> pd.DataFrame:
        """Generate banking customers with 20-30% overlap with insurance"""
        logger.info("Generating banking customers with insurance cross-references...")
        
        customers_count = 25000  # From requirements
        insurance_customers = self.get_insurance_customers()
        
        # Determine overlap (20-30% of banking customers should have insurance)
        overlap_rate = random.uniform(0.20, 0.30)
        overlap_count = int(customers_count * overlap_rate)
        
        logger.info(f"Creating {overlap_count} customers with insurance overlap out of {customers_count} total")
        
        customers = []
        
        # First: Create customers who have insurance policies
        for i in range(overlap_count):
            if i % 1000 == 0:
                logger.info(f"Generated {i:,} customers with insurance overlap...")
            
            customer_id = f"BANK-CUST-{i+1:06d}"
            
            # Pick a random insurance customer to base this on
            insurance_customer = random.choice(insurance_customers)
            
            # Use similar demographics but not identical
            first_name = random.choice(self.norwegian_first_names)
            last_name = random.choice(self.norwegian_last_names)
            
            # Age distribution (insurance customers tend to be homeowners, so older)
            age = random.randint(25, 75)
            dob = date.today() - timedelta(days=age * 365 + random.randint(0, 365))
            
            # Norwegian national ID format (DDMMYY-NNNNN)
            national_id = f"{dob.strftime('%d%m%y')}-{random.randint(10000, 99999)}"
            
            # Use same or nearby location as insurance
            municipality = insurance_customer['MUNICIPALITY']
            city = insurance_customer['CITY']
            postal_code = insurance_customer['POSTAL_CODE']
            
            # Generate new address in same area
            street_number = random.randint(1, 200)
            street_names = ["gate", "vei", "alle", "plass", "strand", "bakken", "åsen"]
            company_prefixes = ["Nord", "Sør", "Øst", "Vest", "Fjord", "Fjell", "Dal", "Skog"]
            address = f"{random.choice(company_prefixes)}{random.choice(street_names)} {street_number}"
            
            # Phone and email
            phone = f"+47 {random.randint(400, 999)} {random.randint(10, 99)} {random.randint(100, 999)}"
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.no', 'hotmail.com'])}"
            
            # Customer since (insurance customers likely became bank customers after or around same time)
            customer_since = date.today() - timedelta(days=random.randint(30, 2555))  # Up to 7 years
            
            customers.append({
                "CUSTOMER_ID": customer_id,
                "FIRST_NAME": first_name,
                "LAST_NAME": last_name,
                "DOB": dob,
                "NATIONAL_ID": national_id,
                "ADDRESS_LINE1": address,
                "CITY": city,
                "MUNICIPALITY": municipality,
                "POSTAL_CODE": postal_code,
                "COUNTRY": "Norway",
                "PHONE": phone,
                "EMAIL": email,
                "CUSTOMER_SINCE": customer_since,
                "STATUS": "ACTIVE",
                "INSURANCE_POLICY_ID": insurance_customer['POLICY_ID'],  # Cross-reference
                "CREATED_AT": datetime.now()
            })
        
        # Then: Create customers without insurance policies
        for i in range(overlap_count, customers_count):
            if i % 5000 == 0:
                logger.info(f"Generated {i:,} total customers...")
            
            customer_id = f"BANK-CUST-{i+1:06d}"
            
            first_name = random.choice(self.norwegian_first_names)
            last_name = random.choice(self.norwegian_last_names)
            
            # Broader age distribution for non-insurance customers
            age = random.randint(18, 85)
            dob = date.today() - timedelta(days=age * 365 + random.randint(0, 365))
            
            national_id = f"{dob.strftime('%d%m%y')}-{random.randint(10000, 99999)}"
            
            # Random location from any Norwegian municipality
            municipality = random.choice(self.municipalities)
            
            # Generate postal codes for the municipality (simplified)
            if municipality == "Oslo":
                postal_code = f"0{random.randint(150, 290)}"
                city = f"Oslo {random.choice(['Sentrum', 'Øst', 'Vest', 'Nord', 'Sør'])}"
            elif municipality == "Bergen":
                postal_code = f"50{random.randint(10, 99)}"
                city = f"Bergen {random.choice(['Sentrum', 'Øst', 'Vest'])}"
            else:
                postal_code = f"{random.randint(1000, 9999)}"
                city = f"{municipality} {random.choice(['Sentrum', 'Øst', 'Vest'])}"
            
            street_number = random.randint(1, 200)
            street_names = ["gate", "vei", "alle", "plass", "strand", "bakken", "åsen"]
            company_prefixes = ["Nord", "Sør", "Øst", "Vest", "Fjord", "Fjell", "Dal", "Skog"]
            address = f"{random.choice(company_prefixes)}{random.choice(street_names)} {street_number}"
            
            phone = f"+47 {random.randint(400, 999)} {random.randint(10, 99)} {random.randint(100, 999)}"
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.no', 'hotmail.com'])}"
            
            customer_since = date.today() - timedelta(days=random.randint(30, 3650))  # Up to 10 years
            
            customers.append({
                "CUSTOMER_ID": customer_id,
                "FIRST_NAME": first_name,
                "LAST_NAME": last_name,
                "DOB": dob,
                "NATIONAL_ID": national_id,
                "ADDRESS_LINE1": address,
                "CITY": city,
                "MUNICIPALITY": municipality,
                "POSTAL_CODE": postal_code,
                "COUNTRY": "Norway",
                "PHONE": phone,
                "EMAIL": email,
                "CUSTOMER_SINCE": customer_since,
                "STATUS": random.choices(["ACTIVE", "INACTIVE"], weights=[0.95, 0.05])[0],
                "INSURANCE_POLICY_ID": None,  # No insurance
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(customers)} banking customers ({overlap_count} with insurance overlap)")
        return pd.DataFrame(customers)
    
    def generate_accounts(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Generate bank accounts for customers"""
        logger.info("Generating bank accounts...")
        
        accounts = []
        account_counter = 1
        
        for _, customer in customers_df.iterrows():
            if account_counter % 10000 == 0:
                logger.info(f"Generated {account_counter:,} accounts...")
            
            customer_id = customer['CUSTOMER_ID']
            customer_since = customer['CUSTOMER_SINCE']
            
            # Number of accounts per customer (1-6, weighted towards 2-3)
            num_accounts = random.choices([1, 2, 3, 4, 5, 6], weights=[0.15, 0.35, 0.25, 0.15, 0.08, 0.02])[0]
            
            account_types = ["CHECKING", "SAVINGS", "MORTGAGE", "LOAN"]
            
            for i in range(num_accounts):
                account_id = f"ACC-{account_counter:08d}"
                account_counter += 1
                
                # Account type selection
                if i == 0:
                    # First account is always checking
                    account_type = "CHECKING"
                elif i == 1:
                    # Second account often savings
                    account_type = random.choices(["SAVINGS", "CHECKING"], weights=[0.7, 0.3])[0]
                else:
                    # Additional accounts
                    account_type = random.choice(account_types)
                
                # Account opening date (after customer since date)
                days_after_customer_since = random.randint(0, min(365, (date.today() - customer_since).days))
                opened_date = customer_since + timedelta(days=days_after_customer_since)
                
                # Balance based on account type and customer demographics
                if account_type == "CHECKING":
                    balance = random.uniform(1000, 50000)
                elif account_type == "SAVINGS":
                    balance = random.uniform(5000, 500000)
                elif account_type == "MORTGAGE":
                    balance = random.uniform(-500000, -2000000)  # Negative balance (owed)
                else:  # LOAN
                    balance = random.uniform(-10000, -500000)  # Negative balance (owed)
                
                # Interest rate
                if account_type == "CHECKING":
                    interest_rate = random.uniform(0.0001, 0.005)  # 0.01% - 0.5%
                elif account_type == "SAVINGS":
                    interest_rate = random.uniform(0.01, 0.03)  # 1% - 3%
                elif account_type == "MORTGAGE":
                    interest_rate = random.uniform(0.02, 0.05)  # 2% - 5%
                else:  # LOAN
                    interest_rate = random.uniform(0.05, 0.12)  # 5% - 12%
                
                accounts.append({
                    "ACCOUNT_ID": account_id,
                    "CUSTOMER_ID": customer_id,
                    "ACCOUNT_TYPE": account_type,
                    "BALANCE": round(balance, 2),
                    "INTEREST_RATE": round(interest_rate, 4),
                    "OPENED_DATE": opened_date,
                    "STATUS": random.choices(["ACTIVE", "CLOSED"], weights=[0.9, 0.1])[0],
                    "CREATED_AT": datetime.now()
                })
        
        logger.info(f"Generated {len(accounts)} bank accounts")
        return pd.DataFrame(accounts)
    
    def generate_transactions(self, accounts_df: pd.DataFrame) -> pd.DataFrame:
        """Generate realistic Norwegian transactions for active accounts"""
        logger.info("Generating banking transactions...")
        
        # Target: 5M transactions for demo (more manageable than 50M)
        target_transactions = 5_000_000
        
        # Filter to active checking and savings accounts for transactions
        transactional_accounts = accounts_df[
            (accounts_df['STATUS'] == 'ACTIVE') & 
            (accounts_df['ACCOUNT_TYPE'].isin(['CHECKING', 'SAVINGS']))
        ].copy()
        
        logger.info(f"Generating {target_transactions:,} transactions across {len(transactional_accounts):,} accounts")
        
        transactions = []
        transaction_counter = 1
        
        # Calculate transactions per account to reach target
        transactions_per_account = target_transactions // len(transactional_accounts)
        
        for idx, account in transactional_accounts.iterrows():
            if transaction_counter % 1_000_000 == 0:
                logger.info(f"Generated {transaction_counter:,} transactions...")
            
            account_id = account['ACCOUNT_ID']
            opened_date = account['OPENED_DATE']
            current_balance = account['BALANCE']
            
            # Generate transactions from account opening to now
            days_active = (date.today() - opened_date).days
            if days_active < 1:
                days_active = 1
            
            # Distribute transactions over time
            for i in range(transactions_per_account):
                transaction_id = f"TXN-{transaction_counter:010d}"
                transaction_counter += 1
                
                # Random transaction date
                days_back = random.randint(0, days_active)
                transaction_date = date.today() - timedelta(days=days_back)
                
                # Select merchant category and merchant
                category = random.choice(list(self.merchant_categories.keys()))
                merchant_name = random.choice(self.merchant_categories[category])
                
                # Transaction amounts based on category
                amount_ranges = {
                    "GROCERY": (50, 2000),
                    "FUEL": (200, 1500),
                    "UTILITIES": (500, 3000),
                    "HEALTHCARE": (100, 5000),
                    "EDUCATION": (1000, 50000),
                    "TRANSPORT": (50, 500),
                    "ENTERTAINMENT": (100, 2000),
                    "RETAIL": (100, 5000),
                    "RESTAURANT": (150, 1500),
                    "SERVICES": (200, 5000)
                }
                
                min_amount, max_amount = amount_ranges.get(category, (50, 1000))
                amount = round(random.uniform(min_amount, max_amount), 2)
                
                # 85% debits, 15% credits (income, refunds)
                transaction_type = random.choices(["DEBIT", "CREDIT"], weights=[0.85, 0.15])[0]
                
                if transaction_type == "DEBIT":
                    amount = -abs(amount)  # Negative for debits
                    description = f"Purchase at {merchant_name}"
                else:
                    amount = abs(amount)  # Positive for credits
                    description = random.choice(["Salary deposit", "Refund", "Transfer received", "Interest payment"])
                    merchant_name = "BANK TRANSFER"
                    category = "INCOME"
                
                # Update running balance
                current_balance += amount
                
                transactions.append({
                    "TRANSACTION_ID": transaction_id,
                    "ACCOUNT_ID": account_id,
                    "TRANSACTION_DATE": transaction_date,
                    "AMOUNT": amount,
                    "TRANSACTION_TYPE": transaction_type,
                    "MERCHANT_NAME": merchant_name,
                    "MERCHANT_CATEGORY": category,
                    "DESCRIPTION": description,
                    "BALANCE_AFTER": round(current_balance, 2),
                    "CREATED_AT": datetime.now()
                })
                
                # Break if we've hit our target
                if transaction_counter > target_transactions:
                    break
            
            if transaction_counter > target_transactions:
                break
        
        logger.info(f"Generated {len(transactions)} banking transactions")
        return pd.DataFrame(transactions)
    
    def generate_loans(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Generate loans for customers"""
        logger.info("Generating loans...")
        
        loans_count = 15000  # From requirements
        loans = []
        
        # Sample customers for loans (active customers preferred)
        active_customers = customers_df[customers_df['STATUS'] == 'ACTIVE'].copy()
        
        for i in range(loans_count):
            if i % 5000 == 0:
                logger.info(f"Generated {i:,} loans...")
                
            loan_id = f"LOAN-{i+1:06d}"
            customer = active_customers.sample(n=1).iloc[0]
            customer_id = customer['CUSTOMER_ID']
            
            # Loan types with weights
            loan_type = random.choices(
                ["MORTGAGE", "PERSONAL", "AUTO"], 
                weights=[0.70, 0.20, 0.10]
            )[0]
            
            # Loan amounts based on type
            if loan_type == "MORTGAGE":
                principal_amount = random.uniform(1_000_000, 8_000_000)  # NOK
                term_months = random.choice([240, 300, 360])  # 20, 25, 30 years
                interest_rate = random.uniform(0.02, 0.05)  # 2-5%
                property_address = customer['ADDRESS_LINE1']
                property_municipality = customer['MUNICIPALITY']
            elif loan_type == "AUTO":
                principal_amount = random.uniform(100_000, 800_000)  # NOK
                term_months = random.choice([36, 48, 60, 72])  # 3-6 years
                interest_rate = random.uniform(0.03, 0.08)  # 3-8%
                property_address = None
                property_municipality = None
            else:  # PERSONAL
                principal_amount = random.uniform(50_000, 500_000)  # NOK
                term_months = random.choice([12, 24, 36, 48])  # 1-4 years
                interest_rate = random.uniform(0.05, 0.12)  # 5-12%
                property_address = None
                property_municipality = None
            
            # Origination date (within last 10 years)
            originated_date = date.today() - timedelta(days=random.randint(30, 3650))
            maturity_date = originated_date + timedelta(days=30 * term_months)
            
            # Current balance (loan has been partially paid down)
            months_elapsed = ((date.today() - originated_date).days) // 30
            if months_elapsed > term_months:
                months_elapsed = term_months
            
            # Simple amortization calculation
            if months_elapsed >= term_months:
                current_balance = 0
                status = "PAID"
            else:
                remaining_months = term_months - months_elapsed
                current_balance = principal_amount * (remaining_months / term_months) * random.uniform(0.8, 1.0)
                status = random.choices(["ACTIVE", "DELINQUENT"], weights=[0.95, 0.05])[0]
            
            loans.append({
                "LOAN_ID": loan_id,
                "CUSTOMER_ID": customer_id,
                "LOAN_TYPE": loan_type,
                "PRINCIPAL_AMOUNT": round(principal_amount, 2),
                "CURRENT_BALANCE": round(current_balance, 2),
                "INTEREST_RATE": round(interest_rate, 4),
                "TERM_MONTHS": term_months,
                "ORIGINATED_DATE": originated_date,
                "MATURITY_DATE": maturity_date,
                "STATUS": status,
                "PROPERTY_ADDRESS": property_address,
                "PROPERTY_MUNICIPALITY": property_municipality,
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(loans)} loans")
        return pd.DataFrame(loans)
    
    def generate_corporate_entities(self) -> pd.DataFrame:
        """Generate Norwegian corporate entities for compliance scenarios"""
        logger.info("Generating corporate entities...")
        
        entities_count = 5000
        entities = []
        
        for i in range(entities_count):
            if i % 1000 == 0:
                logger.info(f"Generated {i:,} corporate entities...")
            
            org_number = f"{920000000 + i:09d}"  # Norwegian format
            
            # Company name
            prefix = random.choice(["Nord", "Sør", "Øst", "Vest", "Fjord", "Fjell", "Dal", "Skog"])
            business_word = random.choice(["Bygg", "Handel", "Service", "Tek", "Consulting", "Solutions", "Group"])
            suffix = random.choice(["AS", "ASA", "DA"])
            company_name = f"{prefix} {business_word} {suffix}"
            
            # Location
            municipality = random.choice(self.municipalities)
            if municipality == "Oslo":
                postal_code = f"0{random.randint(150, 290)}"
                city = f"Oslo {random.choice(['Sentrum', 'Øst', 'Vest'])}"
            else:
                postal_code = f"{random.randint(1000, 9999)}"
                city = f"{municipality} Sentrum"
            
            # Address
            street_number = random.randint(1, 200)
            address = f"Businessgate {street_number}"
            
            # Business details
            business_codes = ["62.010", "46.900", "41.200", "70.220", "82.990", "68.200"]
            business_descriptions = [
                "Computer programming", "Non-specialized wholesale", "Construction", 
                "Business consulting", "Other professional services", "Rental of real estate"
            ]
            
            activity_code = random.choice(business_codes)
            activity_desc = random.choice(business_descriptions)
            
            # Registration date
            registration_date = date.today() - timedelta(days=random.randint(365, 7300))  # 1-20 years
            
            # Company size
            employee_count = random.choices(
                [random.randint(1, 5), random.randint(6, 20), random.randint(21, 100), random.randint(101, 500)],
                weights=[0.6, 0.25, 0.12, 0.03]
            )[0]
            
            revenue_per_employee = random.randint(500000, 2000000)  # NOK
            annual_revenue = employee_count * revenue_per_employee * random.uniform(0.5, 1.5)
            
            # Beneficial ownership (simplified)
            num_owners = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
            beneficial_owners = []
            
            for j in range(num_owners):
                owner_name = f"{random.choice(self.norwegian_first_names)} {random.choice(self.norwegian_last_names)}"
                ownership_pct = random.uniform(20, 80) if num_owners == 1 else random.uniform(10, 50)
                beneficial_owners.append({
                    "name": owner_name,
                    "ownership_percentage": round(ownership_pct, 2),
                    "role": random.choice(["CEO", "Chairman", "Director", "Owner"])
                })
            
            entities.append({
                "ORGANIZATION_NUMBER": org_number,
                "COMPANY_NAME": company_name,
                "REGISTERED_ADDRESS": address,
                "CITY": city,
                "MUNICIPALITY": municipality,
                "POSTAL_CODE": postal_code,
                "BUSINESS_ACTIVITY_CODE": activity_code,
                "BUSINESS_ACTIVITY_DESC": activity_desc,
                "REGISTRATION_DATE": registration_date,
                "STATUS": random.choices(["ACTIVE", "INACTIVE"], weights=[0.9, 0.1])[0],
                "EMPLOYEE_COUNT": employee_count,
                "ANNUAL_REVENUE": round(annual_revenue, 2),
                "BENEFICIAL_OWNERS": beneficial_owners,  # JSON data
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(entities)} corporate entities")
        return pd.DataFrame(entities)
    
    def save_to_snowflake(self, df: pd.DataFrame, table_name: str, schema: str = "BANK"):
        """Save DataFrame to Snowflake table using write_pandas"""
        logger.info(f"Saving {len(df)} records to {schema}.{table_name}...")
        
        # Use the schema
        self.session.sql(f"USE SCHEMA {schema}").collect()
        
        # Use write_pandas with recommended parameters
        result = self.session.write_pandas(
            df, 
            table_name, 
            quote_identifiers=False, 
            auto_create_table=True, 
            overwrite=True
        )
        
        # Handle different return formats
        if isinstance(result, tuple) and len(result) >= 3:
            success = result[0]
            num_chunks = result[1] if len(result) > 1 else 1
            num_rows = result[2] if len(result) > 2 else len(df)
            if success:
                logger.info(f"✓ Saved {num_rows} rows in {num_chunks} chunks to {schema}.{table_name}")
            else:
                logger.error(f"Failed to save data to {table_name}")
                raise Exception(f"Failed to save to {table_name}")
        else:
            logger.info(f"✓ Saved {len(df)} rows to {schema}.{table_name}")
        
        return self.session.table(f"{schema}.{table_name}")  # Return Snowpark DataFrame
    
    def run_banking_data_generation(self):
        """Execute complete banking structured data generation"""
        logger.info("Starting Norwegian Banking Data Generation...")
        
        try:
            # Create session
            self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Generate customers first (with insurance cross-references)
            logger.info("=== Step 1: Generate Customers ===")
            customers_data = self.generate_customers()
            customers_snowpark_df = self.save_to_snowflake(customers_data, "CUSTOMERS")
            
            # Generate accounts
            logger.info("=== Step 2: Generate Accounts ===")
            accounts_data = self.generate_accounts(customers_data)
            accounts_snowpark_df = self.save_to_snowflake(accounts_data, "ACCOUNTS")
            
            # Generate transactions
            logger.info("=== Step 3: Generate Transactions ===")
            transactions_data = self.generate_transactions(accounts_data)
            transactions_snowpark_df = self.save_to_snowflake(transactions_data, "TRANSACTIONS")
            
            # Generate loans
            logger.info("=== Step 4: Generate Loans ===")
            loans_data = self.generate_loans(customers_data)
            loans_snowpark_df = self.save_to_snowflake(loans_data, "LOANS")
            
            # Generate corporate entities
            logger.info("=== Step 5: Generate Corporate Entities ===")
            entities_data = self.generate_corporate_entities()
            entities_snowpark_df = self.save_to_snowflake(entities_data, "BRREG_CORPORATE")
            
            # Validation - get actual row counts from Snowflake
            logger.info("=== Validation Summary ===")
            customers_count = customers_snowpark_df.count()
            accounts_count = accounts_snowpark_df.count()
            transactions_count = transactions_snowpark_df.count()
            loans_count = loans_snowpark_df.count()
            entities_count = entities_snowpark_df.count()
            
            # Check insurance overlap
            overlap_count = self.session.sql("""
                SELECT COUNT(*) as overlap_count
                FROM BANK.CUSTOMERS 
                WHERE INSURANCE_POLICY_ID IS NOT NULL
            """).collect()[0]['OVERLAP_COUNT']
            
            overlap_percentage = (overlap_count / customers_count) * 100
            
            logger.info(f"✓ Banking customers saved: {customers_count:,}")
            logger.info(f"✓ Bank accounts saved: {accounts_count:,}")
            logger.info(f"✓ Banking transactions saved: {transactions_count:,}")
            logger.info(f"✓ Loans saved: {loans_count:,}")
            logger.info(f"✓ Corporate entities saved: {entities_count:,}")
            logger.info(f"✓ Insurance overlap: {overlap_count:,} customers ({overlap_percentage:.1f}%)")
            
            logger.info("Norwegian Banking Data Generation completed successfully!")
            logger.info("Ready for semantic view creation and document generation")
            
        except Exception as e:
            logger.error(f"Banking data generation failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Norwegian Banking Data Generation")
    parser.add_argument("--connection", default="default", help="Connection name from ~/.snowflake/connections.toml")
    args = parser.parse_args()
    
    generator = NorwegianBankingDataGenerator(connection_name=args.connection)
    generator.run_banking_data_generation()

if __name__ == "__main__":
    main()
