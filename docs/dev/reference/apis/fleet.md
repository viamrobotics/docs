---
title: "Manage your fleet with Viam's fleet management API"
linkTitle: "Fleet management"
weight: 20
type: "docs"
description: "Use the fleet management API with Viam's client SDKs to manage your machine fleet with code."
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "cloud management",
    "fleet management",
  ]
aliases:
  - /program/apis/fleet/
  - /dev/reference/apis/fleet/
  - /build/program/apis/fleet/
  - /appendix/apis/fleet/
date: "2024-09-20"
# updated: ""  # When the content was last entirely checked
---

The fleet management API allows you to manage your machine fleet with code the same way you can do in the [web UI](https://app.viam.com/).
With it you can

- create and manage organizations, locations, and individual machines
- manage permissions and authorization
- create and manage fragments

The fleet management API supports the following methods:

{{< readfile "/static/include/app/apis/generated/app-table.md" >}}

## API

{{< readfile "/static/include/app/apis/generated/app.md" >}}

## Find part ID

To copy the ID of your machine {{< glossary_tooltip term_id="part" text="part" >}}, select the part status dropdown to the right of your machine's location and name on the top of its page and click the copy icon next to **Part ID**:

{{<imgproc src="/build/program/data-client/grab-part-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Part ID displayed in the web UI.">}}

## Find machine ID

To copy the ID of your {{< glossary_tooltip term_id="machine" text="machine" >}}, click the **...** (Actions) button in the upper-right corner of your machine's page, then click **Copy machine ID**:

{{<imgproc src="/fleet/app-usage/copy-machine-id.png" resize="1000x" class="shadow imgzoom" style="width: 500px" declaredimensions=true alt="Machine ID in the actions dropdown in the web UI.">}}
