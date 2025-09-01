
My prompt:
I am a sales engineer at Snowflake. My goal is to build an excellent demo for my investment and holding company customer Investor

You have three tasks.
1). Review the info I give you and search the internet for further info that would help.
2). Ask me 10 to 20 good questions that will help you finish a great design for a demo.
3). After I respond to those, you will then create a functional requirements document and also a high level technical design.

The demo I need to build is a Thematic Research Tool that is a AI-driven research assistant that searches and synthesizes internal & external sources to summarize insights on a topic, helping analysts process more information and reach conclusions faster and the scenario that it will show is “An investment associate is exploring the impact of rising inflation on industrial companies, ahead of a strategy offsite. Traditionally, this kind of thematic research would take days: scouring economic reports, news articles, internal analyses, and expert commentary to piece together insights. With Listed’s AI Thematic Research Tool, the associate enters the query and the AI scours both internal and external sources (incl. from paid-for sources behind paywalls) in parallel. (If desired) It retrieves relevant data from Listed’s own archives (past investment memos, sector reviews) and external sources (central bank reports, industry news feeds) and then synthesizes a concise report. For example, the AI might report: “Industrial producers saw costs increase ~12% during 2022, and many passed on 8–10% via price hikes, preserving margins.”

The following data sources and similar would be used in the scenario:

1. News flow
* Factset (Nyhetsbyrån Direkt etc)
* DI, FT, WSJ
* BT specific news letters (LightReading, Exchange News...)
* Investor relations

2. Expert networks
* Guidepoint
* Thirdbridge

3. External research and data
* Factset (equity research)
* Quartr (transcripts)
* McBainCG + other consultants
* BT specific data providers (Dell'Oro, Clarkson, Euromonitor, Preqin...)

I am going to use Snowflake Intelligence, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence, to showcase this scenario and need to generate the data needed both structured and unstructured and also create instructions on how to set up the Agent, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent, and to create the needed tools, Cortex Analyst and

I need to generate synthesised data that mimics those for my demo.

The data generation should use Python and Snowflake Snowpark for Python Dataframes as much as possible.

The generation of unstructured data should be done using Snowflake Cortex Complete function,https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete, using llama3.1-8b as the default model, and should mimic the unstructured data described in attached picture and scenario. The Flow for generating the unstructured data should generate prompts first, store in a Snowflake table, then use with_column(complete()) and save it in a Snowflake table. It should use Python and Snowflake Snowpark for Python Dataframes as much as possible. Each unstructured data source should be stored in a table of its own to mimic that it is acquired from an external source (which could be via Snowflake Marketplace or a direct share from a data provider).

The scenario will have one Agent that can use any combination of Cortex Analyst, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent-that-uses-a-semantic-view-in-cortex-analyst, and Cortex Search, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent-that-uses-the-cortex-search-service. When creating the instructions to configure an Agent, always split into Response Instructions (how to respond) and Planning Instructions (tool selection), each tool will also need a description that makes it easy for the Agent to understand what and when to use the tool.

For Cortex Analyst we will always use SEMANTIC VIEWS, https://docs.snowflake.com/en/user-guide/views-semantic/overview, and pay attention to how a SEMANTIC VIEW is created with SQL https://docs.snowflake.com/en/user-guide/views-semantic/sql and use proper TABLES (https://docs.snowflake.com/en/user-guide/views-semantic/sql#defining-the-logical-tables), RELATIONSHIPS (https://docs.snowflake.com/en/user-guide/views-semantic/sql#label-semantic-views-create-relationships), FACTS, DIMENSIONS, METRICS (https://docs.snowflake.com/en/user-guide/views-semantic/sql#defining-facts-dimensions-and-metrics) structure. Also always include COMMENT and WITH SYNONYMS for all supported elements. A SEMANTIC VIEW can also be queried using SQL, https://docs.snowflake.com/en/user-guide/views-semantic/querying#basic-examples

For Cortex Search we will always create the service with SQL, https://docs.snowflake.com/sql-reference/sql/create-cortex-search,and see the examples at https://docs.snowflake.com/sql-reference/sql/create-cortex-search#example and we can test it using SQL function SEARCH_PREVIEW, https://docs.snowflake.com/sql-reference/functions/search_preview-snowflake-cortex

The demo will use an existing Snowflake demo account.

When connecting to the account Snowpark will be used and using connection_name ie Session.builder.config("connection_name", "myconnection").create(). The actual connection_name value should be provided as a parameter when running the creation of the data, if no name is provided the sfseeurope-mstellwall-aws-us-west3 should be used.

The demo does not need to showcase how to ingest and transform data, focus is to generate the data that will be used by the Agent and its tools.

Gemeni's answer:
# **Thematic Research Tool: A Technical Blueprint for a Snowflake Intelligence Demonstration**

## **Part 1: Functional Requirements Document (FRD)**

### **1.0 Demo Vision: The Analyst's AI Co-Pilot**

#### **1.1 The Challenge: The "Data Overload" Crisis in Investment Research**

In the contemporary landscape of investment management, the role of the investment associate is increasingly defined by a formidable challenge: navigating a deluge of information. For an investment and holding company like "Investor Listed," whose success hinges on making astute capital allocation decisions across a diverse portfolio, the speed and accuracy of thematic research are paramount.

Consider the persona of "Anna," an investment associate at the firm. She has been tasked with preparing a comprehensive report on the impact of rising inflation on industrial companies for an upcoming strategy offsite. Her traditional workflow embodies the modern analyst's dilemma. It begins with a multi-day, manual process of data aggregation. Anna must painstakingly scour a multitude of disconnected sources: real-time news feeds from Factset, the Wall Street Journal, and industry-specific newsletters; dense equity research reports; transcripts of expert network calls from Guidepoint; verbatim earnings call transcripts from Quartr; and lengthy strategic analyses from consulting firms like McBainCG. Compounding this complexity, she must also locate and integrate relevant findings from Investor Listed's own internal repository of past investment memos and sector reviews.

This process is not only time-consuming but also fraught with challenges that directly impact the quality of her analysis. She faces significant data overload, forcing her to sift through massive, unstructured datasets while trying to maintain focus on the key insights. The tools at her disposal are fragmented; she must constantly switch between platforms, manually copying and pasting text into a master document, and attempting to reconcile conflicting information. This manual data entry and modeling in spreadsheets are prone to error, and version control becomes a persistent issue, making collaboration difficult. Ultimately, the most significant hurdle is translating this vast collection of raw data into a coherent, actionable narrative that can confidently inform the firm's strategic decisions.

#### **1.2 The Solution: From Data Gatherer to Strategic Thinker**

The "Thematic Research Tool," built on the Snowflake Intelligence platform, is designed to fundamentally transform this paradigm. It introduces a new workflow where Anna transitions from a data gatherer to a strategic thinker. The tool serves as an AI co-pilot, automating the laborious tasks of data discovery, retrieval, and synthesis, thereby empowering her to focus on the higher-value work of hypothesis testing, critical analysis, and forming a nuanced investment thesis.

A core principle underpinning the tool's design is the imperative for confidence and auditability in the financial services sector. Investment professionals are trained to be skeptical and require verifiable, traceable sources for every claim that informs their decisions. An AI that functions as an opaque "black box," providing answers without justification, is fundamentally unusable in this context. Therefore, the Thematic Research Tool is engineered to ensure that every synthesized insight is transparently linked back to its source.

When the tool generates a statement such as, "Industrial producers saw costs increase approximately 12% during 2022, and many passed on 8–10% via price hikes, preserving margins," it will provide explicit citations. The demonstration will showcase Anna clicking on this synthesized fact and being presented with the precise source passages that support it—whether it's a paragraph from a McBainCG report, a data point from a central bank's Producer Price Index (PPI) release, or a direct quote from a CEO in a Quartr earnings call transcript. This capability not only builds trust in the AI's output but also demonstrates Snowflake's inherent strengths in data governance and reliability, ensuring that the research process remains rigorous and defensible.

#### **1.3 The Business Impact: Alpha Generation at Scale**

The ultimate objective of any tool within an investment firm is to contribute to the generation of "alpha"—returns above the market benchmark. The Thematic Research Tool achieves this by creating significant operational leverage. By drastically accelerating the research cycle from days to minutes, it allows the firm's analysts to cover more ground. They can investigate a greater number of investment themes, uncover nascent opportunities before they become widely recognized, and react to market-moving news with unprecedented agility.

For a holding company structure, which focuses on managing a portfolio of subsidiary businesses and making strategic capital allocation decisions, this capability is a powerful competitive advantage. The ability to rapidly synthesize macroeconomic trends, industry-specific challenges, and company-level performance data allows the firm's leadership to make more informed decisions about which assets to acquire, which subsidiaries to support with additional capital, and where to divest. In essence, the Thematic Research Tool enables Investor Listed to scale its intellectual capital, driving smarter, faster investment decisions across its entire portfolio.

### **2.0 The Thematic Research Tool: Core Capabilities**

The tool's functionality is delivered through a set of tightly integrated capabilities, each powered by a specific component of the Snowflake Cortex ecosystem.

#### **2.1 Natural Language Querying & Conversational Analysis**

The primary user interface is a natural language, conversational chat experience. The system is designed to understand and parse complex, multi-intent user queries. An analyst can ask a broad opening question like, "Summarize the impact of rising inflation on industrial companies, referencing recent news, expert opinions, and our internal memos." The tool also supports stateful, multi-turn conversations, allowing the user to progressively refine their inquiry. For instance, after the initial summary, the analyst can ask a follow-up question such as, "Which companies were most successful at passing on costs? Now show me their stock performance." This conversational flow is enabled by the underlying architecture of Cortex Analyst, which can maintain context across a series of related questions.

#### **2.2 Multi-Source Data Synthesis**

The tool's core value proposition is its ability to query, retrieve, and synthesize information from a diverse and federated data landscape in real-time. It seamlessly integrates structured quantitative data (e.g., financial statements, economic indicators) with unstructured qualitative content (e.g., news articles, research reports, transcripts). This is made possible by the Snowflake Cortex Agent, which acts as an intelligent orchestrator. The Agent receives the user's query, develops a plan to answer it, and intelligently routes sub-tasks to the most appropriate specialized tool—Cortex Analyst for structured data queries and Cortex Search for unstructured text retrieval.

#### **2.3 Structured Data Analysis (via Cortex Analyst)**

For questions that require quantitative analysis, the tool leverages Cortex Analyst. This component translates the user's natural language query into a precise SQL query that is executed against a predefined semantic model. This allows the analyst to ask questions like:

* "What was the average Producer Price Index (PPI) for industrial goods in 2022?"  
* "List the top 5 industrial companies by revenue growth last quarter."  
* "Chart the gross margin trend for Company X versus Company Y."

The accuracy and reliability of these answers depend on a well-architected Semantic View. This object serves as a business logic layer, abstracting the complexity of the physical database schema and providing the AI with the necessary context about business entities, relationships, and key metrics.1

#### **2.4 Unstructured Content Search & Summarization (via Cortex Search)**

To extract insights from the vast corpus of textual documents, the tool utilizes the Cortex Search service. This service enables powerful semantic search, going beyond simple keyword matching to understand the contextual meaning of the user's query. This allows the analyst to ask nuanced questions like:

* "What did the CEO of Company Z say about supply chain bottlenecks in their last earnings call?"  
* "Find expert commentary on labor shortages in the manufacturing sector."  
* "Summarize the key findings from the latest McBainCG report on industrial inflation."

To achieve this, a distinct Cortex Search service is created for each unstructured data source. This service indexes the text and creates vector embeddings, enabling a hybrid search approach that combines the semantic understanding of vector search with the precision of traditional keyword search, ensuring highly relevant results.1

### **3.0 The "Investor Listed" Data Ecosystem**

A realistic and compelling demonstration requires a high-fidelity synthetic data ecosystem that mirrors the complexity of an analyst's real-world information sources. The following tables will be generated to serve as the foundation for the demo.

#### **3.1 Structured Data Sources**

| Table Name | Description | Key Columns | Value Proposition |
| :---- | :---- | :---- | :---- |
| COMPANIES | A master table of fictional industrial companies. | COMPANY\_ID (PK), COMPANY\_NAME, TICKER\_SYMBOL, INDUSTRIAL\_SECTOR, HEADQUARTERS | Serves as the central dimension table, allowing the Semantic View to link financial data and unstructured documents to specific entities. |
| MACROECONOMIC\_INDICATORS | Time-series data for key economic indicators relevant to inflation. | INDICATOR\_ID (PK), INDICATOR\_NAME, REPORT\_DATE, VALUE, REGION | Enables the Agent to answer questions that correlate macroeconomic trends with company-specific performance, showcasing sophisticated analytical capability. |
| COMPANY\_FINANCIALS | Quarterly financial statement data for the fictional companies. | FINANCIAL\_ID (PK), COMPANY\_ID (FK), REPORTING\_PERIOD, REVENUE, COST\_OF\_GOODS\_SOLD, GROSS\_PROFIT | The core dataset for Cortex Analyst, populated with figures that reflect inflationary pressures like rising COGS and varied impacts on margins. |

#### **3.2 Unstructured & Semi-Structured Data Sources**

A crucial element of the demo's realism is its ability to faithfully mimic the distinct modalities of different text-based sources. An analyst consumes a concise news report differently than a conversational expert interview or a formal consultant's analysis. Each format has a unique style, purpose, and level of credibility. A generic text generation process would fail to capture this nuance. Therefore, the data generation strategy will employ highly targeted prompts for the snowflake.cortex.complete function.4 This ensures that the generated text for each source accurately reflects the style and content of its real-world counterpart, making the Agent's subsequent synthesis of these disparate sources appear far more intelligent and impressive.

| Table Name | Description | Key Columns | Content & Style |
| :---- | :---- | :---- | :---- |
| FACTSET\_NEWS\_FEED | Mimics a real-time news feed from sources like Factset, DI, FT, WSJ. | ARTICLE\_ID (PK), PUBLISH\_TIMESTAMP, HEADLINE, ARTICLE\_BODY, SOURCE | Factual, concise news reports on supply chain disruptions, raw material price spikes, labor negotiations, and corporate pricing announcements, reflecting themes from financial news providers. |
| GUIDEPOINT\_EXPERT\_TRANSCRIPTS | Transcripts from fictional interviews with industry experts, mimicking providers like Guidepoint and Thirdbridge. | TRANSCRIPT\_ID (PK), INTERVIEW\_DATE, EXPERT\_PROFILE, TRANSCRIPT\_TEXT | Conversational Q\&A format. Provides qualitative, on-the-ground insights on topics like supplier management and customer reactions to price hikes, as is typical of expert network consultations. |
| MCBAINCG\_CONSULTANT\_REPORTS | In-depth strategic reports from a fictional top-tier consulting firm. | REPORT\_ID (PK), PUBLISH\_DATE, TITLE, EXECUTIVE\_SUMMARY, REPORT\_BODY | Structured, analytical content with sections, bullet points, and data callouts. Topics will include strategic responses to inflation, mirroring reports from firms like Bain and McKinsey. |
| QUARTR\_EARNINGS\_CALLS | Transcripts from quarterly earnings calls, mimicking the format provided by Quartr. | CALL\_ID (PK), COMPANY\_ID (FK), CALL\_TIMESTAMP, TRANSCRIPT\_JSON | The JSON column contains the full transcript, structured by speaker (CEO, CFO, Analyst) and section (Presentation, Q\&A), as per the Quartr data format. Content features management commentary on performance amidst inflation. |
| INTERNAL\_INVESTMENT\_MEMOS | The user's own proprietary research documents. | MEMO\_ID (PK), CREATION\_DATE, AUTHOR, SUBJECT\_COMPANIES, MEMO\_BODY | Internal analyses, investment theses, and meeting notes. This demonstrates the tool's ability to integrate and leverage the customer's own valuable, private data, creating a secure, unified research environment. |

### **4.0 The Demo Scenario: A Step-by-Step Walkthrough**

The live demonstration will follow a scripted narrative, guiding the audience through a compelling and logical analytical workflow.

#### **4.1 The Opening Query: A Broad Thematic Question**

* **User (Anna):** "Summarize the impact of rising inflation on industrial companies, referencing recent news, expert opinions, and our internal memos."  
* **Agent's Action:** The Cortex Agent's planning module will parse this complex request. It will recognize the need to query multiple unstructured data sources to fulfill the user's intent. It will then issue parallel Cortex Search queries against the services for FACTSET\_NEWS\_FEED, GUIDEPOINT\_EXPERT\_TRANSCRIPTS, MCBAINCG\_CONSULTANT\_REPORTS, and INTERNAL\_INVESTMENT\_MEMOS.  
* **Agent's Response:** The Agent will receive the top results from each search, then use its underlying Large Language Model (LLM) to synthesize these disparate pieces of information into a single, cohesive paragraph with citations.  
  * *Example Response:* "Rising inflation is significantly impacting industrial companies by increasing input costs for raw materials and energy, which is leading to considerable margin pressure (McBainCG). News reports indicate that widespread supply chain disruptions continue to exacerbate these costs, particularly in logistics and shipping (Factset). Expert commentary suggests that companies with strong brand loyalty and pricing power are better positioned to pass these costs on to consumers, thereby preserving their margins (Guidepoint). Our internal memo on 'Project Titan' previously highlighted this as a key risk and a critical diligence factor for the heavy machinery sector (Internal Memos)."

#### **4.2 The Follow-Up: Drilling into Quantitative Data**

* **User (Anna):** "That's helpful. Which companies have been most successful in preserving their margins over the last year? Show me a chart."  
* **Agent's Action:** The Agent will identify the keywords "companies," "margins," "preserving," and "chart." This combination of terms strongly indicates a quantitative question that requires calculation and visualization. The Agent's planner will select the Cortex Analyst tool as the appropriate instrument. It will then formulate a natural language query for the Analyst, which will be translated into a SQL query against the INDUSTRIAL\_ANALYSIS\_SV Semantic View. The SQL will calculate the gross margin for each company over the last four reporting periods, compute the variance, and rank the results.  
* **Agent's Response:** The Agent will return a bar chart visualization directly in the chat interface, displaying the change in gross margin for the top 5 most resilient companies. This will be accompanied by a textual summary.  
  * *Example Response:* "Based on the latest financial data, 'Global Logistics Corp' and 'Advanced Machinery Inc.' have shown the most resilient gross margins over the past four quarters, with both companies experiencing a decline of less than 50 basis points."

#### **4.3 The Synthesis: Connecting Quantitative and Qualitative**

* **User (Anna):** "Interesting. For Global Logistics Corp, what has management said about their pricing strategy?"  
* **Agent's Action:** This query demonstrates the Agent's ability to pivot seamlessly back to unstructured data while maintaining the context of the conversation. It recognizes "Global Logistics Corp" as the entity of interest and "pricing strategy" as the topic. The planner will select the Cortex Search tool for QUARTR\_EARNINGS\_CALLS and execute a targeted search, filtering for the specific company and searching for relevant keywords within the transcript text.  
* **Agent's Response:** The Agent will extract the most relevant passage from the earnings call transcript and present it as a direct quote.  
  * *Example Response:* "From the Q3 2022 earnings call, CEO Jane Doe stated: 'Our ability to maintain margins in this highly inflationary environment is a direct result of the dynamic pricing models and fuel surcharges we implemented early in the year. These measures have allowed us to pass through nearly 90% of the inflationary cost pressures we've experienced in our freight and logistics operations.'"

#### **4.4 The Conclusion: An Actionable Insight**

The demonstration will conclude by summarizing the workflow. In the span of a few minutes, Anna has progressed from a broad, high-level research question to a specific, actionable insight. She has identified an outperforming company, quantified its success through financial data, and uncovered the specific strategic rationale behind that success, directly from management commentary. This entire analytical journey, which would have traditionally taken days of manual effort, is completed within a single, seamless, and fully auditable conversational interface.

## **Part 2: High-Level Technical Design (HLD)**

This section provides the complete technical specifications, Python code, and SQL scripts required to construct the "Thematic Research Tool" demonstration environment.

### **1.0 Snowflake Architecture Blueprint**

The solution architecture is designed within a single Snowflake database, DEMO\_DB, to ensure simplicity and portability. It comprises distinct schemas for raw data and the analytical intelligence layer, promoting clean organization and governance.

* **Database:** DEMO\_DB  
* **Schemas:**  
  * RAW\_DATA: This schema will house all the base tables containing the synthetic structured and unstructured data.  
  * ANALYTICS: This schema will contain the Cortex Intelligence Layer objects—the Cortex Search Services and the Semantic View—that provide the analytical capabilities.  
* **Warehouse:** DEMO\_WH (a standard, XS warehouse is sufficient for this demo).  
* **Core Objects:**  
  * **Base Tables (in DEMO\_DB.RAW\_DATA):**  
    1. COMPANIES  
    2. MACROECONOMIC\_INDICATORS  
    3. COMPANY\_FINANCIALS  
    4. FACTSET\_NEWS\_FEED  
    5. GUIDEPOINT\_EXPERT\_TRANSCRIPTS  
    6. MCBAINCG\_CONSULTANT\_REPORTS  
    7. QUARTR\_EARNINGS\_CALLS  
    8. INTERNAL\_INVESTMENT\_MEMOS  
  * **Cortex Search Services (in DEMO\_DB.ANALYTICS):**  
    1. FACTSET\_NEWS\_SEARCH  
    2. GUIDEPOINT\_TRANSCRIPTS\_SEARCH  
    3. MCBAINCG\_REPORTS\_SEARCH  
    4. QUARTR\_EARNINGS\_CALLS\_SEARCH  
    5. INTERNAL\_MEMOS\_SEARCH  
  * **Semantic View (in DEMO\_DB.ANALYTICS):**  
    1. INDUSTRIAL\_ANALYSIS\_SV  
  * **Cortex Agent (in snowflake\_intelligence.agents):**  
    1. THEMATIC\_RESEARCH\_AGENT

The architectural flow is as follows: The user interacts with the THEMATIC\_RESEARCH\_AGENT. The Agent's planner analyzes the user's prompt and decides which tool(s) to use. If a qualitative query is detected, it routes the request to one or more of the Cortex Search Services in the ANALYTICS schema. These services perform a semantic search over the corresponding base tables in the RAW\_DATA schema. If a quantitative query is detected, the Agent routes the request to the INDUSTRIAL\_ANALYSIS\_SV Semantic View (via Cortex Analyst). The Semantic View then executes a SQL query against the structured base tables in the RAW\_DATA schema. The results from the tools are returned to the Agent, which synthesizes them into a final response for the user.

### **2.0 Synthetic Data Generation Framework (Python/Snowpark)**

The following Python script, generate\_data.py, uses the Snowpark for Python library to generate all necessary synthetic data and upload it to Snowflake. It is designed to be executed from a local environment with the Snowflake ML Python package installed.

Python

\# generate\_data.py  
import argparse  
import pandas as pd  
from faker import Faker  
import numpy as np  
import random  
from datetime import datetime, timedelta

from snowflake.snowpark.session import Session  
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, FloatType, TimestampType, DateType  
from snowflake.ml.cortex import Complete

\# Initialize Faker for data generation  
fake \= Faker()

\# \--- Configuration Constants \---  
DB\_NAME \= "DEMO\_DB"  
SCHEMA\_NAME \= "RAW\_DATA"  
NUM\_COMPANIES \= 20  
NUM\_NEWS\_ARTICLES \= 100  
NUM\_EXPERT\_TRANSCRIPTS \= 30  
NUM\_CONSULTANT\_REPORTS \= 15  
NUM\_INTERNAL\_MEMOS \= 25  
LLM\_MODEL \= "llama3.1-8b"

\# \--- Helper Functions \---

def get\_snowpark\_session(connection\_name: str) \-\> Session:  
    """Creates and returns a Snowpark session."""  
    connection\_parameters \= {"connection\_name": connection\_name}  
    return Session.builder.configs(connection\_parameters).create()

def create\_schema(session: Session):  
    """Ensures the database and schema exist."""  
    session.sql(f"CREATE DATABASE IF NOT EXISTS {DB\_NAME}").collect()  
    session.sql(f"USE DATABASE {DB\_NAME}").collect()  
    session.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA\_NAME}").collect()  
    session.sql(f"USE SCHEMA {SCHEMA\_NAME}").collect()  
    print(f"Database '{DB\_NAME}' and schema '{SCHEMA\_NAME}' are ready.")

\# \--- Structured Data Generation \---

def generate\_companies\_data() \-\> pd.DataFrame:  
    """Generates a DataFrame of fictional industrial companies."""  
    sectors \=  
    data \=  
    for i in range(1, NUM\_COMPANIES \+ 1):  
        company\_name \= fake.company()  
        data.append({  
            "COMPANY\_ID": i,  
            "COMPANY\_NAME": company\_name,  
            "TICKER\_SYMBOL": ''.join(filter(str.isupper, company\_name))\[:4\] or "COMP",  
            "INDUSTRIAL\_SECTOR": random.choice(sectors),  
            "HEADQUARTERS": fake.city() \+ ", " \+ fake.state\_abbr()  
        })  
    return pd.DataFrame(data)

def generate\_macroeconomic\_data() \-\> pd.DataFrame:  
    """Generates time-series macroeconomic data."""  
    data \=  
    indicators \=  
    regions \= \['North America', 'Europe', 'Asia-Pacific'\]  
    start\_date \= datetime(2021, 1, 1)  
    for i in range(36): \# 3 years of monthly data  
        report\_date \= start\_date \+ timedelta(days=i\*30)  
        for indicator in indicators:  
            for region in regions:  
                if indicator \== 'Producer Price Index \- Industrial Goods':  
                    value \= round(random.uniform(1.5, 4.5) \+ (i \* 0.15), 2) \# Simulating inflation trend  
                elif indicator \== 'Consumer Price Index':  
                    value \= round(random.uniform(1.0, 3.5) \+ (i \* 0.12), 2)  
                else: \# GDP Growth Rate  
                    value \= round(random.uniform(-0.5, 1.5), 2)  
                data.append({  
                    "INDICATOR\_ID": len(data) \+ 1,  
                    "INDICATOR\_NAME": indicator,  
                    "REPORT\_DATE": report\_date.date(),  
                    "VALUE": value,  
                    "REGION": region  
                })  
    return pd.DataFrame(data)

def generate\_financials\_data(companies\_df: pd.DataFrame) \-\> pd.DataFrame:  
    """Generates quarterly financial data for companies."""  
    data \=  
    start\_date \= datetime(2021, 1, 1)  
    for \_, company in companies\_df.iterrows():  
        base\_revenue \= random.uniform(500e6, 5e9)  
        base\_cogs\_ratio \= random.uniform(0.6, 0.8)  
        for i in range(12): \# 3 years of quarterly data  
            period\_date \= start\_date \+ timedelta(days=i\*91)  
            quarter \= f"{period\_date.year}\-Q{(period\_date.month-1)//3\+1}"  
              
            \# Simulate revenue growth and inflation impact on COGS  
            revenue \= base\_revenue \* (1 \+ random.uniform(0.01, 0.05))  
            cogs\_inflation\_impact \= 1 \+ (i \* random.uniform(0.005, 0.015)) \# COGS grow faster over time  
            cogs \= revenue \* base\_cogs\_ratio \* cogs\_inflation\_impact  
            gross\_profit \= revenue \- cogs  
            op\_income \= gross\_profit \* random.uniform(0.15, 0.25)  
            net\_income \= op\_income \* random.uniform(0.7, 0.85)  
              
            data.append({  
                "FINANCIAL\_ID": len(data) \+ 1,  
                "COMPANY\_ID": company,  
                "REPORTING\_PERIOD": quarter,  
                "REVENUE": round(revenue, 2),  
                "COST\_OF\_GOODS\_SOLD": round(cogs, 2),  
                "GROSS\_PROFIT": round(gross\_profit, 2),  
                "OPERATING\_INCOME": round(op\_income, 2),  
                "NET\_INCOME": round(net\_income, 2)  
            })  
            base\_revenue \= revenue

    return pd.DataFrame(data)

\# \--- Unstructured Data Generation \---

def generate\_prompts(companies\_df: pd.DataFrame) \-\> pd.DataFrame:  
    """Generates a DataFrame of prompts for LLM-based content creation."""  
    prompts\_data \=  
    company\_names \= companies\_df.tolist()  
      
    \# Factset News Prompts  
    for \_ in range(NUM\_NEWS\_ARTICLES):  
        company \= random.choice(company\_names)  
        topic \= random.choice(\[  
            "a sudden spike in international shipping costs",   
            "rising raw material prices for steel and aluminum",   
            "a new labor union agreement and its impact on wages",  
            "the announcement of a price increase across its product line",  
            "a significant supply chain bottleneck affecting production"  
        \])  
        prompt \= f"You are a financial news reporter for a service like Factset. Write a short, factual news headline and a 3-paragraph article about how '{company}' is dealing with {topic}. The tone should be neutral, objective, and data-driven. Mention the potential impact on the company's quarterly earnings."  
        prompts\_data.append({"PROMPT\_ID": len(prompts\_data) \+ 1, "SOURCE\_TABLE": "FACTSET\_NEWS\_FEED", "PROMPT": prompt})

    \# Guidepoint Expert Transcripts Prompts  
    for \_ in range(NUM\_EXPERT\_TRANSCRIPTS):  
        expert\_profile \= random.choice(\[  
            "a former VP of Procurement at a global auto manufacturer",  
            "a 20-year veteran in logistics and supply chain management",  
            "a former plant manager for a large chemical company",  
            "an industry consultant specializing in industrial automation"  
        \])  
        topic \= random.choice(\[  
            "managing supplier relationships during periods of high inflation",  
            "the real-world impact of rising energy costs on manufacturing operations",  
            "strategies for passing on costs to customers without losing market share",  
            "the current state of labor shortages and wage inflation in the industrial sector"  
        \])  
        prompt \= f"You are an expert network service like Guidepoint. Generate a 500-word transcript of an interview between an investment analyst and an expert with the profile: '{expert\_profile}'. The topic is '{topic}'. Use a clear Q\&A format (e.g., 'Analyst:', 'Expert:'). The expert's answers should provide deep, qualitative, on-the-ground insights."  
        prompts\_data.append({"PROMPT\_ID": len(prompts\_data) \+ 1, "SOURCE\_TABLE": "GUIDEPOINT\_EXPERT\_TRANSCRIPTS", "PROMPT": prompt})

    \# McBainCG Consultant Reports Prompts  
    for \_ in range(NUM\_CONSULTANT\_REPORTS):  
        title \= random.choice()  
        prompt \= f"You are a top-tier management consultant at a firm like Bain or McKinsey. Write a 700-word strategic report titled '{title}'. The report must include a concise 'Executive Summary' section and a 'Report Body' with at least three distinct sub-headings. The tone should be authoritative, analytical, and strategic, providing actionable recommendations for senior executives in the industrial sector."  
        prompts\_data.append({"PROMPT\_ID": len(prompts\_data) \+ 1, "SOURCE\_TABLE": "MCBAINCG\_CONSULTANT\_REPORTS", "PROMPT": prompt})

    \# Quartr Earnings Calls Prompts  
    for i in range(1, NUM\_COMPANIES \+ 1):  
        company\_name \= companies\_df.loc \== i, 'COMPANY\_NAME'\].iloc  
        prompt \= f"Generate a partial transcript for a quarterly earnings call for the company '{company\_name}'. The transcript should be in JSON format. It must include a 'presentation' section with remarks from the CEO and CFO discussing recent performance in the context of inflation, cost pressures, and pricing actions. It must also include a 'q\_and\_a' section with at least two questions from analysts (e.g., from 'Goldman Sachs', 'Morgan Stanley') and the corresponding answers from the CEO or CFO. The JSON structure should be: {{'version': '1', 'event\_id': {fake.random\_number(digits=5)}, 'company\_id': {i}, 'transcript': {{'presentation': \[{{'speaker': 'Operator', 'text': '...'}}, {{'speaker': 'CEO', 'text': '...'}}, {{'speaker': 'CFO', 'text': '...'}}\], 'q\_and\_a':}}}}"  
        prompts\_data.append({"PROMPT\_ID": len(prompts\_data) \+ 1, "SOURCE\_TABLE": "QUARTR\_EARNINGS\_CALLS", "PROMPT": prompt})

    \# Internal Investment Memos Prompts  
    for \_ in range(NUM\_INTERNAL\_MEMOS):  
        company \= random.choice(company\_names)  
        topic \= random.choice(\[  
            "an updated investment thesis",  
            "a risk assessment of their supply chain exposure",  
            "notes from a recent management meeting",  
            "a competitive analysis of their pricing strategy"  
        \])  
        prompt \= f"You are a senior investment associate at 'Investor Listed'. Write a 400-word internal investment memo regarding '{company}'. The memo should focus on {topic} in light of the current inflationary environment. The tone should be professional, analytical, and confidential. Include a clear recommendation or conclusion."  
        prompts\_data.append({"PROMPT\_ID": len(prompts\_data) \+ 1, "SOURCE\_TABLE": "INTERNAL\_INVESTMENT\_MEMOS", "PROMPT": prompt})

    return pd.DataFrame(prompts\_data)

def generate\_and\_upload\_unstructured\_data(session: Session, prompts\_df: pd.DataFrame, companies\_df: pd.DataFrame):  
    """Generates unstructured data using Cortex Complete and uploads to Snowflake."""  
    prompts\_sdf \= session.create\_dataframe(prompts\_df)  
      
    \# Use Cortex Complete to generate content in parallel  
    print("Generating unstructured content using Snowflake Cortex... This may take several minutes.")  
    results\_sdf \= prompts\_sdf.with\_column("GENERATED\_CONTENT", Complete(LLM\_MODEL, prompts\_sdf))  
    results\_pdf \= results\_sdf.to\_pandas()  
    print("Content generation complete.")

    \# Process and upload each type of unstructured data  
    \# Factset  
    factset\_pdf \= results\_pdf \== 'FACTSET\_NEWS\_FEED'\].copy()  
    factset\_pdf \= range(1, len(factset\_pdf) \+ 1)  
    factset\_pdf \= \[fake.date\_time\_this\_decade() for \_ in range(len(factset\_pdf))\]  
    factset\_pdf \= factset\_pdf.apply(lambda x: x.split('\\n'))  
    factset\_pdf \= factset\_pdf.apply(lambda x: '\\n'.join(x.split('\\n')\[1:\]).strip())  
    factset\_pdf \=) for \_ in range(len(factset\_pdf))\]  
    session.write\_pandas(factset\_pdf\], 'FACTSET\_NEWS\_FEED', auto\_create\_table=True, overwrite=True)  
    print("Uploaded FACTSET\_NEWS\_FEED.")

    \# Guidepoint  
    guidepoint\_pdf \= results\_pdf \== 'GUIDEPOINT\_EXPERT\_TRANSCRIPTS'\].copy()  
    guidepoint\_pdf \= range(1, len(guidepoint\_pdf) \+ 1)  
    guidepoint\_pdf \= \[fake.date\_this\_decade() for \_ in range(len(guidepoint\_pdf))\]  
    guidepoint\_pdf \= guidepoint\_pdf.apply(lambda p: p.split("'"))  
    guidepoint\_pdf \= guidepoint\_pdf  
    session.write\_pandas(guidepoint\_pdf\], 'GUIDEPOINT\_EXPERT\_TRANSCRIPTS', auto\_create\_table=True, overwrite=True)  
    print("Uploaded GUIDEPOINT\_EXPERT\_TRANSCRIPTS.")

    \# McBainCG  
    mcbaincg\_pdf \= results\_pdf \== 'MCBAINCG\_CONSULTANT\_REPORTS'\].copy()  
    mcbaincg\_pdf \= range(1, len(mcbaincg\_pdf) \+ 1)  
    mcbaincg\_pdf \= \[fake.date\_this\_decade() for \_ in range(len(mcbaincg\_pdf))\]  
    mcbaincg\_pdf \= mcbaincg\_pdf.apply(lambda p: p.split("'"))  
    mcbaincg\_pdf \= mcbaincg\_pdf.apply(lambda x: x.split('Report Body').replace('Executive Summary', '').strip())  
    mcbaincg\_pdf \= mcbaincg\_pdf.apply(lambda x: x.split('Report Body').strip() if 'Report Body' in x else x)  
    session.write\_pandas(mcbaincg\_pdf\], 'MCBAINCG\_CONSULTANT\_REPORTS', auto\_create\_table=True, overwrite=True)  
    print("Uploaded MCBAINCG\_CONSULTANT\_REPORTS.")

    \# Quartr  
    quartr\_pdf \= results\_pdf \== 'QUARTR\_EARNINGS\_CALLS'\].copy()  
    quartr\_pdf \= range(1, len(quartr\_pdf) \+ 1)  
    quartr\_pdf \= quartr\_pdf.apply(lambda p: int(p.split("'company\_id': ").split(',')))  
    quartr\_pdf \= \[fake.date\_time\_this\_decade() for \_ in range(len(quartr\_pdf))\]  
    quartr\_pdf.rename(columns={'GENERATED\_CONTENT': 'TRANSCRIPT\_JSON'}, inplace=True)  
    session.write\_pandas(quartr\_pdf\], 'QUARTR\_EARNINGS\_CALLS', auto\_create\_table=True, overwrite=True)  
    print("Uploaded QUARTR\_EARNINGS\_CALLS.")

    \# Internal Memos  
    memos\_pdf \= results\_pdf \== 'INTERNAL\_INVESTMENT\_MEMOS'\].copy()  
    memos\_pdf \= range(1, len(memos\_pdf) \+ 1)  
    memos\_pdf \= \[fake.date\_this\_decade() for \_ in range(len(memos\_pdf))\]  
    memos\_pdf \= \[fake.name() for \_ in range(len(memos\_pdf))\]  
    memos\_pdf \= memos\_pdf.apply(lambda p: p.split("'"))  
    memos\_pdf.rename(columns={'GENERATED\_CONTENT': 'MEMO\_BODY'}, inplace=True)  
    session.write\_pandas(memos\_pdf\], 'INTERNAL\_INVESTMENT\_MEMOS', auto\_create\_table=True, overwrite=True)  
    print("Uploaded INTERNAL\_INVESTMENT\_MEMOS.")

\# \--- Main Execution Block \---

def main():  
    parser \= argparse.ArgumentParser(description="Generate synthetic data for the Thematic Research Tool demo.")  
    parser.add\_argument("--connection\_name", type\=str, default="sfseeurope-mstellwall-aws-us-west3", help\="The name of the Snowflake connection to use from your config file.")  
    args \= parser.parse\_args()

    print(f"Connecting to Snowflake using connection: {args.connection\_name}")  
    session \= get\_snowpark\_session(args.connection\_name)  
      
    create\_schema(session)  
      
    \# Generate and upload structured data  
    print("Generating structured data...")  
    companies\_df \= generate\_companies\_data()  
    macro\_df \= generate\_macroeconomic\_data()  
    financials\_df \= generate\_financials\_data(companies\_df)  
      
    print("Uploading structured data to Snowflake...")  
    session.write\_pandas(companies\_df, 'COMPANIES', auto\_create\_table=True, overwrite=True)  
    session.write\_pandas(macro\_df, 'MACROECONOMIC\_INDICATORS', auto\_create\_table=True, overwrite=True)  
    session.write\_pandas(financials\_df, 'COMPANY\_FINANCIALS', auto\_create\_table=True, overwrite=True)  
    print("Structured data upload complete.")

    \# Generate and upload unstructured data  
    print("Generating prompts for unstructured data...")  
    prompts\_df \= generate\_prompts(companies\_df)  
    generate\_and\_upload\_unstructured\_data(session, prompts\_df, companies\_df)

    print("\\nData generation and upload process finished successfully\!")  
    session.close()

if \_\_name\_\_ \== "\_\_main\_\_":  
    main()

### **3.0 Cortex Intelligence Layer Configuration**

The following SQL script, setup\_intelligence\_layer.sql, should be executed in a Snowsight worksheet after the data generation script has been successfully run. It creates all the necessary Cortex Search Services, the Semantic View, and the final Cortex Agent.

SQL

\-- setup\_intelligence\_layer.sql  
\-- This script configures the Snowflake Intelligence layer for the demo.  
\-- It should be run after \`generate\_data.py\` has populated the tables.

\-- Step 0: Set Context  
USE ROLE ACCOUNTADMIN; \-- Or a role with sufficient privileges  
CREATE WAREHOUSE IF NOT EXISTS DEMO\_WH;  
USE WAREHOUSE DEMO\_WH;  
USE DATABASE DEMO\_DB;  
CREATE SCHEMA IF NOT EXISTS ANALYTICS;  
USE SCHEMA ANALYTICS;

\--------------------------------------------------------------------  
\-- Step 1: Create Cortex Search Services for Unstructured Data  
\--------------------------------------------------------------------  
\-- This step creates a separate search service for each unstructured text table.  
\-- This allows the Agent to reason about which source is most appropriate for a given query.

\-- 1.1 Factset News Feed Search Service  
CREATE OR REPLACE CORTEX SEARCH SERVICE FACTSET\_NEWS\_SEARCH  
    ON ARTICLE\_BODY \-- The column to perform semantic search on  
    ATTRIBUTES HEADLINE, PUBLISH\_TIMESTAMP, SOURCE \-- Columns to return and filter on  
    WAREHOUSE \= 'DEMO\_WH'  
    TARGET\_LAG \= '1 day'  
    AS SELECT ARTICLE\_ID, HEADLINE, PUBLISH\_TIMESTAMP, SOURCE, ARTICLE\_BODY   
    FROM DEMO\_DB.RAW\_DATA.FACTSET\_NEWS\_FEED;

\-- 1.2 Guidepoint Expert Transcripts Search Service  
CREATE OR REPLACE CORTEX SEARCH SERVICE GUIDEPOINT\_TRANSCRIPTS\_SEARCH  
    ON TRANSCRIPT\_TEXT  
    ATTRIBUTES INTERVIEW\_DATE, EXPERT\_PROFILE  
    WAREHOUSE \= 'DEMO\_WH'  
    TARGET\_LAG \= '1 day'  
    AS SELECT TRANSCRIPT\_ID, INTERVIEW\_DATE, EXPERT\_PROFILE, TRANSCRIPT\_TEXT   
    FROM DEMO\_DB.RAW\_DATA.GUIDEPOINT\_EXPERT\_TRANSCRIPTS;

\-- 1.3 McBainCG Consultant Reports Search Service  
CREATE OR REPLACE CORTEX SEARCH SERVICE MCBAINCG\_REPORTS\_SEARCH  
    ON REPORT\_BODY  
    ATTRIBUTES TITLE, PUBLISH\_DATE, EXECUTIVE\_SUMMARY  
    WAREHOUSE \= 'DEMO\_WH'  
    TARGET\_LAG \= '1 day'  
    AS SELECT REPORT\_ID, TITLE, PUBLISH\_DATE, EXECUTIVE\_SUMMARY, REPORT\_BODY   
    FROM DEMO\_DB.RAW\_DATA.MCBAINCG\_CONSULTANT\_REPORTS;

\-- 1.4 Quartr Earnings Calls Search Service  
CREATE OR REPLACE CORTEX SEARCH SERVICE QUARTR\_EARNINGS\_CALLS\_SEARCH  
    ON TRANSCRIPT\_JSON  
    ATTRIBUTES COMPANY\_ID, CALL\_TIMESTAMP  
    WAREHOUSE \= 'DEMO\_WH'  
    TARGET\_LAG \= '1 day'  
    AS SELECT CALL\_ID, COMPANY\_ID, CALL\_TIMESTAMP, TRANSCRIPT\_JSON   
    FROM DEMO\_DB.RAW\_DATA.QUARTR\_EARNINGS\_CALLS;

\-- 1.5 Internal Investment Memos Search Service  
CREATE OR REPLACE CORTEX SEARCH SERVICE INTERNAL\_MEMOS\_SEARCH  
    ON MEMO\_BODY  
    ATTRIBUTES CREATION\_DATE, AUTHOR, SUBJECT\_COMPANIES  
    WAREHOUSE \= 'DEMO\_WH'  
    TARGET\_LAG \= '1 day'  
    AS SELECT MEMO\_ID, CREATION\_DATE, AUTHOR, SUBJECT\_COMPANIES, MEMO\_BODY   
    FROM DEMO\_DB.RAW\_DATA.INTERNAL\_INVESTMENT\_MEMOS;

\--------------------------------------------------------------------  
\-- Step 2: Create the Semantic View for Structured Data Analysis  
\--------------------------------------------------------------------  
\-- This is a critical component that provides the business context for Cortex Analyst.  
\-- It defines logical tables, relationships, dimensions, and metrics.

CREATE OR REPLACE SEMANTIC VIEW INDUSTRIAL\_ANALYSIS\_SV  
    \-- Define the logical tables, their physical counterparts, and primary keys.  
    TABLES (  
        companies AS DEMO\_DB.RAW\_DATA.COMPANIES  
            PRIMARY KEY (company\_id)  
            WITH SYNONYMS ('industrial companies', 'firms')  
            COMMENT \= 'Master table for industrial companies in the portfolio.',  
          
        financials AS DEMO\_DB.RAW\_DATA.COMPANY\_FINANCIALS  
            PRIMARY KEY (financial\_id)  
            COMMENT \= 'Quarterly financial statement data for each company.',  
              
        macro\_indicators AS DEMO\_DB.RAW\_DATA.MACROECONOMIC\_INDICATORS  
            PRIMARY KEY (indicator\_id)  
            WITH SYNONYMS ('economic data', 'inflation metrics')  
            COMMENT \= 'Time-series data for key macroeconomic indicators.'  
    )  
      
    \-- Define the relationships between the logical tables.  
    RELATIONSHIPS (  
        financials\_to\_companies AS  
            financials (company\_id) REFERENCES companies  
    )  
      
    \-- Define dimensions (attributes to group by or filter on).  
    DIMENSIONS (  
        companies.company\_name AS companies.company\_name  
            WITH SYNONYMS ('company', 'name')  
            COMMENT \= 'The legal name of the industrial company.',  
              
        companies.sector AS companies.industrial\_sector  
            WITH SYNONYMS ('industry sector', 'sub-industry')  
            COMMENT \= 'The specific industrial sector the company operates in.',  
              
        financials.reporting\_period AS financials.reporting\_period  
            WITH SYNONYMS ('quarter', 'period')  
            COMMENT \= 'The financial reporting period, e.g., 2022-Q3.',  
              
        macro\_indicators.indicator\_name AS macro\_indicators.indicator\_name  
            WITH SYNONYMS ('metric name', 'indicator')  
            COMMENT \= 'The name of the macroeconomic indicator, e.g., PPI.',  
              
        macro\_indicators.region AS macro\_indicators.region  
            COMMENT \= 'The geographical region for the macroeconomic indicator.'  
    )  
      
    \-- Define metrics (quantitative measures to be aggregated).  
    METRICS (  
        financials.total\_revenue AS SUM(financials.revenue)  
            WITH SYNONYMS ('sales', 'turnover')  
            COMMENT \= 'The total revenue for a given period.',  
              
        financials.total\_cogs AS SUM(financials.cost\_of\_goods\_sold)  
            WITH SYNONYMS ('cost of sales')  
            COMMENT \= 'The total cost of goods sold for a given period.',  
              
        financials.gross\_margin AS (SUM(financials.gross\_profit) / SUM(financials.revenue)) \* 100  
            WITH SYNONYMS ('margin percentage')  
            COMMENT \= 'The gross profit as a percentage of revenue.',  
              
        companies.company\_count AS COUNT(DISTINCT companies.company\_id)  
            COMMENT \= 'The total number of unique companies.',  
              
        macro\_indicators.average\_indicator\_value AS AVG(macro\_indicators.value)  
            COMMENT \= 'The average value of a macroeconomic indicator over a period.'  
    )  
    COMMENT \= 'Semantic View for analyzing the financial performance of industrial companies against macroeconomic trends.';

\--------------------------------------------------------------------  
\-- Step 3: Create the Cortex Agent  
\--------------------------------------------------------------------  
\-- This final step brings everything together by creating the agent that  
\-- orchestrates queries across all the tools defined above.

\-- First, ensure the necessary privileges are granted for agent creation.  
CREATE DATABASE IF NOT EXISTS snowflake\_intelligence;  
GRANT USAGE ON DATABASE snowflake\_intelligence TO ROLE PUBLIC;  
CREATE SCHEMA IF NOT EXISTS snowflake\_intelligence.agents;  
GRANT USAGE ON SCHEMA snowflake\_intelligence.agents TO ROLE PUBLIC;  
GRANT CREATE AGENT ON SCHEMA snowflake\_intelligence.agents TO ROLE ACCOUNTADMIN; \-- Or your specific role

\-- Now, create the agent.  
CREATE OR REPLACE AGENT THEMATIC\_RESEARCH\_AGENT  
    \-- Define the tools the agent can use. Each tool needs a clear description.  
    TOOLS \= (  
        \-- Cortex Analyst Tool  
        CORTEX\_ANALYST(  
            NAME \=\> 'quantitative\_financial\_and\_economic\_analysis',  
            SEMANTIC\_VIEW \=\> 'DEMO\_DB.ANALYTICS.INDUSTRIAL\_ANALYSIS\_SV',  
            DESCRIPTION \=\> 'Use this tool for quantitative questions about company financials (revenue, costs, margins), counts of companies, or macroeconomic data (PPI, CPI). It is best for calculations, aggregations, trends, and creating charts.'  
        ),  
        \-- Cortex Search Tools  
        CORTEX\_SEARCH(  
            NAME \=\> 'factset\_news\_search',  
            SERVICE \=\> 'DEMO\_DB.ANALYTICS.FACTSET\_NEWS\_SEARCH',  
            DESCRIPTION \=\> 'Use this tool to search for recent news articles from sources like Factset, FT, and WSJ. Best for finding factual, up-to-the-minute information on market events, company announcements, and supply chain updates.'  
        ),  
        CORTEX\_SEARCH(  
            NAME \=\> 'guidepoint\_expert\_transcripts\_search',  
            SERVICE \=\> 'DEMO\_DB.ANALYTICS.GUIDEPOINT\_TRANSCRIPTS\_SEARCH',  
            DESCRIPTION \=\> 'Use this tool to search transcripts of interviews with industry experts. Best for finding qualitative, on-the-ground opinions, and deep industry context on topics like operational challenges and strategic responses.'  
        ),  
        CORTEX\_SEARCH(  
            NAME \=\> 'mcbaincg\_consultant\_reports\_search',  
            SERVICE \=\> 'DEMO\_DB.ANALYTICS.MCBAINCG\_REPORTS\_SEARCH',  
            DESCRIPTION \=\> 'Use this tool to search in-depth strategic reports from a top-tier consulting firm. Best for understanding broad industry trends, strategic frameworks, and management best practices.'  
        ),  
        CORTEX\_SEARCH(  
            NAME \=\> 'quartr\_earnings\_calls\_search',  
            SERVICE \=\> 'DEMO\_DB.ANALYTICS.QUARTR\_EARNINGS\_CALLS\_SEARCH',  
            DESCRIPTION \=\> 'Use this tool to search transcripts of company earnings calls. Best for finding direct quotes and commentary from company executives (CEOs, CFOs) about their performance, strategy, and outlook.'  
        ),  
        CORTEX\_SEARCH(  
            NAME \=\> 'internal\_memos\_search',  
            SERVICE \=\> 'DEMO\_DB.ANALYTICS.INTERNAL\_MEMOS\_SEARCH',  
            DESCRIPTION \=\> 'Use this tool to search your firm''s proprietary internal investment memos. Best for finding past analyses, investment theses, and confidential notes on specific companies or themes.'  
        )  
    )  
    \-- Provide planning instructions to guide the agent's logic.  
    PLANNING\_INSTRUCTIONS \=   
    $$  
    You are an expert investment research assistant. Your goal is to provide comprehensive, accurate, and well\-sourced answers to the user's questions.  
    1\.  First, carefully analyze the user's query to understand their intent.  
    2\.  Break down complex questions into smaller, logical sub\-problems.  
    3\.  Determine if the query is primarily quantitative (requiring calculations, trends, charts of financial or economic data) or qualitative (requiring information from text like news, reports, or transcripts).  
    4\.  For quantitative questions, you MUST use the 'quantitative\_financial\_and\_economic\_analysis' tool.  
    5\.  For qualitative questions, select the most appropriate search tool(s) based on their descriptions. For example, for executive commentary, use 'quartr\_earnings\_calls\_search'. For broad strategic analysis, use 'mcbaincg\_consultant\_reports\_search'. For breaking news, use 'factset\_news\_search'.  
    6\.  If a query is mixed (e.g., "Summarize the news and show me the financial impact"), use multiple tools in sequence. First, use the search tools to gather qualitative context, then use the analysis tool to get the quantitative data.  
    7\.  Think step\-by\-step and formulate a clear plan before executing any tools.  
    $$  
    \-- Provide response instructions to format the final output.  
    RESPONSE\_INSTRUCTIONS \=   
    $$  
    Synthesize the information gathered from the tools into a single, concise, and well\-written answer. Do not just list the raw output from the tools.  
    \-   When you provide a fact, insight, or quote from a specific source, you MUST cite the source in parentheses at the end of the sentence. For example: (Factset News), (Guidepoint Transcript), (McBainCG Report), (Internal Memo), (Quartr Earnings Call).  
    \-   If the user asks for a chart or visualization, generate it and also provide a brief textual summary of the key takeaway from the chart.  
    \-   Structure your answers logically. Start with a high\-level summary and then provide supporting details.  
    $$  
    WAREHOUSE \= 'DEMO\_WH';

\-- Grant usage on the agent to the role that will be running the demo.  
GRANT USAGE ON AGENT THEMATIC\_RESEARCH\_AGENT TO ROLE ACCOUNTADMIN; \-- Or your specific role

SELECT 'SUCCESS: All intelligence layer objects have been created.';

### **4.0 Demo Execution and Validation**

#### **4.1 Master Setup Script**

To streamline the setup process, a master SQL script can be created. This script will first call the Python data generation script (assuming it's been staged and wrapped in a Stored Procedure) and then execute the intelligence layer setup script. For the purpose of this document, the two steps are presented separately for clarity, but they can be combined for a one-click deployment.

**Execution Order:**

1. Run the Python script: python generate\_data.py \--connection\_name \<your\_connection\_name\>  
2. Execute the entire setup\_intelligence\_layer.sql script in a Snowsight worksheet.

#### **4.2 Validation and Rehearsal Queries**

After the setup is complete, use the following queries in the Snowflake Intelligence interface (with the THEMATIC\_RESEARCH\_AGENT selected) to validate the system and rehearse the demonstration flow.

**Query 1: Broad Thematic Synthesis (Tests multiple Cortex Search tools)**

* **Prompt:** "Summarize the impact of rising inflation on industrial companies, referencing recent news, expert opinions, and our internal memos."  
* **Expected Behavior:** The agent should use the factset\_news\_search, guidepoint\_expert\_transcripts\_search, and internal\_memos\_search tools. The response should be a synthesized paragraph with citations from each source.

**Query 2: Quantitative Analysis (Tests Cortex Analyst)**

* **Prompt:** "What was the average gross margin for companies in the 'Heavy Machinery' sector in 2022?"  
* **Expected Behavior:** The agent should use the quantitative\_financial\_and\_economic\_analysis tool. The response should be a single numerical value (e.g., "The average gross margin... was 28.7%.").

**Query 3: Visualization (Tests Cortex Analyst charting)**

* **Prompt:** "Show me a bar chart of total revenue by industrial sector for the last full year."  
* **Expected Behavior:** The agent should use the quantitative\_financial\_and\_economic\_analysis tool and produce a bar chart visualization.

**Query 4: Targeted Qualitative Search (Tests specific Cortex Search tool)**

* **Prompt:** "Find me commentary from company executives about their strategies for managing supply chain costs."  
* **Expected Behavior:** The agent should primarily use the quartr\_earnings\_calls\_search tool and return one or more direct quotes from the generated earnings call transcripts.

**Query 5: Trend Analysis (Tests Cortex Analyst time-series capability)**

* **Prompt:** "Plot the trend of the Producer Price Index for Industrial Goods in North America over the last 3 years."  
* **Expected Behavior:** The agent should use the quantitative\_financial\_and\_economic\_analysis tool and generate a line chart.

**Query 6: Multi-Step, Mixed-Intent Query (Tests full orchestration)**

* **Prompt (Part 1):** "Which company had the highest revenue last quarter?"  
* **Expected Behavior (Part 1):** Agent uses Cortex Analyst to identify the company (e.g., "Global Logistics Corp had the highest revenue...").  
* **Prompt (Part 2 \- Follow-up):** "What are the key findings from the latest McBainCG report about the logistics industry?"  
* **Expected Behavior (Part 2):** Agent maintains context and uses the mcbaincg\_reports\_search tool to summarize the relevant report, demonstrating its ability to pivot between tools within a conversation.

By executing these validation queries, the Sales Engineer can confirm that all components of the demonstration are functioning correctly and can rehearse a fluid, compelling narrative that showcases the full power of Snowflake Intelligence.

#### **Works cited**

1. Overview of Snowflake Intelligence | Snowflake Documentation, accessed August 28, 2025, [https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence)  
2. Using SQL commands to create and manage semantic views ..., accessed August 28, 2025, [https://docs.snowflake.com/en/user-guide/views-semantic/sql](https://docs.snowflake.com/en/user-guide/views-semantic/sql)  
3. CREATE CORTEX SEARCH SERVICE | Snowflake Documentation, accessed August 28, 2025, [https://docs.snowflake.com/sql-reference/sql/create-cortex-search](https://docs.snowflake.com/sql-reference/sql/create-cortex-search)  
4. snowflake.cortex.complete | Snowflake Documentation, accessed August 28, 2025, [https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete)