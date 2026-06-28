# Subsidy Eligibility Skill

## Description
Use this skill whenever a farmer asks about government subsidies, schemes, financial
support, loans, insurance, or assistance for farming. This includes questions like
"what subsidies can I get", "help me find a scheme", "I have X acres and grow Y crop,
what can I apply for", or similar.

## When to use this skill
Trigger this skill when the user's message is about discovering or checking eligibility
for Indian government agricultural schemes. Do NOT trigger this skill for general farming
advice (like crop disease or weather) — only for subsidy/scheme/financial support questions.

## Instructions
1. If the farmer has not yet provided their state, land size, primary crop, and farmer
   category (small/marginal/other), ask for whichever of these are missing, one short
   question at a time. Do not ask for all of them at once.
2. Once you have enough information, refer to references/schemes.md to check eligibility
   against each scheme's conditions.
3. Only state that a farmer "appears eligible" or "may qualify" — never state eligibility
   as a guaranteed fact, since you are not an official verification system.
4. For each matching scheme, explain in plain, simple language:
   - What the scheme offers
   - Why it matched their situation
   - What to do next (which portal or office to approach)
5. If no schemes clearly match, say so honestly rather than guessing or forcing a match.
6. Never ask for sensitive personal identifiers (Aadhaar number, bank account number, etc).
   This skill only needs state, land size, crop, and farmer category.