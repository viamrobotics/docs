---
title: "Configure a Fake Camera"
linkTitle: "fake"
weight: 35
type: "docs"
description: Configure a camera to use for testing."
images: ["/components/img/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a gradient.
This camera also returns a point cloud.

You can optionally specify either a height or width, and the image will be scaled to preserve a 16:9 aspect ratio.
You cannot specify both a height and width.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `fake` model.

Click **Create component**.

![Configuration of a fake camera in the Viam app config builder.](../img/configure-fake.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<camera-name>",
    "type": "camera",
    "model" : "fake",
    "attributes": {
        "width": <int>,
        "height": <int>
    }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` cameras:

| Name | Inclusion | Description |
| ---- | --------- | ----------- |
| `width` | Optional | The width of the image in pixels. The default resolution is 1280 x 720. If you specify either width or height, the image gets scaled to preserve 16:9 aspect ratio. You cannot specify both `width` and `height`. |
| `height` | Optional | The width of the image in pixels. The default resolution is 1280 x 720. If you specify either width or height, the image gets scaled to preserve 16:9 aspect ratio. You cannot specify both `width` and `height` |

## View the camera stream

Once your camera is configured, go to the **Control** tab, and click on the camera's dropdown menu.
Then toggle the camera or the Point Cloud Data view to ON.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

![Fake Camera View](../img/fake-view.png)

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
