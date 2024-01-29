#!/usr/bin/python3
"""DBStorage Module

This module defines the DBStorage class, responsible for interacting
with the MySQL database using SQLAlchemy.

Attributes:
    __engine (Engine): SQLAlchemy engine for database connection.
    __session (Session): Current database session.

Classes:
    DBStorage: Handles database storage operations.

"""
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


classes = {'State': State, 'City': City,
               'User': User, 'Place': Place,
               'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """DBStorage class

    Connects to the MySQL database and provides methods for storage
    operations.

    Methods:
        __init__: Initializes the DBStorage instance.
        all: Retrieves objects from the database.
        new: Adds a new object to the database session.
        save: Commits changes to the database session.
        delete: Deletes an object from the database session.
        reload: Reloads the database session.

    """
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage.

        Connects to the MySQL database based on environment variables.
        Drops tables if in 'test' environment.
        """
        # Define the database connection URI
        connection_url = (
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(
                getenv('HBNB_MYSQL_USER'),
                getenv('HBNB_MYSQL_PWD'),
                getenv('HBNB_MYSQL_HOST'),
                getenv('HBNB_MYSQL_DB'))
            )

        # Create an SQLAlchemy engine
        self.__engine = create_engine(connection_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            # Drop all tables in the database if in 'test' environment
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Get all objects or specific class objects from the database.

        Args:
            cls (class, optional): Class type. Defaults to None.

        Returns:
            dict: Dictionary of objects.
        """
        all_objs = {}
        if cls:
            query_objs = self.__session.query(cls).all()
            for obj in query_objs:
                return {'{}.{}'.format(type(obj).__name__, obj.id): obj}
        else:
            for key, value in classes:
                query_objs = self.__session.query(value)
                for obj in query_objs:
                    return {'{}.{}'.format(type(obj).__name__, obj.id): obj}

    def new(self, obj):
        """Add a new object to the current database session.

        Args:
            obj (BaseModel): Object to be added.
        """
        self.__session.add(obj)

    def save(self):
        """Commit changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session.

        Args:
            obj (BaseModel, optional): Object to be deleted. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the database session.

        Create all tables in the database.
        Set up the current database session using sessionmaker and
        scoped_session.
        """
        # Create all tables in the database.
        Base.metadata.create_all(self.__engine)

        # Set up the current database session
        # Create a session factory using sessionmaker.
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # Wrap the session factory with scoped_session.
        Scope_session = scoped_session(Session)

        # Create a session.
        self.__session = Scope_session()
