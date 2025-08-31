"""
Data validator to ensure all demo requirements are met.
"""

import logging
from typing import Dict, List
from snowflake.snowpark import Session
from config import *

logger = logging.getLogger(__name__)

class DataValidator:
    """Validates that generated data meets all demo requirements."""
    
    def __init__(self, session: Session):
        self.session = session
        # Don't set database/schema here - let caller handle it
        
    def validate_all(self) -> Dict:
        """Run all validation checks."""
        logger.info("Running data validation...")
        
        # Ensure we're in the right database/schema
        try:
            self.session.sql(f"USE DATABASE {DB_NAME}").collect()
            self.session.sql(f"USE SCHEMA {RAW_SCHEMA}").collect()
        except:
            # Database might not exist yet
            pass
        
        results = {
            'success': True,
            'errors': []
        }
        
        # Check if tables exist
        if not self._check_tables_exist():
            results['success'] = False
            results['errors'].append("Required tables are missing")
            return results
        
        # Validate structured data
        results.update(self._validate_structured_data())
        
        # Validate unstructured data
        results.update(self._validate_unstructured_data())
        
        # Validate Nordic Freight Systems requirements
        nfs_validation = self._validate_nordic_freight_systems()
        results.update(nfs_validation)
        if not nfs_validation.get('nfs_valid', False):
            results['success'] = False
            
        # Validate demo prompts can be answered
        demo_validation = self._validate_demo_prompts()
        results['demo_prompts_ready'] = demo_validation
        if not all(demo_validation):
            results['success'] = False
            results['errors'].append("Not all demo prompts can be answered with current data")
            
        return results
    
    def _check_tables_exist(self) -> bool:
        """Check if all required tables exist."""
        required_tables = [
            "COMPANIES",
            "MACROECONOMIC_INDICATORS",
            "COMPANY_FINANCIALS",
            "FACTSET_NEWS_FEED",
            "GUIDEPOINT_EXPERT_TRANSCRIPTS",
            "MCBAINCG_CONSULTANT_REPORTS",
            "QUARTR_EARNINGS_CALLS",
            "INTERNAL_INVESTMENT_MEMOS"
        ]
        
        tables_query = f"""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = '{RAW_SCHEMA}'
        AND TABLE_NAME IN ({','.join([f"'{t}'" for t in required_tables])})
        """
        
        existing_tables = self.session.sql(tables_query).collect()
        existing_table_names = [row['TABLE_NAME'] for row in existing_tables]
        
        missing_tables = [t for t in required_tables if t not in existing_table_names]
        
        if missing_tables:
            logger.error(f"Missing tables: {missing_tables}")
            return False
            
        logger.info("✅ All required tables exist")
        return True
    
    def _validate_structured_data(self) -> Dict:
        """Validate structured data requirements."""
        results = {}
        
        # Check companies
        companies_count = self.session.sql("SELECT COUNT(*) as CNT FROM COMPANIES").collect()[0]['CNT']
        results['companies_count'] = companies_count
        
        # Check if anchor companies exist
        anchor_check = self.session.sql(f"""
            SELECT COMPANY_NAME 
            FROM COMPANIES 
            WHERE COMPANY_NAME = '{ANCHOR_COMPANY}'
        """).collect()
        
        if not anchor_check:
            results['errors'] = results.get('errors', [])
            results['errors'].append(f"Required anchor company '{ANCHOR_COMPANY}' not found")
            
        # Check financials
        quarters_query = """
            SELECT COUNT(DISTINCT REPORTING_PERIOD) as CNT 
            FROM COMPANY_FINANCIALS
        """
        quarters_count = self.session.sql(quarters_query).collect()[0]['CNT']
        results['quarters_count'] = quarters_count
        
        # Check macro data
        macro_query = """
            SELECT COUNT(DISTINCT REPORT_DATE) as CNT 
            FROM MACROECONOMIC_INDICATORS
        """
        macro_months = self.session.sql(macro_query).collect()[0]['CNT']
        results['macro_months'] = macro_months
        
        logger.info(f"✅ Structured data: {companies_count} companies, {quarters_count} quarters, {macro_months} macro months")
        
        return results
    
    def _validate_unstructured_data(self) -> Dict:
        """Validate unstructured data volumes."""
        results = {}
        
        # Check news articles
        news_count = self.session.sql("SELECT COUNT(*) as CNT FROM FACTSET_NEWS_FEED").collect()[0]['CNT']
        results['news_count'] = news_count
        
        # Check Swedish news
        swedish_news = self.session.sql("""
            SELECT COUNT(*) as CNT 
            FROM FACTSET_NEWS_FEED 
            WHERE LANG = 'sv'
        """).collect()[0]['CNT']
        results['swedish_news_count'] = swedish_news
        
        # Check expert transcripts
        expert_count = self.session.sql("SELECT COUNT(*) as CNT FROM GUIDEPOINT_EXPERT_TRANSCRIPTS").collect()[0]['CNT']
        results['expert_count'] = expert_count
        
        # Check consultant reports
        consultant_count = self.session.sql("SELECT COUNT(*) as CNT FROM MCBAINCG_CONSULTANT_REPORTS").collect()[0]['CNT']
        results['consultant_count'] = consultant_count
        
        # Check earnings calls
        earnings_count = self.session.sql("SELECT COUNT(*) as CNT FROM QUARTR_EARNINGS_CALLS").collect()[0]['CNT']
        results['earnings_count'] = earnings_count
        
        # Check internal memos
        memos_count = self.session.sql("SELECT COUNT(*) as CNT FROM INTERNAL_INVESTMENT_MEMOS").collect()[0]['CNT']
        results['memos_count'] = memos_count
        
        logger.info(f"✅ Unstructured data: {news_count} news ({swedish_news} Swedish), "
                   f"{expert_count} experts, {consultant_count} reports, "
                   f"{earnings_count} earnings, {memos_count} memos")
        
        return results
    
    def _validate_nordic_freight_systems(self) -> Dict:
        """Validate Nordic Freight Systems specific requirements."""
        results = {'nfs_valid': True}
        
        # Check earnings calls count
        nfs_earnings_query = f"""
            SELECT COUNT(*) as CNT 
            FROM QUARTR_EARNINGS_CALLS 
            WHERE COMPANY_ID = (
                SELECT COMPANY_ID 
                FROM COMPANIES 
                WHERE COMPANY_NAME = '{ANCHOR_COMPANY}'
            )
        """
        
        nfs_earnings = self.session.sql(nfs_earnings_query).collect()
        nfs_earnings_count = nfs_earnings[0]['CNT'] if nfs_earnings else 0
        results['nfs_earnings_count'] = nfs_earnings_count
        
        if nfs_earnings_count < 6:
            results['nfs_valid'] = False
            results['errors'] = results.get('errors', [])
            results['errors'].append(f"Nordic Freight Systems only has {nfs_earnings_count} earnings calls (need 6+)")
        
        # Check for pricing power mentions
        pricing_query = f"""
            SELECT COUNT(*) as CNT
            FROM QUARTR_EARNINGS_CALLS
            WHERE COMPANY_ID = (
                SELECT COMPANY_ID 
                FROM COMPANIES 
                WHERE COMPANY_NAME = '{ANCHOR_COMPANY}'
            )
            AND (
                LOWER(TRANSCRIPT_JSON) LIKE '%pricing power%'
                OR LOWER(TRANSCRIPT_JSON) LIKE '%pass through%'
                OR LOWER(TRANSCRIPT_JSON) LIKE '%price increase%'
                OR LOWER(TRANSCRIPT_JSON) LIKE '%dynamic pricing%'
                OR LOWER(TRANSCRIPT_JSON) LIKE '%fuel surcharge%'
            )
        """
        
        pricing_mentions = self.session.sql(pricing_query).collect()[0]['CNT']
        results['nfs_has_pricing_quotes'] = pricing_mentions > 0
        
        if not results['nfs_has_pricing_quotes']:
            results['nfs_valid'] = False
            results['errors'] = results.get('errors', [])
            results['errors'].append("Nordic Freight Systems earnings calls lack pricing power discussion")
        
        logger.info(f"✅ Nordic Freight Systems: {nfs_earnings_count} earnings calls, "
                   f"pricing quotes: {results['nfs_has_pricing_quotes']}")
        
        return results
    
    def _validate_demo_prompts(self) -> List[bool]:
        """Validate that each demo prompt can be answered."""
        validations = []
        
        # Prompt 1: Qualitative synthesis on inflation impact
        # Need: News, Reports, Memos about inflation/costs
        inflation_check = self.session.sql("""
            SELECT 
                (SELECT COUNT(*) FROM FACTSET_NEWS_FEED 
                 WHERE LOWER(ARTICLE_BODY) LIKE '%inflation%' 
                    OR LOWER(ARTICLE_BODY) LIKE '%cost%'
                    OR LOWER(ARTICLE_BODY) LIKE '%price%') as news,
                (SELECT COUNT(*) FROM MCBAINCG_CONSULTANT_REPORTS 
                 WHERE LOWER(REPORT_BODY) LIKE '%inflation%'
                    OR LOWER(REPORT_BODY) LIKE '%pricing%') as reports,
                (SELECT COUNT(*) FROM INTERNAL_INVESTMENT_MEMOS 
                 WHERE LOWER(MEMO_BODY) LIKE '%inflation%'
                    OR LOWER(MEMO_BODY) LIKE '%cost%') as memos
        """).collect()[0]
        
        prompt1_valid = (inflation_check['NEWS'] > 0 and 
                        inflation_check['REPORTS'] > 0 and 
                        inflation_check['MEMOS'] > 0)
        validations.append(prompt1_valid)
        
        # Prompt 2: Quantitative comparison of gross margins
        # Need: Financial data for multiple companies over 6 quarters
        margin_check = self.session.sql("""
            SELECT COUNT(DISTINCT c.COMPANY_NAME) as companies,
                   COUNT(DISTINCT f.REPORTING_PERIOD) as quarters
            FROM COMPANY_FINANCIALS f
            JOIN COMPANIES c ON f.COMPANY_ID = c.COMPANY_ID
            WHERE c.SECTOR IN (SELECT DISTINCT SECTOR FROM COMPANIES)
        """).collect()[0]
        
        prompt2_valid = margin_check['COMPANIES'] >= 3 and margin_check['QUARTERS'] >= 6
        validations.append(prompt2_valid)
        
        # Prompt 3: Nordic Freight Systems pricing power quotes
        # Need: Earnings calls with pricing discussion
        nfs_pricing_check = self.session.sql(f"""
            SELECT COUNT(*) as CNT
            FROM QUARTR_EARNINGS_CALLS
            WHERE TITLE LIKE '%Nordic Freight Systems%'
            AND (LOWER(TRANSCRIPT_JSON) LIKE '%pricing power%'
                 OR LOWER(TRANSCRIPT_JSON) LIKE '%pass%through%')
        """).collect()[0]['CNT']
        
        prompt3_valid = nfs_pricing_check > 0
        validations.append(prompt3_valid)
        
        # Prompt 4: Cross-source agreement on pricing
        # Need: Consultant reports and expert interviews
        cross_source_check = self.session.sql("""
            SELECT 
                (SELECT COUNT(*) FROM MCBAINCG_CONSULTANT_REPORTS 
                 WHERE LOWER(REPORT_BODY) LIKE '%pric%') as reports,
                (SELECT COUNT(*) FROM GUIDEPOINT_EXPERT_TRANSCRIPTS 
                 WHERE LOWER(TRANSCRIPT_TEXT) LIKE '%pric%'
                    OR LOWER(TRANSCRIPT_TEXT) LIKE '%margin%') as experts
        """).collect()[0]
        
        prompt4_valid = cross_source_check['REPORTS'] > 0 and cross_source_check['EXPERTS'] > 0
        validations.append(prompt4_valid)
        
        logger.info(f"Demo prompts validation: {validations}")
        
        return validations
