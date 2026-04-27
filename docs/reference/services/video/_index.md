---
title: "Video service"
linkTitle: "Video"
description: "Stream stored video from an RTSP camera between specified timestamps."
layout: "docs"
type: "docs"
weight: 80
date: "2026-04-23"
---

The video service streams recorded video from an RTSP camera between two timestamps.
It stores video segments on disk, optionally uploads them to the cloud through the [data management service](/data/capture-sync/capture-and-sync-data/), and serves the stored footage on request.

Use the video service when you want to record continuous footage from an RTSP IP camera and retrieve it later by time range, for example to build a DVR-style playback feature, review footage around an alert, or archive clips to the cloud.

## Configuration

The video service requires a configured RTSP camera from the [`viam:viamrtsp`](https://app.viam.com/module/viam/viamrtsp) module.
Add the camera first, then add the video service.

### `viam:viamrtsp:video-service`

The `viam:viamrtsp:video-service` model records video from a `viam:viamrtsp` camera and serves stored segments by time range.

To configure it:

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Configuration block**.
Select the `video` type and the `viam:viamrtsp:video-service` model.
Enter a name or use the suggested name for your service and click **Create**.

In your video service's configuration panel, copy and paste the following JSON object into the attributes field:

```json {class="line-numbers linkable-line-numbers"}
{
  "camera": "<your-rtsp-camera-name>",
  "storage": {
    "size_gb": 10
  }
}
```

Edit the attributes as applicable to your machine, according to the table below.

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "<your-video-service>",
  "api": "rdk:service:video",
  "model": "viam:viamrtsp:video-service",
  "attributes": {
    "camera": "<your-rtsp-camera-name>",
    "storage": {
      "size_gb": <integer>,
      "upload_path": "<path>",
      "storage_path": "<path>"
    },
    "video": {
      "bitrate": <integer>,
      "preset": "<preset>"
    },
    "framerate": <integer>
  }
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "name": "video-service-1",
  "api": "rdk:service:video",
  "model": "viam:viamrtsp:video-service",
  "attributes": {
    "camera": "rtsp-cam-1",
    "storage": {
      "size_gb": 10
    }
  }
}
```

{{% /tab %}}
{{< /tabs >}}

The following attributes are available for the `viam:viamrtsp:video-service` model:

<!-- prettier-ignore -->
| Name | Type | Required? | Description |
| ---- | ---- | --------- | ----------- |
| `camera` | string | Optional | Name of the camera component to use as the video source. If omitted, the service runs in read-only mode and serves existing stored video. |
| `storage` | object | **Required** | Storage configuration. See the fields below. |
| `storage.size_gb` | integer | **Required** | Maximum storage size in gigabytes. |
| `storage.upload_path` | string | Optional | Path where uploaded video segments are saved. |
| `storage.storage_path` | string | Optional | Path where video segments are stored on disk. |
| `video` | object | Optional | Video encoding configuration. Only used when re-encoding is required. |
| `video.bitrate` | integer | Optional | Bitrate for video encoding, in bits per second. Only applies to MPEG-4 and MJPEG inputs. |
| `video.preset` | string | Optional | Encoding preset. Options: `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`. |
| `framerate` | integer | Optional | Frame rate to capture video at, in frames per second. Only applies to MPEG-4 and MJPEG inputs. |

To sync captured video to the cloud, also configure the [data management service](/data/capture-sync/capture-and-sync-data/).

## API

The video service supports the following methods:

<!-- prettier-ignore -->
| Method Name | Description |
| ----------- | ----------- |
| [`GetVideo`](/reference/apis/services/video/#getvideo) | Stream video chunks between two timestamps. |
| [`DoCommand`](/reference/apis/services/video/#docommand) | Execute model-specific commands, including `save`, `fetch`, and `get-storage-state`. |

For full method reference, see the [Video service API](/reference/apis/services/video/).
