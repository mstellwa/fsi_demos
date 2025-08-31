"""
Structured data generator for companies, financials, and macroeconomic indicators.
"""

import logging
import datetime
from datetime import timedelta
import random
import pandas as pd
import numpy as np
from typing import List, Dict
from faker import Faker

from snowflake.snowpark import Session
from snowflake.snowpark.types import *
from snowflake.snowpark.functions import col, lit

from config import *

logger = logging.getLogger(__name__)

class StructuredDataGenerator:
    """Generates structured data for the demo."""
    
    def __init__(self, session: Session):
        self.session = session
        self.faker = Faker(['en_US', 'sv_SE'])
        self.faker.seed_instance(RANDOM_SEED)
        random.seed(RANDOM_SEED)
        np.random.seed(RANDOM_SEED)
        
    def generate_companies(self) -> pd.DataFrame:
        """Generate the companies master table."""
        logger.info("Generating companies data...")
        
        companies_data = []
        
        # First, add all anchor companies
        for i, company_name in enumerate(ANCHOR_COMPANIES, 1):
            companies_data.append({
                "COMPANY_ID": i,
                "COMPANY_NAME": company_name,
                "TICKER_SYMBOL": self._generate_ticker(company_name),
                "SECTOR": random.choice(SECTORS),
                "HEADQUARTERS": self._generate_headquarters(),
                "FOUNDED_YEAR": random.randint(1950, 2010),
                "EMPLOYEES": random.randint(500, 15000),
                "DESCRIPTION": f"Leading logistics company specializing in {random.choice(['freight forwarding', 'supply chain management', 'transportation services', 'warehousing solutions'])} across the Nordic region."
            })
        
        # Add additional companies to reach NUM_COMPANIES
        remaining_count = NUM_COMPANIES - len(ANCHOR_COMPANIES)
        for i in range(remaining_count):
            idx = len(ANCHOR_COMPANIES) + i + 1
            company_name = ADDITIONAL_COMPANIES[i] if i < len(ADDITIONAL_COMPANIES) else f"Nordic Logistics Co {idx}"
            
            companies_data.append({
                "COMPANY_ID": idx,
                "COMPANY_NAME": company_name,
                "TICKER_SYMBOL": self._generate_ticker(company_name),
                "SECTOR": random.choice(SECTORS),
                "HEADQUARTERS": self._generate_headquarters(),
                "FOUNDED_YEAR": random.randint(1950, 2010),
                "EMPLOYEES": random.randint(500, 15000),
                "DESCRIPTION": f"Regional logistics provider focusing on {random.choice(['last-mile delivery', 'cross-border transport', 'specialized cargo', 'express services'])}."
            })
        
        # Create DataFrame and save to Snowflake
        companies_df = pd.DataFrame(companies_data)
        
        # Write to Snowflake
        self.session.write_pandas(
            companies_df,
            "COMPANIES",
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False
        )
        
        logger.info(f"Created {len(companies_df)} companies")
        return companies_df
    
    def generate_macroeconomic_data(self) -> pd.DataFrame:
        """Generate macroeconomic indicators data."""
        logger.info("Generating macroeconomic data...")
        
        macro_data = []
        
        # Define indicators
        indicators = [
            ("Producer Price Index - Industrial Goods", "INDEX"),
            ("Consumer Price Index", "INDEX"),
            ("GDP Growth Rate", "PERCENT"),
            ("Unemployment Rate", "PERCENT"),
            ("Fuel Price Index", "INDEX"),
            ("Labor Cost Index", "INDEX")
        ]
        
        # Generate monthly data for NUM_MACRO_MONTHS
        start_date = datetime.datetime.now() - timedelta(days=NUM_MACRO_MONTHS * 30)
        
        indicator_id = 1
        for month_offset in range(NUM_MACRO_MONTHS):
            report_date = start_date + timedelta(days=month_offset * 30)
            
            for indicator_name, unit in indicators:
                for region in REGIONS[:4]:  # Focus on main Nordic countries
                    # Generate values with inflation trend
                    if "Price Index" in indicator_name:
                        # Simulate inflation - increasing trend
                        base_value = 100 + (month_offset * 0.3)
                        value = round(base_value + random.uniform(-2, 3), 2)
                    elif indicator_name == "GDP Growth Rate":
                        value = round(random.uniform(-0.5, 2.5), 2)
                    elif indicator_name == "Unemployment Rate":
                        value = round(random.uniform(3.5, 7.5), 2)
                    else:
                        value = round(random.uniform(95, 115), 2)
                    
                    macro_data.append({
                        "INDICATOR_ID": indicator_id,
                        "INDICATOR_NAME": indicator_name,
                        "REPORT_DATE": report_date.date(),
                        "VALUE": value,
                        "UNIT": unit,
                        "REGION": region,
                        "SOURCE": "Nordic Statistical Bureau"
                    })
                    indicator_id += 1
        
        # Create DataFrame and save to Snowflake
        macro_df = pd.DataFrame(macro_data)
        
        self.session.write_pandas(
            macro_df,
            "MACROECONOMIC_INDICATORS",
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False
        )
        
        logger.info(f"Created {len(macro_df)} macroeconomic indicators")
        return macro_df
    
    def generate_financials(self, companies_df: pd.DataFrame) -> pd.DataFrame:
        """Generate quarterly financial data for companies."""
        logger.info("Generating financial data...")
        
        financials_data = []
        financial_id = 1
        
        # Generate quarterly data for NUM_QUARTERS
        end_date = datetime.datetime.now()
        
        for _, company in companies_df.iterrows():
            company_id = company['COMPANY_ID']
            company_name = company['COMPANY_NAME']
            
            # Set base financials based on company size
            if company_name == ANCHOR_COMPANY:
                # Nordic Freight Systems should be a large company
                base_revenue = random.uniform(800_000_000, 1_200_000_000)
            elif company_name in ANCHOR_COMPANIES:
                # Other anchor companies are medium-large
                base_revenue = random.uniform(400_000_000, 800_000_000)
            else:
                # Other companies are smaller
                base_revenue = random.uniform(100_000_000, 400_000_000)
            
            # Base margins - will be affected by inflation
            base_gross_margin = random.uniform(0.25, 0.35)
            base_operating_margin = random.uniform(0.08, 0.15)
            
            for quarter_offset in range(NUM_QUARTERS):
                # Calculate quarter date
                quarter_date = end_date - timedelta(days=quarter_offset * 91)
                year = quarter_date.year
                quarter_num = ((quarter_date.month - 1) // 3) + 1
                reporting_period = f"{year}-Q{quarter_num}"
                
                # Simulate revenue growth with some volatility
                growth_factor = 1 + (random.uniform(-0.02, 0.05) * (1 - quarter_offset/NUM_QUARTERS))
                quarter_revenue = base_revenue * growth_factor
                
                # Simulate inflation impact on costs (costs increase over time)
                inflation_impact = 1 + (quarter_offset * 0.008)  # 0.8% per quarter inflation
                
                # Calculate COGS with inflation pressure
                cogs_ratio = 1 - base_gross_margin
                cogs = quarter_revenue * cogs_ratio * inflation_impact
                
                # Some companies better at passing costs (especially Nordic Freight Systems)
                if company_name == ANCHOR_COMPANY:
                    # Nordic Freight Systems maintains margins better
                    price_pass_through = 0.85  # Passes 85% of cost increases
                    cogs = cogs * (1 - price_pass_through * (inflation_impact - 1))
                elif company_name in ANCHOR_COMPANIES:
                    price_pass_through = random.uniform(0.5, 0.75)
                    cogs = cogs * (1 - price_pass_through * (inflation_impact - 1))
                
                gross_profit = quarter_revenue - cogs
                gross_margin = gross_profit / quarter_revenue
                
                # Operating expenses
                operating_expenses = quarter_revenue * (1 - base_operating_margin - base_gross_margin)
                operating_income = gross_profit - operating_expenses
                
                # Net income (after tax, interest, etc.)
                net_income = operating_income * random.uniform(0.65, 0.75)
                
                financials_data.append({
                    "FINANCIAL_ID": financial_id,
                    "COMPANY_ID": company_id,
                    "REPORTING_PERIOD": reporting_period,
                    "FISCAL_YEAR": year,
                    "FISCAL_QUARTER": quarter_num,
                    "REVENUE": round(quarter_revenue, 2),
                    "COST_OF_GOODS_SOLD": round(cogs, 2),
                    "GROSS_PROFIT": round(gross_profit, 2),
                    "GROSS_MARGIN": round(gross_margin, 4),
                    "OPERATING_EXPENSES": round(operating_expenses, 2),
                    "OPERATING_INCOME": round(operating_income, 2),
                    "NET_INCOME": round(net_income, 2),
                    "EARNINGS_PER_SHARE": round(net_income / random.uniform(50_000_000, 100_000_000), 2),
                    "REPORT_DATE": quarter_date.date()
                })
                financial_id += 1
        
        # Create DataFrame and save to Snowflake
        financials_df = pd.DataFrame(financials_data)
        
        self.session.write_pandas(
            financials_df,
            "COMPANY_FINANCIALS",
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False
        )
        
        logger.info(f"Created {len(financials_df)} financial records")
        return financials_df
    
    def _generate_ticker(self, company_name: str) -> str:
        """Generate a ticker symbol from company name."""
        # Extract uppercase letters or use first 3-4 chars
        ticker = ''.join([c for c in company_name if c.isupper()])[:4]
        if len(ticker) < 3:
            ticker = company_name.replace(" ", "").upper()[:4]
        return ticker
    
    def _generate_headquarters(self) -> str:
        """Generate a Nordic headquarters location."""
        cities = [
            "Stockholm, Sweden",
            "Oslo, Norway",
            "Copenhagen, Denmark",
            "Helsinki, Finland",
            "Gothenburg, Sweden",
            "Bergen, Norway",
            "Aarhus, Denmark",
            "Turku, Finland",
            "Malmö, Sweden",
            "Trondheim, Norway"
        ]
        return random.choice(cities)
