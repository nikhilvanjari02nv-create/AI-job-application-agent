import httpx


URL = "https://www.remotejobs.io/api/jobs"


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

    for job in data:

        jobs.append(
            {
                "company": job.get("company"),
                "position": job.get("title"),
                "location": job.get("location"),
                "salary": job.get("salary"),
                "url": job.get("url"),
                "description": job.get("description"),
            }
        )

    return jobs