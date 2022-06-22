---
title: Fleet Management
summary: A guide to app.viam.com's fleet management and robot configuration/control functionality
authors:
    - Matt Dannenberg
date: 2022-05-19
---
## Configuration/logging
When a robot part first comes online, it requests its configuration from app.viam.com.

Once it has a configuration, it is cached locally and can be used for up to 60 days.

It checks for new configurations by default every 15 seconds and will reconfigure itself automatically if a new configuration has been set.

All standard process logging is automatically sent to the cloud so you can view all logs remotely.

Both configuration and logging happen securely over HTTPS using secret tokens that are in the robot configuration.

## Remote control    

If a user uses remote control in the app.viam.com UI, all communication to the robot is via WebRTC. 

[WebRTC Docs](https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection)

[Authentication Docs](../deeper-dive/security.md)

Local communication between parts can be done over gRPC or WebRTC.

All communication is always encrypted and secured using shared secrets.

The SDKs connect and use the same security and encryption

# Coming soon!
This page will explain:

- How to set up a robot on app.viam.com
  - Including based on an existing robot or fragment
- Each tab of app.viam.com's robot page:
  - What you can do with them and how they work
- How to filter and modify robots and their permissions
