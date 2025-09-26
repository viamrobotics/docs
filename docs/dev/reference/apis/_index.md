---
title: "Viam's Client APIs"
linkTitle: "APIs"
weight: 10
type: "docs"
description: "Access and control your machine or fleet with the SDKs' client libraries for the resource and robot APIs."
images: ["/general/code.png"]
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - /program/sdks/
  - /program/apis/
  - /build/program/apis/
  - /appendix/apis/
no_list: true
date: "2024-10-01"
# updated: ""  # When the content was last entirely checked
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [application programming interface (API)](https://en.wikipedia.org/wiki/API) described through [protocol buffers](https://developers.google.com/protocol-buffers).

The API methods provided by the SDKs for each of these resource APIs wrap gRPC client requests to the machine when you execute your program, providing you a convenient interface for accessing information about and controlling the {{< glossary_tooltip term_id="resource" text="resources" >}} you have [configured](/operate/modules/supported-hardware/) on your machine.

## Platform APIs

{{< cards >}}
{{% manualcard link="/dev/reference/apis/fleet/" title="Fleet Management API" %}}

Create and manage organizations, locations, and machines, get logs from individual machines, and manage fragments and permissions.

{{% /manualcard %}}
{{% manualcard link="/dev/reference/apis/data-client/" title="Data Client API" %}}

Upload, download, filter, tag or perform other tasks on data like images or sensor readings.

{{% /manualcard %}}
{{% manualcard link="/dev/reference/apis/robot/" title="Machine Management API" %}}

Manage your machines: connect to your machine, retrieve status information, and send commands remotely.

{{% /manualcard %}}
{{% manualcard link="/dev/reference/apis/ml-training-client/" title="ML Training Client API" %}}

Submit and manage ML training jobs running on Viam.

{{% /manualcard %}}
{{% manualcard link="/dev/reference/apis/billing-client/" title="Billing Client API" %}}

Retrieve billing information from Viam.

{{% /manualcard %}}

{{< /cards >}}

## Component APIs

These APIs provide interfaces for controlling and getting information from the {{< glossary_tooltip term_id="component" text="components" >}} of a machine:

{{< cards >}}
{{< card link="/dev/reference/apis/components/arm/" customTitle="Arm API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/base/" customTitle="Base API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/board/" customTitle="Board API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/button/" customTitle="Button API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/encoder/" customTitle="Encoder API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/gantry/" customTitle="Gantry API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/generic/" customTitle="Generic API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/gripper/" customTitle="Gripper API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/input-controller/" customTitle="Input controller API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/motor/" customTitle="Motor API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/power-sensor/" customTitle="Power sensor API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/sensor/" customTitle="Sensor API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/servo/" customTitle="Servo API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/switch/" customTitle="Switch API" noimage="True" >}}
{{< /cards >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a machine.

{{< cards >}}
{{% card link="/dev/reference/apis/services/data/" customTitle="Data management service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/vision/" customTitle="Vision service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/ml/" customTitle="ML model service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/motion/" customTitle="Motion service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/navigation/" customTitle="Navigation service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/generic/" customTitle="Generic service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/slam/" customTitle="SLAM service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/base-rc/" customTitle="Base Remote Control service API" noimage="True" %}}
{{% card link="/dev/reference/apis/services/discovery/" customTitle="Discovery service API" noimage="True" %}}
{{< /cards >}}
