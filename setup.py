#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as reqs_file:
    requirements = reqs_file.readlines()

with open("test-requirements.txt", "r") as test_reqs_file:
    test_requirements = test_reqs_file.readlines()

setup(
    name="gitlab-configuration-as-code",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description="Manage GitLab configuration as code",
    long_description_content_type='text/markdown',
    long_description=readme,
    author="Mateusz Filipowicz",
    author_email="mateusz.filipowicz@roche.com",
    license="Apache-2.0",
    url="https://github.com/Roche/gitlab-configuration-as-code",
    keywords=['gitlab', 'configuration-as-code'],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=test_requirements,
    entry_points={"console_scripts": ["gcasc = gcasc.bin.gcasc:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
