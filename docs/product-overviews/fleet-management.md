---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Manage your robots in the cloud"
---

Viam's Fleet management allows engineers to configure, control, debug, and manage their robots from the cloud at ([https://app.viam.com](https://app.viam.com)).

Once you sign up, you can configure your first robot, connect your robot to the cloud, see the logs, control it, update the configuration, and then start bringing your robot to life.

All communication happen securely over HTTPS using secret tokens that are in the robot's configuration.

## Robot Hierarchy

Whether you have one robot, or millions, you can manage them with Viam.
You organize your robots into Organizations and locations.

### Organization
An organization is the highest level grouping.
It typical would be a company, or other institution, but could also be an individual or department depending on your needs.

Users in Viam, as defined by an email address, can be a member of multiple organizations.

Member of an organization can invite new users to that organization or  create additional organizations at any point in time.

For example, if you have personal robots at home, and also robots at school, you would belong to two organizations to keep those use cases separate.

## Locations
All robots live inside of a locations, wihich live within organizations. 
Locations allow organizations to organize and manage their fleets.
Organizations often contain several locations.

For example, Cool Robot Inc, which is one organization, may have three warehouses (in NYC, LA, and Chicago).
Cool Robot Inc could organize its robots into three locations based on their physical presence in a given warehouse. 


## Configuration/logging
When a robot part first comes online, it requests its configuration from the Viam App ([https://app.viam.com](https://app.viam.com)).

Once the robot has a configuration, it caches it locally and can use the configuration for up to 60 days.

The robot checks for new configurations every 15 seconds and will reconfigure itself automatically if needed.

Logs are automatically sent to the cloud so you can view them easily.

## Remote control    

If the user uses remote control in the Viam App ([https://app.viam.com](https://app.viam.com)) UI, then all communication to the robot is via WebRTC.

* <a href="https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection" target="_blank">WebRTC Docs</a>[^webrtc]

* [Authentication Docs](../../security)

[^webrtc]:WebRTC Documentation: <a href="https://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection" target="_blank">ht<span></span>tps://pkg.go.dev/go.viam.com/utils@v0.0.3/rpc#hdr-Connection</a>

Local communication between parts can be done over gRPC or WebRTC.

# Coming soon!
This page will explain:

- How to set up a robot on the Viam App ([https://app.viam.com](https://app.viam.com)).
  - Including based on an existing robot or fragment
- Each tab of the Viam App's robot page:
  - What you can do with them and how they work
- How to filter and modify robots and their permissions
