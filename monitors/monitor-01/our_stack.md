# `our_stack`

The Monitor 01 AI stack. Consumed by the ranker for in-stack triggers. Reviewed at least quarterly. Versioned changelog at the bottom.

> **Framing:** Prosus is unusual in that its AI stack is both a **consumption stack** (using foundation models and infrastructure from third parties) and a **production stack** (building its own commerce-specialised models, agent platform, and orchestration layer that it sells access to within the portfolio). That matters for Monitor 01 because each persona has to track two categories of vendor risk: classic upstream dependency (what happens if OpenAI deprecates a model we use) and **downstream platform liability** (what happens when iFood's LCM is the system on the hook under the EU AI Act or Brazilian ANPD scrutiny). Both flip on the in-stack rank rules.
>
> **Confidence levels:** `high` = corroborated across multiple primary sources including Prosus's own communications. `medium` = single-source or inferred from public architecture writeups. `low` = likely but unconfirmed. `[shortlist]` = publicly signalled but not yet confirmed adopted.

---

## Layer 1 — Foundation models (third-party, consumed via API)

- **Anthropic Claude family** — `high` confidence. Confirmed in production via iFood Ailo WhatsApp assistant (hybrid Anthropic/OpenAI/AWS architecture). **Claude Opus 4.6** specifically named in Prosus's own "State of AI Agents 2026" piece. All Claude models (Opus, Sonnet, Haiku across versions) and Anthropic API endpoints are `our_stack`.
- **OpenAI GPT family** — `high` confidence. Confirmed in production across Toqan and iFood Ailo. OLX Magic uses commercial LLMs in a model-router pattern that almost certainly includes OpenAI. **GPT-5.3-Codex** named as tracked frontier release. All OpenAI GPT models and APIs are `our_stack`.
- **AWS Bedrock + Amazon-native models** — `high` confidence. Confirmed via three-year **Global Partnership Agreement** signed February 2026 covering iFood, OLX, PayU, Despegar, eMag, JET, and via Ailo's three-vendor architecture explicitly naming AWS. Includes **Amazon Nova family models**, Titan embeddings, and any Bedrock-hosted third-party models accessed via AWS.
- **Alibaba Qwen (open-source)** — `high` confidence. **Confirmed as the foundation Prosus fine-tunes on top of for the LCM.** iFood CEO Diego Barreto: "LCM is integrated with the open-source QwQ3 model with 32 billion parameters, incorporating Reinforcement Learning steps with structured feedback, automatic checkers, and fine-tuning."

  > **Single most important entry on the list for Monitor 01.** Ties Prosus's flagship proprietary AI system directly to a Chinese-origin open-source model. Implications across all four domains:
  > - **AI News:** US export controls on Chinese AI
  > - **Privacy:** cross-border training data flows
  > - **IP:** open-source licence compliance, especially Qwen licence terms
  > - **Legal ops:** vendor due diligence on Chinese-origin model components

- **DeepSeek models** — `[shortlist]`. Prosus's Global Head of AI publicly commented on DeepSeek significance in industry interviews; not confirmed in production deployments. Track for AI-news persona purposes.
- **Other open-source models (Llama, Mistral)** — `medium` confidence. Prosus has signalled extensive open-source experimentation (AgentOps landscape work); treat as `our_stack` pending confirmation — industry-standard alternatives almost certainly present in experiments.

---

## Layer 2 — Proprietary models built on top

### Large Commerce Model (LCM)

`high` confidence. Prosus's **flagship in-house model**. Built on QwQ3 32B with RL and fine-tuning. **Trained on 10 trillion tokens of commercial transaction data from 500M+ users across the portfolio. Processes 200B tokens daily.** Originally developed at iFood; now trained across the portfolio (iFood, OLX, eMAG, Despegar).

> **The LCM is both a `our_stack` entry AND a regulated artefact.** Under the EU AI Act, depending on how it's classified (general-purpose vs. high-risk recommender), it carries **developer obligations on Prosus, not just deployer obligations**. AI persona should treat any EU AI Act, GPAI Code of Practice, or recommender-system guidance as **automatically Rank A** because the LCM is squarely in scope.

### Ailo

`high` confidence. iFood's **WhatsApp-based conversational assistant** powered by LCM plus the hybrid Anthropic/OpenAI/AWS layer. Consumer-facing; processes personal data at scale; deployed via Meta's WhatsApp infrastructure (relevant for both privacy and the Meta-as-channel dependency — see Layer 7).

### OLX Magic

`high` confidence. OLX's **conversational shopping assistant** with multi-modal input (text, image, voice), **semantic+keyword hybrid search**, model-router pattern over commercial and fine-tuned models, traditional ML (learning-to-rank) underneath. Tools include web search, text search, visual search, URL parsing.

---

## Layer 3 — Agent platform and orchestration

### Toqan

`high` confidence. Prosus's **in-house agent development platform**. Originally rolled out 2022. Now runs **30,000+ to 37,000+ agents** across the portfolio. LLM-agnostic by design; routes across multiple foundation models. Integrates with Slack as primary engineering access layer, plus web and API surfaces. Agentic framework decomposes user requests into parallelisable sub-tasks.

> **Toqan is both a `our_stack` entry AND a platform-level system.** AI Act and ANPD enforcement that addresses agentic systems or autonomous decision-making touches Toqan **directly** even when no specific portfolio company is named.

- **Toqan Data Analyst sub-agent** — confirmed specialised agent within the Toqan family; `high` confidence.

---

## Layer 4 — Third-party agent infrastructure consumed

- **Anthropic Agent SDK + Claude Managed Agents** — `medium-high` confidence. Confirmed at minimum as tracked frontier infrastructure in Prosus's own commentary; multi-vendor Ailo architecture strongly suggests Anthropic agentic tooling is in production.
- **Anthropic Agent Skills (open standard)** — `[shortlist]`. Anthropic released as open standard late 2025; Prosus's stated direction toward MCP and standardised agent tooling makes this a track-as-adopted entry.
- **Model Context Protocol (MCP)** — Anthropic-originated, now industry standard for agent-tool communication. Prosus's AgentOps thinking explicitly tracks this category. `medium` confidence as in-production; `high` confidence as tracked dependency.
- **OpenAI Agents SDK** — released March 2025; given OpenAI is in the hybrid stack, treat as `[shortlist]` / track-as-adopted.
- **LangGraph, CrewAI, AutoGen, Google ADK** — explicitly surveyed in Prosus's own AgentOps landscape work. Treat as `medium` confidence tracked infrastructure; **30k+ agent count means at least one is in production somewhere**.

---

## Layer 5 — Infrastructure and cloud

- **Amazon Web Services** — `high` confidence. **Confirmed primary cloud partner under the February 2026 three-year Global Partnership Agreement** covering iFood, OLX, PayU, Despegar, eMag, and JET. Includes Bedrock, SageMaker, S3, EC2/Fargate, and AWS's AI infrastructure stack. **AWS changes — model deprecations, region availability, ToS updates, breach incidents — are Rank A operational triggers under the existing rank rules.**
- **Microsoft Azure** — `[shortlist]` / partial. Some portfolio companies historically used Azure (Stack Overflow's Microsoft acquisition history; some European operations); not confirmed under the new AWS-centric standardisation.
- **Google Cloud Platform** — `[shortlist]`. Likely present somewhere in venture portfolio companies; not confirmed as Prosus-level infrastructure.
- **On-premises / private data centres** — not confirmed at material scale; AWS partnership suggests cloud-primary posture.

---

## Layer 6 — Data infrastructure

- **Vector databases** — `medium` confidence that some vector database is in `our_stack`; **specific vendor TBC**. Confirmed via OLX Magic's hybrid semantic + keyword search architecture; specific vendor (Pinecone, Weaviate, pgvector, Elasticsearch-with-vectors, OpenSearch) not publicly disclosed.
- **Elasticsearch / OpenSearch** — `high` confidence. Confirmed in OLX Magic's tech stack via public LLMOps writeups.
- **FastAPI** — `high` confidence. Confirmed as part of OLX Magic's serving infrastructure.
- **Snowflake, Databricks, BigQuery** — `[shortlist]` given industry norms.

---

## Layer 7 — Channel and distribution dependencies

- **WhatsApp / Meta** — Ailo is distributed via WhatsApp. **Meta is therefore a critical channel dependency.** Any Meta policy change, WhatsApp Business API change, or Meta-side regulatory action affects iFood operationally. **Rank A in-stack trigger.**
- **App stores (Apple App Store, Google Play)** — distribution dependency for every consumer-facing Prosus app. Any platform-level AI policy change (Apple's on-device AI rules, Google's Play AI policy) is an in-stack trigger.
- **Slack** — confirmed as primary internal access channel for Toqan among engineering teams; AI persona should track Slack / Salesforce policy on enterprise AI access.

---

## Layer 8 — AI safety, evaluation, and ops tooling

- **Internal feedback / hallucination tracking** — Prosus runs a documented evaluation regime including the **"Pinocchio" reaction button for hallucination flagging**. In-house tooling rather than a vendor, but worth noting as `our_stack` because guidance from regulators on AI evaluation methodologies (**NIST AI RMF, ISO/IEC 42001 audits, ICO audit frameworks**) plug directly into this layer.
- **Snorkel, Scale AI, Surge, Weights & Biases, LangSmith, Langfuse** — not confirmed in public sources; treat as `[shortlist]` given Prosus's documented engagement with the AgentOps landscape.

---

## Layer 9 — Prosus Ventures AI portfolio (track-as-vendor)

Prosus has explicitly stated **30+ investments in AI-native ecommerce startups** plus broader AI ventures. These appear in Monitor 01 differently from operating-company exposure: they're not `our_stack` in the consumption sense, but events affecting them trigger group-level disclosure obligations and AI-news persona attention.

Notable named entries from public portfolio listings:
- **Advolve.AI** (acquired by iFood 2025)
- **Arivihan**
- Plus the broader Prosus Ventures AI book

**The AI persona should treat material events at any AI-portfolio company as in-stack for intelligence purposes** even when not in-stack for consumption purposes.

---

## In-stack rank rule additions

The base rule from `ranking-criteria.md` ("`trigger_type = vendor_change` AND vendor is in our stack → Rank B; `breach_incident` with stack involvement → Rank A") applies to every `high` confidence entry above. Three operational notes for the ranker:

### Note 1 — multi-vendor architecture lowers urgency for single-vendor events

If Anthropic deprecates a Claude model and Prosus's stack also has OpenAI + AWS Nova + Qwen alternatives, the deprecation is **Rank B, not Rank A**. The ranker should look at whether a stack event affects a **capability** (e.g. all multimodal vision endpoints) versus a **single vendor**. Single-vendor disruptions are recoverable; capability-class disruptions are not.

### Note 2 — Qwen / Chinese-origin model events are upgraded

Any event affecting Qwen specifically, or affecting **US export controls on Chinese AI**, or affecting Alibaba's open-source licensing posture, is **automatically Rank A** because LCM has a direct dependency. This is the AI-stack analogue of the Tencent-attribution rule (Block 2 / `ranking-criteria.md` Rule 6): a specific named exposure deserves automatic priority even when severity assessment is moderate.

### Note 3 — Toqan and LCM as regulated artefacts

The AI persona must read regulatory developments (**EU AI Act conformity assessments, NIST AI RMF updates, ANPD AI guidance, ICO AI audits, CNIL recommender system positions**) with the understanding that **Prosus is itself a developer of GPAI-adjacent and high-risk-adjacent systems**, not only a deployer. This shifts the materiality threshold **downward** for any regulatory development that addresses model developer obligations.

---

## Change log

| Date       | Change                                                                                                              | Author   |
|------------|---------------------------------------------------------------------------------------------------------------------|----------|
| 2026-05-12 | Initial 9-layer stack — foundation models, proprietary models (LCM, Ailo, OLX Magic), Toqan, agent infra, AWS, data infra, channels, ops tooling, ventures. Three in-stack rank notes added. | Operator |
