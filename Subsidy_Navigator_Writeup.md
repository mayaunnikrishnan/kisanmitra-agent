# KisanMitra: An AI Agent for Government Subsidy Discovery
### Subtitle: Helping farmers find the right government schemes without wading through paperwork

**Track:** Agents for Good

---

## 1. The Problem

India runs dozens of central and state-level agricultural subsidy schemes — PM-KISAN for direct income support, PMFBY for crop insurance, KCC for low-interest credit, PM-KUSUM for solar pumps, SMAM for farm machinery, PMKSY for micro-irrigation, and many more. Collectively these programs represent well over a lakh crore rupees in annual support and reach tens of millions of farmers.

The problem isn't that these schemes don't exist — it's that **discovering which ones actually apply to a specific farmer is genuinely hard.** A small farmer in Kerala growing spices on half an acre and a farmer in Punjab running ten acres of wheat qualify for completely different combinations of schemes, with different eligibility rules, different documentation, and different application portals. Most farmers either rely on word-of-mouth, miss schemes entirely, or give up navigating government portals that weren't designed with usability in mind.

This is a discovery and translation problem, not a content problem. The information exists publicly; it simply isn't matched to the individual sitting in front of it.

## 2. Why an Agent — Not Just a Search Tool or a Static FAQ

A static FAQ or a search engine can return scheme names, but it cannot **reason** about a farmer's specific situation. A farmer doesn't think in scheme names — they think in terms of their own land, crop, and constraints ("I have 2 acres and grow tomatoes, can I get help with irrigation?"). 

An agent is the right tool here because the task requires:
- **Multi-turn clarification** — if the farmer's first message is incomplete (e.g., they mention crop but not land size), the agent needs to ask a natural follow-up rather than fail silently.
- **Reasoning over eligibility rules** — matching a farmer's profile against multiple schemes' conditions (land size thresholds, farmer category, crop type, state) is conditional logic best expressed as structured knowledge the agent applies, not a rigid form.
- **Plain-language translation** — converting dense scheme language into a clear next step ("you qualify for X, here's what you need and where to apply") is exactly the kind of generative task LLMs are suited for.

This made it a natural fit for the course's core idea: **Agent = Model + Harness**, where the model reasons over the farmer's situation, and the harness (structured scheme knowledge + guardrails) keeps that reasoning grounded and safe.

## 3. The Solution: KisanMitra

KisanMitra ("farmer's friend") is a conversational agent that:

1. Asks a farmer a small number of simple questions (location/state, land size, primary crop, farmer category — small/marginal/other).
2. Matches their profile against a curated knowledge base of major central government schemes.
3. Returns a short, ranked list of schemes they likely qualify for, in plain language — what the scheme offers, the rough eligibility condition that matched, and the next concrete step (which portal or office to approach).
4. Flags clearly when it is uncertain, rather than guessing — since giving a farmer wrong eligibility information has real consequences.

It intentionally does **not** attempt to be a complete, authoritative eligibility checker covering every state scheme and edge case. Given the one-week build timeline, the goal was a focused, honest, and well-architected agent covering the major central schemes correctly, rather than a sprawling but shaky one covering everything.

### Schemes Covered (initial scope)
- **PM-KISAN** — direct income support for small/marginal landholding farmers
- **PMFBY** (Pradhan Mantri Fasal Bima Yojana) — crop insurance premium subsidy
- **KCC** (Kisan Credit Card) — subsidized short-term credit, with interest subvention
- **PM-KUSUM** — solar pump subsidy for irrigation
- **PMKSY / Per Drop More Crop** — micro-irrigation (drip/sprinkler) subsidy
- **SMAM** — farm mechanization subsidy (tractors, harvesters, etc.)

## 4. Architecture

```
                ┌─────────────────────┐
                │   Farmer (User)     │
                └──────────┬───────────┘
                           │ natural language
                           ▼
                ┌─────────────────────┐
                │   Orchestrator Agent │  (ADK-based)
                │   - asks clarifying  │
                │     questions        │
                │   - calls Eligibility│
                │     Skill            │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌───────────────────┐    ┌───────────────────────┐
    │ Eligibility Skill  │    │  Guardrail / Policy    │
    │ (SKILL.md +         │    │  Layer                │
    │  scheme rules in    │    │  - blocks definitive   │
    │  references/)       │    │    legal/financial      │
    └───────────────────┘    │    promises             │
                              │  - flags low-confidence │
                              │    matches               │
                              └───────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Plain-language reply│
                │  + next steps        │
                └─────────────────────┘
```

**Design rationale:**
- The **Orchestrator Agent** is intentionally a single general-purpose agent rather than a multi-agent swarm — this is a direct application of a Day 3 course concept: for a bounded, well-defined task like this, one agent dynamically loading a skill is simpler and more maintainable than standing up multiple specialized sub-agents.
- Scheme knowledge lives in an **Agent Skill** (a `SKILL.md` file plus a `references/` folder containing scheme eligibility rules), not hardcoded into the system prompt. This keeps the prompt lean and means scheme data can be updated without touching the agent's core logic — a direct application of the **progressive disclosure** principle from Day 3.
- A lightweight **guardrail layer** prevents the agent from stating eligibility with false certainty or providing anything resembling binding legal/financial advice — instead it phrases matches as "likely eligible based on the criteria you shared, please confirm at [portal]." This reflects the Day 4 course principle that agent outputs touching real-world decisions need explicit verification framing, not blind confidence.

## 5. Course Concepts Demonstrated

| Concept | How It's Demonstrated |
|---|---|
| **Agent (ADK)** | The orchestrator agent itself — built using Google's Agent Development Kit, handling the conversational flow and reasoning over farmer input. |
| **Agent Skills** | Scheme eligibility logic and knowledge is packaged as a dedicated Agent Skill (`SKILL.md` + `references/`) rather than baked into the system prompt, loaded only when the eligibility-matching task is triggered. |
| **Security Features** | A guardrail layer enforces that the agent never asserts unverified eligibility as fact, and never requests sensitive identifying information (e.g., Aadhaar number) beyond what's needed for the conversation. |

*(Three concepts were prioritized for depth rather than spreading thinly across all six, in line with the evaluation criteria's "at least three" requirement.)*

## 6. Implementation Notes

- Built using Google's Agent Development Kit (ADK) as the core agent framework.
- Scheme data was compiled from publicly available government sources (PM-KISAN, PMFBY, KCC, PM-KUSUM, PMKSY, and SMAM official scheme details) and structured into the Skill's reference files.
- The agent's eligibility matching is deliberately conservative: when a farmer's input doesn't clearly satisfy a scheme's stated criteria, the agent says so rather than guessing.
- No API keys, credentials, or personal farmer data are stored or logged by the system.

## 7. Limitations and Honest Scope

This project covers six major **central** government schemes. It does not yet cover state-specific schemes, which vary widely and would require significantly more research time than was available. It also does not verify a farmer's actual eligibility with any government database — it is a **discovery and guidance tool**, not an official eligibility determination system, and the agent communicates this clearly to the user. These are deliberate scoping decisions made to ship a focused, correctly-functioning agent within the project timeline, rather than an overextended one.

## 8. What This Project Demonstrates

KisanMitra shows how a single, well-architected agent — built on a clear separation between reasoning (the model), domain knowledge (an Agent Skill), and safety (a guardrail layer) — can turn a genuinely confusing real-world discovery problem into a short, honest conversation. The same architecture pattern (orchestrator + skill + guardrail) generalizes well beyond agriculture to any domain where public information exists but isn't matched to the individual who needs it.

---

*Built as part of the Kaggle x Google 5-Day AI Agents: Intensive Vibe Coding Course Capstone Project.*
