# -*- coding: utf-8 -*-

"""This module defines all functions that are needed to parse args based on a configuration class."""


import argparse
import collections
import enum
import inspect
import pydoc
import typing
import types

import yaml


__author__ = "Patrick Hohenecker"
__copyright__ = \
        """
        Copyright (c) 2017 Patrick Hohenecker

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
        """
__license__ = "MIT License"
__version__ = "2017.1"
__date__ = "Jul 05, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


META_VARS = collections.defaultdict(
        lambda: "X",
        {
                dict: "D",
                float: "R",
                int: "N",
                str: "S"
        }
)
"""collections.defaultdict: A dict that specifies meta variables to be used in the synopsis for the different types."""


def create_arg_parser(spec: typing.Dict[str, dict], app_name: str, app_description: str) -> argparse.ArgumentParser:
    """Creates an arg parser based on the provided specification.

    The specification has to be provided in terms of a ``dict`` that maps names of options to dictionaries that describe
    single arguments. These argument-dicts need to specify the type, a description, and the default value of the
    corresponding option.

    Args:
        spec (dict): The specification that describes the options available.
        app_name (str): The name of the app that should be printed in the synopsis.
        app_description (str): The description of the app that should be printed in the synopsis.

    Returns:
        argparse.ArgumentParser: The created arg parser.
    """
    parser = argparse.ArgumentParser(prog=app_name, description=app_description)

    for prop_name, prop_desc in spec.items():
        arg_name = "--" + prop_name.replace("_", "-")

        if prop_desc["type"] == bool:
            parser.add_argument(
                arg_name,
                dest=prop_name,
                action="store_const",
                const=not prop_desc["default"],
                default=prop_desc["default"],
                help=prop_desc["description"]
            )
        else:
            if issubclass(prop_desc["type"], enum.Enum):
                arg_type = enum_type(prop_desc["type"])
            elif prop_desc["type"] == dict:
                arg_type = yaml.load
            else:
                arg_type = prop_desc["type"]
            parser.add_argument(
                arg_name,
                dest=prop_name,
                type=arg_type,
                default=prop_desc["default"],
                help=prop_desc["description"],
                metavar=META_VARS[prop_desc["type"]]
            )

    return parser


def enum_type(cls: enum.Enum) -> types.FunctionType:
    """Creates a function that may be passed to an ``argparse.ArgumentParser`` for handling an option that is described
    by the provided ``Enum``.

    Args:
        cls (enum.Enum): The ``Enum`` that describes the option.

    Returns:
        function: A function that can be passed to an ``ArgumentParser`` via the keyword arg ``type`` of the method
            ``add_argument``.
    """
    def type_func(val: str):
        if val not in cls.__members__.keys():
            raise ValueError("illegal value '%s', possible values are %s" % (val, ", ".join(cls.__members__.keys())))
        return cls[val].value

    return type_func


def load_configs(cls: type, fixed_types=None) -> dict:
    """Creates a configuration specification based on the provided class.

    The created specification defines one option for each member (instance variable or property) of the given class
    except those that start with an underscore or with ``DEFAULT_``. Members whose names start with ``DEFAULT_`` are
    assumed to define default values for options. Type and description for each of the options are extracted from the
    first line of the corresponding docstring.

    Args:
        cls (type): The class that the configuration is based on.
        fixed_types (optional): A ``dict`` that specifies the types of fields in ``conf_class`` that are not defined in
            the according docstring in the class. Furthermore, this arg may specify enums that should be used for
            certain options.
    """
    if fixed_types is None:
        fixed_types = {}

    configs = {}

    # find all public members (that are not default values)
    for name, field in inspect.getmembers(cls, lambda f: not inspect.isroutine(f)):
        # only consider public members
        if name.startswith("_"):
            continue

        # don't consider default values for now
        if name.startswith("DEFAULT_"):
            continue

        # fetch summary line of docs
        doc_summary = field.__doc__.split("\n")[0]

        # extract type if not fixed
        if name in fixed_types:
            prop_type = fixed_types[name]
        else:
            type_name = doc_summary[:doc_summary.find(":")]
            prop_type = pydoc.locate(type_name)

        # extract description
        description = doc_summary[doc_summary.find(":") + 1:].strip()

        configs[name] = {
                "type": prop_type,
                "description": description
        }

    # load default values
    for name, field in inspect.getmembers(cls, lambda f: not inspect.isroutine(f)):
        # only consider mem
        if not name.startswith("DEFAULT_"):
            continue

        ref_field = name[8:].lower()
        configs[ref_field]["default"] = field

    return configs


def parse_args(conf_class, fixed_types: typing.Dict[str, type]=None, app_name: str=None, app_description: str=None):
    """Parses the args of the current application based on the provided configuration class, and returns an instance of
    the same.

    Args:
        conf_class: The type of the configuration object that should be parsed from the command line args.
        fixed_types (dict): A ``dict`` that specifies the types of fields in ``conf_class`` that are not defined in
            the according docstring in the class. Furthermore, this arg may specify enums that should be used for
            certain options.
        app_name (str): The name of the application that is printed in the synopsis.
        app_description (str): The description of the application that is printed in the synopsis.

    Returns:
        The parsed configuration as an object of type ``conf_class``.
    """
    # fetch all details about the config class
    all_props = load_configs(conf_class, fixed_types)

    # create according arg parser
    parser = create_arg_parser(all_props, app_name, app_description)

    # parse args, create and populate configuration object
    args = parser.parse_args()
    conf = conf_class()
    for prop in all_props.keys():
        setattr(conf, prop, getattr(args, prop))

    return conf


def get_config(conf) -> typing.Dict[str, str]:
    """Creates a ``dict`` that summarizes the values of the members of the provided object.

    This function considers all members of ``conf`` whose name does not start with an underscore, and converts their
    values into strings.

    Args:
        conf: The object to be summarized.

    Returns:
        dict: Maps the names of the considered members to their according values as strings.

    Raises:
        TypeError: If ``conf`` is ``None``.
    """
    if conf is None:
        raise TypeError("The parameter <conf> must not be None!")

    str_conf = {}

    for p, v in inspect.getmembers(conf):
        if p.startswith("_") or p.startswith("DEFAULT_"):
            continue
        str_conf[p] = str(v)

    return str_conf
