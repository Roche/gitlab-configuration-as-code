.. _basics:

###########################
Configuration
###########################

.. toctree::
    :maxdepth: 1
    application_settings
    license

About
=====
GitLab configuration is defined

| **Environment variable**    | **Description**                                                                                                                  | **Default value**                | **Example**                     |
|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------|---------------------------------|
| `GITLAB_CONFIG_FILE`        | Path to GitLab main configuration. It is our Configuration as Code entry point.                                                  | `./gitlab.yml`                   | `/home/myuser/gitlabconf.yml`   |
| `GITLAB_MODE`               | Determine if any changes, when detected, should be applied. Valid values: `APPLY`, `TEST`                                        | `APPLY`                          | `TEST`                          |


Yaml directives
===============

`!include`
----------


`!env`
----------

