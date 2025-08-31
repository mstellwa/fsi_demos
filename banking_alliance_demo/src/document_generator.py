"""
Document generation using Cortex Complete for SnowBank Intelligence Demo
Generates Norwegian industry-specific documents for RAG scenarios
"""

import logging
import uuid
from datetime import datetime
from typing import List, Dict
import random

from snowflake.snowpark import DataFrame
from snowflake.snowpark.functions import col, lit, when, concat_ws
from snowflake.snowpark.types import StructType, StructField, StringType, FloatType
import snowflake.cortex as cortex

from .config import DemoConfig

logger = logging.getLogger(__name__)


class DocumentGenerator:
    """Generates unstructured documents using Cortex Complete"""
    
    # Document scenarios and types
    SCENARIOS = {
        'CLIENT_360': ['CRM_NOTE', 'NEWS'],
        'STRESS_TESTING': ['POLICY'],  
        'GREEN_BOND': ['ANNUAL_REPORT', 'LOAN_DOC', 'THIRD_PARTY'],
        'STRATEGIC_INQUIRY': ['ANNUAL_REPORT', 'QUARTERLY_REPORT']
    }
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
        
    def generate_all_documents(self) -> None:
        """Generate documents for all scenarios"""
        logger.info("Starting document generation...")
        
        # First generate prompts
        self.generate_document_prompts()
        
        # Then generate actual documents using Cortex Complete
        self.generate_documents_from_prompts()
        
        logger.info("Document generation completed")
    
    def generate_document_prompts(self) -> None:
        """Generate prompts for document creation"""
        logger.info("Generating document prompts...")
        
        prompts_data = []
        model_class = self.config.get_config('MODEL_CLASS')
        temperature = 0.7
        
        # Generate prompts for each scenario
        for scenario, doc_types in self.SCENARIOS.items():
            for doc_type in doc_types:
                prompts = self._get_prompts_for_type(scenario, doc_type)
                for prompt_data in prompts:
                    doc_id = str(uuid.uuid4())
                    prompts_data.append((
                        doc_id,
                        scenario,
                        doc_type,
                        prompt_data['target_entity'],
                        prompt_data['prompt_text'],
                        model_class,
                        temperature
                    ))
        
        # Create DataFrame and save
        schema = StructType([
            StructField("DOC_ID", StringType()),
            StructField("SCENARIO", StringType()),
            StructField("DOC_TYPE", StringType()),
            StructField("TARGET_ENTITY", StringType()),
            StructField("PROMPT_TEXT", StringType()),
            StructField("MODEL_CLASS", StringType()),
            StructField("TEMPERATURE", FloatType())
        ])
        
        df = self.session.create_dataframe(prompts_data, schema)
        df.write.mode("overwrite").save_as_table("DOCUMENT_PROMPTS")
        
        logger.info(f"Generated {len(prompts_data)} document prompts")
    
    def _get_prompts_for_type(self, scenario: str, doc_type: str) -> List[Dict]:
        """Get prompts for specific document type"""
        prompts = []
        
        if doc_type == 'CRM_NOTE':
            prompts.extend(self._get_crm_note_prompts())
        elif doc_type == 'NEWS':
            prompts.extend(self._get_news_prompts())
        elif doc_type == 'POLICY':
            prompts.extend(self._get_policy_prompts())
        elif doc_type == 'ANNUAL_REPORT':
            prompts.extend(self._get_annual_report_prompts())
        elif doc_type == 'QUARTERLY_REPORT':
            prompts.extend(self._get_quarterly_report_prompts())
        elif doc_type == 'LOAN_DOC':
            prompts.extend(self._get_loan_doc_prompts())
        elif doc_type == 'THIRD_PARTY':
            prompts.extend(self._get_third_party_prompts())
            
        return prompts
    
    def _get_crm_note_prompts(self) -> List[Dict]:
        """Generate CRM note prompts"""
        companies = [
            "Helio Salmon AS", "Bergen Maritime Services AS", "Nordlys Renewable Energy ASA",
            "Trondheim Tech Solutions AS", "Lofoten Tourism Holdings AS", "Stavanger Oil Services AS",
            "Finnmark Aquaculture AS", "Sunnmøre Shipping AS"
        ]
        
        prompts = []
        for company in companies:
            # Risk-related CRM notes
            prompts.append({
                'target_entity': company,
                'prompt_text': f"""Write a detailed CRM note about a client meeting with {company}. 
                Include discussion about recent operational challenges, specifically mentioning:
                - Algae bloom incidents affecting production
                - New ISA (Infectious Salmon Anemia) regulations from Norwegian FSA
                - Sea lice mitigation requirements and equipment upgrade needs
                - Regional market conditions in Norway
                - Financing needs for regulatory compliance
                
                Format as a professional bank CRM note with date, attendees, and action items.
                Length: 200-300 words."""
            })
            
            # Opportunity-related CRM notes  
            prompts.append({
                'target_entity': company,
                'prompt_text': f"""Write a CRM note documenting a business development opportunity with {company}.
                Include discussion about:
                - Expansion plans in Norwegian regions
                - Green financing opportunities
                - Cross-selling potential for additional banking products
                - Industry-specific financing needs
                - Relationship deepening strategies
                
                Format as a professional bank CRM note with clear next steps.
                Length: 200-300 words."""
            })
        
        return prompts
    
    def _get_news_prompts(self) -> List[Dict]:
        """Generate news article prompts"""
        prompts = [
            {
                'target_entity': 'Norwegian Aquaculture Industry',
                'prompt_text': """Write a news article about new Norwegian FSA regulations affecting aquaculture operations.
                Include specific details about:
                - New sea lice monitoring requirements
                - Equipment upgrade mandates for fish farms
                - Timeline for compliance (18-month implementation period)
                - Estimated industry costs for compliance
                - Impact on smaller vs larger aquaculture operations
                - Regional focus on Helgeland operations
                
                Write in professional financial news style. Length: 400-500 words."""
            },
            {
                'target_entity': 'Norwegian Renewable Energy Sector',
                'prompt_text': """Write a news article about new renewable energy incentives in Norway.
                Include details about:
                - New CO2 reduction targets and timeline
                - Government subsidies for offshore wind projects
                - BREEAM and LEED certification requirements for green buildings
                - Impact on renewable energy financing market
                - Regional development opportunities
                
                Write in professional financial news style. Length: 400-500 words."""
            },
            {
                'target_entity': 'Norwegian Banking Alliance',
                'prompt_text': """Write a news article about Nordic Banking Alliance digital transformation initiatives.
                Include discussion of:
                - SMB digital lending platforms
                - Cross-alliance technology sharing
                - Competitive response to challenger banks
                - Regional bank collaboration benefits
                - Customer experience improvements
                
                Write in professional financial news style. Length: 400-500 words."""
            }
        ]
        
        return prompts
    
    def _get_policy_prompts(self) -> List[Dict]:
        """Generate policy document prompts"""
        prompts = [
            {
                'target_entity': 'Credit Risk Management',
                'prompt_text': """Write a detailed credit policy section on forbearance and restructuring options.
                Include specific clauses about:
                - Payment holiday eligibility criteria (LTV breach situations)
                - Maximum payment holiday duration (6-month standard)
                - Restructuring options for property value declines
                - Interest rate adjustment mechanisms during forbearance
                - Documentation requirements for policy application
                - Regional market considerations for Norwegian properties
                
                Format as formal policy document with numbered sections. Length: 500-600 words."""
            },
            {
                'target_entity': 'LTV Breach Management',
                'prompt_text': """Write a credit policy section on Loan-to-Value breach management procedures.
                Include detailed guidance on:
                - LTV calculation methodologies
                - Property revaluation triggers and frequency  
                - Risk mitigation options when LTV exceeds 85%
                - Forbearance vs restructuring decision criteria
                - Documentation and approval workflows
                - Regional property market risk factors
                
                Format as formal policy document with clear procedures. Length: 500-600 words."""
            },
            {
                'target_entity': 'Green Lending Framework',
                'prompt_text': """Write a green lending policy framework document.
                Include comprehensive coverage of:
                - Green project category definitions and eligibility
                - Environmental impact measurement requirements
                - CO2 reduction target documentation
                - Third-party certification requirements (BREEAM, LEED)
                - Monitoring and reporting obligations
                - Pricing incentives for green bonds
                
                Format as formal policy document. Length: 500-600 words."""
            }
        ]
        
        return prompts
    
    def _get_annual_report_prompts(self) -> List[Dict]:
        """Generate annual report prompts"""
        banks = ["Nordic Bank Helgeland", "Nordic Bank Østlandet", "Nordic Bank Trøndelag"]
        
        prompts = []
        for bank in banks:
            prompts.append({
                'target_entity': bank,
                'prompt_text': f"""Write an annual report section for {bank} focusing on SMB (Small-Medium Business) initiatives.
                Include detailed discussion of:
                - Digital lending platform launches and adoption rates
                - SMB customer acquisition strategies and results
                - Product innovation for small business banking
                - Regional market penetration and growth
                - Technology investments supporting SMB banking
                - Partnership and alliance collaboration benefits
                - Cost reduction initiatives and efficiency gains
                
                Write in formal annual report style with specific metrics where appropriate.
                Length: 600-700 words."""
            })
        
        return prompts
    
    def _get_quarterly_report_prompts(self) -> List[Dict]:
        """Generate Q4 2024 quarterly report prompts"""
        banks = ["Nordic Bank Helgeland", "Nordic Bank Østlandet", "Nordic Bank Trøndelag"]
        
        prompts = []
        for bank in banks:
            prompts.append({
                'target_entity': bank,
                'prompt_text': f"""Write a Q4 2024 quarterly report section for {bank} focusing on SMB digital platform launches and product innovations.
                Include specific discussion of:
                - Digital platform or product launches completed in Q4 2024
                - SMB mobile banking app features launched (digital lending, automated underwriting)
                - New partnership announcements for SMB services
                - Technology infrastructure investments completed
                - Digital transformation milestones achieved in Q4 2024
                - Customer adoption metrics for new digital products
                - Regional SMB market expansion initiatives launched
                - Competitive positioning improvements through digital innovation
                
                Emphasize Q4 2024 timeframe and specific platform/product launch details.
                Write in formal quarterly report style with specific metrics and launch dates.
                Length: 600-700 words."""
            })
        
        return prompts
    
    def _get_loan_doc_prompts(self) -> List[Dict]:
        """Generate loan document prompts"""
        prompts = [
            {
                'target_entity': 'Nordlys Wind Farm Project',
                'prompt_text': """Write a green bond loan documentation summary for a renewable energy project.
                Include comprehensive details about:
                - Project description: 50MW offshore wind farm in Vestlandet
                - Environmental impact: Estimated CO2 reduction of 75,000 tons annually
                - Technology specifications and turbine details
                - Expected energy output and grid connection plans
                - ISS ESG eligibility criteria compliance
                - Monitoring and reporting framework for environmental targets
                - Financial structure and loan terms
                
                Format as professional loan documentation. Length: 500-600 words."""
            },
            {
                'target_entity': 'Bergen Green Building Complex',
                'prompt_text': """Write loan documentation for a dual-certified commercial development pursuing both LEED and BREEAM certification.
                Include detailed coverage of:
                - Building specifications and dual certification strategy (LEED Platinum + BREEAM Excellent targets)
                - Energy efficiency features and systems alignment with both standards
                - Sustainable materials and construction practices meeting LEED and BREEAM requirements
                - Water conservation and waste reduction measures for dual compliance
                - Expected environmental performance metrics for both certification schemes
                - Third-party verification and certification process timeline for LEED and BREEAM
                - Documentation requirements and assessment criteria gaps between standards
                - Loan structure and green bond framework compliance
                - Cost-benefit analysis of dual certification approach
                
                Format as professional loan documentation. Length: 600-700 words."""
            }
        ]
        
        return prompts
    
    def _get_third_party_prompts(self) -> List[Dict]:
        """Generate third-party assessment prompts"""
        prompts = [
            {
                'target_entity': 'ISS ESG Assessment',
                'prompt_text': """Write an ISS ESG assessment report for green bond eligibility.
                Include comprehensive analysis of:
                - Green project category definitions and compliance
                - Environmental impact measurement methodologies
                - Use of proceeds tracking and allocation
                - Impact reporting and transparency requirements
                - Alignment with EU Taxonomy and Norwegian green standards
                - Risk assessment and mitigation measures
                - Ongoing monitoring and verification procedures
                
                Format as professional third-party assessment report. Length: 600-700 words."""
            },
            {
                'target_entity': 'BREEAM Certification Assessment',
                'prompt_text': """Write a comprehensive BREEAM (Building Research Establishment Environmental Assessment Method) certification assessment report for green building projects.
                Include detailed coverage of:
                - BREEAM rating scheme overview (Pass, Good, Very Good, Excellent, Outstanding)
                - Assessment criteria across all BREEAM categories: Energy, Health & Wellbeing, Innovation, Land Use, Materials, Management, Pollution, Transport, Waste, Water
                - Specific requirements for BREEAM Excellent and Outstanding ratings
                - Documentation requirements for each assessment category
                - Comparison with LEED certification standards and Norwegian TEK building regulations
                - Third-party verification and assessment process timeline
                - Cost implications and certification fees structure
                - Ongoing monitoring and post-occupancy evaluation requirements
                - Green bond framework compliance and reporting alignment
                
                Format as professional certification assessment report. Include specific BREEAM credit requirements and scoring methodology. Length: 700-800 words."""
            }
        ]
        
        return prompts
    
    def generate_documents_from_prompts(self) -> None:
        """Generate actual documents using Cortex Complete with snowpark dataframe"""
        logger.info("Generating documents using Cortex Complete with snowpark dataframe...")
        
        try:
            # Read all prompts using snowpark dataframe
            prompts_df = self.session.table("DOCUMENT_PROMPTS")
            
            # Add generated title column
            prompts_with_titles_df = prompts_df.select(
                col("DOC_ID"),
                col("SCENARIO"), 
                col("DOC_TYPE"),
                col("TARGET_ENTITY"),
                col("PROMPT_TEXT"),
                col("MODEL_CLASS"),
                col("TEMPERATURE"),
                # Generate title based on doc_type and target_entity
                self._create_title_expression(col("DOC_TYPE"), col("TARGET_ENTITY")).alias("TITLE")
            )
            
            # Get distinct model classes to process each separately
            # (Cortex Complete requires model name as string literal)
            model_classes = [row['MODEL_CLASS'] for row in prompts_with_titles_df.select("MODEL_CLASS").distinct().collect()]
            logger.info(f"Processing {len(model_classes)} model classes: {model_classes}")
            
            all_documents_dfs = []
            
            # Process each model class separately
            for model_class in model_classes:
                logger.info(f"Processing documents with model: {model_class}")
                
                # Filter prompts for this model class
                model_prompts_df = prompts_with_titles_df.filter(col("MODEL_CLASS") == lit(model_class))
                
                # Generate content using Cortex Complete with literal model string
                model_documents_df = model_prompts_df.select(
                    col("DOC_ID"),
                    col("SCENARIO"),
                    col("DOC_TYPE"), 
                    col("TITLE"),
                    col("TARGET_ENTITY"),
                    # Use Cortex Complete with literal model string
                    cortex.complete(model_class, col("PROMPT_TEXT")).alias("CONTENT_MD"),
                    col("MODEL_CLASS")
                )
                
                all_documents_dfs.append(model_documents_df)
                logger.info(f"Generated documents for model {model_class}")
            
            # Combine all documents from different models
            if all_documents_dfs:
                combined_documents_df = all_documents_dfs[0]
                for df in all_documents_dfs[1:]:
                    combined_documents_df = combined_documents_df.union(df)
                
                # Save all generated documents using save_as_table
                combined_documents_df.write.mode("overwrite").save_as_table("DOCUMENTS")
                
                # Get count for logging
                doc_count = combined_documents_df.count()
                logger.info(f"Generated {doc_count} documents successfully using snowpark dataframe")
            else:
                raise Exception("No model classes found to process")
            
        except Exception as e:
            logger.error(f"Failed to generate documents using snowpark dataframe: {str(e)}")
            # Fallback to individual processing if needed
            logger.info("Falling back to individual document processing...")
            self._generate_documents_individually()
    
    def _generate_content_with_cortex(self, prompt_text: str, model_class: str) -> str:
        """Generate content using Cortex Complete"""
        try:
            # Create a DataFrame with the prompt for Cortex processing
            prompt_df = self.session.create_dataframe(
                [(prompt_text,)], 
                ["prompt"]
            )
            
            # Use Cortex Complete to generate content
            result_df = prompt_df.select(
                cortex.complete(model_class.lower(), col("prompt")).alias("generated_content")
            )
            
            result = result_df.collect()
            if result:
                return result[0]['GENERATED_CONTENT']
            else:
                return "Content generation failed - no result returned"
                
        except Exception as e:
            logger.error(f"Cortex Complete failed: {str(e)}")
            # Fallback to template-based content
            return self._generate_fallback_content(prompt_text)
    
    def _generate_fallback_content(self, prompt_text: str) -> str:
        """Generate fallback content when Cortex is unavailable"""
        # This is a simplified fallback - in production you might want more sophisticated templates
        return f"""[Generated Content - Fallback Mode]

This document was generated based on the following requirements:
{prompt_text}

[Note: This is fallback content generated when Cortex Complete is unavailable. 
In production, this would contain the full generated content based on the prompt.]

The document includes relevant Norwegian industry context and specific answerable phrases 
to support the demo scenarios as required."""
    
    def _generate_title(self, doc_type: str, target_entity: str) -> str:
        """Generate appropriate title for document"""
        title_templates = {
            'CRM_NOTE': f"Client Meeting Notes - {target_entity}",
            'NEWS': f"Market Update: {target_entity}",
            'POLICY': f"Policy Document: {target_entity}",
            'ANNUAL_REPORT': f"Annual Report 2024 - {target_entity} SMB Strategy",
            'QUARTERLY_REPORT': f"Q4 2024 Quarterly Report - {target_entity} - Digital Platform Launches",
            'LOAN_DOC': f"Green Bond Documentation - {target_entity}",
            'THIRD_PARTY': f"Third-Party Assessment - {target_entity}"
        }
        
        return title_templates.get(doc_type, f"{doc_type} - {target_entity}")
    
    def _create_title_expression(self, doc_type_col, target_entity_col):
        """Create title expression for snowpark dataframe"""
        return when(doc_type_col == lit("CRM_NOTE"), concat_ws(lit(" - "), lit("Client Meeting Notes"), target_entity_col)) \
            .when(doc_type_col == lit("NEWS"), concat_ws(lit(" - "), lit("Market Update:"), target_entity_col)) \
            .when(doc_type_col == lit("POLICY"), concat_ws(lit(" - "), lit("Policy Document:"), target_entity_col)) \
            .when(doc_type_col == lit("ANNUAL_REPORT"), concat_ws(lit(" - "), lit("Annual Report 2024"), target_entity_col, lit("SMB Strategy"))) \
            .when(doc_type_col == lit("QUARTERLY_REPORT"), concat_ws(lit(" - "), lit("Q4 2024 Quarterly Report"), target_entity_col, lit("Digital Platform Launches"))) \
            .when(doc_type_col == lit("LOAN_DOC"), concat_ws(lit(" - "), lit("Green Bond Documentation"), target_entity_col)) \
            .when(doc_type_col == lit("THIRD_PARTY"), concat_ws(lit(" - "), lit("Third-Party Assessment"), target_entity_col)) \
            .otherwise(concat_ws(lit(" - "), doc_type_col, target_entity_col))
    
    def _generate_documents_individually(self) -> None:
        """Fallback method to generate documents individually"""
        logger.info("Generating documents individually as fallback...")
        
        # Get all prompts
        prompts_df = self.session.table("DOCUMENT_PROMPTS")
        prompts = prompts_df.collect()
        
        documents_data = []
        
        for prompt_row in prompts:
            doc_id = prompt_row['DOC_ID']
            scenario = prompt_row['SCENARIO']
            doc_type = prompt_row['DOC_TYPE']
            target_entity = prompt_row['TARGET_ENTITY']
            prompt_text = prompt_row['PROMPT_TEXT']
            model_class = prompt_row['MODEL_CLASS']
            
            try:
                # Generate title
                title = self._generate_title(doc_type, target_entity)
                
                # Generate content using Cortex Complete
                content = self._generate_content_with_cortex(prompt_text, model_class)
                
                documents_data.append((
                    doc_id, scenario, doc_type, title, target_entity, content, model_class
                ))
                
                logger.info(f"Generated document: {title}")
                
            except Exception as e:
                logger.error(f"Failed to generate document {doc_id}: {str(e)}")
        
        # Save documents
        if documents_data:
            schema = StructType([
                StructField("DOC_ID", StringType()),
                StructField("SCENARIO", StringType()),
                StructField("DOC_TYPE", StringType()),
                StructField("TITLE", StringType()),
                StructField("TARGET_ENTITY", StringType()),
                StructField("CONTENT_MD", StringType()),
                StructField("MODEL_CLASS", StringType())
            ])
            
            df = self.session.create_dataframe(documents_data, schema)
            df.write.mode("overwrite").save_as_table("DOCUMENTS")
            
            logger.info(f"Generated {len(documents_data)} documents successfully using fallback method")
