#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
"""
Create a SQLAlchemy class called 'User' that corresponds to
the "users" table in the database
"""

Base = declarative_base()


class User(Base):
    """
    Definition of class User
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
