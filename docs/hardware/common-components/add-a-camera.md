---
linkTitle: "Camera"
title: "Add a camera"
weight: 25
layout: "docs"
type: "docs"
description: "Add and configure a camera component, verify the feed, and capture an image programmatically."
date: "2025-01-30"
aliases:
  - /build/foundation/add-a-camera/
  - /foundation/add-a-camera/
  - /hardware-components/add-a-camera/
  - /hardware/add-a-camera/
  - /hardware/components/add-a-camera/
---

Add a camera to your machine's configuration so you can capture images and video from the Viam app and from code.

## Concepts

The camera API gives you `GetImages` (capture frames), `GetPointCloud` (depth data), and stream access regardless of the underlying hardware. Common models include:

- **webcam** (built-in): USB cameras and built-in laptop cameras. Auto-detects available devices.
- **ffmpeg** (built-in): IP cameras and RTSP streams.
- **realsense**: Intel RealSense depth cameras (module).
- **transform**: Applies transformations (crop, resize, overlay) to another camera's output.

Browse all available camera models in the [Viam registry](https://app.viam.com/registry?type=component&subtype=camera).

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
   - For an IP camera that supports RTSP, search for **ffmpeg**.
   - For an Intel RealSense depth camera, search for **realsense**.
4. Name your camera (this guide uses `my-camera`) and click **Create**.

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
3. Click **Toggle stream** to see a live video feed from the camera.
4. Click **Get image** to capture a single frame.

You should see a live feed from the camera.

## Try it

Capture an image from your camera programmatically.

To get the credentials for the code below, go to your machine's page in the Viam app, click the **CONNECT** tab, and select **SDK code sample**.
Toggle **Include API key** on.
Copy the machine address, API key, and API key ID from the code sample.

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

## What's next

- [Camera API reference](/dev/reference/apis/components/camera/): full method documentation.
- [Capture and Sync Data](/data/capture-sync/capture-and-sync-data/): configure your camera to automatically capture images and sync them to the cloud.
- [Add Computer Vision](/vision/configure/): run ML models on your camera feed to detect or classify objects.
