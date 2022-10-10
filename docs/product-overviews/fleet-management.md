---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "A guide to the Viam App's Fleet Management and robot configuration/control functionality"
---

## Cloud App
Users and organizations store, manage, and control their robotic fleets on the website ([https://app.viam.com](https://app.viam.com)).

All communication happen securely over HTTPS using secret tokens that are in the robot's configuration.


## Organization
On Viam ([https://app.viam.com](https://app.viam.com)), robots belong to organizations.
An organization can be an individual, a research group, or a company.

A user can be a member of multiple organizations, but will always be a member of at least one organization.

Currently, any member of an organization can invite new users to that organization.
Additionally, users can create additional organizations at any point in time.
For example, if a user has robots at home, and also has robots at school, that user would likely belong to two organizations to keep those use cases separate (a home organization and also a school organization).

## Locations
Locations live within organizations. All robots belong to a location.
Locations allow organizations to organize and manage their fleets.
Organizations often contain several locations.
For example, Cool Robot Inc, which is one organization, may have three warehouses (in NYC, LA, and Chicago). Cool Robot Inc could organize its robots into three locations based on their physical presence in a given warehouse. 
With that said, locations do not need to align with physical locations in the real world. Locations are simply a way to subdivide and manage robot fleets.
For example, some users may choose to use locations with names such as "production" and "testing" to separate their robots by development stage (rather than by physical location).

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
