# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

<!--

Unreleased

## {version_tag} - YYYY-DD-mm

### Added

### Changed

### Removed

-->

## 0.21.1 - 2023-03-09

### Bugs fixes 🐛

* Hotfix crash when some profiles have a lesser version by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/226>

## 0.21.0 - 2023-03-09

### Bugs fixes 🐛

* Fix: outdated profiles should also be copied when sync_mode=only_different by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/225>

### Features and enhancements 🎉

* Improve upgrade subcommand by handling GitHub Token by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/219>
* Tooling: complete JSON schemas and job documentation by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/224>

### Tooling 🔧

* Add bug report issue form by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/222>

### Documentation 📖

* Documentation: improve download page by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/220>

## 0.20.0 - 2023-03-07

### Features and enhancements 🎉

* Tooling: add pyupgrade as git hook by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/218>
* Profiles synchronization: add sync_mode option by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/97>

### Documentation 📖

* Add funding page by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/217>

## 0.19.0 - 2023-03-03

### Features and enhancements 🎉

* Refacto: remove unused modules (dead code) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/207>
* Improve: test coverage bouncer by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/209>
* Switch to a generic Job object with inheritance by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/208>
* Clean up: rm former validations methods by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/210>
* Tooling: add ruff to git hooks by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/211>
* Feature: use environment variables to set arguments values by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/215>
* Feature: support remote scenario path by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/216>

### Documentation 📖

* Documentation: add how to grab a plugin_id by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/214>

## 0.18.0 - 2023-03-02

### Bugs fixes 🐛

* Fix message when there is no newer version by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/205>

### Features and enhancements 🎉

* Add helper to handle common error on exe name by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/206>
* Feature: job to manage environment variables now handles `remove` action by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/199>

### Documentation 📖

* Add doc page about environment variable job by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/198>

## 0.17.0 - 2023-02-28

A version focused on refacto to reduce external dependencies.

### Features and enhancements 🎉

* Refacto: clean up rm unused subcmd by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/192>
* Refacto: replace click by argparse by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/194>
* Refacto: remove dependency to py-setenv by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/196>
* Refacto: remove rich dependency by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/197>

### Tooling 🔧

* Packaging: build and package for MacOS (experimental) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/195>

## 0.16.2 - 2023-02-23

### Bugs fixes 🐛

* Fix QGIS bin path retriever by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/191>

### Features and enhancements 🎉

* Tooling and documentation: JSON schema for profile editing by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/187>

### Documentation 📖

* Documentation: fix build and switch to Furo theme by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/188>

## 0.16.1 - 2023-01-30

### Bugs fixes 🐛

* Embed shortcut template into packages by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/181>

### Features and enhancements 🎉

* Tooling: upgrade JSON schemas by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/180>
* Feature: upgrade show changelog by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/179>

## 0.16.0 - 2023-01-27

### Features and enhancements 🎉

* Dependencies: replace semver by packaging to compare versions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/177>
* Feature: improve shortcut manager to create shortcuts on Linux (FreeDesktop) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/178>

## 0.15.0 - 2023-01-26

### Features and enhancements 🎉

* Feature: plugins synchronization part 3 - Upgrade older plugins by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/176>

## 0.14.1 - 2023-01-21

### Bugs fixes 🐛

* Fix: download URL should use folder_name when exists instead of name by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/175>

## 0.14.0 - 2023-01-21

### Features and enhancements 🎉

* Feature: add a subcommand to upgrade the CLI by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/169>
* Feature: plugins downloader by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/168>
* Feature: plugins synchronization - part 1 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/172>
* Feature: plugins synchronization part 2 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/174>

### Tooling 🔧

* CI: build Python wheel using build package by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/170>
* Use GE to deploy to GH Pages instead of branch gh-pages by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/171>
* Set minimal Python to 3.10 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/173>

## 0.13.0 - 2023-01-16

### Features and enhancements 🎉

* Add module to check image size by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/151>
* Add test for utils.slugifier by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/165>
* Improve test coverage on check image by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/166>
* Increase test coverage by @vicente23 in <https://github.com/Guts/qgis-deployment-cli/pull/157>
* Feature: add option to check splash screen dimensions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/167>

## 0.12.0 - 2022-11-26

### Bugs fixes 🐛

* Replace the variable scenario by scenario_filepath by @vicente23 in <https://github.com/Guts/qgis-deployment-cli/pull/148>
* Check the validity of the scenario file by @vicente23 in <https://github.com/Guts/qgis-deployment-cli/pull/149>
* Make the remote git handler much more robust to  by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/154>

### Features and enhancements 🎉

* Allow to specify branch to clone/pull by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/152>
* Make logging binary : warning or debug by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/155>
* Add utils module to check paths in a centralized way by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/156>

### Tooling 🔧

* Fix documentation build on CI by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/144>
* Packaging: Add Python 3.11 to supported versions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/153>

## 0.11.0 - 2022-11-16

* Add new job to manage custom splash screen
* Fix: job shortcut-manager was failing when icon is not defined
* Bump dependencies

## 0.10.0 - 2022-05-25

* Minor bug fixes
* Extends unit tests (65%)

## 0.9.0 - 2022-05-18

* handle `~` char in scenario files to represent the end-user home folder
* add [`utils.str2bool`](https://guts.github.io/qgis-deployment-cli/_apidoc/qgis_deployment_toolbelt.utils.str2bool.html) to convert `str` to `bool`. Useful to process environment variables which are always stored/retrieved as strings.
* add [`utils.win32utils.get_environment_variable`](https://guts.github.io/qgis-deployment-cli/_apidoc/qgis_deployment_toolbelt.utils.win32utils.html) to retrieve environment variable directly from Windows registry, because `os.getenv` uses the configuration at the run moment
* Documentation: add an auto-generated table of dependencies and their license within the [Credits page](https://guts.github.io/qgis-deployment-cli/misc/credits.html)
* Fix a bug when the icon path was not set for a shortcut
* Extend unit tests to reach 60% of coverage

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.9.0).

## 0.8.0 - 2022-05-16

* Pin dulwich version to avoid recurring connection errors
* Add support for environment variable `QGIS_CUSTOM_CONFIG_PATH`
* Make clone/pull more robust
* Extend unit tests

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.8.0).

## 0.7.0 - 2022-05-16

* Add module to create and delete application shortcuts
* Add job to use the new module to automatically create shortcuts for QGIS profiles
* Promote constants module to a dataclass (Python 3.7+)
* Remove subcommand to set environment variables
* Rename `environment_variables` section to `settings` in scenario files
* Handle situation where the QGIS profiles folder doesn't exist
* Fix the default QGIS profiles path on Windows
* Fix environment variables manager
* Fix and improve clean command
* Run unit tests on multiple operating systems: MacOS, Ubuntu LTS and Windows 10

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.7.0).

## 0.6.0 - 2022-05-10

* Profiles synchronization now handle the mixed case where some of downloaded profiles are already installed, and some are not.
* Extend unit tests
* Minor clean up

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.6.0).

## 0.5.0 - 2022-05-09

* Improve profiles synchronization logic by filtering on folders which are (or seem to be) QGIS profiles
* Minor changes

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.5.0).

## 0.4.0 - 2022-05-06

* Deploy: install downloaded profiles into a fresh QGIS install
* Check: operaing system compatibility
* Improve isort and codecov configurations

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.4.0).

## 0.3.0 - 2022-05-05

* Add Python Wheel as packaging option
* Deploy release to Python Package Index
* Complete and improve documentation

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.3.0).

## 0.2.0 - 2022-05-04

* Real start of development!
* Implement pseudo-CI behavior
* Add job to set persistent environment variables on Windows
* Add job to download profiles from a public remote git repository
* Complete CI to automatically build and publish executable for Ubuntu LTS and Windows
* Upgrade every dependencies

> See the [GitHub Release for a detailed changelog](https://github.com/Guts/qgis-deployment-cli/releases/tag/0.2.0).

## 0.1.0 - 2021-05-20

* First version, really minimalist
