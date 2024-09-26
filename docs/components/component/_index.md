---
title: "Template Component"
linkTitle: "Template"
childTitleEndOverwrite: "Template Component"
weight: 10
type: "docs"
description: "A NAME is a ... description of what the component is."
tags: ["camera", "components"]
icon: true # this should be used when the image is an icon, it will adjust the sizing and object-fit
images: ["/icons/components.png"]
draft: true
no_list: true
modulescript: true
# SMEs:
---

{{<imgproc src="/icons/components.png" resize="400x" declaredimensions=true alt="ALT" class="alignright">}}

Brief description of the component and what you can do with it.

Use cases (optional):

- A brief description of one sample use case.
- ...

Most machines with a COMPONENT need at least the following hardware (optional):

- Board
- ...

## Available models

To use your <COMPONENT> component, check whether one of the following models supports it.

For configuration information, click on the model name:

{{< tabs >}}
{{% tab name="viam-server" %}}

{{<resources api="rdk:component:component" type="component" no-intro="true">}}

{{< readfile "/static/include/create-your-own-mr.md" >}}

{{% /tab %}}
{{% tab name="viam-micro-server" %}}

{{< alert title="Support Notice" color="note" >}}

There is currently no support for this component in `viam-micro-server`.

{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

## Related services

Add services commonly used with the component.

{{< cards >}}
{{< relatedcard link="/services/data/" >}}
{{< relatedcard link="/services/frame-system/" >}}
{{< /cards >}}

## API

To get started using your COMPONENT, see the [COMPONENT API](/appendix/apis/components/encoder/), which supports the following methods:

_Writing Instructions: Use the method names in the [protobuf](https://github.com/viamrobotics/api/blob/main/component/board/v1/board_grpc.pb.go), not the Python or Go-specific method names._
_Use an included snippet so you can add it to <file>/program/apis/</file>._

{{< readfile "/static/include/components/apis/component.md" >}}

## Troubleshooting

Troubleshooting information for configuration errors.

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

{{< snippet "social.md" >}}

## Next steps

To get started using your COMPONENT, see the [COMPONENT API](/appendix/apis/components/camera/) or check out one of these guides:

<!-- ADD CARDS -->