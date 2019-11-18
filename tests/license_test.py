import pytest

from unittest.mock import Mock
from gcasc import LicenseConfigurer
from gcasc import Mode
from .helpers import read_yaml


@pytest.fixture()
def license_valid():
    return read_yaml('license_valid.yml')['license']


@pytest.fixture()
def license_invalid():
    return read_yaml('license_invalid_1.yml')['license']


def test_license_configuration_valid(license_valid):
    # given
    configurer = LicenseConfigurer(Mock(), license_valid, Mode.TEST_SKIP_VALIDATION)

    # when
    result = configurer.validate()

    # then
    assert not result.has_errors()


def test_license_configuration_invalid(license_invalid):
    # given
    configurer = LicenseConfigurer(Mock(), license_invalid, Mode.TEST_SKIP_VALIDATION)

    # when
    result = configurer.validate()

    # then
    assert result.has_errors()
    assert result.errors.__len__() == 4
    assert result.has_error('starts_at')
    assert result.has_error('plan')
    assert result.has_error('user_limit')
    assert result.has_error('data')


def test_license_not_updated_because_same_exists(license_valid):
    # given
    gitlab = Mock()
    gitlab.get_license.return_value = {
        'starts_at': license_valid['starts_at'],
        'plan': license_valid['plan'],
        'user_limit': license_valid['user_limit'],
    }
    configurer = LicenseConfigurer(gitlab, license_valid)

    # when
    configurer.configure()

    # then
    gitlab.get_license.assert_called_once()
    gitlab.set_license.assert_not_called()


def test_license_updated(license_valid):
    # given
    gitlab = Mock()
    gitlab.get_license.return_value = {
        'starts_at': '1900-01-01',
        'plan': license_valid['plan'],
        'user_limit': license_valid['user_limit'],
    }
    configurer = LicenseConfigurer(gitlab, license_valid)

    # when
    configurer.configure()

    # then
    gitlab.get_license.assert_called_once()
    gitlab.set_license.assert_called_once_with(license_valid['data'])


