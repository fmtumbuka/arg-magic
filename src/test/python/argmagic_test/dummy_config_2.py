# -*- coding: utf-8 -*-


from argmagic import decorators


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
__date__ = "Nov 09, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class DummyConfig2(object):
    
    def __init__(self):
        self._a = None
        self._b = None
        self._c = None
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, DummyConfig2) and
                self._a == other.a,
                self._b == other.b,
                self._c == other.c
        )
    
    def __str__(self):
        return "(a = '{}', b = '{}', c = '{}')".format(self._a, self._b, self._c)
    
    #  PROPERTIES  #####################################################################################################
    
    @decorators.position(1)
    @property
    def a(self):
        return self._a
    
    @a.setter
    def a(self, a):
        self._a = a

    @decorators.position(2)
    @property
    def b(self):
        return self._b
    
    @b.setter
    def b(self, b):
        self._b = b

    @decorators.position(0)
    @property
    def c(self):
        return self._c
    
    @c.setter
    def c(self, c):
        self._c = c
