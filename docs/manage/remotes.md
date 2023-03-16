---
title: "Remotes and Sub-Parts"
linkTitle: "Remotes and Sub-Parts"
weight: 40
type: "docs"
description: "Connect robots to each other."
tags: ["server", "components", "services"]
---

Sometimes you want robots to communicate with each other.
You can do this by establishing a secure connection called a *remote*.
Example use cases include:

- Two rovers mapping a room with SLAM.
  If they can communicate, they can coordinate to divide the work efficiently and avoid crashing into one another.
- A swarm of drones with limited onboard computing power.
  They send images to a computer with significant computing power that runs machine learning code, and sends requests back to the drones based on the data.

Remotes are established using direct [gRPC](https://grpc.io/), or gRPC through [WebRTC](https://webrtc.org/).

Once you configure a remote, the main robot part can access all the components and services configured on the remote robot part as though they were entities of the main robot part.
This is a one-way connection: The main robot part can access the resources of the remote robot part, but the remote robot cannot access the resources of the robot part remoting into it.

## Configuration

Robots are organized into *parts*, where each part represents a computer (a single-board computer like a Raspberry Pi or a desktop, laptop, or other computer), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

To connect two computers that are part of the *same robot*, [configure a sub-part](#configure-a-sub-part).

To connect two computers that are part of *different robots*, [configure a remote](#configure-a-remote).

### Configure a sub-part

You can make a multi-part robot by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.

Use the parts drop-down menu on the [Viam app](https://app.viam.com) to add a new sub-part:

![The Viam app interface with the part drop-down open. A new part called "my-sub-part" is being created.](../img/remotes/sub-part-config.png)

<br>

{{% alert title="Note" color="note" %}}

When you create a sub-part, a *remote* connection is established between the main part and the sub-part without you needing to explicitly configure a remote.

{{% /alert %}}

### Configure a remote

To establish a connection between a part of one robot and a part of a second robot, configure a `remote` on the first robot's part.

1. Go to the Viam app robot page of the robot part to which you wish to establish the remote.
   This is the robot part whose resources will be accessible to the other robot part.
2. Click the **CODE SAMPLE** tab.
3. On the **Language** toggle, select **Remotes**.
4. Copy the `address` of the robot to your clipboard.

![The Viam app CODE SAMPLE tab with Remotes selected and a copyable JSON snippet with the name, address and secret of the robot part.](../img/remotes/remote-address.png)

5. Go to the Viam app robot page of the robot part from which you want to establish a remote connection.
   This is the robot part that will be able to access the resources of the other robot part.
6. Click the **CONFIG** tab, and then click the **REMOTES** sub-tab.

![The Viam app CONFIG tab with the REMOTES sub-tab open.](../img/remotes/remote-create.png)

7. Give the remote connection a name (you can just use the name of the other robot part, for example, "my-other-robot-main") and click **Create Remote**.
8. Paste the `address` (for example, `my-other-robot-main.abc1de23f4.viam.cloud`) into the **Address** field.
9. Click **Add Auth** and paste the `secret` from the other robot's **CODE SAMPLE** tab into the **Auth Key** field.

![The Viam app CONFIG tab with a remote configured.](../img/remotes/remote-config.png)

## Usage

Once your remote is configured, you can access all the components and services configured on the remote robot part as though they were resources of your main robot.
The only difference is that the names of the components have the remote robot part name prepended to them.
For example, instead of calling

```python
servo = Servo.from_robot(robot=robot, name='my_servo')
```

you need to call

```python
servo = Servo.from_robot(robot=robot, name='my-other-robot-main:my_servo')
```

For an example that controls a motor that is a component of a sub-part, see [the Mock Robot tutorial](https://docs.viam.com/tutorials/build-a-mock-robot/#how-to-control-a-sub-part-using-the-viam-sdk).
