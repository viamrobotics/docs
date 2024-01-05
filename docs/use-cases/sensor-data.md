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
You can then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your robots' operation.

<table>
  <tr>
    <th>{{<imgproc src="/icons/components/sensor.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
      <b>1. Configure the data management service</b><br><br>
      <p>First, <a href="/fleet/machines/#add-a-new-machine">create a machine</a> if you haven't yet.</p>
      <p>Then, <a href="/data/">add the data management service</a>, and configure <a href="/data/capture/">data capture</a> and <a href="/data/cloud-sync/">cloud sync</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/sensor.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Capture tabular data from a sensor">}}
      <b>2. Capture data</b><br><br>
      <p>Next, <a href="/data/capture/#configure-data-capture-for-individual-components">capture tabular data from a component on your machine</a>, such as a sensor. With cloud sync enabled, captured data is automatically uploaded to the Viam app after a short delay.
      <br><br>You can view your synced data in the Viam app from the <b>Data</b> tab.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
      <b>3. Query data in the Viam app</b><br><br>
      <p>Once your data has synced, you can <a href="/data/query/#query-tabular-data-in-the-viam-app">query your data from within the Viam app</a> using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.</p>
      <p>For example, this query limits returned results to show data captured by the <code>my-ultrasonic-sensor</code> component only, and with a maximum of 5 results.</p>
      <p>{{< imgproc src="/data/query-ui-sql.png" alt="Viam App Data Query tab with a SQL query shown" resize="800x" class="fill alignleft">}}</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/services/icons/data-capture.svg" class="fill alignleft" style="max-width: 150px" declaredimensions=true alt="Configure the data management service">}}
      <b>4. Query data from a compatible client</b><br><br>
      <p>If you prefer, you can also <a href ="/data/query/#query-tabular-data-directly-from-a-compatible-client">query your data directly from an MQL-compatible client</a>, such as <code>mongosh</code> or MongoDB Compass, using SQL or MQL.</p>
      <p>{{<imgproc src="/data/data-query-mongosh-example.png" class="fill alignleft" resize="600x" declaredimensions=true alt="SQL query in mongosh filtering by machine, component, and specific data readings">}}</p>
    </th>
  </tr>
</table>

## Next steps

{{< cards >}}
{{% card link="/data/query/" %}}
{{% card link="/data/view/" %}}
{{% card link="/data/export/" %}}
{{% card link="/tutorials/" %}}
{{< /cards >}}
