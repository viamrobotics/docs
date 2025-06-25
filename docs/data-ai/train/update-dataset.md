---
linkTitle: "Add to a training dataset"
title: "Add to a training dataset"
weight: 30
layout: "docs"
type: "docs"
description: "Update a dataset used to train a machine learning model."
---

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand%}}

## Add to a dataset

{{< tabs >}}
{{% tab name="Web UI" %}}

1. Open the [**DATA** page](https://app.viam.com/data/view).

1. Navigate to the **ALL DATA** tab.

1. Use the checkbox in the upper left of each image to select labeled images.

1. Click the **Add to dataset** button, select a dataset, and click the **Add ... images** button to add the selected images to the dataset.

{{% /tab %}}
{{% tab name="CLI" %}}

Use the Viam CLI to filter images by label and add the filtered images to a dataset:

1. First, [create a dataset](#create-a-dataset), if you haven't already.

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
{{% tab name="SDK" %}}

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from PIL import Image
from viam.app.app_client import AppClient
from viam.app.data_client import DataClient

MACHINE_PART_ID = "your-machine-part-id-here"
DATASET_ID = "your-dataset-id-here"
API_KEY_ID = "your-api-key-id"
API_KEY = "your-api-key"

async def add_image_to_dataset():
    """Add image to Viam dataset using Python SDK"""

    # Initialize app client
    app_client = AppClient.create_from_api_key(
        api_key_id=API_KEY_ID,
        api_key=API_KEY
    )

    try:
        # Get data client
        data_client = app_client.data_client

        # Load image file
        image_path = "sample_image.jpg"
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Upload image to Viam cloud
        file_upload_metadata = await data_client.file_upload_from_bytes(
            part_id=MACHINE_PART_ID,
            data=image_data,
            component_type="camera",
            component_name="camera-1",
            file_name="training_sample.jpg",
            file_extension="jpg"
        )

        file_id = file_upload_metadata.file_id
        print(f"Image uploaded successfully. File ID: {file_id}")

        # Add uploaded file to dataset
        await data_client.add_binary_data_to_dataset_by_ids(
            binary_ids=[file_id],
            dataset_id=DATASET_ID
        )

        print(f"Image added to dataset {DATASET_ID} successfully")

    except Exception as error:
        print(f"Operation failed: {error}")
        raise

    finally:
        app_client.close()

# Execute function
if __name__ == "__main__":
    asyncio.run(add_image_to_dataset())

```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"
    "os"
    "time"

    "go.viam.com/rdk/app/appclient"
    "go.viam.com/rdk/services/datamanager/app"
)

const (
    MachinePartID = "your-machine-part-id-here"
    DatasetID     = "your-dataset-id-here"
    APIKeyID      = "your-api-key-id"
    APIKey        = "your-api-key"
)

func addImageToDataset() error {
    ctx := context.Background()

    // Create app client
    client, err := appclient.New(ctx, appclient.Config{
        KeyID: APIKeyID,
        Key:   APIKey,
    })
    if err != nil {
        return fmt.Errorf("failed to create app client: %w", err)
    }
    defer client.Close()

    // Get data client
    dataClient := client.DataClient

    // Read image file
    imagePath := "sample_image.jpg"
    imageData, err := os.ReadFile(imagePath)
    if err != nil {
        return fmt.Errorf("failed to read image file: %w", err)
    }

    // Prepare upload options
    componentType := "camera"
    componentName := "camera-1"
    fileName := fmt.Sprintf("training_sample_%d.jpg", time.Now().Unix())
    fileExtension := "jpg"

    uploadOptions := app.FileUploadOptions{
        ComponentType: &componentType,
        ComponentName: &componentName,
        FileName:      &fileName,
        FileExtension: &fileExtension,
    }

    // Upload image
    fileID, err := dataClient.FileUploadFromBytes(
        ctx,
        MachinePartID,
        imageData,
        &uploadOptions,
    )
    if err != nil {
        return fmt.Errorf("failed to upload image: %w", err)
    }

    fmt.Printf("Image uploaded successfully. File ID: %s\n", fileID)

    // Add file to dataset
    err = dataClient.AddBinaryDataToDatasetByIDs(
        ctx,
        []string{fileID},
        DatasetID,
    )
    if err != nil {
        return fmt.Errorf("failed to add image to dataset: %w", err)
    }

    fmt.Printf("Image added to dataset %s successfully\n", DatasetID)
    return nil
}

func main() {
    if err := addImageToDataset(); err != nil {
        fmt.Printf("Operation failed: %v\n", err)
        os.Exit(1)
    }
}

```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```typescript
import { createAppClient } from "@viamrobotics/app-client";
import { promises as fs } from "fs";

const MACHINE_PART_ID = "your-machine-part-id-here";
const DATASET_ID = "your-dataset-id-here";
const API_KEY_ID = "your-api-key-id";
const API_KEY = "your-api-key";

async function addImageToDataset(): Promise<void> {
  // Create app client
  const appClient = createAppClient({
    apiKeyId: API_KEY_ID,
    apiKey: API_KEY,
  });

  try {
    // Get data client
    const dataClient = appClient.dataClient();

    // Read image file
    const imagePath = "sample_image.jpg";
    const imageBuffer = await fs.readFile(imagePath);
    const imageData = new Uint8Array(imageBuffer);

    // Upload image
    const uploadResponse = await dataClient.fileUploadFromBytes({
      partId: MACHINE_PART_ID,
      data: imageData,
      componentType: "camera",
      componentName: "camera-1",
      fileName: `training_sample_${Date.now()}.jpg`,
      fileExtension: "jpg",
    });

    const fileId = uploadResponse.fileId;
    console.log(`Image uploaded successfully. File ID: ${fileId}`);

    // Add file to dataset
    await dataClient.addBinaryDataToDatasetByIds({
      binaryIds: [fileId],
      datasetId: DATASET_ID,
    });

    console.log(`Image added to dataset ${DATASET_ID} successfully`);
  } catch (error) {
    console.error(`Operation failed: ${error}`);
    throw error;
  } finally {
    await appClient.close();
  }
}

// Execute function
addImageToDataset().catch((error) => {
  console.error("Failed to add image to dataset:", error);
  process.exit(1);
});
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
import 'dart:io';
import 'dart:typed_data';
import 'package:viam_sdk/viam_sdk.dart';

const String machinePartId = 'your-machine-part-id-here';
const String datasetId = 'your-dataset-id-here';
const String apiKeyId = 'your-api-key-id';
const String apiKey = 'your-api-key';

Future<void> addImageToDataset() async {
  AppClient? appClient;

  try {
    // Create app client
    appClient = await AppClient.withApiKey(
      apiKeyId: apiKeyId,
      apiKey: apiKey,
    );

    // Get data client
    final dataClient = appClient.dataClient;

    // Read image file
    const imagePath = 'sample_image.jpg';
    final imageFile = File(imagePath);
    final imageBytes = await imageFile.readAsBytes();

    // Upload image
    final uploadOptions = FileUploadOptions(
      componentType: 'camera',
      componentName: 'camera-1',
      fileName: 'training_sample_${DateTime.now().millisecondsSinceEpoch}.jpg',
      fileExtension: 'jpg',
    );

    final fileId = await dataClient.fileUploadFromBytes(
      machinePartId,
      imageBytes,
      uploadOptions,
    );

    print('Image uploaded successfully. File ID: $fileId');

    // Add file to dataset
    await dataClient.addBinaryDataToDatasetByIds(
      [fileId],
      datasetId,
    );

    print('Image added to dataset $datasetId successfully');

  } catch (error) {
    print('Operation failed: $error');
    rethrow;
  } finally {
    await appClient?.close();
  }
}

void main() async {
  try {
    await addImageToDataset();
  } catch (error) {
    print('Failed to add image to dataset: $error');
    exit(1);
  }
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{< /tabs >}}

## Add all images captured by a specific machine to a dataset

The following script adds all images captured from a certain machine to a new dataset:

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from typing import List, Optional

from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient
from viam.utils import create_filter

# Configuration constants – replace with your actual values
DATASET_NAME = "" # a unique, new name for the dataset you want to create
ORG_ID = "" # your organization ID, find in your organization settings
PART_ID = "" # ID of machine that captured target images, find in machine config
API_KEY = "" # API key, find or create in your organization settings
API_KEY_ID = "" # API key ID, find or create in your organization settings

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
       binary_ids=[obj.metadata.binary_data_id for obj in matching_data],
       dataset_id=dataset_id
   )

   print("Added files to dataset.")
   print(f"See dataset: https://app.viam.com/data/datasets?id={dataset_id}")

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

func fetchBinaryDataIDs(ctx context.Context, dataClient data.DataServiceClient, partID string) ([]*data.BinaryData, error) {
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
{{% tab name="Typescript" %}}

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
