#!/usr/bin/env python3
"""
SAM Snowsight Intelligence Demo - Complete Synthetic Data Generation
Unified script that generates all realistic unstructured documents for the complete demo
"""

import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, lit
from snowflake.cortex import complete
import json
import os
from datetime import datetime

def create_snowpark_session():
    """Create Snowpark session using connections.toml"""
    try:
        return snowpark.Session.builder.config("connection_name", "sfseeurope-mstellwall-aws-us-west3").create()
    except:
        # Fallback to environment variables if connections.toml doesn't work
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

def render_prompt_template(template_text, context):
    """Replace placeholders in template with context values"""
    for key, value in context.items():
        placeholder = "{" + str(key) + "}"
        template_text = template_text.replace(placeholder, str(value))
    return template_text

def render_all_prompts(session):
    """Render all prompts and store in RENDERED_PROMPTS table for bulk generation"""
    
    print("📊 Reading prompt inputs and templates...")
    
    # Read prompt inputs and join with templates
    prompt_data = session.sql("""
        SELECT 
            pi.RUN_ID,
            pi.PROMPT_ID,
            pi.COMPANY_NAME,
            pi.DOC_DATE,
            pi.QUARTER,
            pi.ATTENDEES,
            pi.TOPICS,
            pi.EVENT_ANCHOR,
            pi.DOC_VARIANT,
            pi.OUTPUT_FORMAT,
            pi.TARGET_COLLECTION,
            pi.MODEL_NAME,
            pl.PROMPT_TYPE,
            pl.TEMPLATE_TEXT,
            pl.DEFAULT_TONE,
            pl.MIN_TOKENS,
            pl.MAX_TOKENS,
            pl.STYLE_GUIDE
        FROM PROMPT_INPUTS pi
        JOIN PROMPT_LIBRARY pl ON pi.PROMPT_ID = pl.PROMPT_ID
        WHERE pl.IS_ACTIVE = TRUE
        ORDER BY pi.RUN_ID
    """).collect()
    
    print(f"📝 Found {len(prompt_data)} prompts to render...")
    
    rendered_prompts = []
    
    for i, row in enumerate(prompt_data):
        print(f"   📝 Rendering {row.PROMPT_TYPE} for {row.COMPANY_NAME or 'Client'} ({i+1}/{len(prompt_data)})...")
        
        # Build context for template rendering
        year = row.DOC_DATE.strftime('%Y') if row.DOC_DATE else '2024'
        context = {
            'COMPANY_NAME': row.COMPANY_NAME or '',
            'DOC_DATE': row.DOC_DATE.strftime('%B %d, %Y') if row.DOC_DATE else '',
            'QUARTER': row.QUARTER or '',
            'ATTENDEES': row.ATTENDEES or '',
            'TOPICS': row.TOPICS or '',
            'EVENT_ANCHOR': row.EVENT_ANCHOR or '',
            'DOC_VARIANT': row.DOC_VARIANT or '',
            'CLIENT_NAME': row.COMPANY_NAME if row.TARGET_COLLECTION == 'CLIENT_MEETING_ARCHIVE' else '',
            'MEETING_CONTEXT': row.DOC_VARIANT or '',
            'PORTFOLIO_FOCUS': row.TOPICS or '',
            'TOP_HOLDINGS': row.TOPICS or '',
            'MEETING_TYPE': row.DOC_VARIANT or '',
            'FOCUS_AREAS': row.TOPICS or '',
            'YEAR': year,
            'COMPETITOR': 'Amazon' if 'Arkadia' in str(row.COMPANY_NAME) else 'established players',
            'BUSINESS_CONTEXT': get_business_context(row.COMPANY_NAME, row.DOC_DATE)
        }
        
        # Render the prompt template
        rendered_prompt = render_prompt_template(row.TEMPLATE_TEXT, context)
        
        # Create file metadata
        company_part = row.COMPANY_NAME.lower().replace(' ', '_') if row.COMPANY_NAME else 'client'
        doc_id = f"{company_part}_{row.PROMPT_TYPE.lower()}_{row.DOC_DATE.strftime('%Y%m%d')}"
        if row.RUN_ID:
            doc_id += f"_{row.RUN_ID.split('_')[-1]}"
        filename = f"{doc_id}.txt"
        
        # Determine document classification
        doc_type = classify_document_type(row.PROMPT_TYPE, row.TARGET_COLLECTION)
        
        # Create rendered prompt record
        prompt_record = {
            'prompt_render_id': f"render_{doc_id}",
            'doc_id': doc_id,
            'filename': filename,
            'company_name': row.COMPANY_NAME or '',
            'document_type': doc_type,
            'doc_date': row.DOC_DATE,
            'quarter': row.QUARTER or '',
            'author': get_author_for_type(row.PROMPT_TYPE),
            'tags': get_tags_for_document(row.PROMPT_TYPE, row.TOPICS),
            'source_prompt_id': row.PROMPT_ID,
            'model_name': row.MODEL_NAME,
            'full_prompt': rendered_prompt,
            'file_url': f"@SAM_DOCS_STAGE/{filename}"
        }
        
        rendered_prompts.append(prompt_record)
    
    print(f"\\n🎉 Rendered {len(rendered_prompts)} prompts successfully!")
    return rendered_prompts

def get_business_context(company_name, doc_date):
    """Generate business context based on company and time period"""
    if not company_name:
        return "in a dynamic market environment"
        
    contexts = {
        'Tempus AI': 'pioneering medical AI with proprietary genomics datasets',
        'NorthernCell Energy': 'developing next-generation solid-state battery technology', 
        'Arkadia Commerce': 'building a comprehensive e-commerce platform to challenge Amazon',
        'Voltaic Dynamics': 'providing critical supply chain components for the EV revolution',
        'Helios Semiconductors': 'designing specialized AI chips for machine learning workloads',
        'TerraLink Logistics': 'optimizing global supply chain operations through technology'
    }
    
    year = doc_date.year if doc_date else 2024
    base_context = contexts.get(company_name, 'operating in a competitive technology market')
    
    if year <= 2020:
        return f"{base_context} during the early growth phase"
    elif year <= 2022:
        return f"{base_context} amid pandemic-driven market changes"
    else:
        return f"{base_context} in an increasingly competitive landscape"

def classify_document_type(prompt_type, target_collection):
    """Classify documents into standardized types for search services"""
    type_mapping = {
        # Research service document types
        'ResearchNote': 'ResearchNote',
        'EarningsTranscript': 'EarningsTranscript', 
        'FrameworkScaffold': 'FrameworkAnalysis',
        'ExpertNetworkInterview': 'ExpertNetworkInterview',
        'PatentAnalysis': 'PatentAnalysis',
        
        # Corporate memory service document types
        'HistoricalThesis': 'HistoricalThesis',
        'MeetingNotes': 'MeetingNotes',
        'InternalDebateSummary': 'InternalDebateSummary',
        
        # Client service document types  
        'ClientMeetingNotes': 'ClientMeetingNotes',
        
        # Marketing content service document types
        'MarketingContent': 'MarketingContent'
    }
    return type_mapping.get(prompt_type, 'Document')

def get_author_for_type(prompt_type):
    """Get appropriate author based on document type"""
    authors = {
        # Research team documents
        'ResearchNote': 'SAM Research Team',
        'FrameworkScaffold': 'SAM Research Team',
        'ExpertNetworkInterview': 'External Expert Network',
        'PatentAnalysis': 'SAM Research Team',
        
        # Company documents
        'EarningsTranscript': 'Company Management',
        
        # Investment committee documents
        'HistoricalThesis': 'SAM Investment Committee',
        'InternalDebateSummary': 'SAM Investment Committee',
        
        # Portfolio management documents  
        'MeetingNotes': 'SAM Portfolio Management',
        
        # Client relations documents
        'ClientMeetingNotes': 'SAM Client Relations',
        
        # Marketing documents
        'MarketingContent': 'SAM Marketing Team'
    }
    return authors.get(prompt_type, 'SAM Team')

def get_tags_for_document(prompt_type, topics):
    """Generate relevant tags for document categorization"""
    base_tags = []
    
    if prompt_type == 'ResearchNote':
        base_tags = ['Investment Thesis', 'Research', 'Analysis']
    elif prompt_type == 'FrameworkScaffold':
        base_tags = ['10-Question Framework', 'Research', 'Analysis']
    elif prompt_type == 'ExpertNetworkInterview':
        base_tags = ['Expert Interview', 'External Research', 'Industry Insights']
    elif prompt_type == 'PatentAnalysis':
        base_tags = ['Patent Analysis', 'Technology', 'Competitive Moat']
    elif prompt_type == 'EarningsTranscript':
        base_tags = ['Earnings', 'Management Commentary', 'Q&A']
    elif prompt_type == 'HistoricalThesis':
        base_tags = ['Historical', 'Thesis Evolution', 'Corporate Memory']
    elif prompt_type == 'MeetingNotes':
        base_tags = ['Management Meeting', 'Internal Notes']
    elif prompt_type == 'InternalDebateSummary':
        base_tags = ['Internal Debate', 'Investment Committee', 'Decision Making']
    elif prompt_type == 'ClientMeetingNotes':
        base_tags = ['Client Relations', 'Meeting Minutes']
    elif prompt_type == 'MarketingContent':
        base_tags = ['Marketing', 'SAM Philosophy', 'Communications']
    
    # Add topic-based tags
    if topics:
        if 'risk' in topics.lower():
            base_tags.append('Risk Analysis')
        if 'competition' in topics.lower() or 'amazon' in topics.lower():
            base_tags.append('Competitive Analysis')
        if 'technology' in topics.lower() or 'ai' in topics.lower():
            base_tags.append('Technology')
        if 'supply chain' in topics.lower():
            base_tags.append('Supply Chain')
    
    return base_tags

def store_rendered_prompts_to_table(session, prompts):
    """Store rendered prompts in RENDERED_PROMPTS table for bulk generation"""
    
    print(f"\\n💾 Storing {len(prompts)} rendered prompts to RENDERED_PROMPTS table...")
    
    for i, prompt in enumerate(prompts):
        try:
            # Escape single quotes in content for SQL
            safe_prompt = prompt['full_prompt'].replace("'", "''")
            
            # Handle NULL dates properly
            doc_date_value = f"'{prompt['doc_date'].strftime('%Y-%m-%d')}'" if prompt['doc_date'] else 'NULL'
            
            # Use SELECT with ARRAY_CONSTRUCT for tags
            if prompt['tags']:
                # Build ARRAY_CONSTRUCT parameters with proper quoting
                tag_params = ', '.join([f"'{tag}'" for tag in prompt['tags']])
                tags_construct = f"ARRAY_CONSTRUCT({tag_params})"
            else:
                tags_construct = "ARRAY_CONSTRUCT()"
            
            insert_sql = f"""
            INSERT INTO RENDERED_PROMPTS (
                PROMPT_RENDER_ID, DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, 
                DOC_DATE, QUARTER, AUTHOR, TAGS, SOURCE_PROMPT_ID, MODEL_NAME, FULL_PROMPT
            ) 
            SELECT 
                '{prompt['prompt_render_id']}' as PROMPT_RENDER_ID,
                '{prompt['doc_id']}' as DOC_ID,
                '{prompt['file_url']}' as FILE_URL, 
                '{prompt['company_name']}' as COMPANY_NAME,
                '{prompt['document_type']}' as DOCUMENT_TYPE,
                {doc_date_value} as DOC_DATE,
                '{prompt['quarter']}' as QUARTER,
                '{prompt['author']}' as AUTHOR,
                {tags_construct} as TAGS,
                '{prompt['source_prompt_id']}' as SOURCE_PROMPT_ID,
                '{prompt['model_name']}' as MODEL_NAME,
                '{safe_prompt}' as FULL_PROMPT
            """
            
            session.sql(insert_sql).collect()
            
            if (i + 1) % 5 == 0:
                print(f"   ✅ Stored {i + 1}/{len(prompts)} prompts...")
                
        except Exception as e:
            print(f"   ❌ Error storing prompt {prompt['prompt_render_id']}: {str(e)}")
            continue
    
    print(f"✅ Successfully stored rendered prompts to table!")

def bulk_generate_documents_with_sql(session):
    """Generate all documents using SQL bulk operation with AI_COMPLETE"""
    
    print("\\n🚀 Starting bulk document generation with AI_COMPLETE...")
    
    try:
        # Get distinct models to work around string literal requirement
        models = session.sql("SELECT DISTINCT MODEL_NAME FROM RENDERED_PROMPTS").collect()
        
        print(f"   📝 Found {len(models)} distinct models to process...")
        total_generated = 0
        
        for model_row in models:
            model_name = model_row[0]
            print(f"   🤖 Processing model: {model_name}")
            
            # Bulk insert for this specific model (string literal)
            bulk_sql = f"""
            INSERT INTO DOCUMENTS (
                DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, 
                QUARTER, AUTHOR, TAGS, SOURCE_PROMPT_ID, MODEL_NAME, CONTENT
            )
            SELECT 
                DOC_ID,
                FILE_URL,
                COMPANY_NAME,
                DOCUMENT_TYPE,
                DOC_DATE,
                QUARTER,
                AUTHOR,
                TAGS,
                SOURCE_PROMPT_ID,
                MODEL_NAME,
                SNOWFLAKE.CORTEX.COMPLETE('{model_name}', FULL_PROMPT) AS CONTENT
            FROM RENDERED_PROMPTS
            WHERE MODEL_NAME = '{model_name}'
            ORDER BY PROMPT_RENDER_ID
            """
            
            result = session.sql(bulk_sql).collect()
            model_count = len(result) if result else 0
            total_generated += model_count
            print(f"   ✅ Generated {model_count} documents for {model_name}")
        
        print(f"   🎉 Successfully generated {total_generated} documents using bulk SQL!")
        return total_generated
        
    except Exception as e:
        print(f"   ❌ Error in bulk generation: {str(e)}")
        print("   🔄 Falling back to individual generation...")
        
        # Fallback: Generate documents one by one using SQL to avoid array issues
        prompts = session.sql("SELECT PROMPT_RENDER_ID, MODEL_NAME, FULL_PROMPT FROM RENDERED_PROMPTS ORDER BY PROMPT_RENDER_ID").collect()
        
        success_count = 0
        for i, prompt in enumerate(prompts):
            try:
                print(f"   📝 Generating document {i+1}/{len(prompts)}...")
                
                # Generate content
                from snowflake.cortex import complete
                content = complete(model=prompt.MODEL_NAME, prompt=prompt.FULL_PROMPT)
                
                # Escape single quotes in content
                safe_content = content.replace("'", "''")
                
                # Use SQL to copy from RENDERED_PROMPTS and add content, letting SQL handle arrays
                insert_sql = f"""
                INSERT INTO DOCUMENTS (
                    DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE, 
                    QUARTER, AUTHOR, TAGS, SOURCE_PROMPT_ID, MODEL_NAME, CONTENT
                ) 
                SELECT 
                    DOC_ID, FILE_URL, COMPANY_NAME, DOCUMENT_TYPE, DOC_DATE,
                    QUARTER, AUTHOR, TAGS, SOURCE_PROMPT_ID, MODEL_NAME,
                    '{safe_content}' as CONTENT
                FROM RENDERED_PROMPTS
                WHERE PROMPT_RENDER_ID = '{prompt.PROMPT_RENDER_ID}'
                """
                
                session.sql(insert_sql).collect()
                success_count += 1
                
            except Exception as e:
                print(f"   ❌ Error generating document {i+1}: {str(e)}")
                continue
        
        print(f"   ✅ Fallback generation completed: {success_count} documents")
        return success_count

def verify_complete_setup(session):
    """Verify all components are properly set up"""
    
    print("\\n🔍 Verifying complete setup...")
    
    verification_queries = [
        ("Companies in financial data", "SELECT COUNT(DISTINCT COMPANY_NAME) FROM COMPANY_FINANCIALS"),
        ("Client records", "SELECT COUNT(*) FROM CLIENT_CRM"),
        ("Portfolio holdings", "SELECT COUNT(*) FROM PORTFOLIO_HOLDINGS_HISTORY"), 
        ("Generated documents", "SELECT COUNT(*) FROM DOCUMENTS"),
        ("Document types", "SELECT COUNT(DISTINCT DOCUMENT_TYPE) FROM DOCUMENTS"),
        ("Prompt templates", "SELECT COUNT(*) FROM PROMPT_LIBRARY WHERE IS_ACTIVE = TRUE"),
        ("Semantic views", "SHOW SEMANTIC VIEWS")
    ]
    
    for description, query in verification_queries:
        try:
            if query.startswith("SHOW"):
                result = session.sql(query).collect()
                count = len(result)
            else:
                result = session.sql(query).collect()
                count = result[0][0] if result else 0
            print(f"   ✅ {description}: {count}")
        except Exception as e:
            print(f"   ❌ {description}: Error - {str(e)}")
    
    # Show document distribution
    print("\\n📊 Document distribution by company:")
    try:
        doc_dist = session.sql("""
            SELECT COMPANY_NAME, DOCUMENT_TYPE, COUNT(*) as count
            FROM DOCUMENTS 
            GROUP BY COMPANY_NAME, DOCUMENT_TYPE
            ORDER BY COMPANY_NAME, DOCUMENT_TYPE
        """).collect()
        
        for row in doc_dist:
            print(f"   • {row[0]}: {row[1]} ({row[2]} docs)")
            
    except Exception as e:
        print(f"   ❌ Error getting document distribution: {str(e)}")

def main():
    """Main execution function"""
    print("🚀 Starting SAM Demo Complete Synthetic Data Generation")
    print("=" * 60)
    
    try:
        # Create session
        session = create_snowpark_session()
        print("✅ Connected to Snowflake")
        
        # Set context
        session.sql("USE DATABASE FSI_DEMOS").collect()
        session.sql("USE SCHEMA SAM_DEMO").collect()
        print("✅ Using FSI_DEMOS.SAM_DEMO")
        
        # Render prompts (fast - no AI calls)
        rendered_prompts = render_all_prompts(session)
        
        if not rendered_prompts:
            print("❌ No prompts were rendered!")
            return
        
        # Store rendered prompts to table
        store_rendered_prompts_to_table(session, rendered_prompts)
        
        # Bulk generate documents using SQL AI_COMPLETE
        doc_count = bulk_generate_documents_with_sql(session)
        
        # Verify setup
        verify_complete_setup(session)
        
        print("\\n🎉 SAM Demo synthetic data generation completed successfully!")
        print("\\nNext steps:")
        print("• Create Cortex Search services over document collections")
        print("• Configure agents in Snowsight Intelligence UI")
        print("• Test demo scenarios")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
        
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
