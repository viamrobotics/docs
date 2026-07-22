---
title: "Navigation service API"
linkTitle: "Navigation"
weight: 70
type: "docs"
tags: ["navigation", "services", "base", "rover"]
description: "Give commands to define waypoints and move your machine along those waypoints while avoiding obstacles."
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
This page is retained for reference only.
{{< /alert >}}

The navigation service API allows you to define waypoints and move your machine along those waypoints while avoiding obstacles.

The [navigation service](/reference/services/navigation/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/navigation-table.md" >}}

## API

{{< readfile "/static/include/services/apis/generated/navigation.md" >}}
