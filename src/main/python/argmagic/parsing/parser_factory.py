# -*- coding: utf-8 -*-


import abc
import argparse

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
__date__ = "Nov 09, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class ParserFactory(metaclass=abc.ABCMeta):
    """An abstract base class for factory classes whose instances may be used for adding arguments to arg parsers."""
    
    @abc.abstractmethod
    def create_parser(
            self,
            parser: argparse.ArgumentParser,
            config: config_value.ConfigValue
    ) -> argparse.ArgumentParser:
        """Adds the provided configuration as argument to the given arg parser.
        
        Args:
            parser (argparse.ArgumentParser): The parser to add an argument for ``config`` to.
            config (:class:`config_value.ConfigValue`): A configuration value that should be added as an argument to
                ``parser``.
        
        Returns:
            argparse.ArgumentParser: Returns the provided ``parsers`` that an argument was added to.
        """
        pass
