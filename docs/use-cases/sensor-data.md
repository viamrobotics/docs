---
title: "Capture and query sensor data"
linkTitle: "Capture and query sensor data"
weight: 30
type: "docs"
description: "Query tabular data from your machine on the Viam app or from a compatible client."
---

You can use the data management service to capture tabular data from a connected component on your machine and sync that data to the cloud.
Once you have synced that data, you can query that data using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}} to search through that data for actionable insights.

For example, you might configure data capture for several sensors on your machine, or across sensors on multiple machines, to report the ambient operating temperature.
You could then run queries against that data to search for outliers or edge cases, to analyze how the ambient temperature affects your robots' operation.

<table>
  <tr>
    <th>{{<imgproc src="/build/configure/services/icons/data-capture.svg" class="fill alignright" style="max-width: 200px" declaredimensions=true alt="Collect data">}}
      <b>1. Configure the data management service</b>
      <p>Start by adding the <a href="/data/">data management service</a> to your machine, then configure <a href="/data/capture/">data capture</a> and <a href="/data/cloud-sync/">cloud sync</a>.</p>
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/icons/components/sensor.svg" class="fill alignleft" style="max-width: 200px" declaredimensions=true alt="Collect data">}}
      <b>2. Capture data</b>
      <p>Then, <a href="/data/capture/#configure-data-capture-for-individual-components">capture tabular data from a component on your machine</a>, such as a sensor. Captured data is automatically synced to the cloud after a short delay.
      <br><br>You can <a href="/data/view/">view your data in the Viam app</a> from the <b>Data</b> tab.</p>
    </th>
  </tr>
  <tr>
    <th>
      <b>3. Query data in the Viam app</b>
      <p>Once your data has synced, you can <a href="/data/query/#query-tabular-data-in-the-viam-app">query your data from within the Viam app</a> using {{< glossary_tooltip term_id="sql" text="SQL" >}} or {{< glossary_tooltip term_id="mql" text="MQL" >}}.</p>
      <p>
      {{< imgproc src="/data/query-ui-sql.png" alt="Viam App Data Query tab with a SQL query shown" resize="800x" class="fill alignright">}}
      {{< imgproc src="/data/query-ui-mql.png" alt="Viam App Data Query tab with an MQL query shown" resize="800x" class="fill alignright">}}</p>
      <p>For example, the examples to the right demonstrate the same query in SQL and in MQL, limiting returned results to show data captured by the <code>my-ultrasonic-sensor</code> component only, and with a maximum of 5 results.
      <br><br>Matching results are displayed directly below the query.
    </th>
  </tr>
  <tr>
    <th>{{<imgproc src="/data/data-query-mongosh-example.png" class="fill alignleft" resize="600x" declaredimensions=true alt="Train models">}}
      <b>4. Query data from a compatible client</b>
      <p>If you prefer, you can also <a href ="/data/query/#query-tabular-data-directly-from-a-compatible-client">query your directly from an MQL-compatible client</a>, such as <code>mongosh</code> or MongoDB Compass, using SQL or MQL.</p></p>
    </th>
  </tr>
</table>

## Next steps

For more information about working with the data management service, see the following:

- [Query Data with SQL or MQL](/data/query/)
- [View and Filter Data](/data/view/)
- [Export Data Using the Viam CLI](/data/export/)

You can also explore our [tutorials](/tutorials/) for more ideas.
