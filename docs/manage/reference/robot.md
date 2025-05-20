---
title: "Robot Management"
linkTitle: "Robot Management"
weight: 30
type: "docs"
description: "Manage your robots through the Viam app."
aliases:
  - /fleet/manage/robot/
  - /manage/fleet/robot/
  - /manage/fleet/manage/robot/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

The Viam app provides a centralized interface for managing your robots.
You can view and edit robot configurations, monitor robot status, and control robot access.

## View robot details

To view details about a specific robot:

1. Navigate to the [**Locations**](https://app.viam.com/locations) page.
2. Select the location containing your robot.
3. Click on the robot's name to view its details.

The robot details page displays the following information:

- **Robot name**: The name of your robot.
- **Robot {{< glossary_tooltip term_id="machine-id" text="ID" >}}**: A unique identifier for your robot.
- **Status**: Indicates whether the robot is online or offline.
- **Last seen**: The last time the robot connected to the Viam cloud.
- **Parts**: A list of parts associated with the robot.
- **Configuration**: The robot's current configuration.

## Edit robot configuration

To edit a robot's configuration:

1. Navigate to the robot's details page.
2. Click the **CONFIG** tab.
3. Make your changes to the configuration.
4. Click **Save changes** to apply your changes.

The configuration is automatically applied to the robot when it next connects to the Viam cloud.

## Monitor robot status

To monitor a robot's status:

1. Navigate to the robot's details page.
2. Click the **STATUS** tab.

The status page displays real-time information about the robot, including:

- **Connection status**: Whether the robot is online or offline.
- **Resource status**: The status of each resource (component, service, etc.) on the robot.
- **Error logs**: Any errors reported by the robot.

## Control robot access

To control who can access a robot:

1. Navigate to the robot's details page.
2. Click the **ACCESS** tab.
3. Use the interface to add or remove users and set their permissions.

## Generate {{< glossary_tooltip term_id="api" text="API" >}} keys

To generate API keys for programmatic access to a robot:

1. Navigate to the robot's details page.
2. Click the **CONNECT** tab.
3. Click **Create new API key**.
4. Enter a name for the key and select the appropriate permissions.
5. Click **Create**.

The API key and key ID will be displayed. Make sure to save these values, as the key will not be displayed again.

## Delete a robot

To delete a robot:

1. Navigate to the robot's details page.
2. Click the **Settings** icon (gear) in the top right corner.
3. Click **Delete robot**.
4. Confirm the deletion by typing the robot's name.

{{% alert title="Warning" color="warning" %}}
Deleting a robot is permanent and cannot be undone. All data associated with the robot will be lost.
{{% /alert %}}