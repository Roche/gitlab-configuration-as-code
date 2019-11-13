import os

import yaml
from utils.yaml_include import YamlIncluderConstructor
from utils.yaml_env import YamlEnvConstructor

YamlIncluderConstructor.add_to_loader_class(
    loader_class=yaml.FullLoader,
    base_dir=os.path.dirname(os.path.realpath(__file__)))

YamlEnvConstructor.add_to_loader_class(loader_class=yaml.FullLoader)


class GitlabConfiguration(object):

    def __init__(self, config):
        # type: (dict)->GitlabConfiguration
        if config is None:
            raise RuntimeError("GitLab configuration is empty")

        if not isinstance(config, dict):
            raise RuntimeError("Configuration provided must be of dictionary type")

        self.config = config

    @property
    def settings(self):
        # type: ()->dict
        return self.config['settings']

    @staticmethod
    def from_file(path):
        # type: (str)->GitlabConfiguration
        with open(path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return GitlabConfiguration(data)
