#!/usr/bin/env python3
"""
Snowdrift Financials - M4: Unstructured Content Generation
Document generation using PROMPTS table and proper Complete workflow
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
        logging.FileHandler('snowdrift_documents.log')
    ]
)
logger = logging.getLogger(__name__)

class DocumentGenerator:
    """Document generation using PROMPTS table and configurable models"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.connection_name = connection_name
        self.session = None
        self.owns_session = True  # Track if we own the session
        
        # Document generation settings
        insurance_config = self.config.get('insurance', {})
        unstructured_config = insurance_config.get('unstructured_data', {})
        content_config = insurance_config.get('content_generation', {})
        
        self.claims_target = unstructured_config.get('claims_documents', 150)
        self.underwriting_target = unstructured_config.get('underwriting_documents', 120)
        
        # Model configuration
        self.default_model = content_config.get('default_model', 'claude-4-sonnet')
        self.fallback_model = content_config.get('fallback_model', 'llama3.1-8b')
        self.temperature = content_config.get('temperature', 0.3)
        self.max_tokens = content_config.get('max_tokens', 2000)
        
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
                logger.info(f"✓ Saved {num_rows} records in {num_chunks} chunks to {schema}.{table_name}")
            else:
                logger.error(f"Failed to save data to {table_name}")
                raise Exception(f"Failed to save to {table_name}")
        else:
            logger.info(f"✓ Saved {len(df)} records to {schema}.{table_name}")
        
        return self.session.table(f"{schema}.{table_name}")
    
    def get_sample_claims_data(self) -> List[Dict]:
        """Get sample claims data to base documents on"""
        logger.info("Fetching sample claims data...")
        
        # First, ensure we get our golden claims
        golden_claims_df = self.session.sql("""
            SELECT 
                CLAIM_ID,
                POLICY_ID,
                LOSS_DATE,
                REPORTED_DATE,
                DESCRIPTION,
                STATUS,
                CLAIM_AMOUNT,
                ADDRESS_LINE1,
                CITY,
                MUNICIPALITY
            FROM INSURANCE.CLAIMS 
            WHERE CLAIM_ID IN ('CLM-014741', 'CLM-003812', 'CLM-002456', 'CLM-005789', 'CLM-001234')
            ORDER BY CLAIM_ID
        """).to_pandas()
        
        # Then get the rest of the claims
        other_claims_df = self.session.sql("""
            SELECT 
                CLAIM_ID,
                POLICY_ID,
                LOSS_DATE,
                REPORTED_DATE,
                DESCRIPTION,
                STATUS,
                CLAIM_AMOUNT,
                ADDRESS_LINE1,
                CITY,
                MUNICIPALITY
            FROM INSURANCE.CLAIMS 
            WHERE CLAIM_ID NOT IN ('CLM-014741', 'CLM-003812', 'CLM-002456', 'CLM-005789', 'CLM-001234')
            ORDER BY RANDOM()
            LIMIT 195
        """).to_pandas()
        
        # Combine golden claims + random claims
        all_claims_df = pd.concat([golden_claims_df, other_claims_df], ignore_index=True)
        logger.info(f"Retrieved {len(golden_claims_df)} golden claims and {len(other_claims_df)} random claims")
        
        return all_claims_df.to_dict('records')
    
    def get_sample_policy_data(self) -> List[Dict]:
        """Get sample policy data to base underwriting documents on"""
        logger.info("Fetching sample policy data...")
        
        policies_df = self.session.sql("""
            SELECT 
                p.POLICY_ID,
                p.CUSTOMER_ID,
                p.POLICY_TYPE,
                p.PREMIUM,
                p.COVERAGE_AMOUNT,
                p.ADDRESS_LINE1,
                p.CITY,
                p.MUNICIPALITY,
                g.FLOOD_RISK_SCORE
            FROM INSURANCE.POLICIES p
            JOIN INSURANCE.GEO_RISK_SCORES g 
                ON p.MUNICIPALITY = g.MUNICIPALITY
            ORDER BY RANDOM() 
            LIMIT 150
        """).to_pandas()
        
        return policies_df.to_dict('records')
    
    def generate_claims_prompts(self) -> pd.DataFrame:
        """Generate all prompts for claims documents and store in PROMPTS table"""
        logger.info("Generating prompts for claims documents...")
        
        # Get sample claims data
        sample_claims = self.get_sample_claims_data()
        
        prompts = []
        doc_types = [
            'POLICE_REPORT', 'MEDICAL_REPORT', 'WITNESS_STATEMENT', 
            'ADJUSTER_REPORT', 'PROPERTY_ASSESSMENT', 'INCIDENT_REPORT'
        ]
        
        # FIRST: Generate golden documents for our test claims
        logger.info("Generating golden documents for test claims...")
        golden_prompts = self._generate_golden_claims_prompts(sample_claims, doc_types)
        prompts.extend(golden_prompts)
        logger.info(f"✓ Generated {len(golden_prompts)} golden claims documents")
        
        # THEN: Generate the rest randomly
        for i in range(len(golden_prompts), self.claims_target):
            if i % 50 == 0:
                logger.info(f"Generated {i} claims prompts...")
            
            # Select random claim and document type
            claim = random.choice(sample_claims)
            doc_type = random.choice(doc_types)
            
            # Create prompt based on document type
            prompt_text = self._create_claims_prompt(claim, doc_type)
            
            metadata = {
                'doc_id': f"CLAIMS_{i+1:06d}",
                'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                'keywords': self._extract_keywords(claim, doc_type)
            }
            prompts.append(self._create_prompt_dict(
                prompt_id=f"CLAIMS_DOC_{i+1:06d}",
                prompt_type='CLAIMS_DOCUMENT',
                prompt_text=prompt_text,
                metadata=metadata,
                doc_type=doc_type,
                claim_id=claim['CLAIM_ID'],
                policy_id=claim['POLICY_ID'],
                municipality=claim['MUNICIPALITY']
            ))
        
        logger.info(f"Generated {len(prompts)} claims prompts")
        return pd.DataFrame(prompts)
    
    def generate_underwriting_prompts(self) -> pd.DataFrame:
        """Generate all prompts for underwriting documents and store in PROMPTS table"""
        logger.info("Generating prompts for underwriting documents...")
        
        # Get sample policy data
        sample_policies = self.get_sample_policy_data()
        
        prompts = []
        doc_types = [
            'FLOOD_RISK_ASSESSMENT', 'PROPERTY_INSPECTION', 'MARKET_ANALYSIS',
            'UNDERWRITING_MEMO', 'RISK_BULLETIN', 'ENVIRONMENTAL_REPORT'
        ]
        
        # FIRST: Generate golden underwriting documents for test queries
        logger.info("Generating golden underwriting documents for test queries...")
        golden_uw_prompts = self._generate_golden_underwriting_prompts(sample_policies, doc_types)
        prompts.extend(golden_uw_prompts)
        logger.info(f"✓ Generated {len(golden_uw_prompts)} golden underwriting documents")
        
        # THEN: Generate the rest randomly
        for i in range(len(golden_uw_prompts), self.underwriting_target):
            if i % 50 == 0:
                logger.info(f"Generated {i} underwriting prompts...")
            
            # Select random policy and document type
            policy = random.choice(sample_policies)
            doc_type = random.choice(doc_types)
            
            # Create prompt based on document type
            prompt_text = self._create_underwriting_prompt(policy, doc_type)
            
            metadata = {
                'doc_id': f"UW_{i+1:06d}",
                'title': f"{doc_type.replace('_', ' ').title()} - {policy['MUNICIPALITY']}",
                'keywords': self._extract_underwriting_keywords(policy, doc_type),
                'flood_risk_score': policy['FLOOD_RISK_SCORE']  # Store in metadata instead
            }
            prompts.append(self._create_prompt_dict(
                prompt_id=f"UW_DOC_{i+1:06d}",
                prompt_type='UNDERWRITING_DOCUMENT',
                prompt_text=prompt_text,
                metadata=metadata,
                doc_type=doc_type,
                policy_id=policy.get('POLICY_ID'),
                municipality=policy['MUNICIPALITY']
            ))
        
        logger.info(f"Generated {len(prompts)} underwriting prompts")
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
    
    def process_claims_documents(self):
        """Process claims documents using proper workflow"""
        logger.info("=== Processing Claims Documents ===")
        
        # Step 1: Generate prompts
        logger.info("Step 1: Generating claims prompts...")
        claims_prompts_df = self.generate_claims_prompts()
        
        # Step 2: Save prompts to PROMPTS table
        logger.info("Step 2: Saving prompts to CONTROL.PROMPTS...")
        self.save_to_snowflake(claims_prompts_df, "PROMPTS", "CONTROL")
        
        # Step 3: Create Snowpark DataFrame from prompts
        logger.info("Step 3: Creating Snowpark DataFrame from claims prompts...")
        claims_prompts_snowpark = self.session.table("CONTROL.PROMPTS").filter(
            col("PROMPT_TYPE") == "CLAIMS_DOCUMENT"
        )
        
        # Step 4: Execute Complete using with_column
        logger.info("Step 4: Executing Complete on claims prompts...")
        claims_with_content = self.execute_complete_with_fallback(claims_prompts_snowpark)
        
        # Step 5: Transform and save to final table
        logger.info("Step 5: Saving claims documents...")
        claims_documents = claims_with_content.select(
            col("METADATA")['doc_id'].astype('string').alias("DOC_ID"),
            col("METADATA")['title'].astype('string').alias("TITLE"),
            col("DOC_TYPE"),
            col("CLAIM_ID"),
            col("POLICY_ID"),
            col("MUNICIPALITY"),
            col("GENERATED_CONTENT").alias("CONTENT_MD"),
            col("CREATED_AT"),
            col("METADATA")['keywords'].astype('string').alias("KEYWORDS"),
            col("MODEL_USED"),
            col("GENERATION_TIMESTAMP")
        )
        
        # Save using save_as_table
        claims_documents.write.mode("overwrite").save_as_table("INSURANCE.CLAIMS_DOCUMENTS", table_type="")
        
        claims_count = claims_documents.count()
        logger.info(f"✓ Processed {claims_count} claims documents")
        
        return claims_count
    
    def process_underwriting_documents(self):
        """Process underwriting documents using proper workflow"""
        logger.info("=== Processing Underwriting Documents ===")
        
        # Step 1: Generate prompts
        logger.info("Step 1: Generating underwriting prompts...")
        uw_prompts_df = self.generate_underwriting_prompts()
        
        # Step 2: Save prompts to PROMPTS table (append mode)
        logger.info("Step 2: Appending prompts to CONTROL.PROMPTS...")
        # Convert to Snowpark DataFrame and append
        uw_prompts_snowpark = self.session.create_dataframe(uw_prompts_df)
        uw_prompts_snowpark.write.mode("append").save_as_table("CONTROL.PROMPTS", table_type="")
        
        # Step 3: Create Snowpark DataFrame from prompts
        logger.info("Step 3: Creating Snowpark DataFrame from underwriting prompts...")
        uw_prompts_from_table = self.session.table("CONTROL.PROMPTS").filter(
            col("PROMPT_TYPE") == "UNDERWRITING_DOCUMENT"
        )
        
        # Step 4: Execute Complete using with_column
        logger.info("Step 4: Executing Complete on underwriting prompts...")
        uw_with_content = self.execute_complete_with_fallback(uw_prompts_from_table)
        
        # Step 5: Transform and save to final table
        logger.info("Step 5: Saving underwriting documents...")
        uw_documents = uw_with_content.select(
            col("METADATA")['doc_id'].astype('string').alias("DOC_ID"),
            col("METADATA")['title'].astype('string').alias("TITLE"),
            col("DOC_TYPE"),
            col("POLICY_ID"),
            col("MUNICIPALITY"),
            lit(5).alias("FLOOD_RISK_SCORE"),  # Default flood risk score for demo
            col("GENERATED_CONTENT").alias("CONTENT_MD"),
            col("CREATED_AT"),
            col("METADATA")['keywords'].astype('string').alias("KEYWORDS"),
            col("MODEL_USED"),
            col("GENERATION_TIMESTAMP")
        )
        
        # Save using save_as_table
        uw_documents.write.mode("overwrite").save_as_table("INSURANCE.UNDERWRITING_DOCUMENTS", table_type="")
        
        uw_count = uw_documents.count()
        logger.info(f"✓ Processed {uw_count} underwriting documents")
        
        return uw_count
    
    def _create_claims_prompt(self, claim: Dict, doc_type: str) -> str:
        """Create prompts for claims document generation"""
        
        base_context = f"""
        Generate a realistic Norwegian insurance document in English markdown format.
        
        Claim Details:
        - Claim ID: {claim['CLAIM_ID']}
        - Location: {claim['ADDRESS_LINE1']}, {claim['CITY']}, {claim['MUNICIPALITY']}
        - Loss Date: {claim['LOSS_DATE']}
        - Description: {claim['DESCRIPTION']}
        - Amount: {claim['CLAIM_AMOUNT']} NOK
        
        Important: Generate a professional, detailed document that would be typical in Norwegian insurance operations.
        Use proper markdown formatting with headers, lists, and structured content.
        Include realistic Norwegian names, addresses, and references where appropriate.
        """
        
        prompts = {
            'POLICE_REPORT': f"{base_context}\nGenerate a Norwegian police incident report for this insurance claim. Include officer details, incident timeline, witness information, and official conclusions. Format as a formal police report with proper sections and official language.",
            
            'MEDICAL_REPORT': f"{base_context}\nGenerate a comprehensive medical assessment report for injuries related to this claim. Include patient examination findings, diagnosis, treatment recommendations, prognosis, and follow-up care. Format as a professional medical report.",
            
            'WITNESS_STATEMENT': f"{base_context}\nGenerate a detailed witness statement from someone who observed the incident. Include personal details, comprehensive account of events, timeline, and signature block. Format as a formal witness statement.",
            
            'ADJUSTER_REPORT': f"{base_context}\nGenerate a thorough insurance adjuster's assessment report. Include property damage evaluation, cause analysis, liability assessment, repair estimates, and settlement recommendations. Format as a professional adjuster report.",
            
            'PROPERTY_ASSESSMENT': f"{base_context}\nGenerate a detailed property damage assessment report. Include structural damage analysis, repair cost estimates, replacement values, and recommendations. Format as a comprehensive property assessment.",
            
            'INCIDENT_REPORT': f"{base_context}\nGenerate a comprehensive incident report documenting the circumstances of the loss. Include detailed timeline, contributing factors, witness accounts, and preventive measures. Format as a professional incident report."
        }
        
        return prompts.get(doc_type, prompts['INCIDENT_REPORT'])
    
    def _create_underwriting_prompt(self, policy: Dict, doc_type: str) -> str:
        """Create prompts for underwriting document generation"""
        
        base_context = f"""
        Generate a realistic Norwegian insurance underwriting document in English markdown format.
        
        Property Details:
        - Location: {policy['ADDRESS_LINE1']}, {policy['CITY']}, {policy['MUNICIPALITY']}
        - Policy Type: {policy['POLICY_TYPE']}
        - Coverage: {policy['COVERAGE_AMOUNT']} NOK
        - Flood Risk Score: {policy['FLOOD_RISK_SCORE']}/10
        
        Important: Generate a professional, analytical document typical of Norwegian insurance underwriting.
        Include specific Norwegian geographic, climate, and regulatory considerations.
        Use proper markdown formatting with headers, data tables, and structured analysis.
        Reference Norwegian building codes, climate patterns, and insurance regulations where relevant.
        """
        
        prompts = {
            'FLOOD_RISK_ASSESSMENT': f"{base_context}\nGenerate a comprehensive flood risk assessment for this Norwegian municipality. Include historical flood data, topographical analysis, climate projections, seasonal patterns, drainage systems, and detailed risk mitigation recommendations specific to Norwegian conditions.",
            
            'PROPERTY_INSPECTION': f"{base_context}\nGenerate a thorough property inspection report for underwriting purposes. Include building condition assessment, construction materials analysis, maintenance status, compliance with Norwegian building codes, risk factors, and recommendations.",
            
            'MARKET_ANALYSIS': f"{base_context}\nGenerate a detailed market analysis for this Norwegian region. Include property values trends, economic indicators, demographic patterns, development projects, insurance market conditions, and outlook for the Norwegian insurance sector.",
            
            'UNDERWRITING_MEMO': f"{base_context}\nGenerate a comprehensive underwriting memo with detailed risk assessment and pricing recommendations. Include risk factor analysis, competitive market analysis, Norwegian regulatory considerations, and approval recommendations with rationale.",
            
            'RISK_BULLETIN': f"{base_context}\nGenerate a risk bulletin highlighting emerging risks in this Norwegian region. Include weather pattern changes, environmental developments, regulatory updates, industry trends, and recommendations for risk management.",
            
            'ENVIRONMENTAL_REPORT': f"{base_context}\nGenerate a detailed environmental risk report for this location. Include pollution risk assessment, natural hazard analysis, climate change impacts, regulatory compliance, environmental trends specific to Norway, and risk mitigation strategies."
        }
        
        return prompts.get(doc_type, prompts['RISK_BULLETIN'])
    
    def _extract_keywords(self, claim: Dict, doc_type: str) -> str:
        """Extract keywords for claims documents"""
        keywords = [
            claim['MUNICIPALITY'].lower(),
            doc_type.lower().replace('_', ' '),
            claim['STATUS'].lower() if claim['STATUS'] else '',
            'damage', 'assessment', 'investigation', 'norwegian insurance'
        ]
        return ', '.join([k for k in keywords if k])
    
    def _extract_underwriting_keywords(self, policy: Dict, doc_type: str) -> str:
        """Extract keywords for underwriting documents"""
        keywords = [
            policy['MUNICIPALITY'].lower(),
            policy['POLICY_TYPE'].lower(),
            doc_type.lower().replace('_', ' '),
            'flood risk' if policy['FLOOD_RISK_SCORE'] > 6 else 'low risk',
            'underwriting', 'assessment', 'norwegian insurance'
        ]
        return ', '.join([k for k in keywords if k])
    
    def _create_prompt_dict(self, prompt_id: str, prompt_type: str, prompt_text: str, metadata: Dict, 
                           doc_type: str = None, claim_id: str = None, policy_id: str = None, 
                           municipality: str = None) -> Dict:
        """Create a properly structured prompt dictionary that matches the PROMPTS table schema"""
        return {
            'PROMPT_ID': prompt_id,
            'PROMPT_TYPE': prompt_type,
            'DOC_TYPE': doc_type,
            'CLAIM_ID': claim_id,
            'POLICY_ID': policy_id,
            'MUNICIPALITY': municipality,
            'PROMPT_TEXT': prompt_text,
            'MODEL_TO_USE': self.default_model,
            'TEMPERATURE': self.temperature,
            'MAX_TOKENS': self.max_tokens,
            'SEED': None,
            'CREATED_AT': int(datetime.now().timestamp() * 1000000),
            'METADATA': metadata
        }
    
    def _generate_golden_claims_prompts(self, sample_claims: List[Dict], doc_types: List[str]) -> List[Dict]:
        """Generate golden document prompts for our test claims"""
        golden_prompts = []
        
        # Find our golden claims
        golden_claims_dict = {}
        
        for claim in sample_claims:
            claim_id = claim['CLAIM_ID']
            if claim_id in ['CLM-014741', 'CLM-003812', 'CLM-002456', 'CLM-005789', 'CLM-001234']:
                golden_claims_dict[claim_id] = claim
                logger.info(f"✓ Found golden claim {claim_id}: {claim['DESCRIPTION']} in {claim['MUNICIPALITY']}")
        
        # Warn if any golden claims are missing
        expected_claims = ['CLM-014741', 'CLM-003812', 'CLM-002456', 'CLM-005789', 'CLM-001234']
        for claim_id in expected_claims:
            if claim_id not in golden_claims_dict:
                logger.warning(f"Golden claim {claim_id} not found in sample claims!")
        
        # Generate documents for each golden claim based on test query requirements
        doc_counter = 1
        
        # CLM-014741: Main demo claim (motor vehicle accident with injuries, Kristiansand)
        if 'CLM-014741' in golden_claims_dict:
            claim = golden_claims_dict['CLM-014741']
            demo_docs = [
                ('POLICE_REPORT', f'CLAIMS_{doc_counter:06d}'),  # Referenced in agent guide
                ('MEDICAL_REPORT', f'CLAIMS_{doc_counter+1:06d}'),
                ('PROPERTY_ASSESSMENT', f'CLAIMS_{doc_counter+2:06d}'),
                ('INCIDENT_REPORT', f'CLAIMS_{doc_counter+3:06d}')
            ]
            
            for doc_type, doc_id in demo_docs:
                prompt_text = self._create_claims_prompt(claim, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_CLAIMS_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'CLAIMS_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': claim['CLAIM_ID'],
                    'POLICY_ID': claim['POLICY_ID'],
                    'MUNICIPALITY': claim['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': doc_id,
                        'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                        'keywords': self._extract_keywords(claim, doc_type)
                    }
                })
                doc_counter += 1
        
        # CLM-003812: Inconsistency testing claim (flooding, Bergen)
        if 'CLM-003812' in golden_claims_dict:
            claim = golden_claims_dict['CLM-003812']
            demo_docs = [
                ('POLICE_REPORT', f'CLAIMS_{doc_counter:06d}'),
                ('WITNESS_STATEMENT', f'CLAIMS_{doc_counter+1:06d}')
            ]
            
            for doc_type, doc_id in demo_docs:
                prompt_text = self._create_claims_prompt(claim, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_CLAIMS_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'CLAIMS_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': claim['CLAIM_ID'],
                    'POLICY_ID': claim['POLICY_ID'],
                    'MUNICIPALITY': claim['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': doc_id,
                        'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                        'keywords': self._extract_keywords(claim, doc_type)
                    }
                })
                doc_counter += 1
        
        # CLM-002456: Vehicle accident with medical injuries (Oslo)
        if 'CLM-002456' in golden_claims_dict:
            claim = golden_claims_dict['CLM-002456']
            demo_docs = [
                ('MEDICAL_REPORT', f'CLAIMS_{doc_counter:06d}'),  # For "medical injuries in vehicle accidents"
                ('POLICE_REPORT', f'CLAIMS_{doc_counter+1:06d}'),
                ('INCIDENT_REPORT', f'CLAIMS_{doc_counter+2:06d}')
            ]
            
            for doc_type, doc_id in demo_docs:
                prompt_text = self._create_claims_prompt(claim, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_CLAIMS_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'CLAIMS_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': claim['CLAIM_ID'],
                    'POLICY_ID': claim['POLICY_ID'],
                    'MUNICIPALITY': claim['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': doc_id,
                        'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                        'keywords': self._extract_keywords(claim, doc_type)
                    }
                })
                doc_counter += 1
        
        # CLM-005789: Medical claim with fraud indicators (Oslo)
        if 'CLM-005789' in golden_claims_dict:
            claim = golden_claims_dict['CLM-005789']
            demo_docs = [
                ('MEDICAL_REPORT', f'CLAIMS_{doc_counter:06d}'),  # For "medical information in Oslo"
                ('ADJUSTER_REPORT', f'CLAIMS_{doc_counter+1:06d}')  # For "fraud indicators"
            ]
            
            for doc_type, doc_id in demo_docs:
                prompt_text = self._create_claims_prompt(claim, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_CLAIMS_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'CLAIMS_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': claim['CLAIM_ID'],
                    'POLICY_ID': claim['POLICY_ID'],
                    'MUNICIPALITY': claim['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': doc_id,
                        'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                        'keywords': self._extract_keywords(claim, doc_type)
                    }
                })
                doc_counter += 1
        
        # CLM-001234: Vehicle collision with medical injuries
        if 'CLM-001234' in golden_claims_dict:
            claim = golden_claims_dict['CLM-001234']
            demo_docs = [
                ('MEDICAL_REPORT', f'CLAIMS_{doc_counter:06d}'),  # For "medical injuries in vehicle accidents"
                ('POLICE_REPORT', f'CLAIMS_{doc_counter+1:06d}')
            ]
            
            for doc_type, doc_id in demo_docs:
                prompt_text = self._create_claims_prompt(claim, doc_type)
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_CLAIMS_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'CLAIMS_DOCUMENT',
                    'DOC_TYPE': doc_type,
                    'CLAIM_ID': claim['CLAIM_ID'],
                    'POLICY_ID': claim['POLICY_ID'],
                    'MUNICIPALITY': claim['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': doc_id,
                        'title': f"{doc_type.replace('_', ' ').title()} - Claim {claim['CLAIM_ID']}",
                        'keywords': self._extract_keywords(claim, doc_type)
                    }
                })
                doc_counter += 1
        
        return golden_prompts
    
    def _generate_golden_underwriting_prompts(self, sample_policies: List[Dict], doc_types: List[str]) -> List[Dict]:
        """Generate golden underwriting document prompts for our test queries"""
        golden_prompts = []
        
        # Find policies in specific municipalities for underwriting test queries
        tromso_policies = [p for p in sample_policies if p['MUNICIPALITY'] == 'Tromsø']
        stavanger_policies = [p for p in sample_policies if p['MUNICIPALITY'] == 'Stavanger']
        kristiansand_policies = [p for p in sample_policies if p['MUNICIPALITY'] == 'Kristiansand']
        bergen_policies = [p for p in sample_policies if p['MUNICIPALITY'] == 'Bergen']
        
        logger.info(f"Found policies: Tromsø={len(tromso_policies)}, Stavanger={len(stavanger_policies)}, Kristiansand={len(kristiansand_policies)}, Bergen={len(bergen_policies)}")
        
        doc_counter = 1
        
        # Environmental reports for Tromsø (for test query "Find adverse environmental reports for Tromsø region")
        if tromso_policies:
            policy = tromso_policies[0]
            for doc_type in ['ENVIRONMENTAL_REPORT', 'RISK_BULLETIN']:
                prompt_text = self._create_underwriting_prompt(policy, doc_type)
                
                metadata = {
                    'doc_id': f"UW_{doc_counter:06d}",
                    'title': f"{doc_type.replace('_', ' ').title()} - {policy['MUNICIPALITY']}",
                    'keywords': self._extract_underwriting_keywords(policy, doc_type)
                }
                golden_prompts.append(self._create_prompt_dict(
                    prompt_id=f"GOLDEN_UW_DOC_{doc_counter:03d}",
                    prompt_type='UNDERWRITING_DOCUMENT',
                    prompt_text=prompt_text,
                    metadata=metadata,
                    doc_type=doc_type,
                    policy_id=policy['POLICY_ID'],
                    municipality=policy['MUNICIPALITY']
                ))
                doc_counter += 1
        
        # Market analysis for Stavanger (for test query "Research market conditions for Stavanger")
        if stavanger_policies:
            policy = stavanger_policies[0]
            for doc_type in ['MARKET_ANALYSIS', 'PROPERTY_INSPECTION']:
                prompt_text = self._create_underwriting_prompt(policy, doc_type)
                
                metadata = {
                    'doc_id': f"UW_{doc_counter:06d}",
                    'title': f"{doc_type.replace('_', ' ').title()} - {policy['MUNICIPALITY']}",
                    'keywords': self._extract_underwriting_keywords(policy, doc_type)
                }
                golden_prompts.append(self._create_prompt_dict(
                    prompt_id=f"GOLDEN_UW_DOC_{doc_counter:03d}",
                    prompt_type='UNDERWRITING_DOCUMENT',
                    prompt_text=prompt_text,
                    metadata=metadata,
                    doc_type=doc_type,
                    policy_id=policy['POLICY_ID'],
                    municipality=policy['MUNICIPALITY']
                ))
                doc_counter += 1
        
        # Flood risk assessments for Kristiansand and Bergen (for comparison test query)
        for municipality, policies in [('Kristiansand', kristiansand_policies), ('Bergen', bergen_policies)]:
            if policies:
                policy = policies[0]
                prompt_text = self._create_underwriting_prompt(policy, 'FLOOD_RISK_ASSESSMENT')
                
                golden_prompts.append({
                    'PROMPT_ID': f"GOLDEN_UW_DOC_{doc_counter:03d}",
                    'PROMPT_TYPE': 'UNDERWRITING_DOCUMENT',
                    'DOC_TYPE': 'FLOOD_RISK_ASSESSMENT',
                    'POLICY_ID': policy['POLICY_ID'],
                    'MUNICIPALITY': policy['MUNICIPALITY'],
                    'PROMPT_TEXT': prompt_text,
                    'MODEL_TO_USE': self.default_model,
                    'TEMPERATURE': self.temperature,
                    'MAX_TOKENS': self.max_tokens,
                    'SEED': None,
                    'CREATED_AT': int(datetime.now().timestamp() * 1000000),
                    'METADATA': {
                        'doc_id': f"UW_{doc_counter:06d}",
                        'title': f"Flood Risk Assessment - {policy['MUNICIPALITY']}",
                        'keywords': self._extract_underwriting_keywords(policy, 'FLOOD_RISK_ASSESSMENT')
                    }
                })
                doc_counter += 1
        
        return golden_prompts
    
    def run_document_generation(self):
        """Execute document generation workflow"""
        logger.info("Starting M4 - Unstructured Content Generation...")
        
        try:
            # Create session only if not already provided
            if self.session is None:
                self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Process claims documents
            claims_count = self.process_claims_documents()
            
            # Process underwriting documents
            uw_count = self.process_underwriting_documents()
            
            # Validation
            logger.info("=== Validation Summary ===")
            logger.info(f"✓ Claims documents processed: {claims_count:,}")
            logger.info(f"✓ Underwriting documents processed: {uw_count:,}")
            logger.info("✓ All prompts stored in CONTROL.PROMPTS for audit trail")
            logger.info("Unstructured Content Generation completed successfully!")
            logger.info("Ready for Cortex Search service creation")
            
        except Exception as e:
            logger.error(f"Document generation failed: {str(e)}")
            raise
        finally:
            # Only close session if we own it (not shared)
            if self.session and self.owns_session:
                self.session.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate Unstructured Documents")
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
        generator = DocumentGenerator(connection_name=args.connection)
        generator.run_document_generation()
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
