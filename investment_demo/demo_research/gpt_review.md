My Prompt:    
Hi Cursor, I am a sales engineer at Snowflake.  
I want you to design and then eventually build an excellent solution that I can demo to my customer.  
For your task now it is design only and we will do build in a future phase.  
In  you will see where I told Gemini deep research my goals of what I want to do and it produced a functional design and a tech design.    
It failed to give me any options to choose from or for me to clarify any questions.  
I am generally satisfied with what it designed but am doubtful it is excellent and comprehensive and would like you to review it and help me further validate and improve the design.  
In order to do so, you will ask me questions and present some options that I can choose from.  
I do not want you to code anything nor get too deep into the detailed design.    
I first want a good functional design that can be delivered in a reasonable number of steps, but also can be improved in phases After functional design for the use case is complete, I foresee tech tasks will be required.    
All demo scenarios will be using the same Snowflake user, so no need to include security setup (RABC, Users etc).   
A snowflake account already exists, the demo should create it's data in it's own database.   
To connect to Snowflake  connections.toml will be used, you can asume it exists, as described in @https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session\#connect-by-using-the-connections-toml-file   
Cortex Complete will be used to generate the unstructured data, model to be used should be configuarble, avvalible models is described at @https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql\#availability and you can assume that Cross-Region is enabled.  
When generating unstructured data it is most effective to store the prompts, should be dynamic created, in a Snowflake table and then use complete against the table, the Python complete function can be used, @https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete , against a Snowpark Dataframe.  
Snowpark Dataframes shgould be used as much as possible, if data can not be generated with Snowpark Dataframes then Pandas dataframes should be used and then the data should be loaded into Snowflake using the write\_pandas function, @https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/snowpark/api/snowflake.snowpark.Session.write\_pandas , with the quote\_identifiers parameter set to false and also make sure column names are named accordingly to @https://docs.snowflake.com/en/sql-reference/identifiers-syntax   
All data needed to support the scenario must be generated, it should be as realistic as possible.  
Data volumes, history lengths (number of months, quarter, years etc), etc should be configurable.  
Snowflake Intelligence has a GUI of it's own that will be used and Snowsight will be used to configure the Agent, see @https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence\#create-an-agent how Agents are configured.   
It is important that Response instruction, Planning instructions and that for tools Description is used, For Cortex Search tool there also needs to be a ID column and Ttitle column. All tools should have a name that does not have spaces, underscore can be used, and a description that allows the Agenyt to understand when to use it.

It is crucial that we do not use the customer name but use the fictional name in the demo design document.

Please read through all of these materials and suggest some improvements to the design documents and also please ask questions or give me options so that I can also help.

GPT Answer:  
I’m going to set up a short design todo list so I can structure the review, propose improvements, and gather your inputs with options. I’ll start with the review and then present questions and choices.

\[1 tool called\]

I reviewed the Gemini design and drafted an improved functional design with options and questions. I’ll now check off the review task and mark the remaining design tasks complete since I’ve provided them in this message.

\[1 tool called\]

I reviewed the Gemini design and drafted improvements, options, and clarifying questions. I’m going to present a concise, selectable functional design you can confirm now, then we can refine the technical planning in a later phase.

\#\#\# Quick assessment: strengths, gaps, and risks  
\- • Strengths: coherent end-to-end story; clear split of structured via Semantic View and unstructured via Cortex Search; good demo narrative and validation prompts.  
\- • Gaps to address:  
  \- \*\*Cortex Search requirements\*\*: Ensure each service exposes an ID column and a TITLE column the agent can cite. Current examples don’t guarantee that consistently.  
  \- \*\*Chunking strategy\*\*: Not specified for long docs/transcripts. Without chunking \+ overlap, retrieval quality/citations may suffer.  
  \- \*\*Entity linking\*\*: Unstructured sources should map to \`COMPANY\_ID\` where applicable to support pivots (e.g., from Analyst chart → earnings quotes).  
  \- \*\*Configurability\*\*: Volumes, dates, models, and languages should be centralized and parameterized.  
  \- \*\*Data realism\*\*: Prompt templates are good, but lack structured variability (region/industry shocks, inflation regimes, secular trends).  
  \- \*\*Evaluation/guardrails\*\*: No acceptance criteria, quality checks, or citation style for the agent’s responses; risk of hallucinations or weak sourcing.  
  \- \*\*Agent instructions\*\*: Good start; could improve tool selection logic, tool descriptions, and response formatting for citations.  
  \- \*\*Performance/cost\*\*: No plan for generation rate limits, batching, or search index refresh cadence.  
\- • Risks:  
  \- \*\*LLM generation drift\*\* (inconsistent styles across sources) without seeded variability/controls.  
  \- \*\*Index staleness\*\* if you regenerate data but don’t refresh CORTEX SEARCH services.  
  \- \*\*Over-scope\*\* for MVP if all sources \+ deep history are attempted at once.

\#\#\# Proposed functional MVP and phased roadmap  
\- • Phase 1 (MVP): Narrow, high-signal demo that fits in a single session  
  \- Data: 10–12 fictional industrial companies; 8 quarters of financials; 24–36 months of macro indicators.  
  \- Unstructured: 40–60 news articles, 10–12 expert transcripts, 6–8 consultant reports, per-company earnings call snippets, 10–12 internal memos.  
  \- Retrieval: 1 Cortex Search per source type with consistent \`ID\` and \`TITLE\`.  
  \- Analytics: 1 Semantic View with core metrics (revenue, COGS, gross margin), sector dimension, calendar dimension.  
  \- Agent: Clear planning/response instructions; citations with source type, title, and date.  
  \- Config: Centralized parameters for volumes/history/model/seed.  
\- • Phase 2: Quality and realism  
  \- Add chunking \+ overlap; entity linking from unstructured to \`COMPANY\_ID\`; basic prompt variability by region/sector/shock type; index refresh schedule.  
\- • Phase 3: Depth and orchestration  
  \- Add more sources (optional), cross-source synthesis prompts, trend charts, and structured-unstructured joins (e.g., margin trend \+ exec commentary).  
\- • Phase 4: Evaluation and polish  
  \- Add a small evaluation harness (expected-tool checks, citation presence, time-to-first-response budget), plus cost/latency guardrails.

\#\#\# Options to choose (pick one per bullet, or mix)  
\- • Company universe:  
  \- \*\*Generic Industrials\*\* (safer, faster) vs \*\*Named sub-sectors\*\* (machinery, logistics, chemicals) for richer prompts.  
\- • History depth:  
  \- \*\*8 quarters \+ 24 months\*\* (fast MVP) vs \*\*12 quarters \+ 36 months\*\* (richer charts) vs \*\*18 quarters \+ 48 months\*\* (heavier).  
\- • Unstructured scope:  
  \- \*\*News \+ Earnings \+ Memos\*\* (lean) vs \*\*+ Expert\*\* (balanced) vs \*\*+ Consultant\*\* (full).  
\- • Chunking:  
  \- \*\*Fixed tokens with 15–20% overlap\*\* (simple) vs \*\*Semantic sectioning \+ overlap\*\* (best quality) vs \*\*Hybrid\*\* (balanced).  
\- • Search services:  
  \- \*\*Per-source service\*\* (clear reasoning) vs \*\*Single consolidated service\*\* (simpler, but weaker source-specific citations).  
\- • Default model:  
  \- \*\*llama3.1-8b\*\* (fast, cheap) vs \*\*mix (8b for news/memos, 70b for reports/transcripts)\*\* (quality) with config toggle.  
\- • Index refresh:  
  \- \*\*On-demand after data generation\*\* vs \*\*Scheduled daily\*\* (demo consistency).  
\- • Citation style:  
  \- \*\*(SourceType — Title, Date)\*\* vs \*\*\[Title\] (SourceType, Date)\*\*. Ensure TITLE always present in the service.

\#\#\# Clarifying questions (please answer briefly)  
\- • Audience & narrative  
  \- 1\) Primary audience (technical, business, mixed)?  
  \- 2\) Preferred storyline emphasis: inflation → margins → pricing power, or supply chain → costs → mitigation?  
  \- 3\) Must-have “wow” moment: chart, quote with citation, or mixed orchestration?  
\- • Scope choices  
  \- 4\) Pick company universe option above.  
  \- 5\) Pick history depth option above.  
  \- 6\) Pick unstructured scope option above.  
\- • Data realism  
  \- 7\) Regions to emphasize (NA, EU, APAC)? Single or multi-region demo?  
  \- 8\) Any sector(s) you want featured (e.g., logistics, heavy machinery)?  
\- • Generation & retrieval  
  \- 9\) Default model selection (8b vs mixed)?  
  \- 10\) OK to use semantic sectioning for reports/transcripts (slightly more prep time)?  
  \- 11\) Do you want entity linking (company names → \`COMPANY\_ID\`) from unstructured sources in MVP?  
\- • Agent behavior & UX  
  \- 12\) Prefer conservative tool selection (single best tool) or aggressive (parallel tools) for effect?  
  \- 13\) Citation style preference among the two suggested?  
  \- 14\) Is multi-turn follow-up required in MVP or is single-shot enough?  
\- • Evaluation & constraints  
  \- 15\) Target demo runtime budget (e.g., \<15 minutes to show end-to-end)?  
  \- 16\) Any cost sensitivity requiring lower volumes or single-pass generation?  
  \- 17\) Acceptable cold-start time to build indexes during the demo setup (e.g., 5–10 minutes)?  
\- • Localization & polish  
  \- 18\) English-only, or include some EU language news examples?  
  \- 19\) Any branding constraints for fictional names? We’ll keep “Investor Listed.”  
  \- 20\) Any data you absolutely do not want included (e.g., energy/oil)?

\#\#\# Adjustments to Snowflake Intelligence objects (functional, not code)  
\- • Cortex Search services  
  \- Ensure each service SELECT exposes:    
    \- \*\*ID\*\*: unique identifier per document (e.g., \`ARTICLE\_ID\`, \`TRANSCRIPT\_ID\`, \`REPORT\_ID\`, \`CALL\_ID\`, \`MEMO\_ID\`).    
    \- \*\*TITLE\*\*: human-readable title for citation (e.g., \`HEADLINE\`, \`TITLE\`, \`SUBJECT\`, or synthesized title).    
    \- \*\*CONTENT column\*\*: the field you search on (e.g., \`ARTICLE\_BODY\`, \`TRANSCRIPT\_TEXT\`, \`REPORT\_BODY\`, \`TRANSCRIPT\_JSON\`), plus ATTRIBUTES like timestamp, company, source.    
  \- Keep tool names underscore\_cased and descriptions explicit about “when to use.”  
  \- Add light chunking for long fields: section-by-section rows with stable IDs and generated section titles.  
\- • Semantic View  
  \- Add a small \`calendar\` logical table for consistent time grouping.  
  \- Confirm relationships: \`financials.company\_id → companies.company\_id\`.  
  \- Dimensions: sector, company, reporting period; optional region via macro table.  
  \- Metrics: total revenue, total COGS, gross margin %; optionally revenue growth QoQ/YoY (for nicer charts).  
  \- Add COMMENTS and WITH SYNONYMS comprehensively (e.g., “margin,” “gross margin,” “gm%”).  
\- • Agent instructions (refined)  
  \- Planning: classify query as quantitative vs qualitative; prefer exact entity filters when specified; for mixed requests, first retrieve qualitative context, then quantify; avoid redundant tool calls if high-confidence result already exists.  
  \- Response: lead with a one-paragraph summary; always include citations with (SourceType — Title, Date); generate charts when asked; keep 3–5 bullet supporting points maximum.

\#\#\# Synthetic data generation strategy (functional)  
\- • Parameters (configurable): number of companies; sectors; regions; quarters/months; counts per unstructured source; model name; random seed; language mix; per-source chunk size; overlap %; index refresh cadence.  
\- • Prompt tables: store dynamic prompts by \`SOURCE\_TABLE\`, \`COMPANY\_ID\` (when applicable), \`TITLE\_HINT\`, \`TOPIC\_TAGS\`, \`PROMPT\_TEXT\`, \`RANDOM\_SEED\`, \`MODEL\`.  
\- • Completion: run Complete on the prompts table by source; enforce length ranges; inject variability by sector/region/inflation regime; extract or generate \`TITLE\` for each output.  
\- • Normalization: map company names → \`COMPANY\_ID\`; validate JSON for earnings transcripts; attach timestamps; dedupe near-identical content.  
\- • Loading: prefer Snowpark DataFrames; if Pandas is required, use write\_pandas with \`quote\_identifiers=false\` and Snowflake-compliant identifiers.

\#\#\# Demo validation and success criteria  
\- • Smoke checks: tables populated with configured row counts; each Cortex Search service returns results for “inflation” and “pricing” queries; Semantic View answers margin and revenue queries; charts render.  
\- • Orchestration checks: mixed query uses both search and analyst; responses include at least two citations with titles.  
\- • Time/cost: generation ≤ X minutes, indexing ≤ Y minutes; end-to-end demo ≤ 15 minutes.  
\- • Rehearsal prompts: keep Gemini’s list, plus a mixed-intent prompt that forces cross-source synthesis and cites titles.

Please pick your options (company universe, history depth, unstructured scope, chunking, search service strategy, default model, index refresh, citation style), and answer the clarifying questions. Once we lock those, I’ll finalize the functional design and then outline a light technical plan for the build phase.

\- I completed the design review and drafted improvements, options, and questions. After you choose options and answer the questions, I’ll consolidate them into the final functional design and move to the next phase.

My answers:  
Options to choose:  
 \* Company universe: Named sub-sectors start, with logistics  
\* History depth: 18 quarters \+ 48 months   
\* Unstructured scope: Full, we need from all types of unstructured sources mentioned  
\* Chunking: No.chunking needed  
\* Search services: One per type of unstructured source  
\* Default model: llama3.1-8b for generating unstructured data and Claude 4.0 for the Agent  
\* Index refresh: For Cortex Search set every 10 minutes  
\*  Citation style:  \[Title\] (SourceType, Date)  
Clarifying questions:  
\* Audience & narrative  
  1\) Mixed  
  2\) I want the story line divided into multiple steps where the user interacts with the Agent in SNowflake Intelligence ie Question 1, Agent answer, folluwp question, agent answer and so on. Preferable 3-4 questions from teh user.  
  3\) Must-have “wow” moment: All answers should have citations and quotes  
 Scope choices  
  4-6) See my picks earlies  
Data realism:  
  7\) Regions to emphasize: Nordics with a hint of EU  
 8\) logistics  
Generation & retrieval:  
 9\) Se earlier pick  
 10\) Yes  
 11\) Where it make sense ie if the real life source of that data is linked then we will link it  
  Agent behavior & UX  
12\) It should use multiple tools if needed, but please suggest in which order it should use them  
13\) See my pick ealier  
14\) Yes, see my answer to question 2  
Evaluation & constraints  
15 ) \<15 minutes is the target.  
16\)  No  
17\) No need for this  
Localization & polish:  
18\) Primary english, but would bve nice to have one news agency data in Swedish  
19\) Please make up a name, should be related to snow  
20\) No

Please ask any follup questions you might have.  
Do not start coding or create files until I tell you so.

GTP Answer:  
Acknowledged your selections. I’ll consolidate them into an MVP-ready functional design, propose a 4-step demo flow, suggest tool ordering, and ask a few final clarifying questions. No code or files will be created.

\#\#\# Functional design (updated per your choices)  
\- • Company universe: Named sub-sector focus starting with logistics; 10–12 companies.  
\- • History depth: 18 quarters (4.5 years) \+ 48 months macro.  
\- • Unstructured scope: Full set (News, Expert Transcripts, Consultant Reports, Earnings Calls, Internal Memos).  
\- • Search services: One per source type; each exposes ID, TITLE, date/timestamp, source/author, and optional COMPANY\_ID for entity linking.  
\- • Model choices:  
  \- \*\*Generation\*\*: llama3.1-8b (configurable; allow override via parameter).  
  \- \*\*Agent\*\*: Claude 4.0 (set in Snowflake Intelligence if available in your region/account; define fallback model).  
\- • Index refresh: Every 10 minutes for each CORTEX SEARCH service.  
\- • Citation style: \[Title\] (SourceType, Date).  
\- • Regions & localization: Nordics emphasis with EU context; include one Swedish news provider.  
\- • Entity linking: Add COMPANY\_ID where source would have it in real life (earnings calls, many news items, some memos; experts/reports when clearly attributable).  
\- • No chunking: Accepted for MVP. For very long docs, we will still normalize into distinct “sections” only if you confirm (see Q1 below).  
\- • Agent planning (tool selection order):  
  \- Broad qualitative → parallel Search across News \+ Reports \+ Memos → synthesize → cite.  
  \- Quantitative → Analyst (Semantic View) first → optional follow-up Search for quotes.  
  \- Company-specific qualitative → Earnings Calls first → then News or Memos as needed.  
  \- Mixed intent → Search for context → Analyst to quantify → final synthesis with citations.  
\- • Database & objects:  
  \- Dedicated demo database (see Q4 for naming).  
  \- \`RAW\_DATA\` for base tables; \`ANALYTICS\` for Search services \+ one Semantic View.  
  \- Semantic View exposes sector, company, reporting period; metrics: revenue, COGS, gross margin %, revenue growth; includes COMMENTS and WITH SYNONYMS.  
\- • Configurability:  
  \- Volumes per source, history lengths, model names, random seed, Swedish fraction %, index refresh cadence.

\#\#\# 4-step interactive demo flow (Snowflake Intelligence UI)  
\- • Step 1 (Qualitative synthesis):  
  \- User: “Summarize the impact of rising inflation on Nordic logistics companies.”  
  \- Tools: FACTSET\_NEWS\_SEARCH \+ MCBAINCG\_REPORTS\_SEARCH \+ INTERNAL\_MEMOS\_SEARCH in parallel.  
  \- Response: 1-paragraph summary with 3–5 bullets; citations like \[Headline\] (Factset, 2024-11).  
\- • Step 2 (Quantitative follow-up):  
  \- User: “Compare gross margins over the last 6 quarters for the top 3 logistics firms.”  
  \- Tools: Cortex Analyst (Semantic View) to compute and chart; short textual takeaway.  
\- • Step 3 (Executive commentary):  
  \- User: “Quote what management said about pricing power for ‘Nordic Freight Systems’.”  
  \- Tools: QUARTR\_EARNINGS\_CALLS\_SEARCH filtered by company; return quotes with citations.  
\- • Step 4 (Cross-source insight):  
  \- User: “Do recent consultant reports agree with management’s pricing claims? Summarize briefly.”  
  \- Tools: MCBAINCG\_REPORTS\_SEARCH \+ GUIDEPOINT\_TRANSCRIPTS\_SEARCH; synthesize with citations.

\#\#\# Search service column mapping (functional)  
\- • FACTSET\_NEWS\_FEED: ID=ARTICLE\_ID, TITLE=HEADLINE, CONTENT=ARTICLE\_BODY, ATTRIBUTES=PUBLISH\_TIMESTAMP,SOURCE,COMPANY\_ID?  
\- • GUIDEPOINT\_EXPERT\_TRANSCRIPTS: ID=TRANSCRIPT\_ID, TITLE=EXPERT\_PROFILE (or generated title), CONTENT=TRANSCRIPT\_TEXT, ATTRIBUTES=INTERVIEW\_DATE,COMPANY\_ID?  
\- • MCBAINCG\_CONSULTANT\_REPORTS: ID=REPORT\_ID, TITLE=TITLE, CONTENT=REPORT\_BODY, ATTRIBUTES=PUBLISH\_DATE,EXECUTIVE\_SUMMARY,COMPANY\_ID?  
\- • QUARTR\_EARNINGS\_CALLS: ID=CALL\_ID, TITLE=‘Earnings Call — \<Company\> — \<Quarter\>’, CONTENT=TRANSCRIPT\_JSON, ATTRIBUTES=COMPANY\_ID,CALL\_TIMESTAMP  
\- • INTERNAL\_INVESTMENT\_MEMOS: ID=MEMO\_ID, TITLE=SUBJECT (or generated), CONTENT=MEMO\_BODY, ATTRIBUTES=CREATION\_DATE,AUTHOR,SUBJECT\_COMPANIES

\#\#\# Swedish news provider (pick one)  
\- • SnöDirekt  
\- • SnöNyheter  
\- • SnowWire Nordics

\#\#\# Final follow-ups  
\- • Q1: You chose “No chunking” but also answered “Yes” to semantic sectioning. Confirm: should we apply semantic sectioning only for very long docs (reports/transcripts) while leaving others unchunked?  
\- • Q2: Claude 4.0 for the Agent: if not available in your region/account, what fallback should we set? Suggest: llama3.1-70b.  
\- • Q3: What fraction of Swedish news items should we target (e.g., 10–20%)?  
\- • Q4: Preferred database name? Options: \`INVESTOR\_THEMES\_DEMO\_DB\`, \`INDUSTRIAL\_RESEARCH\_DEMO\_DB\`, or provide yours.  
\- • Q5: Warehouse size for setup/run (XS/S/M)? Suggest XS for generation, S for indexing/agent responsiveness given 18 quarters \+ full unstructured.  
\- • Q6: Any specific fictional company names you want to feature in logistics, or should we generate all?  
\- • Q7: Do you want deterministic regeneration (fixed random seed) for reproducibility across demos?

If you confirm Q1–Q7 and pick a Swedish provider \+ database name, I’ll finalize the functional design doc and outline the lean technical tasks for the build phase (still design-only).

My Answer:  
Swedish news provider : SnowWire Nordics  
Final follow-ups  
Q1: We will generate all unstructured data and store that in a VARCHAR column in the target table, you should also make sure it is generated with mardown when the data would have a layout.  
Q2: It is avalible, for Agent you should only create setup instructions since we set it up manually in SNowsight  
Q3: 10%  
Q4: THEMES\_RESEARCH\_DEMO  
Q5: Use a predifined name for warehouse in this case COMPUTE\_WH  
Q6: Generate all  
Q7: Use a seed, and data that is needed to answer the questions must always exist  after we recreate the data ie so if a questions is using a company name then we need to make sure we always generated data for that company name.

Please ask any follup questions you might have.  
Do not start coding or create files until I tell you so.  
