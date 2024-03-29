# CHANGELOG
## [v1.4.1](https://github.com/NubeIO/rubix-data-push/tree/v1.4.1) (2023-10-17)
- Fix: Postgres reconnection issue

## [v1.4.0](https://github.com/NubeIO/rubix-data-push/tree/v1.4.0) (2022-12-08)
- Add additional fields on the sync status
    - Old DB needs to be migrated manually or deleted
    - https://github.com/NubeIO/rubix-data-push/issues/38#issuecomment-1342684672
- Add delete API option for deleting sync logs & pg data

## [v1.3.2](https://github.com/NubeIO/rubix-data-push/tree/v1.3.2) (2022-11-02)
- Make it runnable for old RaspberryPi devices as well

## [v1.3.1](https://github.com/NubeIO/rubix-data-push/tree/v1.3.1) (2022-01-31)
- Add sync logs api endpoints improvements

## [v1.3.0](https://github.com/NubeIO/rubix-data-push/tree/v1.3.0) (2022-01-30)
- Add sync logs api endpoints

## [v1.2.0](https://github.com/NubeIO/rubix-data-push/tree/v1.2.0) (2021-08-18)
- Push all devices output on a bulk

## [v1.1.1](https://github.com/NubeIO/rubix-data-push/tree/v1.1.1) (2021-08-11)
- Decrease reserve time

## [v1.1.0](https://github.com/NubeIO/rubix-data-push/tree/v1.1.0) (2021-07-13)
- Skip data-push sync if points values sync are in process

## [v1.0.9](https://github.com/NubeIO/rubix-data-push/tree/v1.0.9) (2021-07-08)
- Change postgres backup & clear logic

## [v1.0.8](https://github.com/NubeIO/rubix-data-push/tree/v1.0.8) (2021-07-04)
- Backup and clear postgresql data
- Include tags false by default

## [v1.0.7](https://github.com/NubeIO/rubix-data-push/tree/v1.0.7) (2021-06-23)
- Don't timeout on data-push

## [v1.0.6](https://github.com/NubeIO/rubix-data-push/tree/v1.0.6) (2021-06-04)
- Fix: empty point push
- Reconnect on connection failure

## [v1.0.5](https://github.com/NubeIO/rubix-data-push/tree/v1.0.5) (2021-06-02)
- Config driven all data push or limit on new data only

## [v1.0.4](https://github.com/NubeIO/rubix-data-push/tree/v1.0.4) (2021-05-26)
- Add a config to disable ssl verification
- Push all data over and again

## [v1.0.3](https://github.com/NubeIO/rubix-data-push/tree/v1.0.3) (2021-05-26)
- Make each rubix device send it's own payloads

## [v1.0.2](https://github.com/NubeIO/rubix-data-push/tree/v1.0.2) (2021-05-25)
- Add VERSION file

## [v1.0.1](https://github.com/NubeIO/rubix-data-push/tree/v1.0.1) (2021-05-11)
- Config discard_null addition
- Add tags on networks, devices and points

## [v1.0.0](https://github.com/NubeIO/rubix-data-push/tree/v1.0.0) (2021-05-08)
- Initial release
