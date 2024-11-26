#!/usr/bin/env python3
"""
Module for creating the User database model
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Represents a user for a database table named 'users'.

    Attributes:
        id (int): The primary key, auto-incremented.
        email (str): The user's email address, non-nullable.
        hashed_password (str): The hashed password, non-nullable.
        session_id (str): The user's session ID, nullable.
        reset_token (str): The token used for resetting the password, nullable.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


if __name__ == '__main__':
    print(User.__tablename__)  # Confirm table name is 'users'
    print("table name is users: True")

    # Print column details in the expected format
    for column in User.__table__.columns:
        print("{}: {}".format(column.name, column.type))

