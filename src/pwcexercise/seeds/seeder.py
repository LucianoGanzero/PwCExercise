"""Seed script for the database.

Reads data from a CSV file and populates the database.
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.pwcexercise.config.db import SessionLocal, engine
from src.pwcexercise.models.base import Base
from src.pwcexercise.seeds.seeds import seed_database
from src.pwcexercise.utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
csv_path = BASE_DIR / "HR_Analytics.csv"

hr_analytics_df = pd.read_csv(csv_path)

def empty_database(session: Session) -> None:
    """Empty all tables in the database.

    Args:
        session (Session): SQLAlchemy session object.

    """
    inspector = inspect(session.bind)
    for table_name in inspector.get_table_names():
        table = Base.metadata.tables.get(table_name)
        if table is not None:
            session.execute(table.delete())
    session.commit()

def tables_exist() -> bool:
    """Check if any tables exist in the database."""
    inspector = inspect(engine)
    return bool(inspector.get_table_names())


def main() -> None:
    """Empty the database and seed it with data from the CSV file."""
    if not tables_exist():
        logger.info("No tables found. Creating database tables...")
        Base.metadata.create_all(engine)
    else:
        logger.info("Tables already exist. Skipping creation.")

    with SessionLocal() as session:
        logger.info("Emptying the database")
        empty_database(session)
        logger.info("Seeding the database")
        seed_database(session, hr_analytics_df)
        logger.info("Database seeded successfully")

if __name__ == "__main__":
    main()
