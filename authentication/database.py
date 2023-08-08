import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv("CLEARDB_DATABASE_URL")

# create sqlalchemy engine "engine"

engine = create_engine(db_url)

# create a session local class - where each instance of this class will represent a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a Base class of which we will later inherit from this class when creating classes or models
Base = declarative_base()


