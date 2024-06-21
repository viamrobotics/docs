---
title: "Query sensor data with third-party tools"
linkTitle: "Query sensor data"
weight: 30
type: "docs"
images: ["/services/icons/data-query.svg"]
description: "Query sensor data that you have synced to the Viam app using the Viam app with SQL or MQL."
modulescript: true
aliases:
  - /manage/data/query/
  - /data/query/
# SME: Devin Hilly
---

You can use the data management service to [capture sensor data](/use-cases/collect-sensor-data/) from any machine and sync that data to the cloud.
Then, you can follow the steps on this page to query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.
For example, you can configure data capture for several sensors on one machine, or for several sensors across multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

{{< alert title="In this page" color="tip" >}}

1. [Query data in the Viam app](#query-data-in-the-viam-app).
1. [Configure data query](#configure-data-query).
1. [Query data from third-party tools](#query-data-using-third-party-tools).

{{< /alert >}}

## Prerequisites

{{% expand "At least one configured sensor. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a sensor model](/components/sensor/) that supports your sensor.

If you're not sure which sensor model to choose, start with the [`viam:viam-sensor:telegrafsensor`](https://github.com/viamrobotics/viam-telegraf-sensor) which captures performance data (CPU, memory usage, and more) from your machine.

{{% /expand%}}

{{% expand "Captured sensor data. Click to see instructions." %}}

Follow the guide to [capture sensor data](/use-cases/collect-sensor-data/).

{{% /expand%}}

{{% expand "The Viam CLI to set up data query. Click to see instructions." %}}

{{< readfile "/static/include/how-to/install-cli.md" >}}

{{% /expand%}}

{{% expand "`mongosh` or another third-party tool for querying data. Click to see instructions." %}}

[Download the `mongosh` shell](https://www.mongodb.com/try/download/shell) or another third-party tool that can connect to a MongoDB data source to follow along.
See the [`mongosh` documentation](https://www.mongodb.com/docs/mongodb-shell/) for more information.

{{% /expand%}}

## Query data in the Viam app

Once your data has synced, you can query your data from within the Viam app using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You must have the [owner role](/cloud/rbac/) in order to query data in the Viam app.

{{< table >}}
{{< tablestep >}}
**1. Query with SQL or MQL**

Navigate to the [**Query** page](https://app.viam.com/data/query).
Then, select either **SQL** or **MQL** from the **Query mode** dropdown menu on the right-hand side.

{{< /tablestep >}}
{{< tablestep >}}
**2. Run your query**

This example query returns 5 readings from a component called `my-sensor`:

{{< tabs >}}
{{% tab name="SQL" %}}

```sql
SELECT * FROM readings WHERE component_name = 'my-sensor' LIMIT 5
```

{{% /tab %}}
{{% tab name="MQL" %}}

```mql
[{ "$match": { "component_name": "my-sensor" } }, { "$limit": 5 }]
```

{{% /tab %}}
{{< /tabs >}}
{{< /tablestep >}}
{{< tablestep >}}
**3. Review results**

Click **Run query** when ready to perform your query and get matching results.
Query results are displayed as a [JSON array](https://json-schema.org/understanding-json-schema/reference/array) below your query.

{{% expand "See examples" %}}

- The following shows a SQL query that filters by component name and specific column names, and its returned results:

  {{< imgproc src="/services/data/query-ui-results.png" alt="Viam App Data Query tab with a SQL query shown and results shown below including two matching records" resize="800x" >}}

- The following shows a SQL query that returns a count of records matching the search criteria:

  {{< imgproc src="/services/data/query-ui-numreadings.png" alt="Viam App Data Query tab with a SQL query shown with the resulting count of matching records displayed below" resize="800x" >}}

For more information on MQL syntax, see the [MQL (MongoDB Query Language)](https://www.mongodb.com/docs/manual/tutorial/query-documents/) documentation.

{{% /expand%}}

{{< /tablestep >}}
{{< /table >}}

## Configure data query

If you want to query data from third party tools, you have to configure data query to obtain the credentials you need to connect to the third party service.

{{< readfile "/static/include/how-to/query-data.md" >}}

## Query data using third-party tools

You can use third-party tools, such as the [`mongosh` shell](https://www.mongodb.com/docs/mongodb-shell/), [MongoDB Compass](https://www.mongodb.com/docs/compass/current/), to query against captured sensor data.

{{< table >}}
{{< tablestep link="/use-cases/sensor-data-query/#configure-data-query">}}
**1. Connect to your Viam organization's data**

Run the following command to connect to your Viam organization's MongoDB Atlas instance from `mongosh` using the connection URI you obtained during query configuration:

```sh {class="command-line" data-prompt=">"}
mongosh "<YOUR-DB-CONNECTION-URI>"
```

{{< /tablestep >}}
{{< tablestep >}}
**2. Query data from a compatible client**

Once connected, you can run SQL or MQL statements to query captured data directly.

The following query searches the `sensorData` database and `readings` collection, and gets sensor readings from an ultrasonic sensor on a specific `robot_id` where the recorded `distance` measurement is greater than `.2` meters.

{{< tabs >}}
{{% tab name="MQL" %}}

The following MQL query performs the same search as the SQL query above, but uses the [MongoDB query language](https://www.mongodb.com/docs/manual/tutorial/query-documents/):

```mongodb {class="command-line" data-prompt=">" data-output="11"}
use sensorData
db.aggregate(
    [
        { $sql: {
            statement: "select count(*) as numStanding from readings \
                where robot_id = 'abcdef12-abcd-abcd-abcd-abcdef123456' and \
                component_name = 'my-ultrasonic-sensor' and data.readings.distance > 0.2",
            format: "jdbc"
        }}
    ] )
[ { '': { numStanding: 215 } } ]
```

{{% /tab %}}
{{% tab name="SQL" %}}

The following query uses the MongoDB [`$sql` aggregation pipeline stage](https://www.mongodb.com/docs/atlas/data-federation/supported-unsupported/pipeline/sql/):

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
{{< /tabs >}}

{{< /tablestep >}}
{{< /table >}}

{{< alert title="Tip" color="tip" >}}
If you use a data field that is named the same as a [reserved SQL keyword](https://en.wikipedia.org/wiki/List_of_SQL_reserved_words), such as `value` or `position`, you must escape that field name in your query using backticks ( <file>\`</file> ).
For example, to query against a field named `value` which is a subfield of the `data` field in the `readings` collection, you would use:

```mongodb {class="command-line" data-prompt=">"}
select data.`value` from readings
```

See the [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/data-federation/query/sql/language-reference/#compatability-and-limitations) for more information.

{{< /alert >}}

For information on connecting to your Atlas instance from other MQL clients, see the MongoDB Atlas [Connect to your Cluster Tutorial](https://www.mongodb.com/docs/atlas/tutorial/connect-to-your-cluster/).

<!-- markdownlint-disable-file MD001 -->

{{% expand "Need to query by date? Click here." %}}

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

{{% /expand%}}

## Next steps

On top of querying sensor data with third-party tools, you can also [query it with the Python SDK](/use-cases/sensor-data-query-sdk/) or [visualize it](/use-cases/sensor-data-visualize/).

{{< cards >}}
{{% card link="/use-cases/sensor-data-query-sdk/" %}}
{{% card link="/use-cases/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
