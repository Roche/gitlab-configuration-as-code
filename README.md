[![Build Status](https://travis-ci.org/Roche/gitlab-configuration-as-code.svg?branch=master)](https://travis-ci.org/Roche/gitlab-configuration-as-code)
[![Docker Pull count](https://img.shields.io/docker/pulls/hoffmannlaroche/gcasc)](https://hub.docker.com/r/hoffmannlaroche/gcasc)
[![PyPI](https://img.shields.io/pypi/v/gitlab-configuration-as-code)](https://pypi.org/project/gitlab-configuration-as-code)
[![Documentation Status](https://readthedocs.org/projects/gitlab-configuration-as-code/badge/?version=latest)](https://gitlab-configuration-as-code.readthedocs.io/en/latest/?badge=latest)
[![Last Commit](https://img.shields.io/github/last-commit/Roche/gitlab-configuration-as-code)]()
[![Python versions](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)]()
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

# GitLab Configuration as Code (*GCasC*)

Manage GitLab configuration as code to make it easily manageable, traceable and reproducible.

### Table of Contents

* [Introduction](#introduction)
* [Quick start](#quick-start)
   * [Configure client](#configure-client)
   * [Prepare GitLab configuration](#prepare-gitlab-configuration)
   * [Run GCasC](#run-gcasc)
       * [CLI](#cli)
       * [Docker image](#docker-image)
   * [Examples](#examples)
* [Building](#building)
   * [Docker image](#docker-image-1)
   * [Python package](#python-package)
* [Testing](#testing)
* [Contribution](#contribution)
* [License](#license)

## Introduction

When configuring your GitLab instance, part of the settings you put in [Omnibus](https://docs.gitlab.com/12.7/omnibus/settings/README.html)
or [Helm Chart](https://docs.gitlab.com/charts/charts/) configuration, and the rest you configure through GitLab UI
or [API](https://docs.gitlab.com/12.7/ee/api/settings.html). Due to tons of configuration options in UI,
making GitLab work as you intend is a complex process.

We intend to let you automate things you do through now UI in a simple way. The Configuration as Code
has been designed to configure GitLab based on human-readable declarative configuration files written in Yaml.
Writing such a file should be feasible without being a GitLab expert, just translating into code a configuration
process one is used to executing in the web UI.

_GCasC_ offers a functionality to configure:
* [appearance](https://gitlab-configuration-as-code.readthedocs.io/en/latest/configuration/appearance.html)
* [application settings](https://gitlab-configuration-as-code.readthedocs.io/en/latest/configuration/application_settings.html)
* [features](https://gitlab-configuration-as-code.readthedocs.io/en/latest/configuration/features.html)
* [license](https://gitlab-configuration-as-code.readthedocs.io/en/latest/configuration/license.html)
* ... more coming soon!

It gives you also a way to:
* include external files or other Yamls using `!include` directive
* inject environment variables into configuration using `!env` directive
into your Yaml configuration.
 
Visit [our documentation site](https://gitlab-configuration-as-code.readthedocs.io/) for detailed information on how to use it.

Configuring your GitLab instance is as simple as this:
```yaml
appearance:
  title: "Your GitLab instance title"
  logo: "http://path-to-your-logo/logo.png"

settings:
  elasticsearch:
    url: http://elasticsearch.mygitlab.com
    username: !env ELASTICSEARCH_USERNAME
    password: !env ELASTICSEARCH_PASSWORD
  recaptcha_enabled: yes
  terms: '# Terms of Service\n\n *GitLab rocks*!!'
  plantuml:
    enabled: true
    url: 'http://plantuml.url'

features:
  - name: sourcegraph
    value: true
    canaries:
      - group: mygroup
      - project: mygroup1/myproject

license:
  starts_at: 2019-11-17
  expires_at: 2019-12-17
  plan: premium
  user_limit: 30
  data: !include gitlab.lic
```

**Note:** GCasC supports only Python 3+. Because Python 2.7 end of life is January 1st, 2020 we do not consider support
for Python 2.

## Quick start

Here you will learn how to quickly start with _GCasC_.

**Important!** Any execution of _GCasC_ may override properties you define in your Yaml files. Don't try it directly
on your production environment.

Visit [our documentation site](https://gitlab-configuration-as-code.readthedocs.io/) for detailed information on how to use it.

### Configure client

You can configure client in two ways:

* using configuration file:
    ```
    [global]
    url = https://gitlab.yourdomain.com
    ssl_verify = true
    timeout = 5
    private_token = <personal_access_token>
    api_version = 4
    ```
    By default _GCasC_ is trying to find client configuration file in following paths:
    ```
    "/etc/python-gitlab.cfg",
    "/etc/gitlab.cfg",
    "~/.python-gitlab.cfg",
    "~/.gitlab.cfg",
    ```
 
    You can provide a path to your configuration file in `GITLAB_CLIENT_CONFIG_FILE` environment variable.

* using environment variables:
    ```bash
    GITLAB_CLIENT_URL=<gitlab_url> # path to GitLab, default: https://gitlab.com
    GITLAB_CLIENT_API_VERSION=<gitlab_api_version> # GitLab API version, default: 4
    GITLAB_CLIENT_TOKEN=<personal_access_token> # GitLab personal access token
    GITLAB_CLIENT_SSL_VERIFY=<ssl_verify> # Flag if SSL certificate should be verified, default: true
    ```

You can combine both methods and configuration settings will be searched in the following order:

* configuration file
* environment variables (due to limitations in `python-gitlab` if using configuration file only `GITLAB_CLIENT_TOKEN`
  environment variable will be used)

Personal access token is mandatory in any client configuration approach and you can configure your it by following
[these instructions](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

Additionally you can customize HTTP session to enable mutual TLS authentication. To configure this, you should
provide two additional environment variables:
```bash
GITLAB_CLIENT_CONFIG_FILE=<path_to_client_certificate>
GITLAB_CLIENT_KEY=<path_to_client_key>
```

### Prepare GitLab configuration

GitLab configuration must be defined in Yaml file. You can provide a configuration in a single file, or you can
split it into multiple Yaml files and inject them.

For information how to prepare GitLab configuration Yaml file visit
[our documentation site](https://gitlab-configuration-as-code.readthedocs.io/en/latest/configuration).

For `settings` configuration, which defines [Application Settings](https://docs.gitlab.com/12.7/ee/api/settings.html),
the structure is flexible. For example

```yaml
settings:
  elasticsearch:
    url: http://elasticsearch.mygitlab.com
    username: elastic_user
    password: elastic_password
```

and
 
```yaml
settings:
  elasticsearch_url: http://elasticsearch.mygitlab.com
  elasticsearch_username: elastic_user
  elasticsearch_password: elastic_password
```
are exactly the same and match `elasticsearch_url`, `elasticsearch_username` and `elasticsearch_password` settings.
This means you can flexibly structure your configuration Yaml, where a map child keys are prefixed by parent key (here
`elasticsearch` parent key was a prefix for `url`, `username` and `password` keys). You only need to follow available
[Application Settings](https://docs.gitlab.com/12.7/ee/api/settings.html).

You can adjust your Yamls by splitting them into multiple or injecting environment variables into certain values using
`!include` or `!env` directives respectively. Example is shown below:

```yaml
settings:
  elasticsearch:
    url: http://elasticsearch.mygitlab.com
    username: !env ELASTICSEARCH_USERNAME
    password: !env ELASTICSEARCH_PASSWORD
  terms: !include tos.md

license: !include license.yml
```

where:

* `settings.elasticsearch.username` and `settings.elasticsearch.password` are injected from environment variables
`ELASTICSEARCH_USERNAME` and `ELASTICSEARCH_PASSWORD` respectively

* `settings.terms` and `license` are injected from `tos.md` plain text file and `license.yml` Yaml file respectively.
In this scenario, your `license.yml` may look like this:
```yaml
starts_at: 2019-11-17
expires_at: 2019-12-17
plan: premium
user_limit: 30
data: !include gitlab.lic
```

### Run GCasC

To run _GCasC_ you can leverage CLI or Docker image. _Docker image is a preferred way_, because it is simple
and does not require from you installing any additional libraries. Also, Docker image was designed that it can be
easily used in your CI/CD pipelines.

When running locally, you may benefit from running _GCasC_ in TEST mode (default mode is `APPLY`), where no changes
will be applied, but validation will be performed and differences will be logged. Just set `GITLAB_MODE`
environment variable to `TEST`.
```bash
export GITLAB_MODE=TEST
```

#### CLI

_GCasC_ library is available in [PyPI](https://pypi.org/project/gitlab-configuration-as-code/).

To install CLI run `pip install gitlab-configuration-as-code`. Then you can simply execute
```bash
gcasc
```

//TODO add more information on CLI usage

Currently, CLI is limited and does not support passing any arguments to it, but behavior can only be configured
using environment variables. Support for CLI arguments may appear in future releases.

#### Docker image

Image is available in [Docker Hub](https://hub.docker.com/r/hoffmannlaroche/gcasc).

_GCasC_ Docker image working directory is `/workspace`. Thus you can quickly launch `gcasc` with:
```bash
docker run -v $(pwd):/workspace hoffmannlaroche/gcasc
```
It will try to find both GitLab client configuration and GitLab configuration in `/workspace` directory. You can modify
the behavior by passing environment variables:
* `GITLAB_CLIENT_CONFIG_FILE` to provide path to GitLab client configuration file
* `GITLAB_CONFIG_FILE` to provide a path to GitLab configuration file

```bash
docker run -e GITLAB_CLIENT_CONFIG_FILE=/gitlab/client.cfg -e GITLAB_CONFIG_FILE=/gitlab/config.yml
-v $(pwd):/gitlab hoffmannlaroche/gcasc
```

You can also configure a GitLab client using environment variables. More details about the configuration of GitLab client
are available [in this documentation](https://gitlab-configuration-as-code.readthedocs.io/en/latest/client.html).

### Examples

We provide a few examples to give you a quick starting place to use _GCasC_. They can be found in [`examples`](examples) directory.
1. [`gitlab.cfg`](examples/gitlab.cfg) is example GitLab client file configuration.
2. [`basic`](examples/basic/gitlab.yml) is an example GitLab configuration using a single configuration file.
3. [`environment_variables`](examples/environment_variables) shows how environment variables can be injected
into GitLab configuration file using `!env` directive.
4. [`modularized`](examples/modularized) shows how you can split single GitLab configuration file into smaller
and inject files containing static text using `!include` directive.

## Building

### Docker image

Use `make` to build a basic Docker image quickly.
```bash
make docker-build
```
When using `make` you can additionally pass `DOCKER_IMAGE_NAME` to change default `gcasc:latest` to another image name:
```bash
make docker-build DOCKER_IMAGE_NAME=mygcasc:1.0
```

To get more control over builds you can use `docker build` directly:
```bash
docker builds -t gcasc[:TAG] .
```

Dockerfile comes with two build arguments you may use to customize your image by providing `--build-arg` parameter
to `docker build` command:
* `GCASC_PATH` defines the path where _GCasC_ library will be copied. Defaults to `/opt/gcasc`.
* `WORKSPACE` defines a working directory when you run _GCasC_ image. Defaults to `/workspace`.

### Python package

Use `make` to build source distribution (sdist), Wheel binary distribution and Sphinx documentation.
```bash
make build
```
Both source and Wheel distributions will be placed in `dist` directory. Documentation page will be placed
in `build/docs` directory.

Remember to run tests before building your distribution!

## Testing

Before submitting a pull request make sure that the tests still succeed with your change.
Unit tests run using Github Actions and passing tests are mandatory
to get merge requests accepted.

You need to install `tox` to run unit tests locally:

```bash
# run the unit tests for python 3, python 2, and the flake8 tests:
tox

# run tests in one environment only:
tox -e py37

# run flake8 linter and black code formatter
tox -e flake

# run black code formatter
tox -e black
```

Instead of using `tox` directly, it is recommended to use `make`:
```bash
# run tests
make test

# run flake8 linter and black code formatter
make lint
```

## Contribution

Everyone is warm welcome to contribute!

Please make sure to read the [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md)
before making a pull request.

## License

Project is released under [Apache License, Version 2.0 license](LICENSE).
