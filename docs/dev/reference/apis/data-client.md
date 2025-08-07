---
title: "Upload and retrieve data with Viam's data client API"
linkTitle: "Data client"
weight: 10
type: "docs"
description: "Use the data client API to upload and retrieve data directly."
icon: true
images: ["/services/icons/sdk.svg"]
tags:
  [
    "cloud",
    "sdk",
    "viam-server",
    "networking",
    "apis",
    "robot api",
    "data management",
    "data",
  ]
aliases:
  - /program/apis/data-client/
  - /build/program/apis/data-client/
  - /appendix/apis/data-client/

date: "2024-09-19"
# updated: ""  # When the content was last entirely checked
---

The data client API allows you to upload and retrieve data to and from the Viam Cloud.

The data client API supports the following methods:

Methods to upload data like images or sensor readings directly to Viam:

{{< readfile "/static/include/app/apis/generated/data_sync-table.md" >}}

Methods to download, filter, tag, or perform other tasks on data like images or sensor readings:

{{< readfile "/static/include/app/apis/generated/data-table.md" >}}

Methods to work with datasets:

{{< readfile "/static/include/app/apis/generated/dataset-table.md" >}}

## API

{{< readfile "/static/include/app/apis/generated/data_sync.md" >}}

{{< readfile "/static/include/app/apis/generated/data.md" >}}

{{< readfile "/static/include/app/apis/generated/dataset.md" >}}
