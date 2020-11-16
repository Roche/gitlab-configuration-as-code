from unittest.mock import Mock

import pytest

from gcasc import InstanceVariablesConfigurer
from .helpers import read_yaml


@pytest.fixture()
def variables_valid():
    return read_yaml("instance_variables_valid.yml")["instance_variables"]


def test_variables_unchanged(variables_valid):
    # given
    gitlab = Mock()

    var1 = Mock()
    var1.key = "var1"
    var1.value = variables_valid["var1"]

    var2 = Mock()
    var2.key = "var2"
    var2.value = variables_valid["var2"]["value"]
    var2.protected = variables_valid["var2"]["protected"]

    var3 = Mock()
    var3.key = "var3"
    var3.value = variables_valid["var3"]["value"]
    var3.masked = variables_valid["var3"]["masked"]

    variables = [var1, var2, var3]

    gitlab.variables.list.return_value = variables
    configurer = InstanceVariablesConfigurer(gitlab, variables_valid)

    # when
    configurer.configure()

    # then
    gitlab.variables.list.assert_called_once()
    var1.save.assert_not_called()
    var2.save.assert_not_called()
    var3.save.assert_not_called()


def test_variables_changed(variables_valid):
    # given
    gitlab = Mock()

    var1 = Mock()
    var1.key = "var1"
    var1.value = "changed value"

    var2 = Mock()
    var2.key = "var2"
    var2.value = variables_valid["var2"]["value"]
    var2.protected = False

    not_exist = Mock()
    not_exist.key = "not existent"
    not_exist.value = "not existent"

    variables = [var1, var2, not_exist]

    gitlab.variables.list.return_value = variables
    configurer = InstanceVariablesConfigurer(gitlab, variables_valid)

    # when
    configurer.configure()

    # then
    gitlab.variables.list.assert_called_once()
    var1.save.assert_called_once()
    var2.save.assert_called_once()
    not_exist.delete.assert_called_once()
    gitlab.variables.create.assert_called_once_with({**variables_valid["var3"], "key": "var3"})
