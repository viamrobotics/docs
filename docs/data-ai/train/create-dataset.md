---
linkTitle: "Create a training dataset"
title: "Create a training dataset"
weight: 10
layout: "docs"
type: "docs"
description: "Create a dataset to train a machine learning model."
aliases:
  - /fleet/dataset/
  - /manage/data/label/
  - /manage/data/dataset/
  - /data/dataset/
  - /data-ai/ai/create-dataset/
---

To train a machine learning model, you will need a dataset.

## Create a dataset

You can create a dataset using the web UI, the CLI, or one of the SDKs:

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Navigate to the **DATA** page and open the [**DATASETS** tab](https://app.viam.com/data/datasets).

1. Click the **+ Create dataset** button.

   {{< imgproc src="/services/data/create-dataset.png" alt="The **DATASET** tab of the **DATA** page, showing the **+ Create dataset** button." resize="800x" style="width:500px" class="imgzoom" >}}

1. Enter a unique name for the dataset.

1. Click **Create dataset**.

{{% /tab %}}
{{% tab name="CLI" %}}

Run the following [Viam CLI](/dev/tools/cli/) command to create a dataset, replacing the `<org-id>` and `<name>` placeholders with your organization ID and a unique name for the dataset:

```sh {class="command-line" data-prompt="$"}
viam dataset create --org-id=<org-id> --name=<name>
```

{{% /tab %}}
{{% tab name="Python" %}}

To create a dataset, pass a unique dataset name and organization ID to [`data_client.create_dataset`](/dev/reference/apis/data-client/#createdataset):

```python
viam_client = await connect()
data_client = viam_client.data_client

print("Creating dataset...")

try:
    dataset_id = await data_client.create_dataset(
        name="<dataset_name>",
        organization_id="<org_id>",
    )
    print(f"Created dataset: {dataset_id}")
except Exception as e:
    print("Error creating dataset. It may already exist.")
    print(f"Exception: {e}")
    raise
```

{{% /tab %}}
{{% tab name="Go" %}}

To create a dataset, pass a unique dataset name and organization ID to [`DataClient.CreateDataset`](/dev/reference/apis/data-client/#createdataset):

```go
ctx := context.Background()
viamClient, err := client.New(ctx, "<machine_address>", logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

dataClient := viamClient.DataClient()

fmt.Println("Creating dataset...")

datasetID, err := dataClient.CreateDataset(ctx, &datamanager.CreateDatasetRequest{
    Name:           "<dataset_name>",
    OrganizationID: "<org_id>",
})

if err != nil {
    fmt.Println("Error creating dataset. It may already exist.")
    fmt.Printf("Exception: %v\n", err)
    return
}

fmt.Printf("Created dataset: %s\n", datasetID)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

To create a dataset, pass a unique dataset name and organization ID to [`dataClient.createDataset`](/dev/reference/apis/data-client/#createdataset):

```typescript
const client = await createViamClient();
const dataClient = client.dataClient;

console.log("Creating dataset...");

try {
  const datasetId = await dataClient.createDataset({
    name: "<dataset_name>",
    organizationId: "<org_id>",
  });
  console.log(`Created dataset: ${datasetId}`);
} catch (error) {
  console.log("Error creating dataset. It may already exist.");
  console.log(`Exception: ${error}`);
  process.exit(1);
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

To create a dataset, pass a unique dataset name and organization ID to [`dataClient.createDataset`](/dev/reference/apis/data-client/#createdataset):

```dart
final viamClient = await ViamClient.connect();
final dataClient = viamClient.dataClient;

print("Creating dataset...");

try {
    final datasetId = await dataClient.createDataset(
        name: "<dataset_name>",
        organizationId: "<org_id>",
    );
    print("Created dataset: $datasetId");
} catch (e) {
    print("Error creating dataset. It may already exist.");
    print("Exception: $e");
    return;
}
```

{{% /tab %}}
{{< /tabs >}}

Finish creating a dataset by adding annotated images to it.
You can capture new images or add existing images:

## Add to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. Click to select the images you would like to add to your dataset.

1. Click the **Add to dataset** button in the top right.

1. From the **Dataset** dropdown, select the name of your dataset.

1. Click **Add \<n\> images** to add the selected images to the dataset.

{{< alert title="Tip" color="tip" >}}

To select a range of images, select one image, then hold **Ctrl/Cmd** while clicking another image.
This will select both images as well as the entire range of images between those images.

{{< /alert >}}

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, [create a dataset](/data-ai/train/create-dataset/), if you haven't already.

1. If you just created a dataset, use the dataset ID output by the creation command.
   If your dataset already exists, run the following command to get a list of dataset names and corresponding IDs:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset list
   ```

1. Run the following [command](/dev/tools/cli/#dataset) to add all images labeled with a subset of tags to the dataset, replacing the `<dataset-id>` placeholder with the dataset ID output by the command in the previous step:

   ```sh {class="command-line" data-prompt="$"}
   viam dataset data add filter --dataset-id=<dataset-id> --tags=red_star,blue_square
   ```

{{% /tab %}}
{{% tab name="Python" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`data_client.add_binary_data_to_dataset_by_ids`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

```python
# Connect to Viam client
dial_options = DialOptions(
    credentials=Credentials(
        type="api-key",
        payload=API_KEY,
    ),
    auth_entity=API_KEY_ID,
)

viam_client = await ViamClient.create_from_dial_options(dial_options)
data_client = viam_client.data_client

# Add image to dataset
await data_client.add_binary_data_to_dataset_by_ids(
    binary_ids=[EXISTING_IMAGE_ID],
    dataset_id=EXISTING_DATASET_ID
)

print("Image added to dataset successfully")
viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`DataClient.AddBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

```go
ctx := context.Background()
viamClient, err := client.New(ctx, "<machine_address>", logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

dataClient := viamClient.DataClient()

// Add image to dataset
err = dataClient.AddBinaryDataToDatasetByIDs(
    context.Background(),
    []string{ExistingImageID},
    ExistingDatasetID,
)
if err != nil {
    return fmt.Errorf("failed to add image to dataset: %w", err)
}

fmt.Println("Image added to dataset successfully")
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`dataClient.addBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

```typescript
const client: ViamClient = await createViamClient({
  credential: {
    type: "api-key",
    payload: API_KEY,
  },
  authEntity: API_KEY_ID,
});

const dataClient = client.dataClient;

// Add image to dataset
await dataClient.addBinaryDataToDatasetByIds({
  binaryIds: [EXISTING_IMAGE_ID],
  datasetId: EXISTING_DATASET_ID,
});

console.log("Image added to dataset successfully");
client.disconnect();
```

{{% /tab %}}
{{% tab name="Flutter" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Pass both IDs to [`dataClient.addBinaryDataToDatasetByIDs`](/dev/reference/apis/data-client/#addbinarydatatodatasetbyids):

```dart
final client = await ViamClient.withApiKey(
    apiKeyId: apiKeyId,
    apiKey: apiKey,
);

final dataClient = client.dataClient;

try {
    // Add image to dataset
    await dataClient.addBinaryDataToDatasetByIds(
      binaryIds: [existingImageId],
      datasetId: existingDatasetId,
    );

    print('Image added to dataset successfully');
} finally {
    await client.close();
}
```

{{% /tab %}}
{{< /tabs >}}

## Add all images captured by a specific machine to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset from the **Images** tab of the [**DATA** page](https://app.viam.com/data/view):

1. From the **Machine name** dropdown, select the name of a machine.
1. Click the **Apply** button at the bottom of the left sidebar.
1. Click to select the images you would like to add to your dataset.
1. Click the **Add to dataset** button in the top right.
1. From the **Dataset** dropdown, select the name of your dataset.
1. Click **Add \<n\> images** to add the selected images to the dataset.

{{< alert title="Tip" color="tip" >}}

To select a range of images, select one image, then hold **Ctrl/Cmd** while clicking another image.
This will select both images as well as the entire range of images between those images.

{{< /alert >}}

{{% /tab %}}
{{% tab name="Python" %}}

The following script adds all images captured from a certain machine to a new dataset:

```python
import asyncio
from typing import List, Optional

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.utils import create_filter

# Configuration constants – replace with your actual values
DATASET_NAME = ""  # a unique, new name for the dataset you want to create
ORG_ID = ""  # your organization ID, find in your organization settings
PART_ID = ""  # ID of machine that captured images, find in machine config
API_KEY = ""  # API key, find or create in your organization settings
API_KEY_ID = ""  # API key ID, find or create in your organization settings

# Adjust the maximum number of images to add to the dataset
MAX_MATCHES = 500


async def connect() -> ViamClient:
    """Establish a connection to the Viam client using API credentials."""
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID,
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def fetch_binary_data_ids(data_client, part_id: str) -> List[str]:
    """Fetch binary data metadata and return a list of BinaryData objects."""
    data_filter = create_filter(part_id=part_id)
    all_matches = []
    last: Optional[str] = None

    print("Getting data for part...")

    while len(all_matches) < MAX_MATCHES:
        print("Fetching more data...")
        data, _, last = await data_client.binary_data_by_filter(
            data_filter,
            limit=50,
            last=last,
            include_binary_data=False,
        )
        if not data:
            break
        all_matches.extend(data)

    return all_matches


async def main() -> int:
    """Main execution function."""
    viam_client = await connect()
    data_client = viam_client.data_client

    matching_data = await fetch_binary_data_ids(data_client, PART_ID)

    print("Creating dataset...")

    try:
        dataset_id = await data_client.create_dataset(
            name=DATASET_NAME,
            organization_id=ORG_ID,
        )
        print(f"Created dataset: {dataset_id}")
    except Exception as e:
        print("Error creating dataset. It may already exist.")
        print("See: https://app.viam.com/data/datasets")
        print(f"Exception: {e}")
        return 1

    print("Adding data to dataset...")

    await data_client.add_binary_data_to_dataset_by_ids(
        binary_ids=[
            obj.metadata.binary_data_id for obj in matching_data
        ],
        dataset_id=dataset_id
    )

    print("Added files to dataset.")
    print(
        f"See dataset: https://app.viam.com/data/datasets?id={dataset_id}"
    )

    viam_client.close()
    return 0

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

The following script adds all images captured from a certain machine to a new dataset:

```go
package main

import (
    "context"
    "fmt"
    "log"

    "go.viam.com/rdk/rpc"
    "go.viam.com/utils"
    "go.viam.com/rdk/app"
    "go.viam.com/rdk/app/data"
)

// Configuration constants - replace with your actual values
const (
    DATASET_NAME = "" // a unique, new name for the dataset you want to create
    ORG_ID       = "" // your organization ID, find in your organization settings
    PART_ID      = "" // ID of machine that captured target images, find in machine config
    API_KEY      = "" // API key, find or create in your organization settings
    API_KEY_ID   = "" // API key ID, find or create in your organization settings
    MAX_MATCHES  = 500
)

func connect(ctx context.Context) (*app.ViamClient, error) {
    client, err := app.NewViamClientWithAPIKey(ctx, API_KEY, API_KEY_ID)
    if err != nil {
        return nil, fmt.Errorf("failed to create client: %w", err)
    }
    return client, nil
}

func fetchBinaryDataIDs(
                ctx context.Context,
                dataClient data.DataServiceClient,
                partID string) ([]*data.BinaryData, error) {
    filter := &data.Filter{
        PartId: partID,
    }

    var allMatches []*data.BinaryData
    var last string

    fmt.Println("Getting data for part...")

    for len(allMatches) < MAX_MATCHES {
        fmt.Println("Fetching more data...")

        resp, err := dataClient.BinaryDataByFilter(ctx, &data.BinaryDataByFilterRequest{
            DataRequest: &data.DataRequest{
                Filter:            filter,
                Limit:             50,
                Last:              last,
                IncludeBinaryData: false,
            },
        })
        if err != nil {
            return nil, fmt.Errorf("failed to fetch binary data: %w", err)
        }

        if len(resp.Data) == 0 {
            break
        }

        allMatches = append(allMatches, resp.Data...)
        last = resp.Last
    }

    return allMatches, nil
}

func main() {
    ctx := context.Background()

    viamClient, err := connect(ctx)
    if err != nil {
        log.Fatalf("Connection failed: %v", err)
    }
    defer viamClient.Close()

    dataClient := viamClient.DataClient

    matchingData, err := fetchBinaryDataIDs(ctx, dataClient, PART_ID)
    if err != nil {
        log.Fatalf("Failed to fetch binary data: %v", err)
    }

    fmt.Println("Creating dataset...")

    datasetResp, err := dataClient.CreateDataset(ctx, &data.CreateDatasetRequest{
        Name:           DATASET_NAME,
        OrganizationId: ORG_ID,
    })
    if err != nil {
        fmt.Println("Error creating dataset. It may already exist.")
        fmt.Println("See: https://app.viam.com/data/datasets")
        fmt.Printf("Exception: %v\n", err)
        return
    }

    datasetID := datasetResp.Id
    fmt.Printf("Created dataset: %s\n", datasetID)

    fmt.Println("Adding data to dataset...")

    var binaryIDs []string
    for _, obj := range matchingData {
        binaryIDs = append(binaryIDs, obj.Metadata.Id)
    }

    _, err = dataClient.AddBinaryDataToDatasetByIds(ctx, &data.AddBinaryDataToDatasetByIdsRequest{
        BinaryIds: binaryIDs,
        DatasetId: datasetID,
    })
    if err != nil {
        log.Fatalf("Failed to add binary data to dataset: %v", err)
    }

    fmt.Println("Added files to dataset.")
    fmt.Printf("See dataset: https://app.viam.com/data/datasets?id=%s\n", datasetID)
}

```

{{% /tab %}}
{{% tab name="TypeScript" %}}

The following script adds all images captured from a certain machine to a new dataset:

```typescript
import { ViamClient, createViamClient } from "@viamrobotics/sdk";
import { DataServiceClient } from "@viamrobotics/sdk/dist/gen/app/data/v1/data_pb_service";
import {
  BinaryDataByFilterRequest,
  CreateDatasetRequest,
  AddBinaryDataToDatasetByIdsRequest,
  Filter,
  DataRequest,
} from "@viamrobotics/sdk/dist/gen/app/data/v1/data_pb";

// Configuration constants - replace with your actual values
const DATASET_NAME = ""; // a unique, new name for the dataset you want to create
const ORG_ID = ""; // your organization ID, find in your organization settings
const PART_ID = ""; // ID of machine that captured target images, find in machine config
const API_KEY = ""; // API key, find or create in your organization settings
const API_KEY_ID = ""; // API key ID, find or create in your organization settings
const MAX_MATCHES = 500;

async function connect(): Promise<ViamClient> {
  return await createViamClient({
    credential: {
      type: "api-key",
      authEntity: API_KEY_ID,
      payload: API_KEY,
    },
  });
}

async function fetchBinaryDataIds(
  dataClient: DataServiceClient,
  partId: string,
): Promise<any[]> {
  const filter = new Filter();
  filter.setPartId(partId);

  const allMatches: any[] = [];
  let last = "";

  console.log("Getting data for part...");

  while (allMatches.length < MAX_MATCHES) {
    console.log("Fetching more data...");

    const dataRequest = new DataRequest();
    dataRequest.setFilter(filter);
    dataRequest.setLimit(50);
    dataRequest.setLast(last);
    dataRequest.setIncludeBinaryData(false);

    const request = new BinaryDataByFilterRequest();
    request.setDataRequest(dataRequest);

    const response = await dataClient.binaryDataByFilter(request);
    const data = response.getDataList();

    if (data.length === 0) {
      break;
    }

    allMatches.push(...data);
    last = response.getLast();
  }

  return allMatches;
}

async function main(): Promise<number> {
  const viamClient = await connect();
  const dataClient = viamClient.dataClient;

  const matchingData = await fetchBinaryDataIds(dataClient, PART_ID);

  console.log("Creating dataset...");

  try {
    const createRequest = new CreateDatasetRequest();
    createRequest.setName(DATASET_NAME);
    createRequest.setOrganizationId(ORG_ID);

    const datasetResponse = await dataClient.createDataset(createRequest);
    const datasetId = datasetResponse.getId();
    console.log(`Created dataset: ${datasetId}`);

    console.log("Adding data to dataset...");

    const binaryIds = matchingData.map(
      (obj) => obj.getMetadata()?.getId() || "",
    );

    const addRequest = new AddBinaryDataToDatasetByIdsRequest();
    addRequest.setBinaryIdsList(binaryIds);
    addRequest.setDatasetId(datasetId);

    await dataClient.addBinaryDataToDatasetByIds(addRequest);

    console.log("Added files to dataset.");
    console.log(
      `See dataset: https://app.viam.com/data/datasets?id=${datasetId}`,
    );

    viamClient.disconnect();
    return 0;
  } catch (error) {
    console.log("Error creating dataset. It may already exist.");
    console.log("See: https://app.viam.com/data/datasets");
    console.log(`Exception: ${error}`);
    viamClient.disconnect();
    return 1;
  }
}

if (require.main === module) {
  main().then((code) => process.exit(code));
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

The following script adds all images captured from a certain machine to a new dataset:

```dart
import 'package:viam_sdk/viam_sdk.dart';

// Configuration constants - replace with your actual values
const String datasetName = ""; // a unique, new name for the dataset you want to create
const String orgId = ""; // your organization ID, find in your organization settings
const String partId = ""; // ID of machine that captured target images, find in machine config
const String apiKey = ""; // API key, find or create in your organization settings
const String apiKeyId = ""; // API key ID, find or create in your organization settings
const int maxMatches = 500;

Future<ViamClient> connect() async {
  return await ViamClient.withApiKey(
    apiKey: apiKey,
    apiKeyId: apiKeyId,
  );
}

Future<List<BinaryData>> fetchBinaryDataIds(
    DataClient dataClient, String partId) async {
  final filter = Filter(partId: partId);
  final List<BinaryData> allMatches = [];
  String? last;

  print("Getting data for part...");

  while (allMatches.length < maxMatches) {
    print("Fetching more data...");

    final response = await dataClient.binaryDataByFilter(
      filter: filter,
      limit: 50,
      last: last,
      includeBinaryData: false,
    );

    if (response.data.isEmpty) {
      break;
    }

    allMatches.addAll(response.data);
    last = response.last;
  }

  return allMatches;
}

Future<int> main() async {
  final viamClient = await connect();
  final dataClient = viamClient.dataClient;

  final matchingData = await fetchBinaryDataIds(dataClient, partId);

  print("Creating dataset...");

  try {
    final datasetId = await dataClient.createDataset(
      name: datasetName,
      organizationId: orgId,
    );
    print("Created dataset: $datasetId");

    print("Adding data to dataset...");

    final binaryIds = matchingData
        .map((obj) => obj.metadata.binaryDataId)
        .toList();

    await dataClient.addBinaryDataToDatasetByIds(
      binaryIds: binaryIds,
      datasetId: datasetId,
    );

    print("Added files to dataset.");
    print("See dataset: https://app.viam.com/data/datasets?id=$datasetId");

    viamClient.close();
    return 0;

  } catch (error) {
    print("Error creating dataset. It may already exist.");
    print("See: https://app.viam.com/data/datasets");
    print("Exception: $error");
    viamClient.close();
    return 1;
  }
}
```

{{% /tab %}}
{{< /tabs >}}
