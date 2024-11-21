# scripts/main.py
import sys
sys.path.append('../')

from db import DB
from models.user import User

# Create DB instance
my_db = DB()

# Add a user
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)
