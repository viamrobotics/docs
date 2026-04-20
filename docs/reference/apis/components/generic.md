---
title: "Control your generic component with the generic API"
linkTitle: "Generic"
weight: 100
type: "docs"
description: "Give commands for running custom model-specific commands using DoCommand on your generic components."
icon: true
images: ["/icons/components/generic.svg"]
date: "2022-01-01"
aliases:
  - /operate/modules/component-apis/generic/
  - /appendix/apis/components/generic/
# updated: ""  # When the content was last entirely checked
---

The generic API allows you to give commands to your [generic components](/reference/components/generic/) for running model-specific commands using [`DoCommand`](/reference/apis/components/generic/#docommand).

{{% alert title="Example usage" color="tip" %}}

See [Deploy control logic](/build-modules/write-a-logic-module/) for an example of how to use the generic component API, including how to call `DoCommand()` from the SDKs or the web UI.

{{% /alert %}}

The generic component supports the following method:

{{< readfile "/static/include/components/apis/generated/generic_component-table.md" >}}

## API

{{< readfile "/static/include/components/apis/generated/generic_component.md" >}}
