#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.review import Review
from os import getenv
from sqlalchemy import Table, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

if getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
            'place_amenity', Base.metadata,
            Column('place_id', String(60),
                   ForeignKey("places.id",
                              onupdate='CASCADE',
                              ondelete='CASCADE'),
                   primary_key=True),
            Column('amenity_id', String(60),
                   ForeignKey("amenities.id",
                              onupdate='CASCADE',
                              ondelete='CASCADE'),
                   primary_key=True))


class Place(BaseModel, Base):
    """ A place to stay """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
            "Review",
            backref="place",
            cascade="all, delete-orphan")
        amenities = relationship(
            'Amenity',
            secondary="place_amenity",
            back_populates="place_amenities",
            viewonly=False)
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
        """Initializes place instance"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Reviews getter attribute for file storage"""
            return [review for review
                    in models.storage.all(Review)
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """Amenities getter attribute for file storage"""
            return [amenity for amenity
                    in models.storage.all(Amenity)
                    if amenity.id == self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter method for amenities"""
            if (type(obj) == Amenity):
                self.amenity_ids.append(obj.id)
