.PHONY: help clean-pyc clean-build isort lint test build docker-build docker-push docs

ENV=py37
DOCKER_IMAGE_NAME=gcasc

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
	@echo "   build"
	@echo '        Build `gcasc` Python package.'
	@echo "   publish"
	@echo '        Publish `gcasc` Python package.'
	@echo "   docker-build"
	@echo '        Build `gcasc` Docker image.'
	@echo "   docker-push"
	@echo '        Publish `gcasc` Docker image.'

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name 'out_report.xml' -exec rm -f {} +
	rm -rf htmlcov .coverage .pytest-cache .tox

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

install-run-deps:
	pip3 install --user -r requirements.txt

install-test-deps:
	pip3 install --user -r test-requirements.txt

install-deps: install-run-deps install-test-deps

clean: clean-pyc clean-build

isort:
	sh -c "isort --skip-glob=.tox --recursive . "

lint:
	tox -e flake -e black

test: clean-pyc
	@echo "Running tests on environment: " $(ENV)
	tox -e $(ENV)

docs: clean-build
	@echo "Building documentation..."
	pip3 install -r requirements.txt
	mkdir -p build/docs
	cd docs && $(MAKE) html && mv _build/html/* ../build/docs
	@echo "Documentation is available in build/docs directory"

build: clean-build docs
	@echo "Building source and binary Wheel distributions..."
	pip3 install -r requirements.txt
	pip3 install wheel
	python3 setup.py sdist bdist_wheel

publish: build
ifeq ($(strip $(TWINE_USERNAME)),)
	@echo "TWINE_USERNAME variable must be provided"
	exit -1
endif
ifeq ($(strip $(TWINE_PASSWORD)),)
	@echo "TWINE_PASSWORD variable must be provided"
	exit -1
endif
	@echo "Publishing library to PyPi"
	pip3 install --user twine
	twine upload dist/*
	@echo "Library published"

docker-build:
	docker build \
	  --file=./Dockerfile \
	  --tag=$(DOCKER_IMAGE_NAME) ./

docker-push: docker-build
ifeq ($(strip $(DOCKER_USERNAME)),)
	@echo "DOCKER_USERNAME variable must be provided"
	exit -1
endif
ifeq ($(strip $(DOCKER_PASSWORD)),)
	@echo "DOCKER_PASSWORD variable must be provided"
	exit -1
endif
	docker login -u $(DOCKER_USERNAME) -p $(DOCKER_PASSWORD)
	docker push $(DOCKER_IMAGE_NAME)
