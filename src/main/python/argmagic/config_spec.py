# -*- coding: utf-8 -*-


import inspect
import pydoc
import re
import typing

import insanity

import argmagic

from argmagic import config_value


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017 Patrick Hohenecker\n"
        "\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
        "of this software and associated documentation files (the \"Software\"), to deal\n"
        "in the Software without restriction, including without limitation the rights\n"
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
        "copies of the Software, and to permit persons to whom the Software is\n"
        "furnished to do so, subject to the following conditions:\n"
        "\n"
        "The above copyright notice and this permission notice shall be included in all\n"
        "copies or substantial portions of the Software.\n"
        "\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
        "SOFTWARE."
)
__license__ = "MIT License"
__version__ = "2017.1"
__date__ = "Nov 08, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class ConfigSpec(object):
    """A specification of a configuration to be parsed."""
    
    DOC_REGEX = r"^((?P<type>\S+):\s+)?(?P<doc>\S.*)$"
    """str: A regex pattern for parsing doc strings of properties."""
    
    def __init__(self):
        """Create a new instance of ``ConfigSpec``."""
        self._values = {}  # a dict for storing all configurations that are part of this spec as name-value pairs
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return isinstance(other, ConfigSpec) and set(self._values.values()) == set(other)
    
    def __getitem__(self, item):
        return self._values[item]
    
    def __iter__(self):
        return iter(self._values.values())
    
    #  METHODS  ########################################################################################################
    
    def add_config(self, config: config_value.ConfigValue):
        """Adds the provided configuration to the specification.
        
        Args:
            config (:class:`config_value.ConfigValue`): The configuration to add.
        
        Raises:
            ValueError: If a config with the same name exists already.
            TypeError: If ``config`` is not of type :class:`config_value.ConfigValue`.
        """
        insanity.sanitize_type("config", config, config_value.ConfigValue)
        if config.name in self._values:
            raise ValueError("This specification contains a configuration with name '{}' already!".format(config.name))
        
        self._values[config.name] = config
    
    @classmethod
    def create_spec(cls, config_cls: type):
        """Creates a configuration specification based on the provided class.

        The created specification defines one option for each property of the given class except those that start with
        an underscore. Members whose names start with :attr:`DEFAULT_PREFIX` are assumed to define default values for
        options. Type and description for each of the options are extracted from the first line of the corresponding
        docstring.
        
        Args:
            config_cls (type): The class that the configuration is based on.
        """
        spec = ConfigSpec()

        # load default values
        default_values = {}
        for name, field in inspect.getmembers(config_cls, lambda f: not inspect.isroutine(f)):
            if name.startswith(argmagic.DEFAULT_PREFIX):
                field_name = name[len(argmagic.DEFAULT_PREFIX):].lower()
                default_values[field_name] = field

        # find all public members (that are not default values)
        for name, field in inspect.getmembers(config_cls, lambda f: isinstance(f, property)):
            
            # only consider public members
            if name.startswith("_"):
                continue

            data_type = None
            description = None
            default_value = None
            position = None
    
            # fetch and parse summary line of docstring
            if field.__doc__ is not None:
                m = re.match(cls.DOC_REGEX, field.__doc__.split("\n")[0])
                description = m.group("doc")
                data_type = pydoc.locate(m.group("type")) if m.group("type") is not None else None
            else:
                description = "No description available."
            
            # check if the field's value is specified as enum
            if argmagic.CONFIG_VALUES in field.fget.__dict__:
                data_type = field.fget.__dict__[argmagic.CONFIG_VALUES]
            
            # if not type is specified at all, then assume it is str
            if data_type is None:
                data_type = str
            
            # check if there is a default value for the current field
            if name in default_values:
                default_value = default_values[name]
                description += " (Default value: {}.)".format(default_value)
            
            # check if a position has been specified
            if argmagic.POSITION in field.fget.__dict__:
                position = field.fget.__dict__[argmagic.POSITION]
            
            # add configuration to specification
            spec.add_config(
                    config_value.ConfigValue(
                            name,
                            description,
                            data_type,
                            default_value=default_value,
                            position=position
                    )
            )
        
        return spec
    
    def keys(self) -> typing.List[str]:
        """Retrieves a list that contains the names of all configuration values that are contained in a ``ConfigSpec``.
        
        Returns:
             list[str]: A list of the names of all configuration values.
        """
        return list(self._values.keys())
