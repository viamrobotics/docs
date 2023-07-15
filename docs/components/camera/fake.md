---
title: "Configure a Fake Camera"
linkTitle: "fake"
weight: 10
type: "docs"
description: Configure a camera to use for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a gradient.
This camera also returns a point cloud.

You can optionally specify a height and width.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.
Enter a name for your camera, select the type `camera`, and select the `fake` model.

Click **Create component**.

![Configuration of a fake camera in the Viam app config builder.](/components/camera/configure-fake.png)

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
    "name": "<your-camera-name>",
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

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width` | int | Optional | The width of the image in pixels. The default width is 1280. |
| `height` | int | Optional | The height of the image in pixels. The default height is 720. |

## View the camera stream

Once your camera is configured, go to the **Control** tab, and click on the camera's dropdown menu.
Then toggle the camera or the Point Cloud Data view to ON.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/components/camera/fake-view.png" alt="Fake Camera View" resize="600x" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
