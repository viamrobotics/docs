---
title: "Add custom metadata"
linkTitle: "Add custom metadata"
weight: 60
type: "docs"
description: "Add custom metadata as a JSON object to machine parts, machines, locations, and organizations."
date: "2025-11-14"
# updated: ""  # When the tutorial was last entirely checked
---

To store metadata for a machine part, machine, or location you can add custom metadata in the UI or using the Viam SDKs.
You can also add custom metadata for organizations using the Viam SDKs.

## Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

## Add and update custom machine part metadata

{{< tabs >}}
{{% tab name="Web UI" %}}

1. On a machine page, click on the **...** menu next to the machine part.
1. Select **Custom part metadata**.
1. Add the metadata to the JSON object.
1. Click **Save**.

{{% /tab %}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-part.snippet.add-metadata-part.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30-32" >}}

For more information, see [`GetRobotPartMetadata`](/reference/apis/fleet/) and [`UpdateRobotPartMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-part.snippet.add-metadata-part.go" lang="go" class="line-numbers linkable-line-numbers" data-line="29-31" >}}

For more information, see [`GetRobotPartMetadata`](/reference/apis/fleet/) and [`UpdateRobotPartMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-part.snippet.add-metadata-part.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="22-24" >}}

For more information, see [`GetRobotPartMetadata`](/reference/apis/fleet/) and [`UpdateRobotPartMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{< /tabs >}}

## Add and update custom machine metadata

{{< tabs >}}
{{% tab name="Web UI" %}}

1. On a machine page, click on the **...** menu in the top-right corner.
1. Select **Custom machine metadata**.
1. Add the metadata to the JSON object.
1. Click **Save**.

{{% /tab %}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.py" lang="py" class="line-numbers linkable-line-numbers" data-line="41-43" >}}

For more information, see [`GetRobotMetadata`](/reference/apis/fleet/) and [`UpdateRobotMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.go" lang="go" class="line-numbers linkable-line-numbers" data-line="50-52" >}}

For more information, see [`GetRobotMetadata`](/reference/apis/fleet/) and [`UpdateRobotMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="37-39" >}}

For more information, see [`GetRobotMetadata`](/reference/apis/fleet/) and [`UpdateRobotMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{< /tabs >}}

## Add and update custom location metadata

{{< tabs >}}
{{% tab name="Web UI" %}}

1. On a location page, click on the **...** menu in the top-right corner.
1. Select **Custom location metadata**.
1. Add the metadata to the JSON object.
1. Click **Save**.

{{% /tab %}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-location.snippet.add-metadata-location.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30-32" >}}

For more information, see [`GetLocationMetadata`](/reference/apis/fleet/) and [`UpdateLocationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-location.snippet.add-metadata-location.go" lang="go" class="line-numbers linkable-line-numbers" data-line="28-30" >}}

For more information, see [`GetLocationMetadata`](/reference/apis/fleet/) and [`UpdateLocationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-location.snippet.add-metadata-location.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="22-24" >}}

For more information, see [`GetLocationMetadata`](/reference/apis/fleet/) and [`UpdateLocationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{< /tabs >}}

## Add and update custom organization metadata

{{< tabs >}}

{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-organization.snippet.add-metadata-organization.py" lang="py" class="line-numbers linkable-line-numbers" data-line="30-32" >}}

For more information, see [`GetOrganizationMetadata`](/reference/apis/fleet/) and [`UpdateOrganizationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-organization.snippet.add-metadata-organization.go" lang="go" class="line-numbers linkable-line-numbers" data-line="28-30" >}}

For more information, see [`GetOrganizationMetadata`](/reference/apis/fleet/) and [`UpdateOrganizationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata-organization.snippet.add-metadata-organization.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="22-24" >}}

For more information, see [`GetOrganizationMetadata`](/reference/apis/fleet/) and [`UpdateOrganizationMetadata`](/reference/apis/fleet/).

{{% /tab %}}
{{< /tabs >}}

## Verify metadata

After adding metadata, verify it was saved:

- **Web UI**: Click the **...** menu on the resource and select the custom metadata option. The JSON object should contain your metadata.
- **CLI**: Run `viam metadata read --machine-id=<machine-id>` to read metadata for a machine and its parts.
- **SDK**: Use the corresponding `Get` method (`GetRobotPartMetadata`, `GetRobotMetadata`, `GetLocationMetadata`, or `GetOrganizationMetadata`) to retrieve and confirm the metadata.
