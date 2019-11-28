.. GitLab Configuration as Code documentation master file, created by
   sphinx-quickstart on Thu Nov 21 06:49:44 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to GitLab Configuration as Code's documentation!
========================================================

.. image:: https://travis-ci.org/Roche/gitlab-configuration-as-code.svg?branch=master
   :target: https://travis-ci.org/Roche/gitlab-configuration-as-code
   :alt: Build Status
.. image:: https://img.shields.io/docker/pulls/hoffmannlaroche/gcasc
   :target: https://hub.docker.com/r/hoffmannlaroche/gcasc
   :alt: Docker Pull count
.. image:: https://img.shields.io/pypi/v/gitlab-configuration-as-code
   :target: https://pypi.org/project/gitlab-configuration-as-code
   :alt: PyPI
.. image:: https://img.shields.io/badge/license-Apache%202.0-blue
   :alt: License

When configuring your GitLab instance, part of the settings you put in Omnibus_ or `Helm Chart`__ configuration,
and the rest you configure through GitLab UI or API_. Due to tons of configuration options in UI, making GitLab work
as you intend is a complex process.

We intend to let you automate things you do through now UI in a simple way. The Configuration as Code
has been designed to configure GitLab based on human-readable declarative configuration files written in Yaml.
Writing such a file should be feasible without being a GitLab expert, just translating into code a configuration
process one is used to executing in the web UI.

.. _Omnibus: https://docs.gitlab.com/12.4/omnibus/settings/README.html
.. _Helm: https://docs.gitlab.com/charts/charts/
.. _API: https://docs.gitlab.com/12.4/ee/api/settings.html
__ Helm_

Contents:
---------
.. toctree::
   :maxdepth: 2

   install
   usage
   client
   configuration/index
   faq
..   release_notes
..   changelog
