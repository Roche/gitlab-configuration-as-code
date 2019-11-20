# GitLab Configuration as Code (*GCasC*)

Manage GitLab configuration as code to make it easily manageable, traceable and reproducible.


## Introduction

When configuring your GitLab instance, part of settings you put in [Omnibus](https://docs.gitlab.com/12.4/omnibus/settings/README.html) 
or [Helm Chart](https://docs.gitlab.com/charts/charts/) configuration, and the rest you configure through GitLab UI 
or [API](https://docs.gitlab.com/12.4/ee/api/settings.html). Due to tons of configuration options in UI, making 
you GitLab work as you intend is a complex process.

Our intention is to let you automate things you do through UI in a simple way. The Configuration as Code 
has been designed to configure GitLab based on human-readable declarative configuration files. 
Writing such a file should be feasible without being a GitLab expert, just translating into code a configuration 
process one is used to executing in the web UI.

Configuring your GitLab instance is as simple as this:
```yaml
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


## Usage

| **Environment variable**    | **Description**                                                                                                                  | **Default value**                | **Example**                     |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|---------------------------------|
| `GITLAB_CONFIG_FILE`        | Path to GitLab main configuration. It is our Configuration as Code entry point.                                                  | `./gitlab.yml`                   | `/home/myuser/gitlabconf.yml`   |
| `GITLAB_MODE`               | Determine if any changes, when detected, should be applied. Valid values: `APPLY`, `TEST`                                        | `APPLY`                          | `TEST`                          |
| `GITLAB_CLIENT_API_VERSION` | Version of GitLab API. Current latest: `4`                                                                                       | `4`                              | `4`                             |
| `GITLAB_CLIENT_CONFIG_FILE` | Path to GitLab client configuration                                                                                              | `/etc/gitlab.cfg, ~/.gitlab.cfg` | `/home/myuser/gitlabclient.cfg` |
| `GITLAB_CLIENT_URL`         | URL to GitLab instance. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid.                                        | `https://gitlab.com`             | `https://mygitlab.mydomain.com` |
| `GITLAB_CLIENT_SSL_VERIFY`  | Flag if SSL certificate of GitLab instance should be verified. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid. | `true`                           | `false`                         |
| `GITLAB_CLIENT_TOKEN`       | **Required**. Private token used to access GitLab API. Used only if `GITLAB_CLIENT_CONFIG_FILE` not provided or invalid.         |                                  | `-uub91Jax13P1iaLkC3za0`        |
| `GITLAB_CLIENT_CERT`        | Path to client certificate used for mutual TLS authentication to access GitLab API.                                              |                                  | `/home/myuser/client.crt`       |
| `GITLAB_CLIENT_KEY`         | Path to client key used for mutual TLS authentication to access GitLab API.                                                      |                                  | `/home/myuser/key.pem`          |


### GitLab Configuration

#### Application Settings


GCasC targets 
https://docs.gitlab.com/12.4/ee/api/settings.html

#### License

**Only for Enterprise Edition. FOSS/Community Edition instance will fail when trying to configure license**

GCasC offers a way to manage your GitLab instance licenses. The clue is that despite license is just a single file, 
you need to configure other properties of license so GCasC do not upload new (but already used) license with every 
execution. That way it is able to recognize that exactly the same license is already in use and skips uploading new one.
Otherwise you could end with very long license history.

All license properties are required to be able to configure it. Otherwise GCasC will fail.

| **Property**         | **Description**                                                                      | **Example**             |
|----------------------|--------------------------------------------------------------------------------------|-------------------------|
| `license.starts_at`  | Date in format yyyy-MM-dd when license starts                                        | `2019-11-21`            |
| `license.expires_at` | Date in format yyyy-MM-dd when license ends                                          | `2019-12-21`            |
| `license.plan`       | Plan of your GitLab instance license. Valid values: `starter`, `premium`, `ultimate` | `premium`               |
| `license.user_limit` | Number of licensed users                                                             | `120`                   |
| `license.data`       | Content of your license file that you received from GitLab sales                     | `azhxWFZqb1BsrTVxug...` |

Example license configuration:
```yaml
license:
  starts_at: 2019-11-17
  expires_at: 2019-12-17
  plan: premium
  user_limit: 30
  data: |
    azhxWFZqbk1BOUsrTVxug6AdfzIzWXI1WUVsdWNKRk53V2hiV1FlTUN2TTRS
    NkhSVFFhZ3hCajd4bGlLMkhhcUxhd1EySHh2TjJTXG40U3ZNUWM0ZzhqYTE5
    T1lcbkJnNERFOVBORkpxK3FsaHZxNFFVSG9GL0NEWWF0elkyOE9SUE41Ny9v
    WWo0a3JMQXFN91AcxWpjZmV3b1xuU0NsZmM3UTEzZ3VQMVVhNHJaZ2lVOFgr
    cGNYMFNMU1Y1a0x4UkpNMnhIOWlLZ3NFTzlRYTZIUU4wZlZEXG5Lc0ZrV2Zu
```

**Important!** Beware of storing your license in `data` field directly as text. This is insecure and may lead
to leakage of your license. Use `!env` or `!include` directives to inject license to `license.data` field securely from
external source. Also keep your license file itself safe and secure!

### Client configuration


#### Authentication


### Using _GCasC_ Docker image

#### How to build

```yaml
make docker-build
```
When using make you can additionally pass `DOCKER_IMAGE_NAME` to change default `gcasc:latest` to other image name:
```bash
make docker-build DOCKER_IMAGE_NAME=mygcasc:1.0
```

To get more control over building you can use `docker build` directly:
```bash
docker build -t gcasc[:TAG] .
```

#### How to use

_GCasC_ Docker image working directory is `/workspace`. Thus you can quickly launch `gcasc` with:
```bash
docker run -v $(pwd):/workspace hoffmannlaroche/gcasc
```
It will try to find both GitLab client configuration and GitLab configuration in `/workspace` directory. You can modify
the behavior by passing environment variables as defined in TODO anchor here



Bring your own config file: docker run -it --rm -v /path/to/python-gitlab.cfg:/python-gitlab.cfg -e GITLAB_CFG=/python-gitlab.cfg python-gitlab <command> ...
Docker image can be use
`docker run -v $(pwd):/workspace hoffmannlaroche/gcasc`
`docker run -e GITLAB_CLIENT_CONFIG_FILE=/gitlab/client.cfg -e GITLAB_CONFIG_FILE=/gitlab/config.yml 
-v $(pwd):/gitlab hoffmannlaroche/gcasc`


### Examples

We provide few examples to give you a quick starting place to use _GCasC_. They can be found in [`examples`](examples) directory.
1. [`gitlab.cfg`](examples/gitlab.cfg) is example GitLab client file configuration.
2. [`basic`](examples/basic/gitlab.yml) is example GitLab configuration using single configuration file.
3. [`environment_variables`](examples/environment_variables) shows how environment variables can be injected 
into GitLab configuration file using `!env` directive.
4. [`modularized`](examples/modularized) shows how you can split single GitLab configuration file into smaller 
and inject files containing static text using `!include` directive.

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

## Troubleshooting


## Contribution

Everyone is warm welcome to contribute!

Please make sure to read the [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) 
before making a pull request.

## License

Project is released under [Apache License, Version 2.0 license](LICENSE).