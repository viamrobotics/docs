---
title: "Add custom machine metadata"
linkTitle: "Add machine metadata"
weight: 55
type: "docs"
description: "Add custom machine metadata as a JSON object."
date: "2025-11-14"
# updated: ""  # When the tutorial was last entirely checked
---

To store metadata for a machine, you can add custom machine metadata in the UI or using the Viam SDKs.
You can also add custom metadata for locations, organizations, and machine parts using the Viam SDKs.

## Prerequisites

{{% expand "A running machine connected to Viam." %}}

{{% snippet "setup-both.md" %}}

{{% /expand%}}

## Add and update custom machine metadata

{{< tabs >}}
{{% tab name="Web UI" %}}

1. On a machine page, lick on the **...** menu in the top-right corner.
1. Select **Custom machine metadata**.
1. Add the metadata to the JSON object.
1. Click **Save**.

{{% /tab %}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.py" lang="py" class="line-numbers linkable-line-numbers" data-line="41-43" >}}

For more information, see [`GetRobotMetadata`](/dev/reference/apis/fleet/#getrobotmetadata) and [`UpdateRobotMetadata`](/dev/reference/apis/fleet/#updaterobotmetadata).

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.go" lang="go" class="line-numbers linkable-line-numbers" data-line="50-52" >}}

For more information, see [`GetRobotMetadata`](/dev/reference/apis/fleet/#getrobotmetadata) and [`UpdateRobotMetadata`](/dev/reference/apis/fleet/#updaterobotmetadata).

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/add-metadata.snippet.add-metadata.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="37-39" >}}

For more information, see [`GetRobotMetadata`](/dev/reference/apis/fleet/#getrobotmetadata) and [`UpdateRobotMetadata`](/dev/reference/apis/fleet/#updaterobotmetadata).

{{% /tab %}}
{{< /tabs >}}
