import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1"
)

title = os.environ["PR_TITLE"]
body = os.environ.get("PR_BODY", "")

prompt = f"""
Analyze this pull request.

Title:
{title}

Description:
{body}

Classify as EXACTLY one:

feature
bug
enhancement
security

Return ONLY valid JSON:

{{
  "label": ""
}}
"""

response = client.chat.completions.create(
    model="grok-4-fast",
    messages=[
        {
            "role": "system",
            "content": "You are a PR classification assistant. Return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

result = response.choices[0].message.content.strip()

# Validate JSON
try:
    data = json.loads(result)
    print(json.dumps(data))
except json.JSONDecodeError:
    print(json.dumps({"label": "enhancement"}))
