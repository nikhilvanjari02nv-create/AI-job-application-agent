import httpx


URL = "https://jobicy.com/api/v2/remote-jobs"


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
                "company": job.get("companyName"),
                "position": job.get("jobTitle"),
                "location": job.get("jobGeo"),
                "salary": job.get("annualSalaryMin"),
                "url": job.get("url"),
                "description": job.get("jobDescription"),
            }
        )

    return jobs