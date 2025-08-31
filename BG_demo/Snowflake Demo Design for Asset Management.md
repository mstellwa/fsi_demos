My prompt: 
I am a sales engineer at Snowflake. My goal is to make an excellent demo to an asset management company. You have three tasks.

1) Review the attached BG Demo Outline document and the additional info I give you and search the internet for further info that would help.

2). Ask me 10 to 20 good questions that will help you finish a great design for a demo.

3). After I respond to those, you will then create a functional requirements document and also a high level technical design.

I would like to do a demo of Snowflake Intelligence, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence, based on the information in the attached document, BG Demo Outline. Since the demo is using Snowflake Intelligence there is no need for creating a GUI, but the focus is to generate realistic data that support the scenarios. The data should be generated using Python, Snowflake Snowpark for Python, https://docs.snowflake.com/en/developer-guide/snowpark/python/index, and for generating unstructured data it will use the COMPLETE function, https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete , using Snowflake Cortex for Python, https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/index-cortex. The demo will run in my Snowflake demo account and there is no need for implementing RBAC or other type of security (polices etc) since the same user will run all scenarios. The scenarios should be separate Agents, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent.

Please ask any questions which will help you better carry out this request and again, I want you to ask me questions to help shape a great design for a demo.

Response:
# **Snowflake Intelligence for Asset Management: A Technical and Strategic Blueprint**

## **Part I: The Strategic Narrative: From Corporate Memory to Actionable Intelligence**

### **1.1 The Asset Manager's Dilemma: A Crisis of Complexity and Margin Compression**

The modern asset management industry operates at the confluence of several powerful and disruptive forces, creating an environment of unprecedented complexity and sustained pressure on profitability. Firms are navigating a landscape defined by intense market volatility, where unforeseen economic shocks and geopolitical events can dramatically alter investment theses in a matter of hours.1 This requires a level of organizational agility that legacy systems and siloed workflows were never designed to support.

Compounding this challenge is a data deluge of staggering proportions. Asset managers are inundated with information from a vast and growing number of disparate sources. While structured market and financial data have long been the industry's lifeblood, the exponential growth of unstructured data—news articles, regulatory filings, earnings call transcripts, expert network interviews, and decades of internal research notes—presents both a monumental opportunity and a critical operational bottleneck.3 More than half of financial firms report struggling with data errors, timeliness, and the integration of these disparate sources, which hinders their ability to make informed decisions.5

Simultaneously, the regulatory environment has become increasingly stringent and complex. Evolving global requirements for transparency, data security, and reporting place a significant and costly compliance burden on firms, diverting critical resources and time away from core investment research and portfolio management activities.1 This operational friction is exacerbated by a fundamental shift in client expectations. Today's investors demand hyper-personalized communication, greater transparency into the investment process, and alignment with their personal values, such as Environmental, Social, and Governance (ESG) criteria. Meeting these demands at scale with traditional, manual processes is a significant challenge.2

These external and internal pressures converge on the industry's bottom line, creating significant and persistent margin compression. In this environment, incremental improvements are no longer sufficient. Firms require a transformational leap in efficiency and effectiveness. Analysis indicates that the strategic application of artificial intelligence (AI) represents such an opportunity, with the potential to unlock value equivalent to 25 to 40 percent of a typical asset manager's cost base.7

The core of the asset manager's dilemma, however, is more profound than these individual pressures. The daily workflow of every investment professional, from the junior research analyst to the senior portfolio manager, is dominated by the consumption and synthesis of unstructured text.8 This vast corpus of documents, emails, and notes constitutes the firm's "Corporate Memory"—the collective institutional wisdom and the qualitative "why" behind every investment decision ever made. The fundamental problem is that this priceless intellectual property is trapped. It resides in formats and systems that are not easily queryable, preventing the firm from accessing, connecting, and leveraging its own historical experience at scale. The true bottleneck to generating alpha and managing risk in the 21st century is not the lack of information, but the inability to intelligently interrogate this trapped institutional wisdom.

### **1.2 The Snowflake Intelligence Vision: Activating the Corporate Memory**

The solution to this crisis of complexity lies in transforming the firm's fragmented data landscape into a single, intelligent, and secure "Corporate Memory." This is the central vision enabled by Snowflake Intelligence. The foundation of this vision is a unified data platform where all of the firm's data—structured financial tables, unstructured research PDFs, semi-structured CRM notes, and market data feeds—resides and is governed within Snowflake's secure perimeter.11 This act of consolidation breaks down the data silos that have historically plagued the industry, creating a single source of truth for the entire organization.

Built upon this unified data layer, Snowflake Intelligence provides a suite of powerful capabilities, including Cortex Agents, Cortex Search, and Cortex Analyst, that allow users to interact with the entirety of this Corporate Memory using conversational, natural language.12 This fundamentally changes the human-to-data relationship. Instead of requiring users to know which system to log into, which table to query with SQL, or which folder to search for a specific document, it provides a single, intuitive interface to ask complex questions that span the full breadth of the firm's knowledge. This approach directly addresses the industry's need for a solution that does not merely store and manage data, but one that makes that data

*intelligent*, *discoverable*, and *actionable*. It transforms data from a passive liability—something that costs money to store and secure—into the firm's most valuable active asset, a primary source of alpha, efficiency, and competitive differentiation.7

This transformation has profound implications for an asset manager's competitive position. An investment firm's most unique and defensible intellectual property is its collective experience, its history of research, and its internal debates. While any competitor can subscribe to the same market data feeds or read the same public filings, no one can replicate two decades of a firm's proprietary meeting notes, investment committee summaries, and evolving research theses. By activating this Corporate Memory with AI, Snowflake enables the firm to leverage its own history as a strategic weapon against market uncertainty and competitors. The ability to ask, "What were the key risks we debated when we first invested in this company five years ago?" and receive an instant, synthesized answer is a game-changing capability. The demonstration of Snowflake Intelligence is therefore not merely a showcase of new features; it is the presentation of a new paradigm for building a durable, knowledge-based competitive moat in an industry where traditional advantages are rapidly eroding.

## **Part II: Persona-Driven Intelligence: Architecting the User Experience**

### **2.1 Scenario 1: The Research Analyst's 'Curiosity Co-Pilot'**

The 'Curiosity Co-Pilot' agent is designed to be an indispensable partner for the Research Analyst, dramatically accelerating the "time-to-insight" and augmenting their analytical capabilities. The daily life of an analyst is a relentless cycle of information gathering, model updating, and synthesis, especially during the high-pressure environment of earnings season.8 This agent is engineered to streamline these core workflows, freeing the analyst to focus on higher-value critical thinking.

**Functional Requirements:**

* **Conversational Onboarding:** A primary challenge for any analyst, whether new to the firm or just new to a specific company, is rapidly getting up to speed on the existing body of internal knowledge. The agent must handle broad, open-ended queries that mimic how a person would ask a colleague for information. For example, a prompt such as, "Give me a high-level summary of Snowcap Global Investments' current investment thesis on Tempus AI, a private company in our portfolio," must trigger a seamless workflow. The agent will use Cortex Search to perform a semantic query across the INTERNAL\_RESEARCH\_NOTES document collection, identify the most recent and relevant comprehensive report, and then pass its content to the AI\_SUMMARIZE\_AGG function to present a concise, narrative summary of the long-term investment case.11 This capability directly replaces hours of manual searching and reading.  
* **Framework-Driven Research:** Elite asset management firms pride themselves on a disciplined and repeatable research process, often codified in a proprietary framework like the "10-Question Stock Research Framework" mentioned in the demo outline. The agent must be able to support and enforce this methodology. When prompted to, "Scaffold a new research note for Tempus AI using our 10-Question Framework. Start by answering: 'What is the scale of the opportunity?' and 'What is the company's sustainable competitive advantage?'", the agent must intelligently decompose the request. It will orchestrate targeted searches for each component: using Cortex Search on EXPERT\_NETWORK\_INTERVIEWS and NEWS\_ARTICLES to synthesize market sizing information for the "scale of opportunity," while simultaneously querying PATENT\_FILINGS and using EXTRACT\_ANSWER on EARNINGS\_CALL\_TRANSCRIPTS to identify technological moats and specific quotes about proprietary data sets for the "competitive advantage" section.11 This ensures research is not only faster but also more rigorous and consistent with firm-wide best practices.  
* **Hybrid Data Synthesis:** An analyst's work constantly bridges the quantitative and qualitative worlds; they live in both spreadsheets and text documents.9 The agent must reflect this reality by seamlessly combining analysis of structured and unstructured data within a single, unified response. A query like, "What was Tempus AI's R\&D spend over the last 8 quarters, and what is the sentiment from their latest earnings call regarding their AI model development?" requires sophisticated orchestration. The agent must recognize the two distinct parts of the query. It will deploy Cortex Analyst to generate and execute a precise SQL query against the  
  COMPANY\_FINANCIALS table to retrieve the R\&D figures. In parallel, it will use Cortex Search to locate the relevant Q\&A section in the latest EARNINGS\_CALL\_TRANSCRIPTS and apply the AI\_SENTIMENT function to it, returning a sentiment score and a summary of key phrases. The final output will present both the structured data table and the qualitative sentiment analysis together, providing a holistic view that mirrors the analyst's own thought process.11

The cumulative effect of these functions is to reposition the AI agent not merely as a data retrieval tool, but as a "Chief of Staff" for the analyst. The daily reality for an analyst involves constant and fatiguing context-switching between disparate tasks: reading news, updating financial models, listening to conference calls, and preparing notes for meetings.10 The 'Curiosity Co-Pilot' absorbs the cognitive load associated with the "grunt work" of finding, extracting, summarizing, and collating this information. By automating these foundational steps, the agent preserves the analyst's most valuable and finite resource: their mental bandwidth. This allows them to dedicate more time and energy to the tasks that truly generate alpha: forming a differentiated viewpoint, stress-testing assumptions, and effectively communicating their conclusions to portfolio managers. The value proposition, therefore, transcends speed; it is about elevating the quality, depth, and impact of the firm's human analytical talent.

### **2.2 Scenario 2: The Portfolio Manager's 'Conviction Engine'**

The 'Conviction Engine' agent is conceived as a strategic sparring partner for the Portfolio Manager (PM), the ultimate decision-maker responsible for capital allocation. In a world of market volatility and information overload, a PM's greatest challenges are managing risk, overcoming behavioral biases, and making high-stakes decisions with confidence and discipline.5 This agent is designed to provide historical context, challenge assumptions, and institutionalize a rigorous decision-making process, especially during periods of stress when a high-conviction holding is underperforming.

**Functional Requirements:**

* **Historical Context Retrieval:** Before making a decision to buy more, sell, or hold a volatile position, a prudent PM must understand the firm's complete history with that investment. The agent must be capable of performing complex, time-bound semantic searches across the entire CORPORATE\_MEMORY\_ARCHIVE. A prompt like, "Show me our original investment thesis for Shopify when we first invested in 2016\. What were the key risks identified by the team in the initial debate?" should trigger a precise action. The agent will use Cortex Search with a date filter to retrieve the specific 2016 Research\_Notes and Internal\_Debate\_Summaries related to "Shopify." It will then leverage the EXTRACT\_ANSWER function to pull the verbatim "Risks" section from the research note and the key counterarguments from the debate summary, presenting them as a consolidated, easy-to-digest brief.11 This provides instant access to the foundational thinking behind a multi-year investment.  
* **Thesis Evolution Tracking:** An investment thesis is not static; it evolves as new information becomes available and the competitive landscape shifts. The agent must empower the PM to trace this evolution. A sophisticated query such as, "Track the evolution of our thinking on Shopify's competitive moat against Amazon. Summarize the key points from our management meeting notes with their CEO in 2019 and 2022," requires the agent to perform a multi-faceted semantic search across the CORPORATE\_MEMORY\_ARCHIVE for documents containing the concepts "Shopify," "moat," and "Amazon." It will specifically target Management\_Meeting\_Notes from the specified years, use AI\_SUMMARIZE\_AGG to condense the relevant sections, and present a comparative summary. This allows the PM to see exactly how the firm's conviction was reinforced or challenged over time through direct interactions with company leadership.11  
* **Systematic Pre-Mortem Analysis:** This represents the agent's most advanced and strategically vital capability. It is a tool designed to proactively combat confirmation bias and institutionalize learning from past mistakes. When the PM, considering adding to the position, asks, "Generate a 'pre-mortem' analysis. Based on our firm's historical investment mistakes documented in the archive, what are the top three plausible reasons our Shopify thesis could be wrong over the next five years?", the agent initiates a powerful multi-step workflow. First, it searches the archive for documents tagged as "investment post-mortems" or containing phrases like "thesis failure." Second, it uses the AI\_CLASSIFY function to categorize the root causes of these past failures into a predefined taxonomy (e.g., "disruptive technology," "management failure," "margin compression"). Third, it takes these failure categories and performs a new search for current internal and external data related to Shopify that matches these historical risk patterns. Finally, it synthesizes these findings into a concise report outlining the most potent potential risks, grounded not in generic market fears, but in the firm's own painful historical experience.11

The 'Conviction Engine,' particularly through its pre-mortem feature, transcends the role of a productivity tool and becomes a critical component of the firm's governance and risk management framework. Portfolio managers are constantly under pressure to deliver performance, which can lead to well-documented behavioral biases such as "style drift," the tendency to chase hot trends, or the emotional difficulty of selling a losing position.1 This agent acts as a disciplined, unemotional, and systematic check on those biases. By grounding its risk analysis in the firm's

*own* historical mistakes, it forces an objective and deeply relevant review of the current investment thesis. This provides an auditable, systematic process for the PM to demonstrate that they are actively challenging their own assumptions, which is a cornerstone of their fiduciary duty to clients. This capability elevates the demonstration from showcasing a "nice-to-have" analytical aid to a "must-have" platform for institutional-grade decision-making and risk oversight.

### **2.3 Scenario 3: The Client Relationship Manager's 'Personalization & Narrative Suite'**

The 'Personalization & Narrative Suite' agent is designed to revolutionize the client service function, transforming it from a traditionally reactive and time-consuming support role into a proactive, scalable, and high-value client engagement engine. The modern Client Relationship Manager (CRM) is tasked with building deep, trust-based relationships, a process that requires extensive preparation, personalized communication, and rapid, context-aware responsiveness—all of which are difficult to scale across a large client base.19 This agent automates the most labor-intensive aspects of this work, enabling a higher standard of service for all clients.

**Functional Requirements:**

* **Automated Meeting Preparation:** A significant portion of a CRM's time is spent preparing for client meetings.22 The agent must automate this process entirely. On a simple prompt like, "Generate a one-page meeting brief for my call with the 'Scottish Pension Trust'," the agent will orchestrate a multi-tool workflow. It will first use Cortex Analyst to query the  
  CLIENT\_PORTFOLIOS and CLIENT\_CRM tables to retrieve the client's top holdings, recent performance data, and the notes from their last call. Concurrently, it will use Cortex Search to find the latest INTERNAL\_RESEARCH\_NOTES for the top three holdings. It will then employ AI\_SUMMARIZE\_AGG to distill the core investment thesis for each of these holdings into two or three key bullet points. Finally, it will assemble all of this disparate information into a single, structured, and professionally formatted briefing document, ready for the CRM's review.11  
* **Personalized Narrative Generation:** This function showcases the agent's advanced generative capabilities, moving beyond data retrieval to sophisticated content creation. A CRM tasked with drafting a quarterly report might prompt: "Draft a personalized commentary for the Scottish Pension Trust's report. Focus on their holding in Voltaic Dynamics. Explain why we remain a patient investor, connecting it to their stated interest in the energy transition. Use the language from our official 'Actual Investor' philosophy documents." This triggers a complex synthesis process. The agent will: 1\) Query the CLIENT\_CRM table to retrieve the client's specific stated interest in "sustainable energy." 2\) Use Cortex Search to access the INTERNAL\_RESEARCH\_NOTES for the detailed Voltaic Dynamics investment thesis. 3\) Use a separate Cortex Search instance to find approved language from the APPROVED\_MARKETING\_CONTENT corpus that reflects the firm's investment philosophy. 4\) Finally, it will feed these three distinct sources of information as context into a sophisticated prompt for the Cortex COMPLETE function 24, which will weave them together into a coherent, personalized narrative that explains the investment in a way that resonates deeply with the client's specific values and interests.11  
* **Rapid, Context-Aware Response:** Clients often react to breaking news and market volatility, requiring timely and reassuring communication. When a client emails with a question about negative headlines, the CRM can use the agent for immediate support. A prompt such as, "A client is asking about recent negative headlines regarding supply chain issues for EV battery makers. Draft a response that acknowledges the short-term challenge but reiterates our long-term conviction in Voltaic Dynamics, based on our internal research," allows for a swift and well-informed reply. The agent will use Cortex Search to find internal research that specifically discusses supply chain risks for Voltaic Dynamics, demonstrating foresight. It will then use Cortex COMPLETE to draft a response that directly addresses the client's concern but masterfully frames it within the context of the firm's multi-decade investment horizon, reinforcing the patient, long-term philosophy that underpins the client relationship.11

These capabilities have a profound business implication: the democratization of "private banking" level service. The primary constraint in client relationship management has always been the scalability of high-touch, personalized interaction.21 This agent effectively breaks that constraint. By automating the most time-intensive aspects of personalization—research, data gathering, and initial drafting—it empowers a single CRM to deliver a superior, bespoke experience to a much larger book of business. This is not merely a client satisfaction initiative; it is a powerful business growth and asset retention strategy. Clients who feel understood, who receive proactive and personalized communication, are significantly less likely to churn during market downturns and are more likely to consolidate their assets with the firm. This creates a virtuous cycle, or a flywheel effect: superior service leads to higher client retention, which leads to a more stable and growing asset base (AUM), which in turn funds further investment in the platform and its capabilities. The demonstration proves that Snowflake Intelligence is the engine that drives this powerful business flywheel.

## **Part III: The Data Foundation: Engineering a Realistic Corporate Universe**

The credibility and impact of the entire demonstration rest upon the foundation of high-fidelity, realistic synthetic data. A generic or simplistic dataset would undermine the sophistication of the AI tools being showcased. Therefore, the engineering of this "corporate universe" is a critical preliminary step, encompassing both structured tables and a rich corpus of unstructured documents.

### **3.1 Structured Data Architecture**

The structured data will be housed in a series of Snowflake tables, designed with realistic schemas, data types, and relational integrity to mimic a production asset management environment. These tables will provide the quantitative backbone for the demonstration scenarios. The schemas are derived directly from the data requirements specified for the Research Analyst, Portfolio Manager, and Client Relationship Manager personas.11

**Key Table Schemas:**

* COMPANY\_FINANCIALS  
  * COMPANY\_ID: INTEGER, Primary Key  
  * TICKER: VARCHAR(10)  
  * COMPANY\_NAME: VARCHAR(255)  
  * REPORT\_DATE: DATE  
  * QUARTER: VARCHAR(10)  
  * REVENUE\_USD\_M: DECIMAL(18, 2\)  
  * NET\_INCOME\_USD\_M: DECIMAL(18, 2\)  
  * R\&D\_SPEND\_USD\_M: DECIMAL(18, 2\)  
  * CASH\_ON\_HAND\_USD\_M: DECIMAL(18, 2\)  
* MARKET\_DATA  
  * TICKER: VARCHAR(10), Primary Key (Composite with TRADE\_DATE)  
  * TRADE\_DATE: DATE, Primary Key (Composite with TICKER)  
  * OPEN\_PRICE: DECIMAL(10, 2\)  
  * HIGH\_PRICE: DECIMAL(10, 2\)  
  * LOW\_PRICE: DECIMAL(10, 2\)  
  * CLOSE\_PRICE: DECIMAL(10, 2\)  
  * VOLUME: BIGINT  
* PORTFOLIO\_HOLDINGS\_HISTORY  
  * TRANSACTION\_ID: VARCHAR(64), Primary Key  
  * PORTFOLIO\_ID: VARCHAR(50)  
  * TRADE\_DATE: DATE  
  * TICKER: VARCHAR(10)  
  * ACTION: VARCHAR(10) (e.g., 'BUY', 'SELL')  
  * SHARES: DECIMAL(18, 4\)  
  * PRICE\_PER\_SHARE: DECIMAL(10, 2\)  
  * RESULTING\_WEIGHT\_PCT: DECIMAL(5, 2\)  
* CLIENT\_CRM  
  * CLIENT\_ID: VARCHAR(50), Primary Key  
  * CLIENT\_NAME: VARCHAR(255)  
  * CLIENT\_TYPE: VARCHAR(50) (e.g., 'Pension Fund', 'Family Office')  
  * AUM\_USD\_M: DECIMAL(18, 2\)  
  * LAST\_CONTACT\_DATE: DATE  
  * STATED\_INTERESTS: VARCHAR(1000) (e.g., 'sustainable energy, risk-averse, long-term growth')  
  * MEETING\_LOGS: VARCHAR(5000)  
* CLIENT\_PORTFOLIOS  
  * PORTFOLIO\_ID: VARCHAR(50), Primary Key  
  * CLIENT\_ID: VARCHAR(50), Foreign Key to CLIENT\_CRM  
  * PERFORMANCE\_YTD\_PCT: DECIMAL(5, 2\)  
  * INCEPTION\_DATE: DATE

### **3.2 Unstructured Data Corpus Design**

The unstructured data corpus is designed to represent the firm's intellectual property and the external information landscape. The documents will be stored in a Snowflake internal stage and indexed via a Directory Table. The key to making this corpus useful for Cortex Search is a consistent structure and, most importantly, rich, queryable metadata. This metadata is what enables the precise, filtered searches required by the advanced scenarios, particularly the Portfolio Manager's 'Conviction Engine'.11

**Document Types and Metadata Schema:**

* **INTERNAL\_RESEARCH\_NOTES** (Format: PDF/TXT)  
  * Content: Detailed investment theses, financial models, risk assessments.  
  * Metadata: doc\_id, file\_url, last\_modified, company\_name, author, publish\_date, document\_type: 'ResearchNote', tags: \['equity\_research', 'deep\_dive'\].  
* **EARNINGS\_CALL\_TRANSCRIPTS** (Format: TXT)  
  * Content: Verbatim transcripts of quarterly earnings calls, separated into presentation and Q\&A sections.  
  * Metadata: doc\_id, file\_url, last\_modified, company\_name, quarter, call\_date, document\_type: 'EarningsTranscript'.  
* **APPROVED\_MARKETING\_CONTENT** (Format: TXT)  
  * Content: Pre-approved paragraphs and articles on the firm's investment philosophy, market outlooks, and ethos.  
  * Metadata: doc\_id, file\_url, last\_modified, topic, approval\_date, document\_type: 'MarketingContent'.  
* **CORPORATE\_MEMORY\_ARCHIVE** (A collection of various document types)  
  * **Management\_Meeting\_Notes** (Format: PDF/TXT)  
    * Content: Summaries of meetings between PMs/analysts and company management.  
    * Metadata: doc\_id, file\_url, doc\_date, company\_name, attendees, document\_type: 'MeetingNotes'.  
  * **Internal\_Debate\_Summaries** (Format: TXT)  
    * Content: Notes capturing the bull vs. bear arguments for key investment decisions.  
    * Metadata: doc\_id, file\_url, doc\_date, topic, pro\_argument\_summary, con\_argument\_summary, document\_type: 'DebateSummary'.  
  * **Investment\_Post\_Mortems** (Format: PDF)  
    * Content: Analyses of past investment failures, detailing what went wrong and lessons learned.  
    * Metadata: doc\_id, file\_url, doc\_date, investment\_name, failure\_reason, document\_type: 'PostMortem', tags:.

### **3.3 Data Generation Engine: A Snowpark & Cortex COMPLETE Workflow**

The entire synthetic data universe will be generated programmatically using a unified workflow that leverages Snowpark for Python and Snowflake Cortex AI functions. This approach ensures the data is realistic, internally consistent, and can be easily regenerated or modified.

**Generation Workflow:**

1. **Establish Snowpark Session:** A Python script will initiate a Snowpark session, connecting to the Snowflake account where the demo assets will be created.25  
2. **Generate Structured Data:** The script will use Python libraries like pandas and numpy within Snowpark to generate dataframes for each structured table. For example, it will generate stock prices that follow a geometric Brownian motion to appear realistic, and create company financial statements where metrics like revenue, expenses, and net income are logically correlated. These dataframes will then be written directly to Snowflake tables using dataframe.write.save\_as\_table().  
3. **Generate Unstructured Content with Cortex:** The core of the unstructured data generation lies in prompt engineering and the snowflake.cortex.complete function.24 The script will iterate through a list of fictional companies and key dates. For each, it will construct a detailed prompt and call the Cortex function to generate the text.  
   * **Example Prompt for a Research Note:**  
     Python  
     prompt \= f"""  
     As an expert equity research analyst, write a 500-word investment thesis summary for a fictional medical AI company named 'Tempus AI', dated January 15, 2022\.  
     The tone should be that of a long-term, patient investor: cautiously optimistic.  
     Key points to include:  
     \- Thesis: Tempus AI is building a durable competitive advantage through its proprietary, multi-modal dataset of genomic and clinical trial data.  
     \- Positive: Highlight its strong and growing patent portfolio in using AI for genomic data analysis and drug discovery.  
     \- Risk: Raise concerns about its high quarterly cash burn rate and its current reliance on a single academic partnership for data acquisition.  
     \- Conclusion: Conclude that while near-term risks are present, the long-term potential for disrupting the pharmaceutical R\&D market is significant.  
     """  
     \# response \= snowflake.cortex.complete('mistral-large', prompt)

4. **Stage and Load Data:** The generated text content will be saved as individual .txt or .pdf files. The Python script will then use Snowpark file operation commands (session.file.put()) to upload these files, along with the CSVs for the structured data, to a named internal stage within Snowflake. Finally, COPY INTO commands will be executed to load the structured data, and a CREATE DIRECTORY TABLE command will be used to index the unstructured files.

This generation process is more than a logistical prerequisite; it is a powerful demonstration feature in its own right. By using Snowpark and Cortex to build the demo's data foundation, the presentation can highlight that Snowflake is not just a passive repository for data but an active, programmable Data Cloud. This showcases to the client how they could leverage these exact same tools for their own critical use cases, such as creating high-fidelity, anonymized datasets for back-testing quantitative strategies, training internal machine learning models, or provisioning secure developer sandboxes—all without data ever leaving the governed Snowflake environment. This elevates the "Data Generation Proviso" from a simple disclaimer to a compelling proof point of the platform's versatility and power.

### **Table 1: Master Data Asset Inventory**

| Asset Name | Data Type | Format | Description | Key Fields / Metadata | Used in Scenario(s) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| COMPANY\_FINANCIALS | Structured | Table | Quarterly financial metrics for public and private companies. | TICKER, REPORT\_DATE, REVENUE, R\&D\_SPEND | 1: Research Analyst |
| MARKET\_DATA | Structured | Table | Historical daily stock prices and trading volumes. | TICKER, TRADE\_DATE, CLOSE\_PRICE, VOLUME | 1: Research Analyst |
| PORTFOLIO\_HOLDINGS\_HISTORY | Structured | Table | Historical record of all portfolio transactions and positions. | PORTFOLIO\_ID, TRADE\_DATE, TICKER, ACTION | 2: Portfolio Manager |
| CLIENT\_CRM | Structured | Table | Client information, contact history, and stated preferences. | CLIENT\_ID, CLIENT\_NAME, STATED\_INTERESTS | 3: Client RM |
| CLIENT\_PORTFOLIOS | Structured | Table | Links clients to their portfolios and tracks high-level performance. | CLIENT\_ID, PORTFOLIO\_ID, PERFORMANCE\_YTD | 3: Client RM |
| INTERNAL\_RESEARCH\_NOTES | Unstructured | PDF/TXT | Corpus of all historical investment research notes. | company\_name, publish\_date, author | 1, 3 |
| EARNINGS\_CALL\_TRANSCRIPTS | Unstructured | TXT | Transcripts of quarterly earnings calls for covered companies. | company\_name, call\_date, quarter | 1: Research Analyst |
| EXPERT\_NETWORK\_INTERVIEWS | Unstructured | TXT | Summaries of interviews with industry specialists. | topic, interview\_date, expert\_specialty | 1: Research Analyst |
| NEWS\_ARTICLES | Unstructured | TXT | Collection of recent news articles related to key companies. | source, publish\_date, headline | 1: Research Analyst |
| PATENT\_FILINGS | Unstructured | TXT | Text documents describing patents filed by key companies. | company\_name, filing\_date, patent\_title | 1: Research Analyst |
| CORPORATE\_MEMORY\_ARCHIVE | Unstructured | PDF/TXT | 20-year archive of all internal documents. | doc\_date, document\_type, tags | 2: Portfolio Manager |
| APPROVED\_MARKETING\_CONTENT | Unstructured | TXT | Pre-approved text snippets on firm philosophy. | topic, approval\_date | 3: Client RM |

## **Part IV: The Intelligence Layer: A Blueprint for Cortex Agent Implementation**

The intelligence layer of the demonstration is composed of three distinct Cortex Agents, each tailored to a specific user persona. These agents are not monolithic applications but are configured within Snowflake by defining their purpose, granting them access to a curated set of tools, and providing instructions that guide their decision-making process. This section provides the high-level technical design for their implementation.

### **4.1 Cortex Agent Framework**

The Cortex Agent framework provides the orchestration engine that powers the conversational experience. When a user submits a prompt, the agent's designated orchestration model analyzes the user's intent. Based on this analysis and a set of "planning instructions" provided by the developer, the agent selects the most appropriate tool or sequence of tools to fulfill the request. These tools can include Cortex Search services for querying unstructured data, Cortex Analyst for querying structured data via semantic views, or custom tools like UDFs and Stored Procedures for more specialized tasks.12

Each agent for this demonstration will be created as an object within the snowflake\_intelligence.agents schema. Access will be managed via standard Snowflake role-based access control (RBAC), ensuring that only authorized users can interact with each agent and that all underlying data access adheres to the user's existing permissions.

### **4.2 Agent Design & Tool Configuration**

The effectiveness of each agent is determined by the tools it has access to and the logic that governs how it uses them. The following design specifies the configuration for each of the three persona-driven agents.

**Agent 1: 'Curiosity Co-Pilot' (for the Research Analyst)**

This agent is designed for rapid information retrieval and synthesis from a mix of internal research and structured financial data.

* **Tools:**  
  * **Cortex Search Service 1:**  
    * **Name:** research\_service  
    * **Description:** "A service for performing semantic searches on all internal research documents, including investment notes, earnings call transcripts, expert interviews, and patent filings."  
    * **Underlying Data:** Built on a Directory Table pointing to the staged files for INTERNAL\_RESEARCH\_NOTES, EARNINGS\_CALL\_TRANSCRIPTS, EXPERT\_NETWORK\_INTERVIEWS, NEWS\_ARTICLES, and PATENT\_FILINGS.  
  * **Cortex Analyst Tool 1:**  
    * **Name:** financial\_data\_analyst  
    * **Description:** "A tool for answering questions about company financials and market data by writing and executing SQL queries."  
    * **Underlying Data:** Built on a semantic view that joins the COMPANY\_FINANCIALS and MARKET\_DATA tables.  
* **Orchestration Logic (Planning Instructions):**  
  * "When the user asks about qualitative concepts like 'thesis', 'summary', 'sentiment', 'competitive advantage', 'moat', or 'risks', prioritize using the research\_service tool."  
  * "When the user asks for specific quantitative figures like 'revenue', 'R\&D spend', 'stock price', or 'trading volume', prioritize using the financial\_data\_analyst tool."  
  * "If a user's query contains both qualitative and quantitative elements, use both tools in parallel and combine their outputs into a single, comprehensive answer."

**Agent 2: 'Conviction Engine' (for the Portfolio Manager)**

This agent is a specialized tool for deep, historical analysis and advanced risk assessment, interacting with the firm's entire 20-year knowledge base.

* **Tools:**  
  * **Cortex Search Service 2:**  
    * **Name:** corporate\_memory\_service  
    * **Description:** "A specialized service for searching the firm's complete 20-year archive of all internal documents, including meeting notes, debate summaries, and investment post-mortems."  
    * **Underlying Data:** Built on a Directory Table pointing to the CORPORATE\_MEMORY\_ARCHIVE files. This service's effectiveness is critically dependent on the doc\_date, document\_type, and tags metadata for precise filtering.  
  * **Custom Tool 1 (Function):**  
    * **Name:** classify\_investment\_risks  
    * **Description:** "A function that takes text from past investment post-mortems and classifies the primary reason for failure into one of the following categories: 'disruptive technology', 'management failure', 'margin compression', 'regulatory change', or 'macroeconomic shock'."  
    * **Implementation:** A Python User-Defined Function (UDF) that wraps the SNOWFLAKE.CORTEX.CLASSIFY function, providing it with the predefined list of labels to ensure consistent output.  
* **Orchestration Logic (Planning Instructions):**  
  * "If the user's prompt includes the phrase 'pre-mortem analysis' for a specific company, execute the following multi-step plan:  
    1. Use the corporate\_memory\_service to search for all documents where tags contains 'ThesisFailure'.  
    2. Pass the content of the search results to the classify\_investment\_risks tool to get a list of historical failure reasons.  
    3. For each of the top 3 failure reasons returned, perform a new search using corporate\_memory\_service for documents related to the target company that contain keywords related to that failure reason.  
    4. Synthesize the findings from step 3 into a final summary report."

**Agent 3: 'Personalization & Narrative Suite' (for the Client Relationship Manager)**

This agent is an expert at combining client-specific data with firm-wide knowledge to generate highly personalized communications.

* **Tools:**  
  * **Cortex Analyst Tool 2:**  
    * **Name:** client\_data\_analyst  
    * **Description:** "A tool for retrieving all information about a specific client, including their portfolio holdings, performance, contact history, and stated interests."  
    * **Underlying Data:** Built on a semantic view that joins the CLIENT\_CRM and CLIENT\_PORTFOLIOS tables.  
  * **Cortex Search Service 1 (Re-used):**  
    * **Name:** research\_service  
    * **Description:** "Re-uses the service for searching internal research notes to find the investment thesis behind client holdings."  
  * **Cortex Search Service 3:**  
    * **Name:** marketing\_content\_service  
    * **Description:** "A service for finding approved marketing language and text that describes the firm's official investment philosophy."  
    * **Underlying Data:** Built on a Directory Table pointing to the APPROVED\_MARKETING\_CONTENT files.  
* **Orchestration Logic (Planning Instructions):**  
  * "When asked to generate a meeting brief for a client, use the client\_data\_analyst tool to get their portfolio and CRM data, then use the research\_service to get the theses for their top holdings. Combine all information into a structured summary."  
  * "When asked to draft personalized commentary or a client response, identify the key entities in the prompt (client name, company name, topic). Use the client\_data\_analyst, research\_service, and marketing\_content\_service tools to gather all relevant context. Then, feed the complete context into a final call to the SNOWFLAKE.CORTEX.COMPLETE function to generate the final narrative."

### **Table 2: Cortex Agent Tool & Data Source Mapping**

| Agent Name | Tool Type | Tool Name | Underlying Data Asset(s) | Key Functions Used |
| :---- | :---- | :---- | :---- | :---- |
| **Curiosity Co-Pilot** | Cortex Search | research\_service | INTERNAL\_RESEARCH\_NOTES, EARNINGS\_CALL\_TRANSCRIPTS, etc. | EXTRACT\_ANSWER, AI\_SUMMARIZE\_AGG, AI\_SENTIMENT |
|  | Cortex Analyst | financial\_data\_analyst | COMPANY\_FINANCIALS, MARKET\_DATA | (SQL Generation) |
| **Conviction Engine** | Cortex Search | corporate\_memory\_service | CORPORATE\_MEMORY\_ARCHIVE | EXTRACT\_ANSWER, AI\_SUMMARIZE\_AGG |
|  | Custom (UDF) | classify\_investment\_risks | (Processes output from corporate\_memory\_service) | AI\_CLASSIFY |
| **Personalization & Narrative Suite** | Cortex Analyst | client\_data\_analyst | CLIENT\_CRM, CLIENT\_PORTFOLIOS | (SQL Generation) |
|  | Cortex Search | research\_service | INTERNAL\_RESEARCH\_NOTES | AI\_SUMMARIZE\_AGG |
|  | Cortex Search | marketing\_content\_service | APPROVED\_MARKETING\_CONTENT | (Semantic Search) |
|  | (Implicit) | (Generative Synthesis) | (Processes output from all tools) | Cortex COMPLETE |

## **Part V: Execution and Delivery: A Guide to a Compelling Demonstration**

A technically brilliant demonstration can fail to resonate if its story is not told effectively. The final step in this blueprint is to provide a framework for delivering the demo in a way that translates its powerful capabilities into a compelling and persuasive business narrative. The delivery should focus on connecting every feature back to a core business challenge and a tangible impact.

### **5.1 Weaving the Narrative: From Pain Point to "Wow" Moment**

Each of the three scenarios should be presented using a classic "challenge-solution-impact" framework. This structure grounds the technology in the real-world problems of the audience, making the solution more relevant and its impact more profound. The goal is to build towards a "wow" moment in each scenario, where the audience sees a previously difficult or impossible task performed in seconds.

**Example Narrative Flow for Scenario 2 (The Portfolio Manager's 'Conviction Engine'):**

1. **Challenge (Establish the Pain Point):** The presenter begins by setting a relatable scene. "Imagine you're a portfolio manager. One of your highest-conviction, long-term holdings, Shopify, is down 20% on the year due to fears about competition from Amazon. The pressure is immense. Your clients are calling, and your own conviction is being tested. How do you make the critical decision of whether to double down, hold, or cut your losses? How do you separate the signal from the noise and avoid making an emotional decision?"  
2. **Solution (Introduce the Technology):** The presenter then pivots to the solution. "Instead of relying on gut feel, let's ask the firm's collective wisdom. With the 'Conviction Engine,' the PM can instantly access the firm's entire history with this stock." The presenter then executes the first prompt: "Show me our original investment thesis for Shopify when we first invested in 2016\. What were the key risks identified by the team in the initial debate?" As the answer appears, the presenter narrates: "In seconds, Snowflake has searched a 20-year archive and retrieved not only the original 2016 thesis but also the specific risks the team debated back then. This is the foundational context, available on demand."  
3. **Impact (Deliver the "Wow" Moment):** This is where the demonstration elevates from impressive to strategic. "But having historical context is just the beginning. The real challenge is combating our own biases. Here's where this becomes a strategic weapon for risk management. Let's run a pre-mortem analysis to challenge our own thinking." The presenter executes the advanced prompt: "Generate a 'pre-mortem' analysis. Based on our firm's historical investment mistakes documented in the archive, what are the top three plausible reasons our Shopify thesis could be wrong over the next five years?" As the synthesized report is generated, the presenter delivers the final, impactful message: "Look at what just happened. In the time it took me to ask the question, the agent has analyzed every past investment mistake our firm has ever documented, categorized the root causes like 'margin compression' and 'disruptive technology,' and then found evidence of those *same patterns* in the market today that could negatively impact Shopify. This isn't just data retrieval; this is disciplined, institutionalized wisdom, delivered on demand, acting as a systematic check against repeating the mistakes of the past."

### **5.2 Highlighting Snowflake's Unique Differentiators**

Throughout the demonstration, it is crucial to sprinkle in key talking points that emphasize *why* this transformative experience is uniquely possible on the Snowflake Data Cloud. These points should be woven naturally into the narrative to reinforce the platform's core value propositions.

**Key Differentiator Talking Points:**

* **On Security & Governance:** "It's critical to note that everything we are seeing—the data, the large language models processing the prompts, and the queries themselves—is happening inside Snowflake's secure data perimeter. Your most sensitive intellectual property, your 'Corporate Memory,' never leaves the platform to be processed by an external service. This provides maximum capability with zero compromise on security and governance."  
* **On Seamless Integration:** "In that last response for the analyst, we saw the agent seamlessly query a structured SQL table for financial data, perform a semantic search on a PDF of an earnings call transcript, and then use a generative model to synthesize the results into a single answer. This unified experience across all types of data—structured, semi-structured, and unstructured—is native to Snowflake's architecture and eliminates the complexity and security risks of stitching together multiple point solutions."  
* **On Zero Management & Scalability:** "To build and serve these three distinct AI agents and to query terabytes of historical data, our team did not have to provision a single server, manage a GPU cluster, or configure any complex infrastructure. The platform scales compute resources instantly and independently for each workload, ensuring performance whether it's one analyst running a query or five hundred portfolio managers interacting with their agents simultaneously."  
* **On Programmability & Extensibility:** "And as we alluded to with the data generation process, the entire platform is programmable. Using familiar tools like Python with Snowpark, your teams can go beyond analytics to build not just these types of agents, but full-fledged data applications, custom machine learning models, and secure data-sharing solutions. This isn't just a product; it's a platform for innovation, allowing you to build the next generation of data and AI capabilities tailored to your firm's unique needs."

#### **Works cited**

1. Asset Management Strategy: 5 Key Challenges to Tackle \- CIO Investment Club, accessed August 16, 2025, [https://www.cioinvestmentclub.com/asset-management-strategy](https://www.cioinvestmentclub.com/asset-management-strategy)  
2. Interview: Navigating Challenges and Opportunities for Institutional Asset Managers \- Archer, accessed August 16, 2025, [https://archerims.com/2024/07/interview-navigating-challenges-and-opportunities-for-institutional-asset-managers/](https://archerims.com/2024/07/interview-navigating-challenges-and-opportunities-for-institutional-asset-managers/)  
3. Data science and AI: A guide for investment managers | CFA Institute, accessed August 16, 2025, [https://www.cfainstitute.org/insights/articles/data-science-ai-guide-for-investment-managers](https://www.cfainstitute.org/insights/articles/data-science-ai-guide-for-investment-managers)  
4. NLP in Finance: 6 Real World Applications, accessed August 16, 2025, [https://www.thefinanceweekly.com/post/nlp-in-finance-6-real-world-applications](https://www.thefinanceweekly.com/post/nlp-in-finance-6-real-world-applications)  
5. 7 Critical Asset Management Challenges and Ways to Solve Them \- Proxymity, accessed August 16, 2025, [https://www.proxymity.io/views/critical-asset-management-challenges-and-ways-to-solve-them/](https://www.proxymity.io/views/critical-asset-management-challenges-and-ways-to-solve-them/)  
6. 5 Key Challenges for Emerging Managers and Strategies for Success in a Volatile Market, accessed August 16, 2025, [https://www.citrincooperman.com/In-Focus-Resource-Center/5-Key-Challenges-for-Emerging-Managers-and-Strategies-for-Success-in-a-Volatile-Market](https://www.citrincooperman.com/In-Focus-Resource-Center/5-Key-Challenges-for-Emerging-Managers-and-Strategies-for-Success-in-a-Volatile-Market)  
7. How AI could reshape the economics of the asset management industry \- McKinsey, accessed August 16, 2025, [https://www.mckinsey.com/industries/financial-services/our-insights/how-ai-could-reshape-the-economics-of-the-asset-management-industry](https://www.mckinsey.com/industries/financial-services/our-insights/how-ai-could-reshape-the-economics-of-the-asset-management-industry)  
8. Equity Research Careers: Day in the Life, Salaries Bonuses and Exits, accessed August 16, 2025, [https://mergersandinquisitions.com/equity-research-careers/](https://mergersandinquisitions.com/equity-research-careers/)  
9. A Day in the Life of an Equity Research Analyst \- Investopedia, accessed August 16, 2025, [https://www.investopedia.com/articles/personal-finance/082815/day-life-equity-research-analyst.asp](https://www.investopedia.com/articles/personal-finance/082815/day-life-equity-research-analyst.asp)  
10. A Day in the Life: Investment Research Associate \- Vault, accessed August 16, 2025, [https://vault.com/blogs/day-in-the-life/a-day-in-the-life-investment-research-associate](https://vault.com/blogs/day-in-the-life/a-day-in-the-life-investment-research-associate)  
11. BG Demo Outline  
12. Overview of Snowflake Intelligence | Snowflake Documentation, accessed August 16, 2025, [https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence\#create-an-agent](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent)  
13. Investment Management: How AI is Transforming the Industry \- MDOTM Ltd, accessed August 16, 2025, [https://www.mdotm.ai/blog/revolutionizing-investment-management-how-ai-is-transforming-the-industry](https://www.mdotm.ai/blog/revolutionizing-investment-management-how-ai-is-transforming-the-industry)  
14. Investment companies can use AI responsibly to gain an edge | World Economic Forum, accessed August 16, 2025, [https://www.weforum.org/stories/2025/02/ai-redefine-investment-strategy-generate-value-financial-firms/](https://www.weforum.org/stories/2025/02/ai-redefine-investment-strategy-generate-value-financial-firms/)  
15. Daily Life of a Financial Analyst, accessed August 16, 2025, [https://www.nobledesktop.com/careers/financial-analyst/daily-life](https://www.nobledesktop.com/careers/financial-analyst/daily-life)  
16. A Day in the Life of an Investment Research Analyst \- Financial Edge Training, accessed August 16, 2025, [https://www.fe.training/free-resources/careers-in-finance/a-day-in-the-life-of-an-investment-research-analyst/](https://www.fe.training/free-resources/careers-in-finance/a-day-in-the-life-of-an-investment-research-analyst/)  
17. A Day in the Life Of...An Equity Research Analyst \- AnalystForum, accessed August 16, 2025, [https://www.analystforum.com/t/a-day-in-the-life-of-an-equity-research-analyst/46622](https://www.analystforum.com/t/a-day-in-the-life-of-an-equity-research-analyst/46622)  
18. Portfolio Management: Definition, Types, and Strategies \- Investopedia, accessed August 16, 2025, [https://www.investopedia.com/terms/p/portfoliomanagement.asp](https://www.investopedia.com/terms/p/portfoliomanagement.asp)  
19. Client Relationship Manager Asset Management Recruitment \- Exec Capital, accessed August 16, 2025, [https://www.execcapital.co.uk/client-relationship-manager-asset-management-recruitment/](https://www.execcapital.co.uk/client-relationship-manager-asset-management-recruitment/)  
20. Relationship Manager: Roles and Responsibilities \- Hays, accessed August 16, 2025, [https://www.hays.com.hk/blogs/insights/relationship-manager-roles-and-responsibilities](https://www.hays.com.hk/blogs/insights/relationship-manager-roles-and-responsibilities)  
21. Client Relationship Manager Job Description \- Florida Tech, accessed August 16, 2025, [https://online.fit.edu/degrees/graduate/business/mba/marketing/client-relationship-manager-job-description/](https://online.fit.edu/degrees/graduate/business/mba/marketing/client-relationship-manager-job-description/)  
22. Job offer Asset Management \- Global Client Group \- Client Account Manager, Taiwan, accessed August 16, 2025, [https://group.bnpparibas/en/careers/job-offer/asset-management-global-client-group-client-account-manager-taiwan](https://group.bnpparibas/en/careers/job-offer/asset-management-global-client-group-client-account-manager-taiwan)  
23. Main Responsibilities and Required Skills for Client Relationship Manager \- Spotterful, accessed August 16, 2025, [https://spotterful.com/blog/job-description-template/client-relationship-manager-responsibilities-and-required-skills](https://spotterful.com/blog/job-description-template/client-relationship-manager-responsibilities-and-required-skills)  
24. snowflake.cortex.complete | Snowflake Documentation, accessed August 16, 2025, [https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete)  
25. Snowpark Developer Guide for Python | Snowflake Documentation, accessed August 16, 2025, [https://docs.snowflake.com/en/developer-guide/snowpark/python/index](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)