#!/usr/bin/python3
"""Module defines the Amenity class."""

from os import getenv

from sqlalchemy import Column
from sqlalchemy import String
from sqlachmemy.orm import relationship

import models
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Represents an amenity."""

    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a new Amenity instance."""
        super().__init__(*args, **kwargs)
