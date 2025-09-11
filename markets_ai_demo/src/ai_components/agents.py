# src/ai_components/agents.py
# Agent configuration templates for Frost Markets Intelligence Demo

"""
Agent Configuration Templates for Snowflake Intelligence

This module contains the configuration templates for all demo agents.
Copy these configurations into Snowsight when setting up agents.

Phase 1 Agents (Build First):
1. Earnings Analysis Agent - Equity Research Analyst scenario
2. Thematic Research Agent - Equity Research Analyst scenario

Phase 2 Agents (Future):
3. Market Reports Agent - Global Research & Market Insights scenario  
4. Client Strategy Agent - Global Research & Market Insights scenario
"""

from config import DemoConfig


def get_phase_1_agent_configs():
    """Return Phase 1 agent configurations"""
    
    return {
        "earnings_analysis_agent": {
            "agent_name": "earnings_analysis_agent",
            "display_name": "Earnings Analysis Assistant", 
            "description": "Specialized assistant for analyzing quarterly earnings results, consensus estimates, and management commentary",
            "orchestration_model": "Claude 4",
            "tools": [
                "earnings_data_analyzer (Cortex Analyst)",
                "search_earnings_transcripts (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help equity research analysts understand quarterly earnings performance and management commentary.

Tool Selection Logic:
1. For questions about SPECIFIC FINANCIAL RESULTS, headline numbers, consensus beats/misses, or historical performance comparisons:
   → Use the earnings_data_analyzer (Cortex Analyst) tool on ANALYTICS.EARNINGS_ANALYSIS_VIEW
   
2. For questions about MANAGEMENT COMMENTARY, tone, sentiment, analyst questions, or specific quotes from earnings calls:
   → Use the search_earnings_transcripts (Cortex Search) tool on ANALYTICS.EARNINGS_TRANSCRIPTS_SEARCH
   
3. For generating SUMMARIES, REPORTS, or FIRST TAKE notes:
   → Gather data from appropriate tools first, then synthesize the information

Examples:
- "Revenue for Netflix Q3" → Use earnings_data_analyzer
- "What did management say about subscriber growth?" → Use search_earnings_transcripts  
- "Compare revenue vs estimates for last 4 quarters" → Use earnings_data_analyzer
- "Management tone on guidance" → Use search_earnings_transcripts""",
            
            "response_instructions": """You are a world-class equity research assistant specializing in earnings analysis.

Response Guidelines:
- Be concise, accurate, and data-driven in all responses
- Present numerical data clearly in sentences or markdown tables
- When providing charts/visualizations, include the underlying data in table format
- Always cite your sources (e.g., "According to the Q3 10-Q filing...", "Based on the earnings call transcript...")
- Use professional financial terminology appropriate for research analysts
- For beat/miss analysis, clearly state both dollar amounts and percentages
- When quoting management, use exact quotes and provide context

Format for Financial Results:
- Lead with the headline: "[Company] reported [Metric] of $X vs consensus of $Y, a Z% beat/miss"
- Follow with context and drivers
- Include relevant management commentary if available

Tone: Professional, analytical, and confident while remaining objective."""
        },
        
        "thematic_research_agent": {
            "agent_name": "thematic_research_agent",
            "display_name": "Thematic Investment Research Assistant",
            "description": "Advanced assistant for discovering emerging investment themes and cross-sector trends from alternative data sources",
            "orchestration_model": "Claude 4", 
            "tools": [
                "thematic_data_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)",
                "search_news_articles (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help equity research analysts discover and analyze emerging investment themes and trends.

Tool Selection Logic:
1. For questions about THEMATIC TRENDS, investment themes, or cross-sector analysis:
   → Use the thematic_data_analyzer (Cortex Analyst) tool on ANALYTICS.THEMATIC_RESEARCH_VIEW
   
2. For questions about INTERNAL RESEARCH, official firm analysis, or regulatory topics:
   → Use the search_research_reports (Cortex Search) tool on ANALYTICS.RESEARCH_REPORTS_SEARCH
   
3. For questions about MARKET EVENTS, news analysis, or current developments:
   → Use the search_news_articles (Cortex Search) tool on ANALYTICS.NEWS_ARTICLES_SEARCH

4. For STOCK PERFORMANCE related to themes:
   → Use thematic_data_analyzer to get price data and correlations

Strategy for Complex Queries:
- Start with thematic_data_analyzer for quantitative analysis
- Use search tools to provide supporting qualitative context
- Synthesize findings from multiple sources

Examples:
- "Carbon capture technology trends" → search_research_reports + search_news_articles
- "Companies exposed to semiconductor risk" → thematic_data_analyzer
- "Stock performance of climate tech companies" → thematic_data_analyzer""",
            
            "response_instructions": """You are an expert thematic investment research assistant focused on identifying emerging trends and cross-sector opportunities.

Response Guidelines:
- Think like a senior research analyst looking for alpha-generating insights
- Combine quantitative analysis with qualitative context
- Identify unexpected connections between sectors, themes, and market events
- Provide actionable investment implications, not just academic analysis
- When discussing themes, always connect to specific investable companies
- Use data to support qualitative observations

Format for Thematic Analysis:
- Start with the key finding or trend identification
- Provide supporting data (company exposure, performance metrics)
- Include market context and news developments
- End with investment implications or questions for further research

Investment Focus:
- Look for early-stage themes before they become consensus
- Identify companies with unexpected exposure to emerging trends
- Flag both opportunities and risks within themes
- Consider regulatory, technological, and market drivers

Tone: Insightful, forward-looking, and commercially minded while remaining analytically rigorous."""
        }
    }


def get_phase_2_agent_configs():
    """Return Phase 2 agent configurations (for future implementation)"""
    
    return {
        "market_reports_agent": {
            "agent_name": "market_reports_agent", 
            "display_name": "Market Structure Research Assistant",
            "description": "Specialist in market structure analysis, regulatory changes, and institutional client insights",
            "orchestration_model": "Claude 4",
            "tools": [
                "client_engagement_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)"
            ],
            "planning_instructions": "TBD - Phase 2",
            "response_instructions": "TBD - Phase 2"
        },
        
        "client_strategy_agent": {
            "agent_name": "client_strategy_agent",
            "display_name": "Client Strategy Assistant", 
            "description": "Strategic assistant for preparing data-driven client meetings and personalized recommendations",
            "orchestration_model": "Claude 4",
            "tools": [
                "client_impact_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)"
            ],
            "planning_instructions": "TBD - Phase 2", 
            "response_instructions": "TBD - Phase 2"
        }
    }


def print_agent_setup_instructions():
    """Print detailed setup instructions for Snowsight"""
    
    print("\n" + "="*80)
    print("🤖 AGENT SETUP INSTRUCTIONS FOR SNOWSIGHT")
    print("="*80)
    
    print("\n📋 Setup Process:")
    print("1. Open Snowsight and navigate to Snowflake Intelligence")
    print("2. Click 'Create Agent'")
    print("3. Copy the configuration below for each agent")
    print("4. Configure tools as specified")
    print("5. Test with sample queries")
    
    print("\n" + "="*50)
    print("PHASE 1 AGENTS (Build These First)")
    print("="*50)
    
    phase_1_configs = get_phase_1_agent_configs()
    
    for agent_id, config in phase_1_configs.items():
        print(f"\n🔧 {config['display_name'].upper()}")
        print("-" * 60)
        print(f"Agent Name: {config['agent_name']}")
        print(f"Display Name: {config['display_name']}")
        print(f"Description: {config['description']}")
        print(f"Orchestration Model: {config['orchestration_model']}")
        print()
        print("Tools:")
        for tool in config['tools']:
            print(f"  - {tool}")
        print()
        print("Planning Instructions:")
        print(config['planning_instructions'])
        print()
        print("Response Instructions:")
        print(config['response_instructions'])
        print("\n" + "-" * 60)


def get_tool_configurations():
    """Return tool configurations for agents"""
    
    return {
        "earnings_data_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "ANALYTICS.EARNINGS_ANALYSIS_VIEW",
            "description": "Analyzes quarterly earnings results, consensus estimates, and beat/miss calculations. Use for financial metrics, performance comparisons, and quantitative earnings analysis."
        },
        
        "search_earnings_transcripts": {
            "type": "Cortex Search",
            "search_service": "ANALYTICS.EARNINGS_TRANSCRIPTS_SEARCH", 
            "description": "Searches earnings call transcripts for management commentary, analyst questions, and qualitative insights. Use for tone analysis, guidance discussions, and specific quotes."
        },
        
        "thematic_data_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "ANALYTICS.THEMATIC_RESEARCH_VIEW",
            "description": "Analyzes thematic investment trends, company exposures, and cross-sector patterns. Use for identifying emerging themes and quantifying company relationships to trends."
        },
        
        "search_research_reports": {
            "type": "Cortex Search", 
            "search_service": "ANALYTICS.RESEARCH_REPORTS_SEARCH",
            "description": "Searches internal research reports and official firm analysis. Use for regulatory topics, market structure insights, and established firm positions on themes."
        },
        
        "search_news_articles": {
            "type": "Cortex Search",
            "search_service": "ANALYTICS.NEWS_ARTICLES_SEARCH", 
            "description": "Searches news articles and market event coverage. Use for current developments, market reaction analysis, and real-time event context."
        }
    }


def get_demo_test_queries():
    """Return test queries for validating agent setups"""
    
    return {
        "earnings_analysis_agent": [
            "Give me a summary of Netflix's latest quarter results",
            "How did Netflix perform against consensus estimates?", 
            "What was management's tone about subscriber growth in the earnings call?",
            "Generate a chart comparing Netflix revenue vs estimates for the last 4 quarters"
        ],
        
        "thematic_research_agent": [
            "What are the emerging trends in carbon capture technology?",
            "Which companies have the highest exposure to semiconductor supply chain risks?",
            "Show me the stock performance of companies involved in climate technology",
            "Find recent news about direct air capture developments"
        ]
    }


if __name__ == "__main__":
    # Print setup instructions when run directly
    print_agent_setup_instructions()
