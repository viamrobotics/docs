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

{{< figure src="../img/app-usage/my-org.png" width="400px" alt="A screenshot of the org drop down showing an example user's name, email, SIGN OUT button, list of organizations, and ORG SETTINGS button." title="The Org drop-down." >}}

If you used an email invite to sign up, the organization that invited you should be listed here.
You also have a personal organization for projects not associated with other organizations.

Click an organization's name to navigate to its list of locations.

### Creating a new organization

To create a new organization, click **ORG SETTINGS** and use the **New Organization** field in the upper left of the page.

### Inviting users to your organization

To invite another user to your organization, type their email address into the field in **ORG SETTINGS** and click **INVITE**.

{{< figure src="../img/app-usage/invite-user.png" width="400px" alt="Screenshot of the user email address invitation field on the Organization settings page." title="The user invitation email address field." >}}

### Deleting an organization

From the **ORG SETTINGS** page, you can delete any organization that has no locations.
If the organization to delete contains any locations, you must delete them before you can delete the organization.

## Managing locations and sub-locations

### Adding locations

When you create a new organization, Viam automatically creates a new location for you.
You can create additional locations by typing a new location name in the **New Location** field found in the left side navigation bar and clicking **ADD**.

Click a location's name to display the list of robots associated with that location.

### Deleting locations

You can delete a location that is *empty of robots* by clicking the trash can icon next to the location name at the top of the page for that location.
The icon will not appear if there are any robots in the location.

### Sharing a location

A location will always have a parent organization (the organization in which it was created).
Other members of the parent organization of a location are granted access to this location by default.

There are two ways to share a location beyond its parent organization:

- Share with all the members of an additional organization you belong to
- Share programmatic access to a location with location secret keys.

#### Sharing a location with an additional organization

Share your location with another organization you belong to by selecting the organization from the **Add Organization** drop-down menu and clicking **Add**.

{{< figure src="../img/app-usage/add-org-drop-down.png" width="400px" alt="The Add Organization drop-down in the Viam app displays all organizations the user is a member of." title="The Add Organization drop-down displays all organizations the user is a member of." >}}

The Viam app lists the newly added organization, along with the parent organization identified as the **primary owner**:

{{< figure src="../img/app-usage/after-add-org.png" width="400px" alt="After adding another org, the Viam app lists it under the orgs that share this location list." title="The Viam app displays all orgs that share this location list." >}}

#### Sharing a location using location secret keys

Grant programmatic access to your location by sharing a location secret key.

The Viam app lists the secret keys for a location in the **Location Secret Keys** drop-down:

{{< figure src="../img/app-usage/location-secret-keys-drop-down.png" width="500px" alt="Screenshot of the list of secret keys that can grant access to a location displays in the location secret keys drop down menu of the Viam app." title="The Viam app displays the location secret keys that can be used to share a location." >}}

Copy the secret key by clicking on the clipboard icon.
Click on the **Generate Key** button to generate a new key.
Use these keys in your SDK code and scripts to authenticate your access to the robots in your location in the cloud.

{{% alert title="Caution" color="caution" %}}
Be cautious when sharing location secret keys in your code or messages.

Do not make a valid key publicly available, as any entity attempting to access your location who has this token will be authenticated, compromising the security of your system.

Note *where* and *when* you share a location secret key. After generating a new secret key, remember that it's best practice to update all references to the key in your code as soon as possible, even though Viam supports flexible key rotation with up to two keys in use at one time.
{{% /alert %}}

#### Share a location with Viam Support

You must share your location with the Viam Support team when requesting support.
To do so, navigate to the proper location and click, **ADD VIAM SUPPORT**.
The button toggles to **REMOVE VIAM SUPPORT**. Click to remove Viam Support from your location.

#### Removing an organization from a shared location

You can remove any organization except the parent organization and Viam Support from the shared list by simply clicking the "X" to the right of its listing.

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

{{< figure src="../img/app-usage/create-robot.png" width="700px" alt="Screenshot of the 'First Location' page on the Viam app with a new robot name in the New Robot field and the ADD ROBOT button next to the field highlighted." title="The New Robot field populated with a user-chosen name." >}}

### Deleting a robot

You can delete a robot by checking the **Sure?** box in the lower left of the robot page and clicking **DELETE ROBOT**.

{{< figure src="../img/app-usage/delete.png" width="400px" alt="Screenshot of the DELETE ROBOT button and the confirmation checkbox (Sure?) next to it." title="DELETE ROBOT button and confirmation checkbox." >}}

Click the name of a robot to go to that robot's page, where you'll find a variety of tools for working with your robot.

## Navigating the robot page

The banner at the top of the robot page displays the robot's location, name, and a drop down list of all parts of that robot.
The first part you create will be the *main part* but you can create additional parts in the drop down.

{{< figure src="../img/app-usage/part-drop-down.png" width="800px" alt="Screenshot of the robot page for an example robot. The parts drop down is open." title="Example Robot Page with the Parts drop-down open (boxed in red)." >}}

To delete a part or make it the main part, use the buttons in the top right of the **CONFIG** tab.

{{< figure src="../img/app-usage/part-mgmt.png" width="800px" alt="Screenshot of the CONFIG tab of a robot's page noting the location of the Make main part and Delete Part buttons." title="Screenshot of the CONFIG tab of a robot's page highlighting the Make main part and Delete Part buttons (boxed in red)." >}}

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

The **HISTORY** tab shows a timestamped diff view of your robot's configuration changes.

### Code Sample

The **CODE SAMPLE** tab contains boilerplate code snippets you can copy and paste into your SDK code to connect to your robot.
There is also a JSON stub you can copy if you wish to use this robot as a remote of another robot.

{{%  snippet "secret-share.md" %}}

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

### Security

The **SECURITY** tab allows you to access and exchange the **Robot Part Secret Keys** of your robot.
A robot part secret is a unique secret used by the robot to communicate with the cloud.

{{< figure src="../img/app-usage/robot-part-secret-keys-drop-down.png" width="800px" alt="Screenshot of the SECURITY tab of a robot's page noting the Robot Part Secret Keys drop-down menu, with the clipboard icon on the far right and the Generate Key button underneath the drop-down." title="Screenshot of the SECURITY tab of a robot's page." >}}

Copy the secret key by clicking on the clipboard icon.
Click on the **Generate Key** button to generate a new key.

{{% alert title="Caution" color="caution" %}}
Be cautious when sharing robot part secret keys in your code or messages.

Do not make a valid key publicly available, as any entity attempting to access your robot who has this token will be authenticated, compromising the security of your system.

Note *where* and *when* you share a robot part secret key. After generating a new secret key, remember that it's best practice to update all references to the key in your code as soon as possible, even though Viam supports flexible key rotation with up to two keys in use at one time.
{{% /alert %}}
