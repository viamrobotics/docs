---
linkTitle: "Sync to your database"
title: "Sync data to your database"
weight: 40
layout: "docs"
type: "docs"
description: "Use Viam as an ingestion layer and sync captured data to your own MongoDB database."
date: "2025-01-30"
aliases:
  - /data/export/sync-data-to-your-database/
  - /data/sync-data-to-your-database/
  - /build/data/sync-data-to-your-database/
---

Integrate Viam's captured data with your own database or data infrastructure. This is useful when compliance requires you to control where data resides, when you already have a MongoDB cluster with dashboards and pipelines built on it, or when you want to reduce dependency on any single vendor at the storage layer.

Viam handles reliable machine-to-cloud transport. Your database handles long-term storage, retention, access control, and downstream analytics.

## Choose an approach

| Pattern                   | Mechanism                       | Latency   | Best For                                 |
| ------------------------- | ------------------------------- | --------- | ---------------------------------------- |
| API/SDK queries           | Pull from Viam programmatically | On-demand | Dashboards, bulk export, ad-hoc analysis |
| CLI export                | Batch download to local files   | Manual    | One-time migration, backups              |
| Direct MongoDB connection | Query through connection URI    | On-demand | External tools, custom sync scripts      |

### Viam as ingestion layer

In this architecture, Viam handles everything from the machine to the cloud:
data capture on the machine, local buffering when connectivity drops, and
reliable sync to Viam's cloud storage. Your infrastructure takes over from
there. A sync script or direct connection pulls data from Viam and writes it to
your database. Your team manages retention, access control, roll-ups, and
downstream consumers against your own cluster.

## Steps

### 1. Configure database access credentials

Viam provides a MongoDB Atlas Data Federation interface to your captured data.
Before you can connect, you need to set up credentials.

1. Log in to the Viam CLI:

   ```sh
   viam login
   ```

2. Find your organization ID:

   ```sh
   viam organizations list
   ```

   Copy the ID for the organization whose data you want to access.

3. Configure a database password for your organization. This creates a
   database user tied to your organization:

   ```sh
   viam data database configure --org-id=<YOUR-ORG-ID> --password=<NEW-PASSWORD>
   ```

   Choose a strong password. You will use it in connection URIs and scripts.

4. Retrieve the connection hostname:

   ```sh
   viam data database hostname --org-id=<YOUR-ORG-ID>
   ```

   The output includes the hostname and a connection URI. Save both values.

### 2. Connect to your data with mongosh

With credentials configured, you can connect to your Viam data using any
MongoDB client. This step uses `mongosh` (the MongoDB shell) to verify the
connection and explore your data interactively.

1. Install `mongosh` if you do not have it:

   ```sh
   brew install mongosh
   ```

   On Linux, follow the [mongosh installation guide](https://www.mongodb.com/docs/mongodb-shell/install/).

2. Connect using the connection URI from step 1:

   ```sh
   mongosh "mongodb://db-user-<YOUR-ORG-ID>:<PASSWORD>@<HOSTNAME>/?ssl=true&authSource=admin"
   ```

   Replace `<YOUR-ORG-ID>`, `<PASSWORD>`, and `<HOSTNAME>` with your values.

3. Switch to the sensor data database:

   ```text
   use sensorData
   ```

4. List available collections:

   ```text
   show collections
   ```

   You should see a `readings` collection containing your captured tabular data.

5. Query a few documents to verify:

   ```text
   db.readings.find().sort({time_received: -1}).limit(5)
   ```

This connection URI works with any MongoDB-compatible tool: Compass, Studio 3T,
database drivers in any language, or your own applications.

### 3. Export data with the CLI

For one-time exports, backups, or migration, the Viam CLI provides bulk export
commands.

**Export tabular data (sensor readings):**

Tabular export requires you to specify the exact part, resource, and method:

```sh
viam data export tabular \
  --part-id=<YOUR-PART-ID> \
  --resource-name=my-sensor \
  --resource-subtype=sensor \
  --method=Readings \
  --destination=./export
```

You can add time filters to narrow the export:

```sh
viam data export tabular \
  --part-id=<YOUR-PART-ID> \
  --resource-name=my-sensor \
  --resource-subtype=sensor \
  --method=Readings \
  --start=2025-01-01T00:00:00Z \
  --end=2025-02-01T00:00:00Z \
  --destination=./january-export
```

**Export binary data (images, point clouds):**

Binary export supports broad filtering by organization, location, or machine:

```sh
viam data export binary filter --org-ids=<YOUR-ORG-ID> --destination=./export
```

Once exported, you can load these files into your own database, convert them to
CSV for analysis tools, or archive them for compliance.

### 4. Pull data programmatically

For automated workflows, use the Viam SDK to query data from Viam and write it
directly to your own MongoDB cluster.

{{< tabs >}}
{{% tab name="Python" %}}

Install dependencies:

```sh
pip install viam-sdk pymongo
```

Save this as `sync_to_db.py`:

```python
import asyncio
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from pymongo import MongoClient


API_KEY = "<your-api-key>"
API_KEY_ID = "<your-api-key-id>"
ORG_ID = "<your-org-id>"

# Your own MongoDB cluster.
MY_MONGO_URI = "mongodb+srv://user:pass@your-cluster.mongodb.net/"
MY_DB_NAME = "my_robot_data"
MY_COLLECTION_NAME = "sensor_readings"


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
    # Connect to Viam.
    viam_client = await connect()
    data_client = viam_client.data_client

    # Query recent data from Viam.
    data = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        mql_binary=[
            {"$match": {
                "component_name": "my-sensor",
                "time_received": {
                    "$gte": {"$date": "2025-01-01T00:00:00Z"},
                },
            }},
            {"$sort": {"time_received": 1}},
            {"$limit": 1000},
        ],
    )

    print(f"Pulled {len(data)} records from Viam.")

    # Connect to your own database and insert.
    my_client = MongoClient(MY_MONGO_URI)
    my_db = my_client[MY_DB_NAME]
    my_collection = my_db[MY_COLLECTION_NAME]

    inserted = 0
    for record in data:
        my_collection.insert_one(record)
        inserted += 1

    print(f"Inserted {inserted} records into {MY_DB_NAME}.{MY_COLLECTION_NAME}.")

    my_client.close()
    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```sh
python sync_to_db.py
```

{{% /tab %}}
{{% tab name="Go" %}}

Install dependencies:

```sh
mkdir sync-data && cd sync-data
go mod init sync-data
go get go.viam.com/rdk
go get go.mongodb.org/mongo-driver/mongo
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"

    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

func main() {
    apiKey := "YOUR-API-KEY"
    apiKeyID := "YOUR-API-KEY-ID"
    orgID := "YOUR-ORGANIZATION-ID"
    myMongoURI := "mongodb+srv://user:pass@your-cluster.mongodb.net/"

    ctx := context.Background()
    logger := logging.NewDebugLogger("sync-data")

    // Connect to Viam.
    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, apiKey, apiKeyID, logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    // Query recent data from Viam.
    mqlStages := []map[string]interface{}{
        {"$match": map[string]interface{}{
            "component_name": "my-sensor",
            "time_received": map[string]interface{}{
                "$gte": map[string]interface{}{
                    "$date": "2025-01-01T00:00:00Z",
                },
            },
        }},
        {"$sort": map[string]interface{}{"time_received": 1}},
        {"$limit": 1000},
    }
    tabularData, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, nil)
    if err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Pulled %d records from Viam.\n", len(tabularData))

    // Connect to your own MongoDB cluster.
    mongoClient, err := mongo.Connect(ctx,
        options.Client().ApplyURI(myMongoURI))
    if err != nil {
        logger.Fatal(err)
    }
    defer mongoClient.Disconnect(ctx)

    collection := mongoClient.Database("my_robot_data").Collection("sensor_readings")

    inserted := 0
    for _, record := range tabularData {
        _, err := collection.InsertOne(ctx, record)
        if err != nil {
            logger.Errorf("failed to insert record: %v", err)
            continue
        }
        inserted++
    }

    fmt.Printf("Inserted %d records into my_robot_data.sensor_readings.\n", inserted)
}
```

Run it:

```sh
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

To get your credentials, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**. Toggle **Include API key** on and copy the API key and API key ID. Find your organization ID under **Settings** in the left navigation.

### 5. Build an ongoing sync script

A one-time pull is useful, but most teams need ongoing sync. The key is tracking
the last sync timestamp so each run only pulls new data.

{{< tabs >}}
{{% tab name="Python" %}}

Save this as `ongoing_sync.py`:

```python
import asyncio
import json
import os
from datetime import datetime, timezone

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from pymongo import MongoClient


API_KEY = "<your-api-key>"
API_KEY_ID = "<your-api-key-id>"
ORG_ID = "<your-org-id>"
MY_MONGO_URI = "mongodb+srv://user:pass@your-cluster.mongodb.net/"
MY_DB_NAME = "my_robot_data"
MY_COLLECTION_NAME = "sensor_readings"

# File to persist the last sync timestamp between runs.
STATE_FILE = "sync_state.json"


def load_last_sync_time() -> str:
    """Load the last sync timestamp from the state file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
            return state.get("last_sync_time", "2000-01-01T00:00:00Z")
    return "2000-01-01T00:00:00Z"


def save_last_sync_time(timestamp: str) -> None:
    """Save the last sync timestamp to the state file."""
    with open(STATE_FILE, "w") as f:
        json.dump({"last_sync_time": timestamp}, f)


async def connect() -> ViamClient:
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID,
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def sync_once():
    last_sync = load_last_sync_time()
    print(f"Syncing data received after {last_sync}")

    viam_client = await connect()
    data_client = viam_client.data_client

    # Pull only data received since the last sync.
    data = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        mql_binary=[
            {"$match": {
                "time_received": {
                    "$gt": {"$date": last_sync},
                },
            }},
            {"$sort": {"time_received": 1}},
            {"$limit": 5000},
        ],
    )

    if not data:
        print("No new data to sync.")
        viam_client.close()
        return

    print(f"Pulled {len(data)} new records.")

    # Insert into your database.
    my_client = MongoClient(MY_MONGO_URI)
    my_db = my_client[MY_DB_NAME]
    my_collection = my_db[MY_COLLECTION_NAME]

    latest_time = last_sync
    inserted = 0
    for record in data:
        my_collection.insert_one(record)
        inserted += 1
        # Track the most recent timestamp.
        record_time = record.get("time_received", "")
        if hasattr(record_time, "isoformat"):
            record_time = record_time.isoformat()
        if str(record_time) > latest_time:
            latest_time = str(record_time)

    # Persist the latest timestamp for the next run.
    save_last_sync_time(latest_time)
    print(f"Inserted {inserted} records. Last sync time: {latest_time}")

    my_client.close()
    viam_client.close()


if __name__ == "__main__":
    asyncio.run(sync_once())
```

{{% /tab %}}
{{% tab name="Go" %}}

Save this as `main.go`:

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "os"
    "time"

    "go.mongodb.org/mongo-driver/mongo"
    "go.mongodb.org/mongo-driver/mongo/options"
    "go.viam.com/rdk/app"
    "go.viam.com/rdk/logging"
)

const stateFile = "sync_state.json"

type syncState struct {
    LastSyncTime string `json:"last_sync_time"`
}

func loadLastSyncTime() string {
    data, err := os.ReadFile(stateFile)
    if err != nil {
        return "2000-01-01T00:00:00Z"
    }
    var state syncState
    if err := json.Unmarshal(data, &state); err != nil {
        return "2000-01-01T00:00:00Z"
    }
    return state.LastSyncTime
}

func saveLastSyncTime(t string) error {
    data, err := json.Marshal(syncState{LastSyncTime: t})
    if err != nil {
        return err
    }
    return os.WriteFile(stateFile, data, 0644)
}

func main() {
    apiKey := "YOUR-API-KEY"
    apiKeyID := "YOUR-API-KEY-ID"
    orgID := "YOUR-ORGANIZATION-ID"
    myMongoURI := "mongodb+srv://user:pass@your-cluster.mongodb.net/"

    ctx := context.Background()
    logger := logging.NewDebugLogger("sync-data")

    lastSync := loadLastSyncTime()
    fmt.Printf("Syncing data received after %s\n", lastSync)

    // Connect to Viam.
    viamClient, err := app.CreateViamClientWithAPIKey(
        ctx, app.Options{}, apiKey, apiKeyID, logger)
    if err != nil {
        logger.Fatal(err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient()

    // Pull only data received since the last sync.
    mqlStages := []map[string]interface{}{
        {"$match": map[string]interface{}{
            "time_received": map[string]interface{}{
                "$gt": map[string]interface{}{
                    "$date": lastSync,
                },
            },
        }},
        {"$sort": map[string]interface{}{"time_received": 1}},
        {"$limit": 5000},
    }
    tabularData, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, nil)
    if err != nil {
        logger.Fatal(err)
    }

    if len(tabularData) == 0 {
        fmt.Println("No new data to sync.")
        return
    }

    fmt.Printf("Pulled %d new records.\n", len(tabularData))

    // Connect to your own MongoDB cluster.
    mongoClient, err := mongo.Connect(ctx,
        options.Client().ApplyURI(myMongoURI))
    if err != nil {
        logger.Fatal(err)
    }
    defer mongoClient.Disconnect(ctx)

    collection := mongoClient.Database("my_robot_data").Collection("sensor_readings")

    latestTime := lastSync
    inserted := 0
    for _, record := range tabularData {
        _, err := collection.InsertOne(ctx, record)
        if err != nil {
            logger.Errorf("failed to insert record: %v", err)
            continue
        }
        inserted++

        // Track the most recent timestamp.
        if tr, ok := record["time_received"]; ok {
            var ts string
            switch v := tr.(type) {
            case time.Time:
                ts = v.Format(time.RFC3339)
            case string:
                ts = v
            }
            if ts > latestTime {
                latestTime = ts
            }
        }
    }

    // Persist the latest timestamp for the next run.
    if err := saveLastSyncTime(latestTime); err != nil {
        logger.Errorf("failed to save sync state: %v", err)
    }

    fmt.Printf("Inserted %d records. Last sync time: %s\n", inserted, latestTime)
}
```

{{% /tab %}}
{{< /tabs >}}

#### Run on a schedule

Run the sync script on a schedule using cron (Linux/macOS) or Task Scheduler
(Windows). For example, to sync every 15 minutes:

```sh
crontab -e
```

Add this line (adjust the path to your script):

```text
*/15 * * * * cd /path/to/sync-data && python ongoing_sync.py >> sync.log 2>&1
```

For the Go version, compile first and run the binary:

```sh
go build -o sync-data .
```

```text
*/15 * * * * cd /path/to/sync-data && ./sync-data >> sync.log 2>&1
```

## Try It

1. **Configure credentials.** Run the CLI commands from step 1 to set up
   database access. Verify you get a hostname and connection URI back.

2. **Connect with mongosh.** Use the connection URI to connect and run
   `db.readings.find().limit(3)` in the `sensorData` database. Verify you see
   your captured data.

3. **Export with the CLI.** Run `viam data export tabular filter
--org-ids=<YOUR-ORG-ID> --destination=./test-export` and confirm files
   appear in the `./test-export/data/` directory.

4. **Run the one-time sync script.** Copy the Python or Go script from step 4,
   fill in your credentials and MongoDB URI, and run it. Verify records appear
   in your destination database.

5. **Run the ongoing sync script twice.** Run the sync script from step 5. Note
   the count of inserted records. Wait for new data to be captured by your
   machine, then run it again. The second run should only pull data received
   after the first run's latest timestamp.

## Troubleshooting

{{< expand "viam data database configure fails" >}}

- Verify you are logged in: run `viam login` first.
- Verify the organization ID is correct: run `viam organizations list` and
  copy the exact ID.
- The password must meet minimum complexity requirements. Use at least 8
  characters with a mix of letters, numbers, and symbols.

{{< /expand >}}

{{< expand "mongosh connection times out" >}}

- Verify the hostname is correct. Copy it exactly from the output of
  `viam data database hostname`.
- Ensure your network allows outbound connections on port 27017.
- Check that `ssl=true` and `authSource=admin` are both present in the
  connection URI. Without SSL, the connection will be rejected.
- If you are behind a corporate firewall or VPN, you may need to allowlist the
  Data Federation hostname.

{{< /expand >}}

{{< expand "Query returns empty results" >}}

- Verify data has been captured and synced. Check the **DATA** tab in the Viam
  app to confirm entries are visible.
- If filtering by `component_name`, confirm the name matches exactly
  (case-sensitive). Run a query without the component filter first to see what
  data exists.
- If filtering by time, make sure the time range covers a period when data was
  actually captured.

{{< /expand >}}

{{< expand "Authentication error in Python or Go script" >}}

- Verify your API key and API key ID are both correct. These are two separate
  values. The API key is the secret; the API key ID identifies which key is
  being used.
- Verify your organization ID. Find it in the Viam app under **Settings** in
  the left navigation. It is a UUID, not your organization name.
- Check that the API key has data access permissions.

{{< /expand >}}

{{< expand "Duplicate records in destination database" >}}

- The sync scripts do not deduplicate by default. If a run is
  interrupted and restarted, some records may be inserted twice.
- To prevent duplicates, create a unique index on your destination collection
  using a combination of `time_received`, `component_name`, and `robot_id`:

  ```text
  db.sensor_readings.createIndex(
    {time_received: 1, component_name: 1, robot_id: 1},
    {unique: true}
  )
  ```

- Then change `insert_one` to use `update_one` with `upsert=True` (Python) or
  `ReplaceOne` with `Upsert` (Go) to skip duplicates gracefully.

{{< /expand >}}

{{< expand "CLI export is slow or incomplete" >}}

- Large exports download files in parallel, but total time depends on data
  volume and network speed.
- If the export is interrupted, re-run the same command. The CLI resumes where
  it left off.
- Use time range filters (`--start`, `--end`) to break large exports into
  smaller chunks.

{{< /expand >}}

## What's Next

- [Data pipelines](/data/pipelines/create-a-pipeline/) -- set up
  windowed roll-ups and derived metrics to reduce data volume before syncing.
- [Visualize Data](/data/visualize-data/) -- connect Grafana or other
  dashboard tools to your Viam data using the MongoDB connection URI.
- [Query Data](/data/query/query-data/) -- write advanced SQL and MQL queries
  against your data in Viam's cloud before pulling it to your own systems.
