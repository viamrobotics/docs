---
title: "Machine Architecture: Parts"
linkTitle: "Machine Architecture"
weight: 40
type: "docs"
description: "Connect multiple machine parts to each other as sub-parts or remotes."
tags: ["server", "components", "services"]
aliases:
  - /manage/parts-and-remotes/
  - /build/configure/parts-and-remotes/
---

When {{< glossary_tooltip term_id="machine" text="smart machines" >}} communicate with each other, they can share resources and operate collaboratively.
This document explains how to establish secure connections between machines.

### Machine parts

Machines are organized into _parts_, where each part represents a computer (a single-board computer, desktop, laptop, or other computer) running [`viam-server`](/get-started/installation/), the hardware [components](/components/) attached to it, and any [services](/services/) or other resources running on it.

Every smart machine has a main part which is automatically created when you create the machine.
Multi-part machines also have one or more _sub-parts_ representing additional computers running `viam-server`.

There are two ways to link machine parts:

- **Sub-part**: If you have two computers within the _same machine_, use one as the main part and [connect the other to it as a sub-part](#configure-a-sub-part).

- **Remote part**: To connect two computers that are parts of _different machines_, [add one machine part as a remote part of the other machine](#configure-a-remote-part).

Connections between machines are established using the best network path available.

When you configure a remote part or a sub-part, the main machine part can access all the components and services configured on the remote machine part as though they were entities of the main machine part.
This is a one-way connection: the main machine part can access the resources of the remote machine part, but the remote machine cannot access the resources of the machine part remoting into it.

![Example of a remote and a two part machine where the main (and only) part of machine 1 remotes into the main part of machine 2, and thus has access to all resources of machine 2.](/build/configure/parts/remotes-diagram.png)

## Configuration

### Configure a sub-part

You can make a multi-part machine by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.
Sub-parts will _not_ have access to the resources of the main part.

The Viam app automatically creates the main part for you when you create a new {{< glossary_tooltip term_id="machine" text="machine" >}}.
To add a new sub-part:

1. Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
2. Click the **+** (Create) icon next to the name of your main part, then click **Sub-part** from the menu:

   {{<imgproc src="/build/configure/parts/sub-part-config.png" resize="x1100" declaredimensions=true alt="The Viam app interface with the create part dropdown open." style="max-width:500px" >}}

To rename or delete a sub-part, or to make it the main part, click the **...** icon to open the Actions menu:

{{<imgproc src="/build/configure/parts/part-mgmt.png" resize="x1100" declaredimensions=true alt="The Viam app interface with the part actions dropdown open. Options include rename, restart part, make main part, view setup instructions, view history, and delete part." style="max-width:500px" >}}

### Configure a remote part

To establish a connection between a part of one machine and a part of a second machine, add one as a remote part in the other machine part's config:

1. Go to the Viam app machine page of the smart machine part to which you wish to establish the remote connection.
   This is the machine part whose resources will be accessible to the other machine part.
2. Navigate to the **CONNECT** tab.
3. Click **Configure as a remote part** in the left-hand menu.
4. Toggle the **Include secret** switch on, then copy the entire JSON snippet including the name, address, and authentication credentials of the remote part.

   {{% snippet "show-secret.md" %}}

5. Go to the Viam app machine page of the machine part from which you want to establish a remote connection.
   This is the machine part that will be able to access the resources of the other machine part.
6. Navigate to the **CONFIGURE** tab, click the **+** (Create) icon next to the machine part's name in the left side menu.

   {{<imgproc src="/build/configure/parts/remote-create.png" resize="x1100" declaredimensions=true alt="The create menu with options including remote part shown." style="max-width:500px" >}}

7. Click **Remote part**.
8. Find the newly-created remote part in the left hand menu.
   Click it to navigate to its configuration card.
9. Delete the auto-populated JSON from the new remote's config area and replace it by pasting the remote config you copied in step 4 into the empty field.

   {{<imgproc src="/build/configure/parts/remote-config.png" resize="x1100" declaredimensions=true alt="The configured remote." style="max-width:700px" >}}

10. Save the config.

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
