#!/usr/bin/python3
"""Module containing a Review class."""

from os import getenv

from sqlalchemy import Column
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """Represents a Review class."""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = "reviews"
        place_id = Column(String(60), ForeignKey('places.id'))
        user_id = Column(String(60), ForeignKey('users.id'))
        text = Column(String(128), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initializes an instance of Review."""
        super().__init__(*args, **kwargs)
