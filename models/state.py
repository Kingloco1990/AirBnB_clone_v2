#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship('City', backref='state', cascade='all, delete-orphan')
    else:
        @property
        def cities(self):
            """Getter attribute that returns a list of City instances
               associated with the current State.

            Returns:
                list: A list of City instances linked to the current State.

            Example:
                To retrieve the cities associated with a State instance
                named 'my_state':

                ```python
                cities_list = my_state.cities
                ```
            """
            my_list = []
            # Retrieve City objects (or instances) in storage.
            my_obj = models.storage.all(City)

            # Filter City instances that have state_id equal to the
            # current State's id.
            for obj in my_obj.values():
                if obj.state_id == self.id:
                    my_list.append(obj)

            return my_list
