---
title: "Fleet Management"
linkTitle: "Fleet Management"
weight: 30
type: "docs"
description: "Manage your robots in the cloud"
---

Viam's fleet management system allows engineers to configure, control, debug, and manage their robots from the cloud at ([https://app.viam.com](https://app.viam.com)).
[Click here to skip to a walkthrough of the Viam app.](#how-to-use-the-viam-app)

Once you sign up, you can configure your first robot, connect your robot to the cloud, see the logs, control it, update the configuration, and then start bringing your robot to life.

All communication happens securely over HTTPS using secret tokens that are in the robot's configuration.

## Robot Hierarchy

Whether you have one robot, or millions, you can manage them with Viam.
You organize your robots into organizations and locations.

### Organization
An organization is the highest level grouping.
It typical would be a company, or other institution, but could also be an individual or department depending on your needs.

Users in Viam, as defined by an email address, can be a member of multiple organizations.

A member of an organization can invite new users to that organization or create additional organizations.

For example, if you have personal robots at home, and also robots at school, you would belong to two organizations to keep those use cases separate.

### Locations
All robots live inside of locations, which live within organizations. 
Locations allow organizations to organize and manage their fleets.
Organizations often contain several locations.

For example, Cool Robot Inc, which is one organization, may have three warehouses (in NYC, LA, and Chicago).
Cool Robot Inc could organize its robots into three locations based on their physical presence in a given warehouse. Another option would be to organize robots into locations with names such as "Production" and "Testing"--locations do not have to correspond with physical locations.


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

## How to use the Viam app

### Creating an account
If you received an invitation from an existing organization, use the email link to sign up.

If you're signing up without an invitation link, go to [app.viam.com](https://app.viam.com) and create an account with your Google account or an email and password of your choice.

### Navigating organizations
Click the drop down in the upper right corner of the page.
You should see your name, email and a list of organizations you belong to.

If you used an email invite to sign up, the organization that invited you should be listed here.
You also have a personal organization for projects not associated with other organizations.

To create a new organization, click **ORG SETTINGS** and use the **New Organization** field in the upper left of the page.

To invite another user to your organization, type their email address into the **Invite User** field in **ORG SETTINGS** and click **Invite**.

You can delete organizations that are *empty of locations* in the **ORG SETTINGS** page.
If your organization contains any locations, you must delete them before you can delete the organization.

Click the name of an organization to go to the list of its locations.

### Creating locations
When you create a new organization, a location will be automatically created for you.
You can create additional locations by typing a new location name in the **New Location** field found in the left side navigation bar and clicking **ADD**.

You can delete a location that is *empty of robots* by clicking the trash can icon next to the location name at the top of the page for that location.
The icon will not appear if there are any robots in the location.

In the navigation bar on the left, navigate to the location (or sub-location) where you want to create a robot.

Click a location's name to display the list of robots associated with that location.

### Creating robots
When you click on a location that does not contain any robots, you'll be prompted to create a robot by typing in the **New Robot** field and clicking **ADD ROBOT**.

Click the name of a robot to go to the robot page, where you'll find a variety of powerful tools for working with your robot.

### The robot page
The banner at the top of the robot page displays the robot's location, name, and a drop down list of all parts of that robot.
The first part you create will be the _main part_ but you can create additional parts in the drop down.
To delete a part or make it the main part, use the buttons in the top right of the **Config** tab.

If you've connected your robot to a machine running viam-server (instructions below), the banner also displays when the robot was last online, which version of viam-server it is running, the host name, IP address(es), and its operating system.

The following tabs are found on the robot page:

#### Setup
The **Setup** tab contains information for starting an instance of viam-server on your robot's computer. ([See more in-depth install instructions for Linux here](/getting-started/linux-install).) Be sure to select the correct **Mode** and **Architecture** for your system in the upper left of the tab.

#### Config
Here you can start adding robot components, services and remotes.

Toggle between **Builder** (default) or **Raw JSON** in the **Mode** selector in the upper left.
Builder provides a more graphical UI with added features such as a built-in webcam path discovery service.
Raw JSON mode can be useful for users who are familiar with writing JSON, and for seeing and editing everything at once.

Details on configuring specific hardware components and services can be found in these docs:
- [Components](/components/)
- [Services](/services/)

#### Logs
This tab displays debug and other logging information from your robot.

#### History
The History tab shows the edit history of your robot's configuration file.

#### Connect
This tab contains boilerplate code snippets you can copy and paste into your SDK code to connect to your robot.
There is also a JSON stub you can copy if you wish to use this robot as a remote of another robot.

#### Control
The Control tab allows you to control your robot using an interface for each component of your robot.
This is done via WebRTC.
For example, if you have configured a base with wheels, you can control your robot's movement with an arrow pad and fields to change base’s speed.
If you have configured a camera component, a window in the Control tab displays the camera output.

#### Blockly
_**(Experimental!)**_

This tab gives you the option of working on customizing your robot's functionality by using Viam’s block-based coding editor which implements Blockly and Python.