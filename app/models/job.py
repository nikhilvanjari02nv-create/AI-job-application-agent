from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database.database import Base


class Job(Base):
    __tablename__ = "jobs"

    # -----------------------------
    # Primary Key
    # -----------------------------
    id = Column(Integer, primary_key=True, index=True)

    # -----------------------------
    # Job Information
    # -----------------------------
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    location = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    source = Column(String, nullable=True)

    # -----------------------------
    # AI Analysis
    # -----------------------------
    ai_score = Column(Integer, nullable=True)
    ai_category = Column(String, nullable=True)
    should_apply = Column(Boolean, nullable=True)
    ai_reason = Column(Text, nullable=True)

    # -----------------------------
    # Workflow
    # -----------------------------
    status = Column(String, default="new", nullable=False)

    # -----------------------------
    # Generated Documents
    # -----------------------------
    resume_path = Column(String, nullable=True)
    cover_letter_path = Column(String, nullable=True)

    # -----------------------------
    # Application Tracking
    # -----------------------------
    application_status = Column(String, default="pending", nullable=False)
    applied_at = Column(String, nullable=True)

    application_error = Column(Text, nullable=True)