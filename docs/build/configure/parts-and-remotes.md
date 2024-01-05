---
title: "Architecture: Parts, Sub-Parts, and Remotes"
linkTitle: "Machine Architecture"
weight: 40
type: "docs"
description: "Connect multiple machine parts to each other as sub-parts or remotes."
tags: ["server", "components", "services"]
aliases:
  - /manage/parts-and-remotes/
---

When {{< glossary_tooltip term_id="machine" text="smart machines" >}} communicate with each other, they can share resources and operate collaboratively.
This document explains how to establish secure connections between machines.

### Machine parts

Machines are organized into _parts_, where each part represents a computer (a single-board computer, desktop, laptop, or other computer) [running `viam-server`](/get-started/installation/), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

Every smart machine has a main part which is automatically created when you create the machine.
Multi-part machines also have one or more _sub-parts_ representing additional computers running `viam-server`.

There are two ways to link machine parts:

- **Sub-part**: If you have two computers within the _same machine_, use one as the main part and [connect the other to it as a sub-part](#configure-a-sub-part).

- **Remote**: To connect two computers that are parts of _different machines_, [add one machine part as a remote part of the other machine](#configure-a-remote).

Connections between machines are established using the best network path available.

When you configure a remote or a sub-part, the main machine part can access all the components and services configured on the remote machine part as though they were entities of the main machine part.
This is a one-way connection: the main machine part can access the resources of the remote machine part, but the remote machine cannot access the resources of the machine part remoting into it.

![Example of a remote and a two part machine where the main (and only) part of machine 1 remotes into the main part of machine 2, and thus has access to all resources of machine 2.](/build/configure/parts-and-remotes/remotes-diagram.png)

## Configuration

### Configure a sub-part

You can make a multi-part machine by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.
Sub-parts will _not_ have access to the resources of the main part.

Use the parts dropdown menu in the top banner of your machine's page on the [Viam app](https://app.viam.com) to add a new sub-part:

![The Viam app interface with the part dropdown open. A new part called 'my-sub-part' is being created.](/build/configure/parts-and-remotes/sub-part-config.png)

To delete a sub-part or make it the main part, use the buttons in the top right of the **Config** tab.

![The config tab of a machine's page noting the location of the Make main part and Delete Part buttons.](/build/configure/parts-and-remotes/part-mgmt.png)

### Configure a remote

To establish a connection between a part of one machine and a part of a second machine, configure a `remote` on the first machine's part.

1. Go to the Viam app machine page of the smart machine part to which you wish to establish the remote connection.
   This is the machine part whose resources will be accessible to the other machine part.
2. Click the **Code sample** tab.
3. On the **Language** toggle, select **Remotes**, then click **Copy**.

   {{% snippet "show-secret.md" %}}

4. Go to the Viam app machine page of the machinene part from which you want to establish a remote connection.
   This is the machine part that will be able to access the resources of the other machine part.
5. Click the **Config** tab, click the **Remotes** subtab, and select **JSON** mode.

   ![The Viam app CONFIG tab with the REMOTES subtab open and JSON mode selected.](/build/configure/parts-and-remotes/remote-json-create.png)

6. Click **Create Remote**.
7. Paste the remote config you copied in step 4 into the empty field.
8. Click **Save Config** in the bottom left of the screen.

## Using remote parts and sub-parts with the Viam SDKs

Once your sub-part or remote part is configured, you can access all the components and services configured on the sub-part or remote machine part as though they were resources of your main machine part.
The only difference is that the names of the components have the remote machine part name prepended to them.
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

For an example that controls a motor that is a component of a sub-part, see [the Mock Robot tutorial](/tutorials/configure/build-a-mock-robot/#control-a-sub-part-using-the-viam-sdk).
