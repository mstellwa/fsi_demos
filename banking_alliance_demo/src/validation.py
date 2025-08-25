"""
Validation framework for SnowBank Intelligence Demo
Comprehensive validation of data, services, and demo functionality
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

from .config import DemoConfig

logger = logging.getLogger(__name__)


class ValidationFramework:
    """Comprehensive validation framework for demo setup"""
    
    def __init__(self, config: DemoConfig):
        self.config = config
        self.session = config.session
        
    def validate_all(self) -> Dict[str, Any]:
        """Run all validation checks"""
        logger.info("Starting comprehensive demo validation...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'checks': {}
        }
        
        # Run all validation categories
        validation_categories = [
            ('data_volumes', self.validate_data_volumes),
            ('data_integrity', self.validate_data_integrity), 
            ('data_distribution', self.validate_data_distribution),
            ('green_lending', self.validate_green_lending),
            ('document_corpus', self.validate_document_corpus),
            ('search_services', self.validate_search_services),
            ('semantic_model', self.validate_semantic_model),
            ('agent_readiness', self.validate_agent_readiness)
        ]
        
        for category, validation_func in validation_categories:
            try:
                logger.info(f"Running {category} validation...")
                check_result = validation_func()
                results['checks'][category] = check_result
                
                if not check_result.get('passed', False):
                    results['success'] = False
                    
            except Exception as e:
                logger.error(f"Validation {category} failed with error: {str(e)}")
                results['checks'][category] = {
                    'passed': False,
                    'error': str(e)
                }
                results['success'] = False
        
        # Overall summary
        if results['success']:
            logger.info("✅ All validation checks passed!")
        else:
            logger.error("❌ Some validation checks failed")
        
        return results
    
    def validate_data_volumes(self) -> Dict[str, Any]:
        """Validate expected data volumes with ±10% tolerance"""
        expected_volumes = {
            'CUSTOMERS': self.config.get_config('CUSTOMER_COUNT'),
            'LOANS': self.config.get_config('LOAN_COUNT'),
            'MEMBER_BANKS': 5,  # Fixed count
            'MARKET_DATA': 0,  # Will be calculated
            'DOCUMENTS': 0  # Will be calculated based on scenarios
        }
        
        # Calculate expected market data volume
        history_months = self.config.get_config('HISTORY_MONTHS')
        companies_count = 10  # Fixed number of companies
        expected_volumes['MARKET_DATA'] = history_months * 30 * companies_count  # Approx daily data
        
        # Calculate expected documents (35-50 per scenario, 4 scenarios)
        expected_volumes['DOCUMENTS'] = 4 * 40  # Average 40 per scenario
        
        results = {
            'passed': True,
            'details': {},
            'tolerance': 0.1  # 10% tolerance
        }
        
        for table, expected_count in expected_volumes.items():
            try:
                actual_result = self.session.sql(f"SELECT COUNT(*) as cnt FROM {table}").collect()
                actual_count = actual_result[0]['CNT'] if actual_result else 0
                
                # Calculate tolerance range
                min_expected = int(expected_count * (1 - results['tolerance']))
                max_expected = int(expected_count * (1 + results['tolerance']))
                
                passed = min_expected <= actual_count <= max_expected
                
                results['details'][table] = {
                    'expected': expected_count,
                    'actual': actual_count,
                    'range': f"{min_expected}-{max_expected}",
                    'passed': passed
                }
                
                if not passed:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][table] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate referential integrity"""
        integrity_checks = [
            {
                'name': 'customers_to_banks',
                'query': """
                    SELECT COUNT(*) as violations 
                    FROM CUSTOMERS c 
                    LEFT JOIN MEMBER_BANKS mb ON c.MEMBER_BANK_ID = mb.MEMBER_BANK_ID 
                    WHERE mb.MEMBER_BANK_ID IS NULL
                """,
                'description': 'All customers must reference valid member banks'
            },
            {
                'name': 'loans_to_customers',
                'query': """
                    SELECT COUNT(*) as violations 
                    FROM LOANS l 
                    LEFT JOIN CUSTOMERS c ON l.CUSTOMER_ID = c.CUSTOMER_ID 
                    WHERE c.CUSTOMER_ID IS NULL
                """,
                'description': 'All loans must reference valid customers'
            },
            {
                'name': 'loans_to_banks',
                'query': """
                    SELECT COUNT(*) as violations 
                    FROM LOANS l 
                    LEFT JOIN MEMBER_BANKS mb ON l.MEMBER_BANK_ID = mb.MEMBER_BANK_ID 
                    WHERE mb.MEMBER_BANK_ID IS NULL
                """,
                'description': 'All loans must reference valid member banks'
            },
            {
                'name': 'financials_to_customers',
                'query': """
                    SELECT COUNT(*) as violations 
                    FROM FINANCIALS f 
                    LEFT JOIN CUSTOMERS c ON f.CUSTOMER_ID = c.CUSTOMER_ID 
                    WHERE c.CUSTOMER_ID IS NULL
                """,
                'description': 'All financial records must reference valid customers'
            }
        ]
        
        results = {
            'passed': True,
            'details': {}
        }
        
        for check in integrity_checks:
            try:
                result = self.session.sql(check['query']).collect()
                violations = result[0]['VIOLATIONS'] if result else 0
                
                passed = violations == 0
                
                results['details'][check['name']] = {
                    'description': check['description'],
                    'violations': violations,
                    'passed': passed
                }
                
                if not passed:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][check['name']] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def validate_data_distribution(self) -> Dict[str, Any]:
        """Validate geographic and industry distributions"""
        distribution_checks = [
            {
                'name': 'aquaculture_in_helgeland',
                'query': """
                    SELECT 
                        COUNT(*) as total_aquaculture,
                        SUM(CASE WHEN GEOGRAPHIC_REGION = 'Helgeland' THEN 1 ELSE 0 END) as helgeland_aquaculture,
                        (SUM(CASE WHEN GEOGRAPHIC_REGION = 'Helgeland' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as percentage
                    FROM CUSTOMERS 
                    WHERE INDUSTRY_SECTOR = 'Aquaculture'
                """,
                'expected_min_percentage': 40.0,
                'description': 'Aquaculture should be concentrated in Helgeland region'
            },
            {
                'name': 'tech_in_ostlandet_trondelag',
                'query': """
                    SELECT 
                        COUNT(*) as total_tech,
                        SUM(CASE WHEN GEOGRAPHIC_REGION IN ('Østlandet', 'Trøndelag') THEN 1 ELSE 0 END) as tech_regions,
                        (SUM(CASE WHEN GEOGRAPHIC_REGION IN ('Østlandet', 'Trøndelag') THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as percentage
                    FROM CUSTOMERS 
                    WHERE INDUSTRY_SECTOR = 'Technology Services'
                """,
                'expected_min_percentage': 35.0,
                'description': 'Technology should be concentrated in Østlandet and Trøndelag'
            },
            {
                'name': 'date_range_coverage',
                'query': f"""
                    SELECT 
                        MIN(ORIGINATION_DATE) as min_date,
                        MAX(ORIGINATION_DATE) as max_date,
                        DATEDIFF('month', MIN(ORIGINATION_DATE), MAX(ORIGINATION_DATE)) as months_covered
                    FROM LOANS
                """,
                'expected_min_months': self.config.get_config('HISTORY_MONTHS') * 0.8,  # 80% of expected
                'description': 'Loans should cover the full historical period'
            }
        ]
        
        results = {
            'passed': True,
            'details': {}
        }
        
        for check in distribution_checks:
            try:
                result = self.session.sql(check['query']).collect()
                row = result[0] if result else {}
                
                if 'percentage' in check:
                    # Percentage-based check
                    actual_percentage = float(row.get('PERCENTAGE', 0))
                    expected_min = check['expected_min_percentage']
                    passed = actual_percentage >= expected_min
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'actual_percentage': actual_percentage,
                        'expected_min': expected_min,
                        'passed': passed
                    }
                    
                elif 'expected_min_months' in check:
                    # Months coverage check
                    actual_months = int(row.get('MONTHS_COVERED', 0))
                    expected_min = check['expected_min_months']
                    passed = actual_months >= expected_min
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'actual_months': actual_months,
                        'expected_min': expected_min,
                        'min_date': str(row.get('MIN_DATE', '')),
                        'max_date': str(row.get('MAX_DATE', '')),
                        'passed': passed
                    }
                
                if not passed:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][check['name']] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def validate_green_lending(self) -> Dict[str, Any]:
        """Validate green lending portfolio characteristics"""
        green_checks = [
            {
                'name': 'green_portfolio_percentage',
                'query': """
                    SELECT 
                        COUNT(*) as total_loans,
                        SUM(CASE WHEN GREEN_BOND_FRAMEWORK_TAG THEN 1 ELSE 0 END) as green_loans,
                        (SUM(CASE WHEN GREEN_BOND_FRAMEWORK_TAG THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as green_percentage
                    FROM LOANS
                """,
                'expected_min': 15.0,
                'expected_max': 25.0,
                'description': '15-25% of loans should be green bonds'
            },
            {
                'name': 'green_categories_coverage',
                'query': """
                    SELECT COUNT(DISTINCT GREEN_PROJECT_CATEGORY) as category_count
                    FROM LOANS 
                    WHERE GREEN_BOND_FRAMEWORK_TAG = TRUE
                """,
                'expected_min': 3,
                'description': 'Green loans should cover multiple project categories'
            }
        ]
        
        results = {
            'passed': True,
            'details': {}
        }
        
        for check in green_checks:
            try:
                result = self.session.sql(check['query']).collect()
                row = result[0] if result else {}
                
                if 'green_percentage' in check['name']:
                    percentage = float(row.get('GREEN_PERCENTAGE', 0))
                    passed = check['expected_min'] <= percentage <= check['expected_max']
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'actual_percentage': percentage,
                        'expected_range': f"{check['expected_min']}-{check['expected_max']}%",
                        'passed': passed
                    }
                    
                elif 'category_count' in check['name']:
                    count = int(row.get('CATEGORY_COUNT', 0))
                    passed = count >= check['expected_min']
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'actual_count': count,
                        'expected_min': check['expected_min'],
                        'passed': passed
                    }
                
                if not passed:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][check['name']] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def validate_document_corpus(self) -> Dict[str, Any]:
        """Validate document generation and content coverage"""
        doc_checks = [
            {
                'name': 'documents_by_scenario',
                'query': """
                    SELECT 
                        SCENARIO,
                        COUNT(*) as doc_count
                    FROM DOCUMENTS 
                    GROUP BY SCENARIO
                """,
                'expected_min_per_scenario': 35,
                'expected_max_per_scenario': 50,
                'description': 'Each scenario should have 35-50 documents'
            },
            {
                'name': 'answerable_phrases_coverage',
                'queries': [
                    ("algae bloom coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%algae bloom%'"),
                    ("ISA regulation coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%ISA%'"),
                    ("sea lice coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%sea lice%'"),
                    ("forbearance coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%forbearance%'"),
                    ("LTV breach coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%LTV%'"),
                    ("green bond coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%green bond%'"),
                    ("CO2 reduction coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%CO2%'"),
                    ("SMB initiative coverage", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE CONTENT_MD ILIKE '%SMB%'")
                ],
                'expected_min_each': 1,
                'description': 'Key answerable phrases must exist in document corpus'
            }
        ]
        
        results = {
            'passed': True,
            'details': {}
        }
        
        for check in doc_checks:
            try:
                if check['name'] == 'documents_by_scenario':
                    result = self.session.sql(check['query']).collect()
                    
                    scenario_results = {}
                    overall_passed = True
                    
                    for row in result:
                        scenario = row['SCENARIO']
                        count = row['DOC_COUNT']
                        passed = check['expected_min_per_scenario'] <= count <= check['expected_max_per_scenario']
                        
                        scenario_results[scenario] = {
                            'count': count,
                            'expected_range': f"{check['expected_min_per_scenario']}-{check['expected_max_per_scenario']}",
                            'passed': passed
                        }
                        
                        if not passed:
                            overall_passed = False
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'scenarios': scenario_results,
                        'passed': overall_passed
                    }
                    
                elif check['name'] == 'answerable_phrases_coverage':
                    phrase_results = {}
                    overall_passed = True
                    
                    for phrase_name, query in check['queries']:
                        result = self.session.sql(query).collect()
                        count = result[0]['CNT'] if result else 0
                        passed = count >= check['expected_min_each']
                        
                        phrase_results[phrase_name] = {
                            'count': count,
                            'expected_min': check['expected_min_each'],
                            'passed': passed
                        }
                        
                        if not passed:
                            overall_passed = False
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'phrases': phrase_results,
                        'passed': overall_passed
                    }
                
                if not results['details'][check['name']]['passed']:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][check['name']] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def validate_search_services(self) -> Dict[str, Any]:
        """Validate Cortex Search services functionality"""
        # Import here to avoid circular dependency
        from .search_services import SearchServiceManager
        
        search_manager = SearchServiceManager(self.config)
        
        results = {
            'passed': True,
            'details': {}
        }
        
        try:
            # Test service status
            service_status = search_manager.get_service_status()
            
            for service_name, status in service_status.items():
                passed = status == "EXISTS"
                
                results['details'][f"{service_name}_status"] = {
                    'status': status,
                    'passed': passed
                }
                
                if not passed:
                    results['passed'] = False
            
            # Test search functionality
            search_tests = search_manager.test_all_services()
            
            for service_name, test_passed in search_tests.items():
                results['details'][f"{service_name}_search_test"] = {
                    'description': f'Search functionality test for {service_name}',
                    'passed': test_passed
                }
                
                if not test_passed:
                    results['passed'] = False
                    
        except Exception as e:
            results['details']['search_services_error'] = {
                'error': str(e),
                'passed': False
            }
            results['passed'] = False
        
        return results
    
    def validate_semantic_model(self) -> Dict[str, Any]:
        """Validate semantic model and views"""
        # Import here to avoid circular dependency
        from .semantic_model import SemanticModelManager
        
        semantic_manager = SemanticModelManager(self.config)
        
        try:
            validation_results = semantic_manager.validate_semantic_model()
            
            results = {
                'passed': all(validation_results.values()),
                'details': validation_results
            }
            
        except Exception as e:
            results = {
                'passed': False,
                'details': {'error': str(e)}
            }
        
        return results
    
    def validate_agent_readiness(self) -> Dict[str, Any]:
        """Validate agent tool readiness"""
        agent_checks = [
            {
                'name': 'cortex_analyst_data',
                'query': "SELECT COUNT(*) as cnt FROM SNOWBANK_DEMO_SV",
                'expected_min': 1000,
                'description': 'Semantic view should have sufficient data for Cortex Analyst'
            },
            {
                'name': 'search_services_content',
                'queries': [
                    ("policy_content", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE DOC_TYPE = 'POLICY'"),
                    ("crm_news_content", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE DOC_TYPE IN ('CRM_NOTE','NEWS')"),
                    ("compliance_content", "SELECT COUNT(*) as cnt FROM DOCUMENTS WHERE DOC_TYPE IN ('ANNUAL_REPORT','LOAN_DOC','THIRD_PARTY')")
                ],
                'expected_min_each': 5,
                'description': 'Each search service should have sufficient content'
            }
        ]
        
        results = {
            'passed': True,
            'details': {}
        }
        
        for check in agent_checks:
            try:
                if 'queries' in check:
                    # Multiple queries check
                    content_results = {}
                    overall_passed = True
                    
                    for content_name, query in check['queries']:
                        result = self.session.sql(query).collect()
                        count = result[0]['CNT'] if result else 0
                        passed = count >= check['expected_min_each']
                        
                        content_results[content_name] = {
                            'count': count,
                            'expected_min': check['expected_min_each'],
                            'passed': passed
                        }
                        
                        if not passed:
                            overall_passed = False
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'content': content_results,
                        'passed': overall_passed
                    }
                    
                else:
                    # Single query check
                    result = self.session.sql(check['query']).collect()
                    count = result[0]['CNT'] if result else 0
                    passed = count >= check['expected_min']
                    
                    results['details'][check['name']] = {
                        'description': check['description'],
                        'count': count,
                        'expected_min': check['expected_min'],
                        'passed': passed
                    }
                
                if not results['details'][check['name']]['passed']:
                    results['passed'] = False
                    
            except Exception as e:
                results['details'][check['name']] = {
                    'error': str(e),
                    'passed': False
                }
                results['passed'] = False
        
        return results
    
    def generate_validation_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate a human-readable validation report"""
        report = []
        report.append("=" * 80)
        report.append("SNOWBANK INTELLIGENCE DEMO - VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {validation_results['timestamp']}")
        report.append(f"Overall Status: {'✅ PASSED' if validation_results['success'] else '❌ FAILED'}")
        report.append("")
        
        for category, results in validation_results['checks'].items():
            status = "✅ PASSED" if results.get('passed', False) else "❌ FAILED"
            report.append(f"{category.upper().replace('_', ' ')}: {status}")
            
            if 'error' in results:
                report.append(f"  Error: {results['error']}")
            elif 'details' in results:
                # Add specific details based on category
                self._add_category_details(report, category, results['details'])
            
            report.append("")
        
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def _add_category_details(self, report: List[str], category: str, details: Dict[str, Any]) -> None:
        """Add category-specific details to the report"""
        if category == 'data_volumes':
            for table, info in details.items():
                if 'passed' in info:
                    status = "✅" if info['passed'] else "❌"
                    report.append(f"  {table}: {status} {info.get('actual', 'N/A')} (expected: {info.get('range', 'N/A')})")
        
        elif category == 'search_services':
            for service, info in details.items():
                if 'passed' in info:
                    status = "✅" if info['passed'] else "❌"
                    report.append(f"  {service}: {status}")
        
        # Add more category-specific formatting as needed
