from sqlalchemy import create_engine

# Initialize the database engine
DATABASE_URI = 'sqlite:///parliament.db'
engine = create_engine(DATABASE_URI)
