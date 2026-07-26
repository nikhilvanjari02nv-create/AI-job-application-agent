import httpx
import xml.etree.ElementTree as ET


URL = "https://weworkremotely.com/remote-jobs.rss"


def fetch_jobs():

    response = httpx.get(
        URL,
        timeout=30,
        headers={
            "User-Agent": "AI Job Agent"
        },
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    jobs = []

    for item in root.findall("./channel/item"):

        jobs.append(
            {
                "company": "",
                "position": item.findtext("title"),
                "location": "Remote",
                "salary": None,
                "url": item.findtext("link"),
                "description": item.findtext("description"),
            }
        )

    return jobs