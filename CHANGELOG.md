# CHANGELOG

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

<!--

Unreleased

## {version_tag} - YYYY-DD-mm

### Added

### Changed

### Removed

-->

<!-- Release notes generated using configuration in .github/release.yml at main -->

## 0.31.1 - 2024-02-23

### Bugs fixes 🐛

* fix: restore refresh_environment by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/438>

## 0.31.0 - 2024-02-23

### Features and enhancements 🎉

* refacto: remove unused methods and improve doctsrings by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/429>
* Refacto: split profiles sync job by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/432>
* Feature: job environment variables support linux by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/435>

### Tooling 🔧

* ci: use codecov upload token by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/430>
* ci: tag codecov uploads with CI matrix vars by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/431>
* tooling: ignore dev scripts and fixtures from Sonar analisis by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/433>
* ci: disable matrix fail fast by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/434>
* tooling: make sonar ignore tests for duplication by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/436>

## 0.30.2 - 2024-02-22

### Features and enhancements 🎉

* Improve: cleanup OSConfig and refacto CLI's tests to run outside real QGIS profiles folder by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/427>

## 0.30.1 - 2024-02-20

### Bugs fixes 🐛

* fix: undefined variable on Windows if scope != user by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/392>
* fix: change refs to menu_from_projects to match new versioning scheme by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/424>

### Features and enhancements 🎉

* Refacto: factorize logs folders retrieval by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/398>
* fix: tests were failing because of upstream URL change by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/409>
* Feature: log details about Certificates Authority bundle by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/397>
* tests: improve downloader testing by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/412>
* Improve: testing ini files against untracked files by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/416>
* Improve: refacto operating system constants retrieval by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/421>

### Tooling 🔧

* CI: update autolabeler to v5 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/411>
* tooling: enable import autocompletion in VSCode by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/422>

### Documentation 📖

* docs: clean up and fix some syntax errors by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/420>
* docs: add custom qgis profiles folderpath with QGIS_CUSTOM_CONFIG_PATH by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/423>
* docs: add example on run QDT behind a proxy with PowerShell by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/394>
* docs: fix typo spotted by @sylvainbeo by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/395>
* docs: release upper pins of dependencies to reduce dependabot noise by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/417>
* docs: enable social cards by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/418>
* docs: add sitemap by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/419>
* docs: add new plugin's id retrieval method and reorganize the table of contents by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/425>

### Other Changes

* security: bump pillow to 10.2 to fix CVE-2022-22817 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/400>

## 0.30.0 - 2023-12-29

### Bugs fixes 🐛

* Fix: splash screen removal by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/381>

### Features and enhancements 🎉

* Security: increase security scans and improve related documentation by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/352>
* Feature: download from http (part 1) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/351>
* feature: add util to get ProxyHandler and cache some recurring functions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/358>
* feature: use proxy handler in file downloader by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/359>
* feature: add simple http client by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/360>
* improvement: use proxy handle in upgrade sub-command by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/362>
* log: on Linux, add distribution name and version by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/363>
* log: add details about how QDT working folder is determined by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/364>
* Change: move QDT subfolders to generic job by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/347>
* Refacto: use requests to download files by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/367>
* Refacto: remove dead code by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/368>
* Feature: add file size to downloader log by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/369>
* Feature: add log filepath on exit error by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/370>
* feature: HTTP downloader refacto part 2 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/372>
* feature: add function name to log by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/380>
* tests: add more scenarii and factorize test by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/382>
* feature: QdtProfile has now shortcuts to access to ini files and its installed alter-ego by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/383>
* Feature: improve splash screen manager logic by using ini helper intensively by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/384>

### Tooling 🔧

* tooling: add SonarCloud configuration file by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/378>

### Documentation 📖

* docs: improve development guide by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/357>
* docs: update qprofiles-manager with deprecated 'git' value by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/361>
* tooling: add SonarCloud badge by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/371>

## 0.30.0-beta2 - 2023-12-29

### Features and enhancements 🎉

* Refacto: use requests to download files by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/367>
* Refacto: remove dead code by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/368>
* Feature: add file size to downloader log by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/369>
* Feature: add log filepath on exit error by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/370>
* feature: HTTP downloader refacto part 2 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/372>

### Tooling 🔧

* tooling: add SonarCloud configuration file by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/378>

### Documentation 📖

* tooling: add SonarCloud badge by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/371>

## 0.30.0-beta1 - 2023-12-26

### Features and enhancements 🎉

* Security: increase security scans and improve related documentation by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/352>
* Feature: download from http (part 1) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/351>
* feature: add util to get ProxyHandler and cache some recurring functions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/358>
* feature: add simple http client by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/360>
* improvement: use proxy handle in upgrade sub-command by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/362>
* log: on Linux, add distribution name and version by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/363>
* log: add details about how QDT working folder is determined by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/364>
* Change: move QDT subfolders to generic job by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/347>
* feature: use proxy handler in file downloader by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/359>

### Documentation 📖

* docs: improve development guide by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/357>
* docs: update qprofiles-manager with deprecated 'git' value by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/361>

## 0.29.0 - 2023-11-16

### Bugs fixes 🐛

* Fix: local Git repository were not recognized anymore as valid git repository <https://github.com/Guts/qgis-deployment-cli/issues/344>
* Fix: surround profile name with quotes to prevent space by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/348> (<https://github.com/Guts/qgis-deployment-cli/issues/320>)

### Features and enhancements 🎉

* Git synchronization: global improvements by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/346>

### Tooling 🔧

* CI: fix packages-dir path for PyPi upload by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/339>
* Packaging: add operating system name to build report by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/340>
* CI: avoid uploading build reports by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/341>

### Documentation 📖

* Docs: how to manually deploy to PyPi by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/342>

## 0.28.0 - 2023-11-14

### Bugs fixes 🐛

* Disable ConfigParser strict mode to better handling of heterogeneity of QGIS config files by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/334>

### Features and enhancements 🎉

* Add util to format octets size into human-readable format by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/331>
* Refacto: add a Git handler base class to inherit from and avoid duplicate code by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/333>
* Jobs: make downloaded and installed profiles listing more generic by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/336>
* Enhancement: add a module to read and write QGIS ini files by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/337>

### Tooling 🔧

* Packaging: renamed license to match Pypi classifier by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/326>
* Publishing to PyPi: switch to trusted publisher by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/327>
* Add python 3.12 to tests and supported versions by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/328>
* Packaging: restore operating system name in final executables by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/329>
* CI: add discussion category name to link to a GitHub Release by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/330>

### Documentation 📖

* Add demonstration profile viewer mode by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/332>

## 0.27.0 - 2023-11-08

### Bugs fixes 🐛

* Fix missing shortcut template in packaging by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/319>

### Features and enhancements 🎉

* Support custom HTTP proxy setting: QDT_PROXY_HTTP by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/293>
* Refacto: move shortcuts related code into specific subpkg by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/324>
* Quality: global project improvements and clean up by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/325>

### Tooling 🔧

* Improve setup: add extras and factorize requirements loading by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/302>
* Switch license from LGPL3 to Apache License 2 by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/314>
* Packaging: improve output name and PyInstaller options by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/321>
* Tooling: update VS Code config by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/323>

### Documentation 📖

* Mise à jour documentation by @sigeal in <https://github.com/Guts/qgis-deployment-cli/pull/315>

### Other Changes

* Update Pillow to fix CVE related to libwebp by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/313>

## New Contributors

* @sigeal made their first contribution in <https://github.com/Guts/qgis-deployment-cli/pull/315>

**Full Changelog**: <https://github.com/Guts/qgis-deployment-cli/compare/0.26.0...0.27.0>

## 0.26.0 - 2023-06-11

### Bugs fixes 🐛

* Fix: accept different types (URLs or str) as environment variables values by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/291>

## 0.25.0 - 2023-06-13

### Bugs fixes 🐛

* Set download as default action by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/281>

### Features and enhancements 🎉

* Improve: if icon not found, use default QGIS icon (only Linux Free Desktop) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/282>

### Tooling 🔧

* Packaging: add icon to exe by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/285>

### Documentation 📖

* Add demo profile by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/276>
* Documentation: add typical project structure section by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/280>

## 0.24.0 - 2023-05-30

### Features and enhancements 🎉

* Upgrade: download new release binary only in frozen mode by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/266>

### Tooling 🔧

* Docs: deploy only on tags or main by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/265>
* Add feature request issue form by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/272>
* Packaging: publish QDT as Docker image in GHCR by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/274>

### Documentation 📖

* Add job to generate dependencies graph by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/267>
* Complete user manual by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/268>

## 0.23.1 - 2023-05-07

### Bugs fixes 🐛

* Set dulwich minimal version to prevent upstream bug (<https://github.com/jelmer/dulwich/pull/1164>) by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/263>

### Features and enhancements 🎉

* Improve log message during plugin version comparison by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/257>

## 0.23.0 - 2023-04-14

### Features and enhancements 🎉

* Quality: extends tests against file downloader util by @florentfgrs in <https://github.com/Guts/qgis-deployment-cli/pull/245>
* Feature: handle local Git repository by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/255>
* Feature: handle "local" plugins by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/253>

### Documentation 📖

* Docs: use glob to automatically include jobs docs in toctree by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/254>

### New Contributors

* @florentfgrs made their first contribution in <https://github.com/Guts/qgis-deployment-cli/pull/245>

## 0.22.3 - 2023-03-12

* Use QGIS LTR 3.28.4 path as default by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/243>

## 0.22.2 - 2023-03-12

### Features and enhancements 🎉

* Refacto: jobs splash screen and some mutualized methods by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/242>

## 0.22.1 - 2023-03-11

### Bugs fixes 🐛

* Fix: env var obfuscated by lru cache by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/236>
* Fix missing return profile object in shortcut job by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/239>
* Fix and refactoring get_qgis_path which was failing because of bad type passed to ast.literal_eval by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/241>

### Features and enhancements 🎉

* Improvement: make remote scenario downloaded a separate func by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/238>
* Feature: check path now try to expand user vars by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/240>

## 0.22.0 - 2023-03-10

### Features and enhancements 🎉

* Refacto: job shortcuts now use mutualized objects and tools by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/230>
* Feature: add line number to log to make debug easier by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/231>
* Feature: better logging by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/233>
* Improve how invalid YAML files are handled by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/234>
* Improvement: extract name and path from URL of remote scenario and store it properly in QDT work dir by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/235>

## 0.21.3 - 2023-03-09

### Bugs fixes 🐛

* Add default subparser to allow direct run of deployment by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/229>

## 0.21.2 - 2023-03-09

### Bugs fixes 🐛

* Fix unexpected keyword argument 'profiles_folder_to_copy' by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/227>

### Features and enhancements 🎉

* Improve reliability of profiles sync with only_missing by @Guts in <https://github.com/Guts/qgis-deployment-cli/pull/228>

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
