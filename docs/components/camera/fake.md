---
title: "Configure a Fake Camera"
linkTitle: "Fake"
weight: 35
type: "docs"
description: Configure a camera to use for testing."
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a chess board.
This camera also returns a point cloud.

You can optionally specify either a height or width, and the image will be scaled to preserve a 16:9 aspect ratio.
If you specify both a height and width, and the ratio is not 16:9, you will receive an image but no point cloud.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

On the **COMPONENTS** subtab, navigate to the **Create Component** menu.
Enter a name for your camera, select the type `camera`, and select the `fake` model.

<img src="../img/create-fake.png" alt="Creation of a join color depth view in the Viam app config builder." style="max-width:600px" />

Fill in the attributes for your join color depth view:

<img src="../img/configure-fake.png" alt="Configuration of a join color depth view in the Viam app config builder." />

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera_name>",
    "type": "camera",
    "model" : "fake",
    "attributes": {
        "width": <integer>,
        "height": <integer>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for fake cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `width` | *Optional* | The width of the image in pixels. The default resolution is 1280 x 720. If you specify either width or height, the image gets scaled to preserve 16:9 aspect ratio. If you specify both a width and a height and the ratio is not 16:9, you will receive an image but no point cloud. |
| `height` | *Optional* | The width of the image in pixels. The default resolution is 1280 x 720. If you specify either width or height, the image gets scaled to preserve 16:9 aspect ratio. If you specify both a width and a height and the ratio is not 16:9, you will receive an image but no point cloud. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
