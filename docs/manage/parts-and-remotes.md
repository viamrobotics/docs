---
title: "Robot Architecture: Parts, Sub-Parts and Remotes"
linkTitle: "Robot Architecture"
weight: 40
type: "docs"
description: "Connect robots to each other."
tags: ["server", "components", "services"]
---

When robots communicate with each other, they can share resources and operate collaboratively.
This document explains how to establish secure connections between robots.

### Robot parts

Robots are organized into *parts*, where each part represents a computer (a single-board computer, desktop, laptop, or other computer) [running `viam-server`](/installation/), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

Every robot has a main part which is automatically created when you create the robot.
Multi-part robots also have one or more *sub-parts* representing additional computers running `viam-server`.

There are two ways to link robot parts:

- **Sub-part**: If you have two computers within the *same robot*, use one as the main part and [connect the other to it as a sub-part](#configure-a-sub-part).

- **Remote**: To connect two computers that are parts of *different robots*, [add one robot part as a remote part of the other robot](#configure-a-remote).

Connections between robots are established using the best network path available.

When you configure a remote or a sub-part, the main robot part can access all the components and services configured on the remote robot part as though they were entities of the main robot part.
This is a one-way connection: the main robot part can access the resources of the remote robot part, but the remote robot cannot access the resources of the robot part remoting into it.

![Example of a remote and a two part robot where the main (and only) part of robot 1 remotes into the main part of robot 2, and thus has access to all resources of robot 2.](../img/parts-and-remotes/remotes-diagram.png)

## Configuration

### Configure a sub-part

You can make a multi-part robot by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.
Sub-parts will *not* have access to the resources of the main part.

Use the parts drop-down menu in the top banner of your robot's page on the [Viam app](https://app.viam.com) to add a new sub-part:

![The Viam app interface with the part drop-down open. A new part called "my-sub-part" is being created.](../img/parts-and-remotes/sub-part-config.png)

To delete a sub-part or make it the main part, use the buttons in the top right of the **Config** tab.

![The config tab of a robot's page noting the location of the Make main part and Delete Part buttons.](../img/parts-and-remotes/part-mgmt.png)

### Configure a remote

To establish a connection between a part of one robot and a part of a second robot, configure a `remote` on the first robot's part.

1. Go to the Viam app robot page of the robot part to which you wish to establish the remote connection.
   This is the robot part whose resources will be accessible to the other robot part.
2. Click the **Code Sample** tab.
3. On the **Language** toggle, select **Remotes**.
4. Click **Copy JSON**.

   ![The Viam app CODE SAMPLE tab with Remotes selected and a copyable JSON snippet with the name, address and secret of the robot part.](../img/parts-and-remotes/remote-address.png)

5. Go to the Viam app robot page of the robot part from which you want to establish a remote connection.
   This is the robot part that will be able to access the resources of the other robot part.
6. Click the **Config** tab, click the **Remotes** subtab, and select **JSON** mode.

   ![The Viam app CONFIG tab with the REMOTES subtab open and JSON mode selected.](../img/parts-and-remotes/remote-json-create.png)

7. Click **Create Remote**.
8. Paste the remote config you copied in step 4 into the empty field.
9. Click **Save Config** in the bottom left of the screen.

<!-- This is possibly wrong--should update with better understanding of auth key versus secret
4. Copy the `address` of the robot to your clipboard.

![The Viam app CODE SAMPLE tab with Remotes selected and a copyable JSON snippet with the name, address and secret of the robot part.](../img/parts-and-remotes/remote-address.png)

5. Go to the Viam app robot page of the robot part from which you want to establish a remote connection.
   This is the robot part that will be able to access the resources of the other robot part.
6. Click the **Config** tab, and then click the **Remotes** subtab.

![The Viam app CONFIG tab with the REMOTES subtab open.](../img/parts-and-remotes/remote-create.png)

7. Give the remote a name (you can just use the name of the other robot part, for example, "my-other-robot-main") and click **Create Remote**.
8. Paste the `address` (for example, `my-other-robot-main.abc1de23f4.viam.cloud`) into the **Address** field.
9. Click **Add Auth** and paste the `secret` from the other robot's **Code Sample** tab into the **Auth Key** field.

![The Viam app CONFIG tab with a remote configured.](../img/parts-and-remotes/remote-config.png)

-->

## Using remote parts and sub-parts with the Viam SDKs

Once your sub-part or remote part is configured, you can access all the components and services configured on the sub-part or remote robot part as though they were resources of your main robot part.
The only difference is that the names of the components have the remote robot part name prepended to them.
For example, instead of calling

```python
servo = Servo.from_robot(robot=robot, name='my_servo')
```

you need to call

{{< tabs >}}
{{% tab name="Sub-part" %}}

```python
servo = Servo.from_robot(robot=robot, name='my-sub-part-name:my_servo')
```

{{% /tab %}}
{{% tab name="Remote Part" %}}

```python
servo = Servo.from_robot(robot=robot, name='my-other-robot-main:my_servo')
```

{{% /tab %}}
{{< /tabs >}}

For an example that controls a motor that is a component of a sub-part, see [the Mock Robot tutorial](https://docs.viam.com/tutorials/configure/build-a-mock-robot/#how-to-control-a-sub-part-using-the-viam-sdk).
