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
component_description: "A camera model for testing."
toc_hide: true
# SMEs: Bijan, vision team
---

A `fake` camera is a camera model for testing.
The camera always returns the same image, which is an image of a gradient.
This camera also returns a point cloud.

You can optionally specify a height and width.

{{< tabs name="Configure a Fake Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).
Click the **+** icon next to your machine part in the left-hand menu and select **Component**.
Select the `camera` type, then select the `fake` model.
Enter a name or use the suggested name for your camera and click **Create**.

![Configuration of a fake camera in the Viam app config builder.](/components/camera/configure-fake.png)

Edit the attributes as applicable to your camera, according to the table below.

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
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `width` | int | Optional | The width of the image in pixels. The maximum width is 10000. <br> Default: `1280` |
| `height` | int | Optional | The height of the image in pixels. The maximum height is 10000. <br> Default: `720` |
| `animated` | bool | Optional | If you want the camera stream visible on the **CONTROL** tab to be animated. <br> Default: `False` |

## View the camera stream

Once your camera is configured, go to the **CONTROL** tab, and click on the camera's dropdown menu.
Then toggle the camera or the Point Cloud Data view to ON.
You will see the live video feed from your camera.
You can change the refresh frequency as needed to change bandwidth.

{{< imgproc src="/components/camera/fake-view.png" alt="Fake Camera View" resize="600x" >}}

## Next steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
