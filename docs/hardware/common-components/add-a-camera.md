---
linkTitle: "Camera"
title: "Add a camera"
weight: 25
layout: "docs"
type: "docs"
description: "Add and configure a camera component, verify the feed, and capture an image programmatically."
date: "2025-01-30"
aliases:
  - /operate/reference/components/camera/
  - /build/foundation/add-a-camera/
  - /foundation/add-a-camera/
  - /hardware-components/add-a-camera/
  - /hardware/add-a-camera/
  - /hardware/components/add-a-camera/
---

Add a camera to your machine's configuration so you can capture images and video from the Viam app and from code.

## Concepts

The camera API gives you `GetImages` (capture frames), `GetPointCloud` (depth data), and stream access regardless of the underlying hardware.

### Built-in models

- [**webcam**](/reference/components/camera/webcam/): USB cameras and built-in laptop cameras. Auto-detects available devices.
- [**ffmpeg**](/reference/components/camera/ffmpeg/): a camera device, video file, or stream that `ffmpeg` can read. For RTSP IP cameras, prefer the `viam:viamrtsp` registry module listed under Registry modules.
- [**transform**](/reference/components/camera/transform/): applies transformations (crop, resize, rotate, overlay) to another camera's output.
- [**fake**](/reference/components/camera/fake/): a camera model for testing.
- [**image_file**](/reference/components/camera/image-file/): serves color or depth image frames from a file path.

For Micro-RDK, see [Micro-RDK camera models](/reference/components/camera/micro-rdk/).

### Registry modules

Viam-maintained camera modules:

| Module                                                           | Cameras supported                                                                       |
| ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [`viam:viamrtsp`](https://app.viam.com/module/viam/viamrtsp)     | RTSP IP cameras (autodetect, H.264, H.265, MJPEG, MPEG-4) plus ONVIF and UPnP discovery |
| [`viam:realsense`](https://app.viam.com/module/viam/realsense)   | Intel RealSense depth cameras                                                           |
| [`viam:orbbec`](https://app.viam.com/module/viam/orbbec)         | Orbbec 3D cameras                                                                       |
| [`viam:csi-cam-pi`](https://app.viam.com/module/viam/csi-cam-pi) | Raspberry Pi CSI cameras                                                                |
| [`viam:rplidar`](https://app.viam.com/module/viam/rplidar)       | RPLidar 2D lidar (exposed as a point-cloud camera)                                      |

For cameras not covered above, browse [all camera modules in the Viam registry](https://app.viam.com/registry?type=component&subtype=camera).

## Steps

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.
If it shows as offline, verify that `viam-server` is running on your machine.

### 2. Add a camera component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your camera:
   - For a USB webcam or built-in laptop camera, search for **webcam**.
   - For an IP camera that supports RTSP, search for **rtsp** and pick one of the `viam:viamrtsp` models (`rtsp` autodetects codec; specific codecs like `rtsp-h264` or `rtsp-h265` are also available).
   - For an Intel RealSense depth camera, search for **realsense**.
4. Name your camera (this guide uses `my-camera`) and click **Create**.

{{< alert title="Finding your camera" color="tip" >}}

For network cameras you can't locate manually, use a discovery module to find them for you: `viam:viamrtsp` supports ONVIF and UPnP discovery for RTSP cameras, and vendor-specific modules like `viam:realsense` and `viam:orbbec` discover their own cameras over USB.

{{< /alert >}}

### 3. Configure camera attributes

After creating the component, you'll see its configuration panel.

**For a USB webcam (`webcam` model):**

Most USB webcams work with no additional configuration.
If you have multiple cameras connected, specify which one to use:

```json
{
  "video_path": "video0"
}
```

To find available video devices on Linux:

```bash
ls /dev/video*
```

You can also set resolution and frame rate:

```json
{
  "width_px": 640,
  "height_px": 480,
  "frame_rate": 30
}
```

### 4. Save the configuration

Click **Save** in the upper right of the configuration panel.

When you save, `viam-server` automatically reloads the configuration and initializes the new component.
You do not need to restart anything.

### 5. Test the camera

Every component in Viam has a built-in **test panel** in the Configure tab.
The test panel uses the exact same APIs your code will use, so if the camera works here, it will work in your programs.

1. Find your camera component in the configuration view.
2. Expand the **Test** section at the bottom of the component panel.
3. Open the refresh-interval dropdown and select **Live** to see a live video feed from the camera.
4. Click **Get image** to capture a single frame.

You should see a live feed from the camera.

## Try it

Capture an image from your camera programmatically.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **API keys**.
Copy the **API key** and **API key ID**.
Copy the **machine address** from the **Connection details** section on the same tab.

When you run the code below, it saves an image file to your current directory. Check that the image shows what the camera sees.
{{< tabs >}}
{{% tab name="Python" %}}

Install the SDK if you haven't already:

```bash
pip install viam-sdk
```

Save this as `camera_test.py`:

```python
import asyncio
from io import BytesIO
from PIL import Image as PILImage
from viam.robot.client import RobotClient
from viam.components.camera import Camera


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    camera = Camera.from_robot(robot, "my-camera")
    images, metadata = await camera.get_images()
    image = PILImage.open(BytesIO(images[0].data))
    image.save("test-capture.png")
    print(f"Captured {image.size[0]}x{image.size[1]} image")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python camera_test.py
```

You should see output like:

```text
Captured 640x480 image
```

And a file called `test-capture.png` in your current directory.

{{% /tab %}}
{{% tab name="Go" %}}

Initialize a Go module and install the SDK if you haven't already:

```bash
mkdir camera-test && cd camera-test
go mod init camera-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
    "context"
    "fmt"
    "image/png"
    "os"

    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/utils"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("camera-test")

    robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
        client.WithCredentials(utils.Credentials{
            Type:    utils.CredentialsTypeAPIKey,
            Payload: "YOUR-API-KEY",
        }),
        client.WithAPIKeyID("YOUR-API-KEY-ID"),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)

    cam, err := camera.FromProvider(robot, "my-camera")
    if err != nil {
        logger.Fatal(err)
    }

    img, _, err := cam.Images(ctx, nil, nil)
    if err != nil {
        logger.Fatal(err)
    }

    f, err := os.Create("test-capture.png")
    if err != nil {
        logger.Fatal(err)
    }
    defer f.Close()

    image, err := img[0].Image(ctx)
    if err != nil {
        logger.Fatal(err)
    }

    if err := png.Encode(f, image); err != nil {
        logger.Fatal(err)
    }

    fmt.Printf("Captured image and saved to test-capture.png\n")
}
```

Run it:

```bash
go run main.go
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

{{< expand "Camera not appearing as a component option" >}}

- Confirm your machine is **Live** in the Viam app.
- Refresh the page and try again.

{{< /expand >}}

{{< expand "Test panel shows no image or a black frame" >}}

- **USB webcam:** Check the physical connection. Unplug and replug the camera. On Linux, verify the device exists with `ls /dev/video*`.
- **Raspberry Pi camera module:** Ensure the ribbon cable is fully seated and the camera is enabled in `raspi-config`.
- **`video_path` wrong:** If you have multiple cameras, the default device may not be the one you expect. Try different `video_path` values (`video0`, `video1`, etc.).

{{< /expand >}}

{{< expand "\"Failed to find the best driver\" or driver errors" >}}

- On Linux, install required video drivers: `sudo apt install v4l-utils`.
- On macOS, grant camera permissions to the terminal application running `viam-server`.

{{< /expand >}}

{{< expand "Code connects but get_image fails" >}}

- Verify the camera name in your code matches the name in the Viam app exactly (names are case-sensitive).
- Check that the camera test panel works in the Viam app first. If it doesn't work there, the issue is with the camera configuration, not your code.
- Ensure `viam-server` is still running and the machine is online.

{{< /expand >}}

{{< expand "Image is very dark or overexposed" >}}

- Some cameras need a few seconds to adjust exposure after starting. Try adding a short delay before capturing, or capture and discard a few frames first.
- Check if the camera has a physical lens cap or privacy shutter.

{{< /expand >}}

{{< expand "No visible live video feed" >}}

Restart `viam-server`:

1. Navigate to your machine's page.
1. Select the part status dropdown to the right of your machine's name on the top of the page.
1. If you installed `viam-server` with `viam-agent` you will see a **Restart** button. Click it.
   Both `viam-server` and `viam-agent` will restart.

   If you do not see the **Restart** button, click the **...** menu on the right side of the machine part's card, and select **Restart part**.
   If restarting the machine part does not resolve the issue, ssh into the machine and stop and restart `viam-server` manually.

If this doesn't work, you can reboot your machine by running the following command on the machine:

```sh {class="command-line" data-prompt="$"}
sudo reboot
```

{{< /expand >}}

{{< expand "Images are dim on start up when capturing data" >}}

If you are capturing camera data, it can happen that the camera captures and syncs discolored or dark images upon start up. The camera typically stabilizes after a short warm-up period.

{{< /expand >}}

{{< expand "High CPU usage" >}}

Camera streams use a significant amount of CPU resources. The more CPU resources a device has, the more camera streams you can run simultaneously. If your device doesn't have enough CPU resources to support your use case, try lowering the image resolution to decrease the CPU load of the camera streams.

{{< /expand >}}

## Camera calibration

If you are using a camera with the motion service for arm movement or pick-and-place, you may need to calibrate it. Calibration computes the camera's intrinsic and distortion parameters so the motion service can project 2D image coordinates into 3D workspace coordinates accurately. See [Calibrate a camera for motion planning](/motion-planning/frame-system/camera-calibration/).

## Related

- [Camera API reference](/reference/apis/components/camera/): full method documentation.
- [Capture and Sync Data](/data/capture-sync/capture-and-sync-data/): configure your camera to automatically capture images and sync them to the cloud.
- [Add Computer Vision](/vision/configure/): run ML models on your camera feed to detect or classify objects.
- [Video service](/reference/services/video/): record RTSP video to disk and stream stored footage between timestamps.
