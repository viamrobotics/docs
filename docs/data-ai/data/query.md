---
linkTitle: "Query data"
title: "Query data"
weight: 20
layout: "docs"
type: "docs"
aliases:
  - /manage/data/query/
  - /data/query/
  - /use-cases/sensor-data-query/
  - /use-cases/sensor-data-query-with-third-party-tools/
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "core"]
no_list: true
date: "2024-12-03"
description: "Query sensor data that you have synced to the Viam app using the Viam app with SQL or MQL."
---

<!-- TODO: write new one based on query page -->

You can use the data management service to [capture sensor data](/how-tos/collect-sensor-data/) from any machine and sync that data to the cloud.
Then, you can follow the steps on this page to query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
For example, you can configure data capture for several sensors on one machine, or for several sensors across multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

- **SQL:** For querying captured data, Viam supports the [MongoDB Atlas SQL dialect](https://www.mongodb.com/docs/atlas/data-federation/query/sql/query-with-asql-statements/), which supports standard SQL query syntax in addition to Atlas-specific capabilities such as `FLATTEN` and `UNWIND`.
  For more information, see the [MongoDB Atlas SQL language reference](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/).

- **MQL**: Viam also supports the [MongoDB Query language](https://www.mongodb.com/docs/manual/tutorial/query-documents/) for querying captured data from MQL-compatible clients such as `mongosh` or MongoDB Compass.

{{< alert title="In this page" color="tip" >}}

1. [Query data in the Viam app](#query-data-in-the-viam-app).
1. [Configure data query](#configure-data-query).
1. [Query data from third-party tools](#query-data-using-third-party-tools).

{{< /alert >}}

## Prerequisites

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/how-tos/collect-sensor-data/).

{{% /expand%}}
=