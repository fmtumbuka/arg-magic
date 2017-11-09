#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from argmagic import config_spec
from argmagic import config_value
from argmagic_test import dummy_config
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


class ConfigSpecTest(unittest.TestCase):
    
    # noinspection PyTypeChecker
    def test_create_spec(self):
        target = config_spec.ConfigSpec()
        target.add_config(
                config_value.ConfigValue(
                        "x",
                        "Prop x. (Default value: {}.)".format(dummy_config.DummyConfig.DEFAULT_X),
                        dummy_enum.DummyEnum,
                        default_value=dummy_config.DummyConfig.DEFAULT_X
                )
        )
        target.add_config(config_value.ConfigValue("y", "No description available.", str))
        target.add_config(
                config_value.ConfigValue(
                        "z",
                        "Prop z. (Default value: {}.)".format(dummy_config.DummyConfig.DEFAULT_Z),
                        float,
                        default_value=dummy_config.DummyConfig.DEFAULT_Z
                )
        )
        
        self.assertEqual(target, config_spec.ConfigSpec.create_spec(dummy_config.DummyConfig))


if __name__ == "__main__":
    unittest.main()
