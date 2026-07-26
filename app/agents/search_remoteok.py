import httpx

URL = "https://remoteok.com/api"


def fetch_jobs():
    headers = {
        "User-Agent": "AI Job Agent"
    }

    response = httpx.get(URL, headers=headers, timeout=30)

    response.raise_for_status()

    data = response.json()

    return data[1:]