# Changelog
All notable changes, fixes, and additions to the project is listed in this changelog.  
After major version v1.0.0, the project adheres to [semantic versioning](https://semver.org/).

# Unreleased
### Changed
- [#27](https://github.com/disruptive-technologies/disruptive-python/pull/27) Various attributes has been changed.
  - Device attribute `type` renamed to `device_type`.
  - Device attribute `is_emulator` renamed to `is_emulated`.
  - Humidity attribute `temperature` replaced with `celsius` and `fahrenheit`.

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
