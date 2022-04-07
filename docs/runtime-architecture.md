---
title: Viam Runtime Architecture
summary: High level overview of the runtime architecture for Viam's robotics platform
authors:
    - Matt Dannenberg
date: 2022-04-08
---
# Runtime Architecture

## Configuration/logging
When a robot part first comes online, it requests its configuration from app.viam.com

Once it has a configuration, it is cached locally and can be used for up to 60 days.

It checks for new configurations by default every 15 seconds and will reconfigure itself automatically if a new configuration has been set.

All standard process logging is automatically sent to the cloud so you can view all logs remotely.

Both configuration and logging happen securely over HTTPS using secret tokens that are in the robot configuration.

## Remote control    

If a user uses remote control in the app.viam.com ui, all communication to the robot is via webrtc. 

[WebRTC Docs](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection)

[Authentication docs](authentication.md)

Local communication between parts can be done over grpc or webrtc.

All communication is always encrypted and secured using shared secrets.

The SDKS connect and use the same security and encryption
