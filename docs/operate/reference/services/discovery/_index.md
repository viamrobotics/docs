---
title: "Discovery Service"
linkTitle: "Discovery"
description: "Use a discovery service to discover available resources on a machine."
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

A discovery service allows you to return a list of physical hardware available on a machine, and suggest configurations for those components to integrate the hardware into the machine.
If you are [creating a modular resource](/operate/modules/create-module/) that depends on other {{< glossary_tooltip term_id="resource" text="resources" >}} that are discoverable in a systematic way, you can create a discovery service as part of your module to discover those resources.

## Example usage

Imagine you are creating a vision service module that depends on a camera.
To make it easier for users to configure the camera, you include a discovery service in your module.
You implement the discovery service to report all the camera paths your computer or SBC finds.
Users of your module can then:

1. Configure both the vision service and the discovery service in their machine's configuration.
1. Click the **Test** panel in the discovery service configuration to see all cameras recognized by the machine, presented as a list of configuration snippets.
1. Create a camera with the copy-pasteable configuration snippet for the camera they want to use, with the camera path already filled in.
1. Use the configured camera in their vision service configuration.

To see this in action, see [webcam discovery](/operate/reference/components/camera/webcam/#find-a-video-path-using-a-discovery-service) as an example.

To interact with a discovery service programmatically, use the [discovery service API](/dev/reference/apis/services/discovery/).

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
