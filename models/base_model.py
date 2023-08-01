#!/usr/bin/python3
"""Base Class for the AirBnB Clone Project."""

from datetime import datetime
from os import getenv
from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String, DateTime

import models


if getenv('HBNB_TYPE_STORAGE') == "db":
    Base = declarative_base()


class BaseModel(object):
    """Defines the BaseModel class.

    Attributes:
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTime): The datetime at creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """
    if getenv('HBNB_TYPE_STORAGE') == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Iniatializes an instance of BaseModel class.

        Args:
            *args (any): Unused
            *kwargs (dict): Keyworded arguments.
        """
        # Set Random unique ID to instance attribute 'id'
        self.id = str(uuid4())

        # Update instance attributes with kwargs.
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """String Representation of BaseModel class."""
        return ("[{:s}] ({:s}) {}"
                .format(self.__class__.__name__, self.id, self.__dict__))

    def save(self):
        """Update the public instance attribute 'updated_at'."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary of all the key/value pairs."""
        # Create a new dict and directly assign the class name
        new_dict = {'__class__': self.__class__.__name__}

        # Convert 'created_at' and 'updated_at' into ISO format.
        for key, value in self.__dict__.items():
            if key == 'created_at' or key == 'updated_at':
                new_dict[key] = value.isoformat()
            elif (key != '_password' and
                  key not in ('amenities', 'reviews', '_sa_instance_state')):
                new_dict[key] = value

        return new_dict
