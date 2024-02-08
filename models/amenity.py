#!/usr/bin/python3
"""Module defining the Amenity class for the AirBnB clone project."""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity class representing amenities available in places.

    Attributes:
        __tablename__ (str): The table name for the database.
        name (str): The name of the amenity.

    Relationships:
        - place_amenities: Many-to-many relationship with the Place class
          through the PlaceAmenity association table.
    """
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    place_amenities = relationship('Place', secondary='place_amenity')
