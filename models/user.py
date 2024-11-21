from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Base class for models
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'  # Table name in the database

    # Columns of the User table
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))

# In case you need to use the session outside of the model file, you can import it like:
# from config.config import DATABASE_URL
