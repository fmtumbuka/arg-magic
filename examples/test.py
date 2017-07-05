#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""A simple example that demonstrates the use of the package argmagic.

Run ``python3 test.py --help`` to have a synopsis printed to the screen, and
``python3 test.py --name "better name" --data-type INTEGER`` to see a concrete example.
"""


import enum

import argmagic


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


class MyConfig(object):
    """An example of a configuration class."""

    DEFAULT_DATA_TYPE = str
    DEFAULT_NAME = "no name"

    def __init__(self):
        self._data_type = MyConfig.DEFAULT_DATA_TYPE
        self._name = MyConfig.DEFAULT_NAME

    @property
    def data_type(self) -> type:
        """type: An example of an option that describes a type, and has to be either int or str."""
        return self._data_type

    @data_type.setter
    def data_type(self, data_type: type) -> None:
        if data_type != str and data_type != int:
            raise ValueError("The arg <data_type> has to be the type int or the type str, but is %s!" % data_type)
        self._data_type = data_type

    @property
    def name(self) -> str:
        """str: An example of an option of type str."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("The arg <name> has to be of type str, but is %s!" % type(name))
        self._name = name


class DataTypeOption(enum.Enum):
    """Describes the option MyConfig.data_type."""

    INTEGER = int
    STRING = str


# parse the args that were provided to this script
config = argmagic.parse_args(
        MyConfig,
        fixed_types={"data_type": DataTypeOption},
        app_name="Test",
        app_description="This is an example that demonstrates the use of the package argmagic."
)


# print the parsed configuration
print("CONFIGURATION OF TYPE %s:" % type(config))
for option, value in argmagic.get_config(config).items():
    print("*", option, "-", value)
