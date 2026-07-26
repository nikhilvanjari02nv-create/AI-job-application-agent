from app.agents.form_filler import fill_form
from app.agents.submit_application import submit_application
from app.agents.file_upload import (
    upload_resume,
    upload_cover_letter,
)


def apply(page, job):

    if job.resume_path:
        upload_resume(page, job.resume_path)

    if job.cover_letter_path:
        upload_cover_letter(page, job.cover_letter_path)

    fill_form(page, job)

    submit_application(page)