import os

import yaml
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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


def read_yaml_from_string(str):
    return yaml.load(StringIO(str), Loader=yaml.FullLoader)
