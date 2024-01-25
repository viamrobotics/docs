---
title: "Configure a Velodyne Camera"
linkTitle: "velodyne"
weight: 32
type: "docs"
description: "Configure a camera that uses velodyne lidar."
images: ["/icons/components/camera.svg"]
tags: ["camera", "components"]
aliases:
  - "/components/camera/velodyne/"
# SMEs: SLAM team
---

A `velodyne` camera uses [Velodyne lidar](https://velodynelidar.com/).
The velodyne must be running locally at address `127.0.0.1`.

{{< tabs name="Configure a Velodyne Camera" >}}
{{% tab name="Config Builder" %}}

Navigate to the **Config** tab of your machine's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and click **Create component**.
Select the `camera` type, then select the `velodyne` model.
Enter a name for your camera and click **Create**.

{{< imgproc src="/components/camera/configure-velodyne.png" alt="Configuration of a velodyne camera in the Viam app config builder." resize="600x" >}}

Edit and fill in the attributes as applicable.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-camera-name>",
  "model": "velodyne",
  "type": "camera",
  "namespace": "rdk",
  "attributes": {
    "port": <int>,
    "ttl_ms": <int>,
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for `velodyne` cameras:

<!-- prettier-ignore -->
| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `port` | int | **Required** | The port the Velodyne camera is running on. Try `2368` if you are unsure. |
| `ttl_ms` | int | **Required** | Frequency in milliseconds to output the [TTL signal](https://en.wikipedia.org/wiki/Transistor%E2%80%93transistor_logic) from the camera. |

## View the camera stream

{{< readfile "/static/include/components/camera-view-camera-stream.md" >}}

## Next Steps

{{< readfile "/static/include/components/camera-model-next-steps.md" >}}
