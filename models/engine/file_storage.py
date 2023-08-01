#!/usr/bin/python3
"""
file_storage.py

Stores instance dictionaries into JSON format files.
"""

import json
import os
import sys

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class_dict = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'City': City, 'Amenity': Amenity, 'State': State, 'Review': Review
        }


class FileStorage(object):
    """serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""

        # if cls is not given, return all objects
        if not cls:
            return FileStorage.__objects

        # if cls is a string, return objects of that class
        elif isinstance(cls, str):
            return {key: value for key, value in FileStorage.__objects.items()
                    if isinstance(value, eval(cls))}

        # if cls is a class, return objects of that class
        else:
            return {key: value for key, value in FileStorage.__objects.items()
                    if isinstance(value, cls)}

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__,  obj.id)
            FileStorage.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in FileStorage.__objects:
            json_objects[key] = FileStorage.__objects[key].to_dict()

        # write objects to file
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, 'r') as f:
                objects_dict = json.load(f)

                for key, value in objects_dict.items():
                    self.new(class_dict[value['__class__']](**value))

        except Exception as e:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            del FileStorage.__objects[obj.__class__.__name__ + '.' + obj.id]
            self.save()

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in classes:
            total = len(self.all(cls))
        elif cls is None:
            total = len(FileStorage.__objects)
        return total
