#!/usr/bin/python3
"""Database Storage implementantion.

Implementation of database operations using MySQL Database.
"""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def import_models():
    """Dynamic import of models."""
    return {
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }


class DBStorage:
    """Database Engine."""
    __engine = None
    __session = None
    model_mapping = import_models()

    def __init__(self):
        """Starts the DB engine."""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        db_url = ("mysql+mysqldb://{}:{}@{}/{}"
                  .format(user, password, host, db)
                  )
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "dev":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """Returns a dictionary."""
        sql_dict = {}

        if cls:
            # Query the specified class
            objects = self.__session.query(cls).all()
        else:
            # Query all available classes
            models = list(self.model_mapping.values())
            objects = []
            for model in models:
                objects.extend(self.__session.query(model).all())

        for obj in objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            sql_dict[key] = obj

        return sql_dict

    def new(self, obj):
        """Adds the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session."""
        self.__session.commit()

    def reload(self):
        """ Creates all tables in the database.

        Creates the current database scoped session
        """
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session)
        self.__session = Session()

    def delete(self, obj=None):
        """Deletes from the current database session."""
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        """Calls remove() method on the private session attribute."""
        self.__session.close()
