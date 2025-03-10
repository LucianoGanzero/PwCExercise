from sqlalchemy import create_engine, MetaData

meta = MetaData()

engine = create_engine("sqlite:///hr_database.db", echo=True)

conn = engine.connect()

