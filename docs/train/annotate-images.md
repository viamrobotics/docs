---
linkTitle: "Annotate images"
title: "Annotate images"
weight: 15
layout: "docs"
type: "docs"
description: "Label images with tags or bounding boxes for training an ML model."
date: "2025-01-30"
---

Label your dataset images with tags for classification or bounding boxes for
object detection. You need a [dataset with images](/train/create-a-dataset/)
before you can annotate.

## Tag images for classification

Tags are labels that apply to an entire image. Use them when you are building
a classification model -- for example, labeling images as "good-part" or
"defective-part".

**Web UI:**

1. In the **DATA** tab, click an image to open it in the detail view.
2. On the right side panel, find the **Tags** section.
3. Click the **+** button next to **Tags**.
4. Type a tag name (for example, `good-part`) and press Enter.
5. The tag is saved immediately. Repeat for each image.

To tag multiple images at once, use the SDK to add tags programmatically (see
the code example below).

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    binary_data_ids = ["binary-data-id-1", "binary-data-id-2"]

    await data_client.add_tags_to_binary_data_by_ids(
        tags=["good-part"],
        binary_ids=binary_data_ids,
    )
    print("Tags added.")

    viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
binaryIDs := []string{"binary-data-id-1", "binary-data-id-2"}

err = dataClient.AddTagsToBinaryDataByIDs(
    ctx,
    []string{"good-part"},
    binaryIDs,
)
if err != nil {
    logger.Fatal(err)
}
fmt.Println("Tags added.")
```

{{% /tab %}}
{{< /tabs >}}

You can get binary data IDs by querying for images using the data client's
`binary_data_by_filter` method, which returns objects that include the binary
data ID.

Choose tag names that are clear, consistent, and descriptive. Use lowercase with
hyphens (for example, `good-part`, `defective-part`, `no-part`). Avoid vague names like
`type1` or `other`.

## Draw bounding boxes for object detection

Bounding boxes mark the location of specific objects within an image. Use them
when you are building an object detection model -- for example, detecting
packages on a conveyor belt.

**Web UI:**

1. Open your dataset and click an image to open the detail view.
2. In the side panel, click the **Actions** tab.
3. Click **Annotate** to enter annotation mode.
4. Select or create a label (for example, `package`).
5. Hold **Cmd** (macOS) or **Ctrl** (Windows/Linux) and click-and-drag on the
   image to draw a rectangle around the object.
6. The bounding box appears with your selected label. Adjust the box edges by
   dragging them if needed.
7. Repeat for every object in the image that should be detected.
8. Move to the next image and repeat.

Draw tight bounding boxes that closely fit the object. Do not include excessive
background. If an image contains multiple objects, draw a separate bounding box
for each one.

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    bbox_id = await data_client.add_bounding_box_to_image_by_id(
        binary_id="binary-data-id-1",
        label="package",
        x_min_normalized=0.15,
        y_min_normalized=0.20,
        x_max_normalized=0.85,
        y_max_normalized=0.90,
    )
    print(f"Added bounding box: {bbox_id}")

    viam_client.close()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
bboxID, err := dataClient.AddBoundingBoxToImageByID(
    ctx,
    "binary-data-id-1",
    "package",
    0.15, // x_min_normalized
    0.20, // y_min_normalized
    0.85, // x_max_normalized
    0.90, // y_max_normalized
)
if err != nil {
    logger.Fatal(err)
}
fmt.Printf("Added bounding box: %s\n", bboxID)
```

{{% /tab %}}
{{< /tabs >}}

Coordinates are normalized 0.0-1.0, where (0.0, 0.0) is the top-left corner
and (1.0, 1.0) is the bottom-right corner.

## Troubleshooting

{{< expand "Bounding boxes not saving" >}}

- **Annotation mode not active.** You must click the **Annotate** button before
  drawing boxes. Without annotation mode, click-and-drag does nothing.
- **No label selected.** You must select or create a label before drawing a
  bounding box. If no label is selected, the box will not persist.
- **Box too small.** Very small bounding boxes (a few pixels) may not register.
  Draw boxes that clearly encompass the object.

{{< /expand >}}

{{< expand "Tags applied to wrong images" >}}

- **Remove incorrect tags.** In the web UI, click the image, find the tag in
  the Tags section, and click the **x** next to it to remove it.
- **Programmatically remove tags.** Use `remove_tags_from_binary_data_by_ids`
  in the SDK to remove tags from specific images.

{{< /expand >}}

## What's next

- [Automate annotation](/train/automate-annotation/) -- speed up labeling by
  using an existing ML model to generate predictions automatically.
- [Train a model](/train/train-a-model/) -- use your labeled dataset to
  train a classification or object detection model.
