# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

<!--

Unreleased

## {version_tag} - YYYY-DD-mm

### Added

### Changed

### Removed

-->

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
