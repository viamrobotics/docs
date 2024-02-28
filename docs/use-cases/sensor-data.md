---
title: "Capture and query sensor data"
linkTitle: "Capture and query sensor data"
weight: 30
type: "docs"
description: "Query tabular data from your machine on the Viam app or from a compatible client."
---

You can use the data management service to capture tabular data from a connected component on your machine and sync that data to the cloud.
Once you have synced that data, you can query it using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} to obtain actionable insights.

For example, you might configure data capture for several sensors on your machine, or across sensors on multiple machines, to report the ambient operating temperature.
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your machines' operation.

{{< table >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-management.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
**1. Configure the data management service**

First, [create a machine](/fleet/machines/#add-a-new-machine) if you haven't yet.

Then, [add the data management service](/data/), and configure [data capture](/data/capture/) and [cloud sync](/data/cloud-sync/).

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Capture tabular data from a sensor">}}
**2. Capture data**

Next, [capture tabular data from a component on your machine](/data/capture/#configure-data-capture-for-individual-components), such as a sensor. With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.

You can view your synced data in the Viam app from the **Data** tab.

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-query.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
**3. Query data in the Viam app**

Once your data has synced, you can [query your data from within the Viam app](/data/query/#query-tabular-data-in-the-viam-app) using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.

For example, this query limits returned results to show data captured by the <code>my-ultrasonic-sensor</code> component only, and with a maximum of 5 results.

{{< imgproc src="/data/query-ui-sql.png" alt="Viam App Data Query tab with a SQL query shown" resize="800x" class="fill alignleft">}}

{{< /tablestep >}}
{{< tablestep >}}
{{<imgproc src="/services/icons/data-query.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
**4. Query data from a compatible client**

If you prefer, you can also <a href ="/data/query/#query-tabular-data-directly-from-a-compatible-client">query your data directly from an MQL-compatible client</a>, such as <code>mongosh</code> or MongoDB Compass, using SQL or MQL.

{{<imgproc src="/data/data-query-mongosh-example.png" class="fill alignleft" resize="600x" declaredimensions=true alt="SQL query in mongosh filtering by machine, component, and specific data readings">}}

{{< /tablestep >}}
{{< /table >}}

## Next steps

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/data/view/" %}}
{{% card link="/data/export/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
