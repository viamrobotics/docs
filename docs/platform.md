---
title: "Platform Reference"
linkTitle: "Platform Reference"
description: "Use Viam to configure, program, operate, manage, and collect data from your smart machines."
weight: 400
type: docs
images: ["/platform/build.svg", "/services/ml/configure.svg"]
carouselscript: true
---

Viam is a complete software platform for {{< glossary_tooltip term_id="smart-machine" text="smart machines">}} that runs on **any 64bit Linux or macOS**, supporting a wide variety of popular systems, including:
{{< board-carousel >}}
<br>

The open-source executable binary that runs on a Viam-powered {{< glossary_tooltip term_id="machine" text="machine" >}} is called `viam-server`.
`viam-server` runs and manages everything on your machine, including communications between hardware, software, and the cloud.

## What a machine is

A {{< glossary_tooltip term_id="machine" text="machine" >}} is any computer (SBC, server) running [`viam-server`](/architecture/#viam-server-and-viam-micro-server) or any microcontroller running `viam-micro-server`, plus any hardware attached to that computer.

## How machines are structured, configured and organized

Learn more about the structure and configuration of machines:

|                        | Structure...                            | Configuration...                     |
| ---------------------- | --------------------------------------- | ------------------------------------ |
| ...of one machine ->   | [Architecture](/architecture/)          | [Machine Configuration](/configure/) |
| ...of many machines -> | [Cloud Organization Hierarchy](/cloud/) | [Deploy a Large Fleet](/fleet/)      |

## The things that make up a machine

On your machine, you configure [components](/components/) and [services](/services/).
Some are built-in, and many more are available in the [registry](/registry/).
You can also write your own and add them to the registry.

You can configure the following components:
{{< cards >}}
{{% relatedcard link="/components/arm" %}}
{{% relatedcard link="/components/base" %}}
{{% relatedcard link="/components/board" %}}
{{% relatedcard link="/components/camera" %}}
{{% relatedcard link="/components/encoder" %}}
{{% relatedcard link="/components/gantry" %}}
{{% relatedcard link="/components/generic" %}}
{{% relatedcard link="/components/gripper" %}}
{{% relatedcard link="/components/input-controller" %}}
{{% relatedcard link="/components/motor" %}}
{{% relatedcard link="/components/movement-sensor" %}}
{{% relatedcard link="/components/power-sensor" %}}
{{% relatedcard link="/components/sensor" %}}
{{% relatedcard link="/components/servo" %}}
{{< /cards >}}
And you can use the following platform capabilities and services to make your machines smarter and better:
{{< cards >}}
{{% relatedcard link="/services/data" %}}
{{% relatedcard link="/services/ml/deploy" alt_title="Machine Learning" %}}
{{% relatedcard link="/services/motion" %}}
{{% relatedcard link="/services/navigation" %}}
{{% relatedcard link="/services/slam" %}}
{{% relatedcard link="/services/vision" %}}
{{< /cards >}}

## Ways to control a machine

You can control your machine using the SDKs that call standardized API endpoints for each component and service.
You can also use your machine's [Viam app](https://app.viam.com) **CONTROL** tab that uses those same endpoints, or you can use the CLI.

{{< cards >}}
{{% card link="/sdks/" %}}
{{% card link="/cli/" %}}
{{% card link="/fleet/control/" %}}
{{< /cards >}}

## Deeper details

{{< cards >}}
{{% card link="/internals/" %}}
{{< /cards >}}
