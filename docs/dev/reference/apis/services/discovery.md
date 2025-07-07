---
title: "Discovery service API"
linkTitle: "Discovery"
weight: 80
type: "docs"
tags: ["navigation", "services", "resources", "components"]
description: "Reveal which resources are available to configure on a machine based on the hardware that is physically present."
date: "2025-02-18"
# updated: ""  # When the content was last entirely checked
---

The discovery service API allows you to get a list of resources available to configure on a machine based on the hardware that is connected to or part of the machine.
Discoverable resources can include components that are physically connected to the machine, as well as components that are available on the machine's local network (depending on the implementation of the [discovery service](/operate/reference/services/discovery/)).

The discovery service supports the following methods:

{{< readfile "/static/include/services/apis/generated/discovery-table.md" >}}

## API

{{< readfile "/static/include/services/apis/generated/discovery.md" >}}
