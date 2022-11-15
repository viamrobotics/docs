---
title: "Release Notes"
linkTitle: "Release Notes"
weight: 110
draft: true
type: "docs"
description:
# SME: Mike A.
---
## 15 November 2022
### Release Versions
* rdk - v0.2.0
* api - v0.1.7
* slam - v0.1.7
* viam-python-sdk - v0.2.0
* goutils - v0.1.4
* rust-utils - v0.0.5

### New Features
#### New servo model
##### What is it? 
We added a new servo model called `GPIO.` This represents *any* servo that is connected directly to *any* board via GPIO pins. We created this component in response to the common practice of connecting servos to separate hats, such as the `PCA9685`, rather than connecting directly to the board. Our previous implementation required a direct connection from the servo to the Raspberry Pi.
##### What does it affect? 
While Viam continues to support the `pi` model of servo, we encourage users to begin using the `GPIO` model in *all* of their robots moving forward because it is board-agnostic.
#### Added RTT to remote control page
##### What Is It?
We added a new badge in the `Current Operations` card of the remote control page of the Viam app. This badge lists the RTT (round trip time) of a request from your client to the robot, i.e., the time to complete one request/response cycle.
#### Python 3.8 Support
##### What Is It?
Our Python SDK now supports Python 3.8, in addition to 3.9 and 3.10. You will need to update the Python SDK to access the new feature.
### Improvements
#### New Parameter: extra
##### What is the Extra Parameter?
We added a new API method parameter named, `extra`, that gives users the option of extending existing resource functionality by implementing the new field according to whatever logic they chose. 
`extra` is available to requests for all methods in the following APIs.

* Arm
* Data Manager
* Gripper
* Input Controller
* Motion
* Movement Sensor
* Navigation
* Pose Tracker
* Sensor
* SLAM
* Vision

##### What Does it affect?
**Breaking change**:
Users of the Go SDK **must** update their code to specify `extra` in the arguments that pass into each request.

{{% alert="Note" color="note" %}}
This breaking change does NOT affect users of the Python SDK.
{{% /alert %}}
#### Add dependencies to services
##### What Is It? 
Adding dependencies to services allows Viam to initialize and configure resources in the correct order. For example, if the SLAM service depends on a LiDAR, it will always initialize the LiDAR before the service.
##### What does it affect?

**Breaking Change**: This impacts users of the SLAM service. Users must now specify which sensors they are using in the `depends_on` field of the SLAM configuration.
Other service configurations are not affected.

#### Removed width & height fields from Camera API.

##### What Is It?
We removed two fields (`width` and `height`) that were previously part of the response from the `GetImage` method in the camera API.

##### What does it affect?
This *does not* impact any existing camera implementations. 
Users writing custom camera API implementations no longer need to implement the `width` or `height` fields.
