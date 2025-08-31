-- ===================================================================
-- SAM Snowsight Intelligence Demo - Complete Sample Data Population
-- All structured data needed for the complete demo (6 companies, 3 clients)
-- ===================================================================

USE DATABASE FSI_DEMOS;
USE SCHEMA SAM_DEMO;

-- ===================================================================
-- COMPANY FINANCIAL DATA (6 companies across different sectors)
-- ===================================================================

INSERT INTO COMPANY_FINANCIALS VALUES
-- Tempus AI (Private medical AI company) - 8 quarters
(1, 'TMPS', 'Tempus AI', '2023-03-31', '2023Q1', 145.2, -23.1, 38.5, 892.3),
(1, 'TMPS', 'Tempus AI', '2023-06-30', '2023Q2', 167.8, -19.4, 42.1, 873.8),
(1, 'TMPS', 'Tempus AI', '2023-09-30', '2023Q3', 189.3, -15.2, 46.3, 901.2),
(1, 'TMPS', 'Tempus AI', '2023-12-31', '2023Q4', 212.7, -8.9, 51.8, 934.5),
(1, 'TMPS', 'Tempus AI', '2024-03-31', '2024Q1', 238.4, -4.2, 56.2, 978.9),
(1, 'TMPS', 'Tempus AI', '2024-06-30', '2024Q2', 267.9, 2.1, 61.7, 1023.4),
(1, 'TMPS', 'Tempus AI', '2024-09-30', '2024Q3', 294.5, 8.7, 67.3, 1089.2),
(1, 'TMPS', 'Tempus AI', '2024-12-31', '2024Q4', 321.8, 15.4, 73.9, 1156.7),

-- NorthernCell Energy (Private solid-state battery company) - 6 quarters  
(2, 'NCLL', 'NorthernCell Energy', '2023-06-30', '2023Q2', 89.4, -45.7, 67.2, 456.8),
(2, 'NCLL', 'NorthernCell Energy', '2023-09-30', '2023Q3', 102.1, -41.3, 72.8, 478.9),
(2, 'NCLL', 'NorthernCell Energy', '2023-12-31', '2023Q4', 118.7, -35.9, 79.1, 523.4),
(2, 'NCLL', 'NorthernCell Energy', '2024-03-31', '2024Q1', 134.2, -29.8, 85.6, 567.2),
(2, 'NCLL', 'NorthernCell Energy', '2024-06-30', '2024Q2', 151.9, -22.4, 92.3, 612.8),
(2, 'NCLL', 'NorthernCell Energy', '2024-09-30', '2024Q3', 168.5, -16.1, 98.7, 659.3),

-- Arkadia Commerce (Platform retail - key company for PM thesis evolution demo) - 6 quarters
(3, 'ARKD', 'Arkadia Commerce', '2023-03-31', '2023Q1', 2847.3, 312.8, 145.6, 1834.2),
(3, 'ARKD', 'Arkadia Commerce', '2023-06-30', '2023Q2', 3102.7, 389.1, 167.3, 2156.8),
(3, 'ARKD', 'Arkadia Commerce', '2023-09-30', '2023Q3', 3456.9, 478.2, 189.7, 2398.4),
(3, 'ARKD', 'Arkadia Commerce', '2023-12-31', '2023Q4', 3821.5, 567.9, 213.8, 2672.1),
(3, 'ARKD', 'Arkadia Commerce', '2024-03-31', '2024Q1', 4234.8, 645.3, 241.2, 2945.7),
(3, 'ARKD', 'Arkadia Commerce', '2024-06-30', '2024Q2', 4678.2, 734.6, 272.5, 3287.9),

-- Voltaic Dynamics (EV supply chain - for PM pre-mortem scenario) - 6 quarters
(4, 'VOLT', 'Voltaic Dynamics', '2023-06-30', '2023Q2', 456.7, -67.3, 89.4, 578.9),
(4, 'VOLT', 'Voltaic Dynamics', '2023-09-30', '2023Q3', 523.8, -58.2, 102.7, 634.5),
(4, 'VOLT', 'Voltaic Dynamics', '2023-12-31', '2023Q4', 598.4, -45.1, 118.3, 698.2),
(4, 'VOLT', 'Voltaic Dynamics', '2024-03-31', '2024Q1', 672.9, -31.8, 134.8, 756.7),
(4, 'VOLT', 'Voltaic Dynamics', '2024-06-30', '2024Q2', 751.3, -18.4, 152.9, 823.4),
(4, 'VOLT', 'Voltaic Dynamics', '2024-09-30', '2024Q3', 834.7, -8.2, 173.6, 891.8),

-- Helios Semiconductors (AI chips) - 5 quarters
(5, 'HLIO', 'Helios Semiconductors', '2023-09-30', '2023Q3', 1234.6, 189.7, 567.8, 2341.2),
(5, 'HLIO', 'Helios Semiconductors', '2023-12-31', '2023Q4', 1456.8, 234.9, 645.3, 2567.8),
(5, 'HLIO', 'Helios Semiconductors', '2024-03-31', '2024Q1', 1687.9, 287.4, 732.1, 2834.5),
(5, 'HLIO', 'Helios Semiconductors', '2024-06-30', '2024Q2', 1923.4, 345.8, 823.7, 3123.9),
(5, 'HLIO', 'Helios Semiconductors', '2024-09-30', '2024Q3', 2178.5, 412.3, 921.8, 3456.2),

-- TerraLink Logistics (Global supply chain) - 4 quarters
(6, 'TLNK', 'TerraLink Logistics', '2024-03-31', '2024Q1', 890.4, 78.9, 34.5, 456.7),
(6, 'TLNK', 'TerraLink Logistics', '2024-06-30', '2024Q2', 967.8, 89.2, 38.9, 498.3),
(6, 'TLNK', 'TerraLink Logistics', '2024-09-30', '2024Q3', 1052.6, 102.4, 43.7, 543.8),
(6, 'TLNK', 'TerraLink Logistics', '2024-12-31', '2024Q4', 1143.9, 117.8, 49.2, 592.1);

-- ===================================================================
-- MARKET DATA (supporting data for context)
-- ===================================================================

INSERT INTO MARKET_DATA VALUES
-- Sample market data for context (Private companies so this represents reference indices)
('TMPS', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0),  -- Private company placeholder
('NCLL', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0),  -- Private company placeholder
('ARKD', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0),  -- Private company placeholder
('VOLT', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0),  -- Private company placeholder
('HLIO', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0),  -- Private company placeholder
('TLNK', '2024-12-20', 0.00, 0.00, 0.00, 0.00, 0);  -- Private company placeholder

-- ===================================================================
-- CLIENT DATA FOR CRM SCENARIOS
-- ===================================================================

INSERT INTO CLIENT_CRM VALUES
('SPT001', 'Scottish Pension Trust', 'Pension Fund', 2450.5, '2024-11-15', 
 'Sustainable investing, long-term growth, energy transition, ESG integration', 
 'Nov 2024: Discussed Q3 performance and energy transition portfolio alignment. Positive on Voltaic Dynamics despite short-term headwinds.'),

('EUE001', 'Edinburgh University Endowment', 'Endowment', 890.2, '2024-10-28',
 'Long-term capital preservation, growth equity, innovation exposure, tech disruption',
 'Oct 2024: Annual review meeting. Strong interest in AI and semiconductor themes. Pleased with Helios Semiconductors performance.'),

('HFO001', 'Highland Family Office', 'Family Office', 325.8, '2024-12-01',
 'Wealth preservation, next-generation focus, sustainable technology, private market access',
 'Dec 2024: Quarterly check-in. Interested in increasing allocation to private companies like Tempus AI and NorthernCell Energy.');

-- ===================================================================
-- CLIENT PORTFOLIO DATA
-- ===================================================================

INSERT INTO CLIENT_PORTFOLIOS VALUES
('PF_SPT_001', 'SPT001', 8.7, '2019-03-15'),
('PF_EUE_001', 'EUE001', 12.3, '2020-01-08'), 
('PF_HFO_001', 'HFO001', 15.8, '2021-06-22');

-- ===================================================================
-- PORTFOLIO HOLDINGS HISTORY
-- ===================================================================

INSERT INTO PORTFOLIO_HOLDINGS_HISTORY VALUES
-- Scottish Pension Trust holdings (focus on energy transition)
('TXN_001', 'PF_SPT_001', '2023-06-15', 'VOLT', 'BUY', 125000, 45.80, 8.5),
('TXN_002', 'PF_SPT_001', '2024-01-22', 'NCLL', 'BUY', 89000, 67.20, 6.2),
('TXN_003', 'PF_SPT_001', '2024-03-10', 'ARKD', 'BUY', 45000, 156.90, 12.3),

-- Edinburgh University Endowment holdings (focus on tech/innovation)
('TXN_004', 'PF_EUE_001', '2023-09-08', 'HLIO', 'BUY', 78000, 89.40, 15.4),
('TXN_005', 'PF_EUE_001', '2024-02-14', 'TMPS', 'BUY', 156000, 98.70, 11.8),
('TXN_006', 'PF_EUE_001', '2024-05-20', 'TLNK', 'BUY', 234000, 32.50, 9.2),

-- Highland Family Office holdings (focus on private/emerging companies)
('TXN_007', 'PF_HFO_001', '2023-11-30', 'TMPS', 'BUY', 89000, 78.60, 18.9),
('TXN_008', 'PF_HFO_001', '2024-04-18', 'NCLL', 'BUY', 67000, 71.30, 14.6),
('TXN_009', 'PF_HFO_001', '2024-08-25', 'VOLT', 'BUY', 123000, 52.40, 16.7);

-- ===================================================================
-- PROMPT TEMPLATES FOR SYNTHETIC DATA GENERATION
-- ===================================================================

INSERT INTO PROMPT_LIBRARY VALUES
-- Research notes for analyst scenarios
('research_note_001', 'ResearchNote', 
 'As an expert equity research analyst at Snowcap Asset Management, write a comprehensive investment research note for {COMPANY_NAME}, dated {DOC_DATE}. 
 
The tone should reflect SAM''s long-term, patient investor philosophy with phrases like "Actual Investor" and "unusual thinking" where appropriate.

Structure the note with:
1. Investment Thesis Summary (2-3 paragraphs)
2. Competitive Moat Analysis (3 key points)
3. Key Risks (2-3 significant risks) 
4. Long-term Outlook (5-10 year view)

Company Context: {COMPANY_NAME} is {EVENT_ANCHOR}. Focus on sustainable competitive advantages and long-term value creation potential.

Length: 800-1200 words. Include specific quotes that can be extracted later.', 
 'professional-optimistic', 800, 1200, 'SAM long-term philosophy, patient capital, Actual Investor', 'medium', TRUE, NULL),

-- 10-Question Framework scaffolding for analyst scenarios
('framework_scaffold_001', 'FrameworkScaffold', 
 'Using Snowcap Global Investment 10-Question Framework, analyze {COMPANY_NAME} focusing on Questions {QUESTION_NUMBERS}:
 
 Question 3: What is the scale of the opportunity?
 - Assess total addressable market and long-term growth potential
 - Consider secular trends and technological disruption potential
 
 Question 4: What is the company''s sustainable competitive advantage? 
 - Evaluate technology moat and proprietary assets
 - Analyze R&D spending trends over {TIME_PERIOD}
 - Assess network effects and switching costs
 
 Question 5: What is the quality of management?
 - Leadership vision and execution track record
 - Capital allocation decisions and long-term thinking
 - Cultural alignment with stakeholder interests
 
 For competitive advantage analysis, include:
 - R&D spending trends over last 8 quarters with growth rates
 - Technology moat assessment with patent portfolio review
 - Proprietary data advantages and network effects
 - Supporting quotes from earnings calls and management interviews
 
 Structure: Question → Analysis → Evidence → Long-term Implications (5-10 years)
 Tone: Patient capital investor perspective, "unusual thinking" approach
 Length: 1200-1500 words with minimum 3 citations per question
 
 Company Context: {COMPANY_NAME} is {EVENT_ANCHOR}. Apply Snowcap''s "Actual Investor" philosophy focusing on exceptional growth companies and decades-long value creation.', 
 'analytical-framework', 1200, 1500, 'SAM 10-Question Framework, patient capital, unusual thinking', 'medium', TRUE, NULL),

-- Earnings transcripts for analyst scenarios
('earnings_transcript_001', 'EarningsTranscript',
 'Generate a realistic earnings call transcript for {COMPANY_NAME} {QUARTER} earnings call held on {DOC_DATE}.

Include:
- Management Presentation (CEO remarks on performance, outlook)
- Q&A Section with 4-5 analyst questions focusing on:
  * R&D investments and model development progress  
  * Competitive positioning
  * Long-term growth trajectory
  * Technology roadmap

Company context: {TOPICS}

Make management responses sound authentic with specific metrics and forward-looking statements. Include sentiment-rich language about AI model performance, data advantages, or technology breakthroughs.

Length: 1500-2000 words.', 
 'professional-confident', 1500, 2000, 'Earnings call format, management tone', 'medium', TRUE, NULL),

-- Historical thesis documents for PM evolution analysis
('thesis_historical_001', 'HistoricalThesis', 
'As a Snowcap Asset Management research analyst, write a historical investment thesis for {COMPANY_NAME} from {EVENT_ANCHOR}, dated {DOC_DATE}.

This represents our investment thinking from {YEAR}. Focus on:
1. Investment Thesis (why we believe in long-term potential)
2. Competitive Moat Analysis (defensive characteristics) 
3. Key Risks (what could go wrong)
4. Market Position (vs competitors like {COMPETITOR})

Context: This is {YEAR} and {COMPANY_NAME} is {BUSINESS_CONTEXT}.

Tone: Reflect the investment conviction and market understanding of {YEAR}. Use period-appropriate language and concerns.

Length: 1000-1500 words. Write as a formal investment committee memo.', 
'professional-analytical', 1000, 1500, 'Historical SAM investment thinking, period-appropriate', 'medium', TRUE, NULL),

-- Meeting notes for corporate memory
('meeting_notes_001', 'MeetingNotes',
'Generate internal meeting notes from a Snowcap Asset Management portfolio manager meeting with {COMPANY_NAME} management on {DOC_DATE}.

Attendees: {ATTENDEES}
Meeting Type: {MEETING_TYPE}
Key Topics: {TOPICS}

Structure:
1. Executive Summary
2. Management Discussion Points
3. Key Insights and Takeaways  
4. Concerns Raised
5. Follow-up Actions

Include specific quotes from management about {FOCUS_AREAS}. Capture the SAM investment team''s assessment of management quality and strategic vision.

Tone: Internal notes, direct, analytical. Focus on investment-relevant insights.
Length: 800-1200 words.', 
'internal-analytical', 800, 1200, 'Internal meeting documentation, SAM perspective', 'medium', TRUE, NULL),

-- Client meeting notes for CRM scenarios  
('client_meeting_001', 'ClientMeetingNotes',
'Generate professional meeting notes for a Snowcap Asset Management client meeting with {CLIENT_NAME} on {DOC_DATE}.

Meeting Context: {MEETING_CONTEXT}
Attendees: {ATTENDEES}
Portfolio Focus: {PORTFOLIO_FOCUS}

Structure the notes as:
1. Meeting Agenda and Attendees
2. Portfolio Performance Review
3. Top Holdings Discussion (focus on {TOP_HOLDINGS})
4. Client Concerns and Questions
5. Market Outlook Discussion
6. Action Items and Follow-ups

Include specific quotes from investment rationale and ensure the tone reflects SAM''s "Actual Investor" philosophy and long-term approach.

Tone: Professional, client-facing, reassuring yet realistic.
Length: 600-900 words as realistic meeting minutes.', 
'professional-client-facing', 600, 900, 'Client meeting documentation, SAM voice', 'medium', TRUE, NULL),

-- Expert Network Interviews for Research Analyst scenarios
('expert_interview_001', 'ExpertNetworkInterview',
'Generate a comprehensive expert network interview summary for {COMPANY_NAME} industry analysis, conducted on {DOC_DATE}.

Expert Background: {EXPERT_BACKGROUND}
Interview Focus: {FOCUS_AREAS}
Key Questions Addressed: {KEY_QUESTIONS}

Structure the summary as:
1. Expert Credentials and Background
2. Industry Landscape Assessment
3. Company-Specific Insights
4. Competitive Positioning Analysis
5. Technology and Innovation Outlook
6. Key Risks and Opportunities
7. Long-term Perspective (5-10 years)

Include specific expert quotes about:
- {COMPANY_NAME}''s competitive advantages
- Technology moat assessment
- Market dynamics and growth potential
- Regulatory and competitive risks

Apply SAM''s "unusual thinking" lens - surface contrarian or non-consensus views that could inform patient capital investment decisions.

Tone: Professional interview summary, analytical, forward-looking
Length: 1000-1400 words with verbatim expert quotes throughout', 
'expert-analytical', 1000, 1400, 'Expert network insights, contrarian views, SAM unusual thinking', 'medium', TRUE, NULL),

-- Patent Analysis for competitive advantage assessment
('patent_analysis_001', 'PatentAnalysis',
'Generate a detailed patent landscape analysis for {COMPANY_NAME} as of {DOC_DATE}, focusing on competitive moat assessment.

Analysis Scope: {TECHNOLOGY_AREAS}
Competitive Set: {COMPETITORS}
Time Period: {ANALYSIS_PERIOD}

Structure the analysis as:
1. Executive Summary of Patent Position
2. Core Technology Patent Portfolio
3. Patent Filing Trends and R&D Investment Correlation
4. Competitive Patent Landscape Comparison
5. Freedom to Operate Assessment
6. Defensive vs. Offensive Patent Strategy
7. Long-term Innovation Pipeline Indicators

Include specific analysis of:
- Patent quality and citation strength
- Technology moat defensibility
- R&D efficiency (patents per R&D dollar)
- Competitive threats and white space opportunities

Frame analysis for long-term investors: How does this patent position support a 5-10 year investment thesis?

Tone: Technical but accessible to investment professionals
Length: 1200-1600 words with specific patent examples and competitive comparisons', 
'technical-investment', 1200, 1600, 'Patent moat analysis, competitive advantage, long-term defensibility', 'medium', TRUE, NULL),

-- Internal Debate Summaries for PM thesis evolution
('debate_summary_001', 'InternalDebateSummary',
'Generate an internal investment committee debate summary for {COMPANY_NAME} investment decision on {DOC_DATE}.

Debate Context: {DEBATE_CONTEXT}
Key Participants: {PARTICIPANTS}
Decision Point: {INVESTMENT_DECISION}
Market Context: {MARKET_CONDITIONS}

Structure the debate summary as:
1. Investment Proposal Overview
2. Bull Case Arguments (with supporting data)
3. Bear Case Arguments (with risk factors)
4. Key Points of Contention
5. Management Assessment Discussion
6. Valuation Debate and Methodology
7. Final Decision and Rationale
8. Dissenting Views and Concerns

Capture the intellectual rigor of SAM''s debate process:
- Focus on 5-10 year thesis sustainability
- Emphasize "unusual thinking" and contrarian perspectives
- Document conviction levels and risk tolerance
- Include specific quotes from team members

Ensure debate reflects SAM''s patient capital philosophy and commitment to supporting exceptional growth companies through volatility.

Tone: Internal analytical discussion, intellectually rigorous
Length: 1000-1300 words with direct quotes from debate participants', 
'internal-debate', 1000, 1300, 'Investment committee process, SAM debate culture, thesis validation', 'medium', TRUE, NULL),

-- Approved Marketing Content for client communications
('marketing_content_001', 'MarketingContent',
'Generate approved marketing content for Snowcap Asset Management reflecting our core investment philosophy.

Topic: {TOPIC}
Audience: {AUDIENCE}
Key Message Focus: {MESSAGE_FOCUS}
Content Type: {CONTENT_TYPE}

Core Philosophy Elements to Include:
- "Actual Investor" approach and long-term partnership
- "Patient capital" methodology and decades-focused thinking
- "Unusual thinking" and contrarian investment approach
- Focus on "exceptional growth companies" and outliers
- Commitment to bottom-up fundamental research

Content should address:
- Why long-term thinking creates sustainable returns
- How our partnership structure enables patient capital
- The value of intellectual independence and diverse perspectives
- Our approach to supporting companies through growth cycles
- Alignment with client values and investment objectives

Tone Variations by Audience:
- Institutional: Professional, sophisticated, performance-focused
- Individual: Accessible, value-oriented, relationship-focused
- Regulatory: Compliant, transparent, process-oriented

Length: 300-500 words per content piece
Format: Modular paragraphs for flexible client communication assembly', 
'marketing-professional', 300, 500, 'SAM philosophy, approved language, client communications', 'medium', TRUE, NULL);

-- ===================================================================
-- PROMPT INPUTS FOR DOCUMENT GENERATION
-- ===================================================================

INSERT INTO PROMPT_INPUTS VALUES
-- Basic research notes for Phase 1A companies
('run_001', 'research_note_001', 'Tempus AI', '2024-11-15', '2024Q3', 
 'Internal Research Team', 'Medical AI, genomics, drug discovery', 
 'a leading medical AI company building proprietary datasets for drug discovery and precision medicine',
 'comprehensive', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

-- Framework scaffolding for Tempus AI
('run_001a', 'framework_scaffold_001', 'Tempus AI', '2024-12-01', '2024Q4',
 'Research Analyst Team', 'Questions 3-5: Scale, competitive advantage, management quality',
 'framework analysis focusing on opportunity scale, competitive moat, and leadership assessment for patient capital investment',
 'framework_q3_q5', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

('run_002', 'earnings_transcript_001', 'Tempus AI', '2024-11-01', '2024Q3',
 'CEO, CFO, Analysts', 'Q3 results, AI model performance, data partnerships',
 'strong quarter with breakthrough in multimodal AI models for genomics analysis',
 'latest', 'TXT', 'EARNINGS_CALL_TRANSCRIPTS', 'llama3.1-8b'),

('run_003', 'research_note_001', 'NorthernCell Energy', '2024-10-20', '2024Q3',
 'Internal Research Team', 'Solid-state batteries, EV supply chain, energy storage',
 'a pioneering solid-state battery manufacturer targeting the EV and grid storage markets',
 'comprehensive', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

-- Voltaic Dynamics research documents for Client Manager scenarios (CRITICAL FOR DEMO)
('run_004', 'research_note_001', 'Voltaic Dynamics', '2024-09-15', '2024Q3',
 'Internal Research Team', 'EV supply chain, battery management, energy transition, ESG alignment',
 'a critical EV supply chain player specializing in battery management systems and charging infrastructure, positioned at the center of the energy transition',
 'comprehensive', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

('run_005', 'earnings_transcript_001', 'Voltaic Dynamics', '2024-11-08', '2024Q3',
 'CEO, CFO, Analysts', 'Q3 results, energy transition positioning, supply chain resilience, R&D investment',
 'strong quarter with 59% revenue growth driven by EV supply chain demand and energy transition tailwinds',
 'latest', 'TXT', 'EARNINGS_CALL_TRANSCRIPTS', 'llama3.1-8b'),

-- Historical thesis documents for PM evolution demo (2019 vs 2022)
('run_101', 'thesis_historical_001', 'Arkadia Commerce', '2019-06-15', '2019Q2',
 'Investment Committee', 'E-commerce growth, platform economics, vs Amazon competition',
 'our initial investment in this emerging e-commerce platform', 'comprehensive', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_102', 'thesis_historical_001', 'Arkadia Commerce', '2022-09-20', '2022Q3', 
 'Investment Committee', 'Platform maturation, AWS competition, international expansion',
 'our evolved thinking on this now-established platform player', 'updated', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_103', 'thesis_historical_001', 'Arkadia Commerce', '2020-12-10', '2020Q4', 
 'Investment Committee', 'COVID impact, platform growth, competitive dynamics',
 'our investment thesis during the pandemic-driven e-commerce boom', 'covid_update', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_104', 'thesis_historical_001', 'Arkadia Commerce', '2021-08-15', '2021Q3', 
 'Investment Committee', 'Post-pandemic normalization, AWS competition, growth sustainability',
 'our thesis as markets normalized and competition intensified', 'normalization', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

-- Meeting notes for corporate memory
('run_105', 'meeting_notes_001', 'Arkadia Commerce', '2022-03-18', '2022Q1',
 'SAM PM Team, Arkadia CEO, CTO', 'Strategic planning session',
 'AWS competition, international strategy, AI capabilities', 'internal_notes', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_106', 'meeting_notes_001', 'Arkadia Commerce', '2021-11-22', '2021Q4',
 'SAM PM Team, Arkadia CEO, CFO', 'Annual strategy review',
 'Platform monetization, competition response, long-term vision', 'annual_review', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_107', 'meeting_notes_001', 'Arkadia Commerce', '2020-09-14', '2020Q3',
 'SAM Investment Team, Arkadia Leadership', 'Mid-pandemic strategy check',
 'COVID impact, accelerated digital adoption, capacity planning', 'pandemic_review', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_108', 'meeting_notes_001', 'Arkadia Commerce', '2019-12-05', '2019Q4',
 'SAM PM Team, Arkadia Founders', 'Initial investment discussion',
 'Platform vision, competitive moat, scaling strategy vs Amazon', 'initial_meeting', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

-- Voltaic Dynamics for pre-mortem scenario
('run_201', 'thesis_historical_001', 'Voltaic Dynamics', '2021-11-10', '2021Q4',
 'Research Team', 'EV supply chain, battery technology, supply chain risks',
 'our investment in this critical EV supply chain player', 'comprehensive', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_202', 'thesis_historical_001', 'Voltaic Dynamics', '2023-05-20', '2023Q2',
 'Investment Committee', 'Supply chain resilience, EV market growth, technology evolution',
 'our updated thesis on EV supply chain dynamics', 'updated', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_203', 'thesis_historical_001', 'Voltaic Dynamics', '2022-08-15', '2022Q3',
 'Research Team', 'Geopolitical risks, supply chain diversification, technology roadmap', 
 'our thesis amid global supply chain disruptions', 'disruption_era', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_204', 'thesis_historical_001', 'Voltaic Dynamics', '2024-02-28', '2024Q1',
 'Investment Committee', 'Market consolidation, pricing pressure, innovation pipeline',
 'our current thesis in a maturing EV supply chain market', 'maturation', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

-- Client meeting notes for CRM scenarios
('run_301', 'client_meeting_001', 'Scottish Pension Trust', '2024-11-15', '2024Q4',
 'SAM Client Team, SPT Investment Committee', 'Quarterly portfolio review', 
 'Voltaic Dynamics, NorthernCell Energy, Arkadia Commerce', 'quarterly_review', 'TXT', 'CLIENT_MEETING_ARCHIVE', 'llama3.1-8b'),

('run_302', 'client_meeting_001', 'Scottish Pension Trust', '2024-08-20', '2024Q3',
 'SAM Client Team, SPT CIO', 'Mid-year performance review', 
 'Energy transition progress, ESG alignment, performance attribution', 'mid_year', 'TXT', 'CLIENT_MEETING_ARCHIVE', 'llama3.1-8b'),

('run_303', 'client_meeting_001', 'Scottish Pension Trust', '2024-05-10', '2024Q2',
 'SAM PM Team, SPT Investment Committee', 'Strategy alignment meeting', 
 'Long-term energy transition strategy, portfolio positioning', 'strategy_session', 'TXT', 'CLIENT_MEETING_ARCHIVE', 'llama3.1-8b'),

('run_304', 'client_meeting_001', 'Scottish Pension Trust', '2024-02-15', '2024Q1',
 'SAM Client Relations, SPT Board', 'Annual planning session', 
 'Annual objectives, ESG integration, risk management', 'annual_planning', 'TXT', 'CLIENT_MEETING_ARCHIVE', 'llama3.1-8b'),

-- ===================================================================
-- P1 ENHANCEMENT: ADDITIONAL SYNTHETIC DOCUMENTS
-- ===================================================================

-- Expert Network Interviews for Research Analyst scenarios
('run_401', 'expert_interview_001', 'Tempus AI', '2024-10-15', '2024Q3',
 'Healthcare AI Expert, Former Pharma Executive', 'Medical AI competitive landscape, drug discovery automation, genomics data advantages',
 'industry expert perspective on medical AI competitive landscape and Tempus positioning vs traditional pharma R&D',
 'expert_insight', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

('run_402', 'expert_interview_001', 'Tempus AI', '2024-11-20', '2024Q4',
 'Former CTO of Major Biotech, AI/ML Specialist', 'AI model development, data moats, technology scalability',
 'technical expert assessment of Tempus AI technology moat and long-term defensibility in precision medicine',
 'technical_expert', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

-- Patent Analysis for competitive advantage assessment
('run_403', 'patent_analysis_001', 'Tempus AI', '2024-09-20', '2024Q3',
 'Patent Research Team, IP Strategy Consultants', 'AI genomics patents, drug discovery algorithms, data processing IP',
 'comprehensive analysis of Tempus AI patent portfolio and competitive IP landscape vs major pharma and biotech',
 'ip_analysis', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

('run_404', 'patent_analysis_001', 'NorthernCell Energy', '2024-08-15', '2024Q3',
 'Clean Tech Patent Analysts', 'Solid-state battery technology, manufacturing processes, energy density improvements',
 'patent landscape analysis for solid-state battery technology competitive positioning and freedom to operate',
 'battery_ip', 'TXT', 'INTERNAL_RESEARCH_NOTES', 'llama3.1-8b'),

-- Internal Debate Summaries for PM thesis evolution scenarios
('run_405', 'debate_summary_001', 'Arkadia Commerce', '2021-03-15', '2021Q1',
 'Investment Committee: PM Lead, Research Analyst, Risk Officer', 'COVID recovery investment decision',
 'internal debate on Arkadia investment thesis during COVID recovery: platform acceleration vs Amazon competition',
 'covid_debate', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_406', 'debate_summary_001', 'Arkadia Commerce', '2019-08-10', '2019Q3',
 'Investment Committee: Portfolio Managers, Senior Analysts', 'Initial investment decision',
 'original investment committee debate on Arkadia vs Amazon: platform economics and long-term defensibility assessment',
 'initial_debate', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

('run_407', 'debate_summary_001', 'Voltaic Dynamics', '2023-01-25', '2023Q1',
 'Investment Team: PM, ESG Analyst, Supply Chain Expert', 'Position sizing during supply chain crisis',
 'internal debate on Voltaic Dynamics position sizing amid global supply chain disruptions and EV market volatility',
 'supply_chain_debate', 'TXT', 'CORPORATE_MEMORY_ARCHIVE', 'llama3.1-8b'),

-- Approved Marketing Content for client communications
('run_501', 'marketing_content_001', 'Patient Capital Philosophy', '2024-11-01', '2024Q4',
 'Marketing Team, Investment Philosophy Committee', 'Long-term investment approach, patient capital benefits',
 'approved marketing content explaining SAM patient capital approach and long-term value creation methodology',
 'philosophy_content', 'TXT', 'APPROVED_MARKETING_CONTENT', 'llama3.1-8b'),

('run_502', 'marketing_content_001', 'Unusual Thinking Approach', '2024-10-20', '2024Q4',
 'Investment Team, Client Relations', 'Contrarian investing, intellectual independence, diverse perspectives',
 'approved content on SAM unusual thinking philosophy and how intellectual independence creates investment opportunities',
 'contrarian_content', 'TXT', 'APPROVED_MARKETING_CONTENT', 'llama3.1-8b'),

('run_503', 'marketing_content_001', 'ESG Integration', '2024-12-01', '2024Q4',
 'ESG Team, Client Relations', 'Sustainable investing, long-term value creation, stakeholder alignment',
 'approved ESG messaging for sustainability-focused clients emphasizing patient capital approach to ESG integration',
 'esg_content', 'TXT', 'APPROVED_MARKETING_CONTENT', 'llama3.1-8b');

-- ===================================================================
-- VERIFICATION QUERIES
-- ===================================================================

SELECT 'Company Financials Count' as check_type, COUNT(*) as count FROM COMPANY_FINANCIALS
UNION ALL
SELECT 'Companies Total', COUNT(DISTINCT COMPANY_NAME) FROM COMPANY_FINANCIALS  
UNION ALL
SELECT 'Clients Total', COUNT(*) FROM CLIENT_CRM
UNION ALL
SELECT 'Portfolio Holdings', COUNT(*) FROM PORTFOLIO_HOLDINGS_HISTORY
UNION ALL
SELECT 'Prompt Templates Count', COUNT(*) FROM PROMPT_LIBRARY  
UNION ALL
SELECT 'Prompt Inputs Count', COUNT(*) FROM PROMPT_INPUTS;
