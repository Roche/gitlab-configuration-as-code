import yaml

from gcasc.utils.yaml_env import YamlEnvConstructor

yaml.add_constructor(
    u"tag:yaml.org,2002:timestamp", lambda self, node: self.construct_scalar(node)
)
YamlEnvConstructor.add_to_loader_class(loader_class=yaml.FullLoader)
