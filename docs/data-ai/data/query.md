---
linkTitle: "Query data"
title: "Query data"
weight: 30
layout: "docs"
type: "docs"
aliases:
  - /manage/data/query/
  - /data/query/
  - /use-cases/sensor-data-query/
  - /use-cases/sensor-data-query-with-third-party-tools/
  - /how-tos/sensor-data-query-with-third-party-tools/
languages: []
viamresources: ["sensor", "data_manager"]
platformarea: ["data", "core"]
date: "2024-12-03"
description: "Query sensor data that you have synced to Viam with SQL or MQL."
---

You can use the data management service to [capture sensor data](/data-ai/capture-data/capture-sync/) from any machine and sync that data to the cloud.
Then, you can follow the steps on this page to query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
For example, you can configure data capture for several sensors on one machine, or for several sensors across multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

## Query using Viam

### Prerequisites

{{% expand "Captured sensor data" %}}

Follow the guide to [capture sensor data](/data-ai/capture-data/capture-sync/).

{{% /expand%}}

### Query data using Viam

Once your data has synced, you can query your data using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You must have the [owner role](/manage/manage/rbac/) in order to query data on Viam.

{{< tabs >}}
{{% tab name="Web UI" %}}

{{< table >}}
{{% tablestep start=1 %}}
**Query with SQL or MQL**

Navigate to the [**Query** page](https://app.viam.com/data/query).
Then, select either **SQL** or **MQL** from the **Query mode** dropdown menu on the right-hand side.

{{% /tablestep %}}
{{% tablestep %}}
**Run your query**

This example query returns the last 5 readings from any components named `my-sensor` in your organization:

{{< tabs >}}
{{% tab name="SQL" %}}

```sql
SELECT * FROM readings
WHERE component_name = 'sensor-1' LIMIT 5
```

{{% /tab %}}
{{% tab name="MQL" %}}

```mql
[
    { "$match": { "component_name": "sensor-1" } },
    { "$limit": 5 }
]
```

{{% /tab %}}
{{< /tabs >}}

{{% expand "Click to see an example that filters by component name and column names." %}}

{{< tabs >}}
{{% tab name="SQL" %}}

```sh {class="command-line" data-prompt="$" data-output="3-80"}
SELECT time_received, data, tags FROM readings
WHERE component_name = 'sensor-1' LIMIT 2
[
{
  "time_received": "2024-07-30 00:04:02.144 +0000 UTC",
  "data": {
    "readings": {
      "units": "μg/m³",
      "pm_10": 7.6,
      "pm_2.5": 5.7
    }
  },
  "tags": [
    "air-quality"
  ]
},
{
  "time_received": "2024-07-30 00:37:22.192 +0000 UTC",
  "data": {
    "readings": {
      "pm_2.5": 9.3,
      "units": "μg/m³",
      "pm_10": 11.5
    }
  },
  "tags": [
    "air-quality"
  ]
}
]
```

{{% /tab %}}
{{% tab name="MQL" %}}

```sh {class="command-line" data-prompt="$" data-output="16-80"}
[
  {
    $match: {
      component_name: "sensor-1"
    }
  },{
    $limit: 2
  }, {
    $project: {
        time_received: 1,
        data: 1,
        tags: 1
    }
  }
]
[
{
  "time_received": "2024-07-30 00:04:02.144 +0000 UTC",
  "data": {
    "readings": {
      "units": "μg/m³",
      "pm_10": 7.6,
      "pm_2.5": 5.7
    }
  },
  "tags": [
    "air-quality"
  ]
},
{
  "time_received": "2024-07-30 00:37:22.192 +0000 UTC",
  "data": {
    "readings": {
      "pm_2.5": 9.3,
      "units": "μg/m³",
      "pm_10": 11.5
    }
  },
  "tags": [
    "air-quality"
  ]
}
]
```

{{% /tab %}}
{{< /tabs >}}

{{% /expand %}}
{{% expand "Click to see an example that returns a count of records that match a component name from a specific location." %}}

{{< tabs >}}
{{% tab name="SQL" %}}

```sh {class="command-line" data-prompt="$" data-output="3-80"}
SELECT count(*) FROM readings
WHERE component_name = 'sensor-1'
[
  {
    "_1": 111550
  }
]
```

{{% /tab %}}
{{% tab name="MQL" %}}

```sh {class="command-line" data-prompt="$" data-output="11"}
[
  {
    $match: {
      component_name: "sensor-1"
    }
  },{
    $count: "count"
  }
]
{ count: 111550 }
```

{{% /tab %}}
{{< /tabs >}}

{{% /expand %}}

{{% /tablestep %}}
{{% tablestep %}}
**Review results**

Click **Run query** when ready to perform your query and get matching results.
You can view your query results in a table or as a [JSON array](https://json-schema.org/understanding-json-schema/reference/array) below your query.

{{% /tablestep %}}
{{< /table >}}

{{% /tab %}}
{{% tab name="Python" %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query.snippet.data-query.py" lang="py" class="line-numbers linkable-line-numbers" data-line="29-47" >}}

{{% expand "Click to see an example that filters by component name and column names." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-filter.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}
{{% expand "Click to see an example that returns a count of records that match a component name from a specific location." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-count.py" lang="py" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}

{{% /tab %}}
{{% tab name="Go" %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query.snippet.data-query.go" lang="go" class="line-numbers linkable-line-numbers" data-line="28-45" >}}

{{% expand "Click to see an example that filters by component name and column names." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-filter.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}
{{% expand "Click to see an example that returns a count of records that match a component name from a specific location." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-count.go" lang="go" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}

{{% /tab %}}
{{% tab name="TypeScript" %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query.snippet.data-query.ts" lang="ts" class="line-numbers linkable-line-numbers" data-line="18-31" >}}

{{% expand "Click to see an example that filters by component name and column names." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-filter.ts" lang="ts" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}
{{% expand "Click to see an example that returns a count of records that match a component name from a specific location." %}}

{{< read-code-snippet file="/static/include/examples-generated/data-query-examples.snippet.data-query-count.ts" lang="ts" class="line-numbers linkable-line-numbers" >}}

{{% /expand %}}

{{% /tab %}}
{{< /tabs >}}

## Query using third-party tools

### Prerequisites

{{% expand "Captured sensor data" %}}

Follow the guide to [capture sensor data](/data-ai/capture-data/capture-sync/).

{{% /expand%}}

{{% expand "Viam CLI" %}}

You must have the Viam CLI installed to configure querying with third-party tools.

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

{{% expand "A third-party tool for querying data, such as mongosh" %}}

[Download the `mongosh` shell](https://www.mongodb.com/try/download/shell) or another third-party tool that can connect to a MongoDB data source to follow along.
See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

{{% /expand%}}

### Configure data query

If you want to query data from third party tools, you have to configure data query to obtain the credentials you need to connect to the third party service.

{{< readfile "/static/include/how-to/query-data.md" >}}

### Query data using third-party tools

You can use third-party tools, such as the [`mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/) or [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), to query captured sensor data.

{{< table >}}
{{% tablestep start=1 %}}
**Connect to your Viam organization's data**

Run the following command to connect to your Viam organization's MongoDB Atlas instance from `mongosh` using the connection URI you obtained during query configuration:

```sh {class="command-line" data-prompt=">"}
mongosh "mongodb://db-user-abcd1e2f-a1b2-3c45-de6f-ab123456c123:YOUR-PASSWORD-HERE@data-federation-abcd1e2f-a1b2-3c45-de6f-ab123456c123-0z9yx.a.query.mongodb.net/?ssl=true&authSource=admin"
```

{{% /tablestep %}}
{{% tablestep %}}
**Query data from a compatible client**

Once connected, you can run SQL or MQL statements to query captured data directly.

The following query searches the `sensorData` database and `readings` collection, and gets sensor readings from an ultrasonic sensor on a specific `robot_id` where the recorded `distance` measurement is greater than `.2` meters.

{{< tabs >}}
{{% tab name="MQL" %}}

The following MQL query performs counts the number of sensor readings where the `distance` value is above `0.2` using the [MongoDB query language](https://www.mongodb.com/docs/manual/tutorial/query-documents/):

```mongodb {class="command-line" data-prompt=">" data-output="10"}
use sensorData
db.readings.aggregate(
    [
        { $match: {
            'robot_id': 'abcdef12-abcd-abcd-abcd-abcdef123456',
            'component_name': 'my-ultrasonic-sensor',
            'data.readings.distance': { $gt: .2 } } },
        { $count: 'numStanding' }
    ] )
[ { numStanding: 215 } ]
```

{{% /tab %}}
{{% tab name="SQL" %}}

The following query uses the MongoDB [`$sql` aggregation pipeline stage](https://www.mongodb.com/docs/atlas/data-federation/supported-unsupported/pipeline/sql/):

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

{{% /tab %}}
{{< /tabs >}}

<!-- markdownlint-disable-file MD001 -->

{{< expand "Need to query by date? Click here." >}}

##### Query by date

When using MQL to query your data by date or time range, you can optimize query performance by avoiding the MongoDB `$toDate` expression, using the [BSON `date` type](https://www.mongodb.com/docs/manual/reference/bson-types/#date) instead.

For example, use the following query to search by a date range in the `mongosh` shell, using the JavaScript `Date()` constructor to specify an explicit start timestamp, and use the current time as the end timestamp:

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

{{% /tablestep %}}
{{< /table >}}

For information on connecting to your Atlas instance from other MQL clients, see the MongoDB Atlas [Connect to your Cluster Tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

On top of querying sensor data with third-party tools, you can also [query it with the Python SDK](/data-ai/reference/data-client/) or [visualize it](/data-ai/data/visualize/).

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

You can query data with SQL queries using the [MongoDB Atlas SQL dialect](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatability-and-limitations), which supports standard SQL query syntax in addition to Atlas-specific capabilities such as `FLATTEN` and `UNWIND`.

SQL queries are subject to the following limitations:

- If a database, table, or column identifier meets any of the following criteria, you must surround the identifier with backticks (`` ` ``) or double quotes (`"`):
  - begins with a digit (for example `1`)
  - begins with a [reserved character](https://www.postgresql.org/docs/current/functions-matching.html) (for example `%`)
  - conflicts with a [reserved SQL keyword](https://en.wikipedia.org/wiki/List_of_SQL_reserved_words) (for example `select`)
- To include a single quote character in a string literal, use two single quotes (use `o''clock` to represent the literal `o'clock`).
- The `date` data type is not supported. Use `timestamp` instead.

For a full list of limitations, see the [MongoDB Atlas SQL Interface Language Reference](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatability-and-limitations).
