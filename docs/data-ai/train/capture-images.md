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

{{< alert title="Tip" color="tip" >}}

For the best results, use the same camera for both training data capture and production deployment.

{{< /alert >}}

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

Once you've captured [enough images for training](/data-ai/train/train-tflite/), you must [annotate](/data-ai/train/annotate-images/) the images before you can use them to train a model.

## Capture images over time

To capture a large number of images for training an ML model, use the data management service to [capture and sync image data](/data-ai/capture-data/capture-sync/) from your camera.

When you sync with data management, Viam stores the images saved by capture and sync on the [**DATA** page](https://app.viam.com/data/), but does not add the images to a dataset.
To use your captured images for training, [add the images to a dataset](/data-ai/train/update-dataset/) and [annotate them](/data-ai/train/annotate-images/), so you can use them to train a model.

{{< alert title="Tip" color="tip" >}}

Once you have enough images, consider disabling data capture to [avoid incurring fees](https://www.viam.com/product/pricing) for capturing large amounts of training data.

{{< /alert >}}
