import os
from pathlib import Path

import gitlab
import requests

import gcasc.utils.os as uos
from .utils import logger as logging

from .base import Mode
from .appearance import AppearanceConfigurer
from .license import LicenseConfigurer
from .settings import SettingsConfigurer
from .config import GitlabConfiguration

GITLAB_CLIENT_CONFIG_FILE = ["GITLAB_CLIENT_CONFIG", "GITLAB_CLIENT_CONFIG_FILE"]
GITLAB_CLIENT_CERTIFICATE = ["GITLAB_CLIENT_CERT", "GITLAB_CLIENT_CERTIFICATE"]
GITLAB_CLIENT_KEY = "GITLAB_CLIENT_KEY"
GITLAB_CLIENT_URL = "GITLAB_CLIENT_URL"
GITLAB_CLIENT_API_VERSION = "GITLAB_CLIENT_API_VERSION"
GITLAB_CLIENT_TOKEN = "GITLAB_CLIENT_TOKEN"
GITLAB_CLIENT_SSL_VERIFY = "GITLAB_CLIENT_SSL_VERIFY"
GITLAB_CONFIG_FILE = ["GITLAB_CONFIG_FILE", "GITLAB_CONFIG_PATH"]

GITLAB_CONFIG_FILE_DEFAULT_PATHS = [
    "/etc/python-gitlab.cfg",
    "/etc/gitlab.cfg",
    "~/.python-gitlab.cfg",
    "~/.gitlab.cfg",
]

GITLAB_MODE = "GITLAB_MODE"

logger = logging.get_logger()


class GitlabConfigurationAsCode(object):
    def __init__(self):
        # type: ()->GitlabConfigurationAsCode
        self.mode = Mode[uos.get_env_or_else(GITLAB_MODE, Mode.APPLY.name)]
        if self.mode == Mode.TEST:
            logger.info("TEST MODE ENABLED. NO CHANGES WILL BE APPLIED")
        path = uos.get_env_or_else(
            GITLAB_CONFIG_FILE, "{0}/gitlab.yml".format(os.getcwd())
        )
        self.gitlab = init_gitlab_client()
        self.configurers = {}
        self.config = GitlabConfiguration.from_file(path)
        self.configurers["settings"] = SettingsConfigurer(
            self.gitlab, self.config.settings, self.mode
        )
        self.configurers["license"] = LicenseConfigurer(
            self.gitlab, self.config.license, self.mode
        )
        self.configurers["appearance"] = AppearanceConfigurer(
            self.gitlab, self.config.appearance, self.mode
        )

        version, revision = self.gitlab.version()
        logger.info("GitLab version: %s, revision: %s", version, revision)

    @property
    def settings(self):
        # type: ()->SettingsConfigurer
        return self.configurers["settings"]

    @property
    def license(self):
        # type: ()->LicenseConfigurer
        return self.configurers["license"]

    @property
    def appearance(self):
        # type: ()->AppearanceConfigurer
        return self.configurers["appearance"]

    def configure(self, target=None):
        if target is None:
            for name, configurer in self.configurers.items():
                if configurer.config is None:
                    logger.info(
                        "Skipping configurer %s because it does not have any configuration to apply",
                        configurer.__class__.__name__,
                    )
                    continue
                configurer.configure()


def init_gitlab():
    # type: ()->gitlab.Gitlab
    config_path = __find_gitlab_connection_config_file()
    config = gitlab.config.GitlabConfigParser(
        gitlab_id=gitlab_id, config_files=[config_path]
    ) if config_path is not None else None

    token = getattr(config, 'private_token', uos.get_env_or_else(GITLAB_CLIENT_TOKEN))
    if token is None:
        raise ClientInitializationError(
            "GitLab token was not provided. It must be defined in {0} environment variable".format(
                GITLAB_CLIENT_TOKEN
            )
        )

    url = getattr(config, 'url', uos.get_env_or_else(GITLAB_CLIENT_URL, "https://gitlab.com"))
    ssl_verify = getattr(config, 'ssl_verify', uos.get_env_or_else(GITLAB_CLIENT_SSL_VERIFY, True))
    api_version = getattr(config, 'api_version', uos.get_env_or_else(GITLAB_CLIENT_API_VERSION, "4"))

    return gitlab.Gitlab(
        url=url, private_token=token, ssl_verify=ssl_verify, api_version=api_version
    )

def init_gitlab_client():
    # type: ()->gitlab.Gitlab
    logger.info("Initializing GitLab client")
    logger.info("Trying to initialize GitLab client...")
    client = init_gitlab()

    if client is None:
        raise ClientInitializationError(
            "Unable to initialize GitLab client due to missing configuration either in "
            "config file or environment vars"
        )

    __init_session(client)
    return client


def __find_gitlab_connection_config_file():
    # type: ()->str
    config_path = uos.get_env_or_else(GITLAB_CLIENT_CONFIG_FILE)
    if config_path is not None:
        if not __check_file_exists(config_path, "GitLab Client"):
            logger.error(
                "Configuration file was not found under path %s, which was defined in %s env variable."
                "Provide path to existing file or remove this variable and configure client"
                "using environment variables instead of configuration file",
                config_path,
                GITLAB_CLIENT_CONFIG_FILE,
            )
            return None
    else:
        for path in GITLAB_CONFIG_FILE_DEFAULT_PATHS:
            if __check_file_exists(path, "GitLab Client"):
                config_path = path
                break
    return config_path


def __check_file_exists(path, file_context=""):
    # type: (str, str)->bool
    config = Path(path)
    if not config.exists():
        logger.error(
            "[%s] File under %a does not exist. Provide valid path.", file_context, path
        )
        return False

    if config.is_dir():
        logger.error(
            "[%s] Directory was found under %s instead of file. Provide valid path to file.",
            file_context,
            path,
        )
        return False
    return True


def __init_session(gitlab):
    # type: (gitlab.Gitlab)->()
    certificate = uos.get_env_or_else(GITLAB_CLIENT_CERTIFICATE)
    key = uos.get_env_or_else(GITLAB_CLIENT_KEY)
    if certificate is None and key is None:
        return
    elif certificate is None and key is not None:
        pass
    elif certificate is not None and key is None:
        pass
    else:
        check_config = __check_file_exists(
            certificate, "Client Certificate"
        ) and __check_file_exists(key, "Client Key")
        if not check_config:
            raise ClientInitializationError(
                "GitLab client authentication env vars were provided, but point to incorrect file(s)"
            )
        session = requests.Session()
        session.cert = (certificate, key)
        gitlab.session = session


class ClientInitializationError(Exception):
    pass
