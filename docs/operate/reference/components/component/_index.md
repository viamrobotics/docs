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

## Configuration

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
{{< relatedcard link="/operate/mobility/define-geometry/" >}}
{{< /cards >}}

## API

The [COMPONENT API](/dev/reference/apis/components/encoder/) supports the following methods:

_Writing Instructions: Use the method names in the [protobuf](https://github.com/viamrobotics/api/blob/main/component/board/v1/board_grpc.pb.go), not the Python or Go-specific method names._
_Use an included snippet so you can add it to <file>/program/apis/</file>._

{{< readfile "/static/include/components/apis/component.md" >}}

## Troubleshooting

If your COMPONENT is not working as expected, follow these steps:

1. Check your machine logs on the **LOGS** tab to check for errors.
2. Review your COMPONENT model's documentation to ensure you have configured all required attributes.
3. Click on the **TEST** panel on the **CONFIGURE** or **CONTROL** tab and test if you can use the COMPONENT there.

If none of these steps work, reach out to us on the [Community Discord](https://discord.gg/viam) and we will be happy to help.

## Next steps

To get started using your COMPONENT, see the [COMPONENT API](/dev/reference/apis/components/camera/) or check out one of these guides:

<!-- ADD CARDS -->
