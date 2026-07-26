from pathlib import Path

from docx import Document

from app.models.job import Job
from app.services.llm import ask_llm
from app.agents.resume_parser import parse_resume


BASE_DIR = Path(__file__).resolve().parent.parent

MASTER_RESUME = BASE_DIR / "templates" / "master_resume.docx"

PROMPT_FILE = BASE_DIR / "prompts" / "cover_letter.txt"

OUTPUT_DIR = BASE_DIR / "cover_letters"
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_cover_letter(job: Job) -> str:

    resume_data = parse_resume(str(MASTER_RESUME))

    prompt = PROMPT_FILE.read_text(encoding="utf-8")

    final_prompt = f"""
{prompt}

Company:
{job.company}

Job Title:
{job.title}

Job Description:
{job.description}

Candidate Resume:
{resume_data}
"""

    cover_letter = ask_llm(final_prompt)

    document = Document()

    for line in cover_letter.splitlines():

        line = line.strip()

        if not line:
            continue

        document.add_paragraph(line)

    filename = (
        f"{job.company}_{job.title}"
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    output_file = OUTPUT_DIR / f"{filename}.docx"

    document.save(output_file)

    return str(output_file)