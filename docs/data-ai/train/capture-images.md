---
linkTitle: "Capture images for training"
title: "Capture images for training"
weight: 20
layout: "docs"
type: "docs"
description: "Capture images that you can use to train a machine learning model."
---

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand%}}

## Capture individual images

{{< tabs >}}
{{% tab name="Web UI" %}}

You can add images to a dataset directly from a camera or vision component feed in the machine's **CONTROL** or **CONFIGURATION** tabs.

To add an image directly to a dataset from a visual feed, complete the following steps:

1. Open the **TEST** panel of any camera or vision service component to view a feed of images from the camera.
1. Click the button marked with the camera icon to save the currently displayed image to a dataset:
   {{< imgproc src="/components/camera/add_image_to_dataset_button.png" alt="A button marked with the outline of a camera, emphasized in red" resize="800x" style="width:500px" class="imgzoom" >}}
1. Select an existing dataset.
1. Click **Add** to add the image to the selected dataset.
1. When you see a success notification that reads "Saved image to dataset", you have successfully added the image to the dataset.

To view images added to your dataset, go to the **DATA** page, open the [**DATASETS** tab](https://app.viam.com/data/datasets), then select your dataset.

{{% /tab %}}
{{% tab name="SDK" %}}

To add an image to a dataset, find the binary data ID for the image and the dataset ID.
Each SDK provides a method to add an image to a dataset using those IDs:

{{< tabs >}}
{{% tab name="Python" %}}

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

```go
// Connect to Viam client
client, err := app.NewViamClient(
    context.Background()
)
if err != nil {
    return fmt.Errorf("failed to create client: %w", err)
}
defer client.Close()

// Authenticate
err = client.LoginWithAPIKey(context.Background(), APIKeyID, APIKey)
if err != nil {
    return fmt.Errorf("failed to authenticate: %w", err)
}

// Add image to dataset
err = client.AddBinaryDataToDatasetByIDs(
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

```typescript
// Connect to Viam client
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

```dart
  // Connect to Viam client
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

{{% /tab %}}
{{< /tabs >}}

Once you've captured enough images for training, you must [annotate](/data-ai/train/annotate-images/) the images before you can use them to train a model.

## Capture images over time

To capture a large number of images for training an ML model, [Capture and sync image data](/data-ai/capture-data/capture-sync/) using the data management service with your camera.

Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
We recommend you tag the images first and then use the CLI to [add the tagged images to a dataset](/data-ai/train/create-dataset/#add-tagged-images-to-a-dataset).

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}

Once you've captured enough images for training, you must [annotate](/data-ai/train/annotate-images/) the images before you can use them to train a model.

## Capture, annotate, and add images to a dataset

The following example demonstrates how you can capture an image, use an ML model to generate annotations, then add the image to a dataset. You can use this logic to expand and improve your datasets continuously over time as your application runs.
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
{{% tab name="Typescript" %}}

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
