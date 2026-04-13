---
linkTitle: "Query from code"
title: "Query data from code"
weight: 22
layout: "docs"
type: "docs"
description: "Query captured data programmatically using the Viam Python or Go SDK."
date: "2026-03-26"
aliases:
  - /data/query-data-from-code/
---

Pull captured data into your own programs using the Viam data client API. You can run the same SQL and MQL queries available in the app's query editor from Python or Go code.

{{< alert title="Tip: discover your data structure" color="tip" >}}
Not sure what fields to query? Run this in the [query editor](/data/query-data/) first:

```sql
SELECT data FROM readings
WHERE component_name = 'YOUR-COMPONENT'
  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
LIMIT 1
```

Switch to **table view** to see nested fields as dot-notation column headers. Use those paths in your code. See the [readings table schema](/data/schema/#column-reference) for the full reference.
{{< /alert >}}

{{< alert title="Known issue: SQL queries need an explicit lower time bound" color="caution" >}}
SQL queries against `readings` currently return no rows unless the `WHERE` clause includes an explicit lower bound on `time_received`. Include `AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)` in any SQL example on this page if you copy it. MQL queries are not affected. Tracked as APP-10891.
{{< /alert >}}

## Set up a connection

{{< readfile "/static/include/how-to/get-credentials.md" >}}

{{< tabs >}}
{{% tab name="Python" %}}

```bash
pip install viam-sdk
```

```python
import asyncio
from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient

API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def main():
    dial_options = DialOptions.with_api_key(
        api_key=API_KEY,
        api_key_id=API_KEY_ID,
    )
    client = await ViamClient.create_from_dial_options(dial_options)
    data_client = client.data_client

    # ... your queries here ...

    client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```bash
mkdir query-data && cd query-data
go mod init query-data
go get go.viam.com/rdk
```

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

func main() {
    ctx := context.Background()
    logger := logging.NewDebugLogger("query-data")

    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, "YOUR-API-KEY", "YOUR-API-KEY-ID", logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    // ... your queries here ...
}
```

{{% /tab %}}
{{< /tabs >}}

## Query with SQL

Use `tabular_data_by_sql` to run SQL queries. Results come back as a list of rows.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Returns a list of dictionaries, one per row
results = await data_client.tabular_data_by_sql(
    organization_id=ORG_ID,
    sql_query=(
        "SELECT time_received, "
        "  data.readings.temperature AS temperature "
        "FROM readings "
        "WHERE component_name = 'my-sensor' "
        "  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP) "
        "ORDER BY time_received DESC "
        "LIMIT 5"
    ),
)

for row in results:
    print(row)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Returns a slice of maps, one per row
results, err := dataClient.TabularDataBySQL(ctx, orgID,
    "SELECT time_received, "+
        "data.readings.temperature AS temperature "+
        "FROM readings "+
        "WHERE component_name = 'my-sensor' "+
        "  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP) "+
        "ORDER BY time_received DESC LIMIT 5")
if err != nil {
    logger.Fatal(err)
}

for _, row := range results {
    fmt.Printf("%v\n", row)
}
```

{{% /tab %}}
{{< /tabs >}}

## Query with MQL

Use `tabular_data_by_mql` for MongoDB aggregation pipelines. MQL is more powerful than SQL for grouping, computing averages, and reshaping nested data.

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Returns a list of dictionaries from the aggregation result
results = await data_client.tabular_data_by_mql(
    organization_id=ORG_ID,
    query=[
        {"$match": {"component_name": "my-sensor"}},
        {"$group": {
            "_id": "$component_name",
            "avg_temp": {"$avg": "$data.readings.temperature"},
            "count": {"$sum": 1},
        }},
    ],
)

for entry in results:
    print(entry)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Returns a slice of maps from the aggregation result
results, err := dataClient.TabularDataByMQL(ctx, orgID,
    []map[string]interface{}{
        {"$match": map[string]interface{}{
            "component_name": "my-sensor",
        }},
        {"$group": map[string]interface{}{
            "_id":      "$component_name",
            "avg_temp": map[string]interface{}{"$avg": "$data.readings.temperature"},
            "count":    map[string]interface{}{"$sum": 1},
        }},
    }, nil)
if err != nil {
    logger.Fatal(err)
}

for _, entry := range results {
    fmt.Printf("%v\n", entry)
}
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Query reference](/data/reference/): schema, supported operators, and optimization tips
- [Create a data pipeline](/data/pipelines/create-a-pipeline/): schedule recurring queries
- [Sync to your database](/data/sync-data-to-your-database/): export data to your own MongoDB instance
- [Data client API reference](/dev/reference/apis/data-client/): full method documentation
