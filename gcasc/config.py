import os

import yaml

from gcasc.utils import os as uos
from gcasc.utils.yaml_include import YamlIncluderConstructor
from gcasc.utils.yaml_env import YamlEnvConstructor

# includer relative to current path from which script is executed
YamlIncluderConstructor.add_to_loader_class(
    loader_class=yaml.FullLoader, base_dir=os.path.dirname(os.path.realpath(__file__))
)

# includer relative to GitLab configuration file path
config_path = uos.get_env_or_else(
    ["GITLAB_CONFIG_FILE", "GITLAB_CONFIG_PATH"], "{0}/x".format(os.getcwd())
).split("/")
del config_path[-1]
YamlIncluderConstructor.add_to_loader_class(
    loader_class=yaml.FullLoader, base_dir="/".join(config_path)
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

    def get(self, configuration):
        return self.config.get(configuration)

    @staticmethod
    def from_file(path):
        # type: (str)->GitlabConfiguration
        with open(path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return GitlabConfiguration(data)
