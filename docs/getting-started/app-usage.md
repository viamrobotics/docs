--- 
title: "Getting Started with the Viam App"
linkTitle: "Using the Viam App"
weight: 2
type: "docs"
description: "A guide to getting started with app.viam.com."
---
The [Viam app](https://app.viam.com/) is a tool for configuring, controlling, and managing robots from anywhere.
This guide covers how to manage organizations, locations, robots, and robot parts from the Viam app.

{{% alert title="Info" color="tip" %}}
For more conceptual information about what organizations, locations, robots, and parts represent, see our [fleet management overview](/product-overviews/fleet-management/).
{{% /alert %}}

## Creating an account

If you received an invitation from an existing organization, use the email link to sign up.

If you're signing up without an invitation link, go to [app.viam.com](https://app.viam.com/) and create an account with your Google account or an email and password of your choice.

## Navigating organizations

Click the drop down in the upper right corner of the page.
You should see your name, email, and a list of organizations you belong to.

<img src="../img/app-usage/my-org.png" width="500px" alt="A screenshot of the org drop down showing an example user's name, email, SIGN OUT button, list of organizations, and ORG SETTINGS button.">

If you used an email invite to sign up, the organization that invited you should be listed here.
You also have a personal organization for projects not associated with other organizations.

To create a new organization, click **ORG SETTINGS** and use the **New Organization** field in the upper left of the page.

To invite another user to your organization, type their email address into the field in **ORG SETTINGS** and click **INVITE**.

<img src="../img/app-usage/invite-user.png" width="400px" alt="Screenshot of the user invitation field in the organization settings page." title="test"><br>

You can delete organizations that are *empty of locations* in the **ORG SETTINGS** page.
If your organization contains any locations, you must delete them before you can delete the organization.

Click the name of an organization to go to the list of its locations.

## Managing locations and sub-locations

### Adding locations

When you create a new organization, Viam automatically creates a new location for you.
You can create additional locations by typing a new location name in the **New Location** field found in the left side navigation bar and clicking **ADD**.

Click a location's name to display the list of robots associated with that location.

### Deleting locations

You can delete a location that is *empty of robots* by clicking the trash can icon next to the location name at the top of the page for that location.
The icon will not appear if there are any robots in the location.

### Sub-locations

To create a sub-location:

1. Create a location and add at least one robot to it. 
2. From the bottom of the soon-to-be-sub-location's page, use the **New Parent Location** drop-down to choose a parent location.
3. Click **CHANGE** after selecting the new parent location.

You can continue nesting sub-locations in this way.
To move a sub-location to the first level of locations, select **Root** from the **New Parent Location** drop-down and then click **CHANGE**.

## Managing robots

In the navigation bar on the left, navigate to the location (or *sub-location*) where you want to create a robot.

### Adding a new robot

When you click on a location that does not contain any robots, you'll be prompted to create a robot by typing in the **New Robot** field and clicking **ADD ROBOT**.

![A screenshot of the First Location page on app.viam.com with a new robot name in the New Robot field, and the ADD ROBOT button next to the field highlighted.](../img/app-usage/create-robot.png)

### Deleting a robot

You can delete a robot by checking the **Sure?** box in the lower left of the robot page and clicking **DELETE ROBOT**.

<img src="../img/app-usage/delete.png" width="380px" alt="A screenshot of the DELETE ROBOT button and the Sure? checkbox next to it."><br>

Click the name of a robot to go to that robot's page, where you'll find a variety of powerful tools for working with your robot.

## Navigating the robot page

The banner at the top of the robot page displays the robot's location, name, and a drop down list of all parts of that robot.
The first part you create will be the _main part_ but you can create additional parts in the drop down.

![A screenshot of the robot page for an example robot. The parts drop down is open and highlighted.](../img/app-usage/part-drop-down.png)

To delete a part or make it the main part, use the buttons in the top right of the **CONFIG** tab.

![A screenshot of the CONFIG tab of a robot's page. The Make main part and Delete Part buttons are highlighted.](../img/app-usage/part-mgmt.png)

If you've connected your robot to a machine running viam-server (instructions below), the banner also displays when the robot was last online, which version of viam-server it is running, the host name, IP address(es), and its operating system.

The following tabs are found on the robot page:

### Setup

The **SETUP** tab contains information for starting an instance of viam-server on your robot's computer.
Be sure to select the correct **Mode** and **Architecture** for your system in the upper left of the tab.

{{% alert title="Tip" color="tip" %}}
More in-depth information on installing viam-server can be found in our [Linux install](/installation/linux-install/) and [macOS install](/installation/macos-install/) docs.
{{% /alert %}}

### Config

Here you can start adding robot components, services, and remotes.

Toggle between **Builder** (default) or **Raw JSON** using the **Mode** selector in the upper left.
Builder provides a more graphical UI with added features such as a built-in webcam path discovery service.
Raw JSON mode can be useful for users who are familiar with writing JSON, and for seeing and editing everything at once.

Within the **CONFIG** tab (in builder mode) are separate sub-tabs for components, services, remotes, processes, network, authentication, and fragments, so be sure to configure these in their respective tabs.
In raw JSON mode, all of these resources are displayed in a single text field.

Details on configuring specific hardware components and services can be found in these topics:
- [Components](/components/)
- [Services](/services/)

### Logs

The **LOGS** tab displays debug and other logging information from your robot.

### History

The **HISTORY** tab shows the edit history of your robot's configuration file.

### Code Sample

The **CODE SAMPLE** tab contains boilerplate code snippets you can copy and paste into your SDK code to connect to your robot.
There is also a JSON stub you can copy if you wish to use this robot as a remote of another robot.

{{% alert title="Caution" color="caution" %}}  
Do not share your robot secret or robot address publicly.
Sharing this information compromises your system security by allowing unauthorized access to your computer.
{{% /alert %}}

### Control

The **CONTROL** tab allows you to control your robot using an interface for each component of your robot.
This is done via WebRTC.
For example, if you have configured a base with wheels, you can control your robot's movement with an arrow pad and fields to change base’s speed.
If you have configured a camera component, a window in the Control tab displays the camera output.

### Blockly

{{% alert title="Note" color="note" %}}
This is an experimental feature.
Stability is not guaranteed.
Breaking changes are likely to occur, and occur often.
{{% /alert %}}

This tab gives you the option of working on customizing your robot's functionality by using Viam’s block-based coding editor which implements Blockly and Python.