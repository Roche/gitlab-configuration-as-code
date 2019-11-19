# GitLab Configuration as Code (*GCasC*)

Manage GitLab configuration as code to make it easily manageable, traceable and reproducible.


## Introduction


## Quick start


## Usage


### GitLab Configuration


### Client configuration


### Using Docker image


### Examples


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