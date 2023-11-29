---
title: "Capture and query sensor data 2"
linkTitle: "Capture and query sensor data 2"
weight: 30
type: "docs"
description: "Query tabular data from your machine on the Viam app or from a compatible client."
---

You can use the data management service to capture tabular data from a connected component on your machine and sync that data to the cloud.
Once you have synced that data, you can query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} to obtain actionable insights.

For example, you might configure data capture for several sensors on your machine, or across sensors on multiple machines, to report the ambient operating temperature.
You could then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your robots' operation.

{{< cards >}}
{{% manualcard link="/data/" %}}

<h4>1. Configure the data management service</h4>

Add the [data management service](/data/) to your machine, then:

- [Configure data capture](/data/capture/) to capture sensor data
- [Configure cloud sync](/data/cloud-sync/) to sync data to the Viam app

{{% /manualcard %}}
{{% manualcard %}}

<h4>2. Capture data</h4>

Then, [capture tabular data from a component on your machine](/data/capture/#configure-data-capture-for-individual-components), such as a sensor.
<br><br>
Captured data is automatically synced to the cloud after a short delay.
You can [view view your data in the Viam app](/data/view/) from the **Data** tab.

{{% /manualcard %}}
{{% manualcard %}}

<h4>3. Query data in the Viam app</h4>

Once your data has synced, you can [query your data from within the Viam app](/data/query/#query-tabular-data-in-the-viam-app) using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

{{% /manualcard %}}
{{% manualcard %}}

<h4>4. Query data from a compatible client</h4>

If you prefer, you can also [query your data directly from an MQL-compatible client](/data/query/#query-tabular-data-directly-from-a-compatible-client), such as `mongosh` or MongoDB Compass, using SQL or MQL.

{{% /manualcard %}}

{{< /cards >}}

## Next steps

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/data/view/" %}}
{{% card link="/data/export/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
