import os

import pytest
from mock import Mock, patch

from gcasc import ClientInitializationError, GitlabConfigurationAsCode, Mode
from tests import helpers

GITLAB_CLIENT_CONFIG_FILE = ["GITLAB_CLIENT_CONFIG", "GITLAB_CLIENT_CONFIG_FILE"]
GITLAB_CLIENT_CERTIFICATE = ["GITLAB_CLIENT_CERT", "GITLAB_CLIENT_CERTIFICATE"]
GITLAB_CLIENT_KEY = "GITLAB_CLIENT_KEY"
GITLAB_CLIENT_URL = "GITLAB_CLIENT_URL"
GITLAB_CLIENT_API_VERSION = "GITLAB_CLIENT_API_VERSION"
GITLAB_CLIENT_TOKEN = "GITLAB_CLIENT_TOKEN"
GITLAB_CLIENT_SSL_VERIFY = "GITLAB_CLIENT_SSL_VERIFY"
GITLAB_CONFIG_FILE = ["GITLAB_CONFIG_FILE", "GITLAB_CONFIG_PATH"]

GITLAB_MODE = "GITLAB_MODE"

GITLAB_CONFIG_FILE_DEFAULT_PATHS = [
    "/etc/python-gitlab.cfg",
    "/etc/gitlab.cfg",
    "~/.python-gitlab.cfg",
    "~/.gitlab.cfg",
]


def __mock_gitlab(gitlab_class_mock):
    gitlab = Mock()
    gitlab.version.return_value = ('test', 'test')
    gitlab_class_mock.from_config.return_value = gitlab
    gitlab_class_mock.return_value = gitlab
    return gitlab


@pytest.fixture(scope="class", autouse=True)
def configure_shared_environment(request):
    os.environ['GITLAB_CONFIG_FILE'] = helpers.get_file_path('gitlab.yml')

    gitlab_patch = patch('gitlab.Gitlab')
    gitlab_mock_class = gitlab_patch.__enter__()
    __mock_gitlab(gitlab_mock_class)

    def unpatch():
        gitlab_patch.__exit__()

    def clean_env():
        for key, value in os.environ.items():
            if key.startswith('GITLAB_'):
                del os.environ[key]

    request.addfinalizer(unpatch)
    request.addfinalizer(clean_env)


@patch('gitlab.Gitlab')
def test_gitlab_client_created_from_config_file(gitlab_class_mock):
    # given
    config_path = helpers.get_file_path('gitlab_config_valid.cfg')
    os.environ['GITLAB_CLIENT_CONFIG_FILE'] = config_path
    __mock_gitlab(gitlab_class_mock)

    # when
    GitlabConfigurationAsCode()

    # then
    gitlab_class_mock.assert_called_once_with(private_token='my_token', url='https://my.gitlab.com',
                                              ssl_verify=False, api_version='4')


@patch('gitlab.Gitlab')
def test_gitlab_client_created_from_environment(gitlab_class_mock):
    os.environ['GITLAB_CLIENT_TOKEN'] = 'token'
    os.environ['GITLAB_CLIENT_URL'] = 'url'
    os.environ['GITLAB_CLIENT_API_VERSION'] = 'api_version'
    os.environ['GITLAB_CLIENT_SSL_VERIFY'] = 'ssl_verify'
    __mock_gitlab(gitlab_class_mock)

    # when
    GitlabConfigurationAsCode()

    # then
    gitlab_class_mock.assert_called_once_with(private_token='token', url='url', ssl_verify='ssl_verify',
                                              api_version='api_version')

@patch('gitlab.Gitlab')
def test_gitlab_client_created_from_file_and_environment(gitlab_class_mock):
    # given
    config_path = helpers.get_file_path('gitlab_config_invalid.cfg')
    os.environ['GITLAB_CLIENT_CONFIG_FILE'] = config_path
    os.environ['GITLAB_CLIENT_TOKEN'] = 'token'
    os.environ['GITLAB_CLIENT_URL'] = 'url'
    os.environ['GITLAB_CLIENT_API_VERSION'] = 'api_version'
    os.environ['GITLAB_CLIENT_SSL_VERIFY'] = 'ssl_verify'
    __mock_gitlab(gitlab_class_mock)

    # when
    GitlabConfigurationAsCode()

    # then
    gitlab_class_mock.assert_called_once_with(private_token='token', url='https://my.gitlab.com',
                                              ssl_verify=True, api_version='api_version')


def test_gitlab_config_loaded_from_file():
    # given
    os.environ['GITLAB_CLIENT_TOKEN'] = 'some_token'

    # when
    gcasc = GitlabConfigurationAsCode()

    # then
    assert gcasc.config.config == helpers.read_yaml('gitlab.yml')


def test_session_initialized_when_config_provided():
    certificate = helpers.get_file_path('dummycert.crt')
    key = helpers.get_file_path('dummykey.key')
    os.environ['GITLAB_CLIENT_TOKEN'] = 'token'
    os.environ['GITLAB_CLIENT_CERTIFICATE'] = certificate
    os.environ['GITLAB_CLIENT_KEY'] = key

    gcasc = GitlabConfigurationAsCode()

    assert gcasc.gitlab.session.cert == (certificate, key)


def test_error_raised_when_unable_to_create_gitlab_client():
    with pytest.raises(ClientInitializationError) as error:
        GitlabConfigurationAsCode()

        assert "config file" in error
        assert "environment variables" in error


def test_apply_mode_is_used_when_not_provided():
    os.environ['GITLAB_CLIENT_TOKEN'] = 'token'

    gcasc = GitlabConfigurationAsCode()

    assert gcasc.mode == Mode.APPLY
