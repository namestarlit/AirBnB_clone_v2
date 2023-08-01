#!/usr/bin/python3
"""Module contains a City class."""
from os import getenv

from sqlalchemy import Column
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """Represents a City class."""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'))
        places = relationship('Place', backref='cities',
                              cascade='all, delete-orphan')
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of City."""
        super().__init__(*args, **kwargs)
