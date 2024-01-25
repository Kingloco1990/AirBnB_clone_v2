#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """ 
    The City class represents a city in the context of the AirBnB project.

    Attributes:
        __tablename__ (str): The name of the corresponding table in the database.
        state_id (str): The ID of the state to which the city belongs.
        name (str): The name of the city.
    """
    __tablename__ = 'cities'
    state_id = Column(String(60), nullable=False, )
    name = Column(String(128), ForeignKey("states.id"), nullable=False)
