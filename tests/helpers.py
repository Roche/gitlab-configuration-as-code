import os

import yaml


def __context():
    dir = os.getcwd()
    if dir.endswith('tests'):
        return dir
    return '{0}/tests'.format(dir)


CONTEXT = __context()


def read_file(file):
    with open('{0}/data/{1}'.format(CONTEXT, file)) as f:
        data = f.read()
    return data


def read_yaml(file):
    with open('{0}/data/{1}'.format(CONTEXT, file)) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data
