import os

import pytest
import yaml

from .helpers import read_yaml, read_file

from gcasc.utils.yaml_include import YamlIncluderConstructor

YamlIncluderConstructor.add_to_loader_class(loader_class=yaml.FullLoader,
                                            base_dir=os.path.dirname(os.path.realpath(__file__)) + '/data')


@pytest.fixture()
def file1():
    return read_yaml('yaml_include_f1.yml')


@pytest.fixture()
def file2():
    return read_yaml('yaml_include_f2.yml')


@pytest.fixture()
def file_txt():
    return read_file('yaml_include_txt.md')


def test_files_included_into_yaml(file1, file2, file_txt):
    # given
    file = 'yaml_include.yml'

    # when
    data = read_yaml(file)

    # then
    assert data['inc1'] == file1
    assert data['inc2'] == [file2, file_txt]
