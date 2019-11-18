# GitLab Configuration as Code (*GCasC*)

Manage GitLab configuration as code to make it easily manageable and reproducible.


## Introduction


## Quick start


## Usage


### GitLab Configuration


### Client configuration


### Using Docker image


### Examples


## Contributing

### Code style

We use black as code formatter, so you'll need to format your changes using 
the [black code formatter](https://github.com/python/black).

Just run:
```bash
cd python-gitlab/
pip3 install --user tox
tox -e black
```
to format your code according to our guidelines ([tox](https://tox.readthedocs.io/en/latest/) is required).

Additionally, `flake8` linter is used to verify code style. It must succeeded
in order to make pull request approved.

Just run:
```bash
cd python-gitlab/
pip3 install --user tox
tox -e flake
```
to verify code style according to our guidelines (`tox` is required).

### Testing

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
