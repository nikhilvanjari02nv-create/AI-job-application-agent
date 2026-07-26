from app.agents.search_jobicy import fetch_jobs as fetch_jobicy
from app.agents.search_weworkremotely import fetch_jobs as fetch_weworkremotely

from app.agents.job_filter import job_filter as filter_job

from app.database.database import SessionLocal
from app.models.job import Job


db = SessionLocal()


def save_jobs(jobs, source):

    saved = 0
    skipped = 0

    for j in jobs:

        url = j.get("url")

        if not url:
            continue

        exists = (
            db.query(Job)
            .filter(Job.url == url)
            .first()
        )

        if exists:
            skipped += 1
            continue


        job = Job(
            company=j.get("company") or "Unknown",
            title=j.get("position"),
            location=j.get("location"),
            salary=str(j.get("salary")) if j.get("salary") else None,
            url=url,
            description=j.get("description"),
            source=source,
            status="new",
        )


        # AI filter
        result = filter_job(job)


        job.ai_score = result.get("score")
        job.ai_category = result.get("category")
        job.should_apply = result.get("should_apply")
        job.ai_reason = result.get("reason")


        if job.should_apply:
            job.status = "analyzed"
        else:
            job.status = "rejected"


        db.add(job)

        saved += 1


    db.commit()

    return saved, skipped



sources = [
    
    ("Jobicy", fetch_jobicy),
    ("WeWorkRemotely", fetch_weworkremotely),
]


for name, fetcher in sources:

    try:

        jobs = fetcher()

        print(f"\n{name}: {len(jobs)} jobs")

        saved, skipped = save_jobs(
            jobs,
            name,
        )

        print(f"Saved: {saved}")
        print(f"Skipped: {skipped}")


    except Exception as e:

        print(f"\n{name} failed")
        print(e)



db.close()

print("\nDone!")