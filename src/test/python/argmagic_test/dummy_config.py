# -*- coding: utf-8 -*-


from argmagic import decorators
from argmagic_test import dummy_enum


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


class DummyConfig(object):
    
    DEFAULT_X = dummy_enum.DummyEnum.UNO.value
    DEFAULT_Z = 666.666
    
    def __init__(self):
        self._x = self.DEFAULT_X
        self._y = None
        self._z = self.DEFAULT_Z
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, DummyConfig) and
                self._x == other.x and
                self._y == other.y and
                self._z == other.z
        )
    
    def __str__(self):
        return "(x = {}, y = '{}', z = {})".format(self._x, self._y, self._z)

    #  PROPERTIES  #####################################################################################################
    
    @decorators.exhaustive(dummy_enum.DummyEnum)
    @property
    def x(self):
        """Prop x."""
        return self._x
    
    @x.setter
    def x(self, x):
        if x not in [e.value for e in dummy_enum.DummyEnum.__members__.values()]:
            raise ValueError("Illegal value: {}".format(x))
        self._x = x
    
    @property
    def y(self):
        # Here is the docstring missing. Therefore, y is assumed to be of type str.
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y
    
    @property
    def z(self):
        """float: Prop z."""
        return self._z
    
    @z.setter
    def z(self, z):
        if not isinstance(z, float):
            raise TypeError("Illegal value: {}".format(z))
        self._z = z
