from pathlib import Path

import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from src.pwcexercise.config.db import SessionLocal
from src.pwcexercise.models.base import Base
from src.seeds.seeder import seed_database

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
csv_path = BASE_DIR / "HR_Analytics.csv"

df = pd.read_csv(csv_path)

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

def main() -> None:
    with SessionLocal() as session:
        empty_database(session)
        seed_database(session, df)

if __name__ == "__main__":
    main()
