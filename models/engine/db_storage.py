#!/usr/bin/python3
import os
import sqlalchemy
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from sqlalchemy import create_engine
from models.review import Review
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """ DBStorage Module for HBNB project """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes class"""
        user = os.getenv("HBNB_MYSQL_USER")
        passwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{passwd}@{host}/{db}',
            pool_pre_ping=True)
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage,
        or of a specific class"""
        objects = {}
        if cls:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objects[key] = obj
        else:
            for sub_cls in Base.__subclasses__():
                for obj in self.__session.query(sub_cls).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """Adds obj to the db session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj frm db if not none"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """call close() method on the private session attribute"""
        self.__session.close()
