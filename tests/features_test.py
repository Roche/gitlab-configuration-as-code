from unittest.mock import MagicMock, Mock

import pytest
from pytest import mark

from gcasc import FeaturesConfigurer, Mode
from gcasc.exceptions import ValidationException

from .helpers import not_raises, read_yaml


@pytest.fixture()
def features_valid():
    return read_yaml("features_valid.yml")["features"]


@pytest.fixture()
def features_invalid():
    return read_yaml("features_invalid.yml")["features"]


@pytest.fixture()
def features_valid_canary():
    return read_yaml("features_valid_canary.yml")["features"]


@pytest.fixture()
def features_valid_canaries():
    return read_yaml("features_valid_canaries.yml")["features"]


def __mock_gitlab(features=[]):
    features_manager = Mock()
    features_manager.list.return_value = features
    return Mock(features=features_manager)


def test_features_configuration_valid(features_valid):
    # given
    configurer = FeaturesConfigurer(Mock(), features_valid, Mode.TEST_SKIP_VALIDATION)

    # when
    with (not_raises(ValidationException)):
        configurer.validate()


def test_features_configuration_invalid(features_invalid):
    # given
    configurer = FeaturesConfigurer(Mock(), features_invalid, Mode.TEST_SKIP_VALIDATION)

    # when
    with pytest.raises(ValidationException) as error:
        configurer.validate()

    # then
    result = error.value.result
    assert len(result.get()) == 2
    assert result.has_error(message="name", path=0)
    assert result.has_error(message="value", path=0)


def test_existing_features_removed_before_applying():
    # given
    feature1 = Mock()
    feature2 = Mock()
    features = [feature1, feature2]
    gitlab = __mock_gitlab(features)
    configurer = FeaturesConfigurer(gitlab, [])

    # when
    configurer.configure()

    # then
    feature1.delete.assert_called_once()
    feature2.delete.assert_called_once()


def test_canaries_configured_when_in_config(features_valid_canary):
    # given
    feature = features_valid_canary[0]
    name = feature["name"]
    value = feature["value"]
    user = feature["users"][0]
    group = feature["groups"][0]
    project = feature["projects"][0]
    gitlab = __mock_gitlab()
    configurer = FeaturesConfigurer(gitlab, features_valid_canary)

    # when
    configurer.configure()

    # then
    gitlab.features.set.assert_any_call(name, value, feature_group=None, user=user)

    gitlab.features.set.assert_any_call(name, value, feature_group=None, group=group)

    gitlab.features.set.assert_any_call(
        name, value, feature_group=None, project=project
    )


def test_multiple_canaries_are_configured(features_valid_canaries):
    # given
    gitlab = __mock_gitlab()
    configurer = FeaturesConfigurer(gitlab, features_valid_canaries)

    # when
    configurer.configure()

    # then
    assert gitlab.features.set.call_count == 4


@mark.parametrize("mode", [Mode.TEST, Mode.TEST_SKIP_VALIDATION])
def test_configuration_not_applied_when_in_mode_other_than_not_apply(
    features_valid, mode
):
    # given
    gitlab = __mock_gitlab()
    configurer = FeaturesConfigurer(gitlab, features_valid, mode)

    # when
    configurer.configure()

    # then
    assert gitlab.features.set.call_count == 0
