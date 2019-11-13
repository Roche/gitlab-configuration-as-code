from pathlib import Path

import gitlab
import requests

import utils.os as uos

from .settings import *
from .config import *


GITLAB_CLIENT_CONFIG_FILE = ['GITLAB_CLIENT_CONFIG', 'GITLAB_CLIENT_CONFIG_FILE']
GITLAB_CLIENT_CERTIFICATE = ['GITLAB_CLIENT_CERT', 'GITLAB_CLIENT_CERTIFICATE']
GITLAB_CLIENT_KEY = 'GITLAB_CLIENT_KEY'
GITLAB_CLIENT_URL = 'GITLAB_CLIENT_URL'
GITLAB_CLIENT_API_VERSION = 'GITLAB_CLIENT_API_VERSION'
GITLAB_CLIENT_TOKEN = 'GITLAB_CLIENT_TOKEN'
GITLAB_CLIENT_SSL_VERIFY = 'GITLAB_CLIENT_SSL_VERIFY'
GITLAB_CONFIG_FILE = ['GITLAB_CONFIG_FILE', 'GITLAB_CONFIG_PATH']

GITLAB_CONFIG_FILE_DEFAULT_PATHS = ['/etc/python-gitlab.cfg', '/etc/gitlab.cfg', '~/.python-gitlab.cfg',
                                    '~/.gitlab.cfg']

logging.basicConfig(format='[%(levelname)s] [%(name)s] %(message)s', level=logging.DEBUG)

class GitlabConfigurationAsCode(object):

    def __init__(self):
        self.gitlab = init_gitlab_client()
        self.configurers = {}
        path = uos.get_env_or_else(GITLAB_CONFIG_FILE, "gitlab.yml")
        self.config = GitlabConfiguration.from_file(path)
        self.configurers['settings'] = SettingsConfigurer(self.gitlab, self.config.settings)

    @property
    def settings(self):
        return self.configurers['settings']

    def configure(self, target=None):
        if target is None:
            for name, configurer in self.configurers.items():
                configurer.configure()


def init_gitlab_from_env():
    token = uos.get_env_or_else(GITLAB_CLIENT_TOKEN)
    if token is None:
        raise ClientInitializationError(
            "GitLab token was not provided. It must be defined in {0} environment variable".format(GITLAB_CLIENT_TOKEN))

    url = uos.get_env_or_else(GITLAB_CLIENT_URL, "https://gitlab.com")
    ssl_verify = uos.get_env_or_else(GITLAB_CLIENT_SSL_VERIFY, True)
    api_version = uos.get_env_or_else(GITLAB_CLIENT_API_VERSION, "4")

    return gitlab.Gitlab(url=url, private_token=token, ssl_verify=ssl_verify, api_version=api_version)


def init_gitlab_from_config_file():
    config_path = __find_gitlab_connection_config_file()
    if config_path is None:
        raise ClientInitializationError("")
    return gitlab.Gitlab.from_config("global", [config_path])


def init_gitlab_client():
    print("Initializing GitLab client")
    try:
        print("Trying to initialize GitLab client from configuration file...")
        client = init_gitlab_from_config_file()
    except ClientInitializationError:
        print("Trying to initialize GitLab client from environment variables...")
        client = init_gitlab_from_env()
    if client is None:
        raise ClientInitializationError("Unable to initialize GitLab client due to missing configuration either in "
                                        "config file or environment vars")

    __init_session(client)
    return client


def __find_gitlab_connection_config_file():
    config_path = uos.get_env_or_else(GITLAB_CLIENT_CONFIG_FILE)
    if config_path is not None:
        try:
            __check_file_exists(config_path, "GitLab Client")
        except FileNotFoundError:
            raise ClientInitializationError(
                "Configuration file was not found under path {0}, which was defined in {1} env variable."
                "Provide path to existing file or remove this variable and configure client"
                "using environment variables instead of configuration file".format(config_path))
    else:
        for path in GITLAB_CONFIG_FILE_DEFAULT_PATHS:
            try:
                __check_file_exists(path, "GitLab Client")
                config_path = path
                break
            except FileNotFoundError:
                pass
    return config_path


def __check_file_exists(path, file_context=""):
    config = Path(path)
    if not config.exists():
        raise FileNotFoundError(
            "[{0}] File under '" + path + "' does not exist. Provide valid path.".format(file_context))

    if config.is_dir():
        raise FileNotFoundError(
            "[{0}] Directory was found under '" + path + "' instead of file. Provide valid path to file.".format(
                file_context))


def __init_session(gitlab):
    certificate = uos.get_env_or_else(GITLAB_CLIENT_CERTIFICATE)
    key = uos.get_env_or_else(GITLAB_CLIENT_KEY)
    if certificate is None and key is None:
        return
    elif certificate is None and key is not None:
        pass
    elif certificate is not None and key is None:
        pass
    else:
        __check_file_exists(certificate, "Client Certificate")
        __check_file_exists(key, "Client Key")
        session = requests.Session()
        session.cert = (certificate, key)
        gitlab.session = session


class ClientInitializationError(Exception):
    pass
