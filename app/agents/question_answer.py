from app.services.llm import ask_llm


def answer_question(question, job):

    prompt = f"""
You are answering a job application question.

Company:
{job.company}

Job Title:
{job.title}

Job Description:
{job.description}

Question:
{question}

Answer professionally in under 120 words.
"""

    return ask_llm(prompt).strip()