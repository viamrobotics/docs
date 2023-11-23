The following example assumes you have a [camera](/platform/build/configure/components/camera/) called `camera0` configured as a component of your robot.
If your camera has a different name in the Viam app, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera

robot = await connect() # refer to connect code above
my_cam = Camera.from_robot(robot, "camera0")
# Gets a single image from the camera stream
image = await my_cam.get_image()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
import (
"go.viam.com/rdk/components/camera"
)

// grab the camera from the robot
cameraName := "camera0" // make sure to use the same component name that you have in your robot configuration
myCam, err := camera.FromRobot(robot, cameraName)
if err != nil {
  logger.Fatalf("cannot get camera: %v", err)
}

// gets the stream from a camera
camStream, err := myCam.Stream(context.Background())

// gets an image from the camera stream
img, release, err := camStream.Next(context.Background())
defer release()
```

{{% /tab %}}
{{% /tabs %}}
