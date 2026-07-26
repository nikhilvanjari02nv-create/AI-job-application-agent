from app.database.database import SessionLocal
from app.models.job import Job
from app.agents.analyzer import analyze_job

db = SessionLocal()

# Only analyze jobs that haven't been analyzed yet
jobs = db.query(Job).filter(Job.status == "new").all()

print(f"\nFound {len(jobs)} new jobs\n")

for i, job in enumerate(jobs, start=1):

    print("=" * 80)
    print(f"[{i}/{len(jobs)}]")
    print(f"Company : {job.company}")
    print(f"Title   : {job.title}")
    print("-" * 80)

    analysis = analyze_job({
        "company": job.company,
        "position": job.title,
        "location": job.location,
        "description": job.description
    })

    # Save AI analysis to database
    job.ai_score = analysis.get("score")
    job.ai_category = analysis.get("category")
    job.should_apply = analysis.get("should_apply")
    job.ai_reason = analysis.get("reason")
    job.status = "analyzed"

    db.commit()

    print(
        f"✓ Saved | Score: {job.ai_score} | "
        f"Category: {job.ai_category} | "
        f"Apply: {job.should_apply}"
    )

db.close()

print("\nDone!")