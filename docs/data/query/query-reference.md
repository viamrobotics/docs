---
linkTitle: "Query reference"
title: "Query reference"
weight: 15
layout: "docs"
type: "docs"
aliases:
  - /data/query-reference/
  - /manage/data/query/
  - /use-cases/sensor-data-query/
  - /use-cases/sensor-data-query-with-third-party-tools/
  - /how-tos/sensor-data-query-with-third-party-tools/
  - /data-ai/data/query/
date: "2024-12-03"
updated: "2025-09-12"
description: "Query reference: supported operators, SQL limitations, third-party tools, and performance best practices."
---

For a step-by-step guide to querying captured data using SQL and MQL, see [Query Data](/data/query/query-data/).

## Prerequisites

{{% expand "Data query permissions" %}}

Users with owner or operator roles at the organization, location, or machine level can query data.
See [Role-Based Access Control](/organization/rbac/) for details.

{{% /expand%}}

## Query using the Viam app

Navigate to the [**Query** page](https://app.viam.com/data/query) and select **SQL** or **MQL**.

You can optionally change the data source to query data from a configured [hot data store](/data/query/hot-data-store/).

{{< alert title="Tip: Query Assistant" color="tip" >}}
For help with writing queries, use the **Query Assistant** button in the top right corner.
{{< /alert >}}

You can save queries in the web UI.
Click on **Saved** and then **Save current query**.
Fill in a **Name** for your query and click **Save query**.

## Query using TypeScript

{{< tabs >}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query.snippet.data-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18-31" >}}

{{< expand "Click to see an example that filters by component name and column names." >}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-filter.ts" lang="ts" class="line-numbers linkable-line-numbers" >}}

{{< /expand >}}
{{< expand "Click to see an example that returns a count of records that match a component name." >}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-count.ts" lang="ts" class="line-numbers linkable-line-numbers" >}}

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

For Python and Go examples, see [Query Data](/data/query/query-data/#query-data-programmatically).

## Query using third-party tools

You can query captured data using any third-party tool that supports MongoDB, such as the [`mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/) or [MongoDB Compass](https://www.mongodb.com/docs/compass/current/).

### Prerequisites

{{% expand "Viam CLI" %}}

You must have the Viam CLI installed to configure querying with third-party tools.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

{{% expand "Third-party tool for querying data (such as mongosh)" %}}

[Download the `mongosh` shell](https://www.mongodb.com/try/download/shell) or another third-party tool that can connect to a MongoDB data source.

See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

{{% /expand%}}

### Configure data query

If you want to query data from third-party tools, you have to configure data query to obtain the credentials you need to connect to the third-party service.

{{< readfile "/static/include/how-to/query-data.md" >}}

### Connect and query

Run the following command to connect to your Viam organization's MongoDB instance from `mongosh` using the connection URI you obtained during query configuration:

```sh {class="command-line" data-prompt=">"}
mongosh "mongodb://db-user-abcd1e2f-a1b2-3c45-de6f-ab123456c123:YOUR-PASSWORD-HERE@data-federation-abcd1e2f-a1b2-3c45-de6f-ab123456c123-0z9yx.a.query.mongodb.net/?ssl=true&authSource=admin"
```

For information on connecting to your Atlas Data Federation instance from other MQL clients, see the [Connect to your Cluster Tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

Once connected, you can run SQL or MQL statements to query captured data directly.

The following query searches the `readings` collection in the `sensorData` database and gets sensor readings from an ultrasonic sensor on a specific `robot_id` where the recorded `distance` measurement is greater than `0.2` meters.

{{< tabs >}}
{{% tab name="MQL" %}}

```mongodb {class="command-line" data-prompt=">" data-output="10"}
use sensorData
db.readings.aggregate(
    [
        { $match: {
            'robot_id': 'abcdef12-abcd-abcd-abcd-abcdef123456',
            'component_name': 'my-ultrasonic-sensor',
            'data.readings.distance': { $gt: 0.2 } } },
        { $count: 'numStanding' }
    ] )
[ { numStanding: 215 } ]
```

See the [MQL documentation](https://www.mongodb.com/docs/manual/tutorial/query-documents/) for more information.

{{% /tab %}}
{{% tab name="SQL" %}}

```mongodb {class="command-line" data-prompt=">" data-output="11"}
use sensorData
db.aggregate(
[
    { $sql: {
        statement: "select count(*) as numStanding from readings \
            where robot_id = 'abcdef12-abcd-abcd-abcd-abcdef123456' and \
            component_name = 'my-ultrasonic-sensor' and (CAST (data.readings.distance AS DOUBLE)) > 0.2",
        format: "jdbc"
    }}
] )
[ { '': { numStanding: 215 } } ]
```

See the [`$sql` aggregation pipeline stage documentation](https://www.mongodb.com/docs/atlas/data-federation/supported-unsupported/pipeline/sql/) for more information.

{{% /tab %}}
{{< /tabs >}}

<!-- markdownlint-disable-file MD001 -->

{{< expand "Need to query by date? Click here." >}}

##### Query by date

When using MQL to query your data by date or time range, you can optimize query performance by avoiding the MongoDB `$toDate` expression, using the [BSON `date` type](https://www.mongodb.com/docs/manual/reference/bson-types/#date) instead.

For example, use the following query to search by a date range in the `mongosh` shell.
Use the JavaScript `Date()` constructor to specify an explicit start timestamp and the current time as the end timestamp:

```mongodb {class="command-line" data-prompt=">"}
// Switch to sensorData database:
use sensorData

// Set desired start and end times:
const startTime = new Date('2024-02-10T19:45:07.000Z')
const endTime = new Date()

// Run query using $match:
db.readings.aggregate(
    [
        { $match: {
            time_received: {
                $gte: startTime,
                $lte: endTime }
        } }
    ] )
```

{{< /expand>}}

## Query optimization and performance best practices

1. When querying large datasets, whether from default storage or a [hot data store](/data/query/hot-data-store/), you can improve the query's efficiency by specifying the following parameters in the query:

   - `organization_id`
   - `location_id`
   - `robot_id`
   - `part_id`
   - `component_type`
   - `component_name`
   - `method_name`
   - `capture_day`

   Viam stores data in blob storage using the pattern `/organization_id/location_id/robot_id/part_id/component_type/component_name/method_name/capture_day/*`.
   The more specific you can be, starting with the beginning of the path, the faster your query.

1. Filter and reduce the amount of data that needs to be processed early, especially when your query expands the data it works with using operators like `$limit` and `$unwind`.
   If you don't need all fields, use `$project` early to reduce the fields in the processing dataset.
   If you only need a certain number of results, use `$limit` early in the pipeline to reduce data processing.

1. If you are frequently querying recent data, use the [hot data store](/data/query/hot-data-store/) which provides faster data access.

1. If you frequently perform the same types of queries, for example for dashboards, use [data pipelines](/data/query/configure-data-pipelines/).
   Data pipelines allow you to pre-compute a materialized view of your data at specified intervals.

## Supported query languages

### MQL

Viam supports the [MongoDB Query Language](https://www.mongodb.com/docs/manual/tutorial/query-documents/) for querying captured data from MQL-compatible clients such as `mongosh` or MongoDB Compass.

#### Supported aggregation operators

Viam supports the following MongoDB aggregation operators:

<!--
see whitelistStages in https://github.com/viamrobotics/app/blob/e706a2e3ea57a252f102b37e0ab2b9d6eeed51e0/datamanagement/tabular_data_by_query.go#L64
-->

- `$addFields`
- `$bucket`
- `$bucketAuto`
- `$count`
- `$densify`
- `$fill`
- `$geoNear`
- `$group`
- `$limit`
- `$match`
- `$project`
- `$redact`
- `$replaceRoot`
- `$replaceWith`
- `$sample`
- `$set`
- `$setWindowFields`
- `$skip`
- `$sort`
- `$sortByCount`
- `$unset`
- `$unwind`

### SQL

You can query data with SQL queries using the [MongoDB Atlas SQL dialect](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations), which supports standard SQL query syntax in addition to Atlas-specific capabilities such as `FLATTEN` and `UNWIND`.

SQL queries are subject to the following limitations:

- If a database, table, or column identifier meets any of the following criteria, you must surround the identifier with backticks (`` ` ``) or double quotes (`"`):
  - begins with a digit (for example `1`)
  - begins with a [reserved character](https://www.postgresql.org/docs/current/functions-matching.html) (for example `%`)
  - conflicts with a [reserved SQL keyword](https://en.wikipedia.org/wiki/List_of_SQL_reserved_words) (for example `select`)
- To include a single quote character in a string literal, use two single quotes (use `o''clock` to represent the literal `o'clock`).
- The `date` data type is not supported. Use `timestamp` instead.

For a full list of limitations, see the [MongoDB Atlas SQL Interface Language Reference](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatibility-and-limitations).
