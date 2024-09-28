---
title: "Interact with Resources with Viam's Client SDKs"
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
{{< card link="/appendix/apis/components/arm/" noimage="True" >}}
{{< card link="/appendix/apis/components/base/" noimage="True" >}}
{{< card link="/appendix/apis/components/board/" noimage="True" >}}
{{< card link="/appendix/apis/components/camera/" noimage="True" >}}
{{< card link="/appendix/apis/components/encoder/" noimage="True" >}}
{{< card link="/appendix/apis/components/gantry/" noimage="True" >}}
{{< card link="/appendix/apis/components/generic/" noimage="True" >}}
{{< card link="/appendix/apis/components/gripper/" noimage="True" >}}
{{< card link="/appendix/apis/components/input-controller/" noimage="True" >}}
{{< card link="/appendix/apis/components/motor/" noimage="True" >}}
{{< card link="/appendix/apis/components/movement-sensor/" noimage="True" >}}
{{< card link="/appendix/apis/components/power-sensor/" noimage="True" >}}
{{< card link="/appendix/apis/components/sensor/" noimage="True" >}}
{{< card link="/appendix/apis/components/servo/" noimage="True" >}}
{{< /cards >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a machine.

<!-- TODO: move to APIS folder and change links -->

{{< cards >}}
{{% card link="/services/data/" noimage="True" %}}
{{% card link="/services/ml/deploy/" customTitle="Machine Learning" noimage="True" %}}
{{% card link="/services/motion/" noimage="True" %}}
{{% card link="/services/navigation/" noimage="True" %}}
{{% card link="/services/slam/" noimage="True" %}}
{{% card link="/services/vision/" noimage="True" %}}
{{< /cards >}}
