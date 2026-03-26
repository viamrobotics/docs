---
linkTitle: "Capture and sync data"
title: "Capture and sync data"
weight: 5
layout: "docs"
type: "docs"
description: "Capture data from any resource and sync it to the cloud."
date: "2025-01-30"
aliases:
  - /data/capture-and-sync-data/
  - /build/foundation/capture-and-sync-data/
  - /foundation/capture-and-sync-data/
---

## What Problem This Solves

Your machine generates useful data: camera images, sensor readings, detection
results. This how-to shows you how to use Viam's data management service to
capture this data automatically and sync it to the cloud.

## Concepts

### Data capture

Data capture records the output of any component on your machine. You configure
it through the Viam app: select which components to capture from, which API
methods to record, and how often. Captured data is written to the local
filesystem (`~/.viam/capture` by default; see [Capture directories](/data/#capture-directories) for platform-specific paths), so your machine continues capturing even if it temporarily
loses network connectivity.

### Cloud sync

Cloud sync transmits captured data to Viam's cloud storage. After successful
sync, local files are cleaned up automatically. If your machine is offline,
data syncs when the connection is restored. You can configure the sync interval
independently from the capture frequency, and enable or disable sync and
capture independently.

## Steps

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.

### 2. Enable data capture on a component

1. Find your component (for example, `my-camera`) in the machine configuration.
2. Scroll to the **Data capture** section in the component's configuration
   panel.
3. Click **+ Add method**.
4. If this is your first time configuring data capture, Viam will prompt you to
   enable the **data management service**. Click to enable it. This adds the
   service to your machine configuration and enables both capture and cloud
   sync.
5. Select the method to capture:
   - For a camera, select **GetImages**. This captures a frame from the camera
     each time it fires.
   - For a sensor, select **Readings**. This records the sensor's current
     values.
6. Set the **capture frequency**. This is specified in hertz (captures per
   second):
   - `0.5` = one capture every 2 seconds
   - `0.2` = one capture every 5 seconds
   - `1` = one capture per second
   - Start low. For cameras, `0.5` Hz is a reasonable starting point. You can
     always increase it later.
7. Click **Save** in the upper right.

After saving, `viam-server` begins capturing immediately. You do not need to
restart anything.

{{< alert title="Tip" color="tip" >}}

You can add multiple capture methods to a single component (for example,
capture both `GetImages` and `NextPointCloud` from the same camera), each
with its own frequency.

{{< /alert >}}

### 3. Capture from additional components (optional)

Repeat step 2 for any other components you want to capture from. Each
component's data capture is independent -- you can have a camera capturing
images every 2 seconds and a sensor capturing readings every 10 seconds at the
same time.

### 4. Sync data from another directory (optional)

You can also sync files from directories outside of the default capture path.
This is useful for uploading a batch of existing data or syncing files that another process writes to a folder on your machine.

In the data management service configuration, add the directory path to **Additional paths** (or `"additional_sync_paths"` in JSON mode).

{{< alert title="Caution" color="caution" >}}

Data synced from additional paths is deleted from the device after upload, just like captured data.
If you want to keep a local copy, copy the data to a new folder and sync that folder instead.

{{< /alert >}}

{{<imgproc src="/services/data/data-sync-temp.png" resize="x1100" declaredimensions=true alt="Data service configured with an additional sync path." style="width: 600px" class="shadow imgzoom" >}}

### 5. Verify data is syncing

Wait 30 seconds to a minute for data to accumulate and sync, then:

1. In the Viam app, click the **DATA** tab in the top navigation.
2. You should see captured data appearing. For camera captures, you will see
   image thumbnails. For sensor data, you will see tabular entries.
3. Use the filters on the left to narrow by:
   - **Machine** -- select your specific machine
   - **Component** -- select the component you configured
   - **Time range** -- pick a recent window
   - **Data type** -- Images or Tabular

If you see data flowing in, capture and sync are working correctly.

### 6. Explore the Data tab

With data flowing, familiarize yourself with the Data tab's query capabilities:

1. **Filtering:** Use the sidebar filters to narrow data by machine, component,
   location, time range, or tags. This is useful when you have multiple machines
   or components capturing data.
2. **SQL queries:** Click **Query** in the Data tab to open the query editor.
   Write SQL queries to analyze your tabular data:

   ```sql
   SELECT * FROM readings
   WHERE component_name = 'my-sensor'
   ORDER BY time_received DESC
   LIMIT 10
   ```

3. **MQL queries:** Switch to MQL mode for MongoDB-style queries:

   ```json
   [
     { "$match": { "component_name": "my-sensor" } },
     { "$sort": { "time_received": -1 } },
     { "$limit": 10 }
   ]
   ```

## Try It

### Verify capture is running

1. Check the **DATA** tab and confirm new entries are appearing at roughly the
   frequency you configured.
2. For camera data, click an image thumbnail to view the full captured image.
3. For sensor data, inspect the tabular values and confirm they match what you
   expect from your sensor.

### Query captured data programmatically

Beyond the Viam app UI, you can query your captured data from your own code
using the Viam app client. This is useful for building dashboards, running
analysis, or integrating captured data into your applications.

{{< tabs >}}
{{% tab name="Python" %}}

Install the SDK if you haven't already:

```bash
pip install viam-sdk
```

Save this as `query_data.py`:

```python
import asyncio
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def connect() -> ViamClient:
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID,
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    # Query with SQL -- get recent readings from a specific component
    sql_results = await data_client.tabular_data_by_sql(
        organization_id=ORG_ID,
        sql_query=(
            "SELECT * FROM readings "
            "WHERE component_name = 'my-camera' "
            "ORDER BY time_received DESC "
            "LIMIT 5"
        ),
    )
    print("SQL results:")
    for row in sql_results:
        print(f"  {row}")

    # Query with MQL -- count entries by component
    mql_results = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        mql_binary=[
            {"$group": {"_id": "$component_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ],
    )
    print("\nCapture counts by component:")
    for entry in mql_results:
        print(f"  {entry}")

    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Replace `YOUR-API-KEY`, `YOUR-API-KEY-ID`, and `YOUR-ORGANIZATION-ID` with your
values. Find your organization ID in the Viam app under **Settings** in the left
navigation.

Run it:

```bash
python query_data.py
```

You should see your captured data printed to the console.

{{% /tab %}}
{{% tab name="Go" %}}

Initialize a Go module and install the SDK:

```bash
mkdir query-data && cd query-data
go mod init query-data
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

func main() {
    apiKey := "YOUR-API-KEY"
    apiKeyID := "YOUR-API-KEY-ID"
    orgID := "YOUR-ORGANIZATION-ID"

    ctx := context.Background()
    logger := logging.NewDebugLogger("query-data")

    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, apiKey, apiKeyID, logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    // Query with SQL -- get recent readings
    sqlResults, err := dataClient.TabularDataBySQL(ctx, orgID,
        "SELECT * FROM readings WHERE component_name = 'my-camera' ORDER BY time_received DESC LIMIT 5")
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Println("SQL results:")
    for _, row := range sqlResults {
        fmt.Printf("  %v\n", row)
    }

    // Query with MQL -- count entries by component
    mqlStages := []map[string]interface{}{
        {"$group": map[string]interface{}{
            "_id":   "$component_name",
            "count": map[string]interface{}{"$sum": 1},
        }},
        {"$sort": map[string]interface{}{"count": -1}},
    }

    mqlResults, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, nil)
    if err != nil {
        logger.Fatal(err)
    }
    fmt.Println("\nCapture counts by component:")
    for _, entry := range mqlResults {
        fmt.Printf("  %v\n", entry)
    }
}
```

Replace the placeholder values with your API key, API key ID, and organization
ID. Then run:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "No data appears in the Data tab" >}}

- **Wait a minute.** Data must be captured locally and then synced to the cloud.
  The first entries can take 30-60 seconds to appear.
- **Is the data management service enabled?** Go to your machine's
  **CONFIGURE** tab and check that the data management service exists and both
  **Capturing** and **Syncing** are toggled on.
- **Is capture configured on the component?** Verify that the component's Data
  capture section shows at least one method with a non-zero frequency.
- **Is the machine online?** Data syncs only when the machine has a network
  connection. Check the machine's status indicator in the Viam app.

{{< /expand >}}

{{< expand "Data appears but images are missing or blank" >}}

- Verify the camera works in the test panel first. If the test panel shows
  nothing, the issue is with the camera configuration, not data capture.
- Check that the capture method is **GetImages**, not another method.

{{< /expand >}}

{{< expand "Data capture frequency seems wrong" >}}

- The frequency is in hertz (captures per second), not seconds between captures.
  `0.5` Hz means once every 2 seconds, not twice per second.
- High-frequency capture (above 1 Hz for cameras) generates large amounts of
  data. Start with `0.5` Hz or lower unless you need high-frequency capture.

{{< /expand >}}

{{< expand "Local disk filling up" >}}

- By default, captured data is stored in `~/.viam/capture` before syncing. If
  sync is disabled or the machine is offline for an extended period, this
  directory can grow large.
- Re-enable sync or manually clear the capture directory if needed.
- Check that the **Syncing** toggle is on in the data management service
  configuration.

{{< /expand >}}

{{< expand "Machine health alert not received" >}}

- Check that you entered your email address correctly in the trigger
  configuration.
- Look in your spam/junk folder.
- Alerts fire when the machine's connection status changes. If the machine was
  already offline when you configured the trigger, the alert won't fire
  retroactively -- it fires on the next status change.

{{< /expand >}}

{{< expand "Programmatic query returns empty results" >}}

- Verify your organization ID is correct. Find it in the Viam app under
  **Settings**.
- Make sure you're querying the right component name. Component names are
  case-sensitive and must match exactly.
- Confirm that data has actually synced to the cloud (visible in the Data tab)
  before querying.

{{< /expand >}}

## What's Next

- [Query Data](/data/query/query-data/) -- write more advanced queries, set up
  data pipelines, and export data.
- [Add Computer Vision](/vision/configure/) -- run ML
  models on your camera feed and capture detection results.
- [Create a Dataset](/train/create-a-dataset/) -- organize captured images
  into training datasets for machine learning.
- [Supported Resources](/data/#supported-resources) -- which components
  and services support data capture.
- [Advanced Configuration](/data/capture-sync/advanced-data-capture-sync/) --
  JSON-level config, retention policies, and sync optimization.
