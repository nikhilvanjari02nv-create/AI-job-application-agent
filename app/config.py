import os

from dotenv import load_dotenv

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


TARGET_ROLES = [
    "AI Automation",
    "Automation Engineer",
    "Virtual Assistant",
    "Customer Support",
    "Customer Success",
    "Operations Assistant",
    "Administrative Assistant",
    "Technical Support",
    "Data Entry",
    "Research Assistant",
]

COUNTRIES = [
    "Remote",
    "United States",
    "Canada",
    "United Kingdom",
    "Australia",
]

MIN_MATCH_SCORE = 75

AUTO_APPLY = False

MAX_APPLICATIONS_PER_DAY = 30