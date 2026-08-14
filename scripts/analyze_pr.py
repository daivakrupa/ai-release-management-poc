import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
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
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "Return only valid JSON. No markdown."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

result = response.choices[0].message.content.strip()

try:
    data = json.loads(result)
    print(json.dumps(data))
except Exception:
    print(json.dumps({"label": "enhancement"}))
