# `our_stack`

> **[DRAFT — confirm with operator (Anne-Claire); single source of truth shared with Monitor 01]**
>
> **Framing for Monitor 02 (competition lens):** the Prosus AI stack is the same vendor list as Monitor 01's, but Monitor 02 reads it through a different lens. Where Monitor 01 reads dependencies (what happens if OpenAI deprecates a model we use, what happens when iFood's LCM is the regulated artefact), Monitor 02 reads **shared infrastructure as competition risk** — specifically:
>
> - **Hub-and-spoke risk** — when two or more competitors use the same vendor and that vendor sees both, the vendor becomes a potential hub. The doctrine is at the academic-leading stage (the 2022 Skadden article Anne-Claire co-authored on pricing algorithms touches this); the agency-leading stage is approaching.
> - **Information-exchange risk** — competitor-sensitive information may flow through shared infrastructure (cloud, payments, AI model providers) in ways that could be characterised as exchange under Article 101 if a forum or pattern of sharing emerges.
> - **Algorithmic alignment risk** — common pricing intermediaries, common recommender systems, or common foundation models could produce coordinated outcomes that some agencies are increasingly willing to characterise as tacit collusion via algorithm.
> - **Self-preferencing reading (Article 102)** — for the OpCs where dominance is plausible, the use of LCM-driven recommendation, OLX Magic ranking, eMAG own-brand prioritisation against marketplace sellers is the live edge of the self-preferencing-as-abuse doctrine (Google Shopping progeny).
>
> Single source of truth for the underlying vendor list sits with the canonical `monitors/monitor-01/our_stack.md`. This file mirrors that content and adds the competition-lens annotations. **If the underlying vendor list is updated in Monitor 01's `our_stack.md`, it must be mirrored here.** Quarterly review per `operating-preferences.md` confirms parity.

---

## Layer 1 — Foundation models (third-party, consumed via API)

The competition-lens read on Layer 1 turns on whether multiple Prosus OpCs *and competitors of those OpCs* share the same foundation-model provider, creating potential hub-and-spoke vectors.

- **Anthropic Claude family** — `high` confidence in Prosus stack via iFood Ailo. Competition-lens question: do competitors (Uber Eats, Deliveroo, DoorDash) also use Claude via Anthropic API? If yes, Anthropic is a shared intermediary handling competitor data; hub-and-spoke vector is live.
- **OpenAI GPT family** — `high` confidence via Toqan, Ailo, OLX Magic. Same competition-lens question. OpenAI's enterprise contracts typically include data-isolation clauses but the broader question of inference-side metadata visibility is unsettled.
- **AWS Bedrock + Amazon-native models** — `high` confidence under the February 2026 Global Partnership Agreement. Particularly important hub-and-spoke vector because AWS is also the cloud provider for many platform competitors.
- **Alibaba Qwen (open-source)** — `high` confidence. LCM is fine-tuned on QwQ3 32B. Open-source nature partially mitigates the hub-and-spoke concern (Alibaba doesn't see inference) but doesn't eliminate it (Alibaba may see traffic-side metadata if the model is hosted on Alibaba Cloud infrastructure).
- **DeepSeek models** — `[shortlist]`. Track for competition-lens reasons in case Chinese-origin models become subject to US-style data-flow rules under FSR or sectoral regulation.
- **Other open-source models (Llama, Mistral)** — `medium` confidence in Prosus stack; open-source reading reduces direct hub-and-spoke risk but the question of fine-tuning data sharing remains.

---

## Layer 2 — Proprietary models built on top

The competition-lens read on Layer 2 turns on **self-preferencing under Article 102** for OpCs plausibly dominant in their markets, and on **ecosystem theories of harm under merger control** for any deal involving an OpC that operates a flagship proprietary model.

### Large Commerce Model (LCM)

`high` confidence. Prosus's **flagship in-house model**. Built on QwQ3 32B with RL and fine-tuning. Trained on 10 trillion tokens of commercial transaction data from 500M+ users across the portfolio. Processes 200B tokens daily. Originally developed at iFood; now trained across the portfolio.

> **Competition-lens read:** The LCM is the operational substrate for cross-OpC recommendation. The doctrinal questions are (a) whether LCM-driven recommendation on iFood, OLX, Despegar, or eMAG constitutes self-preferencing under Article 102 in markets where the relevant OpC is plausibly dominant; (b) whether the cross-OpC training data flow constitutes information exchange under Article 101 between adjacent-market sister companies; and (c) whether any future deal reinforcing the LCM/ecosystem architecture will attract conglomerate-effects analysis under EUMR.

### Ailo

`high` confidence. iFood's WhatsApp-based conversational assistant.

> **Competition-lens read:** Ailo's exclusive relationship with iFood's restaurant supply (and its potential use to influence restaurant or consumer choice) is the live edge of self-preferencing doctrine in the food-delivery market. iFood Brazil is plausibly dominant; the CADE TCC from 2023 already restricts exclusivity arrangements; future agency attention to AI-mediated demand-shaping is a forward-looking risk.

### OLX Magic

`high` confidence. OLX's conversational shopping assistant.

> **Competition-lens read:** OLX Magic's ranking is the operational substrate for the self-preferencing question on OLX's classifieds platforms (particularly OLX Brasil and OLX Polska, where dominance is plausible). The line between unilateral algorithmic optimisation and self-preferencing-as-abuse is being drawn right now in the Google Shopping / Google Ad Tech progeny.

---

## Layer 3 — Agent platform and orchestration

### Toqan

`high` confidence. Prosus's in-house agent platform; 30,000+ agents.

> **Competition-lens read:** Toqan is a substantial cross-portfolio coordinator. The doctrinal question is whether agentic decision-making across multiple OpCs raises information-exchange concerns if the agents share data or learning across the portfolio in ways that could be characterised as competitor-data sharing. Currently not a frontline doctrine, but in the academic literature.

---

## Layer 4 — Third-party agent infrastructure consumed

- **Anthropic Agent SDK + Claude Managed Agents** — Anthropic-hub-and-spoke read.
- **Model Context Protocol (MCP)** — industry standard for agent-tool communication.
- **OpenAI Agents SDK** — OpenAI-hub-and-spoke read.
- **LangGraph, CrewAI, AutoGen, Google ADK** — multiple potential hubs; competition-lens read tracks which Prosus competitors use the same frameworks.

---

## Layer 5 — Infrastructure and cloud

- **Amazon Web Services** — primary cloud partner. AWS is also the cloud provider for many competitor platforms; classic hub-and-spoke vector.

> **Competition-lens specific note:** AWS sees infrastructure-level signals about competitor activity through its standard provider relationship. The line between provider-of-cloud-services and hub-of-competitor-data is doctrinally unsettled; agency action on cloud-as-hub would be a frontline development.

- **Microsoft Azure**, **Google Cloud Platform** — partial / venture-portfolio presence.

---

## Layer 6 — Data infrastructure

- **Vector databases** (vendor TBC) — competition-lens read tracks whether vector-database vendors operate at industry-shared scale.
- **Elasticsearch / OpenSearch, FastAPI, Snowflake, Databricks, BigQuery** — standard data infrastructure; lower competition-lens priority unless an industry-specific data-pooling pattern emerges.

---

## Layer 7 — Channel and distribution dependencies

- **WhatsApp / Meta** — Ailo distribution via WhatsApp. Meta is a critical channel and also a **DMA-designated gatekeeper**. Any Meta DMA enforcement, Article 102 exposure, or business-user obligations are Rank A in-stack triggers for Monitor 02 per Rule 18 (DMA designation auto-rank).
- **App stores (Apple, Google Play)** — both DMA-designated gatekeepers. Same Rank A trigger.
- **Slack, Salesforce** — internal channel dependency; lower competition-lens priority.

---

## Layer 8 — AI safety, evaluation, and ops tooling

Lower competition-lens priority than Layers 1, 2, 5, 7. The Pinocchio internal tooling sits inside Prosus, no competition vector.

---

## Layer 9 — Prosus Ventures AI portfolio

`high` confidence. 30+ AI-ecommerce startups.

> **Competition-lens read:** the venture book is the demand side of the killer-acquisition concern under merger control (Rule 16 — below-threshold call-in auto-rank). Any acquisition from the venture book into a controlled OpC is potentially in scope for Article 22 EUMR referral, CMA discretionary call-in, BKartA §39a, or comparable below-threshold mechanisms. The Cunningham/Ederer/Ma academic literature on killer acquisitions reads through to this book directly.

---

## In-stack competition rank rule additions

The base rules from `ranking-criteria.md` Rules 9–21 apply. Two operational notes for the ranker specific to in-stack reading:

### Note 1 — Hub-and-spoke promotion

If a development concerns a shared-infrastructure vendor used by Prosus AND a competitor of Prosus, and the development concerns information flow, data isolation, or competitor-data handling, the rank is promoted **one tier**. This is a sub-rule of the general competition-lens framing and applies even where the development is not yet at agency-decision stage.

### Note 2 — DMA-gatekeeper-as-vendor double-trigger

When a DMA-designated gatekeeper (Google, Apple, Meta, Amazon, Microsoft, ByteDance, Booking Holdings) is in our stack and the development concerns that gatekeeper's DMA compliance, the development triggers both Rule 18 (DMA designation auto-rank, Rank A) AND the in-stack hub-and-spoke read above. Result: Rank A automatic, with Anne-Claire AND the relevant OpCo GC in the escalation chain.

### Note 3 — LCM / Toqan as ecosystem artefact for merger purposes

For any merger control finding where Prosus is a notifying party, the LCM and Toqan are read as ecosystem-architecture inputs. Conglomerate-effects analysis on Prosus mergers will rely on the LCM/ecosystem read; any precedent on EUMR ecosystem theories that affects portfolio-based undertakings is Rank A material.

---

## Change log

| Date       | Change | Author |
|------------|--------|--------|
| 2026-05-13 | Initial Monitor 02 mirror of Monitor 01's `our_stack.md` with competition-lens annotations added at each layer. Single source of truth for underlying vendor list remains in Monitor 01. Pending Anne-Claire's Block 1 redline. | K. Maleevska |
