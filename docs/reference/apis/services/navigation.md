---
title: "Navigation service API"
linkTitle: "Navigation"
weight: 70
type: "docs"
tags: ["navigation", "services", "base", "rover"]
description: "Give commands to define waypoints and move your machine along those waypoints while avoiding obstacles."
capabilities: ["sdks", "navigation"]
diataxis: reference
date: "2022-01-01"
aliases:
  - /dev/reference/apis/services/navigation/
  - /appendix/apis/services/navigation/
build:
  render: always
  list: never
  publishResources: true
---

{{< alert title="Discontinued" color="caution" >}}
Support for the navigation service has been discontinued.
`viam-server` v1.13.0, the Go SDK in RDK v1.13.0, the Python SDK v0.85.0, and the Flutter SDK v0.23.0 replace the API on this page with a navigation API built around saved locations, routes, and zones.
In those versions, `GetMode`, `SetMode`, `GetWaypoints`, `AddWaypoint`, `RemoveWaypoint`, `GetObstacles`, and `GetPaths` no longer exist, and `GetLocation` returns a saved location instead of the machine's current position.
The TypeScript SDK still uses the API on this page, which `viam-server` v1.13.0 and later don't serve.
This page is retained for reference only.
{{< /alert >}}

The navigation service API allows you to define waypoints and move your machine along those waypoints while avoiding obstacles.

The [navigation service](/reference/services/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/navigation-table.md" >}}

## API

{{< readfile "/static/include/services/apis/generated/navigation.md" >}}
