import httpx


URL = "https://remotive.com/api/remote-jobs"


def fetch_jobs():

    response = httpx.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "AI Job Agent"
        },
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):

        jobs.append(
            {
                "company": job.get("company_name"),
                "position": job.get("title"),
                "location": job.get("candidate_required_location"),
                "salary": job.get("salary"),
                "url": job.get("url"),
                "description": job.get("description"),
            }
        )

    return jobs