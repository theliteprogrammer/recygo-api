from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = ("postgresql://xuvhfjpqhdsymb:e5f2e3e9770dfc1e16880d0061d900dfed08b21d1056fce3b5846e9ca159e1c8@ec2-3-92-151-217.compute-1.amazonaws.com:5432/d2r3pui5sgp38q")

# create sqlalchemy engine "engine"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Handle dropped connections
)

# create a session local class - where each instance of this class will represent a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a Base class of which we will later inherit from this class when creating classes or models
Base = declarative_base()


