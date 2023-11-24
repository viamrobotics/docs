---
title: "Configure a Fake Camera"
linkTitle: "fake"
weight: 10
type: "docs"
description: Configure a camera to use for testing."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/fake/"
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a gradient.
This camera also returns a point cloud.

You can optionally specify a height and width.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `fake` model.
Enter a name for your camera and click **Create**.

![Configuration of a fake camera in the Viam app config builder.](/build/configure/components/camera/configure-fake.png)

Copy and paste the following attribute template into your camera's **Attributes** box.
Then remove and fill in the attributes as applicable to your camera, according to the table below.

{{< tabs >}}
{{% tab name="Attributes template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "width": <int>,
  "height": <int>
}
```

{{% /tab %}}
{{% tab name="Attributes example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "width": 640,
  "height": 360
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "fake",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "width": <int>,
    "height": <int>
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `fake` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `width` | int | Optional | The width of the image in pixels. The default width is 1280. |
| `height` | int | Optional | The height of the image in pixels. The default height is 720. |

## View the camera stream

Once your camera is configured, go to the **Control** tab, and click on the camera's dropdown menu.
Then toggle the camera or the Point Cloud Data view to ON.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/build/configure/components/camera/fake-view.png" alt="Fake Camera View" resize="600x" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
