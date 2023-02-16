This reads a single image from a [camera](/components/camera/) called "camera0" on the robot.

The following example assumes you have a camera called `camera0` configured as a component of your robot.
If your camera has a different name, change the `name` in the example.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
from viam.components.camera import Camera

robot = await connect() # refer to connect code above
my_cam = Camera.from_robot(robot, "camera0")
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
