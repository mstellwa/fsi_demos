#!/usr/bin/env python3
"""
Snowdrift Financials Phase 1 - Structured Data Generation
Generates synthetic Norwegian insurance data with realistic patterns and distributions
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

class NorwegianDataGenerator:
    """Generates realistic Norwegian insurance data"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        """Initialize with configuration"""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.connection_name = connection_name
        self.session = None
        
        # Set up random seeds for deterministic generation
        self.global_seed = self.config['global']['global_seed']
        self.module_seed = self.config['insurance']['module_seed']
        random.seed(self.global_seed + self.module_seed)
        np.random.seed(self.global_seed + self.module_seed)
        
        # Load Norwegian data
        self.municipalities = self.config['insurance']['data_generation']['norwegian_municipalities']
        self.flood_risk_dist = self.config['insurance']['data_generation']['flood_risk_distribution']
        
        # Norwegian first names (mix of traditional and modern)
        self.norwegian_first_names = [
            "Lars", "Anna", "Ole", "Kari", "Nils", "Ingrid", "Erik", "Astrid", "Magnus", "Solveig",
            "Bjørn", "Liv", "Tor", "Maja", "Ove", "Sigrid", "Rune", "Thea", "Svein", "Ida",
            "Gunnar", "Ellen", "Stein", "Marit", "Oddvar", "Randi", "Terje", "Anne", "Kjell", "Eva",
            "Hans", "Grete", "Per", "Inger", "Dag", "Tone", "Arild", "Kristin", "Geir", "Brit",
            "Jan", "Lise", "Morten", "Hilde", "Espen", "Cathrine", "Thomas", "Maria", "Andreas", "Emma"
        ]
        
        # Norwegian last names
        self.norwegian_last_names = [
            "Hansen", "Johansen", "Olsen", "Larsen", "Andersen", "Pedersen", "Nilsen", "Kristiansen",
            "Jensen", "Karlsen", "Johnsen", "Pettersen", "Eriksen", "Berg", "Haugen", "Hagen",
            "Johannessen", "Andreassen", "Jacobsen", "Dahl", "Jørgensen", "Halvorsen", "Lund", "Strand",
            "Solberg", "Moen", "Lie", "Fossum", "Bakken", "Amundsen", "Knudsen", "Knutsen",
            "Mathisen", "Evensen", "Svendsen", "Rasmussen", "Bjerke", "Fredriksen", "Nygård", "Løken"
        ]
        
        # Norwegian company name components
        self.company_prefixes = [
            "Nord", "Sør", "Øst", "Vest", "Fjord", "Fjell", "Dal", "Skog", "Kyst", "Åsen",
            "Berg", "Vik", "Strand", "Haugen", "Lund", "Bakken", "Moen", "Dalen", "Røed", "Grønn"
        ]
        
        self.company_suffixes = [
            "AS", "ASA", "BA", "ANS", "DA", "Drift AS", "Invest AS", "Eiendom AS", "Service AS",
            "Teknologi AS", "Consulting AS", "Solutions AS", "Partner AS", "Group ASA"
        ]
        
        self.business_types = [
            "Bygg og anlegg", "Handel", "Transport", "IT-tjenester", "Rådgivning", "Eiendom",
            "Industri", "Maritim", "Energi", "Landbruk", "Turisme", "Helse", "Utdanning", "Finans"
        ]
        
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
    
    def generate_postal_codes(self) -> Dict[str, List[Tuple[str, str]]]:
        """Generate realistic Norwegian postal codes for each municipality"""
        postal_codes = {}
        base_codes = {
            "Oslo": ["0150", "0160", "0170", "0180", "0190", "0250", "0260", "0270", "0280", "0290"],
            "Bergen": ["5003", "5006", "5007", "5009", "5010", "5020", "5030", "5031", "5032", "5033"],
            "Stavanger": ["4001", "4002", "4003", "4004", "4005", "4006", "4007", "4008", "4009", "4010"],
            "Trondheim": ["7001", "7002", "7003", "7004", "7005", "7006", "7007", "7008", "7009", "7010"],
            "Tromsø": ["9001", "9002", "9003", "9004", "9005", "9006", "9007", "9008", "9009", "9010"],
            "Kristiansand": ["4601", "4602", "4603", "4604", "4605", "4606", "4607", "4608", "4609", "4610"],
            "Fredrikstad": ["1601", "1602", "1603", "1604", "1605", "1606", "1607", "1608", "1609", "1610"],
            "Tønsberg": ["3101", "3102", "3103", "3104", "3105", "3106", "3107", "3108", "3109", "3110"],
            "Drammen": ["3001", "3002", "3003", "3004", "3005", "3006", "3007", "3008", "3009", "3010"],
            "Skien": ["3701", "3702", "3703", "3704", "3705", "3706", "3707", "3708", "3709", "3710"]
        }
        
        for municipality in self.municipalities:
            if municipality in base_codes:
                postal_codes[municipality] = [(code, f"{municipality} {random.choice(['Sentrum', 'Øst', 'Vest', 'Nord', 'Sør'])}") 
                                            for code in base_codes[municipality]]
            else:
                # Generate codes for other municipalities
                base = random.randint(1000, 9999)
                postal_codes[municipality] = [(f"{base + i:04d}", f"{municipality} {random.choice(['Sentrum', 'Øst', 'Vest'])}")
                                            for i in range(5)]
        
        return postal_codes
    
    def generate_geo_risk_scores(self) -> pd.DataFrame:
        """Generate geographic risk scores for Norwegian locations"""
        logger.info("Generating geographic risk scores...")
        
        postal_codes = self.generate_postal_codes()
        geo_records = []
        
        for municipality, codes in postal_codes.items():
            # Coastal cities have higher flood risk
            coastal_cities = ["Bergen", "Stavanger", "Kristiansand", "Fredrikstad", "Tromsø"]
            base_risk = 6 if municipality in coastal_cities else 3
            
            logger.info(f"Processing municipality: {municipality}")
            
            for postal_code, area_name in codes:
                # Generate fewer addresses per postal code to avoid performance issues
                num_addresses = random.randint(5, 15)  # Reduced from 10-25
                for i in range(num_addresses):
                    address_key = f"{municipality}_{postal_code}_{i:03d}"
                    street_number = random.randint(1, 200)
                    street_names = ["gate", "vei", "alle", "plass", "strand", "bakken", "åsen"]
                    street_name = f"{random.choice(self.company_prefixes)}{random.choice(street_names)}"
                    address = f"{street_name} {street_number}"
                    
                    # Calculate flood risk score (1-10)
                    risk_modifier = random.normalvariate(0, 1.5)
                    flood_risk = max(1, min(10, int(base_risk + risk_modifier)))
                    
                    # Apply risk distribution weights
                    rand_val = random.random()
                    if rand_val < self.flood_risk_dist['low_risk']:
                        flood_risk = min(flood_risk, random.randint(1, 3))
                    elif rand_val < self.flood_risk_dist['low_risk'] + self.flood_risk_dist['medium_risk']:
                        flood_risk = max(4, min(6, flood_risk))
                    else:
                        flood_risk = max(7, flood_risk)
                    
                    risk_factors = {
                        "proximity_to_water": random.choice(["river", "coast", "lake", "none"]),
                        "elevation": random.randint(0, 500),
                        "drainage_quality": random.choice(["poor", "fair", "good", "excellent"]),
                        "historical_floods": random.randint(0, 5)
                    }
                    
                    geo_records.append({
                        "ADDRESS_KEY": address_key,
                        "ADDRESS_LINE1": address,
                        "CITY": area_name,
                        "MUNICIPALITY": municipality,
                        "POSTAL_CODE": postal_code,
                        "COUNTRY": "Norway",
                        "FLOOD_RISK_SCORE": flood_risk,
                        "RISK_FACTORS": risk_factors,
                        "UPDATED_AT": datetime.now()
                    })
        
        logger.info(f"Generated {len(geo_records)} geographic risk records")
        return pd.DataFrame(geo_records)
    
    def generate_brreg_companies(self) -> pd.DataFrame:
        """Generate synthetic Norwegian business registry data"""
        logger.info("Generating Norwegian business registry data...")
        
        companies_count = self.config['insurance']['structured_data']['brreg_companies_count']
        postal_codes = self.generate_postal_codes()
        
        companies = []
        for i in range(companies_count):
            if i % 1000 == 0:
                logger.info(f"Generated {i:,} companies...")
            org_number = f"{910000000 + i:09d}"  # Norwegian format
            
            # Generate company name
            prefix = random.choice(self.company_prefixes)
            suffix = random.choice(self.company_suffixes)
            business_word = random.choice(["Bygg", "Handel", "Service", "Tek", "Consulting", "Solutions"])
            company_name = f"{prefix} {business_word} {suffix}"
            
            # Random location
            municipality = random.choice(self.municipalities)
            postal_code, area_name = random.choice(postal_codes[municipality])
            
            street_number = random.randint(1, 200)
            street_names = ["gate", "vei", "alle", "plass"]
            address = f"{random.choice(self.company_prefixes)}{random.choice(street_names)} {street_number}"
            
            # Business activity
            activity_code = f"{random.randint(10, 99)}.{random.randint(10, 99)}.{random.randint(1, 9)}"
            business_activity = random.choice(self.business_types)
            
            # Financial data
            employee_count = random.choices(
                [random.randint(1, 5), random.randint(6, 20), random.randint(21, 100), random.randint(101, 500)],
                weights=[0.6, 0.25, 0.12, 0.03]
            )[0]
            
            # Revenue correlated with employee count
            revenue_per_employee = random.randint(500000, 2000000)  # NOK
            annual_revenue = employee_count * revenue_per_employee * random.uniform(0.5, 1.5)
            
            registration_date = datetime.now() - timedelta(days=random.randint(30, 3650))
            
            companies.append({
                "ORGANIZATION_NUMBER": org_number,
                "COMPANY_NAME": company_name,
                "REGISTERED_ADDRESS": address,
                "CITY": area_name,
                "MUNICIPALITY": municipality,
                "POSTAL_CODE": postal_code,
                "BUSINESS_ACTIVITY_CODE": activity_code,
                "BUSINESS_ACTIVITY_DESC": business_activity,
                "REGISTRATION_DATE": registration_date.date(),
                "STATUS": random.choices(["ACTIVE", "INACTIVE"], weights=[0.9, 0.1])[0],
                "EMPLOYEE_COUNT": employee_count,
                "ANNUAL_REVENUE": annual_revenue,
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(companies)} business registry records")
        return pd.DataFrame(companies)
    
    def generate_policies(self, geo_data: pd.DataFrame) -> pd.DataFrame:
        """Generate insurance policies linked to geographic locations"""
        logger.info("Generating insurance policies...")
        
        policies_count = self.config['insurance']['structured_data']['policies_count']
        history_years = self.config['insurance']['structured_data']['history_years']
        
        # Sample addresses from geo data
        available_addresses = geo_data.sample(n=min(policies_count, len(geo_data)), replace=True).reset_index(drop=True)
        
        policies = []
        for i in range(policies_count):
            if i % 5000 == 0:
                logger.info(f"Generated {i:,} policies...")
            policy_id = f"POL-{i+1:06d}"
            customer_id = f"CUST-{i+1:06d}"
            
            # Use address from geo data
            address_data = available_addresses.iloc[i % len(available_addresses)]
            
            # Policy dates
            effective_date = datetime.now().date() - timedelta(days=random.randint(0, history_years * 365))
            expiry_date = effective_date + timedelta(days=365)
            
            # Determine policy type (80% residential, 20% commercial)
            policy_type = random.choices(
                ["RESIDENTIAL", "COMMERCIAL"], 
                weights=[0.8, 0.2]
            )[0]
            
            # Coverage amount based on policy type and location risk
            if policy_type == "COMMERCIAL":
                base_coverage = random.randint(5000000, 50000000)  # Higher for commercial
            else:
                base_coverage = random.randint(2000000, 15000000)  # Residential range
                
            risk_multiplier = 1.0 + (address_data['FLOOD_RISK_SCORE'] - 5) * 0.1
            coverage_amount = int(base_coverage * risk_multiplier)
            
            # Premium calculation (1-3% of coverage, commercial slightly higher rate)
            risk_factor = address_data['FLOOD_RISK_SCORE'] / 10
            base_rate = 0.012 if policy_type == "COMMERCIAL" else 0.01
            premium_rate = base_rate + (risk_factor * 0.02)
            annual_premium = int(coverage_amount * premium_rate)
            
            policies.append({
                "POLICY_ID": policy_id,
                "CUSTOMER_ID": customer_id,
                "POLICY_TYPE": policy_type,
                "PREMIUM": annual_premium,
                "COVERAGE_AMOUNT": coverage_amount,
                "EFFECTIVE_DATE": effective_date,
                "EXPIRY_DATE": expiry_date,
                "STATUS": random.choices(["ACTIVE", "EXPIRED", "CANCELLED"], weights=[0.8, 0.15, 0.05])[0],
                "ADDRESS_LINE1": address_data['ADDRESS_LINE1'],
                "CITY": address_data['CITY'],
                "MUNICIPALITY": address_data['MUNICIPALITY'],
                "POSTAL_CODE": address_data['POSTAL_CODE'],
                "COUNTRY": "Norway",
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(policies)} insurance policies")
        return pd.DataFrame(policies)
    
    def generate_claims(self, policies_df: pd.DataFrame, geo_data: pd.DataFrame) -> pd.DataFrame:
        """Generate claims associated with policies"""
        logger.info("Generating insurance claims...")
        
        claims_count = self.config['insurance']['structured_data']['claims_count']
        
        # Merge policies with geo data for risk information
        policies_with_risk = policies_df.merge(
            geo_data[['MUNICIPALITY', 'POSTAL_CODE', 'FLOOD_RISK_SCORE']], 
            on=['MUNICIPALITY', 'POSTAL_CODE'], 
            how='left'
        )
        
        claims = []
        
        # FIRST: Generate golden demo records that match our test queries
        logger.info("Generating golden demo records...")
        golden_claims = self._generate_golden_claims(policies_with_risk, geo_data)
        claims.extend(golden_claims)
        logger.info(f"✓ Generated {len(golden_claims)} golden demo claims")
        
        # THEN: Generate the rest randomly
        # Skip IDs that are already used by golden claims
        used_ids = {'CLM-014741', 'CLM-003812', 'CLM-002456', 'CLM-005789', 'CLM-001234'}
        
        for i in range(len(golden_claims), claims_count):
            if i % 5000 == 0:
                logger.info(f"Generated {i:,} claims...")
            
            # Generate a claim ID that doesn't conflict with golden claims
            claim_id = f"CLM-{i+1:06d}"
            while claim_id in used_ids:
                i += 1
                claim_id = f"CLM-{i+1:06d}"
            used_ids.add(claim_id)
            
            # Select policy (higher risk locations more likely to have claims)
            weights = [max(1, risk) for risk in policies_with_risk['FLOOD_RISK_SCORE'].fillna(5)]
            policy = policies_with_risk.sample(n=1, weights=weights).iloc[0]
            
            # Claim dates
            policy_start = policy['EFFECTIVE_DATE']
            policy_end = policy['EXPIRY_DATE']
            if isinstance(policy_start, str):
                policy_start = datetime.strptime(policy_start, '%Y-%m-%d').date()
            if isinstance(policy_end, str):
                policy_end = datetime.strptime(policy_end, '%Y-%m-%d').date()
                
            loss_date = policy_start + timedelta(days=random.randint(0, (policy_end - policy_start).days))
            reported_date = loss_date + timedelta(days=random.randint(0, 30))
            
            # Claim amount based on coverage and damage severity
            damage_severity = random.uniform(0.05, 0.5)  # 5-50% of coverage
            flood_risk_multiplier = 1.0 + (policy['FLOOD_RISK_SCORE'] - 5) * 0.1
            claim_amount = int(policy['COVERAGE_AMOUNT'] * damage_severity * flood_risk_multiplier)
            
            # Payment amount (may be less than claim due to deductibles, disputes)
            payment_ratio = random.uniform(0.7, 1.0)
            paid_amount = int(claim_amount * payment_ratio) if random.random() > 0.1 else 0
            
            # Claim descriptions
            damage_types = [
                "Water damage from flooding", "Storm damage to roof", "Flooding in basement",
                "Wind damage to windows", "Hail damage", "Water pipe burst", "Fire damage",
                "Theft and vandalism", "Flooding from heavy rain", "Storm surge damage"
            ]
            
            description = random.choice(damage_types)
            
            status = "CLOSED" if paid_amount > 0 else random.choice(["OPEN", "UNDER_REVIEW", "PENDING"])
            
            claims.append({
                "CLAIM_ID": claim_id,
                "POLICY_ID": policy['POLICY_ID'],
                "LOSS_DATE": loss_date,
                "REPORTED_DATE": reported_date,
                "DESCRIPTION": description,
                "STATUS": status,
                "CLAIM_AMOUNT": claim_amount,
                "PAID_AMOUNT": paid_amount,
                "ADDRESS_LINE1": policy['ADDRESS_LINE1'],
                "CITY": policy['CITY'],
                "MUNICIPALITY": policy['MUNICIPALITY'],
                "POSTAL_CODE": policy['POSTAL_CODE'],
                "COUNTRY": "Norway",
                "CREATED_AT": datetime.now()
            })
        
        logger.info(f"Generated {len(claims)} insurance claims")
        return pd.DataFrame(claims)
    
    def _generate_golden_claims(self, policies_with_risk: pd.DataFrame, geo_data: pd.DataFrame) -> List[Dict]:
        """Generate golden demo claims that match our test queries"""
        golden_claims = []
        
        # Find policies in different municipalities for our test scenarios
        kristiansand_policies = policies_with_risk[policies_with_risk['MUNICIPALITY'] == 'Kristiansand']
        bergen_policies = policies_with_risk[policies_with_risk['MUNICIPALITY'] == 'Bergen']
        oslo_policies = policies_with_risk[policies_with_risk['MUNICIPALITY'] == 'Oslo']
        
        if len(kristiansand_policies) == 0 or len(bergen_policies) == 0 or len(oslo_policies) == 0:
            logger.warning("Missing policies in required municipalities for golden claims")
            return []
        
        # Golden Claim 1: CLM-014741 (Main demo claim - NEW motor vehicle accident with injuries, Kristiansand)
        policy_1 = kristiansand_policies.iloc[0]
        # Use current date to indicate this "just came in"
        current_date = datetime.now().date()
        yesterday = current_date - timedelta(days=1)
        
        golden_claims.append({
            "CLAIM_ID": "CLM-014741",
            "POLICY_ID": policy_1['POLICY_ID'],
            "LOSS_DATE": yesterday,  # Loss happened yesterday
            "REPORTED_DATE": current_date,  # Reported today ("just came in")
            "DESCRIPTION": "Motor vehicle accident with multiple injuries",
            "STATUS": "OPEN",  # New claim, just came in
            "CLAIM_AMOUNT": 2850000,  # 2.85M NOK for medical/vehicle claim
            "PAID_AMOUNT": 0,  # No payment yet since it's new
            "ADDRESS_LINE1": policy_1['ADDRESS_LINE1'],
            "CITY": policy_1['CITY'],
            "MUNICIPALITY": "Kristiansand",
            "POSTAL_CODE": policy_1['POSTAL_CODE'],
            "COUNTRY": "Norway",
            "CREATED_AT": datetime.now()
        })
        
        # Golden Claim 2: CLM-003812 (Inconsistency testing - Bergen)
        policy_2 = bergen_policies.iloc[0]
        golden_claims.append({
            "CLAIM_ID": "CLM-003812",
            "POLICY_ID": policy_2['POLICY_ID'],
            "LOSS_DATE": date(2024, 5, 20),
            "REPORTED_DATE": date(2024, 5, 25),  # 5-day delay for inconsistency
            "DESCRIPTION": "Flooding from heavy rain",
            "STATUS": "PENDING",
            "CLAIM_AMOUNT": 10819370,
            "PAID_AMOUNT": 0,
            "ADDRESS_LINE1": policy_2['ADDRESS_LINE1'],
            "CITY": policy_2['CITY'],
            "MUNICIPALITY": "Bergen",
            "POSTAL_CODE": policy_2['POSTAL_CODE'],
            "COUNTRY": "Norway",
            "CREATED_AT": datetime.now()
        })
        
        # Golden Claim 3: CLM-002456 (Vehicle accident with injuries - Oslo)
        policy_3 = oslo_policies.iloc[0]
        golden_claims.append({
            "CLAIM_ID": "CLM-002456",
            "POLICY_ID": policy_3['POLICY_ID'],
            "LOSS_DATE": date(2024, 7, 10),
            "REPORTED_DATE": date(2024, 7, 11),
            "DESCRIPTION": "Vehicle accident with property damage",
            "STATUS": "CLOSED",
            "CLAIM_AMOUNT": 850000,
            "PAID_AMOUNT": 785000,
            "ADDRESS_LINE1": policy_3['ADDRESS_LINE1'],
            "CITY": policy_3['CITY'],
            "MUNICIPALITY": "Oslo",
            "POSTAL_CODE": policy_3['POSTAL_CODE'],
            "COUNTRY": "Norway",
            "CREATED_AT": datetime.now()
        })
        
        # Golden Claim 4: CLM-005789 (Medical claim with potential fraud - Oslo)
        policy_4 = oslo_policies.iloc[1] if len(oslo_policies) > 1 else oslo_policies.iloc[0]
        golden_claims.append({
            "CLAIM_ID": "CLM-005789",
            "POLICY_ID": policy_4['POLICY_ID'],
            "LOSS_DATE": date(2024, 4, 25),
            "REPORTED_DATE": date(2024, 4, 26),
            "DESCRIPTION": "Water damage from burst pipe",
            "STATUS": "UNDER_REVIEW",
            "CLAIM_AMOUNT": 1250000,
            "PAID_AMOUNT": 0,
            "ADDRESS_LINE1": policy_4['ADDRESS_LINE1'],
            "CITY": policy_4['CITY'],
            "MUNICIPALITY": "Oslo",
            "POSTAL_CODE": policy_4['POSTAL_CODE'],
            "COUNTRY": "Norway",
            "CREATED_AT": datetime.now()
        })
        
        # Golden Claim 5: CLM-001234 (Vehicle accident with medical injuries)
        policy_5 = kristiansand_policies.iloc[1] if len(kristiansand_policies) > 1 else kristiansand_policies.iloc[0]
        golden_claims.append({
            "CLAIM_ID": "CLM-001234",
            "POLICY_ID": policy_5['POLICY_ID'],
            "LOSS_DATE": date(2024, 8, 5),
            "REPORTED_DATE": date(2024, 8, 6),
            "DESCRIPTION": "Motor vehicle collision with injuries",
            "STATUS": "OPEN",
            "CLAIM_AMOUNT": 2100000,
            "PAID_AMOUNT": 500000,  # Partial payment
            "ADDRESS_LINE1": policy_5['ADDRESS_LINE1'],
            "CITY": policy_5['CITY'],
            "MUNICIPALITY": "Kristiansand",
            "POSTAL_CODE": policy_5['POSTAL_CODE'],
            "COUNTRY": "Norway",
            "CREATED_AT": datetime.now()
        })
        
        return golden_claims
    
    def save_to_snowflake(self, df: pd.DataFrame, table_name: str, schema: str = "INSURANCE"):
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
    
    def run_data_generation(self):
        """Execute complete structured data generation"""
        logger.info("Starting Norwegian Insurance Data Generation...")
        
        try:
            # Create session
            self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Generate all data
            logger.info("=== Step 1: Geographic Risk Scores ===")
            geo_data = self.generate_geo_risk_scores()
            geo_snowpark_df = self.save_to_snowflake(geo_data, "GEO_RISK_SCORES")
            
            logger.info("=== Step 2: Business Registry ===")
            companies_data = self.generate_brreg_companies()
            companies_snowpark_df = self.save_to_snowflake(companies_data, "BRREG_SNAPSHOT")
            
            logger.info("=== Step 3: Insurance Policies ===")
            policies_data = self.generate_policies(geo_data)
            policies_snowpark_df = self.save_to_snowflake(policies_data, "POLICIES")
            
            logger.info("=== Step 4: Insurance Claims ===")
            claims_data = self.generate_claims(policies_data, geo_data)
            claims_snowpark_df = self.save_to_snowflake(claims_data, "CLAIMS")
            
            # Validation - get actual row counts from Snowflake
            logger.info("=== Validation Summary ===")
            geo_count = geo_snowpark_df.count()
            companies_count = companies_snowpark_df.count()
            policies_count = policies_snowpark_df.count()
            claims_count = claims_snowpark_df.count()
            
            logger.info(f"✓ Geographic locations saved: {geo_count:,}")
            logger.info(f"✓ Business registry entries saved: {companies_count:,}")
            logger.info(f"✓ Insurance policies saved: {policies_count:,}")
            logger.info(f"✓ Insurance claims saved: {claims_count:,}")
            
            logger.info("Norwegian Insurance Data Generation completed successfully!")
            logger.info("Ready for semantic view creation")
            
        except Exception as e:
            logger.error(f"Data generation failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description="Norwegian Insurance Data Generation")
    parser.add_argument("--connection", default="default", help="Connection name from ~/.snowflake/connections.toml")
    args = parser.parse_args()
    
    generator = NorwegianDataGenerator(connection_name=args.connection)
    generator.run_data_generation()

if __name__ == "__main__":
    main()
