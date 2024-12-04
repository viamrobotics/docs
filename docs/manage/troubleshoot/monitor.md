---
linkTitle: "Monitor machine status"
title: "Monitor machine status"
weight: 10
layout: "docs"
type: "docs"
no_list: true
description: "Monitor the status of all machines in an organization and investigate issues when needed."
---

You can view all machines in an organization from a dashboard and access each machine from it.

{{< table >}}
{{% tablestep %}}
**1. Monitor your fleet's parts statuses and synced data**

You can monitor your machines from your **FLEET**'s [**ALL MACHINES DASHBOARD** subtab](https://app.viam.com/fleet/machines).

{{< imgproc src="/fleet/dashboard.png" alt="Fleet dashboard showing the machine parts, location, status, architecture and more" resize="1200x" class="imgzoom aligncenter" >}}

You can also monitor the amount of binary and tabular data your fleet has synced in the last 48 hours from the **FLEET**'s [**DASHBOARD** subtab](https://app.viam.com/fleet/dashboard).

{{<imgproc src="how-tos/manage-fleet/dashboard.png" resize="500x" declaredimensions=true alt="Fleet dashboard showing the machine parts and data sync overview">}}

{{% /tablestep %}}
{{% tablestep %}}
**2. Investigate machine status**

If you click on a machine part, you can get more information about the machine.
At the top of the machine page, there is an indicator of the machine's status.
Click on the **status** dropdown to open a menu with information about each {{< glossary_tooltip term_id="part" text="part" >}} of your machine.
Once you connect to the `viam-server` instance on a part, this display includes its OS, Host, `viam-server` version, IP addresses, and what time it was last online or remote address (if live):

![The machine page with part menu expanded](/fleet/app-usage/machine-page.png)

{{% /tablestep %}}
{{% tablestep link="/fleet/control/" %}}
**3. Test your machines remotely**

On a machine's [**CONTROL** tab](/fleet/control/), you can remotely operate the machine and test its resources.

{{<gif webm_src="/fleet/control.webm" mp4_src="/fleet/control.mp4" alt="Using the control tab" max-width="800px">}}

{{% /tablestep %}}
{{< /table >}}
