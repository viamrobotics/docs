
---
title: "Changelog"
---

## 2023-02-28

### Added

* Remote control power input on machine's CONTROL tab in Viam app
* New encoder model: AMS AS5048
* GetLinearAcceleration method in movement sensor API
* Support for capsule geometry in motion service
* Modular resources in registry
* URDF kinematic file support
* New movement sensor models: ADXL345 and MPU-6050

### Improved

* Camera performance and reliability
* Motion planning with remote components
* Motion planning path smoothing
* Data synchronization reliability

### Changed

* Camera configuration for Webcam, FFmpeg, Transform, and Join pointclouds
* RTT indicator in Viam app
* Python 3.8 support
* New parameter: `extra` in API methods
* Service dependencies
* Removed width and height fields from camera API

## 2022-12-28

### Added

* New servo model called `gpio`
* Badge for RTT (round trip time) of a request from client to machine

### Improved

* RRT\* paths now undergo rudimentary smoothing
* Plan manager now performs direct interpolation for any solution within some factor of the best score

## 2022-11-28

### Changed

* Configuration schemes for camera models: Webcam, FFmpeg, Transform, and Join pointclouds

## 2022-11-15

### Added

* New parameter: `extra` in API methods
* Service dependencies
* RTT indicator in Viam app
* Python 3.8 support
* New servo model called `gpio`
* Badge for RTT (round trip time) of a request from client to machine

### Removed

* Width and height fields from camera API

---

Note: The ina226 power sensor has moved to a module in the repo https://github.com/randhid/renogy. Please update the documentation to reflect this.
