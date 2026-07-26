from pathlib import Path

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from app.models.job import Job

from app.agents.form_filler import fill_form
from app.agents.submit_application import submit_application

from app.agents.file_upload import (
    upload_resume,
    upload_cover_letter,
)


SCREENSHOT_DIR = (
    Path(__file__).resolve().parent.parent / "screenshots"
)

SCREENSHOT_DIR.mkdir(exist_ok=True)
DRY_RUN = True


APPLY_KEYWORDS = [
    "apply",
    "apply now",
    "easy apply",
    "start application",
    "continue",
]


def detect_platform(url: str):

    url = url.lower()

    if "greenhouse" in url:
        return "greenhouse"

    if "lever" in url:
        return "lever"

    if "ashby" in url:
        return "ashby"

    if "workday" in url:
        return "workday"

    return "external"


def find_apply_button(page):

    selectors = [
        "button",
        "a",
        "input[type='submit']",
    ]

    for selector in selectors:

        elements = page.locator(selector)

        for i in range(elements.count()):

            element = elements.nth(i)

            try:

                text = (
                    element.inner_text()
                    .strip()
                    .lower()
                )

                if any(
                    word in text
                    for word in APPLY_KEYWORDS
                ):
                    return element

            except Exception:
                continue

    return None

SUCCESS_TEXT = [
    "application submitted",
    "thank you for applying",
    "application received",
    "your application has been submitted",
    "thanks for applying",
]

def application_submitted(page):

    content = page.content().lower()
    for  text in SUCCESS_TEXT:
        if text in content:
            return True
    return False


def apply_to_job(job: Job):

    result = {
        "success": False,
        "status": "failed",
        "platform": "",
        "message": "",
        "screenshot": ""
    }
   

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=200,
        )

        page = browser.new_page()

        try:

            print(
                f"\nOpening {job.company}"
            )

            page.goto(
                job.url,
                wait_until="networkidle",
                timeout=60000,
            )

            page.wait_for_timeout(3000)

            result["platform"] = detect_platform(
                page.url
            )

            print("Platform:", result["platform"])
            
            

            apply_button = find_apply_button(page)

            if apply_button:

                print("Apply button found")

                apply_button.click()

                page.wait_for_timeout(5000)

            else:

                print(
                    "Apply button not found"
                )

            # Resume upload

            if job.resume_path:

                upload_resume(
                    page,
                    job.resume_path,
                )

            # Cover letter upload

            if job.cover_letter_path:

                upload_cover_letter(
                    page,
                    job.cover_letter_path,
                )

            fill_form(page, job)

            if DRY_RUN:
               print("DRY RUN: Skipping submit.")

            else:
                submit_application(page)  

            screenshot = (
                SCREENSHOT_DIR
                /
                f"{job.id}.png"
            )

            page.screenshot(
                path=str(screenshot),
                full_page=True,
            )

            if application_submitted(page):

                result["success"] = True
                result["status"] = "applied"
                result["message"] = "Application submitted successfully"

            else:

                result["success"] = False
                result["status"] = "unknown"
                result["message"] = "Submission could not be verified"

        except PlaywrightTimeoutError:

            result["message"] = (
                "Page timeout"
            )

        except Exception as e:

            result["message"] = f"{type(e).__name__}: {e}"

        finally:

            browser.close()


    return result