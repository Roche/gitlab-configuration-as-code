from unittest.mock import Mock

import pytest

from gcasc import AppearanceConfigurer

from .helpers import read_yaml


@pytest.fixture()
def appearance_valid():
    return read_yaml('appearance_valid.yml')['appearance']


def test_appearance_not_updated_because_unchanged(appearance_valid):
    # given
    gitlab = Mock()
    appearance = Mock()
    appearance.title = appearance_valid['title']
    appearance.description = appearance_valid['description']
    appearance.header_message = appearance_valid['header']['message']
    gitlab.appearance.get.return_value = appearance
    configurer = AppearanceConfigurer(gitlab, appearance_valid)

    # when
    configurer.configure()

    # then
    gitlab.appearance.get.assert_called_once()
    appearance.save.assert_not_called()


def test_appearance_modified(appearance_valid):
    # given
    gitlab = Mock()
    appearance = Mock()
    appearance.title = appearance_valid['title']
    appearance.description = 'modified description'
    appearance.header_message = appearance_valid['header']['message']
    gitlab.appearance.get.return_value = appearance
    configurer = AppearanceConfigurer(gitlab, appearance_valid)

    # when
    saved = configurer.configure()

    # then
    gitlab.appearance.get.assert_called_once()
    appearance.save.assert_called_once()
    assert saved.description == appearance_valid['description']
