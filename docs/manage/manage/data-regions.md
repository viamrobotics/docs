---
title: "Choose data region"
linkTitle: "Choose data region"
description: "Configure where in the world Viam stores your cloud data."
weight: 30
type: "docs"
tags: ["data region", "region", "data continent", "compliance", "performance"]
---

When you specify a data region, Viam stores all data captured by your machines in that region.
By default, new organizations store data in North America.
Locations shared across multiple organizations store data in the primary organization region.

## Supported regions

Viam supports the following data regions:

- **North America** (`us-central`):

- **Europe** (`eu-west`):

## Set organization data region

{{< alert title="Caution: You cannot change region if you have already synced data" color="caution" >}}

You must set the region before syncing data.
Once you sync data in an organization, you cannot change the data region.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Open the organization dropdown in the top right of Viam, next to your initials.
1. Click **Settings and invites** to open the organization settings menu.
1. From the **Data region** dropdown, choose the geographic location where you would like to store data.
1. A dialog will appear at the bottom of the screen containing the text **Region updated**.

{{% /tab %}}
{{% tab name="Python" %}}

You can check your organization's data region using [`get_organization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`update_organization`](/dev/reference/apis/fleet/#updateorganization):

{{< read-code-snippet file="/static/include/examples-generated/data-region.snippet.data-region.py" lang="python" class="line-numbers linkable-line-numbers" data-line="34-37" >}}

{{% /tab %}}
{{% tab name="Go" %}}

You can check your organization's data region using [`GetOrganization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`UpdateOrganization`](/dev/reference/apis/fleet/#updateorganization):

{{< read-code-snippet file="/static/include/examples-generated/data-region.snippet.data-region.go" lang="python" class="line-numbers linkable-line-numbers" data-line="36-40" >}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

You can check your organization's data region using [`getOrganization`](/dev/reference/apis/fleet/#getorganization), and set your organization's data region using [`UpdateOrganization`](/dev/reference/apis/fleet/#updateorganization):

{{< read-code-snippet file="/static/include/examples-generated/data-region.snippet.data-region.ts" lang="python" class="line-numbers linkable-line-numbers" data-line="23-28" >}}

{{% /tab %}}
{{< /tabs >}}
