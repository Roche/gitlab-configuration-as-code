import pytest

from gcasc import GitlabConfiguration


def test_error_raised_when_configuration_none():
    with pytest.raises(RuntimeError):
        GitlabConfiguration(None)


def test_error_raised_when_configuration_not_a_dict():
    with pytest.raises(RuntimeError):
        GitlabConfiguration("str")
