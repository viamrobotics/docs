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

### Classify images with tags

Classification determines a descriptive tag or set of tags for an image.
For example, you could use classification to answer the following questions:

- does an image of a food display appear `full`, `empty`, or `average`?
- the quality of manufacturing output `good` or `bad`?
- what combination of toppings exists on a pizza: `pepperoni`, `sausage`, and `pepper`? or `pineapple`, `ham`, and `mushroom`?

Viam supports single and multiple label classification.
To create a training dataset for classification, annotate tags to describe your images.

{{< alert title="Tip" color="tip" >}}

Unless you already have an ML model that can generate tags for your dataset, use the Web UI to annotate.

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

### Detect objects with bounding boxes

Object detection identifies and determines the location of certain objects in an image.
For example, object detection could help you identify:

- how many `pizza` objects appear on a counter
- the number of `bicycle` and `pedestrian` objects on a greenway
- which `plant` objects are popular with `deer` in your garden

To create a training set for object detection, annotate bounding boxes to teach your model to identify objects that you want to detect in future images.

{{< alert title="Tip" color="tip" >}}

To start a new dataset with no preexisting data or model, use the Web UI to annotate tags.
If you have an ML model that can generate tags for your dataset, consider using the model in an SDK to speed up annotation.

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

