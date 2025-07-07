---
linkTitle: "Capture and annotate images"
title: "Capture and annotate images for training"
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

{{< alert title="Tip" color="tip" >}}

For the best results, use the same camera for both training data capture and production deployment.

{{< /alert >}}

## Capture images

### Capture individual images

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
{{% tab name="Python" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`data_client.binary_data_capture_upload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

```python
CAMERA_NAME = "<camera-name>"
MACHINE_ADDRESS = "<machine-address.viam.cloud>"

dial_options = DialOptions(
    credentials=Credentials(
        type="api-key",
        payload=API_KEY,
    ),
    auth_entity=API_KEY_ID,
)

robot_opts = RobotClient.Options.with_api_key(
    api_key=API_KEY,
    api_key_id=API_KEY_ID
)

viam_client = await ViamClient.create_from_dial_options(dial_options)
data_client = viam_client.data_client

robot_client = await RobotClient.at_address(ROBOT_ADDRESS, robot_opts)
camera = Camera.from_robot(robot_client, CAMERA_NAME)

# Capture image
image_frame = await camera.get_image()

# Upload data
file_id = await data_client.binary_data_capture_upload(
    part_id=PART_ID,
    component_type="camera",
    component_name=CAMERA_NAME,
    method_name="GetImage",
    data_request_times=[datetime.utcnow(), datetime.utcnow()],
    file_extension=".jpg",
    binary_data=image_frame
)

# Cleanup
await robot_client.close()
viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`DataClient.BinaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

```go
const (
    CAMERA_NAME      = "<camera-name>"
    MACHINE_ADDRESS  = "<machine-address.viam.cloud>"
    API_KEY          = "<api-key>"
    API_KEY_ID       = "<api-key-id>"
    PART_ID          = "<part-id>"
)

ctx := context.Background()
machine, err := client.New(
    ctx,
    MACHINE_ADDRESS,
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
        API_KEY_ID,
        rpc.Credentials{
            Type:    rpc.CredentialsTypeAPIKey,
            Payload: API_KEY,
        },
    )),
)
if err != nil {
    return "", err
}
defer machine.Close(ctx)

viamClient, err := client.New(ctx, MACHINE_ADDRESS, logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

dataClient := viamClient.DataClient()

camera, err := camera.FromRobot(machine, CAMERA_NAME)
if err != nil {
    return "", err
}

// Capture image
img, _, err := camera.GetImage(ctx)
if err != nil {
    return "", err
}

// Upload binary data
now := time.Now().UTC()
fileID, err := dataClient.BinaryDataCaptureUpload(ctx, app.BinaryDataCaptureUploadOptions{
    PartID:            PART_ID,
    ComponentType:     "camera",
    ComponentName:     CAMERA_NAME,
    MethodName:        "GetImage",
    DataRequestTimes:  []time.Time{now, now},
    FileExtension:     ".jpg",
    BinaryData:        img,
})
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`dataClient.binaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

```typescript
const CAMERA_NAME = "<camera-name>";
const MACHINE_ADDRESS = "<machine-address.viam.cloud>";
const API_KEY = "<api-key>";
const API_KEY_ID = "<api-key-id>";
const PART_ID = "<part-id>";

const machine = await Viam.createRobotClient({
  host: MACHINE_ADDRESS,
  credential: {
    type: "api-key",
    payload: API_KEY,
  },
  authEntity: API_KEY_ID,
});

const client: ViamClient = await createViamClient({
  credential: {
    type: "api-key",
    payload: API_KEY,
  },
  authEntity: API_KEY_ID,
});

const dataClient = client.dataClient;

const camera = new Viam.CameraClient(machine, CAMERA_NAME);

// Capture image
const imageFrame = await camera.getImage();

// Upload binary data
const now = new Date();
const fileId = await dataClient.binaryDataCaptureUpload({
  partId: PART_ID,
  componentType: "camera",
  componentName: CAMERA_NAME,
  methodName: "GetImage",
  dataRequestTimes: [now, now],
  fileExtension: ".jpg",
  binaryData: imageFrame,
});

// Cleanup
await machine.disconnect();
dataClient.close();
```

{{% /tab %}}
{{% tab name="Flutter" %}}

To capture an image and add it to your **DATA** page, fetch an image from your camera through your machine.
Pass that image and an appropriate set of metadata to [`dataClient.binaryDataCaptureUpload`](/dev/reference/apis/data-client/#binarydatacaptureupload):

```dart
const String CAMERA_NAME = '<camera-name>';
const String MACHINE_ADDRESS = '<robot-address.viam.cloud>';
const String API_KEY = '<api-key>';
const String API_KEY_ID = '<api-key-id>';
const String PART_ID = '<part-id>';

final machine = await RobotClient.atAddress(
    MACHINE_ADDRESS,
    RobotClientOptions.withApiKey(
        apiKey: API_KEY,
        apiKeyId: API_KEY_ID,
    ),
);

final client = await ViamClient.withApiKey(
    apiKeyId: API_KEY_ID,
    apiKey: API_KEY,
);

final dataClient = client.dataClient;

final camera = Camera.fromRobot(machine, CAMERA_NAME);

// Capture image
final imageFrame = await camera.getImage();

// Upload binary data
final now = DateTime.now().toUtc();
final fileId = await dataClient.binaryDataCaptureUpload(
    partId: PART_ID,
    componentType: 'camera',
    componentName: CAMERA_NAME,
    methodName: 'GetImage',
    dataRequestTimes: [now, now],
    fileExtension: '.jpg',
    binaryData: imageFrame,
);

// Cleanup
await robotClient.close();
dataClient.close();
```

{{% /tab %}}
{{< /tabs >}}

Once you've captured [enough images for training](/data-ai/train/train-tflite/), you must [annotate](#annotate-images) the images before you can use them to train a model.

### Capture images over time

To capture a large number of images for training an ML model, use the data management service to [capture and sync image data](/data-ai/capture-data/capture-sync/) from your camera.

When you sync with data management, Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
To use your captured images for training, [add the images to a dataset](/data-ai/train/create-dataset/#add-to-a-dataset) and [annotate them](#annotate-images), so you can use them to train a model.

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}

You can either manually add annotations through the Viam web UI, or add annotations with an existing ML model.

## Annotate images

Images must be annotated in order to train an ML model on them. Viam supports two ways to annotate an image:

- Adding tags to images (classifier)
- Labeling objects within images (object detector)

### Add tags to an image

Use tags to add metadata about an entire image, for example if the quality of a manufacturing output is `good` or `bad`.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Python" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`data_client.add_tags_to_binary_data_by_ids`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

```python
detector = VisionClient.from_robot(machine, "<detector_name>")

# Get the captured data for a camera
result = await detector.capture_all_from_camera(
    "<camera_name>",
    return_image=True,
    return_detections=True,
)
image = result.image
detections = result.detections

tags = ["tag1", "tag2"]

my_filter = create_filter(
    component_name="camera-1", organization_ids=["<org-id>"]
)
binary_metadata, count, last = await data_client.binary_data_by_filter(
    filter=my_filter,
    limit=20,
    include_binary_data=False
)

my_ids = []

for obj in binary_metadata:
    my_ids.append(
        obj.metadata.binary_data_id
    )

binary_data = await data_client.add_tags_to_binary_data_by_ids(tags, my_ids)
```

{{% /tab %}}
{{% tab name="Go" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`DataClient.AddTagsToBinaryDataByIDs`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

```go
ctx := context.Background()

viamClient, err := client.New(ctx, "<machine_address>", logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

myDetector, err := vision.FromRobot(viamClient, "<detector_name>")
if err != nil {
    log.Fatal(err)
}

dataClient := viamClient.DataClient()

// Get the captured data for a camera
result, err := myDetector.CaptureAllFromCamera(ctx, "<camera_name>", &vision.CaptureAllFromCameraRequest{
    ReturnImage:      true,
    ReturnDetections: true,
})
if err != nil {
    log.Fatal(err)
}

image := result.Image
detections := result.Detections

tags := []string{"tag1", "tag2"}

myFilter := &datamanager.Filter{
    ComponentName:   "camera-1",
    OrganizationIDs: []string{"<org-id>"},
}

binaryResult, err := dataClient.BinaryDataByFilter(ctx, &datamanager.BinaryDataByFilterRequest{
    Filter:            myFilter,
    Limit:             20,
    IncludeBinaryData: false,
})
if err != nil {
    log.Fatal(err)
}

var myIDs []string
for _, obj := range binaryResult.BinaryMetadata {
    myIDs = append(myIDs, obj.Metadata.BinaryDataID)
}

_, err = dataClient.AddTagsToBinaryDataByIDs(ctx, &datamanager.AddTagsRequest{
    Tags:          tags,
    BinaryDataIDs: myIDs,
})
if err != nil {
    log.Fatal(err)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`dataClient.addTagsToBinaryDataByIds`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

```typescript
const client = await createViamClient();
const myDetector = new VisionClient(client, "<detector_name>");
const dataClient = client.dataClient;

// Get the captured data for a camera
const result = await myDetector.captureAllFromCamera("<camera_name>", {
  returnImage: true,
  returnDetections: true,
});
const image = result.image;
const detections = result.detections;

const tags = ["tag1", "tag2"];

const myFilter = createFilter({
  componentName: "camera-1",
  organizationIds: ["<org-id>"],
});

const binaryResult = await dataClient.binaryDataByFilter({
  filter: myFilter,
  limit: 20,
  includeBinaryData: false,
});

const myIds: string[] = [];

for (const obj of binaryResult.binaryMetadata) {
  myIds.push(obj.metadata.binaryDataId);
}

await dataClient.addTagsToBinaryDataByIds(tags, myIds);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

Use an ML model to generate tags for an image or set of images.
Then, pass the tags and image IDs to [`dataClient.addTagsToBinaryDataByIds`](/dev/reference/apis/data-client/#addtagstobinarydatabyids):

```dart
final viamClient = await ViamClient.connect();
final myDetector = VisionClient.fromRobot(viamClient, "<detector_name>");
final dataClient = viamClient.dataClient;

// Get the captured data for a camera
final result = await myDetector.captureAllFromCamera(
    "<camera_name>",
    returnImage: true,
    returnDetections: true,
);
final image = result.image;
final detections = result.detections;

final tags = ["tag1", "tag2"];

final myFilter = createFilter(
    componentName: "camera-1",
    organizationIds: ["<org-id>"],
);

final binaryResult = await dataClient.binaryDataByFilter(
    filter: myFilter,
    limit: 20,
    includeBinaryData: false,
);

final myIds = <String>[];

for (final obj in binaryResult.binaryMetadata) {
    myIds.add(obj.metadata.binaryDataId);
}

await dataClient.addTagsToBinaryDataByIds(tags, myIds);
```

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.

### Label objects within an image

Use labels to add metadata about objects within an image, for example the number of bicycles in a street scene.

{{< alert title="Tip" color="tip" >}}

If you have an ML model, use code to speed up annotating your data, otherwise use the Web UI.

{{< /alert >}}

{{< tabs >}}
{{% tab name="Web UI" %}}

The [**DATA** page](https://app.viam.com/data/view) provides an interface for annotating images.

To label an object with a bounding box:

1. Click on an image, then click the **Annotate** button in right side menu.
1. Choose an existing label or create a new label.
1. Holding the command key (on macOS), or the control key (on Linux and Windows), click and drag on the image to create the bounding box:

   {{<gif webm_src="/services/data/label-magnemite.webm" mp4_src="/services/data/label-magnemite.mp4" alt="Add a bounding box around the magnemite pokemon in an image">}}

{{< alert title="Tip" color="tip" >}}

Once created, you can move, resize, or delete the bounding box.

{{< /alert >}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="Python" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`data_client.add_bounding_box_to_image_by_id`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

```python
detector = VisionClient.from_robot(machine, "<detector_name>")

# Get the captured data for a camera

# Initialize data client
data_client = DataClient.create_from_dial_options(
    dial_options=DialOptions(
        credentials=Credentials(
            type="api-key",
            payload="<YOUR-API-KEY>"
        )
    ),
    organization_id="<YOUR-ORG-ID>",
    location_id="<YOUR-LOCATION-ID>"
)

# Initialize vision service
detector = VisionClient.from_robot(machine, "<detector_name>")

# Capture data with image and detections
result = await detector.capture_all_from_camera(
    "<camera_name>",
    return_image=True,
    return_detections=True,
)

image = result.image
detections = result.detections

# Upload image to obtain binary ID
binary_id = await data_client.binary_data_capture_upload(
    binary_data=image.data,
    part_id="<YOUR-PART-ID>",
    component_type="camera",
    component_name="<camera_name>",
    method_name="get_image",
    file_extension=".jpg"
)

# Process each detection and create bounding boxes
for detection in detections:
    bbox = detection.bounding_box

    # Create bounding box annotation
    bbox_id = await data_client.add_bounding_box_to_image_by_id(
        binary_id=binary_id.file_id,
        label=detection.class_name,
        x_min_normalized=bbox.x_min_normalized,
        y_min_normalized=bbox.y_min_normalized,
        x_max_normalized=bbox.x_max_normalized,
        y_max_normalized=bbox.y_max_normalized
    )

    print(f"Bounding box created: {bbox_id} for class: {detection.class_name}")
```

{{% /tab %}}
{{% tab name="Go" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`DataClient.AddBoundingBoxToImageByID`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

```go
ctx := context.Background()

viamClient, err := client.New(ctx, "<machine_address>", logger)
if err != nil {
    log.Fatal(err)
}
defer viamClient.Close(ctx)

myDetector, err := vision.FromRobot(viamClient, "<detector_name>")
if err != nil {
    log.Fatal(err)
}

dataClient := viamClient.DataClient()

// Get the captured data for a camera
result, err := myDetector.CaptureAllFromCamera(ctx, "<camera_name>", &vision.CaptureAllFromCameraRequest{
    ReturnImage:      true,
    ReturnDetections: true,
})
if err != nil {
    log.Fatal(err)
}

image := result.Image
detections := result.Detections

for _, detection := range detections {
    bboxID, err := dataClient.AddBoundingBoxToImageByID(ctx, &datamanager.AddBoundingBoxRequest{
        BinaryID:        "<YOUR-BINARY-DATA-ID>",
        Label:           detection.Label,
        XMinNormalized:  detection.BoundingBox.Min.X,
        YMinNormalized:  detection.BoundingBox.Min.Y,
        XMaxNormalized:  detection.BoundingBox.Max.X,
        YMaxNormalized:  detection.BoundingBox.Max.Y,
    })

    fmt.Printf("Added bounding box ID: %s for detection: %s\n", bboxID, detection.ClassName)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`dataClient.addBoundingBoxToImageById`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

```typescript
const client = await createViamClient();
const myDetector = new VisionClient(client, "<detector_name>");
const dataClient = client.dataClient;

// Get the captured data for a camera
const result = await myDetector.captureAllFromCamera("<camera_name>", {
  returnImage: true,
  returnDetections: true,
});
const image = result.image;
const detections = result.detections;

// Process each detection and add bounding boxes
for (const detection of detections) {
  const bboxId = await dataClient.addBoundingBoxToImageById({
    binaryId: "<YOUR-BINARY-DATA-ID>",
    label: detection.className,
    xMinNormalized: detection.boundingBox.xMin,
    yMinNormalized: detection.boundingBox.yMin,
    xMaxNormalized: detection.boundingBox.xMax,
    yMaxNormalized: detection.boundingBox.yMax,
  });

  console.log(
    `Added bounding box ID: ${bboxId} for detection: ${detection.className}`,
  );
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

Use an ML model to generate bounding boxes for an image.
Then, separately pass each bounding box and the image ID to [`dataClient.addBoundingBoxToImageById`](/dev/reference/apis/data-client/#addboundingboxtoimagebyid):

```dart
final viamClient = await ViamClient.connect();
final myDetector = VisionClient.fromRobot(viamClient, "<detector_name>");
final dataClient = viamClient.dataClient;

// Get the captured data for a camera
final result = await myDetector.captureAllFromCamera(
    "<camera_name>",
    returnImage: true,
    returnDetections: true,
);
final image = result.image;
final detections = result.detections;

// Process each detection and add bounding boxes
for (final detection in detections) {
    final bboxId = await dataClient.addBoundingBoxToImageById(
      binaryId: "<YOUR-BINARY-DATA-ID>",
      label: detection.className,
      xMinNormalized: detection.boundingBox.xMin,
      yMinNormalized: detection.boundingBox.yMin,
      xMaxNormalized: detection.boundingBox.xMax,
      yMaxNormalized: detection.boundingBox.yMax,
    );

    print('Added bounding box ID: $bboxId for detection: ${detection.className}');
}
```

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.

## Combine these steps: capture, annotate, and add images to a dataset in a single script

The following example demonstrates how you can capture an image, use an ML model to generate annotations, and then add the image to a dataset.
You can use this logic to expand and improve your datasets continuously over time.
Check the annotation accuracy in the **DATA** tab, then re-train your ML model on the improved dataset to improve the ML model.

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
