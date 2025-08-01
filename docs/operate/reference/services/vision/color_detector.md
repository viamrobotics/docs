---
title: "Configure a color_detector"
linkTitle: "color_detector"
weight: 10
type: "docs"
description: "A heuristic detector that draws boxes around objects according to their hue (does not detect black, gray, and white)."
service_description: "A heuristic detector that draws boxes around objects according to their hue (does not detect black, gray, and white)."
tags: ["vision", "computer vision", "CV", "services", "detection"]
images: ["/services/vision/dog-detector.png"]
aliases:
  - /services/vision/detection/
  - /services/vision/classification/
  - /ml/vision/color_detector/
  - /services/vision/color_detector/
  - /data-ai/services/vision/color_detector/
  - /tutorials/services/basic-color-detection/
  - /tutorials/services/try-viam-color-detection/
  - /tutorials/try-viam-color-detection/
  - /tutorials/viam-rover/try-viam-color-detection/
# SMEs: Bijan, Khari
---

The `color_detector` vision service model is a heuristic detector that draws boxes around objects according to their hue.
Color detectors do not detect black, perfect grays (grays where the red, green, and blue color component values are equal), or white.
It only detects hues found on the color wheel.

{{% alert title="Tip" color="tip" %}}
Object colors can vary dramatically based on the light source.
We recommend you verify the desired color detection value under actual lighting conditions.
To determine the color value from the actual camera component image, you can use a pixel color tool, like [Color Picker for Chrome](https://chrome.google.com/webstore/detail/color-picker-for-chrome/clldacgmdnnanihiibdgemajcfkmfhia).

If the color is not reliably detected, increase the `hue_tolerance_pct`.
{{< /alert >}}

{{< tabs >}}
{{% tab name="Builder" %}}

Navigate to the **CONFIGURE** tab of your machine's page.
Click the **+** icon next to your machine part in the left-hand menu and select **Component or service**.
Select the `vision` type, then select the `color detector` model.
Enter a name or use the suggested name for your service and click **Create**.

In your vision service's panel, select the color your vision service will be detecting, as well as a hue tolerance and a segment size (in pixels):

![Color detector panel with color and hue tolerance selection and a field for the segment size](/services/vision/color-detector-panel.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

Add the vision service object to the services array in your JSON configuration:

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "<service_name>",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": <integer>,
      "detect_color": "#ABCDEF",
      "hue_tolerance_pct": <number>,
      "saturation_cutoff_pct": <number>,
      "value_cutoff_pct": <number>
    }
  },
  ... // Other services
]
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

```json {class="line-numbers linkable-line-numbers"}
"services": [
  {
    "name": "blue_square",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 100,
      "detect_color": "#1C4599",
      "hue_tolerance_pct": 0.07,
      "value_cutoff_pct": 0.15
    }
  },
  {
    "name": "green_triangle",
    "api": "rdk:service:vision",
    "model": "color_detector",
    "attributes": {
      "segment_size_px": 200,
      "detect_color": "#62963F",
      "hue_tolerance_pct": 0.05,
      "value_cutoff_pct": 0.20
    }
  }
]
```

{{% /tab %}}
{{< /tabs >}}

The following parameters are available for a `color_detector`:

<!-- prettier-ignore -->
| Parameter | Required? | Description |
| --------- | --------- | ----------- |
| `segment_size_px` | **Required** | An integer that sets a minimum size (in pixels) of a contiguous color region to be detected, and filters out all other found objects below that size. |
| `detect_color` | **Required** | The color to detect in the image, as a string of the form `#RRGGBB`. The color is written as a hexadecimal string prefixed by ‘#’. |
| `hue_tolerance_pct` | **Required** | A number bigger than 0.0 and smaller than or equal to 1.0 that defines how strictly the detector must match to the hue of the color requested. ~0.0 means the color must match exactly, while 1.0 matches to every color, regardless of the input color. 0.05 is a good starting value. |
| `saturation_cutoff_pct` | Optional | A number > 0.0 and <= 1.0 which defines the minimum saturation before a color is ignored. Defaults to 0.2. |
| `value_cutoff_pct` | Optional | A number > 0.0 and <= 1.0 which defines the minimum value before a color is ignored. Defaults to 0.3. |

{{% alert title="Info" color="info" %}}

**hue_tolerance_pct**, **saturation_cutoff_pct**, and **value_cutoff_pct** refer to hue, saturation, and value (brightness) in the HSV Color Model, but do not set color values in Viam.

**hue_tolerance_pct** specifies the exactness of the color match to **detect_color**.

The optional **saturation_cutoff_pct** and **value_cutoff_pct** attributes specify cutoff thresholds levels for saturation and brightness, rather than specifying color saturation and brightness as they do in the standard HSV Color Model.

{{% /alert %}}

Click the **Save** button in the top right corner of the page.
Proceed to [test your detector](#test-your-detector).

## Test your detector

You can test your detector with [live camera footage](#live-camera-footage) or [existing images](#existing-images).

### Live camera footage

1. Configure a [camera component](/operate/reference/components/camera/).
   {{< alert title="Tip" color="tip" >}}
   This is the camera whose name you need to pass to vision service methods.
   {{< /alert >}}
2. After adding the camera, click the **Save** button in the top right corner of the page.
3. Click on the **Test** area on the vision service configuration panel, or navigate to the **CONTROL** tab, click on the vision service and select your camera and vision service and then click **Refresh**.
   The panel will show detections with confidence above the `default_minimum_confidence` with bounding boxes on the image.

   ![Blue boxes detected](/services/vision/detections.png)

{{% expand "Click to see how to configure a camera live feed that shows detections or classifications" %}}

Configure a [transform camera](/operate/reference/components/camera/transform/) with the following attributes:

```json
{
  "pipeline": [
    {
      "type": "detections",
      "attributes": {
        "confidence_threshold": 0.5,
        "detector_name": "<vision-service-name>",
        "valid_labels": ["<label>"]
      }
    }
  ],
  "source": "<camera-name>"
}
```

Then save your configuration.
Navigate to the **CONTROL** tab, click on your transform camera and toggle it on to see a live feed with detections.

![Detections on a transform camera](/services/vision/transform-detections.png)

{{% /expand%}}

4. To access detections with code, use the Vision Service methods on the camera you configured in step 1.
   The following code gets the machine’s vision service and then runs a color detector vision model on output from the machine's camera `"cam1"`:

   {{% alert title="Tip" color="tip" %}}

   Pass the name of the camera you configured in step 1.
   Do not pass a transform camera that already has the "detections" or "classifications" transform applied to it.

   {{% /alert %}}

   {{< tabs >}}
   {{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient

robot = await connect()
camera_name = "cam1"

# Grab camera from the machine
cam1 = Camera.from_robot(robot, camera_name)
# Grab Viam's vision service for the detector
my_detector = VisionClient.from_robot(robot, "my_detector")

detections = await my_detector.get_detections_from_camera(camera_name)

# If you need to store the image, get the image first
# and then run detections on it. This process is slower:
img = await cam1.get_image()
detections_from_image = await my_detector.get_detections(img)

await robot.close()
```

To learn more about how to use detection, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

    {{% /tab %}}
    {{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/config"
  "go.viam.com/rdk/services/vision"
  "go.viam.com/rdk/components/camera"
  "go.viam.com/rdk/utils"
)

// Grab the camera from the machine
cameraName := "cam1" // make sure to use the same component name that you have in your machine configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

myDetector, err := vision.from_robot(robot, "my_detector")
if err != nil {
    logger.Fatalf("Cannot get vision service: %v", err)
}

// Get detections from the camera output
detections, err := myDetector.DetectionsFromCamera(context.Background(), myCam, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(directDetections) > 0 {
    logger.Info(detections[0])
}

// If you need to store the image, get the image first
// and then run detections on it. This process is slower:

// Get an image from the camera decoded as an image.Image
img, err = camera.DecodeImageFromCamera(context.Background(), utils.MimeTypeJPEG, nil, myCam)
if err != nil {
    logger.Fatalf("Could not decode image from camera: %v", err)
}

// Apply the color classifier to the image from your camera (configured as "cam1")
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
    logger.Info(detectionsFromImage[0])
}

```

To learn more about how to use detection, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

    {{% /tab %}}
    {{< /tabs >}}

### Existing images

If you would like to test your detector with existing images, load the images and pass them to the detector:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.services.vision import VisionClient
from PIL import Image

robot = await connect()
# Grab Viam's vision service for the detector
my_detector = VisionClient.from_robot(robot, "my_detector")

# Load an image
img = Image.open('test-image.png')

# Apply the detector to the image
detections_from_image = await my_detector.get_detections(img)

await robot.close()
```

To learn more about how to use detection, see the [Python SDK docs](https://python.viam.dev/autoapi/viam/services/vision/index.html).

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
  "go.viam.com/rdk/config"
  "go.viam.com/rdk/services/vision"
  "image/jpeg"
  "os"
)

myDetector, err := vision.from_robot(robot, "my_detector")
if err != nil {
    logger.Fatalf("Cannot get Vision Service: %v", err)
}

// Read image from existing file
file, err := os.Open("test-image.jpeg")
if err != nil {
    logger.Fatalf("Could not get image: %v", err)
}
defer file.Close()
img, err := jpeg.Decode(file)
if err != nil {
    logger.Fatalf("Could not decode image: %v", err)
}
defer img.Close()

// Apply the detector to the image
detectionsFromImage, err := myDetector.Detections(context.Background(), img, nil)
if err != nil {
    logger.Fatalf("Could not get detections: %v", err)
}
if len(detectionsFromImage) > 0 {
    logger.Info(detectionsFromImage[0])
}

```

To learn more about how to use detection, see the [Go SDK docs](https://pkg.go.dev/go.viam.com/rdk/vision).

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Tip" color="tip" %}}
To see more code examples of how to use Viam's Vision Service, see [our example repo](https://github.com/viamrobotics/vision-service-examples).
{{% /alert %}}

## Next steps

For general configuration and development info, see:

{{< cards >}}
{{% card link="/operate/get-started/supported-hardware/" noimage="true" %}}
{{% card link="/operate/control/web-app/" noimage="true" %}}
{{< /cards >}}
