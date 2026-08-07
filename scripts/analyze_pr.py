import os
import json
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
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

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=prompt
)

print(response.text)
