---
title: "Discovery Service"
linkTitle: "Discovery"
description: "The discovery service is used to discover resources on a robot."
type: docs
weight: 50
no_list: true
#icon: true
#images: ["/services/icons/discovery.svg"]
tags: ["discovery", "services"]
no_service: true
date: "2025-03-03"
# updated: ""  # When the content was last entirely checked
# SMEs: John N.
modulescript: true
---

The discovery service is used to discover resources on a robot.
If you are [creating a modular resource](/operate/get-started/other-hardware/) that depends on other resources, you can create a discovery service as part of your module to discover those resources if they are discoverable in a systematic way.

For example, if you are creating a vision service module that depends on a camera, you can include both a vision service and a discovery service in your module to discover the camera.
Users can then:

1. Configure the discovery service in their machine's configuration.
1. Use it to discover any cameras that are connected to the machine.
1. Use one of the discovered cameras in their vision service configuration.

Or, using the discovery service API, you can discover resources on a robot programmatically.

## Configuration

To use a discovery service, you need to add it to your machine's configuration.

Go to your machine's **CONFIGURE** page, and add your discovery service.

The following list shows the available discovery service models.
For additional configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:service:discovery" type="discovery" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="Micro-RDK" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component compatible with the Micro-RDK.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## API

The [discovery service API](/dev/reference/apis/services/discovery/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/discovery-table.md" >}}
