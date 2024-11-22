---
title: "Configure a teleop workspace"
linkTitle: "Configure a teleop workspace"
weight: 10
type: "docs"
description: "Create and configure a teleop workspace with widgets."
images: ["/how-tos/teleop/full-workspace.png"]
icon: true
tags: ["teleop", "configuration"]
languages: []
viamresources: ["sensor", "camera", "movement sensor"]
platformarea: ["viz", "data"]
level: "Intermediate"
date: "2024-11-13"
# updated: "2024-08-26"  # When the tutorial was last entirely checked
cost: "0"
---

You can use teleop to create a custom workspace where you can visualize and aggregate data from a machine.
You can currently visualize data from a camera, a sensor, or a movement sensor.

{{% alert title="In this page" color="info" %}}

- [Configure a workspace](#configure-a-workspace)

{{% /alert %}}

## Prerequisites

{{% expand "A configured machine with teleoperable components" %}}

Make sure your machine has at least one of the following:

- A [camera](/components/camera/)
- A [movement sensor](/components/movement-sensor/)
- A [sensor](/components/sensor/)

See [configure a machine](/how-tos/configure/) for more information.

{{% /expand%}}

## Configure a workspace

{{< table >}}
{{% tablestep %}}
**1. Create a workspace in the Viam app**

Log in to the [Viam app](https://app.viam.com/).

Navigate to the **FLEET** page's **TELEOP** tab.
Create a workspace by clicking **+ Create workspace**.
Give it a name.

{{<imgproc src="/how-tos/teleop/blank-workspace.png" resize="800x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Blank teleop page.">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Add widgets**

Click **Add widget** and select the appropriate widget for your machine.
Repeat as many times as necessary.

- If you have a camera, select **Camera stream**, which allows you to view a camera stream.
  Enter the name of your camera.

- If you have a movement sensor, select a **GPS map**, which displays the location of a machine on a map.
  Enter the name of your movement sensor.
  Toggle **Historic positions** to on to see how position has changed over time.

- If you have a sensor, select **Stat** to view a single sensor value.
  Enter the name of the sensor for **Sensor name** and enter the key for the value in **Path**, for example `time_unix`.
  Optionally, add **Units** and give the stat a **Widget title**.

  Then, add that same sensor as a time series graph.
  Click **Add widget** again and select **Time series**, which allows you to graph sensor values over time.
  Enter the name of the sensor for **Sensor name**.
  Give the graph a line title and enter the key for the sensor value in **Path**, for example `time_unix`.
  Add more lines if your sensor measures multiple values.

Now your workspace setup is complete:

{{<imgproc src="/how-tos/teleop/configured-workspace.png" resize="700x" style="width: 500px" class="fill aligncenter" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets.">}}

{{% /tablestep %}}
{{% tablestep %}}
**3. Select a machine**

Now, select a machine with which to make your teleop workspace come to life.
Select **Monitor** in the top right corner to leave editing mode.
Click **Select machine** and select your configured machine.

Your dashboard now shows the configured widgets for the data from your machine:

{{<imgproc src="/how-tos/teleop/full-workspace.png" resize="900x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets on monitor mode.">}}

You can go back to **Edit** mode and drag and drop the widgets' panes around to edit their appearance.
For example:

{{<imgproc src="/how-tos/teleop/four-panes.png" resize="900x" style="width: 500px" class="fill aligncenter imgzoom" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets on monitor mode with four panes.">}}

{{% /tablestep %}}
{{< /table >}}

## Next steps

Follow more of our how-to guides to do more with the Viam platform:

{{< cards >}}
{{% card link="/how-tos/detect-people/" %}}
{{% card link="/how-tos/drive-rover/" %}}
{{% card link="/how-tos/train-deploy-ml/" %}}
{{< /cards >}}
