"""
Unstructured data generator using Cortex Complete for realistic content generation.
"""

import logging
import datetime
from datetime import timedelta
import random
import json
import pandas as pd
from typing import List, Dict, Optional

from snowflake.snowpark import Session
from snowflake.snowpark.types import *
from snowflake.snowpark.functions import col, lit, call_function

from config import *

logger = logging.getLogger(__name__)

class UnstructuredDataGenerator:
    """Generates unstructured data using Cortex Complete."""
    
    def __init__(self, session: Session):
        self.session = session
        random.seed(RANDOM_SEED)
        
    def generate_all(self, companies_df: pd.DataFrame):
        """Generate all unstructured data sources."""
        logger.info("Starting unstructured data generation...")
        
        # Generate prompts for each data source
        self.generate_news_articles(companies_df)
        self.generate_expert_transcripts(companies_df)
        self.generate_consultant_reports(companies_df)
        self.generate_earnings_calls(companies_df)
        self.generate_internal_memos(companies_df)
        
        logger.info("Unstructured data generation complete")
        
    def generate_news_articles(self, companies_df: pd.DataFrame):
        """Generate news articles about inflation and logistics companies."""
        logger.info(f"Generating {NUM_NEWS_ARTICLES} news articles...")
        
        prompts_data = []
        
        # Topics for news articles
        topics = [
            "rising fuel costs affecting transportation margins",
            "labor shortages driving wage inflation in logistics sector",
            "supply chain bottlenecks at Nordic ports",
            "new sustainability regulations impacting freight costs",
            "technology investments to combat rising operational costs",
            "merger and acquisition activity in Nordic logistics",
            "quarterly earnings beats expectations despite inflation",
            "price increases announced to offset rising costs",
            "expansion into new markets to drive growth",
            "partnership agreements to improve efficiency"
        ]
        
        # Generate prompts
        for i in range(NUM_NEWS_ARTICLES):
            # Determine if this should be Swedish
            is_swedish = i < int(NUM_NEWS_ARTICLES * SWEDISH_NEWS_FRACTION)
            
            # Pick a company (ensure anchor companies get coverage)
            if i < len(ANCHOR_COMPANIES) * 2:
                company_idx = i % len(ANCHOR_COMPANIES)
                company_name = ANCHOR_COMPANIES[company_idx]
                company_id = company_idx + 1
            else:
                company = companies_df.sample(n=1).iloc[0]
                company_name = company['COMPANY_NAME']
                company_id = int(company['COMPANY_ID'])
            
            topic = random.choice(topics)
            
            if is_swedish:
                source = SWEDISH_PROVIDER
                lang = "sv"
                prompt = f"""Write a Swedish financial news article about {company_name} and {topic}.
                The article should be 3 paragraphs, factual and data-driven.
                Include specific percentages and figures.
                Write in Swedish language.
                Focus on the Nordic logistics market."""
            else:
                source = random.choice(["Nordic Business Daily", "Logistics Weekly", "Transport Times", "Freight News Network"])
                lang = "en"
                prompt = f"""Write a financial news article about {company_name} dealing with {topic}.
                The article should be 3 paragraphs, factual and neutral in tone.
                Include specific data points, percentages, and quarterly impacts.
                Mention how this affects their competitive position in the Nordic logistics market.
                Reference industry analysts or company executives when appropriate."""
            
            prompts_data.append({
                "PROMPT_ID": i + 1,
                "SOURCE_TABLE": "FACTSET_NEWS_FEED",
                "COMPANY_ID": company_id,
                "COMPANY_NAME": company_name,
                "TITLE_HINT": f"{company_name} - {topic}",
                "TOPIC_TAGS": topic,
                "PROMPT_TEXT": prompt,
                "RANDOM_SEED": RANDOM_SEED + i,
                "MODEL_NAME": DEFAULT_LLM_MODEL,
                "NEWS_SOURCE": source,
                "LANG": lang
            })
        
        # Generate content using Cortex Complete
        self._generate_and_save_content(prompts_data, "FACTSET_NEWS_FEED", self._process_news)
        
    def generate_expert_transcripts(self, companies_df: pd.DataFrame):
        """Generate expert interview transcripts."""
        logger.info(f"Generating {NUM_EXPERT_TRANSCRIPTS} expert transcripts...")
        
        prompts_data = []
        
        expert_profiles = [
            "former VP of Operations at major Nordic logistics firm",
            "20-year veteran supply chain consultant",
            "former CFO of international freight company",
            "logistics technology specialist",
            "Nordic transportation industry analyst",
            "port operations expert",
            "labor relations specialist in transport sector",
            "sustainability advisor for logistics companies"
        ]
        
        topics = [
            "strategies for maintaining margins during inflationary periods",
            "the impact of fuel price volatility on contract negotiations",
            "labor market dynamics in Nordic logistics",
            "technology adoption to improve operational efficiency",
            "pricing power differences across logistics segments",
            "customer retention during price increases",
            "competitive dynamics in Nordic freight markets"
        ]
        
        for i in range(NUM_EXPERT_TRANSCRIPTS):
            expert = random.choice(expert_profiles)
            topic = random.choice(topics)
            
            # Some transcripts linked to specific companies
            company_id = None
            company_ref = ""
            if i < 4:  # First few linked to anchor companies
                company = ANCHOR_COMPANIES[i % len(ANCHOR_COMPANIES)]
                company_id = (i % len(ANCHOR_COMPANIES)) + 1
                company_ref = f" Use {company} as an example when relevant."
            
            prompt = f"""Generate an expert interview transcript between an investment analyst and an expert ({expert}).
            Topic: {topic}
            
            Format the transcript as a Q&A with clear labels:
            **Analyst:** [question]
            **Expert:** [detailed answer]
            
            Include 4-5 exchanges.{company_ref}
            The expert should provide specific insights, data points, and real-world examples.
            Focus on actionable intelligence for investors.
            The expert should sound knowledgeable and provide nuanced views."""
            
            prompts_data.append({
                "PROMPT_ID": i + 1,
                "SOURCE_TABLE": "GUIDEPOINT_EXPERT_TRANSCRIPTS",
                "COMPANY_ID": company_id,
                "COMPANY_NAME": None,
                "TITLE_HINT": f"Expert Interview - {expert}",
                "TOPIC_TAGS": topic,
                "PROMPT_TEXT": prompt,
                "RANDOM_SEED": RANDOM_SEED + i,
                "MODEL_NAME": DEFAULT_LLM_MODEL,
                "EXPERT_PROFILE": expert
            })
        
        self._generate_and_save_content(prompts_data, "GUIDEPOINT_EXPERT_TRANSCRIPTS", self._process_expert_transcripts)
        
    def generate_consultant_reports(self, companies_df: pd.DataFrame):
        """Generate consultant reports on logistics and inflation."""
        logger.info(f"Generating {NUM_CONSULTANT_REPORTS} consultant reports...")
        
        prompts_data = []
        
        report_titles = [
            "Nordic Logistics Sector: Navigating the Inflation Storm",
            "Pricing Power in Scandinavian Freight Markets",
            "Digital Transformation as a Hedge Against Rising Costs",
            "M&A Opportunities in Nordic Transport Sector",
            "Sustainability Regulations: Cost Burden or Competitive Advantage?",
            "Labor Market Dynamics in Nordic Logistics",
            "The Future of Last-Mile Delivery in Scandinavia",
            "Supply Chain Resilience: Lessons from Recent Disruptions"
        ]
        
        for i in range(NUM_CONSULTANT_REPORTS):
            title = report_titles[i % len(report_titles)]
            
            # Ensure at least 2 reports cover pricing strategies
            if i < 2:
                focus = "pricing strategies and cost pass-through mechanisms"
            else:
                focus = "operational efficiency and strategic positioning"
            
            prompt = f"""Write a strategic consulting report titled: "{title}"
            
            Structure the report with:
            
            ## Executive Summary
            3-4 key bullet points summarizing findings and recommendations
            
            ## Market Analysis
            Detailed analysis of current market conditions, focusing on {focus}
            Include specific data points and percentages
            
            ## Strategic Recommendations
            3-4 actionable recommendations for logistics companies
            
            ## Case Studies
            Brief examples from Nordic logistics companies (you can reference Nordic Freight Systems, Arctic Cargo AB, or similar)
            
            ## Conclusion
            Forward-looking perspective on the sector
            
            Make it analytical, data-driven, and actionable for C-suite executives."""
            
            prompts_data.append({
                "PROMPT_ID": i + 1,
                "SOURCE_TABLE": "MCBAINCG_CONSULTANT_REPORTS",
                "COMPANY_ID": None,
                "COMPANY_NAME": None,
                "TITLE_HINT": title,
                "TOPIC_TAGS": focus,
                "PROMPT_TEXT": prompt,
                "RANDOM_SEED": RANDOM_SEED + i,
                "MODEL_NAME": DEFAULT_LLM_MODEL,
                "REPORT_TITLE": title
            })
        
        self._generate_and_save_content(prompts_data, "MCBAINCG_CONSULTANT_REPORTS", self._process_consultant_reports)
        
    def generate_earnings_calls(self, companies_df: pd.DataFrame):
        """Generate earnings call transcripts with focus on pricing power."""
        logger.info("Generating earnings call transcripts...")
        
        prompts_data = []
        prompt_id = 1
        
        # Generate earnings calls based on configuration
        for company_name, num_quarters in EARNINGS_CALLS_CONFIG.items():
            company_id = list(ANCHOR_COMPANIES).index(company_name) + 1
            
            for quarter_offset in range(num_quarters):
                year = 2024 - (quarter_offset // 4)
                quarter = 4 - (quarter_offset % 4)
                if quarter == 0:
                    quarter = 4
                    year -= 1
                
                reporting_period = f"{year}-Q{quarter}"
                
                # Special handling for Nordic Freight Systems - ensure pricing power discussion
                if company_name == ANCHOR_COMPANY:
                    pricing_instruction = """
                    IMPORTANT: The CEO must explicitly discuss pricing power and the company's ability to pass through cost increases to customers.
                    Include specific quotes about:
                    - Dynamic pricing models
                    - Fuel surcharges
                    - Contract renegotiations
                    - Maintaining margins despite inflation
                    Use specific percentages (e.g., "we've successfully passed through 85-90% of cost increases")"""
                else:
                    pricing_instruction = "Discuss cost pressures and pricing strategies."
                
                prompt = f"""Generate an earnings call transcript for {company_name} for {reporting_period}.
                
                Format as JSON with this structure:
                {{
                    "company": "{company_name}",
                    "period": "{reporting_period}",
                    "participants": ["CEO", "CFO", "Analyst 1", "Analyst 2"],
                    "presentation": [
                        {{"speaker": "CEO", "text": "Opening remarks about quarterly performance..."}},
                        {{"speaker": "CFO", "text": "Financial details..."}}
                    ],
                    "qa": [
                        {{"speaker": "Analyst 1", "text": "Question about margins..."}},
                        {{"speaker": "CEO", "text": "Answer about pricing power..."}}
                    ]
                }}
                
                {pricing_instruction}
                
                Include discussion of:
                - Revenue growth and margin trends
                - Impact of inflation on operations
                - Strategic initiatives to combat rising costs
                - Forward guidance
                
                Make it realistic with specific numbers and industry context."""
                
                prompts_data.append({
                    "PROMPT_ID": prompt_id,
                    "SOURCE_TABLE": "QUARTR_EARNINGS_CALLS",
                    "COMPANY_ID": company_id,
                    "COMPANY_NAME": company_name,
                    "TITLE_HINT": f"Earnings Call - {company_name} - {reporting_period}",
                    "TOPIC_TAGS": "earnings, pricing power, inflation",
                    "PROMPT_TEXT": prompt,
                    "RANDOM_SEED": RANDOM_SEED + prompt_id,
                    "MODEL_NAME": DEFAULT_LLM_MODEL,
                    "REPORTING_PERIOD": reporting_period
                })
                prompt_id += 1
        
        # Add earnings calls for remaining companies (2 quarters each)
        remaining_companies = [c for c in companies_df['COMPANY_NAME'].unique() 
                              if c not in EARNINGS_CALLS_CONFIG.keys()]
        
        for company_name in remaining_companies[:5]:  # Limit to keep total reasonable
            company_id = int(companies_df[companies_df['COMPANY_NAME'] == company_name]['COMPANY_ID'].iloc[0])
            
            for quarter_offset in range(2):
                year = 2024 - quarter_offset
                quarter = 4 - quarter_offset
                reporting_period = f"{year}-Q{quarter}"
                
                prompt = f"""Generate a brief earnings call transcript for {company_name} for {reporting_period}.
                
                Format as JSON (same structure as before).
                Focus on operational updates and inflation impacts.
                Keep it shorter than major company calls but still substantive."""
                
                prompts_data.append({
                    "PROMPT_ID": prompt_id,
                    "SOURCE_TABLE": "QUARTR_EARNINGS_CALLS",
                    "COMPANY_ID": company_id,
                    "COMPANY_NAME": company_name,
                    "TITLE_HINT": f"Earnings Call - {company_name} - {reporting_period}",
                    "TOPIC_TAGS": "earnings, operations",
                    "PROMPT_TEXT": prompt,
                    "RANDOM_SEED": RANDOM_SEED + prompt_id,
                    "MODEL_NAME": DEFAULT_LLM_MODEL,
                    "REPORTING_PERIOD": reporting_period
                })
                prompt_id += 1
        
        self._generate_and_save_content(prompts_data, "QUARTR_EARNINGS_CALLS", self._process_earnings_calls)
        
    def generate_internal_memos(self, companies_df: pd.DataFrame):
        """Generate internal investment memos."""
        logger.info(f"Generating {NUM_INTERNAL_MEMOS} internal memos...")
        
        prompts_data = []
        
        memo_topics = [
            "Investment thesis update",
            "Risk assessment - inflation impact",
            "Competitive positioning analysis",
            "Management meeting notes",
            "Sector rotation recommendation",
            "Due diligence findings",
            "Portfolio review - logistics holdings"
        ]
        
        for i in range(NUM_INTERNAL_MEMOS):
            # Ensure Nordic Freight Systems gets coverage
            if i < 3:
                company_name = ANCHOR_COMPANY
                company_id = 1
            else:
                company = companies_df.sample(n=1).iloc[0]
                company_name = company['COMPANY_NAME']
                company_id = int(company['COMPANY_ID'])
            
            topic = memo_topics[i % len(memo_topics)]
            
            prompt = f"""Write an internal investment memo for 'Investor Listed' regarding {company_name}.
            
            Subject: {topic} - {company_name}
            
            Structure:
            
            ## Summary
            Brief overview of the analysis/meeting/findings
            
            ## Key Points
            - 3-4 bullet points with specific insights
            - Include data and percentages where relevant
            
            ## Investment Implications
            How this affects our position or thesis
            
            ## Risks and Concerns
            What we need to monitor
            
            ## Recommendation
            Clear action item or position
            
            Make it professional, analytical, and actionable.
            Reference current inflationary environment and its impacts."""
            
            prompts_data.append({
                "PROMPT_ID": i + 1,
                "SOURCE_TABLE": "INTERNAL_INVESTMENT_MEMOS",
                "COMPANY_ID": company_id,
                "COMPANY_NAME": company_name,
                "TITLE_HINT": f"{topic} - {company_name}",
                "TOPIC_TAGS": topic,
                "PROMPT_TEXT": prompt,
                "RANDOM_SEED": RANDOM_SEED + i,
                "MODEL_NAME": DEFAULT_LLM_MODEL,
                "AUTHOR": random.choice(["Anna Lindberg", "Erik Johansson", "Maria Nilsson", "Lars Andersson"])
            })
        
        self._generate_and_save_content(prompts_data, "INTERNAL_INVESTMENT_MEMOS", self._process_internal_memos)
        
    def _generate_and_save_content(self, prompts_data: List[Dict], table_name: str, process_func):
        """Generate content using Cortex Complete and save to table."""
        
        # Create prompts table
        prompts_df = pd.DataFrame(prompts_data)
        temp_table = f"TEMP_PROMPTS_{table_name}"
        
        self.session.write_pandas(
            prompts_df,
            temp_table,
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False
        )
        
        logger.info(f"Generating content for {table_name} using Cortex Complete...")
        
        # Use Cortex Complete to generate content
        df = self.session.table(temp_table)
        
        # Generate content using Complete function
        result_df = df.with_column(
            "GENERATED_CONTENT",
            call_function("SNOWFLAKE.CORTEX.COMPLETE", 
                         lit(DEFAULT_LLM_MODEL),
                         col("PROMPT_TEXT"))
        )
        
        # Collect results
        results = result_df.to_pandas()
        
        # Process and save final content
        processed_df = process_func(results)
        
        # Save to final table
        self.session.write_pandas(
            processed_df,
            table_name,
            auto_create_table=True,
            overwrite=True,
            quote_identifiers=False
        )
        
        # Clean up temp table
        self.session.sql(f"DROP TABLE IF EXISTS {temp_table}").collect()
        
        logger.info(f"Saved {len(processed_df)} records to {table_name}")
        
    def _process_news(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Process generated news articles."""
        processed = []
        
        for _, row in results_df.iterrows():
            content = row['GENERATED_CONTENT']
            
            # Extract headline (first line) and body
            lines = content.strip().split('\n')
            headline = lines[0].replace('#', '').strip()
            if not headline:
                headline = row['TITLE_HINT']
            
            body = '\n'.join(lines[1:]).strip()
            
            processed.append({
                "ARTICLE_ID": row['PROMPT_ID'],
                "HEADLINE": headline,
                "ARTICLE_BODY": body,
                "PUBLISH_TIMESTAMP": datetime.datetime.now() - timedelta(days=random.randint(1, 90)),
                "NEWS_SOURCE": row['NEWS_SOURCE'],
                "COMPANY_ID": row['COMPANY_ID'] if pd.notna(row['COMPANY_ID']) else None,
                "LANG": row['LANG']
            })
        
        return pd.DataFrame(processed)
    
    def _process_expert_transcripts(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Process generated expert transcripts."""
        processed = []
        
        for _, row in results_df.iterrows():
            # Generate title
            interview_date = datetime.datetime.now() - timedelta(days=random.randint(1, 60))
            title = f"Expert Interview — {row['EXPERT_PROFILE']} — {interview_date.strftime('%Y-%m-%d')}"
            
            processed.append({
                "TRANSCRIPT_ID": row['PROMPT_ID'],
                "TITLE": title,
                "INTERVIEW_DATE": interview_date.date(),
                "EXPERT_PROFILE": row['EXPERT_PROFILE'],
                "TRANSCRIPT_TEXT": row['GENERATED_CONTENT'],
                "COMPANY_ID": row['COMPANY_ID'] if pd.notna(row['COMPANY_ID']) else None
            })
        
        return pd.DataFrame(processed)
    
    def _process_consultant_reports(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Process generated consultant reports."""
        processed = []
        
        for _, row in results_df.iterrows():
            content = row['GENERATED_CONTENT']
            
            # Extract executive summary if present
            exec_summary = ""
            if "Executive Summary" in content:
                start = content.find("Executive Summary")
                end = content.find("##", start + 1)
                if end == -1:
                    end = len(content)
                exec_summary = content[start:end].replace("Executive Summary", "").strip()
            
            processed.append({
                "REPORT_ID": row['PROMPT_ID'],
                "TITLE": row['REPORT_TITLE'],
                "PUBLISH_DATE": datetime.datetime.now().date() - timedelta(days=random.randint(1, 45)),
                "EXECUTIVE_SUMMARY": exec_summary[:500] if exec_summary else "Strategic analysis of Nordic logistics sector",
                "REPORT_BODY": content,
                "COMPANY_ID": None  # Reports are sector-wide
            })
        
        return pd.DataFrame(processed)
    
    def _process_earnings_calls(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Process generated earnings call transcripts."""
        processed = []
        
        for _, row in results_df.iterrows():
            # Generate title
            title = f"Earnings Call — {row['COMPANY_NAME']} — {row['REPORTING_PERIOD']}"
            
            # Parse quarter to get timestamp
            year, quarter = row['REPORTING_PERIOD'].split('-Q')
            month = int(quarter) * 3
            call_date = datetime.datetime(int(year), month, 15)
            
            processed.append({
                "CALL_ID": row['PROMPT_ID'],
                "TITLE": title,
                "COMPANY_ID": row['COMPANY_ID'],
                "CALL_TIMESTAMP": call_date,
                "REPORTING_PERIOD": row['REPORTING_PERIOD'],
                "TRANSCRIPT_JSON": row['GENERATED_CONTENT']  # Store as VARCHAR with JSON content
            })
        
        return pd.DataFrame(processed)
    
    def _process_internal_memos(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """Process generated internal memos."""
        processed = []
        
        for _, row in results_df.iterrows():
            subject = row['TITLE_HINT']
            
            processed.append({
                "MEMO_ID": row['PROMPT_ID'],
                "SUBJECT": subject,
                "CREATION_DATE": datetime.datetime.now().date() - timedelta(days=random.randint(1, 30)),
                "AUTHOR": row['AUTHOR'],
                "SUBJECT_COMPANIES": row['COMPANY_NAME'] if pd.notna(row['COMPANY_NAME']) else None,
                "MEMO_BODY": row['GENERATED_CONTENT']
            })
        
        return pd.DataFrame(processed)
