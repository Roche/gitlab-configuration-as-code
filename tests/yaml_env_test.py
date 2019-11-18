import os

import pytest
import yaml

from .helpers import read_yaml
from gcasc.utils.yaml_env import YamlEnvConstructor

YamlEnvConstructor.add_to_loader_class(loader_class=yaml.FullLoader)

ENV1_VAL = 'envvar1'
ENV2_VAL = 'envvar2\nmultiline\ttabbed'


@pytest.fixture(autouse=True)
def prepare_environment():
    # before
    os.environ['ENV1'] = ENV1_VAL
    os.environ['ENV2'] = ENV2_VAL
    # test
    yield
    # after
    os.unsetenv('ENV1')
    os.unsetenv('ENV2')


def test_environment_injected_into_yaml():
    # given
    file = 'yaml_env.yml'

    # when
    data = read_yaml(file)

    # then
    assert data['env1'] == ENV1_VAL
    assert data['env_list'] == [ENV1_VAL, 'someval', ENV2_VAL]
