from unittest.mock import Mock

import pytest

from gcasc import Mode, SettingsConfigurer

from .helpers import read_yaml


@pytest.fixture()
def settings_valid():
    return read_yaml('settings_valid.yml')['settings']


def test_settings_not_updated_because_unchanged(settings_valid):
    # given
    gitlab = Mock()
    settings = Mock()
    settings.auto_devops_enabled = settings_valid['auto_devops_enabled']
    settings.help_page_text = settings_valid['help_page']['text']
    settings.help_page_support_url = settings_valid['help_page']['support_url']
    settings.polling_interval_multiplier = settings_valid['polling_interval_multiplier']
    gitlab.settings.get.return_value = settings
    configurer = SettingsConfigurer(gitlab, settings_valid)

    # when
    configurer.configure()

    # then
    gitlab.settings.get.assert_called_once()
    settings.save.assert_not_called()


def test_settings_modified(settings_valid):
    # given
    gitlab = Mock()
    settings = Mock()
    settings.auto_devops_enabled = settings_valid['auto_devops_enabled']
    settings.help_page_text = 'modified help page text'
    settings.help_page_support_url = settings_valid['help_page']['support_url']
    settings.polling_interval_multiplier = settings_valid['polling_interval_multiplier']
    gitlab.settings.get.return_value = settings
    configurer = SettingsConfigurer(gitlab, settings_valid)

    # when
    saved = configurer.configure()

    # then
    gitlab.settings.get.assert_called_once()
    settings.save.assert_called_once()
    assert saved.help_page_text == settings_valid['help_page']['text']


def test_invalid_configuration_options_are_skipped(settings_valid):
    # given
    gitlab = Mock()
    settings = Mock()
    settings.help_page_text = settings_valid['help_page']['text']
    gitlab.settings.get.return_value = settings
    configurer = SettingsConfigurer(gitlab, settings_valid)

    # when
    configurer.configure()

    # then
    gitlab.settings.get.assert_called_once()


@pytest.mark.parametrize('mode', [Mode.TEST, Mode.TEST_SKIP_VALIDATION])
def test_no_changes_in_not_apply_mode(mode, settings_valid):
    # given
    text = 'modified help page text'
    gitlab = Mock()
    settings = Mock()
    settings.help_page_text = text
    gitlab.settings.get.return_value = settings
    configurer = SettingsConfigurer(gitlab, settings_valid, mode)

    # when
    saved = configurer.configure()

    # then
    gitlab.settings.get.assert_called_once()
    settings.save.assert_not_called()
    assert saved.help_page_text == text
