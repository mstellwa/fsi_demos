#!/usr/bin/env python3
"""
Snowdrift Financials - M3: Semantic View Creation
Creates proper SEMANTIC VIEW with FACTS, DIMENSIONS, METRICS, COMMENTS, and SYNONYMS
"""

import logging
import yaml
from typing import List, Dict, Any
from snowflake.snowpark import Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('snowdrift_semantic_view.log')
    ]
)
logger = logging.getLogger(__name__)

class SemanticViewCreator:
    """Create proper SEMANTIC VIEW for Snowdrift Financials Insurance analytics"""
    
    def __init__(self, config_path: str = "config.yaml", connection_name: str = "default"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self.connection_name = connection_name
        self.session = None
        
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
    
    def create_policy_semantic_view(self):
        """Create proper SEMANTIC VIEW for Norwegian insurance analytics using correct syntax"""
        logger.info("Creating INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW...")
        
        self.session.sql("USE SCHEMA INSURANCE_ANALYTICS").collect()
        
        # Create proper SEMANTIC VIEW with correct syntax
        create_semantic_view_sql = """
        CREATE OR REPLACE SEMANTIC VIEW NORWEGIAN_INSURANCE_SEMANTIC_VIEW

          TABLES (
            policies AS INSURANCE.POLICIES
              PRIMARY KEY (POLICY_ID)
              WITH SYNONYMS ('insurance policies', 'policy data', 'contracts')
              COMMENT = 'Norwegian property insurance policies with coverage and risk information',
              
            claims AS INSURANCE.CLAIMS
              PRIMARY KEY (CLAIM_ID)
              WITH SYNONYMS ('insurance claims', 'loss data', 'claim reports', 'flood claims', 'property claims')
              COMMENT = 'Insurance claims data including amounts, status, dates, and location information for flood and property damage analysis',
              
            geo_risk AS INSURANCE.GEO_RISK_SCORES
              PRIMARY KEY (MUNICIPALITY, POSTAL_CODE)
              WITH SYNONYMS ('flood risk', 'geographic risk', 'location risk', 'norwegian risk')
              COMMENT = 'Norwegian geographic flood risk scores by municipality and postal code'
          )

          RELATIONSHIPS (
            claims_to_policies AS
              claims (POLICY_ID) REFERENCES policies,
            policies_to_geo_risk AS
              policies (MUNICIPALITY, POSTAL_CODE) REFERENCES geo_risk (MUNICIPALITY, POSTAL_CODE),
            claims_to_geo_risk AS
              claims (MUNICIPALITY, POSTAL_CODE) REFERENCES geo_risk (MUNICIPALITY, POSTAL_CODE)
          )

          FACTS (
            policies.policy_identifier AS policies.POLICY_ID
              WITH SYNONYMS = ('policy number', 'policy code', 'contract id')
              COMMENT = 'Unique identifier for each insurance policy',
              
            policies.customer_identifier AS policies.CUSTOMER_ID
              WITH SYNONYMS = ('customer id', 'client id', 'policyholder id')
              COMMENT = 'Unique identifier for the policyholder',
              
            claims.claim_identifier AS claims.CLAIM_ID
              WITH SYNONYMS = ('claim number', 'claim code', 'loss id')
              COMMENT = 'Unique identifier for each insurance claim'
          )

          DIMENSIONS (
            policies.policy_type AS policies.POLICY_TYPE
              WITH SYNONYMS = ('insurance type', 'coverage type', 'product type', 'property type')
              COMMENT = 'Type of insurance policy (RESIDENTIAL, COMMERCIAL)',
              
            policies.policy_status AS policies.STATUS
              WITH SYNONYMS = ('status', 'policy state', 'contract status')
              COMMENT = 'Current status of the insurance policy',
              
            policies.policy_year AS YEAR(policies.EFFECTIVE_DATE)
              WITH SYNONYMS = ('underwriting year', 'policy start year', 'effective year')
              COMMENT = 'Year when the policy became effective',
              
            policies.policy_quarter AS QUARTER(policies.EFFECTIVE_DATE)
              WITH SYNONYMS = ('underwriting quarter', 'policy quarter')
              COMMENT = 'Quarter when the policy became effective',
              
            policies.policy_municipality AS policies.MUNICIPALITY
              WITH SYNONYMS = ('municipality', 'kommune', 'local authority', 'norwegian municipality')
              COMMENT = 'Norwegian municipality where the insured property is located',
              
            policies.policy_city AS policies.CITY
              WITH SYNONYMS = ('city', 'town', 'urban area')
              COMMENT = 'City where the insured property is located',
              
            policies.policy_postal_code AS policies.POSTAL_CODE
              WITH SYNONYMS = ('postal code', 'zip code', 'post code')
              COMMENT = 'Norwegian postal code for the property location',
              
            geo_risk.flood_risk_score AS geo_risk.FLOOD_RISK_SCORE
              WITH SYNONYMS = ('flood risk', 'risk score', 'flood rating', 'climate risk')
              COMMENT = 'Flood risk score from 1-10 where 10 is highest risk based on Norwegian climate data',
              
            geo_risk.flood_risk_category AS 
              CASE 
                WHEN geo_risk.FLOOD_RISK_SCORE BETWEEN 1 AND 3 THEN 'Low Risk'
                WHEN geo_risk.FLOOD_RISK_SCORE BETWEEN 4 AND 6 THEN 'Medium Risk'
                WHEN geo_risk.FLOOD_RISK_SCORE BETWEEN 7 AND 10 THEN 'High Risk'
                ELSE 'Unknown Risk'
              END
              WITH SYNONYMS = ('risk category', 'risk level', 'flood category', 'risk classification')
              COMMENT = 'Categorized flood risk level for Norwegian properties',
              
            claims.claim_status AS claims.STATUS
              WITH SYNONYMS = ('claim status', 'claim state', 'loss status')
              COMMENT = 'Current status of the insurance claim',
              
            claims.loss_year AS YEAR(claims.LOSS_DATE)
              WITH SYNONYMS = ('loss year', 'claim year', 'incident year')
              COMMENT = 'Year when the loss occurred',
              
            claims.claim_municipality AS claims.MUNICIPALITY
              WITH SYNONYMS = ('claim municipality', 'claim location', 'loss municipality', 'damage municipality')
              COMMENT = 'Norwegian municipality where the claim occurred',
              
            claims.claim_city AS claims.CITY
              WITH SYNONYMS = ('claim city', 'loss city', 'damage location', 'incident city', 'Kristiansand', 'Bergen', 'Oslo', 'Stavanger', 'Trondheim')
              COMMENT = 'City where the claim occurred - searchable by Norwegian city names',
              
            claims.is_flood_related AS 
              CASE 
                WHEN LOWER(claims.DESCRIPTION) LIKE '%flood%' 
                  OR LOWER(claims.DESCRIPTION) LIKE '%water damage%'
                  OR LOWER(claims.DESCRIPTION) LIKE '%storm surge%'
                  OR LOWER(claims.DESCRIPTION) LIKE '%heavy rain%'
                  OR LOWER(claims.DESCRIPTION) LIKE '%overflowing%'
                THEN 'Yes'
                ELSE 'No'
              END
              WITH SYNONYMS = ('flood claim', 'flood damage', 'water damage claim', 'flood related')
              COMMENT = 'Text indicator with values "Yes" or "No" - whether claim is flood-related',
              
            claims.has_flood_damage AS (
              LOWER(claims.DESCRIPTION) LIKE '%flood%' 
              OR LOWER(claims.DESCRIPTION) LIKE '%water damage%'
              OR LOWER(claims.DESCRIPTION) LIKE '%storm surge%'
              OR LOWER(claims.DESCRIPTION) LIKE '%heavy rain%'
              OR LOWER(claims.DESCRIPTION) LIKE '%overflowing%'
            )
              WITH SYNONYMS = ('flood damage', 'is flood', 'flood claim', 'water damage')
              COMMENT = 'Boolean indicator (TRUE/FALSE) for flood-related claims - use for filtering'
          )

          METRICS (
            policies.policy_count AS COUNT(policies.POLICY_ID)
              WITH SYNONYMS = ('number of policies', 'policy count', 'total policies')
              COMMENT = 'Total number of insurance policies',
              
            policies.total_premium AS SUM(policies.PREMIUM)
              WITH SYNONYMS = ('total premium', 'premium income', 'total cost')
              COMMENT = 'Total annual premium amount in Norwegian Kroner (NOK)',
              
            policies.average_premium AS AVG(policies.PREMIUM)
              WITH SYNONYMS = ('average premium', 'mean premium', 'typical cost')
              COMMENT = 'Average annual premium per policy in NOK',
              
            policies.total_coverage AS SUM(policies.COVERAGE_AMOUNT)
              WITH SYNONYMS = ('total coverage', 'total insured amount', 'sum insured')
              COMMENT = 'Total coverage amount across all policies in NOK',
              
            policies.average_coverage AS AVG(policies.COVERAGE_AMOUNT)
              WITH SYNONYMS = ('average coverage', 'mean coverage', 'typical coverage')
              COMMENT = 'Average coverage amount per policy in NOK',
              
            claims.claim_count AS COUNT(claims.CLAIM_ID)
              WITH SYNONYMS = ('number of claims', 'claim count', 'total claims')
              COMMENT = 'Total number of insurance claims',
              
            claims.total_claim_amount AS SUM(claims.CLAIM_AMOUNT)
              WITH SYNONYMS = ('total claims', 'claim amount', 'loss amount', 'total loss')
              COMMENT = 'Total claimed amount across all claims in NOK',
              
            claims.average_claim_amount AS AVG(claims.CLAIM_AMOUNT)
              WITH SYNONYMS = ('average claim', 'mean claim', 'typical claim')
              COMMENT = 'Average claim amount in NOK',
              
            claims.total_paid_amount AS SUM(claims.PAID_AMOUNT)
              WITH SYNONYMS = ('total paid', 'settlements', 'compensation paid')
              COMMENT = 'Total amount paid out for claims in NOK',
              
            claims.claim_frequency AS COUNT(claims.CLAIM_ID) / NULLIF(COUNT(DISTINCT claims.POLICY_ID), 0)
              WITH SYNONYMS = ('claim frequency', 'claims per policy', 'loss frequency', 'claim rate')
              COMMENT = 'Average number of claims per policy - key metric for underwriting',
              
            claims.claims_per_municipality AS COUNT(claims.CLAIM_ID) / NULLIF(COUNT(DISTINCT claims.MUNICIPALITY), 0)
              WITH SYNONYMS = ('claims per municipality', 'municipal claim density', 'regional claim frequency')
              COMMENT = 'Average number of claims per municipality for geographic risk analysis',
              
            claims.flood_claim_count AS COUNT(CASE WHEN LOWER(claims.DESCRIPTION) LIKE '%flood%' OR LOWER(claims.DESCRIPTION) LIKE '%water damage%' THEN 1 END)
              WITH SYNONYMS = ('flood claims', 'water damage claims', 'flood claim count')
              COMMENT = 'Number of flood-related claims based on description',
              
            claims.flood_claim_severity AS AVG(CASE WHEN LOWER(claims.DESCRIPTION) LIKE '%flood%' OR LOWER(claims.DESCRIPTION) LIKE '%water damage%' THEN claims.CLAIM_AMOUNT END)
              WITH SYNONYMS = ('flood claim severity', 'average flood claim', 'flood damage amount')
              COMMENT = 'Average claim amount for flood-related claims in NOK'
          )

          COMMENT = 'Comprehensive Norwegian Insurance Analytics - Policy, claims, and flood risk data for Snowdrift Financials with geographic and financial metrics'
        """
        
        self.session.sql(create_semantic_view_sql).collect()
        logger.info("✓ NORWEGIAN_INSURANCE_SEMANTIC_VIEW created successfully")
    
    def validate_semantic_view(self):
        """Validate semantic view using proper SEMANTIC_VIEW query syntax"""
        logger.info("Validating semantic view with test queries...")
        
        test_queries = [
            {
                'description': 'Total policy count metric',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    METRICS policies.policy_count
                )
                """
            },
            {
                'description': 'Total premium and average premium metrics',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    METRICS policies.total_premium, policies.average_premium
                )
                """
            },
            {
                'description': 'Policy count by municipality dimension',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    DIMENSIONS policies.policy_municipality
                    METRICS policies.policy_count
                ) LIMIT 5
                """
            },
            {
                'description': 'Premium by flood risk category',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    DIMENSIONS geo_risk.flood_risk_category
                    METRICS policies.total_premium
                )
                """
            },
            {
                'description': 'Claims metrics summary',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    METRICS claims.claim_count, claims.total_claim_amount, claims.average_claim_amount
                )
                """
            },
            {
                'description': 'Policy count by year dimension',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    NORWEGIAN_INSURANCE_SEMANTIC_VIEW
                    DIMENSIONS policies.policy_year
                    METRICS policies.policy_count
                ) ORDER BY POLICY_YEAR LIMIT 5
                """
            }
        ]
        
        for i, query in enumerate(test_queries, 1):
            try:
                logger.info(f"Q{i}: {query['description']}")
                result = self.session.sql(query['sql']).collect()
                logger.info(f"✓ Results: {len(result)} rows returned")
                
                # Log sample results
                for j, row in enumerate(result[:3]):
                    row_dict = {col: row[col] for col in row.as_dict().keys()}
                    logger.info(f"  Row {j+1}: {row_dict}")
                    
            except Exception as e:
                logger.error(f"✗ Query {i} failed: {str(e)}")
                raise
        
        logger.info(f"Semantic view validation completed: {len(test_queries)}/{len(test_queries)} queries passed")
    
    def create_banking_semantic_view(self):
        """Create comprehensive Banking semantic view with cross-division integration"""
        logger.info("Creating BANK_ANALYTICS.CUSTOMER_360_VIEW...")
        
        self.session.sql("USE SCHEMA BANK_ANALYTICS").collect()
        
        # Create comprehensive Banking + Insurance semantic view with proper syntax
        create_banking_view_sql = """
        CREATE OR REPLACE SEMANTIC VIEW CUSTOMER_360_VIEW

          TABLES (
            customers AS BANK.CUSTOMERS
              PRIMARY KEY (CUSTOMER_ID)
              WITH SYNONYMS ('banking customers', 'bank clients', 'customer data')
              COMMENT = 'Norwegian banking customers with cross-references to insurance policies',
              
            accounts AS BANK.ACCOUNTS
              PRIMARY KEY (ACCOUNT_ID)
              WITH SYNONYMS ('bank accounts', 'checking accounts', 'savings accounts', 'account data')
              COMMENT = 'Customer bank accounts including checking, savings, and loan accounts',
              
            transactions AS BANK.TRANSACTIONS
              PRIMARY KEY (TRANSACTION_ID)
              WITH SYNONYMS ('banking transactions', 'payments', 'spending data', 'transaction history')
              COMMENT = 'Banking transaction history with Norwegian merchant patterns and spending behavior',
              
            loans AS BANK.LOANS
              PRIMARY KEY (LOAN_ID)
              WITH SYNONYMS ('customer loans', 'mortgages', 'personal loans', 'auto loans')
              COMMENT = 'Customer loan portfolio including mortgages, personal, and auto loans',
              
            corporate_entities AS BANK.BRREG_CORPORATE
              PRIMARY KEY (ORGANIZATION_NUMBER)
              WITH SYNONYMS ('norwegian companies', 'corporate clients', 'business registry', 'brreg data')
              COMMENT = 'Norwegian corporate entities with beneficial ownership for compliance analysis',
              
            insurance_policies AS INSURANCE.POLICIES
              PRIMARY KEY (POLICY_ID)
              WITH SYNONYMS ('insurance policies', 'property insurance', 'coverage data')
              COMMENT = 'Insurance policies for cross-division customer analysis',
              
            insurance_claims AS INSURANCE.CLAIMS
              PRIMARY KEY (CLAIM_ID)
              WITH SYNONYMS ('insurance claims', 'loss data', 'claim reports')
              COMMENT = 'Insurance claims data for risk correlation analysis'
          )

          RELATIONSHIPS (
            customers_to_accounts AS
              customers (CUSTOMER_ID) REFERENCES accounts,
            accounts_to_transactions AS
              accounts (ACCOUNT_ID) REFERENCES transactions,
            customers_to_loans AS
              customers (CUSTOMER_ID) REFERENCES loans,
            customers_to_insurance AS
              customers (INSURANCE_POLICY_ID) REFERENCES insurance_policies (POLICY_ID),
            insurance_policies_to_claims AS
              insurance_policies (POLICY_ID) REFERENCES insurance_claims
          )

          FACTS (
            customers.customer_identifier AS customers.CUSTOMER_ID
              WITH SYNONYMS = ('customer id', 'client id', 'banking customer id')
              COMMENT = 'Unique identifier for banking customers',
              
            customers.first_name AS customers.FIRST_NAME
              WITH SYNONYMS = ('first name', 'given name')
              COMMENT = 'Customer first name',
              
            customers.last_name AS customers.LAST_NAME
              WITH SYNONYMS = ('last name', 'surname', 'family name')
              COMMENT = 'Customer last name',
              
            customers.national_id AS customers.NATIONAL_ID
              WITH SYNONYMS = ('national id', 'norwegian id', 'personal number')
              COMMENT = 'Norwegian national identification number',
              
            customers.insurance_policy_id AS customers.INSURANCE_POLICY_ID
              WITH SYNONYMS = ('insurance policy', 'policy reference', 'cross reference')
              COMMENT = 'Cross-reference to insurance policy for integrated customer view',
              
            accounts.account_identifier AS accounts.ACCOUNT_ID
              WITH SYNONYMS = ('account id', 'account number', 'bank account')
              COMMENT = 'Unique identifier for bank accounts',
              
            transactions.transaction_identifier AS transactions.TRANSACTION_ID
              WITH SYNONYMS = ('transaction id', 'payment id', 'txn id')
              COMMENT = 'Unique identifier for banking transactions',
              
            loans.loan_identifier AS loans.LOAN_ID
              WITH SYNONYMS = ('loan id', 'loan number', 'mortgage id')
              COMMENT = 'Unique identifier for customer loans'
          )

          DIMENSIONS (
            customers.customer_municipality AS customers.MUNICIPALITY
              WITH SYNONYMS = ('municipality', 'kommune', 'local authority', 'norwegian municipality')
              COMMENT = 'Norwegian municipality where customer resides',
              
            customers.customer_city AS customers.CITY
              WITH SYNONYMS = ('city', 'town', 'urban area')
              COMMENT = 'City where customer resides',
              
            customers.customer_status AS customers.STATUS
              WITH SYNONYMS = ('customer status', 'account status', 'client status')
              COMMENT = 'Current status of banking customer',
              
            customers.customer_since_year AS YEAR(customers.CUSTOMER_SINCE)
              WITH SYNONYMS = ('onboarding year', 'customer start year', 'relationship start')
              COMMENT = 'Year when customer relationship began',
              
            accounts.account_type AS accounts.ACCOUNT_TYPE
              WITH SYNONYMS = ('account type', 'product type', 'banking product')
              COMMENT = 'Type of bank account (checking, savings, mortgage, loan)',
              
            accounts.account_status AS accounts.STATUS
              WITH SYNONYMS = ('account status', 'account state')
              COMMENT = 'Current status of bank account',
              
            transactions.merchant_category AS transactions.MERCHANT_CATEGORY
              WITH SYNONYMS = ('spending category', 'merchant type', 'expense category')
              COMMENT = 'Category of merchant for spending analysis',
              
            transactions.transaction_type AS transactions.TRANSACTION_TYPE
              WITH SYNONYMS = ('transaction type', 'payment type', 'debit credit')
              COMMENT = 'Type of transaction (debit or credit)',
              
            transactions.transaction_month AS MONTH(transactions.TRANSACTION_DATE)
              WITH SYNONYMS = ('transaction month', 'spending month')
              COMMENT = 'Month of transaction for seasonal analysis',
              
            loans.loan_type AS loans.LOAN_TYPE
              WITH SYNONYMS = ('loan type', 'loan product', 'lending product')
              COMMENT = 'Type of loan (mortgage, personal, auto)',
              
            loans.loan_status AS loans.STATUS
              WITH SYNONYMS = ('loan status', 'payment status', 'loan state')
              COMMENT = 'Current status of loan',
              
            corporate_entities.business_activity AS corporate_entities.BUSINESS_ACTIVITY_DESC
              WITH SYNONYMS = ('business activity', 'industry', 'business type')
              COMMENT = 'Description of corporate business activity',
              
            customers.has_insurance AS 
              CASE 
                WHEN customers.INSURANCE_POLICY_ID IS NOT NULL THEN 'Yes'
                ELSE 'No'
              END
              WITH SYNONYMS = ('has insurance', 'insurance customer', 'cross division customer')
              COMMENT = 'Whether customer has insurance policy for cross-selling analysis'
          )

          METRICS (
            customers.customer_count AS COUNT(customers.CUSTOMER_ID)
              WITH SYNONYMS = ('number of customers', 'customer count', 'client count')
              COMMENT = 'Total number of banking customers',
              
            accounts.total_balance AS SUM(accounts.BALANCE)
              WITH SYNONYMS = ('total balance', 'total deposits', 'account balances')
              COMMENT = 'Total balance across all customer accounts in NOK',
              
            accounts.average_balance AS AVG(accounts.BALANCE)
              WITH SYNONYMS = ('average balance', 'mean balance', 'typical balance')
              COMMENT = 'Average account balance per customer in NOK',
              
            transactions.transaction_count AS COUNT(transactions.TRANSACTION_ID)
              WITH SYNONYMS = ('number of transactions', 'transaction volume', 'payment count')
              COMMENT = 'Total number of banking transactions',
              
            transactions.total_transaction_amount AS SUM(ABS(transactions.AMOUNT))
              WITH SYNONYMS = ('total transaction volume', 'total spending', 'payment volume')
              COMMENT = 'Total transaction amount across all customers in NOK',
              
            transactions.average_transaction_amount AS AVG(ABS(transactions.AMOUNT))
              WITH SYNONYMS = ('average transaction', 'typical spending', 'mean payment')
              COMMENT = 'Average transaction amount per transaction in NOK',
              
            loans.total_loan_balance AS SUM(loans.CURRENT_BALANCE)
              WITH SYNONYMS = ('total loan balance', 'outstanding loans', 'loan portfolio')
              COMMENT = 'Total outstanding loan balance across all customers in NOK',
              
            loans.loan_count AS COUNT(loans.LOAN_ID)
              WITH SYNONYMS = ('number of loans', 'loan count', 'lending volume')
              COMMENT = 'Total number of active loans',
              
            customers.insurance_overlap_count AS COUNT(CASE WHEN customers.INSURANCE_POLICY_ID IS NOT NULL THEN 1 END)
              WITH SYNONYMS = ('cross division customers', 'insurance overlap', 'integrated customers')
              COMMENT = 'Number of banking customers who also have insurance policies'
          )
          COMMENT = 'Comprehensive customer 360 view combining banking and insurance data for Norwegian customers'
        """
        
        self.session.sql(create_banking_view_sql).collect()
        logger.info("✓ CUSTOMER_360_VIEW created successfully")
    
    def validate_banking_semantic_view(self):
        """Validate Banking semantic view with cross-division test queries"""
        logger.info("Validating Banking semantic view with test queries...")
        
        test_queries = [
            {
                'description': 'Customer count by municipality',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    CUSTOMER_360_VIEW
                    DIMENSIONS customers.customer_municipality
                    METRICS customers.customer_count
                ) LIMIT 5
                """
            },
            {
                'description': 'Cross-division customer analysis',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    CUSTOMER_360_VIEW
                    DIMENSIONS customers.has_insurance
                    METRICS customers.customer_count, customers.insurance_overlap_count
                )
                """
            },
            {
                'description': 'Account balances by account type',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    CUSTOMER_360_VIEW
                    DIMENSIONS accounts.account_type
                    METRICS accounts.total_balance, accounts.average_balance
                )
                """
            },
            {
                'description': 'Transaction patterns by category',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    CUSTOMER_360_VIEW
                    DIMENSIONS transactions.merchant_category
                    METRICS transactions.transaction_count, transactions.total_transaction_amount
                ) LIMIT 10
                """
            },
            {
                'description': 'Loan portfolio summary',
                'sql': """
                SELECT * FROM SEMANTIC_VIEW(
                    CUSTOMER_360_VIEW
                    DIMENSIONS loans.loan_type
                    METRICS loans.loan_count, loans.total_loan_balance
                )
                """
            }
        ]
        
        for i, query in enumerate(test_queries, 1):
            try:
                logger.info(f"Q{i}: {query['description']}")
                result = self.session.sql(query['sql']).collect()
                logger.info(f"✓ Results: {len(result)} rows returned")
                
                # Log sample results
                for j, row in enumerate(result[:3]):
                    row_dict = {col: row[col] for col in row.as_dict().keys()}
                    logger.info(f"  Row {j+1}: {row_dict}")
                    
            except Exception as e:
                logger.error(f"✗ Query {i} failed: {str(e)}")
                raise
        
        logger.info(f"Banking semantic view validation completed: {len(test_queries)}/{len(test_queries)} queries passed")
    
    def run_semantic_view_creation(self):
        """Execute complete semantic view creation and validation"""
        logger.info("Starting M3 - Semantic View Creation...")
        
        try:
            self.create_session()
            self.session.sql(f"USE DATABASE {self.config['global']['database']}").collect()
            
            # Step 1: Create Insurance Semantic View (if not exists)
            logger.info("=== Step 1: Create Insurance SEMANTIC VIEW ===")
            try:
                # Test if insurance view exists
                self.session.sql("SELECT * FROM SEMANTIC_VIEW(NORWEGIAN_INSURANCE_SEMANTIC_VIEW) LIMIT 1").collect()
                logger.info("✓ Insurance semantic view already exists")
            except:
                logger.info("Creating Insurance semantic view...")
                self.create_policy_semantic_view()
            
            # Step 2: Create Banking Cross-Division Semantic View
            logger.info("=== Step 2: Create Banking CUSTOMER_360_VIEW ===")
            self.create_banking_semantic_view()
            
            # Step 3: Validate Banking Semantic View
            logger.info("=== Step 3: Validate Banking SEMANTIC VIEW ===")
            self.validate_banking_semantic_view()
            
            logger.info("Semantic View Creation completed successfully!")
            logger.info("Both Insurance and Banking SEMANTIC VIEWs are ready for Cortex Analyst")
            
        except Exception as e:
            logger.error(f"Semantic view creation failed: {str(e)}")
            raise
        finally:
            if self.session:
                self.session.close()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create Semantic View")
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
        creator = SemanticViewCreator(connection_name=args.connection)
        creator.run_semantic_view_creation()
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
