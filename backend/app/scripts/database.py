from sqlalchemy import create_engine, inspect
import pandas as pd

# Initialize the database engine
DATABASE_URI = 'sqlite:///parliament.db'
engine = create_engine(DATABASE_URI)

def table_exists(engine, table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

