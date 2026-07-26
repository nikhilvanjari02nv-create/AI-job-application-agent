from datetime import datetime

from app.database.database import SessionLocal
from app.models.job import Job

from app.agents.playwright_agent import apply_to_job

MAX_APPLICATIONS = 5
DRY_RUN = True

db = SessionLocal()

jobs = (
    db.query(Job)
    .filter(Job.status == "analyzed")
    .filter(Job.should_apply == True)
    .filter(Job.application_status == "pending")
    .limit(MAX_APPLICATIONS)
    .all()
)

print(f"\nFound {len(jobs)} jobs\n")

for i, job in enumerate(jobs, start=1):

    print("=" * 80)
    print(f"[{i}/{len(jobs)}]")
    print(job.company)
    print(job.title)

    result = apply_to_job(job)

    print(result["message"])

    if result["success"]:

        job.application_status = "opened"
        job.applied_at = datetime.now().isoformat()
        job.application_error = None

    else:

        job.application_status = "failed"
        job.application_error = result["message"]

    db.commit()

db.close()

print("\nDone!")