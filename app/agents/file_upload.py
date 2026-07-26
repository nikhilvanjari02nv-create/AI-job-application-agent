from pathlib import Path


def upload_resume(page, resume_path):

    if not resume_path:
        return False

    resume_path = str(Path(resume_path).resolve())

    inputs = page.locator("input[type='file']")

    for i in range(inputs.count()):

        try:

            inputs.nth(i).set_input_files(resume_path)

            print("Resume uploaded")

            return True

        except Exception:
            continue

    return False


def upload_cover_letter(page, cover_letter_path):

    if not cover_letter_path:
        return False

    cover_letter_path = str(
        Path(cover_letter_path).resolve()
    )

    inputs = page.locator("input[type='file']")

    for i in range(inputs.count()):

        try:

            inputs.nth(i).set_input_files(
                cover_letter_path
            )

            print("Cover Letter uploaded")

            return True

        except Exception:
            continue

    return False