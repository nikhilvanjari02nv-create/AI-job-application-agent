from app.database.database import Base, engine
from app.models.job import Job


def create_database():
    Base.metadata.create_all(bind=engine)
    print("Database created successfully.")


if __name__ == "__main__":
    create_database()