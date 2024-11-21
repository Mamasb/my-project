import sys
sys.path.append('../')

from db import DB
from models.user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from auth import _hash_password  # Importing _hash_password from auth.py

# Create DB instance
my_db = DB()

# Add users
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(f"User 1 ID: {user_1.id}")

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(f"User 2 ID: {user_2.id}")

# Test: Find a user by a valid email
try:
    found_user = my_db.find_user_by(email="test@test.com")
    print(f"Found User 1 ID: {found_user.id}")
except NoResultFound:
    print("User not found with the given email")

# Test: Try to find a user by a non-existing email
try:
    found_user = my_db.find_user_by(email="nonexistent@test.com")
    print(f"Found User ID: {found_user.id}")
except NoResultFound:
    print("No user found with the given email")

# Test: Try to find a user with an invalid query argument (wrong field name)
try:
    found_user = my_db.find_user_by(no_email="test@test.com")
    print(f"Found User ID: {found_user.id}")
except InvalidRequestError:
    print("Invalid query argument passed")

# Test: Hash a password
hashed_password = _hash_password("MySecurePassword123")
print(f"Hashed Password: {hashed_password}")
