from sqlalchemy import create_engine

db = create_engine("sqlite:///data.db", echo=True)
