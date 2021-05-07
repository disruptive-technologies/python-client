# Changelog
All notable changes, fixes, and additions to the project is listed in this changelog.  
After major version v1.0.0, the project adheres to [semantic versioning](https://semver.org/).

# Unreleased
### Changed
- [#52](https://github.com/disruptive-technologies/disruptive-python/pull/52) Replaced `disruptive.errors.TypeError` and `disruptive.errors.ValueError` with built-ins.

# v0.4.1
_Released on 2020-05-04._
### Fixed
- [#49](https://github.com/disruptive-technologies/disruptive-python/pull/49) Fixed forgotten Humidity attribute rename from `temperature` to `celsius`.
- [#50](https://github.com/disruptive-technologies/disruptive-python/pull/50) ConnectionStatus event parameter `available` should be `list[str]`, not `str`.

# v0.4.0
_Released on 2020-05-02._
### Changed
- [#44](https://github.com/disruptive-technologies/disruptive-python/pull/44) A few parameters and attributes has been renamed for consistency.
  - Organization attribute `id` renamed to `organization_id`.
  - Methods `create_dataconnector()` and `update_dataconnector()` parameter `events` renamed to `event_types`.
  - Method `get_device()` parameter `project_id` now defaults to wildcard `"-"` instead of None.
- [#45](https://github.com/disruptive-technologies/disruptive-python/pull/45) Config variable `request_retries` renamed to `request_attempts` to better reflect what is actually does.
- [#46](https://github.com/disruptive-technologies/disruptive-python/pull/46) Logging has been expanded to use either `disruptive.log_level` or the `logging` module.

# v0.3.1
_Released on 2020-04-24._
### Fixed
- [#39](https://github.com/disruptive-technologies/disruptive-python/pull/39) Request retry logic ran 1 loop too few.
### Added
- [#38](https://github.com/disruptive-technologies/disruptive-python/pull/38) Type constant `CLOUD_CONNECTOR` were missing on the Device resource.
- [#41](https://github.com/disruptive-technologies/disruptive-python/pull/41) Added events module type constants on the form `disruptive.events.EVENT_TYPE`.

# v0.3.0
_Released on 2020-04-22._
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
_Released on 2020-04-20._
### Fixed
- [#25](https://github.com/disruptive-technologies/disruptive-python/pull/25) Double timezone info `(+00:00Z)` would break allowed format.
### Added
- [#24](https://github.com/disruptive-technologies/disruptive-python/pull/24) Public classes provided with `__repr__` that adheres to `eval(repr(x))`.
- [#26](https://github.com/disruptive-technologies/disruptive-python/pull/26) Added type constants to Device, DataConnector, and Role resource classes.

# v0.2.2
_Released on 2020-04-18._ 
### Added
- [#23](https://github.com/disruptive-technologies/disruptive-python/pull/23) Added missing metadata about the project for better PyPI presentation.

# v0.2.1
_Released on 2020-04-17._  
Initial pre-release, open-sourcing, and PyPI publication of the project.
