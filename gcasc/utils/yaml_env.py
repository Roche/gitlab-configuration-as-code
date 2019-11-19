# -*- coding: utf-8 -*-

import os.path

import yaml

try:
    from yaml import FullLoader
except ImportError:
    FullLoader = None

__all__ = ["YamlEnvConstructor"]


class YamlEnvConstructor:
    DEFAULT_TAG_NAME = "!env"

    def __call__(self, loader, node):
        args = []
        if isinstance(node, yaml.nodes.ScalarNode):
            args = [loader.construct_scalar(node)]
        elif isinstance(node, yaml.nodes.SequenceNode):
            args = loader.construct_sequence(node)
        else:
            raise TypeError("Un-supported YAML node {!r}".format(node))
        return YamlEnvConstructor.load(*args)

    @staticmethod
    def load(env):
        # type: (str)-> str
        splitted = env.split(":", 1)
        value = os.getenv(splitted[0], splitted[1] if splitted.__len__() == 2 else None)
        if value is None:
            raise RuntimeError(
                "Expected {0} environment variable, but value was not found in environment".format(
                    env
                )
            )
        return value

    @classmethod
    def add_to_loader_class(cls, loader_class=None, tag=None, **kwargs):
        # type: (type(yaml.Loader), str, **str)-> YamlEnvConstructor

        if tag is None:
            tag = ""
        tag = tag.strip()
        if not tag:
            tag = cls.DEFAULT_TAG_NAME
        if not tag.startswith("!"):
            raise ValueError('`tag` argument should start with character "!"')
        instance = cls(**kwargs)
        if loader_class is None:
            if FullLoader:
                yaml.add_constructor(tag, instance, FullLoader)
            else:
                yaml.add_constructor(tag, instance)
        else:
            yaml.add_constructor(tag, instance, loader_class)
        return instance
