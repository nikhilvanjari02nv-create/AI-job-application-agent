from playwright.sync_api import Page


BUTTON_TEXT = [
    "next",
    "continue",
    "review",
    "submit",
    "submit application",
    "finish",
]


def submit_application(page: Page) -> bool:

    while True:

        clicked = False

        for text in BUTTON_TEXT:

            try:

                button = page.get_by_role(
                    "button",
                    name=text,
                    exact=False,
                )

                if button.count():

                    button.first.click()

                    page.wait_for_timeout(2000)

                    clicked = True

                    print(f"Clicked: {text}")

                    break

            except Exception:
                continue

        if not clicked:
            break

    return True