# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

<!--

Unreleased

## {version_tag} - YYYY-DD-mm

### Added

### Changed

### Removed

-->

## 0.11.0 - 2022-11-16

- Add new job to manage custom splash screen
- Fix: job shortcut-manager was failing when icon is not defined
- Bump dependencies

## 0.10.0 - 2022-05-25

- Minor bug fixes
- Extends unit tests (65%)

## 0.9.0 - 2022-05-18

- handle `~` char in scenario files to represent the end-user home folder
- add [`utils.str2bool`](https://guts.github.io/qgis-deployment-cli/_apidoc/qgis_deployment_toolbelt.utils.str2bool.html) to convert `str` to `bool`. Useful to process environment variables which are always stored/retrieved as strings.
- add [`utils.win32utils.get_environment_variable`](https://guts.github.io/qgis-deployment-cli/_apidoc/qgis_deployment_toolbelt.utils.win32utils.html) to retrieve environment variable directly from Windows registry, because `os.getenv` uses the configuration at the run moment
- Documentation: add an auto-generated table of dependencies and their license within the [Credits page](https://guts.github.io/qgis-deployment-cli/misc/credits.html)
- Fix a bug when the icon path was not set for a shortcut
- Extend unit tests to reach 60% of coverage

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.9.0).

## 0.8.0 - 2022-05-16

- Pin dulwich version to avoid recurring connection errors
- Add support for environment variable `QGIS_CUSTOM_CONFIG_PATH`
- Make clone/pull more robust
- Extend unit tests

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.8.0).

## 0.7.0 - 2022-05-16

- Add module to create and delete application shortcuts
- Add job to use the new module to automatically create shortcuts for QGIS profiles
- Promote constants module to a dataclass (Python 3.7+)
- Remove subcommand to set environment variables
- Rename `environment_variables` section to `settings` in scenario files
- Handle situation where the QGIS profiles folder doesn't exist
- Fix the default QGIS profiles path on Windows
- Fix environment variables manager
- Fix and improve clean command
- Run unit tests on multiple operating systems: MacOS, Ubuntu LTS and Windows 10

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.7.0).

## 0.6.0 - 2022-05-10

- Profiles synchronization now handle the mixed case where some of downloaded profiles are already installed, and some are not.
- Extend unit tests
- Minor clean up

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.6.0).

## 0.5.0 - 2022-05-09

- Improve profiles synchronization logic by filtering on folders which are (or seem to be) QGIS profiles
- Minor changes

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.5.0).

## 0.4.0 - 2022-05-06

- Deploy: install downloaded profiles into a fresh QGIS install
- Check: operaing system compatibility
- Improve isort and codecov configurations

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.4.0).

## 0.3.0 - 2022-05-05

- Add Python Wheel as packaging option
- Deploy release to Python Package Index
- Complete and improve documentation

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.3.0).

## 0.2.0 - 2022-05-04

- Real start of development!
- Implement pseudo-CI behavior
- Add job to set persistent environment variables on Windows
- Add job to download profiles from a public remote git repository
- Complete CI to automatically build and publish executable for Ubuntu LTS and Windows
- Upgrade every dependencies

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.2.0).

## 0.1.0 - 2021-05-20

- First version, really minimalist
