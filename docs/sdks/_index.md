---
title: "SDKs"
linkTitle: "SDKs"
weight: 700
type: "docs"
description: "Program and control your machines in the languages you already know like Python, Go, TypeScript, C++, and Flutter."
no_list: true
---

Viam's SDK libraries wrap the Viam's APIs for interacting with a machine's [components](/build/program/apis/#component-apis) and [services](/build/program/apis/#service-apis), as well as for [cloud capabilities](/build/program/apis/#robot-api), such as [data management](/build/program/apis/#data-client-api) and [fleet management](/build/program/apis/#fleet-management-api).

## Backend SDKs

Use the backend SDK to build business logic to control [components](/build/program/apis/#component-apis) and [services](/build/program/apis/#service-apis), as well as manage your [fleet](/build/program/apis/#fleet-management-api) and [data](/build/program/apis/data-client/), and [billing information](/build/program/apis/billing-client/), or [provision](/fleet/provision/#provision-a-new-machine) machines.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/python/" %}}
{{% sectionlist-custom-item link="/sdks/go/" %}}
{{% sectionlist-custom-item link="/sdks/cpp/" %}}
{{< /sectionlist-custom >}}

## Frontend SDKs

Use the frontend SDK to control your machine's [components](/build/program/apis/#component-apis), as well as manage your [data](/build/program/apis/data-client/) or [provision](/fleet/provision/#provision-a-new-machine) machines.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/typescript/" %}}
{{< /sectionlist-custom >}}

## Mobile SDK

Use the mobile SDK to build iOS and Android apps to control your machine's [components](/build/program/apis/#component-apis), as well as manage your [fleet](/build/program/apis/#fleet-management-api) and [data](/build/program/apis/data-client/), or [provision](/fleet/provision/#provision-a-new-machine) machines.

{{< sectionlist-custom >}}
{{% sectionlist-custom-item link="/sdks/flutter/" %}}
{{< /sectionlist-custom >}}

<br>

For extra guidance and examples, see:

{{< cards >}}
{{% card link="/build/program" customDescription="More guidance on how to use the SDKs." %}}
{{% card link="/build/program/apis" customDescription="Usage examples for each API method." %}}
{{< /cards >}}
