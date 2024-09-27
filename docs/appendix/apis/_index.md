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

## Machine and Fleet APIs

{{< cards >}}
{{% manualcard link="/appendix/apis/fleet/" %}}

#### Fleet Management API

Create and manage organizations, locations, and individual machines, fragments and permissions.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/data-client/" %}}

#### Data Client API

Upload, download, filter, tag or perform other tasks on data like images or sensor readings.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/robot/" %}}

#### Machine Management API

Manage your machines: connect to your machine, retrieve status information, and send commands remotely.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/ml-training-client/" %}}

#### ML Training Client API

Submit and manage ML training jobs running on the Viam app.

{{% /manualcard %}}
{{% manualcard link="/appendix/apis/billing-client/" %}}

#### Billing Client API

Retrieve billing information from the Viam app.

{{% /manualcard %}}

{{< /cards >}}

## Component APIs

These APIs provide interfaces for controlling and getting information from various components of a machine:

{{< cards >}}
{{< relatedcard link="/appendix/apis/components/arm/" >}}
{{< relatedcard link="/appendix/apis/components/base/" >}}
{{< relatedcard link="/appendix/apis/components/board/" >}}
{{< relatedcard link="/appendix/apis/components/camera/" >}}
{{< relatedcard link="/appendix/apis/components/encoder/" >}}
{{< relatedcard link="/appendix/apis/components/gantry/" >}}
{{< relatedcard link="/appendix/apis/components/generic/" >}}
{{< relatedcard link="/appendix/apis/components/gripper/" >}}
{{< relatedcard link="/appendix/apis/components/input-controller/" >}}
{{< relatedcard link="/appendix/apis/components/motor/" >}}
{{< relatedcard link="/appendix/apis/components/movement-sensor/" >}}
{{< relatedcard link="/appendix/apis/components/power-sensor/" >}}
{{< relatedcard link="/appendix/apis/components/sensor/" >}}
{{< relatedcard link="/appendix/apis/components/servo/" >}}
{{< /cards >}}

## Service APIs

These APIs provide interfaces for controlling and getting information from the services you configured on a machine.

{{< cards >}}
{{% relatedcard link="/services/data/api/" %}}
{{% relatedcard link="/services/ml/deploy/api/" alt_title="Machine Learning" %}}
{{% relatedcard link="/services/motion/api/" %}}
{{% relatedcard link="/services/navigation/api/" %}}
{{% relatedcard link="/services/slam/api/" %}}
{{% relatedcard link="/services/vision/api/" %}}
{{< /cards >}}

