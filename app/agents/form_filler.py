from playwright.sync_api import Page

from app.profile import PROFILE
from app.agents.question_answer import answer_question


FIELDS = {
    "name": ["name", "full name"],
    "email": ["email"],
    "phone": ["phone", "mobile"],
    "linkedin": ["linkedin"],
    "github": ["github"],
    "portfolio": ["portfolio", "website"],
    "address": ["address"],
}


def fill_text_fields(page: Page):

    inputs = page.locator("input")
    count = inputs.count()

    for i in range(count):
        try:
            field = inputs.nth(i)

            if not field.is_visible():
                continue

            if not field.is_enabled():
                continue

            placeholder = (field.get_attribute("placeholder") or "").lower()
            aria = (field.get_attribute("aria-label") or "").lower()
            name = (field.get_attribute("name") or "").lower()

            combined = f"{placeholder} {aria} {name}"

            for key, labels in FIELDS.items():
                if any(label in combined for label in labels):
                    value = PROFILE.get(key)
                    
                    if field.input_value():
                    
                        field.fill(value)

        except Exception:
            continue


def fill_textareas(page: Page, job):

    textareas = page.locator("textarea")

    for i in range(textareas.count()):

        try:

            textarea = textareas.nth(i)

            if textarea.input_value():
                continue

            question = (
                textarea.get_attribute("aria-label")
                or textarea.get_attribute("placeholder")
                or ""
            ).strip()

            if not question:

                try:

                    question = textarea.evaluate(
                        """
                        el => {
                            const label = document.querySelector(
                                `label[for="${el.id}"]`
                            );
                            return label ? label.innerText : "";
                        }
                        """
                    ).strip()

                except Exception:

                    question = ""

            if question:

                answer = answer_question(
                    question,
                    job,
                )

            else:

                answer = (
                    "Please refer to my resume for additional details."
                )

            textarea.fill(answer)

        except Exception:
            continue


def fill_dropdowns(page: Page):

    selects = page.locator("select")

    for i in range(selects.count()):

        try:

            select = selects.nth(i)

            options = select.locator("option")

            if options.count() > 1:

                value = options.nth(1).get_attribute("value")

                if value:

                    select.select_option(value)

        except Exception:
            continue


def tick_checkboxes(page: Page):

    checkboxes = page.locator(
        "input[type='checkbox']"
    )

    for i in range(checkboxes.count()):

        try:

            box = checkboxes.nth(i)

            if not box.is_checked():

                box.check()

        except Exception:
            continue


def select_radio_buttons(page: Page):

    radios = page.locator(
        "input[type='radio']"
    )

    selected = set()

    for i in range(radios.count()):

        try:

            radio = radios.nth(i)

            name = radio.get_attribute("name")

            if name in selected:
                continue

            radio.check()

            selected.add(name)

        except Exception:
            continue


def fill_form(page: Page, job):

    fill_text_fields(page)

    fill_textareas(page, job)

    fill_dropdowns(page)

    tick_checkboxes(page)

    select_radio_buttons(page)


