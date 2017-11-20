# -*- coding: utf-8 -*-


import numbers
import typing

import insanity

from argmagic import decorators


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017, Patrick Hohenecker\n"
        "All rights reserved.\n"
        "\n"
        "Redistribution and use in source and binary forms, with or without\n"
        "modification, are permitted provided that the following conditions are met:\n"
        "\n"
        "1. Redistributions of source code must retain the above copyright notice, this\n"
        "   list of conditions and the following disclaimer.\n"
        "2. Redistributions in binary form must reproduce the above copyright notice,\n"
        "   this list of conditions and the following disclaimer in the documentation\n"
        "   and/or other materials provided with the distribution.\n"
        "\n"
        "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"
        "ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"
        "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
        "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\n"
        "ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"
        "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\n"
        "ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"
        "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"
        "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
)
__license__ = "Simplified BSD License"
__version__ = "2017.1"
__date__ = "Nov 20, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class DummyConfig3(object):
    
    DEFAULT_A = "default"
    """str: Default value of :attr:`a`."""
    
    #  CONSTRUCTOR  ####################################################################################################
    
    def __init__(self):
        self._a = self.DEFAULT_A
        self._b = None
        self._c = None
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, DummyConfig3) and
                other.a == self._a and
                other.b == self._b and
                other.c == self._c
        )
    
    def __str__(self):
        return "(a = '{}', b = {}, c = {})".format(self._a, self._b, self._c)
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def a(self) -> str:
        """str: Config a."""
        return self._a
    
    @a.setter
    def a(self, a: str) -> None:
        self._a = str(a)

    @property
    def b(self) -> typing.Optional[float]:
        """float: Config b."""
        return self._b

    @b.setter
    def b(self, b: numbers.Real) -> None:
        insanity.sanitize_type("b", b, numbers.Real)
        self._b = float(b)

    @decorators.optional
    @property
    def c(self) -> typing.Optional[int]:
        """int: Config c."""
        return self._c

    @c.setter
    def c(self, c: int) -> None:
        insanity.sanitize_type("c", c, int)
        self._c = c
