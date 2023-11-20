---
title: "Query Data"
linkTitle: "Query Data"
weight: 40
no_list: true
type: "docs"
tags: ["data management", "data", "services"]
description: "Query tabular data that you have synced to the Viam app using the data management service with SQL or MQL."
# SME: Devin Hilly
---

Once you have [added the data management service](/services/data/configure-data-capture/#add-the-data-management-service) and [synced tabular data to the Viam app](/services/data/#cloud-sync), you can perform queries against that data using either {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You can:

- [Query tabular data in the Viam app](#query-tabular-data-in-the-viam-app): Run SQL or MQL queries against your synced tabular data from the **Query** subtab under the **Data** tab in the Viam app.
- [Query tabular data using the API](#query-tabular-data-using-the-api): Use data management API methods in your code to query tabular data.
- [Query tabular data directly from a compatible client](#query-tabular-data-directly-from-a-compatible-client): Directly query tabular data from an MQL-compatible client, such as `mongosh`.

You can query against both the captured tabular data itself as well as its metadata, including robot ID, organization ID, and [tags](/manage/data/label/#image-tags).

Only tabular data, such as sensor readings, can be queried in this fashion.

## Requirements

Before you can query your data, you must:

1. [Add the data management service](/services/data/configure-data-capture/#add-the-data-management-service).
1. [Configure data capture](/services/data/configure-data-capture/) for at least one component, such as a sensor.
   Only components that capture tabular data support data query.
1. [Configure cloud sync](/services/data/configure-cloud-sync/), and sync data to the Viam app.
   When you are able to [view your data in the Viam app](/manage/data/view/), you are ready to proceed.

In addition, if you intend to directly query tabular data from an MQL-compatible client, you must also [configure direct data query](/services/data/configure-data-query/).

## Query tabular data in the Viam app

Once you have synced tabular data to the Viam app, you can run SQL or MQL queries against your synced data from the **Query** subtab under the **Data** tab in the Viam app.

1. Navigate to the App.

1. Click a button.

## Query tabular data using the API

Once you have synced tabular data to the Viam app, you can use data management API methods in your code to query tabular data.

1. Open up your IDE.

1. Enter some code.

## Query tabular data directly from a compatible client

Once you have synced tabular data to the Viam app, you can directly query tabular data from an MQL-compatible client, such as [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/) or [Compass](https://www.mongodb.com/docs/compass/current/).

1. If you haven't already, [configure direct data query](/services/data/configure-data-query/#configure-data-query) to be able to use this query mode.

1. Follow the instructions to [query your data directly](/services/data/configure-data-query/#query-data-directly) from your MQL-compatible client.

## Next Steps

To export your captured data from the cloud, see [Export Data](../export/).

To adjust the rate at which your machine captures data, see [Configure Data Capture](/services/data/configure-data-capture/#configure-data-capture-for-individual-components).

To adjust the sync frequency, see [Configure Cloud Sync](/services/data/configure-cloud-sync/).
