# -*- coding: utf-8 -*-

"""The root of the python package argmagic."""


import inspect
import typing

from argmagic import magic_parser


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
__date__ = "Jul 05, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Production"


CONFIG_VALUES = "argmagic.config_values"
"""str: The key that is used for storing configuration values that are specified as ``Enum``s."""

DEFAULT_PREFIX = "DEFAULT_"
"""str: A prefix that identifies class variables as default values."""

OPTIONAL_KEY = "argmagic.optional"
"""str: The key that is used for storing that an arg is optional."""

POSITION = "argmagic.position"
"""str: The key that is used for storing the position of positional args."""


def get_config(conf) -> typing.Dict[str, str]:
    """Creates a ``dict`` that summarizes the values of the members of the provided object.

    This function considers all members of ``conf`` whose names do neither start with an underscore nor with
    :attr:`DEFAULT_PREFIX`, and converts their values into strings.

    Args:
        conf: The object to be summarized.

    Returns:
        dict: Maps the names of the considered members to their according values as strings.

    Raises:
        TypeError: If ``conf`` is ``None``.
    """
    if conf is None:
        raise TypeError("The parameter <conf> must not be None!")

    str_conf = {}

    for p, v in inspect.getmembers(conf):
        if p.startswith("_") or p.startswith(DEFAULT_PREFIX):
            continue
        str_conf[p] = str(v)

    return str_conf


def parse_args(
        conf_class,
        app_name: str=None,
        app_description: str=None,
        positional_args: bool=True
):
    """Parses the args of the current application based on the provided configuration class, and returns an instance of
    the same that is populated accordingly.

    Args:
        conf_class: The type of the configuration object that should be parsed from the command line args.
        app_name (str): The name of the application that is printed in the synopsis.
        app_description (str): The description of the application that is printed in the synopsis.
        positional_args (bool, optional): Indicates whether required config values should be parsed as positional args.

    Returns:
        The parsed configuration as an object of type ``conf_class``.
    """
    return magic_parser.MagicParser(
            conf_class,
            app_name=app_name,
            app_description=app_description,
            positional_args=positional_args
    ).parse_args()
