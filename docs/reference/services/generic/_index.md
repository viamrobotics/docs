---
title: "Generic service"
linkTitle: "Generic"
weight: 500
layout: "docs"
type: "docs"
description: "A service that does not fit any of the other APIs."
modulescript: true
date: "2026-04-18"
aliases:
  - "/operate/reference/services/generic/"
  - /registry/advanced/generic/
---

The _generic_ service API enables you to add support for unique types of services that do not already have an [appropriate API](/reference/apis/#service-apis) defined for them.

For example, when writing code to manage simultaneous localization and mapping (SLAM) for your machine, it makes sense to use the existing SLAM API, which provides specific functionality required for generating accurate maps of an environment.
However, if you want to create a new service to monitor your machine's CPU and RAM usage for example, you need very different functionality that isn't currently exposed in any API.
Instead, you can use the generic service API to add support for your unique type of service, like local system monitoring, to your machine.

Use generic for a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} model that represents a unique type of service.
If you are adding support for unique or proprietary hardware, rather than adding new high-level software functionality, use the [generic component](/reference/components/generic/) instead.

There are no built-in generic service models (other than `fake`).

{{% alert title="Important" color="note" %}}

The generic service API only supports the `DoCommand` method.
If you use the generic API, your module needs to define any and all service functionality and pass it through `DoCommand`.

Whenever possible, it is best to use an [existing service API](/reference/apis/services/) instead of generic so that you do not have to replicate code.
If you want to use most of an existing API but need just a few other functions, try using the `DoCommand` endpoint and extra parameters to add custom functionality to an existing API, instead of using the generic service.

{{% /alert %}}

## Configuration

{{<resources_svc api="rdk:service:generic" type="generic">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

## API

The [generic service API](/reference/apis/services/generic/) supports the following method:

{{< readfile "/static/include/services/apis/generated/generic_service-table.md" >}}

## Troubleshooting

You can find additional assistance in the [Troubleshooting section](/monitor/troubleshoot/).

{{< snippet "social.md" >}}
