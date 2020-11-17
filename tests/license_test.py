from unittest.mock import Mock

import pytest

from gcasc import LicenseConfigurer, Mode
from gcasc.exceptions import ValidationException

from .helpers import not_raises, read_yaml


@pytest.fixture()
def license_valid():
    return read_yaml("license_valid.yml")["license"]


@pytest.fixture()
def license_invalid():
    return read_yaml("license_invalid_1.yml")["license"]


def test_license_configuration_valid(license_valid):
    # given
    configurer = LicenseConfigurer(Mock(), license_valid, Mode.TEST_SKIP_VALIDATION)

    # when
    with (not_raises(ValidationException)):
        configurer.validate()


def test_license_configuration_invalid(license_invalid):
    # given
    configurer = LicenseConfigurer(Mock(), license_invalid, Mode.TEST_SKIP_VALIDATION)

    # when
    with pytest.raises(ValidationException) as error:
        configurer.validate()

    # then
    result = error.value.result
    assert len(result.get()) == 5
    assert result.has_error_message("user_limit")
    assert result.has_error_message("data")
    assert result.has_error_path("expires_at")
    assert result.has_error_path("plan")
    assert result.has_error_path("starts_at")


def test_license_not_updated_because_same_exists(license_valid):
    # given
    gitlab = Mock()
    gitlab.get_license.return_value = {
        "starts_at": license_valid["starts_at"],
        "expires_at": license_valid["expires_at"],
        "plan": license_valid["plan"],
        "user_limit": license_valid["user_limit"],
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
        "starts_at": "1900-01-01",
        "expires_at": license_valid["expires_at"],
        "plan": license_valid["plan"],
        "user_limit": license_valid["user_limit"],
    }
    configurer = LicenseConfigurer(gitlab, license_valid)

    # when
    configurer.configure()

    # then
    gitlab.get_license.assert_called_once()
    gitlab.set_license.assert_called_once_with(license_valid["data"])
