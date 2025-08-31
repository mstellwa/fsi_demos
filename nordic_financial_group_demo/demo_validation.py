#!/usr/bin/env python3
"""
Demo Validation Script
Tests key demo scenarios and provides sample queries for Snowdrift Financials agents.
"""

import logging
import sys
import json
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from setup import SnowdriftSetup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DemoValidator:
    def __init__(self, connection_name: str):
        self.connection_name = connection_name
        self.session = None
        self.demo_data = {}
        
    def connect(self):
        """Establish Snowflake connection"""
        setup = SnowdriftSetup(connection_name=self.connection_name)
        self.session = setup.create_session()
        self.session.sql("USE DATABASE SNOWDRIFT_FINANCIALS").collect()
        self.session.sql("USE SCHEMA INSURANCE").collect()
        
    def disconnect(self):
        """Close Snowflake connection"""
        if self.session:
            self.session.close()
    
    def gather_demo_samples(self):
        """Gather sample data for demo scenarios"""
        logger.info("🎯 Gathering demo sample data...")
        
        # Sample Claims with various characteristics
        claims_query = """
        SELECT 
            c.CLAIM_ID,
            c.POLICY_ID,
            c.DESCRIPTION,
            c.CLAIM_AMOUNT,
            c.STATUS,
            c.MUNICIPALITY,
            p.POLICY_TYPE,
            g.FLOOD_RISK_SCORE
        FROM CLAIMS c
        JOIN POLICIES p ON c.POLICY_ID = p.POLICY_ID
        JOIN GEO_RISK_SCORES g ON c.MUNICIPALITY = g.MUNICIPALITY
        WHERE c.CLAIM_AMOUNT > 50000  -- Higher value claims for demo impact
        ORDER BY c.CLAIM_AMOUNT DESC
        LIMIT 10
        """
        
        claims_result = self.session.sql(claims_query).collect()
        self.demo_data['sample_claims'] = [
            {
                'claim_id': row['CLAIM_ID'],
                'policy_id': row['POLICY_ID'], 
                'description': row['DESCRIPTION'],
                'amount': row['CLAIM_AMOUNT'],
                'status': row['STATUS'],
                'municipality': row['MUNICIPALITY'],
                'policy_type': row['POLICY_TYPE'],
                'flood_risk': row['FLOOD_RISK_SCORE']
            }
            for row in claims_result[:5]  # Top 5 for demo
        ]
        
        # Sample municipalities with different risk levels
        risk_query = """
        SELECT 
            g.MUNICIPALITY,
            g.FLOOD_RISK_SCORE,
            COUNT(DISTINCT p.POLICY_ID) as policy_count,
            COUNT(DISTINCT c.CLAIM_ID) as claim_count,
            AVG(c.CLAIM_AMOUNT) as avg_claim_amount
        FROM GEO_RISK_SCORES g
        LEFT JOIN POLICIES p ON g.MUNICIPALITY = p.MUNICIPALITY
        LEFT JOIN CLAIMS c ON p.POLICY_ID = c.POLICY_ID
        GROUP BY g.MUNICIPALITY, g.FLOOD_RISK_SCORE
        HAVING policy_count > 50  -- Municipalities with sufficient data
        ORDER BY g.FLOOD_RISK_SCORE DESC, policy_count DESC
        LIMIT 15
        """
        
        risk_result = self.session.sql(risk_query).collect()
        self.demo_data['sample_municipalities'] = [
            {
                'municipality': row['MUNICIPALITY'],
                'flood_risk_score': row['FLOOD_RISK_SCORE'],
                'policy_count': row['POLICY_COUNT'],
                'claim_count': row['CLAIM_COUNT'],
                'avg_claim_amount': row['AVG_CLAIM_AMOUNT']
            }
            for row in risk_result
        ]
        
        # Sample companies for underwriting scenarios
        companies_query = """
        SELECT 
            COMPANY_NAME,
            ORGANIZATION_NUMBER,
            MUNICIPALITY,
            BUSINESS_ACTIVITY_DESC,
            EMPLOYEE_COUNT,
            ANNUAL_REVENUE
        FROM BRREG_SNAPSHOT
        WHERE EMPLOYEE_COUNT > 20  -- Larger companies for commercial scenarios
        ORDER BY ANNUAL_REVENUE DESC
        LIMIT 10
        """
        
        companies_result = self.session.sql(companies_query).collect()
        self.demo_data['sample_companies'] = [
            {
                'name': row['COMPANY_NAME'],
                'org_number': row['ORGANIZATION_NUMBER'],
                'municipality': row['MUNICIPALITY'],
                'industry': row['BUSINESS_ACTIVITY_DESC'],
                'employees': row['EMPLOYEE_COUNT'],
                'revenue': row['ANNUAL_REVENUE']
            }
            for row in companies_result[:5]
        ]
        
        logger.info(f"✅ Gathered demo samples: {len(self.demo_data['sample_claims'])} claims, {len(self.demo_data['sample_municipalities'])} municipalities, {len(self.demo_data['sample_companies'])} companies")
    
    def generate_demo_scripts(self):
        """Generate demo scripts with real data"""
        logger.info("📝 Generating demo scripts...")
        
        # Claims Intake Assistant Demo Script
        high_value_claim = self.demo_data['sample_claims'][0]
        flood_risk_municipality = [m for m in self.demo_data['sample_municipalities'] if m['flood_risk_score'] >= 8][0]
        
        claims_demo = {
            "scenario": "Claims Intake Assistant Demo",
            "duration": "10-15 minutes",
            "setup": f"New flood damage claim for commercial property in {high_value_claim['municipality']}",
            "sample_claim_id": high_value_claim['claim_id'],
            "steps": [
                {
                    "step": 1,
                    "title": "Claim Overview",
                    "duration": "3 minutes",
                    "prompt": f"I need to review claim {high_value_claim['claim_id']} that just came in. Can you give me a quick summary of what happened?",
                    "expected_response": [
                        "3-5 sentence incident summary",
                        "Key dates and location", 
                        f"Damage estimate around {high_value_claim['amount']:,} NOK",
                        "Citation to claims documents"
                    ]
                },
                {
                    "step": 2,
                    "title": "Medical Details Extraction",
                    "duration": "4 minutes", 
                    "prompt": f"Extract all medical information from claim {high_value_claim['claim_id']} and present it in a structured table. Include injuries, treatments, and prognosis.",
                    "expected_response": [
                        "Structured table with medical details",
                        "Injury severity assessment",
                        "Treatment recommendations",
                        "Recovery timeline",
                        "Citations to medical reports"
                    ]
                },
                {
                    "step": 3,
                    "title": "Inconsistency Detection",
                    "duration": "5 minutes",
                    "prompt": f"Review all documents for claim {high_value_claim['claim_id']} and identify any inconsistencies in the timeline, witness statements, or reported facts.",
                    "expected_response": [
                        "List of identified discrepancies",
                        "Timeline analysis",
                        "Conflicting statements highlighted",
                        "Recommendations for follow-up investigation",
                        "Document citations for each finding"
                    ]
                },
                {
                    "step": 4,
                    "title": "Investigation Recommendations",
                    "duration": "3 minutes",
                    "prompt": f"Based on your analysis of claim {high_value_claim['claim_id']}, what additional investigation steps would you recommend?",
                    "expected_response": [
                        "Prioritized investigation tasks",
                        "Required documentation",
                        "Expert consultations needed",
                        "Estimated complexity/timeline",
                        "Risk assessment"
                    ]
                }
            ]
        }
        
        # Underwriting Co-Pilot Demo Script
        high_risk_municipality = [m for m in self.demo_data['sample_municipalities'] if m['flood_risk_score'] >= 8][0]
        sample_company = self.demo_data['sample_companies'][0]
        
        underwriting_demo = {
            "scenario": "Underwriting Co-Pilot Demo",
            "duration": "10-15 minutes",
            "setup": f"New commercial property application for {sample_company['name']} in {high_risk_municipality['municipality']}",
            "sample_municipality": high_risk_municipality['municipality'],
            "sample_company": sample_company['name'],
            "steps": [
                {
                    "step": 1,
                    "title": "Location Risk Analysis",
                    "duration": "4 minutes",
                    "prompt": f"I have a new commercial property application in {high_risk_municipality['municipality']}. What can you tell me about the flood risk and historical claims in this area?",
                    "expected_response": [
                        f"Flood risk score interpretation ({high_risk_municipality['flood_risk_score']}/10)",
                        "Historical claims patterns",
                        "Geographic risk factors",
                        "Comparison to other municipalities",
                        "Citation to risk assessments"
                    ]
                },
                {
                    "step": 2,
                    "title": "Prior History Research",
                    "duration": "4 minutes",
                    "prompt": f"Research the claims history for similar commercial properties in {high_risk_municipality['municipality']}. Are there any patterns or concerns I should know about?",
                    "expected_response": [
                        "Claims frequency analysis",
                        "Common loss types",
                        "Seasonal patterns",
                        "Property type risk profiles",
                        "Supporting data tables"
                    ]
                },
                {
                    "step": 3,
                    "title": "Market Intelligence",
                    "duration": "4 minutes",
                    "prompt": f"Find any recent market analysis or environmental reports that might affect underwriting decisions for {high_risk_municipality['municipality']}.",
                    "expected_response": [
                        "Market condition summaries",
                        "Environmental risk updates",
                        "Regulatory changes",
                        "Climate trend analysis",
                        "Citations to research documents"
                    ]
                },
                {
                    "step": 4,
                    "title": "Underwriting Recommendation",
                    "duration": "3 minutes",
                    "prompt": f"Based on all available information, provide your underwriting recommendation for {sample_company['name']} in {high_risk_municipality['municipality']}, including pricing, coverage considerations, and any special conditions.",
                    "expected_response": [
                        "Risk rating (High/Medium/Low)",
                        "Recommended premium adjustment", 
                        "Coverage limitations",
                        "Special conditions/endorsements",
                        "Supporting rationale with citations"
                    ]
                }
            ]
        }
        
        self.demo_data['claims_demo'] = claims_demo
        self.demo_data['underwriting_demo'] = underwriting_demo
        
        logger.info("✅ Demo scripts generated with real data references")
    
    def create_quick_validation_queries(self):
        """Create quick validation queries for agent testing"""
        logger.info("🔬 Creating validation queries...")
        
        sample_claim = self.demo_data['sample_claims'][0]
        high_risk_area = [m for m in self.demo_data['sample_municipalities'] if m['flood_risk_score'] >= 8][0]
        
        validation_queries = {
            "claims_intake_quick_tests": [
                f"Summarize claim {sample_claim['claim_id']} in 3 sentences",
                f"What is the status and claim amount for {sample_claim['claim_id']}?",
                "Show me the top 5 highest value claims from the last month",
                f"Find all claims in {sample_claim['municipality']} and their total value",
                "List claims that might need medical review based on their descriptions"
            ],
            "underwriting_quick_tests": [
                f"What is the flood risk score for {high_risk_area['municipality']}?",
                f"Compare claims history between {high_risk_area['municipality']} and Oslo",
                "Show me municipalities with flood risk scores above 7",
                f"How many policies do we have in {high_risk_area['municipality']}?",
                "Find areas with the highest average claim amounts"
            ],
            "semantic_view_tests": [
                "What is our total premium income?",
                "Show me the loss ratio by municipality",
                "Which policy types have the highest claim frequency?",
                "What are the top 5 municipalities by policy count?",
                "Show me average claim amounts by flood risk category"
            ]
        }
        
        self.demo_data['validation_queries'] = validation_queries
        logger.info("✅ Validation queries created")
    
    def save_demo_package(self):
        """Save complete demo package to file"""
        logger.info("💾 Saving demo package...")
        
        demo_package = {
            "metadata": {
                "title": "Snowdrift Financials Demo Package",
                "description": "Complete demo scripts and validation queries for Insurance agents",
                "generated_for_connection": self.connection_name,
                "total_claims": len(self.demo_data['sample_claims']),
                "total_municipalities": len(self.demo_data['sample_municipalities']),
                "total_companies": len(self.demo_data['sample_companies'])
            },
            "infrastructure_summary": {
                "semantic_view": "INSURANCE_ANALYTICS.NORWEGIAN_INSURANCE_SEMANTIC_VIEW",
                "search_services": ["CLAIMS_SEARCH_SERVICE", "UNDERWRITING_SEARCH_SERVICE"],
                "document_counts": {
                    "claims_documents": 150,
                    "underwriting_documents": 120
                }
            },
            "sample_data": self.demo_data['sample_claims'][:3],  # Top 3 for reference
            "demo_scripts": {
                "claims_intake": self.demo_data['claims_demo'],
                "underwriting": self.demo_data['underwriting_demo']
            },
            "validation_queries": self.demo_data['validation_queries'],
            "recommended_municipalities": [
                m for m in self.demo_data['sample_municipalities'][:5]
            ]
        }
        
        with open("DEMO_PACKAGE.json", "w") as f:
            json.dump(demo_package, f, indent=2, default=str)
        
        logger.info("✅ Demo package saved to DEMO_PACKAGE.json")
    
    def run_validation(self):
        """Run complete demo validation"""
        logger.info("🚀 Starting Demo Validation...")
        
        try:
            self.connect()
            self.gather_demo_samples()
            self.generate_demo_scripts()
            self.create_quick_validation_queries()
            self.save_demo_package()
            
            print("\n" + "="*70)
            print("🎪 DEMO VALIDATION COMPLETE")
            print("="*70)
            
            # Print demo summary
            print(f"\n📊 DEMO DATA SUMMARY:")
            print(f"   • Sample Claims: {len(self.demo_data['sample_claims'])}")
            print(f"   • Sample Municipalities: {len(self.demo_data['sample_municipalities'])}")
            print(f"   • Sample Companies: {len(self.demo_data['sample_companies'])}")
            
            print(f"\n🎯 FEATURED DEMO SCENARIOS:")
            print(f"   • Claims Intake: Claim {self.demo_data['sample_claims'][0]['claim_id']} ({self.demo_data['sample_claims'][0]['amount']:,} NOK)")
            print(f"   • Underwriting: {[m for m in self.demo_data['sample_municipalities'] if m['flood_risk_score'] >= 8][0]['municipality']} (Risk Score {[m for m in self.demo_data['sample_municipalities'] if m['flood_risk_score'] >= 8][0]['flood_risk_score']}/10)")
            
            print(f"\n📝 QUICK TEST QUERIES:")
            print(f"   • Claims: {len(self.demo_data['validation_queries']['claims_intake_quick_tests'])} validation queries")
            print(f"   • Underwriting: {len(self.demo_data['validation_queries']['underwriting_quick_tests'])} validation queries") 
            print(f"   • Semantic View: {len(self.demo_data['validation_queries']['semantic_view_tests'])} validation queries")
            
            print(f"\n🎉 READY FOR DEMO!")
            print(f"📖 Detailed scripts saved in DEMO_PACKAGE.json")
            print(f"🎪 Configure agents in Snowsight and use the generated demo scripts")
            
            return True
            
        except Exception as e:
            logger.error(f"Demo validation failed: {str(e)}")
            return False
        finally:
            self.disconnect()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo Validation for Snowdrift Financials")
    parser.add_argument(
        "--connection", 
        default="sfseeurope-mstellwall-aws-us-west3",
        help="Snowflake connection name"
    )
    
    args = parser.parse_args()
    
    validator = DemoValidator(args.connection)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
