# Kisanmitra Agricultural Subsidy Discovery Agent

Kisanmitra is a helpful conversational assistant built using Google's Agent Development Kit (ADK) and Gemini 2.0 Flash. It helps Indian farmers discover government agricultural subsidy schemes relevant to their profiles.

## Folder Structure

```
kisanmitra-agent/
├── agent/
│   └── main.py              # Main agent logic and interactive CLI loop
├── skills/
│   └── subsidy_eligibility/
│       ├── SKILL.md         # Skill instructions & rules for the agent
│       └── references/
│           └── schemes.md   # Reference data containing major government schemes
├── .env                     # Environment variables (API keys)
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Add API Key**:
   Create or open the `.env` file at the root of the project and add your Google API key:
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. **Run the Interactive CLI**:
   ```bash
   python agent/main.py
   ```
