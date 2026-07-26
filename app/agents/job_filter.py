TARGET_KEYWORDS = [
    "automation",
    "ai",
    "python",
    "assistant",
    "support",
    "customer",
    "operations",
    "data",
    "research",
]


def job_filter(job):

    title = job.title or ""
    description = job.description or ""

    text = f"{title} {description}".lower()

    matched = []

    for keyword in TARGET_KEYWORDS:
        if keyword in text:
            matched.append(keyword)

    should_apply = len(matched) > 0

    return {
        "score": min(len(matched) * 10, 100),
        "category": "Keyword Match" if should_apply else "Rejected",
        "should_apply": should_apply,
        "reason": (
            f"Matched keywords: {', '.join(matched)}"
            if should_apply
            else "No target keywords found."
        ),
    }