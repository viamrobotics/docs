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

The following script adds all images captured from a certain machine to a new dataset:

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

## Capture, annotate, and add images to a dataset

The following example demonstrates how you can capture an image, use an ML model to generate annotations, and then add the image to a dataset.
You can use this logic to expand and improve your datasets continuously over time as your application runs.
Re-train your ML model on the improved dataset to improve the ML model.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import os
import time
from typing import Optional
from io import BytesIO

from PIL import Image
from viam.app.app_client import AppClient
from viam.logging import getLogger

# Global machine configuration
MACHINE_PART_ID = "your-machine-part-id-here"


class DataCollector:
    def __init__(self,
                 component_name: str, dataset_id: str,
                 api_key_id: str, api_key: str):

        self.logger = getLogger(__name__)
        self.component_name = component_name
        self.dataset_id = dataset_id
        self.api_key_id = api_key_id
        self.api_key = api_key

    async def capture_and_store_image(self,
                                      processed_image: Image.Image,
                                      classification: str) -> None:

        if not MACHINE_PART_ID:
            raise ValueError("machine part ID not configured")

        # Create fresh data client connection
        async with await self._create_data_client() as data_client:
            image_data = self._encode_image_to_png(processed_image)

            # Generate unique filename with timestamp
            timestamp = int(time.time())
            filename = f"{classification}-sample-{timestamp}.png"

            component_type = "rdk:component:camera"

            upload_metadata = {
                "component_type": component_type,
                "component_name": self.component_name,
                "file_name": filename,
                "file_extension": "png"
            }

            try:
                file_id = await data_client.file_upload_from_bytes(
                    part_id=MACHINE_PART_ID,
                    data=image_data,
                    **upload_metadata
                )

                # Associate file with dataset immediately
                await data_client.add_binary_data_to_dataset_by_ids(
                    binary_ids=[file_id],
                    dataset_id=self.dataset_id
                )

                self.logger.info(
                    f"successfully added {classification} image to dataset "
                    f"{self.dataset_id} (file ID: {file_id}, "
                    f"machine: {MACHINE_PART_ID})"
                )

            except Exception as e:
                self.logger.error(f"failed to upload and associate image: {e}")
                raise

    async def _create_data_client(self) -> AppClient:
        if not self.api_key_id or not self.api_key:
            raise ValueError("API credentials not configured")

        try:
            client = AppClient.create_from_dial_options(
                dial_options={
                    "auth_entity": self.api_key_id,
                    "credentials": {
                        "type": "api-key",
                        "payload": self.api_key
                    }
                }
            )
            return client

        except Exception as e:
            raise ValueError(f"failed to create app client: {e}")

    def _encode_image_to_png(self, img: Image.Image) -> bytes:
        buffer = BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        return buffer.getvalue()


def create_data_collector(
                    component_name: str,
                    dataset_id: str,
                    api_key_id: str,
                    api_key: str
                ) -> DataCollector:
    if not component_name:
        raise ValueError("component name is required")
    if not dataset_id:
        raise ValueError("dataset ID is required")
    if not api_key_id or not api_key:
        raise ValueError("API credentials are required")

    return DataCollector(
        component_name=component_name,
        dataset_id=dataset_id,
        api_key_id=api_key_id,
        api_key=api_key
    )


# Example usage
async def main():
    collector = create_data_collector(
        component_name="main_camera",
        dataset_id="your-dataset-id",
        api_key_id="your-api-key-id",
        api_key="your-api-key"
    )

    # Example with PIL Image
    sample_image = Image.new('RGB', (640, 480), color='red')
    await collector.capture_and_store_image(sample_image, "positive_sample")

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package datasetcreation

import (
    "context"
    "fmt"
    "image"
    "time"

    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/services/datamanager/app"
    "go.viam.com/rdk/app/appclient"
)

var MachinePartID string = "your-machine-part-id-here"

type DataCollector struct {
    logger         logging.Logger
    componentName  string
    datasetID      string
    apiKeyID       string
    apiKey         string
}

func (dc *DataCollector) CaptureAndStoreImage(ctx context.Context, processedImage image.Image, classification string) error {
    if MachinePartID == "" {
        return fmt.Errorf("machine part ID not configured")
    }

    // Create fresh data client connection
    dataClient, err := dc.createDataClient(ctx)
    if err != nil {
        dc.logger.Errorf("failed to create data client: %v", err)
        return fmt.Errorf("data client initialization failed: %w", err)
    }
    defer dataClient.Close()

    imageData, err := dc.encodeImageToPNG(processedImage)
    if err != nil {
        dc.logger.Errorf("image encoding failed: %v", err)
        return fmt.Errorf("failed to encode image: %w", err)
    }

    // Generate unique filename with timestamp
    timestamp := time.Now().Unix()
    filename := fmt.Sprintf("%s-sample-%d.png", classification, timestamp)

    componentType := "rdk:component:camera"
    fileExtension := "png"

    uploadOptions := app.FileUploadOptions{
        ComponentType: &componentType,
        ComponentName: &dc.componentName,
        FileName:      &filename,
        FileExtension: &fileExtension,
    }

    fileID, err := dataClient.FileUploadFromBytes(ctx, MachinePartID, imageData, &uploadOptions)
    if err != nil {
        dc.logger.Errorf("file upload failed for %s: %v", filename, err)
        return fmt.Errorf("failed to upload image: %w", err)
    }

    // Associate file with dataset immediately
    err = dataClient.AddBinaryDataToDatasetByIDs(ctx, []string{fileID}, dc.datasetID)
    if err != nil {
        dc.logger.Errorf("dataset association failed for file %s: %v", fileID, err)
        return fmt.Errorf("failed to add image to dataset: %w", err)
    }

    dc.logger.Infof("successfully added %s image to dataset %s (file ID: %s, machine: %s)",
        classification, dc.datasetID, fileID, MachinePartID)

    return nil
}

func (dc *DataCollector) createDataClient(ctx context.Context) (app.AppServiceClient, error) {
    if dc.apiKeyID == "" || dc.apiKey == "" {
        return nil, fmt.Errorf("API credentials not configured")
    }

    client, err := appclient.New(ctx, appclient.Config{
        KeyID: dc.apiKeyID,
        Key:   dc.apiKey,
    })
    if err != nil {
        return nil, fmt.Errorf("failed to create app client: %w", err)
    }

    return client.DataClient, nil
}

func (dc *DataCollector) encodeImageToPNG(img image.Image) ([]byte, error) {
    // PNG encoding implementation
    return nil, nil // Placeholder
}

func NewDataCollector(logger logging.Logger, componentName, datasetID, apiKeyID, apiKey string) (*DataCollector, error) {
    if logger == nil {
        return nil, fmt.Errorf("logger is required")
    }
    if componentName == "" {
        return nil, fmt.Errorf("component name is required")
    }
    if datasetID == "" {
        return nil, fmt.Errorf("dataset ID is required")
    }
    if apiKeyID == "" || apiKey == "" {
        return nil, fmt.Errorf("API credentials are required")
    }

    return &DataCollector{
        logger:        logger,
        componentName: componentName,
        datasetID:     datasetID,
        apiKeyID:      apiKeyID,
        apiKey:        apiKey,
    }, nil
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```typescript
import { createRobotClient, RobotClient } from "@viamrobotics/sdk";
import { AppClient, DataClient } from "@viamrobotics/app-client";
import { Logger } from "@viamrobotics/utils";

const MACHINE_PART_ID: string = "your-machine-part-id-here";

interface FileUploadOptions {
  componentType?: string;
  componentName?: string;
  fileName?: string;
  fileExtension?: string;
}

export class DataCollector {
  private logger: Logger;
  private componentName: string;
  private datasetId: string;
  private apiKeyId: string;
  private apiKey: string;

  constructor(
    logger: Logger,
    componentName: string,
    datasetId: string,
    apiKeyId: string,
    apiKey: string,
  ) {
    this.logger = logger;
    this.componentName = componentName;
    this.datasetId = datasetId;
    this.apiKeyId = apiKeyId;
    this.apiKey = apiKey;
  }

  async captureAndStoreImage(
    processedImage: ArrayBuffer,
    classification: string,
  ): Promise<void> {
    if (!MACHINE_PART_ID) {
      throw new Error("Machine part ID not configured");
    }

    let dataClient: DataClient | null = null;

    try {
      dataClient = await this.createDataClient();

      const imageData = await this.encodeImageToPng(processedImage);
      const timestamp = Math.floor(Date.now() / 1000);
      const filename = `${classification}-sample-${timestamp}.png`;

      const componentType = "rdk:component:camera";
      const fileExtension = "png";

      const uploadOptions: FileUploadOptions = {
        componentType,
        componentName: this.componentName,
        fileName: filename,
        fileExtension,
      };

      const fileId = await dataClient.fileUploadFromBytes(
        MACHINE_PART_ID,
        new Uint8Array(imageData),
        uploadOptions,
      );

      await dataClient.addBinaryDataToDatasetByIds([fileId], this.datasetId);

      this.logger.info(
        `Successfully added ${classification} image to dataset ${this.datasetId} ` +
          `(file ID: ${fileId}, machine: ${MACHINE_PART_ID})`,
      );
    } catch (error) {
      this.logger.error(`File upload failed for ${classification}: ${error}`);
      throw new Error(`Failed to upload image: ${error}`);
    } finally {
      if (dataClient) {
        await dataClient.close();
      }
    }
  }

  private async createDataClient(): Promise<DataClient> {
    if (!this.apiKeyId || !this.apiKey) {
      throw new Error("API credentials not configured");
    }

    const appClient = new AppClient({
      apiKeyId: this.apiKeyId,
      apiKey: this.apiKey,
    });

    return appClient.dataClient();
  }

  private async encodeImageToPng(image: ArrayBuffer): Promise<ArrayBuffer> {
    try {
      // PNG encoding implementation would depend on your image processing library
      // This is a placeholder - you would use a library like 'pngjs' or 'canvas'
      return image; // Assuming image is already PNG encoded
    } catch (error) {
      this.logger.error(`Image encoding failed: ${error}`);
      throw new Error(`Failed to encode image: ${error}`);
    }
  }

  static create(
    logger: Logger,
    componentName: string,
    datasetId: string,
    apiKeyId: string,
    apiKey: string,
  ): DataCollector {
    if (!logger) {
      throw new Error("Logger is required");
    }
    if (!componentName) {
      throw new Error("Component name is required");
    }
    if (!datasetId) {
      throw new Error("Dataset ID is required");
    }
    if (!apiKeyId || !apiKey) {
      throw new Error("API credentials are required");
    }

    return new DataCollector(
      logger,
      componentName,
      datasetId,
      apiKeyId,
      apiKey,
    );
  }
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
import 'dart:typed_data';
import 'dart:io';
import 'package:viam_sdk/viam_sdk.dart';
import 'package:viam_sdk/src/app/app_client.dart';
import 'package:viam_sdk/src/app/data_client.dart';
import 'package:image/image.dart' as img;

const String machinePartId = 'your-machine-part-id-here';

class DataCollector {
  final Logging logger;
  final String componentName;
  final String datasetId;
  final String apiKeyId;
  final String apiKey;

  DataCollector({
    required this.logger,
    required this.componentName,
    required this.datasetId,
    required this.apiKeyId,
    required this.apiKey,
  });

  Future<void> captureAndStoreImage(
    Image processedImage,
    String classification,
  ) async {
    if (machinePartId.isEmpty) {
      throw Exception('Machine part ID not configured');
    }

    DataClient? dataClient;
    try {
      dataClient = await _createDataClient();

      final imageData = await _encodeImageToPng(processedImage);
      final timestamp = DateTime.now().millisecondsSinceEpoch ~/ 1000;
      final filename = '$classification-sample-$timestamp.png';

      const componentType = 'rdk:component:camera';
      const fileExtension = 'png';

      final uploadOptions = FileUploadOptions(
        componentType: componentType,
        componentName: componentName,
        fileName: filename,
        fileExtension: fileExtension,
      );

      final fileId = await dataClient.fileUploadFromBytes(
        machinePartId,
        imageData,
        uploadOptions,
      );

      await dataClient.addBinaryDataToDatasetByIds(
        [fileId],
        datasetId,
      );

      logger.info(
        'Successfully added $classification image to dataset $datasetId '
        '(file ID: $fileId, machine: $machinePartId)',
      );
    } catch (error) {
      logger.error('File upload failed for $classification: $error');
      rethrow;
    } finally {
      await dataClient?.close();
    }
  }

  Future<DataClient> _createDataClient() async {
    if (apiKeyId.isEmpty || apiKey.isEmpty) {
      throw Exception('API credentials not configured');
    }

    final appClient = await AppClient.withApiKey(
      apiKeyId: apiKeyId,
      apiKey: apiKey,
    );

    return appClient.dataClient;
  }

  Future<Uint8List> _encodeImageToPng(Image image) async {
    try {
      final pngBytes = img.encodePng(image);
      return Uint8List.fromList(pngBytes);
    } catch (error) {
      logger.error('Image encoding failed: $error');
      throw Exception('Failed to encode image: $error');
    }
  }

  static DataCollector create({
    required Logging logger,
    required String componentName,
    required String datasetId,
    required String apiKeyId,
    required String apiKey,
  }) {
    if (componentName.isEmpty) {
      throw ArgumentError('Component name is required');
    }
    if (datasetId.isEmpty) {
      throw ArgumentError('Dataset ID is required');
    }
    if (apiKeyId.isEmpty || apiKey.isEmpty) {
      throw ArgumentError('API credentials are required');
    }

    return DataCollector(
      logger: logger,
      componentName: componentName,
      datasetId: datasetId,
      apiKeyId: apiKeyId,
      apiKey: apiKey,
    );
  }
}
```

{{% /tab %}}
{{< /tabs >}}
