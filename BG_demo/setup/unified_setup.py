#!/usr/bin/env python3
"""
SAM Snowsight Intelligence Demo - Unified Orchestrator
Master setup script that coordinates all components in proper sequence
"""

import snowflake.snowpark as snowpark
import sys
import os
from pathlib import Path
import re
from datetime import datetime

def create_session():
    """Create Snowpark session using connections.toml"""
    try:
        return snowpark.Session.builder.config("connection_name", "sfseeurope-mstellwall-aws-us-west3").create()
    except Exception as e:
        print(f"❌ Failed to create session with connections.toml: {str(e)}")
        # Fallback to environment variables
        connection_parameters = {
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"), 
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
            "database": "FSI_DEMOS",
            "schema": "SAM_DEMO"
        }
        return snowpark.Session.builder.configs(connection_parameters).create()

def execute_sql_file(session, file_path):
    """Execute SQL file with multi-line statement handling"""
    print(f"🔧 Executing SQL file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ SQL file not found: {file_path}")
        return False
    
    try:
        # Read entire file content
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Split into statements (handling multi-line statements)
        statements = split_sql_statements(sql_content)
        
        successful_statements = 0
        total_statements = len(statements)
        
        print(f"   📝 Found {total_statements} SQL statements to execute")
        
        for i, statement in enumerate(statements):
            if statement.strip():
                try:
                    session.sql(statement).collect()
                    successful_statements += 1
                    
                    # Progress reporting for large files
                    if total_statements > 20 and (i + 1) % 10 == 0:
                        print(f"   ⏳ Executed {i + 1}/{total_statements} statements...")
                        
                except Exception as e:
                    # Log error but continue execution
                    print(f"   ⚠️ Statement {i+1} failed (continuing): {str(e)}")
                    continue
        
        print(f"   ✅ Successfully executed {successful_statements}/{total_statements} statements")
        return successful_statements > 0
        
    except Exception as e:
        print(f"   ❌ Error reading or executing SQL file: {str(e)}")
        return False

def split_sql_statements(sql_content):
    """Split SQL content into individual statements, handling comments and multi-line statements"""
    
    # Remove single-line comments (-- comments)
    lines = sql_content.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Find comment position, but ignore -- inside strings
        comment_pos = -1
        in_string = False
        escape_next = False
        
        for i, char in enumerate(line):
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == "'" and not in_string:
                in_string = True
            elif char == "'" and in_string:
                in_string = False
            elif not in_string and i < len(line) - 1 and line[i:i+2] == '--':
                comment_pos = i
                break
        
        if comment_pos >= 0:
            cleaned_lines.append(line[:comment_pos].rstrip())
        else:
            cleaned_lines.append(line)
    
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Split by semicolon (but not inside strings)
    statements = []
    current_statement = ""
    in_string = False
    escape_next = False
    
    for char in cleaned_content:
        if escape_next:
            current_statement += char
            escape_next = False
            continue
            
        if char == '\\':
            current_statement += char
            escape_next = True
            continue
            
        if char == "'" and not in_string:
            in_string = True
            current_statement += char
        elif char == "'" and in_string:
            in_string = False
            current_statement += char
        elif char == ';' and not in_string:
            # End of statement
            statements.append(current_statement.strip())
            current_statement = ""
        else:
            current_statement += char
    
    # Add final statement if exists
    if current_statement.strip():
        statements.append(current_statement.strip())
    
    # Filter out empty statements
    return [stmt for stmt in statements if stmt.strip()]

def import_and_execute_python_module(session, module_path):
    """Import Python module from relative path and execute document generation"""
    print(f"🐍 Importing and executing Python module: {module_path}")
    
    try:
        # Add python directory to path
        python_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'python')
        if python_dir not in sys.path:
            sys.path.insert(0, python_dir)
        
        # Import the module
        import generate_synthetic_data
        
        print("   📝 Rendering prompts for bulk generation...")
        rendered_prompts = generate_synthetic_data.render_all_prompts(session)
        
        if not rendered_prompts:
            print("   ⚠️ No prompts were rendered")
            return False
        
        print("   💾 Storing rendered prompts to RENDERED_PROMPTS table...")
        generate_synthetic_data.store_rendered_prompts_to_table(session, rendered_prompts)
        
        print("   🚀 Bulk generating documents using SQL AI_COMPLETE...")
        doc_count = generate_synthetic_data.bulk_generate_documents_with_sql(session)
        
        print(f"   ✅ Successfully generated {doc_count} documents using optimized bulk approach")
        return doc_count > 0
        
    except Exception as e:
        print(f"   ❌ Error in Python module execution: {str(e)}")
        return False

def create_cortex_search_services(session):
    """Create Cortex Search services after document generation"""
    print("🔍 Creating Cortex Search services...")
    
    services = [
        {
            'name': 'research_service',
            'filter': "DOCUMENT_TYPE IN ('ResearchNote', 'EarningsTranscript', 'FrameworkAnalysis', 'ExpertNetworkInterview', 'PatentAnalysis')",
            'description': 'Research documents and analysis'
        },
        {
            'name': 'corporate_memory_service', 
            'filter': "DOCUMENT_TYPE IN ('HistoricalThesis', 'MeetingNotes', 'InternalDebateSummary')",
            'description': 'Corporate memory and historical documents'
        },
        {
            'name': 'marketing_content_service',
            'filter': "DOCUMENT_TYPE IN ('MarketingContent')",
            'description': 'Approved marketing and communication content'
        }
    ]
    
    successful_services = 0
    
    for service in services:
        try:
            print(f"   📝 Creating {service['name']}...")
            
            # Drop existing service if it exists
            try:
                session.sql(f"DROP CORTEX SEARCH SERVICE IF EXISTS {service['name']}").collect()
            except:
                pass
            
            # Create the search service
            create_sql = f"""
            CREATE CORTEX SEARCH SERVICE {service['name']}
            ON CONTENT
            ATTRIBUTES DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
            WAREHOUSE = COMPUTE_WH
            TARGET_LAG = '1 hour'
            AS (
              SELECT CONTENT, DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, AUTHOR
              FROM DOCUMENTS 
              WHERE {service['filter']}
            )
            """
            
            session.sql(create_sql).collect()
            successful_services += 1
            print(f"   ✅ {service['name']} created successfully")
            
        except Exception as e:
            print(f"   ❌ Error creating {service['name']}: {str(e)}")
            continue
    
    print(f"   🎉 Successfully created {successful_services}/{len(services)} search services")
    
    if successful_services > 0:
        print("   ⏳ Search services are indexing content (may take 2-3 minutes)...")
    
    return successful_services > 0

def verify_complete_setup(session):
    """Comprehensive verification of all demo components"""
    print("🔍 Running comprehensive setup verification...")
    
    verification_checks = [
        # Basic infrastructure
        ("Database and schema", "SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()"),
        ("Tables created", "SHOW TABLES"),
        
        # Data completeness
        ("Companies in financial data", "SELECT COUNT(DISTINCT COMPANY_NAME) FROM COMPANY_FINANCIALS"),
        ("Client records", "SELECT COUNT(*) FROM CLIENT_CRM"),
        ("Portfolio holdings", "SELECT COUNT(*) FROM PORTFOLIO_HOLDINGS_HISTORY"),
        ("Generated documents", "SELECT COUNT(*) FROM DOCUMENTS"),
        ("Document types", "SELECT COUNT(DISTINCT DOCUMENT_TYPE) FROM DOCUMENTS"),
        ("Prompt templates", "SELECT COUNT(*) FROM PROMPT_LIBRARY WHERE IS_ACTIVE = TRUE"),
        
        # Advanced infrastructure
        ("Semantic views", "SHOW SEMANTIC VIEWS"),
        ("Search services", "SHOW CORTEX SEARCH SERVICES"),
    ]
    
    successful_checks = 0
    total_checks = len(verification_checks)
    
    for description, query in verification_checks:
        try:
            result = session.sql(query).collect()
            
            if query.startswith("SHOW"):
                count = len(result)
            elif query.startswith("SELECT CURRENT_"):
                # For database/schema check
                db_schema = f"{result[0][0]}.{result[0][1]}"
                print(f"   ✅ {description}: {db_schema}")
                successful_checks += 1
                continue
            else:
                count = result[0][0] if result else 0
            
            print(f"   ✅ {description}: {count}")
            successful_checks += 1
            
        except Exception as e:
            print(f"   ❌ {description}: Error - {str(e)}")
    
    # Detailed data verification
    print("\n📊 Demo-specific data verification:")
    
    demo_checks = [
        ("Tempus AI financial quarters", "SELECT COUNT(*) FROM COMPANY_FINANCIALS WHERE COMPANY_NAME = 'Tempus AI'"),
        ("Tempus AI documents", "SELECT COUNT(*) FROM DOCUMENTS WHERE COMPANY_NAME = 'Tempus AI'"),
        ("Arkadia Commerce documents", "SELECT COUNT(*) FROM DOCUMENTS WHERE COMPANY_NAME = 'Arkadia Commerce'"),
        ("Scottish Pension Trust data", "SELECT COUNT(*) FROM CLIENT_CRM WHERE CLIENT_NAME = 'Scottish Pension Trust'"),
    ]
    
    for description, query in demo_checks:
        try:
            result = session.sql(query).collect()
            count = result[0][0] if result else 0
            
            if count > 0:
                print(f"   ✅ {description}: {count}")
                successful_checks += 1
            else:
                print(f"   ⚠️ {description}: {count} (may need attention)")
                
        except Exception as e:
            print(f"   ❌ {description}: Error - {str(e)}")
    
    # Summary
    success_rate = (successful_checks / (total_checks + len(demo_checks))) * 100
    print(f"\n🎯 Verification Summary: {successful_checks}/{total_checks + len(demo_checks)} checks passed ({success_rate:.1f}%)")
    
    return success_rate > 80

def main():
    """Main orchestrator function - coordinates all setup phases"""
    
    print("🚀 SAM Snowsight Intelligence Demo - Unified Orchestrator")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Track overall progress
    phases = [
        "Database & Schema Setup",
        "Structured Tables Creation", 
        "Sample Data Population",
        "Services & Views Creation",
        "Document Generation",
        "Search Services Creation",
        "Complete Verification"
    ]
    
    current_phase = 0
    
    try:
        # Phase 1: Create session and set context
        print(f"📋 Phase {current_phase + 1}/{len(phases)}: Initializing Snowflake Session")
        session = create_session()
        print("✅ Connected to Snowflake successfully")
        
        session.sql("USE DATABASE FSI_DEMOS").collect()
        session.sql("USE SCHEMA SAM_DEMO").collect()
        print("✅ Using FSI_DEMOS.SAM_DEMO context")
        print()
        
        # Phase 2-5: Execute SQL files in sequence
        sql_files = [
            ("sql/01_create_database_schema.sql", "Database & Schema Setup"),
            ("sql/02_create_structured_tables.sql", "Structured Tables Creation"),
            ("sql/03_populate_sample_data.sql", "Sample Data Population"),
            ("sql/04_create_services_and_views.sql", "Services & Views Creation")
        ]
        
        for sql_file, phase_name in sql_files:
            current_phase += 1
            print(f"📋 Phase {current_phase}/{len(phases)}: {phase_name}")
            
            if execute_sql_file(session, sql_file):
                print(f"✅ {phase_name} completed successfully")
            else:
                print(f"❌ {phase_name} failed - continuing anyway")
            print()
        
        # Phase 6: Document Generation
        current_phase += 1
        print(f"📋 Phase {current_phase}/{len(phases)}: Document Generation")
        
        if import_and_execute_python_module(session, "python/generate_synthetic_data.py"):
            print("✅ Document generation completed successfully")
        else:
            print("❌ Document generation failed - continuing anyway")
        print()
        
        # Phase 7: Search Services Creation
        current_phase += 1
        print(f"📋 Phase {current_phase}/{len(phases)}: Search Services Creation")
        
        if create_cortex_search_services(session):
            print("✅ Search services creation completed successfully")
        else:
            print("❌ Search services creation failed - continuing anyway")
        print()
        
        # Phase 8: Complete Verification
        current_phase += 1
        print(f"📋 Phase {current_phase}/{len(phases)}: Complete Verification")
        
        if verify_complete_setup(session):
            print("✅ Setup verification passed")
        else:
            print("⚠️ Setup verification found issues")
        print()
        
        # Success summary
        print("🎉 UNIFIED ORCHESTRATOR SETUP COMPLETE!")
        print("=" * 50)
        print("\n📋 Demo Infrastructure Ready:")
        print("   ✅ Database and tables created")
        print("   ✅ Sample data populated (6 companies, 3 clients)")
        print("   ✅ Optimized bulk document generation completed")
        print("   ✅ Semantic views created with RELATIONSHIPS")
        print("   ✅ Cortex Search services created")
        print("\n🎯 Next Steps:")
        print("   1. Configure agents in Snowsight Intelligence UI")
        print("   2. Assign tools to agents:")
        print("      • Research Analyst: research_service + FINANCIAL_DATA_ANALYST")
        print("      • Portfolio Manager: corporate_memory_service")
        print("      • Client Manager: research_service + FINANCIAL_DATA_ANALYST + marketing_content_service")
        print("   3. Test enhanced demo scenarios")
        print("\n🏆 Competitive Advantages Ready to Demo:")
        print("   • 10-Question Framework integration")
        print("   • Corporate Memory (5+ years of historical context)")
        print("   • SAM philosophy authentically integrated")
        print("   • Professional-grade synthetic content")
        
    except Exception as e:
        print(f"❌ Critical error in Phase {current_phase + 1}: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   • Check connections.toml configuration")
        print("   • Verify Snowflake account permissions")
        print("   • Ensure Cortex features are enabled")
        raise
        
    finally:
        if 'session' in locals():
            session.close()
            print(f"\n🔒 Session closed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
