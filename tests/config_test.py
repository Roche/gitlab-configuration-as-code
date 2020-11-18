import pytest

from gcasc import GcascException, GitlabConfiguration


def test_error_raised_when_configuration_none():
    with pytest.raises(GcascException):
        GitlabConfiguration(None)


def test_error_raised_when_configuration_not_a_dict():
    with pytest.raises(GcascException):
        GitlabConfiguration("str")
