# Changelog

This document contains comprehensive information of the new features, enhancements, 
fixes and other changes of GitLab Configuration as Code.

## [Unreleased]

## [0.6.0] - 2020-11-26

### Added

-   Support for configuring Instance CI/CD Variables

### Changed

-   Validation of resources using JSON Schema
-   Switch CI from Travis to GitHub Actions

### Security

-   Do not log values of any variables, because this may lead to leak of secrets

## [0.5.0] - 2020-04-14

### Added

-   Use `!include` directive with path relative to GitLab configuration file path

## [0.4.0] - 2020-03-12

### Added

-   Support for configuring Feature Flags
-   Support for mixing GitLab client configuration in file and environment variables

## [0.3.1] - 2020-02-06

### Fixed

-   Calculation of key prefixes in `UpdateOnlyConfigurer`

## [0.3.0] - 2020-02-04

### Added

-   Support for configuring Appearance

### Changed

-   Updated dependency on `python-gitlab`
-   Code modularization

## [0.2.0] - 2019-11-28

### Added

-   Documentation available under <https://gitlab-configuration-as-code.readthedocs.io/>

## [0.1.0] - 2019-11-28

### Added

-   Initial release with support for application settings and license

[Unreleased]: https://github.com/Roche/gitlab-configuration-as-code/compare/0.6.0...HEAD

[0.6.0]: https://github.com/Roche/gitlab-configuration-as-code/compare/0.5.0...0.6.0
