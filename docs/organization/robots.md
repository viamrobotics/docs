---
title: "Manage Robots"
linkTitle: "Robots"
weight: 40
type: "docs"
no_list: true
description: "A robot is an organizational concept, consisting of either one or multiple parts working closely together to complete tasks."
tags: ["fleet management", "cloud", "app"]
---

A robot is an organizational concept, consisting of either one _part_, or multiple _parts_ working closely together to complete tasks.
The robot represents the configuration and entry point for one or more computers (and the components they control) coupled into one logical grouping of parts that work together to complete tasks.
A robot usually reflects a physical device, from a camera collecting images, to a wheeled rover, or an articulated arm on a factory floor.
A robot always has a main part that receives client requests, and any number of other parts.

## Robot parts

Robots are organized into _parts_, where each part represents a computer (a single-board computer, desktop, laptop, or other computer) [running `viam-server`](/installation/), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

Every robot has a main part.
Multi-part robots also have one or more _sub-parts_ representing additional computers running `viam-server`.

There are two ways to link robot parts:

- **Sub-part**: If you have two computers within the _same robot_, use one as the main part and [connect the other to it as a sub-part](#configure-a-sub-part).

- **Remote**: To connect two computers that are parts of _different robots_, [add one robot part as a remote part of the other robot](../../configuration/remotes).

Connections between robots are established using the best network path available.

When you configure a remote or a sub-part, the main robot part can access all the components and services configured on the remote robot part as though they were entities of the main robot part.
This is a one-way connection: The main robot part can access the resources of the remote robot part, but the remote robot cannot access the resources of the robot part remoting into it.

![Example of a remote and a two part robot where the main (and only) part of robot 1 remotes into the main part of robot 2, and thus has access to all resources of robot 2.](../img/remotes-diagram.png)

## Add a new robot

Add a new robot by providing a name in the **New Robot** field and clicking **ADD ROBOT**.

![The 'First Location' page on the Viam app with a new robot name in the New Robot field and the ADD ROBOT button next to the field highlighted.](../img/app-usage/create-robot.png)

Click the name of a robot to go to that robot's page, where you'll find a variety of tools for working with your robot.

The banner at the top of the robot page displays the robot's location, name, and a drop down list of all parts of that robot.
When you crate a robot, a _main part_ is automatically created for you but you can create additional parts in the drop down.

![The robot page for an example robot with the parts drop down open.](../img/app-usage/part-drop-down.png)
To delete a part or make it the main part, use the buttons in the top right of the **CONFIG** tab.

![The CONFIG tab of a robot's page noting the location of the Make main part and Delete Part buttons.](../img/app-usage/part-mgmt.png)

If you've connected your robot to a machine running `viam-server`, the banner also displays when the robot was last online, which version of `viam-server` it is running, the host name, the IP address or addresses, and its operating system.

## Configure a sub-part

You can make a multi-part robot by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.
Sub-parts will _not_ have access to the resources of the main part.

Use the parts drop-down menu in the top banner of your robot's page on the [Viam app](https://app.viam.com) to add a new sub-part:

![The Viam app interface with the part drop-down open. A new part called "my-sub-part" is being created.](../img/sub-part-config.png)

### Using sub-parts with the Viam SDKs

Once your sub-part is configured, you can access all the components and services configured on the sub-part as though they were resources of your main robot part.
The only difference is that the names of the components have the sub-part name prepended to them.
For example, instead of calling

```python
servo = Servo.from_robot(robot=robot, name='my_servo')
```

you need to call

```python
servo = Servo.from_robot(robot=robot, name='my-sub-part-name:my_servo')
```

For an example that controls a motor that is a component of a sub-part, see [the Mock Robot tutorial](https://docs.viam.com/tutorials/configure/build-a-mock-robot/#how-to-control-a-sub-part-using-the-viam-sdk).

## Delete a robot

You can delete a robot by checking the **Sure?** box in the lower left of the robot page and clicking **DELETE ROBOT**.

![The DELETE ROBOT button and the confirmation checkbox (Sure?) next to it.](../img/app-usage/delete.png)
