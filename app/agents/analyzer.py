import json

from app.services.llm import ask_llm


def analyze_job(job):

    prompt = f"""
You are an expert AI career advisor.

Analyze the following job posting.

Return ONLY valid JSON.

{{
    "category": "",
    "score": 0,
    "should_apply": false,
    "reason": ""
}}

Job Title:
{job.get("position")}

Company:
{job.get("company")}

Location:
{job.get("location")}

Description:
{job.get("description")}
"""

    response = ask_llm(prompt)

    # Remove markdown code blocks if Gemini returns them
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "category": "Unknown",
            "score": 0,
            "should_apply": False,
            "reason": response
        }