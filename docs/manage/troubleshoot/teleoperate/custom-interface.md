---
title: "Teleoperate with custom control interface"
linkTitle: "Custom interface"
weight: 25
type: "docs"
description: "Use a teleop workspace to create a custom control interface for operating a machine or visualizign and aggregating its data."
tags: ["teleop", "fleet management", "control", "app"]
languages: []
viamresources: ["sensor", "camera", "movement sensor"]
platformarea: ["viz", "data"]
images: ["/how-tos/teleop/full-workspace.png"]
level: "Intermediate"
date: "2024-11-13"
# updated: ""  # When the content was last entirely checked
cost: "0"
prev: "/manage/troubleshoot/alert/"
---

You can remotely operate any configured machine and visualize and aggregate its data using a custom control interface by creating a teleop workspace.

### Prerequisites

{{% expand "A configured machine with teleoperable components" %}}

Make sure your machine has at least one camera, movement sensor, sensor, base, arm, board, gantry, gripper, motor or servo.

See [configure a machine](/operate/get-started/supported-hardware/) for more information.

{{% /expand%}}

### Configure a workspace

{{< table >}}
{{% tablestep start=1 %}}
**Create a workspace**

Log into [Viam](https://app.viam.com/).

Navigate to the **FLEET** page's **TELEOP** tab.
Create a workspace by clicking **+ Create workspace**.
Give it a name.

{{<imgproc src="/how-tos/teleop/blank-workspace.png" resize="800x" style="width: 700px" class="shadow fill imgzoom" declaredimensions=true alt="Blank teleop page.">}}

{{% /tablestep %}}
{{% tablestep %}}
**Add widgets**

Click **Add widget** and select the appropriate widget for your machine.
Use the widget header to configure the panel.
Repeat as many times as necessary.

{{% /tablestep %}}
{{% tablestep %}}
**Select a location and a machine**

Now, select a location and a machine.
This will make your widgets connect to your machine.

Your dashboard now shows the configured widgets for the data from your machine:

{{<imgproc src="/how-tos/teleop/full-workspace.png" resize="800x" style="width: 700px" class="shadow fill imgzoom" declaredimensions=true alt="Teleop workspace with values configured for each of the four widgets on monitor mode.">}}

{{% /tablestep %}}
{{< /table >}}
