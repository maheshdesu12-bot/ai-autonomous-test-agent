from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create client AFTER loading env
client = OpenAI()

SYSTEM_PROMPT = """
You are an autonomous QA testing agent.

Your goal is to complete testing using tools step by step.

Available tools:

generate_tests → use this FIRST if test_cases do not exist
execute_tests → use this AFTER test_cases exist
search_memory → use this AFTER execution if error exists
analyze_failure → use this AFTER execution if error exists
save_memory → use this AFTER analysis
done → use this when goal is complete

Rules:

If no test_cases in context → generate_tests
If test_cases exist but no execution → execute_tests
If execution error exists → search_memory
If memory searched → analyze_failure
If analysis exists → save_memory
If everything complete → done

Return ONLY tool name.
"""


def decide_next_tool(goal, context):

    prompt = f"""
You are an autonomous QA agent.

GOAL:
{goal}

CURRENT STATE:
{context}

AVAILABLE TOOLS:
- generate_tests → use if test_cases not present
- execute_tests → use if execution not present
- search_memory → use if memory not present AND error present
- analyze_failure → use if analysis not present AND error present
- save_memory → use if memory_saved not present AND analysis present
- done → use if everything complete

RULES:
Never repeat the same tool if its result already exists in state.

Return ONLY tool name.
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text.strip()