---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "A guide to the Viam App's Fleet Management and robot configuration/control functionality"
---

## Configuration/logging
When a robot part first comes online, it requests its configuration from the Viam App ([https://app.viam.com](https://app.viam.com)).

Once the robot has a configuration, it caches it locally and can use the configuration for up to 60 days.

The robot checks for new configurations by default every 15 seconds and will reconfigure itself automatically if a new configuration has been set.

All standard process logging is automatically sent to the cloud so you can view all logs remotely.

Both configuration and logging happen securely over HTTPS using secret tokens that are in the robot's configuration.

## Remote control    

If the user uses remote control in the Viam App ([https://app.viam.com](https://app.viam.com)) UI, then all communication to the robot is via WebRTC.

* <a href="https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection" target="_blank">WebRTC Docs</a>[^webrtc]

* [Authentication Docs](../../security)

[^webrtc]:WebRTC Documentation: <a href="https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection" target="_blank">ht<span></span>tps://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection</a>

Local communication between parts can be done over gRPC or WebRTC.

All communication is always encrypted and secured using shared secrets.

The SDKs connect and use the same security and encryption

# Coming soon!
This page will explain:

- How to set up a robot on the Viam App ([https://app.viam.com](https://app.viam.com)).
  - Including based on an existing robot or fragment
- Each tab of the Viam App's robot page:
  - What you can do with them and how they work
- How to filter and modify robots and their permissions
