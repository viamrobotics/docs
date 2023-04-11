---
title: "Remotes"
linkTitle: "Remotes"
weight: 30
type: "docs"
no_list: true
description: "Remotes are a way to connect two separate robots so one can access the resources of the other."
tags: ["manage", "components"]
---

Configuring a remote is a way to connect two separate robots so one can access the resources of the other.

To establish a connection between a part of one robot and a part of a second robot, configure a `remote` on the first robot's part.

1. Go to the Viam app robot page of the robot part to which you wish to establish the remote connection.
   This is the robot part whose resources will be accessible to the other robot part.
2. Click the **CODE SAMPLE** tab.
3. On the **Language** toggle, select **Remotes**.
4. Click **COPY JSON**.

   ![The Viam app CODE SAMPLE tab with Remotes selected and a copyable JSON snippet with the name, address and secret of the robot part.](../img/parts-and-remotes/remote-address.png)

5. Go to the Viam app robot page of the robot part from which you want to establish a remote connection.
   This is the robot part that will be able to access the resources of the other robot part.
6. Click the **CONFIG** tab, click the **REMOTES** sub-tab, and select **JSON** mode.

   ![The Viam app CONFIG tab with the REMOTES sub-tab open and JSON mode selected.](../img/parts-and-remotes/remote-json-create.png)

7. Click **Create Remote**.
8. Paste the remote config you copied in step 4 into the empty field.
9. Click **Save Config** in the bottom left of the screen.

<!-- This is possibly wrong--should update with better understanding of auth key versus secret
4. Copy the `address` of the robot to your clipboard.

![The Viam app CODE SAMPLE tab with Remotes selected and a copyable JSON snippet with the name, address and secret of the robot part.](../img/parts-and-remotes/remote-address.png)

5. Go to the Viam app robot page of the robot part from which you want to establish a remote connection.
   This is the robot part that will be able to access the resources of the other robot part.
6. Click the **CONFIG** tab, and then click the **REMOTES** sub-tab.

![The Viam app CONFIG tab with the REMOTES sub-tab open.](../img/parts-and-remotes/remote-create.png)

7. Give the remote a name (you can just use the name of the other robot part, for example, "my-other-robot-main") and click **Create Remote**.
8. Paste the `address` (for example, `my-other-robot-main.abc1de23f4.viam.cloud`) into the **Address** field.
9. Click **Add Auth** and paste the `secret` from the other robot's **CODE SAMPLE** tab into the **Auth Key** field.

![The Viam app CONFIG tab with a remote configured.](../img/parts-and-remotes/remote-config.png)

-->

## Using remote parts with the Viam SDKs

Once your remote part is configured, you can access all the components and services configured on the remote robot part as though they were resources of your main robot part.
The only difference is that the names of the components have the remote robot part name prepended to them.
For example, instead of calling

```python
servo = Servo.from_robot(robot=robot, name='my_servo')
```

you need to call

```python
servo = Servo.from_robot(robot=robot, name='my-other-robot-main:my_servo')
```
