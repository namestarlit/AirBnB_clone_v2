#!/usr/bin/python3
""" FileStorage Module for HBNB project """
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {'BaseModel': BaseModel,
           'User': User,
           'Place': Place,
           'State': State,
           'City': City,
           'Amenity': Amenity,
           'Review': Review}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return self.__objects
        else:
            filterd_obj = {}
            for key, obj in self.__objects.items():
                if isinstance(obj, cls):
                    filterd_obj[key] = obj
            return filterd_obj

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """delete objects"""
        if obj is None:
            return
        else:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
            self.save()

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def close(self):
        """Deserializing the JSON file to objects"""
        self.reload()
