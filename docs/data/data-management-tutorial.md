---
linkTitle: "Tutorial"
title: "Capture, sync, and query data tutorial"
weight: 2
layout: "docs"
type: "docs"
description: "Capture sensor data, sync it to the cloud, view it in the Data tab, and query it from code."
date: "2026-03-26"
aliases:
  - /data/capture-sync/data-capture-tutorial/
---

In this tutorial, you will set up a complete data pipeline: capture sensor data on your machine, sync it to Viam's cloud, view it in the Data tab, and query it from your own code. By the end, you will understand how data flows from your robot to the cloud and how to access it programmatically.

**Time:** ~15 minutes

**What you need:**

- A machine connected to the Viam app (if you don't have one yet, follow [Set up a machine](/foundation/))
- Python 3 installed on your laptop or desktop (for the final step)

We will use a fake sensor so this tutorial works without any physical hardware.

## 1. Add a fake sensor

We need a component that produces data. The built-in `sensor/fake` component returns a fixed set of readings every time it is polled, which is enough to exercise the capture, sync, and query pipeline end to end.

1. Go to your machine's page in the Viam app.
2. Click the **+** button in the left sidebar.
3. Select **Configuration block**.
4. Search for **sensor/fake** and select the result.
5. Name it `test-sensor` and click **Create**.
6. Click **Save** in the upper right.

Expand the **test** section on the sensor's component card. You should see `{"a": 1, "b": 2, "c": 3}` returned from `GetReadings`. This confirms the sensor is working.

{{< alert title="Note" color="note" >}}
`sensor/fake` always returns the same values. As you capture data in the next steps, every row will have identical `data` but a fresh `time_received` timestamp. That is enough to verify the full pipeline. With a real sensor, the values would change each reading.
{{< /alert >}}

## 2. Enable data capture

Now we will tell Viam to record every reading from this sensor.

1. Find the `test-sensor` component in the **CONFIGURE** tab.
2. Scroll to the **Data capture** section on the component card.
3. Click **+ Add method**.
4. If this is your first time configuring data capture, Viam will prompt you to enable the **data management service**. Click to enable it.
5. Select the **Readings** method.
6. Set the capture frequency to **0.2** (one reading every 5 seconds).
7. Click **Save**.

After saving, `viam-server` begins capturing immediately. You do not need to restart anything.

## 3. Watch data sync to the cloud

The data management service captures readings to local disk, then syncs them to Viam's cloud. By default, sync runs every 6 seconds.

Wait about 30 seconds, then:

1. Click the **DATA** tab in the top navigation of the Viam app. The tab opens on the **Images** view by default.
2. Click the **Sensors** tab.
3. You should see a machine card for your machine with `test-sensor` listed and its most recent reading displayed.

The Sensors tab shows the latest reading per resource per machine, not a table of historical rows. You will query the historical rows from the query editor in the next step.

If you don't see your machine or sensor yet, wait another 30 seconds. The first sync can take a moment as the service initializes.

{{< alert title="What just happened?" color="info" >}}

Behind the scenes:

1. `viam-server` called `test-sensor.GetReadings()` every 5 seconds.
2. Each reading was appended to a `.capture` file (length-delimited binary protobuf) in `$HOME/.viam/capture` on your machine. When `viam-server` runs as root through `viam-agent`, that path is `/root/.viam/capture`.
3. The sync process uploaded those files to Viam's cloud storage.
4. The local files were deleted after successful sync.

Your data is now stored in MongoDB (tabular data) in the cloud, queryable and exportable.

{{< /alert >}}

## 4. Query your data in the app

Now that data is in the cloud, you can query it.

1. On the **Sensors** tab, find your `test-sensor` and click the small search icon next to it to jump to the query editor. (If you don't see the icon, it is in the same row as the sensor name. Its tooltip reads "Query historical data".) You can also click **Query** in the data tab navigation to open the editor manually.
2. The query editor opens. Paste this SQL query:

   ```sql
   SELECT time_received, data
   FROM readings
   WHERE component_name = 'test-sensor'
     AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
   ORDER BY time_received DESC
   LIMIT 5
   ```

   {{< alert title="Known issue" color="caution" >}}
   The `AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)` clause is a workaround for APP-10891: SQL queries against `readings` currently return no rows unless the `WHERE` clause includes an explicit lower bound on `time_received`. Include it on every SQL query on this page.
   {{< /alert >}}

3. Click **Run query**.

The results appear as a list of JSON rows by default. Click the **table view** toggle (the small table icon in the results area) to see the rows as columns. You should see 5 rows with `time_received` values a few seconds apart and identical `data` values (`{"a": 1, "b": 2, "c": 3}`, because `sensor/fake` returns constant readings).

To understand the structure, try this:

```sql
SELECT data FROM readings
WHERE component_name = 'test-sensor'
  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
LIMIT 1
```

Switch to **table view** (the table icon in the results area). You'll see nested fields flattened into column headers like `data.readings.x`. These dot-notation paths are what you use to extract specific values in queries. For the full schema, see the [readings table schema](/data/schema/#column-reference).

Try one more query:

```sql
SELECT COUNT(*) as total_readings
FROM readings
WHERE component_name = 'test-sensor'
  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP)
```

This tells you how many readings have been captured so far.

## 5. Query your data from code

The same data is accessible from your own code through the Viam SDK.

{{< readfile "/static/include/how-to/get-credentials.md" >}}

Install the Viam Python SDK:

```bash
pip install viam-sdk
```

Save this as `query_data.py`:

```python
import asyncio
from viam.rpc.dial import DialOptions
from viam.app.viam_client import ViamClient


async def main():
    dial_options = DialOptions.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID",
    )
    client = await ViamClient.create_from_dial_options(dial_options)
    data_client = client.data_client

    # Query the 5 most recent readings from test-sensor
    results = await data_client.tabular_data_by_sql(
        organization_id="YOUR-ORGANIZATION-ID",
        sql_query=(
            "SELECT time_received, data "
            "FROM readings "
            "WHERE component_name = 'test-sensor' "
            "  AND time_received >= CAST('2000-01-01T00:00:00.000Z' AS TIMESTAMP) "
            "ORDER BY time_received DESC "
            "LIMIT 5"
        ),
    )

    print(f"Got {len(results)} readings:\n")
    for row in results:
        print(row)

    client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python query_data.py
```

You should see your 5 most recent sensor readings printed to the console. This is the same data you saw in the app's query editor, now accessible from your own code.

## 6. Clean up

To stop capturing data from the test sensor:

1. Go back to the **CONFIGURE** tab.
2. Find `test-sensor`.
3. In the **Data capture** section, click the trash icon next to the **Readings** method to remove the capture configuration.
4. Click **Save**.

Capture stops immediately. Data already synced to the cloud remains available for querying.

If you want to remove the test sensor entirely, click the trash icon on the component card and save.

## What you learned

You set up a complete data pipeline:

- **Capture**: `viam-server` recorded sensor readings to local disk at a configured frequency.
- **Sync**: the data management service uploaded captured data to Viam's cloud automatically.
- **View**: the Data tab in the Viam app showed your synced data with filtering and browsing.
- **Query**: you queried your data with SQL, both in the app and from your own Python code.

## What's next

Now that you understand the data pipeline, you can:

- [Capture data from real hardware](/data/capture-sync/capture-and-sync-data/): configure capture on cameras, motors, or any component.
- [Filter data at the edge](/data/filter-at-the-edge/): reduce data volume by capturing only what matters.
- [Data pipelines](/data/pipelines/create-a-pipeline/): schedule transformations on your captured data.
- [Visualize your data](/data/visualize-data/): build monitoring dashboards.
