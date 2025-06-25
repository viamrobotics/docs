---
linkTitle: "Annotate images for training"
title: "Annotate images for training"
weight: 40
layout: "docs"
type: "docs"
description: "Annotate images to train a machine learning model."
---

Use the interface on the [**DATA** page](https://app.viam.com/data/view) to annotate your images.
When you label your dataset, include:

- images with and _without_ the categories you’re looking to identify
- a roughly equal number of images for each category
- images from your production environment, including lighting and camera quality
- examples from every angle and distance that you expect the model to handle

Viam enables you to annotate images for use with the following machine learning methods.

## Prerequisites

{{% expand "A machine connected to Viam" %}}

{{% snippet "setup.md" %}}

{{% /expand %}}

{{% expand "A camera, connected to your machine, to capture images" %}}

Follow the guide to configure a [webcam](/operate/reference/components/camera/webcam/) or similar [camera component](/operate/reference/components/camera/).

{{% /expand %}}

## Classify images with tags

Classification determines a descriptive tag or set of tags for an image.
For example, classification could help you identify:

- whether an image of a food display appears `full`, `empty`, or `average`
- the quality of manufacturing output: `good` or `bad`
- what combination of toppings exists on a pizza: `pepperoni`, `sausage` and `pepper`, or `pineapple` and `ham` and `mushroom`

Viam supports single and multiple label classification.
To create a training set for classification, annotate tags to describe your images.

{{< tabs >}}
{{% tab name="Web UI" %}}

To tag an image:

1. Click on an image, then click the **+** next to the **Tags** option.
1. Add one or more tags to your image.

   {{<gif webm_src="/services/data/tag-tortilla.webm" mp4_src="/services/data/tag-tortilla.mp4" alt="Tag image with a full label">}}

Repeat these steps for all images in the dataset.

{{% /tab %}}
{{% tab name="SDK" %}}

Use an ML model to generate tags for an image.
The following code shows how to add tags to an image in Viam:

{{< tabs >}}
{{% tab name="Python" %}}

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

my_filter =
    create_filter(component_name="camera-1", organization_ids=["<org-id>"])
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

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.

## Detect objects with bounding boxes

Object detection identifies and determines the location of certain objects in an image.
For example, object detection could help you identify:

- how many `pizza` objects appear on a counter
- the number of `bicycle` and `pedestrian` objects on a greenway
- which `plant` objects are popular with `deer` in your garden

To create a training set for object detection, annotate bounding boxes to teach your model to identify objects that you want to detect in future images.

{{< tabs >}}
{{% tab name="Web UI" %}}

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
{{% tab name="SDK" %}}

Use an ML model to generate bounding boxes for an image.
The following code shows how to add bounding boxes to an image in Viam:

{{< tabs >}}
{{% tab name="Python" %}}

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

{{% /tab %}}
{{< /tabs >}}

Once you've annotated your dataset, you can [train](/data-ai/train/train-tflite/) an ML model to make inferences.
