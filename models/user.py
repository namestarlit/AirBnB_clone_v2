#!/usr/bin/python3
"""Module contains User class."""

import hashlib
from os import getenv

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Represents a User class."""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        places = relationship('Place', backref='user',
                              cascade='all, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete-orphan')
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        """hashing password values"""
        self._password = hashlib.sha256(pwd.encode()).hexdigest()
