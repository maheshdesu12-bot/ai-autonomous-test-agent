from openai import OpenAI
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def heal_selector_with_llm(dom_html, failed_selector, element_name):

    prompt = f"""
You are an expert QA automation engineer.

The selector failed:
{failed_selector}

Element name:
{element_name}

Here is the DOM:
{dom_html[:5000]}

Find the BEST selector for this element.

Return ONLY valid CSS selector.

Priority order:
1. data-test
2. id
3. name
4. placeholder
5. type
6. class

Return JSON:

{{
  "selector": "value"
}}
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[
            {"role": "system", "content": "You are selector healing expert"},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content

    try:
        result = json.loads(text)
        return result["selector"]
    except:
        return None