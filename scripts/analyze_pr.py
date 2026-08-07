import os
import json
from google import genai

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

title = os.environ["PR_TITLE"]
body = os.environ.get("PR_BODY", "")

prompt = f"""
Analyze this PR.

Title:
{title}

Description:
{body}

Classify as one of:

feature
bug
enhancement
security

Return JSON:

{{
  "label":"",
  "summary":"",
  "risk":"",
  "deployment_notes":""
}}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)