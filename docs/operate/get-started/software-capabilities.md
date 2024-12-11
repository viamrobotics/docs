---
linkTitle: "Add software capabilities"
title: "Add software capabilities"
weight: 40
layout: "docs"
type: "docs"
no_list: true
description: "TODO"
---

## Augmented hardware

Bases, failover sensors, etc

Base
- [sensor-controlled](https://docs.viam.com/components/base/sensor-controlled/)
- [wheeled](https://docs.viam.com/components/base/wheeled/)
- [ackermann](https://github.com/mcvella/viam-ackermann-base)

Camera
- [transform](https://docs.viam.com/components/camera/transform/)
- [ffmpeg](https://docs.viam.com/components/camera/ffmpeg/)

Motor
- [encoded](https://docs.viam.com/components/motor/encoded-motor/#control-motor-velocity-with-encoder-feedback)

Movement Sensor
- [wheeled odometry](https://docs.viam.com/components/movement-sensor/wheeled-odometry/)
- [merged](https://docs.viam.com/components/movement-sensor/merged/)
- [failover](https://github.com/viam-modules/failover)

Power Sensor
- [failover](https://github.com/viam-modules/failover)

Sensor
- [failover](https://github.com/viam-modules/failover)

## Software-only components

### Generic components/services

- [Event manager](https://github.com/viam-labs/SAVCAM-event-manager)
- [ChatGPT](https://github.com/jeremyrhyde/chat-gpt-module)
- [i2cdetect](https://github.com/michaellee1019/i2cdetect) (detects all active i2c addresses)

### Sensors

Random number generator, etc

### Cameras

[rtsp](https://github.com/viam-modules/viamrtsp) (can connect to a family of cameras)
