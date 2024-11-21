import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base, User
from config.config import DATABASE_URL

# Set up the engine and session
engine = create_engine(DATABASE_URL)

# Create the tables in the database (if not already created)
Base.metadata.create_all(engine)

# Print table name and columns
print(User.__tablename__)
for column in User.__table__.columns:
    print(f"{column}: {column.type}")

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Query and display all users
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
