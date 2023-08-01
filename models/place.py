#!/usr/bin/python3
"""Module containing Place class."""

from os import getenv

from sqlalchemy import Table, Column
from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review


if getenv('HBNB_TYPE_STORAGE') == "db":
    place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   primary_key=True),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   primary_key=True)
            )


class Place(BaseModel, Base):
    """Represents a Place class."""
    if getenv('HBNB_TYPE_STORAGE') == "db":
        __tablename__ = 'places'

        city_id = Column(String(60), ForeignKey('cities.id'))
        user_id = Column(String(60), ForeignKey('users.id'))
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Float, default=0, nullable=False)
        latitude = Column(Float, default=0.0)
        longitude = Column(Float, default=0.0)
        reviews = relationship('Review', backref='places',
                               cascade='all, delete')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 backref='place_amenities', viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """Initializes an instance of Place."""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE', None) != "db":
        @property
        def reviews(self):
            """Returns list of Review instances."""
            reviews_ = models.storage.all(Review).values()
            reviews_list = []
            for review in reviews_:
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """Returns list of Amenity instances."""
            amenities_ = models.storage.all(Amenity).values()
            amenities_list = []
            for amenity in amenities_:
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, value):
            """Setter method for amenities property."""
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
