import os
import asyncio
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.runners import InMemoryRunner

# ==========================================
# 1. ENVIRONMENT CONFIGURATION & API KEYS
# ==========================================
# Resolve paths relative to this script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, "..", ".env")

# Load environment variables from the .env file
load_dotenv(dotenv_path=dotenv_path)

# Retreive GOOGLE_API_KEY from environment/dotenv
google_api_key = os.getenv("GOOGLE_API_KEY")

# Set the key as GEMINI_API_KEY which the google-adk (via google-genai) expects
if google_api_key:
    os.environ["GEMINI_API_KEY"] = google_api_key


# ==========================================
# 2. LOAD SKILL GUIDELINES & REF SCHEMES
# ==========================================
# Paths to skill and schemes documentation
skill_path = os.path.abspath(os.path.join(current_dir, "..", "skills", "subsidy_eligibility", "SKILL.md"))
schemes_path = os.path.abspath(os.path.join(current_dir, "..", "skills", "subsidy_eligibility", "references", "schemes.md"))

# Read the plain text content of both files at startup
try:
    with open(skill_path, "r", encoding="utf-8") as f:
        skill_content = f.read()
except FileNotFoundError:
    skill_content = "Skill configuration file not found."

try:
    with open(schemes_path, "r", encoding="utf-8") as f:
        schemes_content = f.read()
except FileNotFoundError:
    schemes_content = "Schemes reference file not found."


# ==========================================
# 3. AGENT DEFINITION & SYSTEM INSTRUCTION
# ==========================================
# Build the comprehensive instruction context for the agent
system_instruction = (
    "You are a helpful assistant named 'kisanmitra' that helps Indian farmers discover relevant government subsidy schemes.\n"
    "Guidelines:\n"
    "- Ask for missing details one at a time: state, land size, primary crop, and farmer category (small/marginal/other).\n"
    "- Never claim guaranteed eligibility; only state that the farmer is 'likely eligible' or 'may qualify'.\n"
    "- Never ask for sensitive personal identifiers (Aadhaar number, bank account number, PAN number, etc).\n\n"
    f"=== SKILL PROTOCOL (SKILL.md) ===\n{skill_content}\n\n"
    f"=== ELIGIBILITY REFERENCE (schemes.md) ===\n{schemes_content}\n"
)

# Instantiate the single Kisanmitra Agent using gemini-3-flash-preview
agent = Agent(
    name="kisanmitra",
    model="gemini-3-flash-preview",
    instruction=system_instruction
)


# ==========================================
# 3.5. SECURITY GUARDRAILS (OUTPUT FILTER)
# ==========================================
def check_output_safety(text: str) -> tuple[bool, str | None]:
    """
    Independent, code-level safety check that intercepts and validates the agent's
    output text. This acts as a reliable secondary defense mechanism that runs locally
    and does not rely solely on system instruction compliance.
    """
    # 1. Define list of forbidden terms (case-insensitive)
    forbidden_terms = ["aadhaar", "pan number", "bank account number", "otp"]
    
    # 2. Define list of overconfident phrases (case-insensitive)
    overconfident_phrases = ["guaranteed", "you will definitely get", "100% eligible", "certainly eligible"]
    
    text_lower = text.lower()
    
    # 3. Scan the input text for forbidden terms
    for term in forbidden_terms:
        if term in text_lower:
            return False, "blocked_sensitive_request"
            
    # 4. Scan the input text for overconfident phrases
    for phrase in overconfident_phrases:
        if phrase in text_lower:
            return False, "blocked_overconfidence"
            
    # 5. Passed safety validation
    return True, None


# ==========================================
# 4. INTERACTIVE COMMAND-LINE LOOP
# ==========================================
async def run_cli():
    """Asynchronous command line loop for testing the agent interactively."""
    # Use InMemoryRunner to run the agent session
    runner = InMemoryRunner(agent=agent)
    
    print("==================================================")
    print("      Kisanmitra Subsidy Assistant (CLI)          ")
    print(" Type 'quit' or 'exit' to end the session.       ")
    print("==================================================")
    
    # We maintain conversation history by keeping the same session_id
    session_id = "kisanmitra_interactive_session"
    
    while True:
        try:
            # Get user message
            user_input = input("\nYou > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting interactive loop...")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
            
        # Run the agent in quiet mode to handle the response formatting manually
        events = await runner.run_debug(
            user_messages=user_input,
            session_id=session_id,
            quiet=True
        )
        
        # Concatenate text response parts from 'kisanmitra' agent
        agent_reply = ""
        for event in events:
            if event.author == "kisanmitra" and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        agent_reply += part.text
                        
        # Display the response
        if agent_reply:
            # Run code-level safety guardrail check
            is_safe, trigger_reason = check_output_safety(agent_reply)
            if not is_safe:
                print(f"\n[GUARDRAIL TRIGGERED]: {trigger_reason}")
                print("\nKisanmitra > I need to rephrase that response to stay within safety guidelines. Could you ask that again?")
            else:
                print(f"\nKisanmitra > {agent_reply}")
        else:
            print("\nKisanmitra > (No response returned by the agent)")


if __name__ == "__main__":
    asyncio.run(run_cli())
