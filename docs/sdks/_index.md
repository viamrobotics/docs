---
title: "SDKs"
linkTitle: "SDKs"
weight: 650
type: "docs"
description: "Program and control your machines in the languages you already know like Python, Go, TypeScript, C++, and Flutter."
no_list: true
menuindent: true
---

Viam's SDK libraries wrap the Viam's APIs for interacting with a machine's [components](/appendix/apis/#component-apis) and [services](/appendix/apis/#service-apis), as well as for [cloud capabilities](/appendix/apis/#robot-api), such as [data management](/appendix/apis/#data-client-api) and [fleet management](/appendix/apis/#fleet-management-api).
You can run SDK code from anywhere, it does not necessarily have to be run on the same machine that runs `viam-server`.

## Backend SDKs

Use the backend SDK to build business logic to control [components](/appendix/apis/#component-apis) and [services](/appendix/apis/#service-apis), as well as manage your [fleet](/appendix/apis/#fleet-management-api) and [data](/appendix/apis/data-client/), and [billing information](/appendix/apis/billing-client/), or [provision](/fleet/provision/#provision-a-new-machine) machines.
With the backend SDKs you can also create custom {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/python/" %}}
{{% sectionlist-custom-item link="/sdks/go/" %}}
{{% sectionlist-custom-item link="/sdks/cpp/" %}}
{{< /sectionlist-custom >}}

## Frontend SDKs

Use the frontend SDK to control your machine's [components](/appendix/apis/#component-apis), as well as manage your [data](/appendix/apis/data-client/) or [provision](/fleet/provision/#provision-a-new-machine) machines.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/typescript/" %}}
{{< /sectionlist-custom >}}

## Mobile SDK

Use the mobile SDK to build iOS and Android apps to control your machine's [components](/appendix/apis/#component-apis), as well as manage your [fleet](/appendix/apis/#fleet-management-api) and [data](/appendix/apis/data-client/), or [provision](/fleet/provision/#provision-a-new-machine) machines.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/flutter/" %}}
{{< /sectionlist-custom >}}

<br>

For extra guidance and examples, see:

{{< cards >}}
{{% card link="/build/program" customDescription="More guidance on how to use the SDKs." %}}
{{% card link="/appendix/apis" customDescription="Usage examples for each API method." %}}
{{< /cards >}}
