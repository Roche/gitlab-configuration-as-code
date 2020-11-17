from unittest.mock import Mock

import pytest

from gcasc import InstanceVariablesConfigurer, Mode
from gcasc.exceptions import ValidationException

from .helpers import read_yaml


@pytest.fixture()
def variables_valid():
    return read_yaml("instance_variables_valid.yml")["instance_variables"]


@pytest.fixture()
def variables_invalid():
    return read_yaml("instance_variables_invalid.yml")["instance_variables"]


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
    gitlab.variables.create.assert_called_once_with(
        {**variables_valid["var3"], "key": "var3"}
    )


def test_variables_invalid(variables_invalid):
    # given
    configurer = InstanceVariablesConfigurer(
        Mock(), variables_invalid, Mode.TEST_SKIP_VALIDATION
    )

    # when
    with pytest.raises(ValidationException) as error:
        configurer.validate()

    # then
    result = error.value.result
    assert len(result.get()) == 5
    assert result.has_error(message="pattern", path="inv@lid")
    assert result.has_error(message="not of type", path="var1")
    assert result.has_error(message="value", path="var2")
    assert result.has_error(message="8 chars", path=["var3", "value"])
    assert result.has_error(message="not one of", path=["var4", "variable_type"])
