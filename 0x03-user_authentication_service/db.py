#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from typing import Dict

from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        # Create a new SQLite database connection
        self._engine = create_engine("sqlite:///a.db", echo=True)
        # Drop existing tables and recreate them
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        # Initialize private session attribute
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created user instance.
        """
        # Create a new User instance
        user = User(email=email, hashed_password=hashed_password)
        # Add to session and commit changes
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find user by arbitrary attributes"""
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided.")

        # Validate the filter arguments against the table columns
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise InvalidRequestError(f"Invalid filter key: {key}")

        # Query the database
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found with the provided filters.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes"""
        # Find the user by ID
        user = self.find_user_by(id=user_id)

        # Validate that all keys are valid columns
        valid_columns = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in valid_columns:
                raise ValueError(f"Invalid update key: {key}")

        # Update the user's attributes
        for key, value in kwargs.items():
            setattr(user, key, value)

        # Commit the changes
        self._session.commit()
