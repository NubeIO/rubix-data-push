# CHANGELOG
## [v1.5.1](https://github.com/NubeIO/lora-raw/tree/v1.5.1) (2020-04-22)
### Added
- Publish calculated values over MQTT
- Republish MQTT value on program start
- Publish over MQTT only if any point value gets updated

## [v1.5.0](https://github.com/NubeIO/lora-raw/tree/v1.5.0) (2020-04-22)
### Fix
- Fix to point scale

## [v1.4.9](https://github.com/NubeIO/lora-raw/tree/v1.4.9) (2020-04-21)
### Fix
- remove points like snr
- made it so point name isnt unique

## [v1.4.8](https://github.com/NubeIO/lora-raw/tree/v1.4.8) (2020-04-20) (deleted)
### Fix
- Add Unary arithmetic operator #960

## [v1.4.7](https://github.com/NubeIO/lora-raw/tree/v1.4.7) (2020-04-20) (deleted)
### Fix
- Add defult value for value_operation #94
- remove naming of point name (device_name) #93
- Improvement/misc #92
- convert bool for motion to int #90


## [v1.4.6](https://github.com/NubeIO/lora-raw/tree/v1.4.6) (2020-04-16) (deleted)
### Fix
- Micro edge Add/Patch

## [v1.4.5](https://github.com/NubeIO/lora-raw/tree/v1.4.5) (2020-04-16) (deleted)
### Fix
- Try/Catch block for looping decoded devices operation

## [v1.4.4](https://github.com/NubeIO/lora-raw/tree/v1.4.4) (2020-04-15) (deleted)
### Fix
- Micro edge output issue

## [v1.4.3](https://github.com/NubeIO/lora-raw/tree/v1.4.3) (2020-04-12) (deleted)
### Fix
- Got inputs types working for the micro-edge

## [v1.4.2](https://github.com/NubeIO/lora-raw/tree/v1.4.2) (2020-04-12) (deleted)
### Fix
- Advanced math function related improvements

## [v1.4.1](https://github.com/NubeIO/lora-raw/tree/v1.4.1) (2020-04-11) 
### Added
- Let user do a more advanced math function

## [v1.4.0](https://github.com/NubeIO/lora-raw/tree/v1.4.0) (2020-03-30)
### Added
- Change value on value_operation PATCH
- LoRa float values inputs PATCH (it was taking only integers values)

## [v1.3.9](https://github.com/NubeIO/lora-raw/tree/v1.3.9) (2020-03-25)
### Added
- Send JSON payload instead of Dictionary

## [v1.3.8](https://github.com/NubeIO/lora-raw/tree/v1.3.8) (2020-03-21)
### Added
- Use gevent instead thread for mapping sync
- Sync points mappings issues fixes

## [v1.3.7](https://github.com/NubeIO/lora-raw/tree/v1.3.7) (2020-03-10)
### Added
- Point Server Generic API uuid/name change support

## [v1.3.6](https://github.com/NubeIO/lora-raw/tree/v1.3.6) (2020-03-03)
### Added
- Upgrade mqtt-rest-bridge (listener issue fix)
- Separate data and config files

## [v1.3.5](https://github.com/NubeIO/lora-raw/tree/v1.3.5) (2020-02-26)
### Added
- MQTT publish value topic issue fix

## [v1.3.4](https://github.com/NubeIO/lora-raw/tree/v1.3.4) (2020-02-25)
### Added
- Use rubix-mqtt base
- Standardize MQTT publish topic

## [v1.3.3](https://github.com/NubeIO/lora-raw/tree/v1.3.3) (2020-02-22)
### Added
- Upgrade rubix-http version

## [v1.3.2](https://github.com/NubeIO/lora-raw/tree/v1.3.2) (2020-02-22)
### Added
- Support for Generic Point payload write
- Edit lora patch point URL
- Add validation on fields network, device, point name
- Implement rubix-http for standardizing HTTP error msg

## [v1.3.1](https://github.com/NubeIO/lora-raw/tree/v1.3.1) (2020-02-16)
### Added
- Updates to protocl bridge

## [v1.3.0](https://github.com/NubeIO/lora-raw/tree/v1.3.0) (2020-02-15)
### Added
- Add protocl bridge

## [v1.2.9](https://github.com/NubeIO/lora-raw/tree/v1.2.9) (2020-02-10)
### Added
- Allow unknown options & ignore while running app

## [v1.2.8](https://github.com/NubeIO/lora-raw/tree/v1.2.8) (2020-02-08)
### Added
- JSON string publish instead of python dictionary

## [v1.2.7](https://github.com/NubeIO/lora-raw/tree/v1.2.7) (2020-01-29)
### Added
- Added a way to patch points

## [v1.2.1](https://github.com/NubeIO/lora-raw/tree/v1.2.1) (2020-01-10)
### Added
- Fixes to MQTT and threading

## [v1.2.0](https://github.com/NubeIO/lora-raw/tree/v1.2.0) (2020-01-07)
### Added
- Temporary fix on MQTT connection establishment
- Points refactor

## [v1.1.0](https://github.com/NubeIO/lora-raw/tree/v1.1.0) (2020-12-29)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting file format from `.ini` to `.json`
- Dockerize

## [v1.1.0-rc.2](https://github.com/NubeIO/lora-raw/tree/v1.1.0-rc.2) (2020-12-28)
### Changed
- Change setting file format from `.ini` to `.json`

## [v1.1.0-rc.1](https://github.com/NubeIO/lora-raw/tree/v1.1.0-rc.1) (2020-12-28)
### Added
- **Breaking Changes**: Make delivery artifact as `binary`
- Change setting.conf format
- Dockerize

