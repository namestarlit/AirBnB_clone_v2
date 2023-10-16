#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from os import getenv
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Column, String

if getenv("HBNB_TYPE_STORAGE") == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime,
                            nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, val in kwargs.items():
                if key != '__class__':
                    setattr(self, key, val)
            if (kwargs.get('created_at') and
                    type(self.created_at) is str):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.now()
            if (kwargs.get('updated_at') and
                    type(self.updated_at) is str):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'],
                    '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.now()
            if kwargs.get('id') is None:
                self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        pr_dct = self.__dict__
        pr_dct.pop("_sa_instance_state", None)
        return '[{}] ({}) {}'.format(
            self.__class__.__name__,
            self.id,
            pr_dct)

    def delete(self):
        """delete current instance"""
        from models import storage
        storage.delete(self)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = self.__dict__.copy()
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        """below line adds the class name of the instance dictionary"""
        """important for deserialization"""
        dictionary['__class__'] = type(self).__name__
        if "_sa_instance_state" in dictionary.keys():
            dictionary.pop('_sa_instance_state', None)
        return dictionary
