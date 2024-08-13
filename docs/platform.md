---
title: "Platform Reference"
linkTitle: "Platform Reference"
description: "Use Viam to configure, program, operate, manage, and collect data from your smart machines."
weight: 400
type: docs
images: ["/platform/build.svg", "/services/ml/configure.svg"]
carouselscript: true
---

Viam is a complete software platform for {{< glossary_tooltip term_id="smart-machine" text="smart machines">}} that runs on Linux and macOS and supports a wide variety of popular systems, including:

{{< board-carousel >}}
<br>

The open-source executable binary that runs on a Viam-powered {{< glossary_tooltip term_id="machine" text="machine" >}} is called `viam-server`.
`viam-server` runs and manages everything on your machine, including communications between hardware, software, and the cloud.

## What a machine is in Viam

A machine is any computer (SBC, server, or microcontroller) running [`viam-server`](/architecture/#viam-server-and-the-micro-rdk) (or the micro-RDK in the case of a microcontroller), plus any hardware attached to that computer.

## How machines are structured, configured and organized

Learn more about the structure and configuration of machines:

|                        | Structure...                            | Configuration...                     |
| ---------------------- | --------------------------------------- | ------------------------------------ |
| ...of one machine ->   | [Architecture](/architecture/)          | [Machine Configuration](/configure/) |
| ...of many machines -> | [Cloud Organization Hierarchy](/cloud/) | [Deploy a Large Fleet](/fleet/)      |

{{< cards >}}
{{% card link="/architecture/" %}}
{{% card link="/configure/" %}}
{{% card link="/cloud/" %}}
{{% card link="/fleet/" %}}
{{< /cards >}}

## The things that make up a machine

On your machine, you configure components and services.
Some are built-in, and many more are available in the registry.
You can also write your own and add them to the registry.

In addition to modular components and services, the registry contains ML models.

{{< cards >}}
{{% card link="/components/" %}}
{{% card link="/services/" %}}
{{% card link="/registry/" %}}
{{< /cards >}}

## Ways to control a machine

You can control your machine using the SDKs that call standardized API endpoints for each component and service.
You can also use your machine's [Viam app](https://app.viam.com) **CONTROL** tab that uses those same endpoints, or you can use the CLI.

{{< cards >}}
{{% card link="/sdks/" %}}
{{% card link="/cli/" %}}
{{< /cards >}}

## Deeper details

{{< cards >}}
{{% card link="/internals/" %}}
{{< /cards >}}
