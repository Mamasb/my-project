from models.user import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        # Load credentials from environment variables
        db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        self._engine = create_engine(db_url, echo=True)
        Base.metadata.drop_all(self._engine)  # Drop all tables (for testing purposes)
        Base.metadata.create_all(self._engine)  # Create tables
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database and return the user object"""
        # Create a new user instance
        user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session and commit
        self._session.add(user)
        self._session.commit()

        # Return the user object (with an id assigned by the database)
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments"""
        try:
            # Create a query object for the User table
            query = self._session.query(User)

            # Apply filters based on the provided keyword arguments
            user = query.filter_by(**kwargs).one()  # Use `.one()` to raise NoResultFound if no match is found

            return user

        except NoResultFound:
            # Raise NoResultFound exception if no result is found
            raise NoResultFound("No user found matching the given criteria.")
        
        except InvalidRequestError:
            # Raise InvalidRequestError for any invalid query
            raise InvalidRequestError("Invalid query: The provided query arguments are not valid.")
        
        except Exception as e:
            # Raise any other exceptions
            raise InvalidRequestError(f"Invalid query: {str(e)}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update the user with the given user_id based on provided keyword arguments."""
        try:
            # Find the user by id
            user = self.find_user_by(id=user_id)

            # List of valid user attributes
            valid_attributes = ['email', 'hashed_password']

            # Update user attributes from kwargs
            for key, value in kwargs.items():
                if key not in valid_attributes:
                    raise ValueError(f"Invalid attribute: {key}")
                setattr(user, key, value)

            # Commit the changes to the database
            self._session.commit()

        except NoResultFound:
            raise NoResultFound(f"User with id {user_id} not found.")
        except Exception as e:
            raise InvalidRequestError(f"Failed to update user: {str(e)}")
