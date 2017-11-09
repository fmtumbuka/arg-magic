# -*- coding: utf-8 -*-


import enum
import typing

import insanity


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


class ConfigValue(object):
    """Describes a single value that is part of a configuration to be parsed."""
    
    def __init__(
            self,
            name: str,
            description: str,
            data_type: type,
            default_value=None,
            position: int=None
    ):
        """Creates a new instance of ``ConfigValue``.
        
        Args:
            name (str): Specifies :attr:`name`.
            description (str): Specifies :attr:`description`.
            data_type (type): Specifies :attr:`data_type`.
            default_value (optional): Specifies :attr:`default_value`.
            position (int, optional): Specifies :attr:`position`.
        
        Raises:
            ValueError: If ``data_type`` is ``bool`` and ``default_value`` is ``None``.
        """
        # define attributes for properties
        self._data_type = None
        self._default_value = None
        self._description = None
        self._exhaustive = None
        self._name = None
        self._position = None
        self._required = None
        
        # specify properties
        self.name = name
        self.description = description
        self.data_type = data_type
        self.default_value = default_value
        self.position = position
        
        # if the config value has type bool, then a default value needs to be present
        if self.data_type == bool and self.default_value is None:
            raise ValueError("A ConfigValue with data_type bool has to have a default value!")
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, ConfigValue) and
                self._data_type == other.data_type and
                self._default_value == other.default_value and
                self._description == other.description and
                self._exhaustive == other.exhaustive and
                self._name == other.name and
                self._position == other.position and
                self._required == other.required
        )
    
    def __hash__(self):
        return hash(
                "{}-{}-{}-{}-{}-{}".format(
                    self._data_type,
                    self._default_value,
                    self._description,
                    self._exhaustive,
                    self._name,
                    self._required
                )
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def data_type(self) -> typing.Union[type, enum.Enum]:
        """type: The data type of the configuration or an ``Enum`` that completely specifies its possible values."""
        return self._data_type
    
    @data_type.setter
    def data_type(self, data_type: typing.Union[type, enum.Enum]) -> None:
        insanity.sanitize_type("data_type", data_type, type)
        self._data_type = data_type
        self._exhaustive = issubclass(data_type, enum.Enum)
    
    @property
    def default_value(self) -> typing.Any:
        """The default value of the specified configuration."""
        return self._default_value
    
    @default_value.setter
    def default_value(self, default_value) -> None:
        self._default_value = default_value
        self._required = default_value is None
    
    @property
    def description(self) -> str:
        """str: A description of the specified configuration."""
        return self._description
    
    @description.setter
    def description(self, description: str) -> None:
        self._description = str(description)
    
    @property
    def exhaustive(self) -> bool:
        """bool: Indicates whether the possible values of the configuration are specified exhaustively.
        
        The possible values of a configuration are considered to be specified exhaustively, if the :attr:`data_type` is
        given by means of an ``Enum``.
        """
        return self._exhaustive
    
    @property
    def name(self) -> str:
        """str: The name of the specified configuration."""
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = str(name)
    
    @property
    def position(self) -> typing.Union[int, None]:
        """int: Indicates the position of the specified configuration.
        
        This attributes is only considered if the specified configuration is required, i.e., positional.
        """
        return self._position
    
    @position.setter
    def position(self, position: typing.Union[int, None]):
        insanity.sanitize_type("position", position, int, none_allowed=True)
        if position is not None:
            insanity.sanitize_range("position", position, minimum=0)
        self._position = position

    @property
    def required(self) -> bool:
        """bool: Indicates whether the specified configuration has to be provided by a user.
        
        This is the case if and only if no :attr:`default_value` is specified.
        """
        return self._required
