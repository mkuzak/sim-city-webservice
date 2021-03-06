# SIM-CITY webservice
#
# Copyright 2015 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import simcityweb.cli
from simcityweb.cli import (confirm, dialog, choice_dialog, new_or_overwrite)
from nose.tools import assert_equals, assert_raises, assert_true, assert_false
import tempfile
import os


class CliInput(object):
    def __init__(self, responses):
        self.i = 0
        self.responses = responses
        self.messages = [None] * len(responses)
        simcityweb.cli._input_mechanism = self.input

    def input(self, message):
        j = self.i % len(self.responses)
        self.i += 1
        self.messages[j] = message
        return self.responses[j]


def test_confirm_positive():
    my_input = CliInput(["y"])
    assert_equals(True, confirm("lalala",
                  default_response=True))
    assert_equals("lalala [Y/n]? ", my_input.messages[0])
    assert_equals(True, confirm("lalala",
                  default_response=False))
    assert_equals("lalala [y/N]? ", my_input.messages[0])


def test_confirm_negative():
    my_input = CliInput(["n"])
    assert_equals(False, confirm("lalala",
                  default_response=True))
    assert_equals("lalala [Y/n]? ", my_input.messages[0])
    assert_equals(False, confirm("lalala",
                  default_response=False))
    assert_equals("lalala [y/N]? ", my_input.messages[0])


def test_confirm_empty():
    my_input = CliInput([""])
    assert_equals(True, confirm("lalala",
                  default_response=True))
    assert_equals("lalala [Y/n]? ", my_input.messages[0])
    assert_equals(False, confirm("lalala",
                  default_response=False))
    assert_equals("lalala [y/N]? ", my_input.messages[0])



def test_confirm_invalid():
    my_input = CliInput(["neither", ""])
    assert_equals(True, confirm("lalala",
                  default_response=True))
    assert_equals("lalala [Y/n]? ", my_input.messages[0])
    assert_equals("Please answer yes or no. lalala [Y/n]? ",
                  my_input.messages[1])
    assert_equals(False, confirm("lalala",
                  default_response=False))
    assert_equals("lalala [y/N]? ", my_input.messages[0])
    assert_equals("Please answer yes or no. lalala [y/N]? ",
                  my_input.messages[1])


def test_choice_dialog():
    my_input = CliInput(["option0"])
    assert_equals("option0", choice_dialog("opt", ("option0", "option1")))
    assert_equals("opt ('option0', 'option1'): ", my_input.messages[0])


def test_choice_dialog_invalid_option():
    my_input = CliInput(["option3", "option0"])
    assert_equals("option0", choice_dialog("opt", ("option0", "option1")))
    assert_equals("opt ('option0', 'option1'): ", my_input.messages[0])
    assert_equals("Value 'option3' invalid. opt ('option0', 'option1'): ",
                  my_input.messages[1])


def test_choice_dialog_default_option():
    CliInput([""])
    assert_equals("option1", choice_dialog("opt", ("option0", "option1"),
        default_response="option1"))


def test_choice_dialog_invalid_default_option_raises():
    CliInput([""])
    assert_raises(ValueError, choice_dialog, "opt", ("option0", "option1"),
                  default_response="option3")


def test_choice_dialog_empty_options_raises():
    CliInput([""])
    assert_raises(ValueError, choice_dialog, "opt", [])


def test_dialog():
    my_input = CliInput(["val"])
    assert_equals("val", dialog("opt"))
    assert_equals("opt: ", my_input.messages[0])


def test_dialog_invalid():
    my_input = CliInput(["", "val"])
    assert_equals("val", dialog("opt"))
    assert_equals("opt: ", my_input.messages[0])
    assert_equals("Value '' invalid. opt: ", my_input.messages[1])


def test_dialog_default():
    CliInput([""])
    assert_equals("def", dialog("opt", "def"))


def test_dialog_default_override():
    CliInput(["faa"])
    assert_equals("faa", dialog("opt", "def"))


def test_new_or_overwrite_no_exist():
    fd, filename = tempfile.mkstemp()
    os.remove(filename)
    assert_true(new_or_overwrite(filename))


def test_new_or_overwrite_exist():
    fd, filename = tempfile.mkstemp()
    try:
        my_input = CliInput([""])
        assert_false(new_or_overwrite(filename))
        assert_false(my_input.messages[0] is None)
        my_input = CliInput(["n"])
        assert_false(new_or_overwrite(filename))
        assert_false(my_input.messages[0] is None)
        my_input = CliInput(["y"])
        assert_true(new_or_overwrite(filename))
        assert_false(my_input.messages[0] is None)
    finally:
        os.remove(filename)
