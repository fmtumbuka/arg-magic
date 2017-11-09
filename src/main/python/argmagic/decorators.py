# -*- coding: utf-8 -*-

"""This module defines various decorators that can be used to specify additional information about properties of a
configuration class.
"""


import enum
import typing

import insanity

import argmagic


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


def exhaustive(values: type) -> typing.Callable[[property], property]:
    """This is a decorator that allows for annotating a property of a configuration class with an ``Enum`` that
    describes the admissible values of the same.
    
    Notice that ``argmagic`` ignores this decorator for properties of type ``bool``.
    
    Args:
        values (type): An enum that specifies the admissible values of the annotated property.
    """
    insanity.sanitize_type("values", values, type)
    if not issubclass(values, enum.Enum):
        raise TypeError("The parameter <values> has to be an Enum, but type {} is not!".format(type.__name__))
    
    def _exhaustive(func: property) -> property:
        if not isinstance(func, property):
            raise TypeError("The decorator @exhaustive may be applied to properties only!")
        func.fget.__dict__[argmagic.CONFIG_VALUES] = values
        return func
    
    return _exhaustive


def position(index: int) -> typing.Callable[[property], property]:
    """A decorator that allows for specifying the position of a property of a configuration class among all parsed
    positional args.
    
    Notice that ``argmagic`` ignore this decorator if positional args are not used or if the annotated property
    defines an optional configuration value.
    
    Args:
        index (int): The index of the annotated configuration in the sequence of positional args.
    """
    insanity.sanitize_type("index", index, int)
    insanity.sanitize_range("index", index, minimum=0)
    
    def _position(func: property) -> property:
        if not isinstance(func, property):
            raise TypeError("The decorator @position may be applied to properties only!")
        func.fget.__dict__[argmagic.POSITION] = index
        return func
    
    return _position
