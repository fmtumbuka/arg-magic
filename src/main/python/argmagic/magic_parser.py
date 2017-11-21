# -*- coding: utf-8 -*-


import argparse
import collections
import re
import typing

import insanity

from argmagic import config_spec
from argmagic.parsing import default_parser_factory
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
__date__ = "Nov 08, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class MagicParser(object):
    """TODO"""
    # TODO
    
    ARG_VALUE_REGEX = r"\<[^\>]+\>"
    """str: A regex that matches parameters of the format <param_name> in error messages created by the insanity
    package.
    """
    
    #  CONSTRUCTOR  ####################################################################################################
    
    def __init__(
            self, conf_class: type,
            app_name: str=None,
            app_description: str=None,
            positional_args: bool=True,
            custom_parsers: typing.Dict[type, parser_factory.ParserFactory]=None
    ):
        """Creates a new instance of ``MagicParser``.
        
        Args:
            conf_class: A specification of the configuration that should be parsed. This can be either an instance of
                :class:`config_spec.ConfigSpec` or a configuration class. In the latter case, an according specification
                is created automatically.
            app_name (str, optional): The name of the application whose args are being parsed. This is printed in the
                help text.
            app_description (str, optional): A description of the application whose args are being parsed. This is
                printed in the help text.
            positional_args (bool, optional): Specifies whether the parser should use positional args for required
                configuration values.
            custom_parsers (dict, optional): An optional ``dict`` that maps types to objects of type
                :class:`parser_factory.ParserFactory`. This allows for providing custom parsers for configuration values
                of certain data types.
        """
        # sanitize args
        insanity.sanitize_type("conf_class", conf_class, type)
        insanity.sanitize_type("custom_parser", custom_parsers, dict, none_allowed=True)
        if custom_parsers is not None:
            insanity.sanitize_iterable("custom_parsers.keys", custom_parsers.keys(), elements_type=type)
            insanity.sanitize_iterable(
                    "custom_parsers.values",
                    custom_parsers.values(),
                    elements_type=parser_factory.ParserFactory
            )
        
        # save config class and create specification for parsing
        self._conf_class = conf_class
        self._spec = config_spec.ConfigSpec.create_spec(conf_class)
        
        # create dict that maps types to factories for adding options to our parser (that is created subsequently)
        default_factory = default_parser_factory.DefaultParserFactory(positional_args)
        factory_functions = collections.defaultdict(lambda: default_factory)
        if custom_parsers is not None:
            factory_functions.update(custom_parsers)
        
        # //////// Sort Configuration Values ---------------------------------------------------------------------------
        
        conf_indices = {}  # maps config values to indices
        max_index = 0      # store the highest index encountered yet

        # run through all values in the specification
        for conf in self._spec:
            # non-required config values are parsed as options, and thus don't need an index
            if not conf.required:
                conf_indices[conf] = -1
            # for required config values, check whether an index has been specified in the config class
            elif conf.position is not None:
                conf_indices[conf] = conf.position
                max_index = max(max_index, conf.position)
        
        # run once again through all values in the specification, and assign them (max_index + 1) as index, i.e., the
        # last position, if they don't have one yet
        for conf in self._spec:
            if conf not in conf_indices:
                conf_indices[conf] = max_index + 1
        
        # //////// Create Arg Parser -----------------------------------------------------------------------------------

        # create arg parser
        self._parser = argparse.ArgumentParser(prog=str(app_name), description=str(app_description))
        
        # run through all configuration values and add them to the arg parser
        for conf in sorted(self._spec, key=(lambda x: conf_indices[x])):
            factory_functions[conf.data_type].create_parser(self._parser, conf)
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def spec(self) -> config_spec.ConfigSpec:
        """:class:`config_spec.ConfigSpec`: The configuration that is used for parsing command-line args."""
        return self._spec
    
    #  METHODS  ########################################################################################################
    
    def error(self, msg: typing.Optional[str]) -> None:
        """Prints a usage message incorporating the provided error message to stderr and exits.
        
        If the provided message contains the names of fields in the used configuration class, then these should be
        put between angle angle brackets, e.g., ``<some_config>``. An such reference will be automatically replaced with
        the name that is printed for the respective config in the application's synopsis.
        
        Args:
            msg (str): The error message to include in the output.
        """
        # reformat parameter names such that they match the names that are printed in the synopsis
        if msg is not None:
            msg = re.sub(
                    self.ARG_VALUE_REGEX,
                    lambda m: m.group(0)[1:-1].upper(),  # maps <param_name> -> PARAM_NAME
                    msg
            )
        
        # call error function of the used parser
        self._parser.error(msg)
    
    def parse_args(self):
        """Parses the args of the current application based on the configuration class that was handed to the
        ``MagicParser``, and returns an instance of this very class that has been populated accordingly.

        Returns:
            The parsed configuration.
        """
        try:
            # parse args
            args = self._parser.parse_args()
            
            # create and populate configuration object
            conf = self._conf_class()
            for config_value in self._spec:
                # get parsed value for current config value
                value = getattr(args, config_value.name)
                
                # if current config value is optional and no value was provided -> skip
                if not config_value.required and value is None:
                    continue
                
                setattr(conf, config_value.name, value)
        
            return conf
        except (TypeError, ValueError) as e:
            self.error(str(e))
