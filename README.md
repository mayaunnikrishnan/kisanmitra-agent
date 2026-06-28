# KisanMitra — AI Agent for Government Subsidy Discovery

KisanMitra ("farmer's friend") is a conversational AI agent that helps Indian farmers
discover which central government agricultural subsidy schemes they are likely
eligible for, based on a short conversation about their land, crop, location, and
farmer category.

Built for the **Kaggle x Google 5-Day AI Agents: Intensive Vibe Coding Course Capstone Project**
(Track: Agents for Good).

---

## The Problem

India runs dozens of agricultural subsidy schemes — PM-KISAN, PMFBY, KCC, PM-KUSUM,
PMKSY, SMAM, and more — collectively supporting tens of millions of farmers. The
schemes themselves are well-documented, but **discovering which ones apply to a
specific farmer is genuinely hard.** Eligibility rules vary by land size, crop,
farmer category, and state, and most farmers either rely on word-of-mouth or give
up navigating government portals not designed for easy discovery.

This is a discovery and translation problem — the information exists publicly, it's
just not matched to the individual who needs it.

## The Solution

KisanMitra asks a farmer a small number of simple questions (state, land size,
primary crop, farmer category), then matches their profile against a curated
knowledge base of major central schemes and explains, in plain language:

- What each matching scheme offers
- Why it matches their specific situation
- What concrete next step to take (which portal or office to approach)

The agent is deliberately cautious — it phrases matches as "likely eligible" or
"may qualify," never as guaranteed fact, since final eligibility is always
determined by the relevant government department after document verification.

**Schemes currently covered:** PM-KISAN, PMFBY, KCC, PM-KUSUM, PMKSY (Per Drop More
Crop), and SMAM. (Central schemes only — state-specific schemes are out of scope
for this version; see Limitations below.)

## Architecture

```
                ┌─────────────────────┐
                │   Farmer (User)      │
                └──────────┬───────────┘
                           │ natural language
                           ▼
                ┌─────────────────────┐
                │   Kisanmitra Agent   │  (Google ADK + Gemini)
                │   - asks clarifying  │
                │     questions        │
                │   - applies skill    │
                │     instructions     │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
    ┌───────────────────┐    ┌───────────────────────┐
    │ Agent Skill         │    │  Code-Level Guardrail  │
    │ subsidy_eligibility  │    │  check_output_safety()│
    │ - SKILL.md (rules)   │    │  - blocks sensitive    │
    │ - schemes.md         │    │    info requests       │
    │   (reference data)   │    │  - blocks overconfident│
    │                       │    │    eligibility claims │
    └───────────────────┘    └───────────────────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │  Plain-language reply│
                │  + next steps        │
                └─────────────────────┘
```

**Design choices:**

- **A single agent, not a multi-agent swarm.** For a bounded task like this, one
  general-purpose agent dynamically using a Skill is simpler and easier to maintain
  than multiple specialized sub-agents.
- **Scheme knowledge lives in an Agent Skill, not the system prompt.** `SKILL.md`
  defines *when and how* to use the knowledge; `references/schemes.md` holds the
  actual eligibility data. This keeps the core prompt lean and means scheme data
  can be updated independently of the agent's logic.
- **A guardrail runs independently of the model's own caution.** The system prompt
  already instructs the model to avoid sensitive data requests and overconfident
  claims — but prompt-level instructions alone can be brittle. `check_output_safety()`
  is a plain Python function that scans every reply before it's shown to the user,
  so safety doesn't rely solely on the model choosing to follow instructions.

## Course Concepts Demonstrated

| Concept | Where It's Implemented |
|---|---|
| **Agent (ADK)** | `agent/main.py` — the core conversational agent, built with Google's Agent Development Kit |
| **Agent Skills** | `skills/subsidy_eligibility/` — scheme knowledge and matching rules, loaded as a dedicated Skill rather than hardcoded into the prompt |
| **Security Features** | `check_output_safety()` in `agent/main.py` — an independent, code-level filter blocking sensitive-data requests and overconfident eligibility claims |

## Folder Structure

```
kisanmitra-agent/
├── agent/
│   └── main.py              # Agent logic, CLI loop, and security guardrail
├── skills/
│   └── subsidy_eligibility/
│       ├── SKILL.md         # When/how the agent should use scheme knowledge
│       └── references/
│           └── schemes.md   # Reference data for 6 major government schemes
├── .env                      # API key (NOT committed — see .gitignore)
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Running

**Requirements:** Python 3.10+, a Google AI Studio API key.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mayaunnikrishnan/kisanmitra-agent.git
   cd kisanmitra-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key:**
   Create a `.env` file at the project root (same level as the `agent/` folder)
   with the following content:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Run the interactive CLI:**
   ```bash
   cd agent
   python main.py
   ```

5. **Try it out** — for example:
   ```
   You > I have 2 acres of land in Kerala and grow tomatoes. I am a marginal farmer.
   ```
   The agent will ask for any missing details, then return a list of likely-matching
   schemes with plain-language explanations and next steps.

   Type `quit` or `exit` to end the session.

### Note on model choice

This project uses `gemini-3-flash-preview`. If you encounter a `429 RESOURCE_EXHAUSTED`
quota error with a different Gemini model, this is typically a Google Cloud project
verification issue (new/unverified projects are capped at a 0 free-tier quota for some
models), not a bug in this code — see [Google's rate limit docs](https://ai.google.dev/gemini-api/docs/rate-limits)
for current guidance.

## Limitations

- Covers 6 major **central** government schemes only — state-specific schemes are
  not yet included, as they vary significantly by state and were out of scope for
  this version's timeline.
- This is a **discovery and guidance tool**, not an official eligibility verification
  system. It does not check a farmer's eligibility against any live government
  database — the agent communicates this clearly and always recommends confirming
  at the relevant official portal or local agriculture office.

## License

This project was built for educational purposes as part of a Kaggle capstone
submission.
