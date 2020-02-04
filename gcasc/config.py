import os

import yaml
from gcasc.utils.yaml_include import YamlIncluderConstructor
from gcasc.utils.yaml_env import YamlEnvConstructor

YamlIncluderConstructor.add_to_loader_class(
    loader_class=yaml.FullLoader, base_dir=os.path.dirname(os.path.realpath(__file__))
)

YamlEnvConstructor.add_to_loader_class(loader_class=yaml.FullLoader)


class GitlabConfiguration(object):
    def __init__(self, config):
        # type: (dict)->GitlabConfiguration
        if config is None:
            raise RuntimeError("GitLab configuration is empty")

        if not isinstance(config, dict):
            raise RuntimeError("Configuration provided must be of dictionary type")

        self.config = config

    def __get(self, configuration):
        return self.config.get(configuration)

    @property
    def settings(self):
        # type: ()->dict
        return self.__get("settings")

    @property
    def license(self):
        # type: ()->dict
        return self.__get("license")

    @property
    def appearance(self):
        # type: ()->dict
        return self.__get("appearance")

    @staticmethod
    def from_file(path):
        # type: (str)->GitlabConfiguration
        with open(path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return GitlabConfiguration(data)
