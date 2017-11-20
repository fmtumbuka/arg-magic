# -*- coding: utf-8 -*-


import argparse
import enum
import types

import insanity
import yaml

from argmagic import config_value
from argmagic.parsing import parser_factory


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


class DefaultParserFactory(parser_factory.ParserFactory):
    """A simple implementation of :class:`parser_factory.ParserFactory` that supports configurations with data types
    ``str``, ``int``, ``float`` as well as lists and dictionaries that contain those types only. Furthermore,
    configurations whose admissible values are given by means of an ``Enum`` can be handled by instances of this class.
    """
    
    SUPPORTED_TYPES = [bool, str, int, float, dict, list]
    """list[type]: A list of all data types that are supported by a ``DefaultParserFactory``."""
    
    #  CONSTRUCTOR  ####################################################################################################
    
    def __init__(self, positional_args: bool):
        """Creates a new instance of ``DefaultParserFactory``.
        
        Args:
            positional_args (bool): Specifies whether required configuration values should be treated as positional
                args.
        """
        self._positional_args = positional_args
    
    #  METHODS  ########################################################################################################
    
    def create_parser(
            self,
            parser: argparse.ArgumentParser,
            config: config_value.ConfigValue
    ) -> argparse.ArgumentParser:
        """
        Raises:
            ValueError: If the type of the provided ``config`` is not supported by the ``DefaultParserFactory``.
        """
        # sanitize args
        insanity.sanitize_type("parser", parser, argparse.ArgumentParser)
        insanity.sanitize_type("config", config, config_value.ConfigValue)
        
        # check if the type of the provided config is supported
        if not issubclass(config.data_type, enum.Enum) and config.data_type not in self.SUPPORTED_TYPES:
            raise ValueError(
                    "The data type of the provided <config> is not supported: {}!".format(config.data_type.__qualname__)
            )

        # the names of the command line args are simply those of the corresponding config values where
        # underscores are replaced with dashes
        # furthermore, optional args get "--" prepended to their names
        arg_name = config.name.replace("_", "-")
        if not self._positional_args or not config.required:
            arg_name = "--" + arg_name

        # boolean optional are treated differently (notice that they are required to have default values)
        # if the default value is True, then the name of the according option starts with "--no-"
        if config.data_type == bool:
            if config.default_value:
                arg_name = "--no-" + arg_name[2:]
            parser.add_argument(
                    arg_name,
                    dest=config.name,
                    action="store_const",
                    const=not config.default_value,
                    default=config.default_value,
                    help=config.description
            )
        else:
            if config.exhaustive:
                arg_type = self._enum_type(config.data_type)
            elif config.data_type == dict or config.data_type == list:
                arg_type = yaml.load
            else:
                arg_type = config.data_type
    
            if self._positional_args and config.required:
                parser.add_argument(
                        config.name,
                        type=arg_type,
                        default=config.default_value,
                        help=config.description
                )
            else:
                parser.add_argument(
                        arg_name,
                        dest=config.name,
                        type=arg_type,
                        default=config.default_value,
                        help=config.description
                )
        
        return parser

    @staticmethod
    def _enum_type(cls: enum.Enum) -> types.FunctionType:
        """Creates a function that may be passed to an ``argparse.ArgumentParser`` for handling an option that is
        described by the provided ``Enum``.

        Args:
            cls (enum.Enum): The ``Enum`` that describes the option.

        Returns:
            function: A function that can be passed to an ``ArgumentParser`` via the keyword arg ``type`` of the method
                ``add_argument``.
        """
    
        # noinspection PyUnresolvedReferences
        def type_func(val: str):
            if val not in cls.__members__.keys():
                raise ValueError(
                    "illegal value '%s', possible values are {%s}" % (val, ", ".join(cls.__members__.keys())))
            return cls[val].value
    
        return type_func
