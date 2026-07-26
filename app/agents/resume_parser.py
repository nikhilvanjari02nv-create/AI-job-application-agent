from docx import Document


SECTION_HEADERS = {
    "summary",
    "professional summary",
    "profile",
    "skills",
    "technical skills",
    "core skills",
    "experience",
    "professional experience",
    "work experience",
    "employment",
    "projects",
    "project",
    "education",
    "certifications",
    "certification",
    "awards",
    "languages",
    "interests",
    "contact",
}


def _normalize_heading(text: str) -> str:
    return text.strip().lower().rstrip(":")


def parse_resume(file_path: str) -> dict:
    """
    Parse the master resume into a structured dictionary.

    This parser is intentionally generic so it works with
    different resume formats. It identifies common section
    headings and groups their content.

    Later, Gemini will use this structured data to build
    a tailored resume for each job.
    """

    document = Document(file_path)

    structured_resume = {
        "contact": [],
        "summary": [],
        "skills": [],
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
        "awards": [],
        "languages": [],
        "interests": [],
        "other": [],
        "paragraphs": [],
    }

    current_section = "other"

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        structured_resume["paragraphs"].append(text)

        heading = _normalize_heading(text)

        if heading in SECTION_HEADERS:
            if heading in (
                "summary",
                "professional summary",
                "profile",
            ):
                current_section = "summary"

            elif heading in (
                "skills",
                "technical skills",
                "core skills",
            ):
                current_section = "skills"

            elif heading in (
                "experience",
                "professional experience",
                "work experience",
                "employment",
            ):
                current_section = "experience"

            elif heading in (
                "projects",
                "project",
            ):
                current_section = "projects"

            elif heading == "education":
                current_section = "education"

            elif heading in (
                "certifications",
                "certification",
            ):
                current_section = "certifications"

            elif heading == "awards":
                current_section = "awards"

            elif heading == "languages":
                current_section = "languages"

            elif heading == "interests":
                current_section = "interests"

            elif heading == "contact":
                current_section = "contact"

            continue

        structured_resume[current_section].append(text)

    return structured_resume