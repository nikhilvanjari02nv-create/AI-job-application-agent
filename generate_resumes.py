from app.database.database import SessionLocal
from app.models.job import Job

from app.agents.resume_generator import generate_resume
from app.agents.cover_letter_generator import generate_cover_letter


db = SessionLocal()

jobs = (
    db.query(Job)
    .filter(Job.status == "analyzed")
    .filter(Job.resume_path == None)
    .all()
)

print(f"\nFound {len(jobs)} jobs\n")

for i, job in enumerate(jobs, start=1):

    print("=" * 80)
    print(f"[{i}/{len(jobs)}]")
    print(job.company)
    print(job.title)

    # Generate Resume
    resume_path = generate_resume(job)
    job.resume_path = resume_path

    print("✓ Resume Generated")
    print(resume_path)

    # Generate Cover Letter
    cover_letter_path = generate_cover_letter(job)
    job.cover_letter_path = cover_letter_path

    print("✓ Cover Letter Generated")
    print(cover_letter_path)

    db.commit()

db.close()

print("\nDone!")