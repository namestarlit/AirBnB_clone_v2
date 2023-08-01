#!/usr/bin/python3
"""A console application for Airbnb clone."""

import cmd
import sys
import re
import os
import shlex

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """Represents HBNBCommand class."""

    # Define console  prompt
    prompt = "(hbnb) " if sys.__stdin__.isatty() else ''

    classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
            }

    # Define the dot commands
    action_cmds = ['all', 'count', 'show', 'destroy', 'update']

    # Define the types for certain attributes
    types = {
            'number_rooms': int,
            'number_bathrooms': int,
            'max_guest': int,
            'price_by_night': int,
            'latitude': float,
            'longitude': float
            }

    def precmd(self, line):
        """
        Reformat command line for advanced command syntax.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ""  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if not ("." in line and "(" in line and ")" in line):
            return line

        try:
            pline = line[:]  # copy line
            # isolate <class name>
            _cls = pline[: pline.find(".")]

            # isolate and validate <command>
            _cmd = pline[pline.find(".") + 1:pline.find("(")]
            if _cmd not in self.action_cmds:
                raise ValueError(f"{_cmd}: invalid command")

            # if parentheses contain arguments, parse them
            pline = pline[pline.find("(") + 1:pline.find(")")]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(", ")  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('"', "")
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline.startswith("{") and pline.endswith("}"):
                        if type(eval(pline)) is dict:
                            _args = pline
                    else:
                        _args = pline.replace(",", "")

            # handle commands
            if _cmd == "all":
                self.do_all(_cls)
                return ""
            elif _cmd == "count":
                self.do_count(_cls)
                return ""
            elif _cmd == "show":
                if not _id:
                    raise ValueError("missing id")
                self.do_show(f"{_cls} {_id}")
                return ""
            elif _cmd == "destroy":
                if not _id:
                    raise ValueError("missing id")
                self.do_destroy(f"{_cls} {_id}")
                return ""
            elif _cmd == "update":
                if not _id:
                    raise ValueError("missing id")
                if not _args:
                    raise ValueError("missing attribute dictionary or \
                            attribute name/value pair")
                self.do_update(f"{_cls} {_id} {_args}")
                return ""

        except ValueError as ve:
            print(f"*** {ve}")
        except Exception as ex:
            print(f"*** {ex}")
        finally:
            line = " ".join([_cmd, _cls, _id, _args])
            return line

    def postcmd(self, stop, line):
        """Prints prompt if isatty is False."""
        if not sys.stdin.isatty():
            print('(hbnb) ', end='')
        return stop

    def emptyline(self):
        """Do nothing instead of repeating last
        command when an empty line is entered."""
        pass

    def do_create(self, args):
        """Creates an instance of a specified class"""
        # Attributes to be ignored when creating a new object
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        # Pattern to match the class name
        class_regex = r'(?P<class_name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(class_regex, args)

        obj_kwargs = {}

        if class_match:
            # Get the class name from the input
            class_name = class_match.group('class_name')
            # Get the params to create the object from the input
            params_str = args[len(class_name):].strip()
            # Split the params string into a list of params
            params = params_str.split(' ')

            # Pattern to match string, float and integer types
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'

            # Pattern to match param name and value
            param_pattern = '{}=({}|{}|{})'.format(
                    class_regex,
                    str_pattern,
                    float_pattern,
                    int_pattern
                    )

            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match:
                    key_name = param_match.group('class_name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v:
                        obj_kwargs[key_name] = float(float_v)
                    if int_v:
                        obj_kwargs[key_name] = int(int_v)
                    if str_v:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            print("** class name missing **")
            return

        # Check if class exists in HBNBCommand.classes
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Create a new instance of the specified class
        new_instance = HBNBCommand.classes[class_name]()

        # Set attributes of the new object
        for key, value in obj_kwargs.items():
            if key not in ignored_attrs:
                setattr(new_instance, key, value)

        # Save the new object to the JSON file
        new_instance.save()

        # Print the ID of the new object
        print(new_instance.id)

    def do_show(self, args):
        """Show an individual object"""

        # Parse the arguments to extract the class name and instance id
        class_name, _, instance_id = args.partition(" ")

        # Guard against trailing args
        if instance_id and ' ' in instance_id:
            instance_id = instance_id.partition(' ')[0]

        # Check if class name is missing
        if not class_name:
            print("** class name missing **")
            return

        # Check if the class doesn't exist
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Check if the instance id is missing
        if not instance_id:
            print("** instance id missing **")
            return

        # Create the key for the instance to be shown
        key = "{}.{}".format(class_name, instance_id)

        # Check if the instance exists in the storage
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes a specified object"""
        arg_list = args.split()
        if len(arg_list) == 0:
            print("** class name missing **")
            return
        elif arg_list[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        elif len(arg_list) == 1:
            print("** instance id missing **")
            return

        obj_key = arg_list[0] + "." + arg_list[1]
        obj_dict = storage.all()

        if obj_key not in obj_dict:
            print("** no instance found **")
            return

        storage.delete(obj_dict[obj_key])
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        objects = storage.all()
        obj_list = []
        if len(arg) == 0:
            for obj in objects.values():
                obj_list.append(str(obj))
        else:
            arg_list = arg.split()
            if arg_list[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for obj in objects.values():
                if obj.__class__.__name__ == arg_list[0]:
                    obj_list.append(str(obj))
        print(obj_list)

    def do_count(self, args):
        """
        Count the number of instances of a specified class.
        Usage: count <class name>
        """
        class_name = args.split(' ')[0] if args else None

        if not class_name:
            print("** class name missing **")
            return

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        count = 0
        for obj_id, obj in storage.all().items():
            if obj.__class__.__name__ == class_name:
                count += 1

        print(count)

    def do_update(self, args):
        """Updates an instance based on the class name and id"""
        try:
            # Parsing the input
            args_list = shlex.split(args)
            if not args_list:
                raise ValueError("** class name missing **")
            class_name = args_list[0]
            if class_name not in HBNBCommand.classes:
                raise ValueError("** class doesn't exist **")
            if len(args_list) < 2:
                raise ValueError("** instance id missing **")
            instance_id = args_list[1]
            key = class_name + "." + instance_id
            if key not in storage.all():
                raise ValueError("** no instance found **")
            obj = storage.all()[key]

            # Updating the attributes
            if len(args_list) < 3:
                raise ValueError("** attribute name missing **")
            if len(args_list) < 4:
                raise ValueError("** value missing **")
            attr_name = args_list[2]
            attr_val = args_list[3]
            try:
                attr_val = eval(attr_val)
                if isinstance(attr_val, dict):
                    obj.update(attr_val)
                else:
                    setattr(obj, attr_name, attr_val)
            except (NameError, SyntaxError):
                setattr(obj, attr_name, attr_val)
            storage.save()

        except ValueError as e:
            print(e)

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        return True

    def postloop(self):
        print()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
