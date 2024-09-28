---
title: "Viam's Client APIs"
linkTitle: "APIs"
weight: 20
type: "docs"
description: "Access and control your machine or fleet with the SDKs' client libraries for the resource and robot APIs."
icon: true
images: ["/services/icons/sdk.svg"]
tags: ["client", "sdk", "viam-server", "networking", "apis", "robot api"]
aliases:
  - /program/sdks/
  - /program/apis/
  - /build/program/apis/
no_list: true
---

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API) described through [protocol buffers](https://developers.google.com/protocol-buffers).

The API methods provided by the SDKs for each of these resource APIs wrap gRPC client requests to the machine when you execute your program, providing you a convenient interface for accessing information about and controlling the {{< glossary_tooltip term_id="resource" text="resources" >}} you have [configured](/configure/) on your machine.

## Machine and fleet APIs

{{< cards >}}
{{% manualcard link="/appendix/apis/fleet/" title="Fleet Management API" %}}

Create and manage organizations, locations, and individual machines, fragments and permissions.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/data-client/" title="Data Client API" %}}

Upload, download, filter, tag or perform other tasks on data like images or sensor readings.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/robot/" title="Machine Management API" %}}

Manage your machines: connect to your machine, retrieve status information, and send commands remotely.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/ml-training-client/" title="ML Training Client API" %}}

Submit and manage ML training jobs running on the Viam app.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/billing-client/" title="Billing Client API" %}}

Retrieve billing information from the Viam app.

{{% /manualcard %}}

{{< /cards >}}

## Component APIs

These APIs provide interfaces for controlling and getting information from various components of a machine:

{{< cards >}}
{{< card link="/appendix/apis/components/arm/" customTitle="Arm API" noimage="True" >}}
{{< card link="/appendix/apis/components/base/" customTitle="Base API" noimage="True" >}}
{{< card link="/appendix/apis/components/board/" customTitle="Board API" noimage="True" >}}
{{< card link="/appendix/apis/components/camera/" customTitle="Camera API" noimage="True" >}}
{{< card link="/appendix/apis/components/encoder/" customTitle="Encoder API" noimage="True" >}}
{{< card link="/appendix/apis/components/gantry/" customTitle="Gantry API" noimage="True" >}}
{{< card link="/appendix/apis/components/generic/" customTitle="Generic API" noimage="True" >}}
{{< card link="/appendix/apis/components/gripper/" customTitle="Gripper API" noimage="True" >}}
{{< card link="/appendix/apis/components/input-controller/" customTitle="Input controller API" noimage="True" >}}
{{< card link="/appendix/apis/components/motor/" customTitle="Motor API" noimage="True" >}}
{{< card link="/appendix/apis/components/movement-sensor/" customTitle="Movement sensor API" noimage="True" >}}
{{< card link="/appendix/apis/components/power-sensor/" customTitle="Power sensor API" noimage="True" >}}
{{< card link="/appendix/apis/components/sensor/" customTitle="Sensor API" noimage="True" >}}
{{< card link="/appendix/apis/components/servo/" customTitle="Servo API" noimage="True" >}}
{{< /cards >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a machine.

<!-- TODO: move to APIS folder and change links -->

{{< cards >}}
{{% card link="/services/data/" customTitle="Data management service API" noimage="True" %}}
{{% card link="/services/ml/deploy/" customTitle="ML service API" noimage="True" %}}
{{% card link="/services/motion/" customTitle="Motion service API" noimage="True" %}}
{{% card link="/services/navigation/" customTitle="Navigation service API" noimage="True" %}}
{{% card link="/services/slam/" customTitle="SLAM service API" noimage="True" %}}
{{% card link="/services/vision/" customTitle="Vision service API" noimage="True" %}}
{{< /cards >}}
