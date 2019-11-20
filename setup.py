#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup


with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r") as reqs_file:
    requirements = reqs_file.readlines()

setup(
    name="gitlab-configuration-as-code",
    version="0.1",
    description="Manage GitLab configuration as code",
    long_description=readme,
    author="Mateusz Filipowicz",
    author_email="mateusz.filipowicz@roche.com",
    license="Apache-2.0",
    url="https://github.com/Roche/gitlab-configuration-as-code",
    keywords=['gitlab', 'configuration-as-code'],
    packages=find_packages(),
    install_requires=requirements,
    entry_points={"console_scripts": ["gitlab = bin.gcasc:main"]},
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
