---
title: "Machine architecture: Parts"
linkTitle: "Parts, sub-parts, remotes"
weight: 40
type: "docs"
description: "Connect multiple machine parts to each other as sub-parts or remotes."
tags: ["server", "components", "services"]
aliases:
  - /manage/parts-and-remotes/
  - /build/configure/parts-and-remotes/
  - /configure/parts/
  - /build/configure/parts/
  - /architecture/parts/
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
---

When {{< glossary_tooltip term_id="machine" text="smart machines" >}} communicate with each other, they can share resources and operate collaboratively.
This document explains how to establish secure connections between machines.

## Machine parts

Machines are organized into _parts_, where each part represents a computer (a single-board computer, desktop, laptop, or other computer) running [`viam-server`](/operate/reference/viam-server/), the hardware {{< glossary_tooltip term_id="component" text="components" >}} attached to it, and any {{< glossary_tooltip term_id="service" text="services" >}} or other {{< glossary_tooltip term_id="resource" text="resources" >}} running on it.

Every smart machine has a main part which is automatically created when you create the machine.
Multi-part machines also have one or more _sub-parts_ representing additional computers running `viam-server`.

There are two ways to link machine parts:

- **Sub-part**: If you have multiple computers within the _same machine_, use one as the main part and [connect each additional part to it as a sub-part](#configure-a-sub-part).
  Any given part can only be a sub-part of one main part.

  <details>
    <summary>Click for an example.</summary>
   Imagine you have a system of five cameras in different places along an assembly line, each attached to its own single-board computer, and you want to run an object detector on the streams from all of them.
   You have one main computer with greater compute power set up as the main part.
   You set up each of the single-board computers as a sub-part.
   This allows the main part to access all the camera streams and run object detection on all of them.<br><br>
   You could also set this up with each single-board computer being a remote part instead of a sub-part, but it is slightly easier to configure sub-parts because you do not need to add the address of each part to your machine's config.
   Additionally, configuring a discrete system of parts as one multi-part machine helps keep your fleet more clearly organized.
  </details><br>

- **Remote part**: To connect multiple computers that are parts of _different machines_ in the same or different organizations, [add one machine part as a remote part of the other machine or machines](#configure-a-remote-part).
  A part can be a remote part of any number of other parts.

  <details>
    <summary>Click for an example.</summary>
    If you have one camera connected to a computer in a warehouse that many machines should be able to share, you can configure the camera as a remote part of each machine that needs it.
  </details>

Connections between machines are established using the best network path available.

When you configure a remote part or a sub-part, the main machine part can access all the components and services configured on the remote machine part as though they were entities of the main machine part.
This is a one-way connection: the main machine part can access the resources of the remote machine part, but the remote machine cannot access the resources of the machine part remoting into it.

When a part starts up, it attempts to connect to any remotes and sub-parts.
If it cannot connect to them, the part will still successfully start up.

![Example of a remote and a two part machine where the main (and only) part of machine 1 remotes into the main part of machine 2, and thus has access to all resources of machine 2.](/build/configure/parts/remotes-diagram.png)

### Find part ID

To copy the ID of your machine part, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**.

For example:

{{<imgproc src="/build/program/data-client/grab-part-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Part ID displayed.">}}

## Configuration

### Configure a sub-part

You can make a multi-part machine by first configuring one part which is the "main" part, and then configuring one or more sub-parts.
The main part will be able to access the resources of its sub-parts.
Sub-parts will _not_ have access to the resources of the main part.

Viam automatically creates the main part for you when you create a new {{< glossary_tooltip term_id="machine" text="machine" >}}.
To add a new sub-part:

1. Navigate to the **CONFIGURE** tab of your machine's page.
2. Click the **+** (Create) icon next to the name of your main part, then click **Sub-part** from the menu:

   {{<imgproc src="/build/configure/parts/sub-part-config.png" resize="x1100" declaredimensions=true alt="The create part dropdown open." style="width:500px" class="shadow" >}}

3. Save the config.

{{% hiddencontent %}}
The sub-part will not be visible as a `remote` in the debug config until after you use the setup instructions to make the sub-part go live.
{{% /hiddencontent %}}

To rename or delete a sub-part, or to make it the main part, click the **...** menu:

{{<imgproc src="/build/configure/parts/part-mgmt.png" resize="x1100" declaredimensions=true alt="The part actions dropdown open. Options include rename, restart part, make main part, view setup instructions, view history, and delete part." style="width:500px" class="shadow" >}}

By default, all sub-parts appear in the [frame system](/operate/reference/services/frame-system/) at the world origin.
You can specify translations for sub-parts by configuring their frames with appropriate translation values relative to their parent frame.
You can view the `frame` of each sub-part in the `remotes` section of the debug config.

### Configure a remote part

To establish a connection between a part of one machine and a part of a second machine, add one as a remote part in the other machine part's config:

1. Go to the machine page of the machine part from which you want to establish a remote connection.
   This is the machine part that will be able to access the resources of the other machine part.
1. Navigate to the **CONFIGURE** tab, click the **+** (Create) icon next to the machine part's name in the left side menu.

   {{<imgproc src="/build/configure/parts/remote-create.png" resize="x1100" declaredimensions=true alt="The create menu with options including remote part shown." style="width:500px" class="shadow" >}}

1. Click **Remote part**.
1. Select the remote part from the list of parts.

   Alternatively, click **Add empty remote** and then scroll to the newly-created remote part configuration card.
   Click on **{}** (Switch to advanced) and replace the JSON object with a remote config.

   {{<imgproc src="/build/configure/parts/remote-config.png" resize="x1100" declaredimensions=true alt="The configured remote." style="width:700px" class="shadow" >}}

   {{< expand "Click to see how to get a remote config object" >}}

1. Go to the machine page of the smart machine part to which you wish to establish the remote connection.
   This is the machine part whose resources will be accessible to the other machine part.
1. Navigate to the **CONNECT** tab.
1. Click **Configure as a remote part** in the left-hand menu.
1. Toggle the **Include API key** switch on, then copy the entire JSON snippet including the name, address, and authentication credentials of the remote part.

   {{% snippet "show-secret.md" %}}

   {{< /expand >}}

   Remotes have the following parameters:

   <!-- prettier-ignore -->
   | Name               | Type   | Required? | Description |
   | ------------------ | ------ | --------- | ----------- |
   | `name` |  string | Optional | The name of the remote part. |
   | `address` |  string | Optional | The address of the remote part. |
   | `auth` | string | Object | The authentication credentials of the remote part. For example: `{ "credential": { "type": "api-key", "payload": "abcdefghijklmnop123456789abcdefg" } }`. |
   | `prefix` | string | Optional | If set, all resource names fetched from the remote part will have the prefix. |

1. Click **Save** in the upper right corner of the page to save your config.

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
