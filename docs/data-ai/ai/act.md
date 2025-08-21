---
linkTitle: "Act based on inferences"
title: "Act based on inferences"
weight: 70
layout: "docs"
type: "docs"
description: "Use the vision service API to act based on inferences."
next: "/data-ai/train/upload-external-data/"
---

You can use the [vision service API](/dev/reference/apis/services/vision/) to get information about your machine's inferences and program behavior based on that.

The following are examples of what you can do using a vision service alongside hardware:

- [Line following robot](#program-a-line-following-robot): Using computer vision to follow objects or a pre-determined path
- [Accident prevention and quality assurance](#act-in-industrial-applications)

## Program a line following robot

For example, you can [program a line following robot](/tutorials/services/color-detection-scuttle/) that uses a vision service to follow a colored object.

You can use the following code to detect and follow the location of a colored object:

{{% expand "Click to view code" %}}

```python {class="line-numbers linkable-line-numbers"}
async def connect():
    opts = RobotClient.Options.with_api_key(
        # TODO: Replace "<API-KEY>" (including brackets) with your machine's
        # API key
        api_key='<API-KEY>',
        # TODO: Replace "<API-KEY-ID>" (including brackets) with your machine's
        # API key ID
        api_key_id='<API-KEY-ID>'
    )
    # TODO: Replace "<MACHINE-ADDRESS>" with address from the CONNECT tab.
    return await RobotClient.at_address("<MACHINE-ADDRESS>", opts)


# Get largest detection box and see if it's center is in the left, center, or
# right third
def leftOrRight(detections, midpoint):
    largest_area = 0
    largest = {"x_max": 0, "x_min": 0, "y_max": 0, "y_min": 0}
    if not detections:
        print("nothing detected :(")
        return -1
    for d in detections:
        a = (d.x_max - d.x_min) * (d.y_max-d.y_min)
        if a > largest_area:
            a = largest_area
            largest = d
    centerX = largest.x_min + largest.x_max/2
    if centerX < midpoint-midpoint/6:
        return 0  # on the left
    if centerX > midpoint+midpoint/6:
        return 2  # on the right
    else:
        return 1  # basically centered


async def main():
    spinNum = 10         # when turning, spin the motor this much
    straightNum = 300    # when going straight, spin motor this much
    numCycles = 200      # run the loop X times
    vel = 500            # go this fast when moving motor

    # Connect to robot client and set up components
    machine = await connect()
    base = Base.from_robot(machine, "my_base")
    camera_name = "<camera-name>"
    camera = Camera.from_robot(machine, camera_name)
    frame = await camera.get_image(mime_type="image/jpeg")

    # Convert to PIL Image
    pil_frame = viam_to_pil_image(frame)

    # Grab the vision service for the detector
    my_detector = VisionClient.from_robot(machine, "my_color_detector")

    # Main loop. Detect the ball, determine if it's on the left or right, and
    # head that way. Repeat this for numCycles
    for i in range(numCycles):
        detections = await my_detector.get_detections_from_camera(camera_name)

        answer = leftOrRight(detections, pil_frame.size[0]/2)
        if answer == 0:
            print("left")
            await base.spin(spinNum, vel)     # CCW is positive
            await base.move_straight(straightNum, vel)
        if answer == 1:
            print("center")
            await base.move_straight(straightNum, vel)
        if answer == 2:
            print("right")
            await base.spin(-spinNum, vel)
        # If nothing is detected, nothing moves

    await robot.close()

if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")
```

{{% /expand%}}

If you configured the color detector to detect red, your rover should detect and navigate towards any red objects that come into view of its camera.
Use something like a red sports ball or book cover as a target to follow to test your rover:

<div class="aligncenter">
{{<video webm_src="https://storage.googleapis.com/docs-blog/tutorials/videos/scuttledemos_colordetection.webm" mp4_src="https://storage.googleapis.com/docs-blog/tutorials/videos/scuttledemos_colordetection.mp4" poster="/tutorials/scuttlebot/scuttledemos_colordetection.jpg" alt="Detecting color with a Scuttle Robot">}}
</div>

## Act in industrial applications

You can also act based on inferences in an industrial context.
For example, you can program a robot arm to halt operations when workers enter dangerous zones, preventing potential accidents.

The code for this would look like:

```python {class="line-numbers linkable-line-numbers"}
detections = await detector.get_detections_from_camera(camera_name)
for d in detections:
    if d.confidence > 0.6 and d.class_name == "PERSON":
        arm.stop()
```

You can also use inferences of computer vision for quality assurance purposes.
For example, you can program a robot arm doing automated harvesting to use vision to identify ripe produce and pick crops selectively.

The code for this would look like:

```python {class="line-numbers linkable-line-numbers"}
classifications = await detector.get_classifications_from_camera(
    camera_name,
    4)
for c in classifications:
    if d.confidence > 0.6 and d.class_name == "RIPE":
        arm.pick()
```

To get inferences programmatically, you will want to use the vision service API:

{{< cards >}}
{{% card link="/dev/reference/apis/services/vision/" customTitle="Vision service API" noimage="True" %}}
{{< /cards >}}

To implement industrial solutions in code, you can also explore the following component APIs:

{{< cards >}}
{{< card link="/dev/reference/apis/components/arm/" customTitle="Arm API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/base/" customTitle="Base API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/camera/" customTitle="Camera API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/gripper/" customTitle="Gripper API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/motor/" customTitle="Motor API" noimage="True" >}}
{{< card link="/dev/reference/apis/components/sensor/" customTitle="Sensor API" noimage="True" >}}
{{< /cards >}}
