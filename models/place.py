#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review
from sqlalchemy.schema import Table
from models.amenity import Amenity


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []


if getenv("HBNB_TYPE_STORAGE") == "db":
    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)

if getenv("HBNB_TYPE_STORAGE") == "FileStorage":
    @property
    def review(self):
        my_list = []
        # Retrieve City objects (or instances) in storage.
        my_obj = models.storage.all(Review)

        # Filter Review instances that have place_id equal to the
        # current Place's id.
        for obj in my_obj.values():
            if obj.place_id == self.id:
                my_list.append(obj)

        return (my_list)

    @property
    def amenities(self):
        my_list = []
        my_obj = models.storage.all(Amenity)
        for obj in my_obj.values():
            if obj.id in self.amenity_ids:
                my_list.append(obj)

        return (my_list)
    
    @amenities.setter
    def amenities(self, value):
        if type(value) == Amenity:
            self.amenity_ids.append(value.id)
        

place_amenity = Table(
    'association',
    Base.metadata,
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id'),
        primary_key=True,
        nullable=False
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id'),
        primary_key=True,
        nullable=False
    )
)
