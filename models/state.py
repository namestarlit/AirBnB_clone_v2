#!/usr/bin/python3
"""Module contains a State class."""

from os import getenv

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.city import City


class State(BaseModel, Base):
    """Represents State class."""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='states',
                              cascade='all, delete')
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of State."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE', None) != "db":
        @property
        def cities(self):
            """File storage getter attribute that returns City instances."""
            cities_ = models.storage.all(City).values()
            cities_list = []
            for city in cities_:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
