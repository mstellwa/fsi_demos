"""
Unstructured Data Generation for SAM Demo

This module generates realistic unstructured documents including:
- Broker research reports
- Earnings transcripts and summaries  
- Press releases
- NGO reports and ESG controversies
- Internal engagement notes
- Policy documents and sales templates
"""

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, call_function
from typing import List
import uuid
import random
from datetime import datetime, timedelta
import config

def build_all(session: Session, document_types: List[str], test_mode: bool = False):
    """
    Build all unstructured data for the specified document types.
    
    Args:
        session: Active Snowpark session
        document_types: List of document types to generate
        test_mode: If True, use reduced document counts for faster testing
    """
    print("📝 Starting unstructured data generation...")
    
    # Step 1: Generate prompts for each document type
    print("🎯 Generating content prompts...")
    if test_mode:
        print("🧪 Test mode: Using reduced document counts for faster generation")
    generate_prompts(session, document_types, test_mode)
    
    # Step 2: Generate content using Cortex Complete
    print("🤖 Generating content with LLM...")
    generate_content(session, document_types)
    
    # Step 3: Normalize to corpus tables
    print("📚 Creating normalized corpus tables...")
    create_corpus_tables(session, document_types)
    
    print("✅ Unstructured data generation complete")

def generate_prompts(session: Session, document_types: List[str], test_mode: bool = False):
    """Generate detailed prompts for each document type and store in RAW.GENERATION_PROMPTS."""
    
    # Create prompts table with SecurityID and IssuerID support
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.RAW.GENERATION_PROMPTS (
            PROMPT_ID VARCHAR PRIMARY KEY,
            DOCUMENT_TYPE VARCHAR NOT NULL,
            SecurityID BIGINT,                            -- New: immutable SecurityID
            IssuerID BIGINT,                              -- New: issuer linkage
            TICKER VARCHAR,
            COMPANY_NAME VARCHAR,
            GICS_SECTOR VARCHAR,
            PROMPT_TEXT TEXT NOT NULL,
            MODEL_NAME VARCHAR DEFAULT '{config.MODEL_NAME}',
            CREATED_TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
    """).collect()
    
    # Get securities data for context using new SecurityID model
    # Prioritize real tickers (non-pattern tickers) for better demo quality
    securities = session.sql(f"""
        SELECT 
            ds.SecurityID,
            xref.IdentifierValue as TICKER,
            ds.Description as COMPANY_NAME,
            di.GICS_Sector,
            ds.AssetClass,
            di.CountryOfIncorporation as COUNTRY_OF_DOMICILE,
            di.IssuerID,
            di.LegalName as ISSUER_NAME
        FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY ds
        JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER di ON ds.IssuerID = di.IssuerID
        JOIN {config.DATABASE_NAME}.CURATED.DIM_SECURITY_IDENTIFIER_XREF xref ON ds.SecurityID = xref.SecurityID
        WHERE xref.IdentifierType = 'TICKER' 
        AND xref.IsPrimaryForType = TRUE
        AND ds.AssetClass = 'Equity'
        ORDER BY 
            -- Prioritize major US stocks that are in portfolios and demo scenarios
            CASE 
                WHEN xref.IdentifierValue IN ('AAPL', 'MSFT', 'NVDA', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'CRM', 'ORCL') THEN 1
                WHEN xref.IdentifierValue RLIKE '^[A-Z]{{1,5}}$' AND LENGTH(xref.IdentifierValue) <= 5 THEN 2  -- Other real US tickers
                WHEN xref.IdentifierValue RLIKE '^(EQ|CB|ETF)[0-9]+$' THEN 4  -- Synthetic tickers
                ELSE 3  -- Other real tickers
            END,
            -- Then order alphabetically within each group
            xref.IdentifierValue
    """).collect()
    
    prompt_data = []
    
    # Use test mode counts if specified
    doc_counts = config.TEST_UNSTRUCTURED_COUNTS if test_mode else config.UNSTRUCTURED_COUNTS
    coverage_multiplier = 0.1 if test_mode else 1.0  # Reduce coverage in test mode
    
    for doc_type in document_types:
        print(f"📝 Generating prompts for: {doc_type}")
        
        if doc_type == 'broker_research':
            # Generate broker research prompts for equities
            coverage_count = int(400 * coverage_multiplier)  # Reduce coverage in test mode
            for security in securities[:coverage_count]:
                for report_num in range(doc_counts['broker_research']):
                    prompt_data.append(generate_broker_research_prompt(security, report_num))
        
        elif doc_type == 'earnings_transcripts':
            # Generate earnings transcript prompts
            coverage_count = int(400 * coverage_multiplier)
            for security in securities[:coverage_count]:
                for transcript_num in range(doc_counts['earnings_transcripts']):
                    transcript_type = 'Summary' if transcript_num == 0 else 'Q&A'
                    prompt_data.append(generate_earnings_transcript_prompt(security, transcript_type))
        
        elif doc_type == 'press_releases':
            # Generate press release prompts
            coverage_count = int(800 * coverage_multiplier)
            for security in securities[:coverage_count]:
                prompt_data.append(generate_press_release_prompt(security))
        
        elif doc_type == 'ngo_reports':
            # Generate NGO report prompts (issuer level)
            coverage_count = int(250 * coverage_multiplier)
            for security in securities[:coverage_count]:
                for report_num in range(doc_counts['ngo_reports']):
                    prompt_data.append(generate_ngo_report_prompt(security, report_num))
        
        elif doc_type == 'engagement_notes':
            # Generate engagement note prompts
            coverage_count = int(150 * coverage_multiplier)
            for security in securities[:coverage_count]:
                prompt_data.append(generate_engagement_note_prompt(security))
        
        elif doc_type in ['policy_docs', 'sales_templates', 'philosophy_docs']:
            # Generate global document prompts (not security-specific)
            count = doc_counts[doc_type]
            for doc_num in range(count):
                prompt_data.append(generate_global_document_prompt(doc_type, doc_num))
    
    # Save all prompts
    if prompt_data:
        prompts_df = session.create_dataframe(prompt_data)
        prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.GENERATION_PROMPTS")
        print(f"✅ Generated {len(prompt_data)} content prompts")

def generate_broker_research_prompt(security: dict, report_num: int) -> dict:
    """Generate broker research report prompt."""
    
    ratings = ['Strong Buy', 'Buy', 'Hold', 'Sell', 'Strong Sell']
    rating_weights = [0.10, 0.25, 0.45, 0.15, 0.05]  # Realistic distribution
    rating = random.choices(ratings, weights=rating_weights)[0]
    
    broker_names = ['Goldman Sachs', 'Morgan Stanley', 'J.P. Morgan', 'Bank of America', 'Barclays', 'UBS']
    broker = random.choice(broker_names)
    
    prompt_text = f"""You are a senior equity research analyst at {broker}. Write a comprehensive research report for {security['COMPANY_NAME']} ({security['TICKER']}) with a {rating} rating.

Structure your report as follows:

# {security['COMPANY_NAME']} ({security['TICKER']}) - {rating}

## Executive Summary
Write 2-3 sentences summarising your investment thesis and rating rationale for this {security['GICS_SECTOR']} company.

## Investment Highlights
- **Strong Market Position**: Describe competitive advantages in the {security['GICS_SECTOR']} sector
- **Growth Drivers**: Identify 2-3 key revenue and earnings growth catalysts
- **Financial Strength**: Highlight balance sheet and profitability metrics

## Key Risks
- List 2-3 primary risk factors that could impact the investment thesis
- Include sector-specific and company-specific risks

## Valuation and Price Target
- Current Price: $[realistic price based on sector]
- Price Target: $[price target consistent with rating]
- Valuation: [P/E ratio]x P/E vs sector average
- Include brief valuation methodology

## Recommendation
Conclude with {rating} recommendation and key rationale.

Use professional, confident tone. Include specific financial metrics and industry context. Write 700-1200 words in UK English."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': 'Broker Research Report',
        'SecurityID': security['SECURITYID'],
        'IssuerID': security['ISSUERID'],
        'TICKER': security['TICKER'],
        'COMPANY_NAME': security['COMPANY_NAME'],
        'GICS_SECTOR': security['GICS_SECTOR'],
        'PROMPT_TEXT': prompt_text
    }

def generate_earnings_transcript_prompt(security: dict, transcript_type: str) -> dict:
    """Generate earnings transcript prompt."""
    
    # Generate a more realistic quarter distribution
    # For demo purposes, we'll generate transcripts for the last 4 quarters
    current_date = datetime.now()
    quarters_back = random.randint(0, 3)
    quarter_date = current_date - timedelta(days=90 * quarters_back)
    quarter = f'Q{((quarter_date.month - 1) // 3) + 1}'
    year = quarter_date.year
    
    if transcript_type == 'Summary':
        prompt_text = f"""You are summarising an earnings call transcript for {security['COMPANY_NAME']} ({security['TICKER']}) {quarter} {year} earnings call.

Create a comprehensive earnings call summary:

# {security['COMPANY_NAME']} {quarter} {year} Earnings Call Summary

## Key Financial Results
- Revenue: $[realistic revenue for this sector]B (vs estimate $[estimate]B)
- EPS: $[realistic EPS] (vs estimate $[estimate])
- Guidance: Next quarter revenue $[low]B - $[high]B

## Management Commentary Highlights
Include 3-4 key quotes from CEO/CFO covering:
- Business performance and market conditions
- Strategic initiatives and investments
- Sector-specific trends in {security['GICS_SECTOR']}

## Q&A Key Points
Summarise 2-3 important analyst questions and management responses covering:
- Growth outlook and market dynamics
- Competitive positioning
- Capital allocation priorities

## Outlook
Management's forward-looking statements and strategic priorities for the {security['GICS_SECTOR']} sector.

Write 6,000-10,000 words in UK English with realistic financial metrics and industry-specific commentary."""
    else:  # Q&A
        prompt_text = f"""You are creating Q&A excerpts from {security['COMPANY_NAME']} ({security['TICKER']}) {quarter} {year} earnings call.

Create realistic analyst Q&A excerpts:

# {security['COMPANY_NAME']} {quarter} {year} Earnings Call - Q&A Excerpts

## Analyst Questions and Management Responses

Create 8-10 realistic Q&A exchanges covering:
- Revenue growth outlook in {security['GICS_SECTOR']}
- Margin expansion opportunities
- Capital expenditure plans
- Market share dynamics
- Regulatory or competitive concerns

Format each exchange as:
**[Analyst Name, Firm]**: [Detailed question]
**[CEO/CFO Name]**: [Detailed response with specific metrics and forward guidance]

Write 2,500-4,000 words in UK English. Include realistic financial figures and sector-specific insights."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': f'Earnings Transcript {transcript_type}',
        'SecurityID': security['SECURITYID'],
        'IssuerID': security['ISSUERID'],
        'TICKER': security['TICKER'],
        'COMPANY_NAME': security['COMPANY_NAME'],
        'GICS_SECTOR': security['GICS_SECTOR'],
        'PROMPT_TEXT': prompt_text
    }

def generate_press_release_prompt(security: dict) -> dict:
    """Generate press release prompt."""
    
    release_types = ['Earnings', 'Product', 'Corporate', 'ESG']
    release_type = random.choice(release_types)
    
    prompt_text = f"""You are writing a corporate press release for {security['COMPANY_NAME']} ({security['TICKER']}).

Create a {release_type} press release:

# {security['COMPANY_NAME']} [Headline Related to {release_type}]

**[City, Date]** - {security['COMPANY_NAME']} ({security['TICKER']}), a leading {security['GICS_SECTOR']} company, today announced [key development].

## Key Points
- [Primary announcement with specific details]
- [Financial or operational impact]
- [Strategic context and market implications]

## Management Commentary
Include 1-2 quotes from CEO or relevant executive providing context and forward-looking statements.

## About {security['COMPANY_NAME']}
Brief company description highlighting position in {security['GICS_SECTOR']} sector.

## Forward-Looking Statements
Standard disclaimer about forward-looking statements.

Write 250-400 words in UK English with professional corporate tone. Include specific metrics where appropriate."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': 'Press Release',
        'SecurityID': security['SECURITYID'],
        'IssuerID': security['ISSUERID'],
        'TICKER': security['TICKER'],
        'COMPANY_NAME': security['COMPANY_NAME'],
        'GICS_SECTOR': security['GICS_SECTOR'],
        'PROMPT_TEXT': prompt_text
    }

def generate_ngo_report_prompt(security: dict, report_num: int) -> dict:
    """Generate NGO report prompt."""
    
    ngo_names = ['Global Labour Watch', 'Environmental Defence Fund', 'Corporate Accountability International', 
                 'Oxfam', 'Human Rights Watch', 'Greenpeace', 'Transparency International']
    ngo_name = random.choice(ngo_names)
    
    categories = ['Environmental', 'Social', 'Governance']
    category = random.choice(categories)
    
    severity_levels = ['High', 'Medium', 'Low']
    severity_weights = [0.1, 0.3, 0.6]  # Most reports are low-medium severity
    severity = random.choices(severity_levels, weights=severity_weights)[0]
    
    # Select appropriate keywords based on category and severity
    keywords = random.choice(config.ESG_CONTROVERSY_KEYWORDS[category.lower()][severity.lower()])
    
    prompt_text = f"""You are writing an NGO report from {ngo_name} about {category.lower()} issues at {security['COMPANY_NAME']}.

Create a {severity.lower()}-severity NGO report:

# {ngo_name} Report: {category} Concerns at {security['COMPANY_NAME']}

**Organisation**: {ngo_name}  
**Publication Date**: [Recent date]  
**Companies Affected**: {security['COMPANY_NAME']} ({security['TICKER']})

## Executive Summary
Provide overview of the {category.lower()} investigation findings related to {keywords}.

## Key Findings
- **{category} Issues**: Describe specific allegations or concerns related to {keywords}
- **Evidence**: Detail supporting documentation or investigation methods
- **Company Response**: Include any official company statements or responses

## Recommendations
List {ngo_name}'s recommended actions for the company and investors.

## Severity Assessment
**Level**: {severity}  
**Rationale**: Explain why this {severity.lower()} severity level was assigned based on {keywords}.

Write 400-800 words in UK English. Use factual, investigative tone appropriate for {severity.lower()} severity issues in the {security['GICS_SECTOR']} sector."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': 'NGO Report',
        'SecurityID': None,  # Issuer-level document
        'IssuerID': security['ISSUERID'],
        'TICKER': security['TICKER'],
        'COMPANY_NAME': security['COMPANY_NAME'],
        'GICS_SECTOR': security['GICS_SECTOR'],
        'PROMPT_TEXT': prompt_text
    }

def generate_engagement_note_prompt(security: dict) -> dict:
    """Generate ESG engagement note prompt."""
    
    meeting_types = ['Management Meeting', 'Shareholder Call', 'Site Visit']
    meeting_type = random.choice(meeting_types)
    
    prompt_text = f"""You are an ESG analyst at Snowcrest Asset Management writing an engagement log after a {meeting_type.lower()} with {security['COMPANY_NAME']}.

Create an engagement note:

# ESG Engagement Log: {security['COMPANY_NAME']} {meeting_type}

**Date**: [Recent date]  
**Meeting Type**: {meeting_type}  
**Participants**: SAM ESG Team, {security['COMPANY_NAME']} [relevant executives]

## Meeting Overview
Brief summary of the engagement purpose and key topics discussed.

## ESG Topics Discussed
- **Environmental**: [Specific environmental initiatives or concerns in {security['GICS_SECTOR']} context]
- **Social**: [Workforce, community, or supply chain topics]
- **Governance**: [Board composition, executive compensation, or transparency issues]

## Management Commitments
List 2-3 specific commitments or actions management agreed to undertake.

## Follow-up Actions
- [SAM internal actions]
- [Timeline for management deliverables]
- [Next engagement planned]

## Assessment
Brief evaluation of management's ESG commitment and progress.

Write 150-300 words in UK English with professional, objective tone."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': 'ESG Engagement Log',
        'SecurityID': None,  # Issuer-level document
        'IssuerID': security['ISSUERID'],
        'TICKER': security['TICKER'],
        'COMPANY_NAME': security['COMPANY_NAME'],
        'GICS_SECTOR': security['GICS_SECTOR'],
        'PROMPT_TEXT': prompt_text
    }

def generate_global_document_prompt(doc_type: str, doc_num: int) -> dict:
    """Generate prompts for global documents (policy, sales, philosophy)."""
    
    if doc_type == 'policy_docs':
        if doc_num == 0:
            title = "Sustainable Investment Policy"
            prompt_text = """You are writing Snowcrest Asset Management's Sustainable Investment Policy.

Create a comprehensive ESG investment policy:

# Snowcrest Asset Management - Sustainable Investment Policy

## Policy Statement
Our commitment to integrating environmental, social, and governance (ESG) factors into investment decisions.

## Investment Approach
- **ESG Integration**: How ESG factors are incorporated into fundamental analysis
- **Exclusion Criteria**: Specific industries and practices excluded from investment
- **Engagement Strategy**: Active ownership and stewardship approach

## Compliance Requirements
- Minimum ESG rating thresholds (BBB or higher for ESG-labelled portfolios)
- Controversy exclusion procedures (high-severity controversies trigger review)
- Regular portfolio screening processes

## Governance and Oversight
- ESG committee structure and responsibilities
- Reporting and monitoring procedures
- Policy review and update processes

Write 800-1500 words in UK English with formal, policy-appropriate tone."""

        elif doc_num == 1:
            title = "Investment Management Agreement Template"
            prompt_text = """You are writing an Investment Management Agreement (IMA) template for Snowcrest Asset Management.

Create a sample IMA with key investment constraints:

# Investment Management Agreement - Sample Template

## Investment Objectives
Portfolio objectives and performance benchmarks.

## Investment Guidelines
- **Asset Allocation**: Permitted asset classes and ranges
- **Concentration Limits**: Maximum 7% in any single issuer, early warning at 6.5%
- **Quality Requirements**: Minimum 75% Investment Grade for fixed income
- **Duration Limits**: Portfolio duration within ±1.0 years of benchmark
- **ESG Requirements**: Minimum BBB ESG rating for ESG-labelled portfolios

## Prohibited Investments
- Specific exclusions and restricted activities
- ESG-related exclusions for applicable portfolios
- High-severity ESG controversy exclusions

## Risk Management
- Concentration monitoring and reporting
- Credit quality constraints (maximum 5% CCC and below)
- Liquidity requirements and guidelines

Write 800-1500 words in UK English with legal, professional tone."""

        else:
            title = "Compliance Manual"
            prompt_text = """You are writing Snowcrest Asset Management's Compliance Manual.

Create a compliance procedures manual:

# SAM Compliance Manual - Investment Operations

## Overview
Compliance framework for investment management operations.

## Daily Compliance Monitoring
- Position concentration checks (7% limit, 6.5% warning)
- Investment mandate adherence verification
- Trade compliance procedures and approvals

## ESG Compliance
- ESG rating monitoring (BBB minimum for ESG portfolios)
- Controversy screening procedures using keyword detection
- Engagement documentation requirements

## Fixed Income Compliance
- Credit quality monitoring (75% IG minimum, 5% CCC maximum)
- Duration risk management (±1.0 years vs benchmark)
- Rating migration tracking

## Reporting Requirements
- Daily breach reporting and escalation
- Monthly compliance summary reports
- Quarterly ESG compliance reviews

Write 800-1500 words in UK English with authoritative, procedural tone."""
    
    elif doc_type == 'sales_templates':
        if doc_num == 0:
            title = "Monthly Client Report Template"
            prompt_text = """You are creating a monthly client report template for Snowcrest Asset Management.

Create a professional monthly report template:

# Monthly Portfolio Report Template

## Executive Summary
[Template section for key performance highlights and market commentary]

## Performance Summary
- **Fund Performance**: [Template for returns vs benchmark with specific periods]
- **Attribution Analysis**: [Template for sector/security attribution breakdown]
- **Risk Metrics**: [Template for volatility, tracking error, and concentration]

## Portfolio Changes
- **New Positions**: [Template for position additions with rationale]
- **Position Changes**: [Template for increases/decreases]
- **Disposals**: [Template for position exits with reasoning]

## Holdings Analysis
- **Top 10 Holdings**: [Template for largest positions and weights]
- **Sector Allocation**: [Template for GICS sector breakdown]
- **Geographic Exposure**: [Template for country/region allocation]

## Market Commentary
[Template section for market outlook and portfolio positioning]

## ESG Highlights
[Template for ESG-related updates, engagement activities, and sustainability metrics]

## Outlook and Strategy
[Template for forward-looking commentary and strategic positioning]

## Important Information
Standard disclaimers: "This report is for informational purposes only and does not constitute investment advice. Past performance does not guarantee future results. Snowcrest Asset Management is a fictitious entity for demonstration purposes."

Write 800-1500 words in UK English with professional, client-appropriate tone."""

        else:
            title = "Quarterly Client Letter Template"
            prompt_text = """You are creating a quarterly client letter template for Snowcrest Asset Management.

Create an extended quarterly letter template:

# Quarterly Client Letter Template

## Dear [Client Name]

## Performance Review
Detailed quarterly performance analysis including:
- Absolute and relative returns across multiple time periods
- Key contributors and detractors to performance
- Benchmark comparison and tracking analysis
- Risk-adjusted performance metrics

## Portfolio Positioning
- Current asset allocation and strategic positioning
- Sector and regional exposures with rationale
- Key conviction positions and investment themes
- Recent portfolio changes and their impact

## Market Environment
- Quarterly market review and key developments
- Economic outlook and policy implications
- Sector rotation and thematic trends
- Volatility and risk environment assessment

## ESG Integration
- ESG performance highlights and metrics
- Active engagement activities and outcomes
- Sustainable investment updates and initiatives
- Climate transition and impact considerations

## Investment Themes
- Thematic investment updates (AI, renewable energy, cybersecurity)
- Innovation and disruption trends
- Long-term structural changes and opportunities

## Looking Ahead
- Investment outlook and market expectations
- Portfolio strategy and positioning for next quarter
- Risk considerations and mitigation strategies
- Opportunities and challenges on the horizon

## Conclusion
[Template for closing remarks, appreciation, and next steps]

Write 800-1500 words in UK English with personal, relationship-building tone."""
    
    else:  # philosophy_docs
        if doc_num == 0:
            title = "ESG Investment Philosophy"
            prompt_text = """You are writing Snowcrest Asset Management's ESG Investment Philosophy.

Create our ESG investment philosophy document:

# Snowcrest Asset Management - ESG Investment Philosophy

## Our ESG Approach
Our belief that environmental, social, and governance factors are financially material and drive long-term returns.

## Investment Integration
- **Fundamental Analysis**: How ESG factors enhance traditional financial analysis
- **Risk Assessment**: ESG as a risk mitigation and opportunity identification tool
- **Thematic Investing**: ESG-driven investment themes and secular trends

## Active Ownership and Stewardship
- **Engagement Strategy**: Constructive dialogue with portfolio companies on ESG issues
- **Proxy Voting**: Responsible voting policies aligned with long-term value creation
- **Collaborative Initiatives**: Industry engagement and policy advocacy

## Thematic Focus Areas
- **Climate Transition**: Renewable energy, energy efficiency, and decarbonisation
- **Digital Innovation**: AI, automation, and technological transformation
- **Social Impact**: Human capital, diversity, and community development

## Measurement and Reporting
- ESG metrics and performance measurement
- Impact assessment and outcome tracking
- Transparency and stakeholder communication

Write 800-1500 words in UK English with philosophical, thought-leadership tone."""

        elif doc_num == 1:
            title = "Risk Management Philosophy"
            prompt_text = """You are writing Snowcrest Asset Management's Risk Management Philosophy.

Create our risk management philosophy:

# Risk Management Philosophy

## Risk Framework
Our comprehensive approach to identifying, measuring, and managing investment risks across all asset classes.

## Risk Types and Management
- **Market Risk**: Systematic and specific risk management across equities and fixed income
- **Credit Risk**: Issuer and counterparty risk assessment and monitoring
- **Liquidity Risk**: Portfolio liquidity management and funding considerations
- **Operational Risk**: Process, system, and human capital risk mitigation

## Risk Management Process
- **Identification**: Early warning systems and comprehensive risk monitoring
- **Measurement**: Quantitative models and qualitative assessment frameworks
- **Management**: Active risk mitigation strategies and portfolio controls
- **Monitoring**: Continuous oversight, reporting, and governance

## Integration with Investment Process
- Portfolio construction and risk budgeting
- Security selection and risk-adjusted returns
- Performance attribution and risk decomposition
- Stress testing and scenario analysis

## Governance and Oversight
- Risk committee structure and responsibilities
- Risk reporting and escalation procedures
- Regular risk framework review and enhancement

Write 800-1500 words in UK English with authoritative, technical tone."""

        else:
            title = "Brand Messaging Guidelines"
            prompt_text = """You are writing Snowcrest Asset Management's Brand Messaging Guidelines.

Create brand messaging guidelines:

# Brand Messaging Guidelines

## Brand Positioning
Snowcrest Asset Management as a forward-thinking, technology-enhanced, ESG-focused investment manager.

## Core Value Propositions
- **Innovation Leadership**: Pioneering AI-enhanced investment processes and data analytics
- **ESG Excellence**: Deep expertise in sustainable investing and active stewardship
- **Performance Focus**: Delivering superior risk-adjusted returns through disciplined processes

## Key Messages by Audience
- **Institutional Clients**: Sophisticated investment solutions and risk management
- **Consultants**: Differentiated capabilities and consistent performance
- **Prospects**: Innovation, sustainability, and fiduciary excellence

## Communication Principles
- **Authentic**: Genuine commitment to stated values and client success
- **Transparent**: Clear, honest communication about performance and processes
- **Professional**: Institutional-quality expertise and service delivery
- **Forward-Looking**: Emphasis on innovation and future-ready solutions

## Competitive Differentiators
- Advanced AI and machine learning capabilities
- Integrated ESG expertise across all strategies
- Multi-asset investment platform and solutions
- Strong performance track record and risk management

## Tone and Style Guidelines
Professional yet approachable, confident but not arrogant, innovative while maintaining institutional credibility.

Write 800-1500 words in UK English with marketing-appropriate, professional tone."""
    
    return {
        'PROMPT_ID': str(uuid.uuid4()),
        'DOCUMENT_TYPE': doc_type.replace('_', ' ').title(),
        'SecurityID': None,  # Global document
        'IssuerID': None,    # Global document
        'TICKER': None,
        'COMPANY_NAME': None,
        'GICS_SECTOR': None,
        'PROMPT_TEXT': prompt_text
    }

def generate_content(session: Session, document_types: List[str]):
    """Generate content using Cortex Complete function."""
    
    # Process each document type separately for better control
    for doc_type in document_types:
        print(f"🤖 Generating {doc_type} content with {config.MODEL_NAME}...")
        
        try:
            # Map document types to their filter patterns
            if doc_type == 'broker_research':
                doc_filter = "DOCUMENT_TYPE = 'Broker Research Report'"
            elif doc_type == 'earnings_transcripts':
                doc_filter = "DOCUMENT_TYPE LIKE 'Earnings Transcript%'"
            elif doc_type == 'press_releases':
                doc_filter = "DOCUMENT_TYPE = 'Press Release'"
            elif doc_type == 'ngo_reports':
                doc_filter = "DOCUMENT_TYPE = 'NGO Report'"
            elif doc_type == 'engagement_notes':
                doc_filter = "DOCUMENT_TYPE = 'ESG Engagement Log'"
            else:
                doc_filter = f"DOCUMENT_TYPE = '{doc_type.replace('_', ' ').title()}'"
            
            # Generate content using Cortex Complete with batch processing
            session.sql(f"""
                CREATE OR REPLACE TABLE {config.DATABASE_NAME}.RAW.{config.DOCUMENT_TYPES[doc_type]['table_name']}_TEMP AS
                SELECT 
                    PROMPT_ID,
                    DOCUMENT_TYPE,
                    SecurityID,
                    IssuerID,
                    TICKER,
                    COMPANY_NAME,
                    GICS_SECTOR,
                    SNOWFLAKE.CORTEX.COMPLETE('{config.MODEL_NAME}', PROMPT_TEXT) as GENERATED_CONTENT,
                    CURRENT_TIMESTAMP() as GENERATED_TIMESTAMP
                FROM {config.DATABASE_NAME}.RAW.GENERATION_PROMPTS
                WHERE {doc_filter}
            """).collect()
            
            # Transform to final RAW table with proper schema
            create_raw_table(session, doc_type)
            
            print(f"✅ Generated {doc_type} content successfully")
            
        except Exception as e:
            print(f"❌ Failed to generate {doc_type} content: {e}")
            # Continue with other document types

def create_raw_table(session: Session, doc_type: str):
    """Create properly structured RAW table from generated content."""
    
    table_name = f"{config.DATABASE_NAME}.RAW.{config.DOCUMENT_TYPES[doc_type]['table_name']}"
    temp_table = f"{table_name}_TEMP"
    
    if doc_type == 'broker_research':
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                SecurityID,
                IssuerID,
                TICKER || ' Research Report - ' || SUBSTR(GENERATED_CONTENT, 1, 50) as DOCUMENT_TITLE,
                'Broker Research Report' as DOCUMENT_TYPE,
                CURRENT_DATE() - UNIFORM(1, 90, RANDOM())::int as PUBLISH_DATE,
                SPLIT_PART(GENERATED_CONTENT, 'analyst at ', 2) as BROKER_NAME,
                'Analyst_' || UNIFORM(1, 100, RANDOM())::int as ANALYST_NAME,
                CASE 
                    WHEN GENERATED_CONTENT LIKE '%Strong Buy%' THEN 'Strong Buy'
                    WHEN GENERATED_CONTENT LIKE '%Buy%' THEN 'Buy'
                    WHEN GENERATED_CONTENT LIKE '%Sell%' THEN 'Sell'
                    WHEN GENERATED_CONTENT LIKE '%Strong Sell%' THEN 'Strong Sell'
                    ELSE 'Hold'
                END as RATING,
                UNIFORM(50, 500, RANDOM()) as PRICE_TARGET,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM {temp_table}
        """).collect()
        
    elif doc_type == 'earnings_transcripts':
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            WITH numbered_transcripts AS (
                -- First, number the transcripts
                SELECT 
                    *,
                    ROW_NUMBER() OVER (PARTITION BY SecurityID ORDER BY PROMPT_ID) as transcript_num
                FROM {temp_table}
            ),
            quarter_assignments AS (
                -- Assign quarters based on transcript number
                SELECT 
                    nt.*,
                    -- Each company gets transcripts for last 4 quarters
                    CASE MOD(nt.transcript_num - 1, 4)
                        WHEN 0 THEN DATEADD(quarter, -3, DATE_TRUNC('quarter', CURRENT_DATE()))
                        WHEN 1 THEN DATEADD(quarter, -2, DATE_TRUNC('quarter', CURRENT_DATE()))
                        WHEN 2 THEN DATEADD(quarter, -1, DATE_TRUNC('quarter', CURRENT_DATE()))
                        WHEN 3 THEN DATE_TRUNC('quarter', CURRENT_DATE())
                    END as quarter_start
                FROM numbered_transcripts nt
            )
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                SecurityID,
                IssuerID,
                TICKER || ' Earnings Call - ' || SUBSTR(GENERATED_CONTENT, 1, 50) as DOCUMENT_TITLE,
                CASE 
                    WHEN DOCUMENT_TYPE LIKE '%Summary%' THEN 'Earnings Transcript Summary'
                    ELSE 'Earnings Q&A Excerpts'
                END as DOCUMENT_TYPE,
                -- Publish date is 2-4 weeks after quarter end
                DATEADD(day, UNIFORM(14, 28, RANDOM())::int, LAST_DAY(quarter_start, 'quarter')) as PUBLISH_DATE,
                -- Fiscal quarter matches the actual quarter of the earnings
                'Q' || QUARTER(quarter_start) || ' ' || YEAR(quarter_start) as FISCAL_QUARTER,
                CASE 
                    WHEN DOCUMENT_TYPE LIKE '%Summary%' THEN 'Summary'
                    ELSE 'Q&A'
                END as TRANSCRIPT_TYPE,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM quarter_assignments
        """).collect()
    
    elif doc_type == 'press_releases':
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                SecurityID,
                IssuerID,
                TICKER || ' Press Release - ' || SUBSTR(GENERATED_CONTENT, 1, 50) as DOCUMENT_TITLE,
                'Press Release' as DOCUMENT_TYPE,
                CURRENT_DATE() - UNIFORM(1, 60, RANDOM())::int as PUBLISH_DATE,
                ARRAY_CONSTRUCT('Earnings', 'Product', 'Corporate', 'ESG')[UNIFORM(0, 3, RANDOM())::int] as RELEASE_TYPE,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM {temp_table}
        """).collect()
    
    elif doc_type == 'ngo_reports':
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                NULL as SecurityID,  -- Issuer-level document
                IssuerID,
                SUBSTR(GENERATED_CONTENT, 1, 100) as DOCUMENT_TITLE,
                'NGO Report' as DOCUMENT_TYPE,
                CURRENT_DATE() - UNIFORM(1, 180, RANDOM())::int as PUBLISH_DATE,
                ARRAY_CONSTRUCT('Global Labour Watch', 'Environmental Defence Fund', 'Human Rights Watch')[UNIFORM(0, 2, RANDOM())::int] as NGO_NAME,
                ARRAY_CONSTRUCT('Environmental', 'Social', 'Governance')[UNIFORM(0, 2, RANDOM())::int] as REPORT_CATEGORY,
                ARRAY_CONSTRUCT('High', 'Medium', 'Low')[UNIFORM(0, 2, RANDOM())::int] as SEVERITY_LEVEL,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM {temp_table}
        """).collect()
    
    elif doc_type == 'engagement_notes':
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                NULL as SecurityID,  -- Issuer-level document
                IssuerID,
                TICKER || ' ESG Engagement - ' || SUBSTR(GENERATED_CONTENT, 1, 50) as DOCUMENT_TITLE,
                'ESG Engagement Log' as DOCUMENT_TYPE,
                CURRENT_DATE() - UNIFORM(1, 365, RANDOM())::int as PUBLISH_DATE,
                ARRAY_CONSTRUCT('Management Meeting', 'Shareholder Call', 'Site Visit')[UNIFORM(0, 2, RANDOM())::int] as MEETING_TYPE,
                'SAM ESG Team, Company Management' as PARTICIPANTS,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM {temp_table}
        """).collect()
    
    else:  # policy_docs, sales_templates, philosophy_docs
        session.sql(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT 
                PROMPT_ID as DOCUMENT_ID,
                NULL as SecurityID,  -- Global document
                NULL as IssuerID,    -- Global document
                SUBSTR(GENERATED_CONTENT, 1, 100) as DOCUMENT_TITLE,
                '{doc_type.replace('_', ' ').title()}' as DOCUMENT_TYPE,
                CURRENT_DATE() - UNIFORM(30, 365, RANDOM())::int as PUBLISH_DATE,
                GENERATED_CONTENT as RAW_MARKDOWN,
                'en' as LANGUAGE
            FROM {temp_table}
        """).collect()
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {temp_table}").collect()

def create_corpus_tables(session: Session, document_types: List[str]):
    """Create normalized corpus tables for Cortex Search indexing."""
    
    for doc_type in document_types:
        print(f"📚 Creating {doc_type} corpus table...")
        
        raw_table = f"{config.DATABASE_NAME}.RAW.{config.DOCUMENT_TYPES[doc_type]['table_name']}"
        corpus_table = f"{config.DATABASE_NAME}.CURATED.{config.DOCUMENT_TYPES[doc_type]['corpus_name']}"
        
        # Create standardized corpus table with SecurityID and IssuerID
        session.sql(f"""
            CREATE OR REPLACE TABLE {corpus_table} AS
            SELECT 
                DOCUMENT_ID,
                DOCUMENT_TITLE,
                DOCUMENT_TYPE,
                SecurityID,
                IssuerID,
                PUBLISH_DATE,
                'en' as LANGUAGE,
                RAW_MARKDOWN as DOCUMENT_TEXT
            FROM {raw_table}
        """).collect()
        
        print(f"✅ Created corpus table: {corpus_table}")
    
    print("✅ All corpus tables created successfully")
