---
title: "Collect and view sensor data from any machines"
linkTitle: "Collect sensor data"
weight: 29
type: "docs"
images: ["/services/icons/data-query.svg"]
description: "Gather sensor data, sync it to the cloud, and query it from the Viam app."
modulescript: true
# SME: Devin Hilly
---

You can use the data management service to capture sensor or time-series data from any machine and sync that data to the cloud.
Then, you can query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} to obtain actionable insights or connect it to third-party visualization tools.

For example, you can configure data capture for several sensors on one machine, or for serveral sensors across multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

You can do all of this using the [Viam app](https://app.viam.com/) user interface. You will not need to write any code.

{{< alert title="In this page" color="tip" >}}

1. [Gathering data on any machine and syncing it to the cloud](#gather-and-sync-data).
1. [Querying data in the Viam app](#query-data-in-the-viam-app).

{{< /alert >}}

## Prerequisites

{{% expand "A running machine connected to the Viam app. Click to see instructions." %}}

{{% snippet "setup.md" %}}

{{% /expand%}}

{{% expand "At least one configured sensor. Click to see instructions." %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Then [find and add a sensor model](/components/sensor/) that supports your sensor.

{{% /expand%}}

## Gather and sync data

{{< readfile "/static/include/how-to/gather-sync-sensor.md" >}}

## Query data in the Viam app

Once your data has synced, you can [query your data from within the Viam app](/use-cases/sensor-data-query/#query-data-in-the-viam-app) using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

You must have the [owner](/cloud/rbac/) role in order to query data in the Viam app.

{{< table >}}
{{< tablestep >}}
**1. Navigate to Query page**

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

## Next steps

Now that you have collected sensor data, you can also [query it](/use-cases/sensor-data-query/) or [visualize it](/use-cases/sensor-data-visualize/) with third-party tools.

{{< cards >}}
{{% card link="/use-cases/sensor-data-query/" %}}
{{% card link="/use-cases/sensor-data-visualize/" %}}
{{< /cards >}}

To see sensor data in action, check out this tutorial:

{{< cards >}}
{{% card link="/tutorials/control/air-quality-fleet/" %}}
{{< /cards >}}
