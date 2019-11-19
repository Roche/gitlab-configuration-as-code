.PHONY: help clean-pyc clean-build isort lint test docker-build

TEST_PATH=./tests

help:
	@echo "make"
	@echo "   clean-pyc"
	@echo "       Remove python artifacts."
	@echo "   clean-build"
	@echo "        Remove build artifacts."
	@echo "   isort"
	@echo "        Sort import statements."
	@echo "   lint"
	@echo "        Check style with flake8."
	@echo "   test"
	@echo "        Run tests and produce report in test/out_report.xml"
	@echo "   docker-build"
	@echo '        Build the `gcasc` Docker image.'

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name 'out_report.xml' -exec rm -f {} +
	rm -rf htmlcov .coverage .pytest-cache .tox

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean: clean-pyc clean-build

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	tox -e flake -e black

test: clean-pyc
	tox -e py37

build: clean-build
	python setup.py bdist_egg

docker-build:
	docker build \
	  --file=./Dockerfile \
	  --tag=gcasc ./