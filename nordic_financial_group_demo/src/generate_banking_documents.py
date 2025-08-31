#!/usr/bin/env python3
"""
Snowdrift Financials Phase 2 - Banking Document Generation
Generates economic reports and compliance documents for Banking agents
"""

import logging
import yaml
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit
from snowflake.cortex import Complete

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('snowdrift_banking_documents.log')
    ]
)
logger = logging.getLogger(__name__)

class BankingDocumentGenerator:
    """Banking document generation using PROMPTS table and configurable models"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.connection_name = connection_name
        self.session = None
        
        # Document generation settings
        banking_config = self.config.get('banking', {})
        unstructured_config = banking_config.get('unstructured_data', {})
        content_config = self.config.get('insurance', {}).get('content_generation', {})  # Reuse content config
        
        self.economic_target = unstructured_config.get('economic_documents', 100)
        self.compliance_target = unstructured_config.get('compliance_documents', 75)
        
        # Model configuration
        self.default_model = content_config.get('default_model', 'claude-4-sonnet')
        self.fallback_model = content_config.get('fallback_model', 'llama3.1-8b')
        self.temperature = content_config.get('temperature', 0.3)
        self.max_tokens = content_config.get('max_tokens', 2000)
        
        # Norwegian municipalities for geographic focus
        self.municipalities = self.config['insurance']['data_generation']['norwegian_municipalities']
        
        logger.info(f"Configured models: {self.default_model} (primary), {self.fallback_model} (fallback)")
        
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
                logger.info(f"✓ Saved {num_rows} records in {num_chunks} chunks to {schema}.{table_name}")
            else:
                logger.error(f"Failed to save data to {table_name}")
                raise Exception(f"Failed to save to {table_name}")
        else:
            logger.info(f"✓ Saved {len(df)} records to {schema}.{table_name}")
        
        return self.session.table(f"{schema}.{table_name}")
    
    def get_sample_customer_data(self) -> List[Dict]:
        """Get sample customer and transaction data for economic context"""
        logger.info("Fetching sample customer data for economic reports...")
        
        customer_data = self.session.sql("""
            SELECT 
                c.MUNICIPALITY,
                c.CITY,
                COUNT(DISTINCT c.CUSTOMER_ID) as customer_count,
                AVG(a.BALANCE) as avg_balance,
                COUNT(DISTINCT l.LOAN_ID) as loan_count,
                AVG(l.PRINCIPAL_AMOUNT) as avg_loan_amount
            FROM BANK.CUSTOMERS c
            LEFT JOIN BANK.ACCOUNTS a ON c.CUSTOMER_ID = a.CUSTOMER_ID
            LEFT JOIN BANK.LOANS l ON c.CUSTOMER_ID = l.CUSTOMER_ID
            WHERE c.STATUS = 'ACTIVE'
            GROUP BY c.MUNICIPALITY, c.CITY
            ORDER BY customer_count DESC
            LIMIT 50
        """).to_pandas()
        
        logger.info(f"Retrieved data for {len(customer_data)} municipalities")
        return customer_data.to_dict('records')
    
    def get_sample_corporate_data(self) -> List[Dict]:
        """Get sample corporate entity data for compliance context"""
        logger.info("Fetching sample corporate data for compliance reports...")
        
        corporate_data = self.session.sql("""
            SELECT 
                ORGANIZATION_NUMBER,
                COMPANY_NAME,
                MUNICIPALITY,
                BUSINESS_ACTIVITY_DESC,
                EMPLOYEE_COUNT,
                ANNUAL_REVENUE,
                STATUS
            FROM BANK.BRREG_CORPORATE
            ORDER BY RANDOM()
            LIMIT 100
        """).to_pandas()
        
        logger.info(f"Retrieved data for {len(corporate_data)} corporate entities")
        return corporate_data.to_dict('records')
    
    def generate_economic_prompts(self) -> pd.DataFrame:
        """Generate all prompts for economic documents"""
        logger.info("Generating prompts for economic documents...")
        
        # Get sample data
        customer_data = self.get_sample_customer_data()
        
        prompts = []
        doc_types = [
            'HOUSING_REPORT', 'EMPLOYMENT_DATA', 'MARKET_ANALYSIS',
            'REGIONAL_ECONOMIC_OUTLOOK', 'SECTOR_ANALYSIS', 'MORTGAGE_MARKET_REPORT'
        ]
        
        # Generate golden economic documents for key municipalities
        logger.info("Generating golden economic documents for test queries...")
        golden_economic_prompts = self._generate_golden_economic_prompts(customer_data, doc_types)
        prompts.extend(golden_economic_prompts)
        logger.info(f"✓ Generated {len(golden_economic_prompts)} golden economic documents")
        
        # Generate the rest randomly
        for i in range(len(golden_economic_prompts), self.economic_target):
            if i % 25 == 0:
                logger.info(f"Generated {i} economic prompts...")
            
            # Select random customer area and document type
            area_data = random.choice(customer_data)
            doc_type = random.choice(doc_types)
            
            # Create prompt based on document type
            prompt_text = self._create_economic_prompt(area_data, doc_type)
            
            metadata = {
                'doc_id': f"ECON_{i+1:06d}",
                'title': f"{doc_type.replace('_', ' ').title()} - {area_data['MUNICIPALITY']}",
                'keywords': self._extract_economic_keywords(area_data, doc_type)
            }
            prompts.append(self._create_prompt_dict(
                prompt_id=f"ECON_DOC_{i+1:06d}",
                prompt_type='ECONOMIC_DOCUMENT',
                prompt_text=prompt_text,
                metadata=metadata,
                doc_type=doc_type,
                municipality=area_data['MUNICIPALITY'],
                region=area_data.get('CITY', area_data['MUNICIPALITY'])
            ))
        
        logger.info(f"Generated {len(prompts)} economic prompts")
        return pd.DataFrame(prompts)
    
    def generate_compliance_prompts(self) -> pd.DataFrame:
        """Generate all prompts for compliance documents"""
        logger.info("Generating prompts for compliance documents...")
        
        # Get sample corporate data
        corporate_data = self.get_sample_corporate_data()
        
        prompts = []
        doc_types = [
            'KYC_REPORT', 'AML_ASSESSMENT', 'BENEFICIAL_OWNERSHIP',
            'SANCTIONS_SCREENING', 'RISK_PROFILE', 'COMPLIANCE_REVIEW'
        ]
        
        # Generate golden compliance documents for test entities
        logger.info("Generating golden compliance documents for test queries...")
        golden_compliance_prompts = self._generate_golden_compliance_prompts(corporate_data, doc_types)
        prompts.extend(golden_compliance_prompts)
        logger.info(f"✓ Generated {len(golden_compliance_prompts)} golden compliance documents")
        
        # Generate the rest randomly
        for i in range(len(golden_compliance_prompts), self.compliance_target):
            if i % 25 == 0:
                logger.info(f"Generated {i} compliance prompts...")
            
            # Select random corporate entity and document type
            entity = random.choice(corporate_data)
            doc_type = random.choice(doc_types)
            
            # Create prompt based on document type
            prompt_text = self._create_compliance_prompt(entity, doc_type)
            
            metadata = {
                'doc_id': f"COMP_{i+1:06d}",
                'title': f"{doc_type.replace('_', ' ').title()} - {entity['COMPANY_NAME']}",
                'keywords': self._extract_compliance_keywords(entity, doc_type)
            }
            prompts.append(self._create_prompt_dict(
                prompt_id=f"COMP_DOC_{i+1:06d}",
                prompt_type='COMPLIANCE_DOCUMENT',
                prompt_text=prompt_text,
                metadata=metadata,
                doc_type=doc_type,
                organization_number=entity['ORGANIZATION_NUMBER'],
                company_name=entity['COMPANY_NAME']
            ))
        
        logger.info(f"Generated {len(prompts)} compliance prompts")
        return pd.DataFrame(prompts)
    
    def execute_complete_with_fallback(self, prompts_df):
        """Execute Complete using Snowpark with_column and fallback model"""
        logger.info(f"Executing Complete on {prompts_df.count()} prompts...")
        
        try:
            # Try with primary model first
            logger.info(f"Attempting content generation with {self.default_model}...")
            
            result_df = prompts_df.with_column(
                "GENERATED_CONTENT",
                Complete(self.default_model, col("PROMPT_TEXT"))
            ).with_column(
                "MODEL_USED", 
                lit(self.default_model)
            ).with_column(
                "GENERATION_TIMESTAMP",
                lit(datetime.now())
            )
            
            # Test if generation worked by collecting a small sample
            test_result = result_df.limit(1).collect()
            if test_result and test_result[0]['GENERATED_CONTENT']:
                logger.info(f"✓ Content generation successful with {self.default_model}")
                return result_df
            else:
                raise Exception(f"No content generated with {self.default_model}")
                
        except Exception as e:
            logger.warning(f"Primary model {self.default_model} failed: {str(e)}")
            logger.info(f"Falling back to {self.fallback_model}...")
            
            try:
                # Fallback to secondary model
                result_df = prompts_df.with_column(
                    "GENERATED_CONTENT",
                    Complete(self.fallback_model, col("PROMPT_TEXT"))
                ).with_column(
                    "MODEL_USED", 
                    lit(self.fallback_model)
                ).with_column(
                    "GENERATION_TIMESTAMP",
                    lit(datetime.now())
                )
                
                logger.info(f"✓ Content generation successful with fallback model {self.fallback_model}")
                return result_df
                
            except Exception as e2:
                logger.error(f"Fallback model {self.fallback_model} also failed: {str(e2)}")
                raise Exception(f"Both models failed: {self.default_model}, {self.fallback_model}")
    
    def process_economic_documents(self):
        """Process economic documents using proper workflow"""
        logger.info("=== Processing Economic Documents ===")
        
        # Step 1: Generate prompts
        logger.info("Step 1: Generating economic prompts...")
        economic_prompts_df = self.generate_economic_prompts()
        
        # Step 2: Save prompts to PROMPTS table (append mode)
        logger.info("Step 2: Appending prompts to CONTROL.PROMPTS...")
        economic_prompts_snowpark = self.session.create_dataframe(economic_prompts_df)
        economic_prompts_snowpark.write.mode("append").save_as_table("CONTROL.PROMPTS", table_type="")
        
        # Step 3: Create Snowpark DataFrame from prompts
        logger.info("Step 3: Creating Snowpark DataFrame from economic prompts...")
        economic_prompts_from_table = self.session.table("CONTROL.PROMPTS").filter(
            col("PROMPT_TYPE") == "ECONOMIC_DOCUMENT"
        )
        
        # Step 4: Execute Complete using with_column
        logger.info("Step 4: Executing Complete on economic prompts...")
        economic_with_content = self.execute_complete_with_fallback(economic_prompts_from_table)
        
        # Step 5: Transform and save to final table
        logger.info("Step 5: Saving economic documents...")
        economic_documents = economic_with_content.select(
            col("METADATA")['doc_id'].astype('string').alias("DOC_ID"),
            col("METADATA")['title'].astype('string').alias("TITLE"),
            col("DOC_TYPE"),
            col("MUNICIPALITY"),
            col("METADATA")['region'].astype('string').alias("REGION"),
            col("GENERATED_CONTENT").alias("CONTENT_MD"),
            col("CREATED_AT"),
            col("METADATA")['keywords'].astype('string').alias("KEYWORDS"),
            col("MODEL_USED"),
            col("GENERATION_TIMESTAMP")
        )
        
        # Save using save_as_table
        economic_documents.write.mode("overwrite").save_as_table("BANK.ECONOMIC_DOCUMENTS", table_type="")
        
        economic_count = economic_documents.count()
        logger.info(f"✓ Processed {economic_count} economic documents")
        
        return economic_count
    
    def process_compliance_documents(self):
        """Process compliance documents using proper workflow"""
        logger.info("=== Processing Compliance Documents ===")
        
        # Step 1: Generate prompts
        logger.info("Step 1: Generating compliance prompts...")
        compliance_prompts_df = self.generate_compliance_prompts()
        
        # Step 2: Save prompts to PROMPTS table (append mode)
        logger.info("Step 2: Appending prompts to CONTROL.PROMPTS...")
        compliance_prompts_snowpark = self.session.create_dataframe(compliance_prompts_df)
        compliance_prompts_snowpark.write.mode("append").save_as_table("CONTROL.PROMPTS", table_type="")
        
        # Step 3: Create Snowpark DataFrame from prompts
        logger.info("Step 3: Creating Snowpark DataFrame from compliance prompts...")
        compliance_prompts_from_table = self.session.table("CONTROL.PROMPTS").filter(
            col("PROMPT_TYPE") == "COMPLIANCE_DOCUMENT"
        )
        
        # Step 4: Execute Complete using with_column
        logger.info("Step 4: Executing Complete on compliance prompts...")
        compliance_with_content = self.execute_complete_with_fallback(compliance_prompts_from_table)
        
        # Step 5: Transform and save to final table
        logger.info("Step 5: Saving compliance documents...")
        compliance_documents = compliance_with_content.select(
            col("METADATA")['doc_id'].astype('string').alias("DOC_ID"),
            col("METADATA")['title'].astype('string').alias("TITLE"),
            col("DOC_TYPE"),
            col("METADATA")['organization_number'].astype('string').alias("ORGANIZATION_NUMBER"),
            col("METADATA")['company_name'].astype('string').alias("COMPANY_NAME"),
            col("GENERATED_CONTENT").alias("CONTENT_MD"),
            col("CREATED_AT"),
            col("METADATA")['keywords'].astype('string').alias("KEYWORDS"),
            col("MODEL_USED"),
            col("GENERATION_TIMESTAMP")
        )
        
        # Save using save_as_table
        compliance_documents.write.mode("overwrite").save_as_table("BANK.COMPLIANCE_DOCUMENTS", table_type="")
        
        compliance_count = compliance_documents.count()
        logger.info(f"✓ Processed {compliance_count} compliance documents")
        
        return compliance_count
    
    def _create_economic_prompt(self, area_data: Dict, doc_type: str) -> str:
        """Create prompts for economic document generation"""
        
        municipality = area_data['MUNICIPALITY']
        customer_count = area_data.get('customer_count', 0)
        avg_balance = area_data.get('avg_balance', 0)
        
        base_context = f"""
        Generate a comprehensive Norwegian economic analysis document in English markdown format.
        
        Regional Focus:
        - Municipality: {municipality}
        - Banking customers: {customer_count:,}
        - Average account balance: {avg_balance:,.0f} NOK
        
        Important: Generate professional economic analysis that would be typical for Norwegian regional banking.
        Include specific Norwegian economic indicators, housing market data, employment statistics, and regulatory context.
        Use proper markdown formatting with headers, tables, charts, and structured analysis.
        Reference Norwegian economic institutions, regulations, and market conditions where relevant.
        """
        
        prompts = {
            'HOUSING_REPORT': f"{base_context}\nGenerate a detailed housing market report for {municipality}. Include property price trends, housing supply/demand, mortgage market conditions, construction activity, and residential investment patterns. Analyze factors affecting housing affordability and market outlook.",
            
            'EMPLOYMENT_DATA': f"{base_context}\nGenerate a comprehensive employment and labor market analysis for {municipality}. Include unemployment rates, job growth trends, sector employment, wage levels, skills demand, and economic development initiatives affecting local employment.",
            
            'MARKET_ANALYSIS': f"{base_context}\nGenerate a detailed market analysis covering economic conditions in {municipality}. Include GDP growth, business activity, retail trends, consumer spending patterns, economic indicators, and market opportunities for financial services.",
            
            'REGIONAL_ECONOMIC_OUTLOOK': f"{base_context}\nGenerate a forward-looking economic outlook for {municipality} region. Include growth projections, investment trends, demographic changes, infrastructure development, and factors affecting regional economic competitiveness.",
            
            'SECTOR_ANALYSIS': f"{base_context}\nGenerate a comprehensive sector analysis for key industries in {municipality}. Include manufacturing, services, technology, maritime, energy, and other significant sectors. Analyze employment impact, growth prospects, and financing needs.",
            
            'MORTGAGE_MARKET_REPORT': f"{base_context}\nGenerate a detailed mortgage market report for {municipality}. Include lending volumes, interest rate trends, default rates, refinancing activity, regulatory changes, and mortgage market outlook for the region."
        }
        
        return prompts.get(doc_type, prompts['MARKET_ANALYSIS'])
    
    def _create_compliance_prompt(self, entity: Dict, doc_type: str) -> str:
        """Create prompts for compliance document generation"""
        
        org_number = entity['ORGANIZATION_NUMBER']
        company_name = entity['COMPANY_NAME']
        business_activity = entity['BUSINESS_ACTIVITY_DESC']
        employee_count = entity.get('EMPLOYEE_COUNT', 0)
        
        base_context = f"""
        Generate a professional Norwegian compliance document in English markdown format.
        
        Entity Details:
        - Organization Number: {org_number}
        - Company Name: {company_name}
        - Business Activity: {business_activity}
        - Employee Count: {employee_count}
        
        Important: Generate detailed compliance analysis typical for Norwegian financial institutions.
        Include Norwegian regulatory requirements, AML/KYC procedures, beneficial ownership analysis, and risk assessments.
        Use proper markdown formatting with structured sections, risk matrices, and compliance recommendations.
        Reference Norwegian laws, regulations (including EU directives), and compliance frameworks.
        """
        
        prompts = {
            'KYC_REPORT': f"{base_context}\nGenerate a comprehensive Know Your Customer (KYC) report for this Norwegian entity. Include identity verification, business verification, ownership structure analysis, source of funds assessment, and ongoing monitoring recommendations.",
            
            'AML_ASSESSMENT': f"{base_context}\nGenerate a detailed Anti-Money Laundering (AML) risk assessment. Include transaction monitoring results, suspicious activity analysis, risk scoring, regulatory compliance status, and AML program effectiveness evaluation.",
            
            'BENEFICIAL_OWNERSHIP': f"{base_context}\nGenerate a beneficial ownership analysis report. Include ownership structure mapping, ultimate beneficial owner identification, control mechanisms analysis, Norwegian UBO register compliance, and ownership change monitoring.",
            
            'SANCTIONS_SCREENING': f"{base_context}\nGenerate a sanctions screening report covering Norwegian and international sanctions lists. Include PEP screening, adverse media checks, sanctions compliance status, and ongoing monitoring procedures.",
            
            'RISK_PROFILE': f"{base_context}\nGenerate a comprehensive risk profile assessment for this entity. Include credit risk, operational risk, compliance risk, reputational risk, and overall risk rating with mitigation recommendations.",
            
            'COMPLIANCE_REVIEW': f"{base_context}\nGenerate a compliance review report covering regulatory adherence. Include Norwegian financial regulations compliance, EU directives implementation, internal controls assessment, and compliance program recommendations."
        }
        
        return prompts.get(doc_type, prompts['COMPLIANCE_REVIEW'])
    
    def _extract_economic_keywords(self, area_data: Dict, doc_type: str) -> str:
        """Extract keywords for economic documents"""
        keywords = [
            area_data['MUNICIPALITY'].lower(),
            doc_type.lower().replace('_', ' '),
            'norwegian economy', 'regional analysis', 'market conditions'
        ]
        return ', '.join([k for k in keywords if k])
    
    def _extract_compliance_keywords(self, entity: Dict, doc_type: str) -> str:
        """Extract keywords for compliance documents"""
        keywords = [
            entity['BUSINESS_ACTIVITY_DESC'].lower() if entity['BUSINESS_ACTIVITY_DESC'] else '',
            doc_type.lower().replace('_', ' '),
            'compliance', 'norwegian regulation', 'aml kyc', 'risk assessment'
        ]
        return ', '.join([k for k in keywords if k])
    
    def _create_prompt_dict(self, prompt_id: str, prompt_type: str, prompt_text: str, metadata: Dict, 
                           doc_type: str = None, municipality: str = None, region: str = None,
                           organization_number: str = None, company_name: str = None) -> Dict:
        """Create a properly structured prompt dictionary that matches the PROMPTS table schema"""
        # Store Banking-specific fields in metadata
        enhanced_metadata = metadata.copy()
        if region:
            enhanced_metadata['region'] = region
        if organization_number:
            enhanced_metadata['organization_number'] = organization_number
        if company_name:
            enhanced_metadata['company_name'] = company_name
            
        return {
            'PROMPT_ID': prompt_id,
            'PROMPT_TYPE': prompt_type,
            'DOC_TYPE': doc_type,
            'CLAIM_ID': None,  # Not applicable for Banking docs
            'POLICY_ID': None,  # Not applicable for Banking docs
            'MUNICIPALITY': municipality,
            'PROMPT_TEXT': prompt_text,
            'MODEL_TO_USE': self.default_model,
            'TEMPERATURE': self.temperature,
            'MAX_TOKENS': self.max_tokens,
            'SEED': None,
            'CREATED_AT': int(datetime.now().timestamp() * 1000000),
            'METADATA': enhanced_metadata
        }
    
    def _generate_golden_economic_prompts(self, customer_data: List[Dict], doc_types: List[str]) -> List[Dict]:
        """Generate golden economic document prompts for test queries"""
        golden_prompts = []
        
        # Find key municipalities for economic test queries
        oslo_data = next((d for d in customer_data if d['MUNICIPALITY'] == 'Oslo'), None)
        bergen_data = next((d for d in customer_data if d['MUNICIPALITY'] == 'Bergen'), None)
        stavanger_data = next((d for d in customer_data if d['MUNICIPALITY'] == 'Stavanger'), None)
        
        doc_counter = 1
        
        # Oslo housing market analysis (for test query "housing market conditions in Oslo")
        if oslo_data:
            for doc_type in ['HOUSING_REPORT', 'EMPLOYMENT_DATA']:
                prompt_text = self._create_economic_prompt(oslo_data, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_ECON_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'ECONOMIC_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': None,
                    'POLICY_ID': None,
                    'MUNICIPALITY': oslo_data['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': f"ECON_{doc_counter:06d}",
                        'title': f"{doc_type.replace('_', ' ').title()} - {oslo_data['MUNICIPALITY']}",
                        'keywords': self._extract_economic_keywords(oslo_data, doc_type),
                        'region': oslo_data.get('CITY', oslo_data['MUNICIPALITY'])
                    }
                })
                doc_counter += 1
        
        # Bergen market analysis (for test query "Bergen market conditions")
        if bergen_data:
            doc_type = 'MARKET_ANALYSIS'
            prompt_text = self._create_economic_prompt(bergen_data, doc_type)
            golden_prompts.append({
                'PROMPT_ID': f"GOLDEN_ECON_DOC_{doc_counter:03d}",
                'PROMPT_TYPE': 'ECONOMIC_DOCUMENT',
                'DOC_TYPE': doc_type,
                'CLAIM_ID': None,
                'POLICY_ID': None,
                'MUNICIPALITY': bergen_data['MUNICIPALITY'],
                'PROMPT_TEXT': prompt_text,
                'MODEL_TO_USE': self.default_model,
                'TEMPERATURE': self.temperature,
                'MAX_TOKENS': self.max_tokens,
                'SEED': None,
                'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                'METADATA': {
                    'doc_id': f"ECON_{doc_counter:06d}",
                    'title': f"{doc_type.replace('_', ' ').title()} - {bergen_data['MUNICIPALITY']}",
                    'keywords': self._extract_economic_keywords(bergen_data, doc_type),
                    'region': bergen_data.get('CITY', bergen_data['MUNICIPALITY'])
                }
            })
            doc_counter += 1
        
        # Stavanger sector analysis (for test query "Stavanger economic outlook")
        if stavanger_data:
            doc_type = 'SECTOR_ANALYSIS'
            prompt_text = self._create_economic_prompt(stavanger_data, doc_type)
            golden_prompts.append({
                'PROMPT_ID': f"GOLDEN_ECON_DOC_{doc_counter:03d}",
                'PROMPT_TYPE': 'ECONOMIC_DOCUMENT',
                'DOC_TYPE': doc_type,
                'CLAIM_ID': None,
                'POLICY_ID': None,
                'MUNICIPALITY': stavanger_data['MUNICIPALITY'],
                'PROMPT_TEXT': prompt_text,
                'MODEL_TO_USE': self.default_model,
                'TEMPERATURE': self.temperature,
                'MAX_TOKENS': self.max_tokens,
                'SEED': None,
                'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                'METADATA': {
                    'doc_id': f"ECON_{doc_counter:06d}",
                    'title': f"{doc_type.replace('_', ' ').title()} - {stavanger_data['MUNICIPALITY']}",
                    'keywords': self._extract_economic_keywords(stavanger_data, doc_type),
                    'region': stavanger_data.get('CITY', stavanger_data['MUNICIPALITY'])
                }
            })
            doc_counter += 1
        
        return golden_prompts
    
    def _generate_golden_compliance_prompts(self, corporate_data: List[Dict], doc_types: List[str]) -> List[Dict]:
        """Generate golden compliance document prompts for test queries"""
        golden_prompts = []
        
        # Select entities for different compliance scenarios
        entities_sample = corporate_data[:5]  # Use first 5 entities for golden documents
        
        doc_counter = 1
        
        for entity in entities_sample:
            # Generate KYC and AML documents for each entity
            for doc_type in ['KYC_REPORT', 'AML_ASSESSMENT']:
                prompt_text = self._create_compliance_prompt(entity, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_COMP_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'COMPLIANCE_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': None,
                    'POLICY_ID': None,
                    'MUNICIPALITY': None,
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': f"COMP_{doc_counter:06d}",
                        'title': f"{doc_type.replace('_', ' ').title()} - {entity['COMPANY_NAME']}",
                        'keywords': self._extract_compliance_keywords(entity, doc_type),
                        'organization_number': entity['ORGANIZATION_NUMBER'],
                        'company_name': entity['COMPANY_NAME']
                    }
                })
                doc_counter += 1
                
                # Only generate 2 documents per entity to keep golden set manageable
                if doc_counter > 10:
                    break
            
            if doc_counter > 10:
                break
        
        return golden_prompts
    
    def run_banking_document_generation(self):
        """Execute Banking document generation workflow"""
        logger.info("Starting Banking Document Generation...")
        
        try:
            self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Process economic documents
            economic_count = self.process_economic_documents()
            
            # Process compliance documents
            compliance_count = self.process_compliance_documents()
            
            # Validation
            logger.info("=== Validation Summary ===")
            logger.info(f"✓ Economic documents processed: {economic_count:,}")
            logger.info(f"✓ Compliance documents processed: {compliance_count:,}")
            logger.info("✓ All prompts stored in CONTROL.PROMPTS for audit trail")
            logger.info("Banking Document Generation completed successfully!")
            logger.info("Ready for Cortex Search service creation")
            
        except Exception as e:
            logger.error(f"Banking document generation failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Banking Documents")
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
    
    try:
        generator = BankingDocumentGenerator(connection_name=args.connection)
        generator.run_banking_document_generation()
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
