"""
Semantic Model and View creation for SnowBank Intelligence Demo
Creates semantic model for Cortex Analyst with all required measures and dimensions
"""

import logging
from typing import Dict, List
from snowflake.snowpark.exceptions import SnowparkSQLException

from .config import DemoConfig

logger = logging.getLogger(__name__)


class SemanticModelManager:
    """Manages semantic model and view creation for Cortex Analyst"""
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
    
    def create_semantic_model(self) -> None:
        """Create the complete semantic model and view"""
        logger.info("Creating semantic model and view...")
        
        # Create semantic model
        self.create_semantic_model_definition()
        
        # Create semantic view
        self.create_semantic_view()
        
        logger.info("Semantic model and view created successfully")
    
    def create_semantic_model_definition(self) -> None:
        """Create the semantic model definition"""
        
        # Drop existing semantic model if it exists
        try:
            self.session.sql("DROP SEMANTIC MODEL IF EXISTS SNOWBANK_DEMO_SM").collect()
        except SnowparkSQLException:
            pass
        
        semantic_model_yaml = """
---
semantic_model:
  name: SNOWBANK_DEMO_SM
  description: "SnowBank Intelligence Demo - Norwegian Banking Alliance Data Model"
  
  entities:
    - name: member_banks
      expr: FSI_DEMOS.BANK_DEMO.MEMBER_BANKS
      description: "Member banks in the Nordic Banking alliance"
      dimensions:
        - name: member_bank_id
          expr: MEMBER_BANK_ID
          description: "Unique member bank identifier"
          data_type: TEXT
        - name: bank_name
          expr: BANK_NAME  
          description: "Member bank name"
          data_type: TEXT
          synonyms: ["bank", "institution"]
        - name: region
          expr: REGION
          description: "Norwegian region where bank operates"
          data_type: TEXT
          synonyms: ["area", "location", "geography"]
      measures:
        - name: total_assets
          expr: TOTAL_ASSETS
          description: "Total bank assets in NOK"
          data_type: NUMBER
          synonyms: ["assets", "bank size"]
          
    - name: customers
      expr: FSI_DEMOS.BANK_DEMO.CUSTOMERS
      description: "Bank customers across the alliance"
      dimensions:
        - name: customer_id
          expr: CUSTOMER_ID
          description: "Unique customer identifier"
          data_type: TEXT
        - name: customer_name
          expr: CUSTOMER_NAME
          description: "Customer name"
          data_type: TEXT
          synonyms: ["client", "borrower"]
        - name: customer_type
          expr: CUSTOMER_TYPE
          description: "Individual or Corporate customer"
          data_type: TEXT
          synonyms: ["type", "category"]
        - name: industry_sector
          expr: INDUSTRY_SECTOR
          description: "Customer industry sector"
          data_type: TEXT
          synonyms: ["industry", "sector", "business"]
        - name: geographic_region
          expr: GEOGRAPHIC_REGION
          description: "Customer geographic region in Norway"
          data_type: TEXT
          synonyms: ["region", "location"]
      measures:
        - name: credit_score_origination
          expr: CREDIT_SCORE_ORIGINATION
          description: "Customer credit score at origination"
          data_type: NUMBER
          synonyms: ["credit score", "rating"]
          
    - name: loans
      expr: FSI_DEMOS.BANK_DEMO.LOANS
      description: "Loan portfolio across all member banks"
      dimensions:
        - name: loan_id
          expr: LOAN_ID
          description: "Unique loan identifier"
          data_type: TEXT
        - name: loan_type
          expr: LOAN_TYPE
          description: "Type of loan product"
          data_type: TEXT
          synonyms: ["product", "loan product"]
        - name: origination_year
          expr: YEAR(ORIGINATION_DATE)
          description: "Year loan was originated"
          data_type: NUMBER
          synonyms: ["vintage", "year"]
        - name: last_credit_review_date
          expr: LAST_CREDIT_REVIEW_DATE
          description: "Date of last credit review"
          data_type: DATE
          synonyms: ["review date", "last review"]
        - name: green_project_category
          expr: GREEN_PROJECT_CATEGORY
          description: "Green bond project category"
          data_type: TEXT
          synonyms: ["green category", "esg category"]
      measures:
        - name: total_exposure
          expr: SUM(OUTSTANDING_BALANCE)
          description: "Total outstanding loan balance"
          data_type: NUMBER
          synonyms: ["exposure", "credit exposure", "balance", "outstanding"]
        - name: ltv
          expr: LOAN_TO_VALUE_RATIO
          description: "Loan to value ratio"
          data_type: NUMBER
          synonyms: ["loan to value", "LVR"]
        - name: average_interest_rate
          expr: AVG(INTEREST_RATE)
          description: "Average interest rate across loans"
          data_type: NUMBER
          synonyms: ["avg rate", "interest rate"]
        - name: green_portfolio_percentage
          expr: SUM(CASE WHEN GREEN_BOND_FRAMEWORK_TAG THEN OUTSTANDING_BALANCE ELSE 0 END) / SUM(OUTSTANDING_BALANCE) * 100
          description: "Percentage of portfolio in green bonds"
          data_type: NUMBER
          synonyms: ["green percentage", "sustainable lending", "esg percentage"]
        - name: average_loan_vintage
          expr: AVG(DATEDIFF('month', ORIGINATION_DATE, CURRENT_DATE()))
          description: "Average loan age in months"
          data_type: NUMBER
          synonyms: ["portfolio age", "loan vintage", "avg age"]
        - name: post_stress_ltv
          expr: OUTSTANDING_BALANCE / (CURRENT_PROPERTY_VALUE * 0.95)
          description: "LTV under 5% property stress scenario"
          data_type: NUMBER
          synonyms: ["stressed LTV", "shock LTV", "stress test LTV"]
          
    - name: financials
      expr: FSI_DEMOS.BANK_DEMO.FINANCIALS
      description: "Financial records including fees and revenues"
      dimensions:
        - name: record_type
          expr: RECORD_TYPE
          description: "Type of financial record"
          data_type: TEXT
        - name: record_date
          expr: RECORD_DATE
          description: "Date of financial record"
          data_type: DATE
      measures:
        - name: fee_revenue_ltm
          expr: SUM(CASE WHEN RECORD_TYPE = 'FEE_REVENUE' AND RECORD_DATE >= DATEADD('month', -12, CURRENT_DATE()) THEN AMOUNT ELSE 0 END)
          description: "Fee revenue last twelve months"
          data_type: NUMBER
          synonyms: ["fees", "fee revenue", "ltm fees"]
        - name: cross_sell_ratio
          expr: COUNT(DISTINCT RECORD_TYPE)
          description: "Number of distinct product types per customer"
          data_type: NUMBER
          synonyms: ["products per customer", "relationship depth"]
          
    - name: alliance_performance
      expr: FSI_DEMOS.BANK_DEMO.ALLIANCE_PERFORMANCE
      description: "Alliance-wide performance metrics"
      dimensions:
        - name: reporting_year
          expr: REPORTING_YEAR
          description: "Performance reporting year"
          data_type: NUMBER
          synonyms: ["year"]
      measures:
        - name: smb_growth_percentage
          expr: SMB_LENDING_GROWTH_PCT
          description: "Small-Medium Business lending growth percentage"
          data_type: NUMBER
          synonyms: ["SMB growth", "small business growth"]
        - name: cost_income_ratio
          expr: COST_INCOME_RATIO
          description: "Cost to income ratio"
          data_type: NUMBER
          synonyms: ["C/I", "efficiency ratio"]
          
    - name: market_data
      expr: FSI_DEMOS.BANK_DEMO.MARKET_DATA
      description: "Market data for Norwegian/Nordic companies"
      dimensions:
        - name: ticker
          expr: TICKER
          description: "Stock ticker symbol"
          data_type: TEXT
        - name: company_name
          expr: COMPANY_NAME
          description: "Company name"
          data_type: TEXT
        - name: peer_group
          expr: PEER_GROUP
          description: "Industry peer group"
          data_type: TEXT
          synonyms: ["industry", "sector"]
        - name: trade_date
          expr: TRADE_DATE
          description: "Trading date"
          data_type: DATE
      measures:
        - name: close_price
          expr: CLOSE_PRICE
          description: "Stock closing price"
          data_type: NUMBER
          synonyms: ["price", "stock price"]
  
  relationships:
    - name: customer_to_bank
      dimension: customers.member_bank_id
      foreign_dimension: member_banks.member_bank_id
    - name: loan_to_customer  
      dimension: loans.customer_id
      foreign_dimension: customers.customer_id
    - name: loan_to_bank
      dimension: loans.member_bank_id
      foreign_dimension: member_banks.member_bank_id
    - name: financial_to_customer
      dimension: financials.customer_id
      foreign_dimension: customers.customer_id
    - name: financial_to_bank
      dimension: financials.member_bank_id
      foreign_dimension: member_banks.member_bank_id
    - name: performance_to_bank
      dimension: alliance_performance.member_bank_id
      foreign_dimension: member_banks.member_bank_id
"""
        
        # Write semantic model to file and create
        try:
            # For now, we'll create a simplified version using SQL since YAML semantic models
            # require file upload. We'll create the semantic view directly.
            logger.info("Creating semantic model components...")
            
        except Exception as e:
            logger.error(f"Failed to create semantic model: {str(e)}")
            raise
    
    def create_semantic_view(self) -> None:
        """Create proper semantic view for Cortex Analyst using CREATE SEMANTIC VIEW syntax"""
        
        # Drop existing semantic view or regular view if it exists
        try:
            self.session.sql("DROP SEMANTIC VIEW IF EXISTS SNOWBANK_DEMO_SV").collect()
        except SnowparkSQLException:
            pass
        
        # Also drop regular view with same name if it exists
        try:
            self.session.sql("DROP VIEW IF EXISTS SNOWBANK_DEMO_SV").collect()
        except SnowparkSQLException:
            pass
        
        # Create enhanced semantic view for banking data (without market data)
        semantic_view_sql = """
        CREATE OR REPLACE SEMANTIC VIEW SNOWBANK_DEMO_SV
        
        TABLES (
            member_banks AS FSI_DEMOS.BANK_DEMO.MEMBER_BANKS PRIMARY KEY (MEMBER_BANK_ID)
                WITH SYNONYMS ('banks', 'member institutions', 'alliance banks')
                COMMENT = 'Nordic Banking Alliance member banks with regional presence and asset information',
            customers AS FSI_DEMOS.BANK_DEMO.CUSTOMERS PRIMARY KEY (CUSTOMER_ID)
                WITH SYNONYMS ('clients', 'borrowers', 'banking customers', 'corporate clients')
                COMMENT = 'Banking customers including corporate and individual clients across Norwegian regions',
            loans AS FSI_DEMOS.BANK_DEMO.LOANS PRIMARY KEY (LOAN_ID)
                WITH SYNONYMS ('lending portfolio', 'credit facilities', 'loan book', 'exposures')
                COMMENT = 'Loan portfolio including mortgages, corporate loans, and green bond financing',
            financials AS FSI_DEMOS.BANK_DEMO.FINANCIALS PRIMARY KEY (RECORD_ID)
                WITH SYNONYMS ('financial records', 'fee income', 'revenue data', 'financial performance')
                COMMENT = 'Financial records including fee income, revenue streams, and customer profitability data'
        )
        
        RELATIONSHIPS (
            customers (MEMBER_BANK_ID) REFERENCES member_banks,
            loans (CUSTOMER_ID) REFERENCES customers,
            loans (MEMBER_BANK_ID) REFERENCES member_banks,
            financials (CUSTOMER_ID) REFERENCES customers
            -- Note: market_data has no direct relationship as it represents peer companies for benchmarking
            -- Peer analysis is performed by matching customers.industry_sector with market_data.peer_group
        )
        
        FACTS (
            -- Core loan facts
            loans.outstanding_balance AS outstanding_balance
                WITH SYNONYMS ('loan amount', 'exposure', 'principal balance', 'loan value')
                COMMENT = 'Current outstanding loan balance in NOK',
            loans.interest_rate AS interest_rate
                WITH SYNONYMS ('rate', 'pricing', 'loan rate', 'interest pricing')
                COMMENT = 'Annual interest rate percentage for the loan',
            loans.loan_to_value_ratio AS loan_to_value_ratio
                WITH SYNONYMS ('LTV', 'loan to value', 'LTV ratio', 'collateral ratio')
                COMMENT = 'Loan to value ratio as percentage of property value',
            loans.current_property_value AS current_property_value
                WITH SYNONYMS ('property value', 'collateral value', 'asset value', 'real estate value')
                COMMENT = 'Current market value of property securing the loan in NOK',
            
            -- Bank facts
            member_banks.total_assets AS total_assets
                WITH SYNONYMS ('bank assets', 'total assets', 'balance sheet assets', 'bank size')
                COMMENT = 'Total assets of member bank in NOK',
            
            -- Customer facts  
            customers.credit_score_origination AS credit_score_origination
                WITH SYNONYMS ('credit score', 'credit rating', 'creditworthiness', 'risk score')
                COMMENT = 'Credit score at loan origination time',
            
            -- Financial facts
            financials.amount AS amount
                WITH SYNONYMS ('financial amount', 'monetary value', 'transaction amount', 'fee amount')
                COMMENT = 'Financial transaction amount in NOK'
        )
        
        DIMENSIONS (
            -- Bank dimensions
            member_banks.bank_name AS bank_name
                WITH SYNONYMS ('bank', 'institution name', 'member bank', 'bank institution')
                COMMENT = 'Name of Nordic Banking Alliance member bank',
            member_banks.region AS region
                WITH SYNONYMS ('bank region', 'geographical area', 'territory', 'coverage area')
                COMMENT = 'Norwegian region where member bank operates',
            
            -- Customer dimensions
            customers.customer_name AS customer_name
                WITH SYNONYMS ('client name', 'customer', 'borrower name', 'company name')
                COMMENT = 'Name of banking customer or borrowing entity',
            customers.customer_type AS customer_type
                WITH SYNONYMS ('client type', 'customer category', 'borrower type', 'entity type')
                COMMENT = 'Type of customer: Corporate or Individual',
            customers.industry_sector AS industry_sector
                WITH SYNONYMS ('industry', 'sector', 'business sector', 'economic sector')
                COMMENT = 'Industry sector of corporate customer business activity',
            customers.geographic_region AS geographic_region
                WITH SYNONYMS ('customer region', 'location', 'geographical location', 'regional presence')
                COMMENT = 'Norwegian region where customer is located',
            
            -- Loan dimensions
            loans.loan_type AS loan_type
                WITH SYNONYMS ('loan product', 'credit type', 'lending product', 'facility type')
                COMMENT = 'Type of loan product (mortgage, corporate loan, green bond, etc.)',
            loans.green_project_category AS green_project_category
                WITH SYNONYMS ('green category', 'sustainability category', 'environmental category', 'ESG category')
                COMMENT = 'Category of green project for sustainable financing',
            loans.green_bond_framework_tag AS green_bond_framework_tag
                WITH SYNONYMS ('green bond', 'sustainable loan', 'ESG financing', 'green financing')
                COMMENT = 'Flag indicating if loan qualifies for green bond framework',
            loans.origination_date AS origination_date
                WITH SYNONYMS ('loan date', 'start date', 'booking date', 'disbursement date')
                COMMENT = 'Date when loan was originated and disbursed',
            loans.maturity_date AS maturity_date
                WITH SYNONYMS ('end date', 'expiry date', 'final payment date', 'term end')
                COMMENT = 'Date when loan reaches final maturity',
            
            -- Financial dimensions
            financials.record_type AS record_type
                WITH SYNONYMS ('transaction type', 'financial type', 'record category', 'revenue type')
                COMMENT = 'Type of financial record (Fee Income, Interest Income, etc.)',
            financials.record_date AS record_date
                WITH SYNONYMS ('transaction date', 'financial date', 'booking date', 'value date')
                COMMENT = 'Date when financial transaction was recorded'
        )
        
        METRICS (
            -- Portfolio metrics
            loans.total_exposure AS SUM(loans.outstanding_balance)
                WITH SYNONYMS ('total portfolio', 'total lending', 'portfolio exposure', 'loan portfolio value')
                COMMENT = 'Total outstanding loan portfolio exposure across all customers in NOK',
            loans.loan_count AS COUNT(loans.loan_id)
                WITH SYNONYMS ('number of loans', 'loan volume', 'total loans', 'loan transactions')
                COMMENT = 'Total number of active loans in the portfolio',
            loans.average_ltv AS AVG(loans.loan_to_value_ratio)
                WITH SYNONYMS ('average LTV', 'portfolio LTV', 'mean loan to value', 'collateral ratio')
                COMMENT = 'Average loan-to-value ratio across the loan portfolio',
            loans.average_interest_rate AS AVG(loans.interest_rate)
                WITH SYNONYMS ('average rate', 'portfolio rate', 'mean interest rate', 'weighted average rate')
                COMMENT = 'Average interest rate across the loan portfolio',
            
            -- Green bond metrics
            loans.green_portfolio_amount AS SUM(CASE WHEN loans.green_bond_framework_tag THEN loans.outstanding_balance ELSE 0 END)
                WITH SYNONYMS ('green portfolio', 'sustainable lending', 'ESG portfolio', 'green bond exposure')
                COMMENT = 'Total value of loans qualifying for green bond framework in NOK',
            loans.green_portfolio_percentage AS (SUM(CASE WHEN loans.green_bond_framework_tag THEN loans.outstanding_balance ELSE 0 END) / SUM(loans.outstanding_balance)) * 100
                WITH SYNONYMS ('green percentage', 'ESG percentage', 'sustainability ratio', 'green bond ratio')
                COMMENT = 'Percentage of total portfolio that qualifies for green bond framework',
            loans.green_loan_count AS COUNT(CASE WHEN loans.green_bond_framework_tag THEN loans.loan_id ELSE NULL END)
                WITH SYNONYMS ('green loans', 'sustainable loans', 'ESG loans', 'green bond count')
                COMMENT = 'Number of loans that qualify for green bond framework',
            
            -- Customer metrics
            customers.customer_count AS COUNT(customers.customer_id)
                WITH SYNONYMS ('total customers', 'client count', 'customer base', 'total clients')
                COMMENT = 'Total number of banking customers',
            customers.corporate_customer_count AS COUNT(CASE WHEN customers.customer_type = 'Corporate' THEN customers.customer_id ELSE NULL END)
                WITH SYNONYMS ('corporate clients', 'business customers', 'corporate accounts', 'B2B customers')
                COMMENT = 'Number of corporate banking customers',
            customers.individual_customer_count AS COUNT(CASE WHEN customers.customer_type = 'Individual' THEN customers.customer_id ELSE NULL END)
                WITH SYNONYMS ('individual clients', 'retail customers', 'personal banking', 'B2C customers')
                COMMENT = 'Number of individual retail banking customers',
            customers.average_credit_score AS AVG(customers.credit_score_origination)
                WITH SYNONYMS ('average credit score', 'portfolio credit quality', 'mean creditworthiness', 'risk profile')
                COMMENT = 'Average credit score across customer portfolio at origination',
            
            -- Bank metrics
            member_banks.bank_count AS COUNT(member_banks.member_bank_id)
                WITH SYNONYMS ('number of banks', 'alliance members', 'member institutions', 'bank network')
                COMMENT = 'Total number of Nordic Banking Alliance member banks',
            member_banks.total_alliance_assets AS SUM(member_banks.total_assets)
                WITH SYNONYMS ('alliance assets', 'total assets', 'combined assets', 'network assets')
                COMMENT = 'Combined total assets across all Nordic Banking Alliance member banks in NOK',
            
            -- Financial metrics (LTM = Last Twelve Months)
            financials.total_fee_revenue AS SUM(financials.amount)
                WITH SYNONYMS ('fee income', 'fee revenue', 'non-interest income', 'service fees')
                COMMENT = 'Total fee revenue and income across all financial records in NOK',
            financials.ltm_fee_income AS SUM(CASE WHEN financials.record_type IN ('FEE_REVENUE', 'COMMISSION') AND financials.record_date >= DATEADD(month, -12, CURRENT_DATE()) THEN financials.amount ELSE 0 END)
                WITH SYNONYMS ('LTM fees', 'last twelve months fees', 'trailing fee income', 'annual fee revenue')
                COMMENT = 'Last twelve months fee income for customer profitability analysis in NOK'
        );
        """
        
        try:
            self.session.sql(semantic_view_sql).collect()
            logger.info("Created SNOWBANK_DEMO_SV banking semantic view for Cortex Analyst")
            
            # Also create the market data semantic view
            market_success = self.create_market_semantic_view()
            if market_success:
                logger.info("Created both banking and market semantic views successfully")
            else:
                logger.warning("Banking semantic view created, but market semantic view failed")
            
        except Exception as e:
            logger.error(f"Failed to create banking semantic view: {str(e)}")
            raise
    
        # No need for separate helper views - everything is defined in the semantic view
    
    def validate_semantic_model(self) -> Dict[str, bool]:
        """Validate semantic view creation"""
        logger.info("Validating semantic view...")
        
        validation_results = {}
        
        # Check if semantic view exists
        try:
            # Check if semantic view exists using SHOW SEMANTIC VIEWS
            result = self.session.sql("SHOW SEMANTIC VIEWS").collect()
            semantic_views = [row['name'].upper() for row in result]
            
            # Check banking semantic view
            if 'SNOWBANK_DEMO_SV' in semantic_views:
                validation_results['SNOWBANK_DEMO_SV'] = True
                logger.info("SNOWBANK_DEMO_SV banking semantic view exists")
                
                # Try to query semantic view structure using DESCRIBE
                try:
                    describe_result = self.session.sql("DESCRIBE SEMANTIC VIEW SNOWBANK_DEMO_SV").collect()
                    
                    # Count dimensions and metrics from describe output
                    dimensions_count = len([row for row in describe_result if row['object_kind'] == 'DIMENSION'])
                    metrics_count = len([row for row in describe_result if row['object_kind'] == 'METRIC'])
                    
                    validation_results['SNOWBANK_DEMO_SV_DIMENSIONS'] = dimensions_count > 0
                    validation_results['SNOWBANK_DEMO_SV_METRICS'] = metrics_count > 0
                    
                    logger.info(f"Banking semantic view has {dimensions_count} dimensions and {metrics_count} metrics")
                    
                except Exception as e:
                    logger.warning(f"Could not validate banking semantic view structure: {str(e)}")
                    validation_results['SNOWBANK_DEMO_SV_DIMENSIONS'] = False
                    validation_results['SNOWBANK_DEMO_SV_METRICS'] = False
            else:
                validation_results['SNOWBANK_DEMO_SV'] = False
                logger.error("SNOWBANK_DEMO_SV banking semantic view does not exist")
            
            # Check market semantic view
            if 'MARKET_PEER_ANALYSIS_SV' in semantic_views:
                validation_results['MARKET_PEER_ANALYSIS_SV'] = True
                logger.info("MARKET_PEER_ANALYSIS_SV market semantic view exists")
                
                # Try to query semantic view structure using DESCRIBE
                try:
                    describe_result = self.session.sql("DESCRIBE SEMANTIC VIEW MARKET_PEER_ANALYSIS_SV").collect()
                    
                    # Count dimensions and metrics from describe output
                    dimensions_count = len([row for row in describe_result if row['object_kind'] == 'DIMENSION'])
                    metrics_count = len([row for row in describe_result if row['object_kind'] == 'METRIC'])
                    
                    validation_results['MARKET_PEER_ANALYSIS_SV_DIMENSIONS'] = dimensions_count > 0
                    validation_results['MARKET_PEER_ANALYSIS_SV_METRICS'] = metrics_count > 0
                    
                    logger.info(f"Market semantic view has {dimensions_count} dimensions and {metrics_count} metrics")
                    
                except Exception as e:
                    logger.warning(f"Could not validate market semantic view structure: {str(e)}")
                    validation_results['MARKET_PEER_ANALYSIS_SV_DIMENSIONS'] = False
                    validation_results['MARKET_PEER_ANALYSIS_SV_METRICS'] = False
            else:
                validation_results['MARKET_PEER_ANALYSIS_SV'] = False
                logger.error("MARKET_PEER_ANALYSIS_SV market semantic view does not exist")
                
        except Exception as e:
            validation_results['SNOWBANK_DEMO_SV'] = False
            logger.error(f"Failed to validate semantic view: {str(e)}")
        
        return validation_results
    
    def create_market_semantic_view(self):
        """Create semantic view for market data peer analysis"""
        logger.info("Creating market data semantic view...")
        
        # Drop existing market semantic view first
        try:
            self.session.sql("DROP SEMANTIC VIEW IF EXISTS MARKET_PEER_ANALYSIS_SV").collect()
        except SnowparkSQLException:
            pass
        
        # Also drop regular view with same name if it exists
        try:
            self.session.sql("DROP VIEW IF EXISTS MARKET_PEER_ANALYSIS_SV").collect()
        except SnowparkSQLException:
            pass
        
        # Create dedicated semantic view for market data and peer analysis
        market_semantic_view_sql = """
        CREATE OR REPLACE SEMANTIC VIEW MARKET_PEER_ANALYSIS_SV
        
        TABLES (
            market_data AS FSI_DEMOS.BANK_DEMO.MARKET_DATA PRIMARY KEY (TICKER, TRADE_DATE)
                WITH SYNONYMS ('stock prices', 'peer performance', 'market benchmarks', 'competitor data', 'stock market')
                COMMENT = 'Norwegian and Nordic stock market data for industry peer analysis and benchmarking'
        )
        
        -- No relationships needed - single table for market analysis
        
        FACTS (
            -- Market data facts
            market_data.close_price AS close_price
                WITH SYNONYMS ('stock price', 'share price', 'market price', 'closing price', 'stock value')
                COMMENT = 'Daily closing stock price in NOK'
        )
        
        DIMENSIONS (
            -- Market data dimensions for peer analysis
            market_data.ticker AS ticker
                WITH SYNONYMS ('stock ticker', 'symbol', 'stock symbol', 'trading symbol', 'stock code')
                COMMENT = 'Stock exchange ticker symbol for Norwegian/Nordic companies',
            market_data.company_name AS company_name
                WITH SYNONYMS ('company', 'listed company', 'public company', 'stock company', 'corporation')
                COMMENT = 'Name of publicly traded company for peer analysis',
            market_data.peer_group AS peer_group
                WITH SYNONYMS ('industry group', 'sector group', 'peer sector', 'industry category', 'sector')
                COMMENT = 'Industry peer group for competitive benchmarking (Aquaculture, Banking, Maritime, etc.)',
            market_data.trade_date AS trade_date
                WITH SYNONYMS ('trading date', 'market date', 'price date', 'quotation date', 'business date')
                COMMENT = 'Date of stock market trading and price quotation'
        )
        
        METRICS (
            -- Stock performance metrics for peer analysis
            market_data.avg_stock_price AS AVG(market_data.close_price)
                WITH SYNONYMS ('average stock price', 'mean share price', 'peer stock performance', 'average price')
                COMMENT = 'Average stock price for peer analysis and competitive benchmarking in NOK',
            market_data.max_stock_price AS MAX(market_data.close_price)
                WITH SYNONYMS ('highest stock price', 'peak price', 'maximum price', 'highest value')
                COMMENT = 'Highest stock price in the period for peer comparison in NOK',
            market_data.min_stock_price AS MIN(market_data.close_price)
                WITH SYNONYMS ('lowest stock price', 'minimum price', 'lowest value', 'trough price')
                COMMENT = 'Lowest stock price in the period for peer comparison in NOK',
            market_data.price_count AS COUNT(market_data.close_price)
                WITH SYNONYMS ('trading days', 'price observations', 'data points', 'trading frequency')
                COMMENT = 'Number of trading days with price data for peer comparison',
            market_data.price_volatility AS STDDEV(market_data.close_price)
                WITH SYNONYMS ('stock volatility', 'price variance', 'market volatility', 'price stability')
                COMMENT = 'Price volatility measure for risk assessment in peer analysis'
        );
        """
        
        try:
            self.session.sql(market_semantic_view_sql).collect()
            logger.info("Created MARKET_PEER_ANALYSIS_SV semantic view for peer analysis")
            return True
        except Exception as e:
            logger.error(f"Failed to create market semantic view: {str(e)}")
            return False
