#!/usr/bin/python3
"""Module defining the Place class for the AirBnB clone project."""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from os import getenv
from sqlalchemy.orm import relationship
from models.review import Review
from models.amenity import Amenity


place_amenity = Table(
    'place_amenity',
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


class Place(BaseModel, Base):
    """A class representing a place to stay.

    Attributes:
        __tablename__ (str): The table name for the database.
        city_id (str): The ID of the city where the place is located.
        user_id (str): The ID of the user who owns the place.
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): The number of rooms in the place.
        number_bathrooms (int): The number of bathrooms in the place.
        max_guest (int): The maximum number of guests the place can
                        accommodate.
        price_by_night (int): The price per night for staying at the place.
        latitude (float): The latitude coordinate of the place.
        longitude (float): The longitude coordinate of the place.
        amenity_ids (list): A list of IDs of amenities associated with
                            the place.

    Relationships:
        - reviews: One-to-many relationship with the Review class,
                   representing reviews for the place.
        - amenities: Many-to-many relationship with the Amenity class through
                     the place_amenity association table.
    """
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
    reviews = relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = relationship(
        'Amenity',
        secondary='place_amenity',
        viewonly=False,
        back_populates="place_amenities"
    )

if getenv("HBNB_TYPE_STORAGE") == "FileStorage":
    @property
    def reviews(self):
        """Getter attribute that returns a list of Review instances associated
            with the current Place.

        Returns:
            list: A list of Review instances linked to the current Place.

        Example:
            To retrieve the reviews associated with a Place instance
            named 'my_place':

            ```python
            reviews_list = my_place.review
            ```
        """
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
        """Getter attribute that returns a list of Amenity instances associated
               with the current Place.

        Returns:
            list: A list of Amenity instances linked to the current Place.

        Example:
            To retrieve the amenities associated with a Place instance
            named 'my_place':

            ```python
            amenities_list = my_place.amenities
            ```
        """
        my_list = []
        my_obj = models.storage.all(Amenity)
        for obj in my_obj.values():
            if obj.id in self.amenity_ids:
                my_list.append(obj)

        return (my_list)

    @amenities.setter
    def amenities(self, value):
        """Setter attribute that assigns a new Amenity instance to
           the current Place.
        Args:
            value (Amenity): The Amenity instance to be associated
            with the current Place.
        """
        if type(value) == Amenity:
            self.amenity_ids.append(value.id)


