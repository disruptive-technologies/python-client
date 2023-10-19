# Changelog
All notable changes, fixes, and additions to the project is listed in this changelog.  
The project adheres to [semantic versioning](https://semver.org/).

# v1.6.2
### Added
- [#129](https://github.com/disruptive-technologies/python-client/pull/129) Added optional `organization_id` in method `claim_info()`.

# v1.6.1
### Fixed
- [#126](https://github.com/disruptive-technologies/python-client/pull/126) Fixed an issue where UTC tzinfo "Z" was appended to iso-strings already containing tzinfo, resulting in an invalid format.

# v1.6.0
### Changed
- [#124](https://github.com/disruptive-technologies/python-client/pull/124) Bumped pandas extras dependency to major 2.0.
- [#125](https://github.com/disruptive-technologies/python-client/pull/125) Python 3.7 is end-of-life and has been deprecated.

# v1.5.6
### Fixed
- [#123](https://github.com/disruptive-technologies/python-client/pull/123) Added missing constant `disruptive.Device.MOTION`.

# v1.5.5
### Fixed
- [#122](https://github.com/disruptive-technologies/python-client/pull/122) Explicit definition of `Key` and `Member` classes.

# v1.5.4
### Added
- [#121](https://github.com/disruptive-technologies/python-client/pull/121) Support for new `remarks` field in `deskOccupancy` events.

# v1.5.3
### Fixed
- [#120](https://github.com/disruptive-technologies/python-client/pull/120) Unhandled `RequestExceptions` now raised directly.
- [#119](https://github.com/disruptive-technologies/python-client/pull/119) Redirected `/v2/:claim-info` to `/v2/claimInfo`.

### Added
- [#118](https://github.com/disruptive-technologies/python-client/pull/118) Python 3.11 support.

# v1.5.2
### Fixed
- [#117](https://github.com/disruptive-technologies/python-client/pull/117) Method `dt.Claim.claim` parameter `dry_run` True by default.

# v1.5.1
### Fixed
- [#116](https://github.com/disruptive-technologies/python-client/pull/116) Namespace conflict between `dt.Device` and `dt.Claim.Device` in documentation.

# v1.5.0
### Added
- [#114](https://github.com/disruptive-technologies/python-client/pull/114) Implemented Claim API under the `dt.Claim` namespace.

# v1.4.2
### Added
- [#112](https://github.com/disruptive-technologies/python-client/pull/112) Event state constants for code completion ease.
- [#113](https://github.com/disruptive-technologies/python-client/pull/113) Experimental events `DataFrame` support.

# v1.4.1
### Added
- [#108](https://github.com/disruptive-technologies/python-client/pull/108) Emulator desk occupancy support.

# v1.4.0
### Fixed
  - [#106](https://github.com/disruptive-technologies/python-client/pull/106) NetworkStatus event parameters made optional to better reflect API.
  - [#107](https://github.com/disruptive-technologies/python-client/pull/107) `Co2` event parameter `ppm` should be int.
### Added
  - [#105](https://github.com/disruptive-technologies/python-client/pull/105) Added support for new Desk Occupancy sensor and event.

# v1.3.5
### Fixed
  - [#104](https://github.com/disruptive-technologies/python-client/pull/104) Ensure event constants and classes are re-exported and seen by LSPs.

# v1.3.4
### Fixed
  - [#103](https://github.com/disruptive-technologies/python-client/pull/103) Ensure modules are re-exported and seen by LSPs.

# v1.3.3
### Added
  - [#102](https://github.com/disruptive-technologies/python-client/pull/102) Type-checkers like MyPy will now assume we're PEP 561 compliant.

# v1.3.2
### Fixed
  - [#101](https://github.com/disruptive-technologies/python-client/pull/101) `Member` class should have attribute `member_id`.

# v1.3.1
### Changed
- [#100](https://github.com/disruptive-technologies/python-client/pull/100) Method `get_device` optional parameter `project_id` default changed to `None` for consistency.

# v1.3.0
### Fixed
- [#95](https://github.com/disruptive-technologies/python-client/pull/95) Changed stream decoding from ascii to utf-8.
- [#97](https://github.com/disruptive-technologies/python-client/pull/97) Retry policy refined to account for more exceptions.

### Added
- [#98](https://github.com/disruptive-technologies/python-client/pull/98) Added support for motion sensor and event.
- [#99](https://github.com/disruptive-technologies/python-client/pull/99) Added raw attribute to all resource result classes.

# v1.2.2
### Changed
- [#93](https://github.com/disruptive-technologies/python-client/pull/93) Attribute `Project.id` deprecated in favor of `Project.project_id`.

### Added
- [#91](https://github.com/disruptive-technologies/python-client/pull/91) Added `Co2`- and `Pressure` events in `publish_event()` parameter types.
- [#92](https://github.com/disruptive-technologies/python-client/pull/92) Added members `errors` and `outputs` to disruptive module.

# v1.2.1
### Fixed
- [#90](https://github.com/disruptive-technologies/python-client/pull/90) Added missing `EVENT_TYPES` constant of list of all types.

# v1.2.0
### Added
- [#89](https://github.com/disruptive-technologies/python-client/pull/89) Added support for new Co2 sensor and its Co2- and Pressure event types.

# v1.1.0
### Added
- [#87](https://github.com/disruptive-technologies/python-client/pull/87) Package will now authenticate using service account credential environment variables if set.

# v1.0.3
### Changed
- [#86](https://github.com/disruptive-technologies/python-client/pull/86) Added custom User-Agent header.

# v1.0.2
### Changed
- Updates to the [reference documentation](https://developer.disruptive-technologies.com/api/libraries/python/index.html).

# v1.0.1
### Fixed
- [#82](https://github.com/disruptive-technologies/python-client/pull/82) Invalid `log_level` string would cause recusion fixed.

# v1.0.0
Moved to development stage Production/Stable.

# v0.7.1
### Fixed
- [#80](https://github.com/disruptive-technologies/python-client/pull/80) Fixed formatting bug for non-datetime timestamps.

# v0.7.0
### Changed
- [#78](https://github.com/disruptive-technologies/python-client/pull/78) Renamed `NetworkStatusCloudConnector` attribute `cloudconnector_id` to `device_id` for consistency.

# v0.6.2
### Fixed
- [#77](https://github.com/disruptive-technologies/python-client/pull/77) Fixed a bug where Device constructor crashed if productNumber was missing in response.

# v0.6.1
### Fixed
- [#74](https://github.com/disruptive-technologies/python-client/pull/74) Fixed a bug where the stream would simply exit silently if an error were returned by the API.

### Added
- [#75](https://github.com/disruptive-technologies/python-client/pull/75) Added new `product_number` attribute to `Device` class.

# v0.6.0
### Changed
- [#69](https://github.com/disruptive-technologies/python-client/pull/69) Renamed Humidity event attribute "humidity" to "relative_humidity".
- [#70](https://github.com/disruptive-technologies/python-client/pull/70) Replaced EmptyStringError with more general ConfigurationError.

### Added
- [#72](https://github.com/disruptive-technologies/python-client/pull/72) Added support for 2nd generation temperature sensors.

# v0.5.1
_Released on 2021-06-07._
### Fixed
- [e1ae80b](https://github.com/disruptive-technologies/python-client/commit/e1ae80b31c657450ff75521a1bbeace5c30e665b) Added missing constructor for UnknownError.

### Added
- [#68](https://github.com/disruptive-technologies/python-client/pull/68) Added stricter rules for MyPy, resulting in stronger typing.

# v0.5.0
_Released on 2021-05-13._
### Changed
- [#52](https://github.com/disruptive-technologies/disruptive-python/pull/52) Replaced `disruptive.errors.TypeError` and `disruptive.errors.ValueError` with built-ins.
- [#54](https://github.com/disruptive-technologies/disruptive-python/pull/54) Combined `disruptive.Stream.device()` and `.project()` into `.event_stream()`.
- [#56](https://github.com/disruptive-technologies/disruptive-python/pull/56) Method `disruptive.Project.update_member()` roles parameter no longer optional.
- [#57](https://github.com/disruptive-technologies/disruptive-python/pull/57) Method `disruptive.EventHistory.list_events()` now returns a list of events, not an `EventHistory` object.
- [#58](https://github.com/disruptive-technologies/disruptive-python/pull/58) A few key names have been changed.
  - All `serviceaccount` occurances have been renamed to `service_account`.
  - All `dataconnector` occurances have been renamed to `data_connector`.
- [#60](https://github.com/disruptive-technologies/disruptive-python/pull/60) `Auth` methods now returns instances of classes special to the chosen method, like `ServiceAccountAuth`.
- [#61](https://github.com/disruptive-technologies/disruptive-python/pull/61) Renamed a few variables and parameters.
  - Renamed `ServiceAccount` attribute `basic_auth` to `basic_auth_enabled`.
  - Renamed `api_url` to `base_url`.
  - Renamed `emulator_url` to `emulator_base_url`.
- [#64](https://github.com/disruptive-technologies/disruptive-python/pull/64) Method `disruptive.Stream.event_stream()` parameter `label_filters` now takes dict instead of list.

### Added
- [#62](https://github.com/disruptive-technologies/disruptive-python/pull/62) Batch-style resource methods now return a list of errors objects.
- [#63](https://github.com/disruptive-technologies/disruptive-python/pull/63) Exceptions are now grouped into four main groups for easier handling.

# v0.4.1
_Released on 2021-05-04._
### Fixed
- [#49](https://github.com/disruptive-technologies/disruptive-python/pull/49) Fixed forgotten Humidity attribute rename from `temperature` to `celsius`.
- [#50](https://github.com/disruptive-technologies/disruptive-python/pull/50) ConnectionStatus event parameter `available` should be `list[str]`, not `str`.

# v0.4.0
_Released on 2021-05-02._
### Changed
- [#44](https://github.com/disruptive-technologies/disruptive-python/pull/44) A few parameters and attributes has been renamed for consistency.
  - Organization attribute `id` renamed to `organization_id`.
  - Methods `create_dataconnector()` and `update_dataconnector()` parameter `events` renamed to `event_types`.
  - Method `get_device()` parameter `project_id` now defaults to wildcard `"-"` instead of None.
- [#45](https://github.com/disruptive-technologies/disruptive-python/pull/45) Config variable `request_retries` renamed to `request_attempts` to better reflect what is actually does.
- [#46](https://github.com/disruptive-technologies/disruptive-python/pull/46) Logging has been expanded to use either `disruptive.log_level` or the `logging` module.

# v0.3.1
_Released on 2021-04-24._
### Fixed
- [#39](https://github.com/disruptive-technologies/disruptive-python/pull/39) Request retry logic ran 1 loop too few.
### Added
- [#38](https://github.com/disruptive-technologies/disruptive-python/pull/38) Type constant `CLOUD_CONNECTOR` were missing on the Device resource.
- [#41](https://github.com/disruptive-technologies/disruptive-python/pull/41) Added events module type constants on the form `disruptive.events.EVENT_TYPE`.

# v0.3.0
_Released on 2021-04-22._
### Changed
- [#27](https://github.com/disruptive-technologies/disruptive-python/pull/27) Various attributes has been changed.
  - Device attribute `type` renamed to `device_type`.
  - Device attribute `is_emulator` renamed to `is_emulated`.
  - Humidity attribute `temperature` replaced with `celsius` and `fahrenheit`.
- [#35](https://github.com/disruptive-technologies/disruptive-python/pull/35) Moved Data Connector configuration classes to the DataConnector resource.

### Fixed
- [#29](https://github.com/disruptive-technologies/disruptive-python/pull/29) Log would show default `request_retries` even when it was overwritten.
- [#30](https://github.com/disruptive-technologies/disruptive-python/pull/30) Stream.project() did not support `**kwargs`, which it should.
- [#31](https://github.com/disruptive-technologies/disruptive-python/pull/31) Stream retry logic ran one too many times.

# V0.2.3
_Released on 2021-04-20._
### Fixed
- [#25](https://github.com/disruptive-technologies/disruptive-python/pull/25) Double timezone info `(+00:00Z)` would break allowed format.
### Added
- [#24](https://github.com/disruptive-technologies/disruptive-python/pull/24) Public classes provided with `__repr__` that adheres to `eval(repr(x))`.
- [#26](https://github.com/disruptive-technologies/disruptive-python/pull/26) Added type constants to Device, DataConnector, and Role resource classes.

# v0.2.2
_Released on 2021-04-18._ 
### Added
- [#23](https://github.com/disruptive-technologies/disruptive-python/pull/23) Added missing metadata about the project for better PyPI presentation.

# v0.2.1
_Released on 2021-04-17._  
Initial pre-release, open-sourcing, and PyPI publication of the project.
