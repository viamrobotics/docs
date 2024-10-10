---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam is a software platform that makes it easy to integrate hardware and software to build machines, connect them with the cloud, and make them smarter."
weight: 1
no_list: true
type: "docs"
noToc: true
hide_feedback: true
sitemap:
  priority: 1.0
outputs:
  - html
aliases:
  - "/getting-started/"
  - "/getting-started/high-level-overview"
  - "/product-overviews/"
  - "/viam/"
  - "/viam/app.viam.com/"
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
noedit: true
date: "2024-09-17"
# updated: ""  # When the content was last entirely checked
---

<div class="max-page">
  <div class="hero-container">
    <div class="hero-text">
      <h1>Viam Documentation</h1>
      <p>
        Welcome to the Viam Documentation!
        Viam is a software platform that makes it easy to combine and integrate hardware and software to build machines, connect them with the cloud, and make them smarter with machine learning.
      </p>
      <div class="cards max-page">
        <div class="front-card-container">
          <div class="hover-card primary">
            <a href="how-tos/" class="noanchor">
            <div>
              <p>How-to Guides</p>
            </div>
          </a>
          </div>
          <div class="cta secondary">
            <a href="platform/" class="noanchor"><div>
            <p>Platform Reference →</p></div>
            </a>
          </div>
        </div>
      </div>
    </div>
    <img src=viam.svg class="hero">
  </div>
</div>
<br>
<hr>
<div class="max-page">
<br>
<br>
  <h2 class="frontpage-headers">Program any device</h2>
  <p>

Viam integrates with hardware and software on **any device**. To get started, install Viam and create a configuration that describes your machine's {{< glossary_tooltip term_id="component" text="components" >}}. Then you can control your devices and any attached physical hardware **from anywhere in the world** as well as from local networks:

  </p>

{{< tabs class="horizontalheaders program">}}
{{% tab name="Drive any base" %}}

<div class="tabcontent">

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def moveInSquare(base):
    for _ in range(4):
        # move forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        # spin 90 degrees at 100 degrees/s
        await base.spin(velocity=100, angle=90)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // move forward 500mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        // spin 90 degrees at 100 degrees/s
        base.Spin(ctx, 90, 100.0, nil)
    }
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts
async function moveInSquare(baseClient: VIAM.BaseClient) {
  for (let i = 0; i < 4; i++) {
    // move forward 500mm at 500mm/s
    await baseClient.moveStraight(500, 500);
    // spin 90 degrees at 100 degrees/s
    await baseClient.spin(90, 100);
  }
}
```


{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
Future<void> moveSquare() async {
  for (var i=0; i<4; i++) {
    // move forward 500mm at 500mm/s
    await base.moveStraight(500, 500);
    // spins the rover 90 degrees at 100 degrees/s
    await base.spin(90, 100);
  }
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    // move forward 500mm at 500mm/s
    base->move_straight(500, 500);
    // spins the rover 90 degrees at 100 degrees/s
    base->spin(90, 100);
  }
}
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Try it yourself, [drive a rover](/how-tos/drive-rover/).

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square.">}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Control motor" %}}
<div class="tabcontent">

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def spin_motor(motor):
    # turn the motor at 35% power forwards
    await motor.set_power(power=0.35)
    # let the motor spin for 3 seconds
    time.sleep(3)
    # stop the motor
    await await motor_1.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func spinMotor(ctx context.Context, motor motor.Motor, logger logging.Logger) {
  // turn the motor at 35% power forwards
  err = motor1Component.SetPower(context.Background(), 0.35, nil)
  // let the motor spin for 3 seconds
  time.Sleep(3 * time.Second)
  // stop the motor
  err = motor1Component.Stop(context.Background(), nil)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts
async function spinMotor(motorClient: VIAM.MotorClient) {
  // turn the motor at 35% power forwards
  await motor.setPower(0.35);
  // let the motor spin for 3 seconds
  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));
  await sleep(3000);
  // stop the motor
  await motor.stop();
}
```


{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
Future<void> spinMotor() async {
  // turn the motor at 35% power forwards
  await motorClient.setPower(0.35);
  // let the motor spin for 3 seconds
  // TODO (also fix control-motor...)

  // stop the motor
  await motorClient.stop();
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
void spin_motor(std::shared_ptr<viam::sdk::Motor> motor) {
  // turn the motor at 35% power forwards
  motor->set_power(0.35);
  // let the motor spin for 3 seconds
  sleep(3);
  // stop the motor
  motor->stop();
}
```


{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Try it yourself, [control a motor](/how-tos/control-motor/).

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/single-component-tutorials-servo-mousemover/angle-100.webm" mp4_src="/tutorials/single-component-tutorials-servo-mousemover/angle-100.mp4" alt="A gif at the top of the CONTROL tab in the Viam app. The pointer finger is pressing the 10 button and it changes the angle from 90 to 100 repeatedly. The red STOP button is in the upper right corner. There is a blue circular arrow depicting the servo's direction as being counterclockwise. Below this is a gif of the Raspberry Pi to the left and the FS90R servo on the right. The servo stops, then spins counterclockwise repeatedly.">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Get sensor reading" %}}
<div class="tabcontent">

```python
TODO
```

<div class="explanation">
  <div class="explanationtext">

  TODO: figure out zoom on video

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/services/data/monitor.webm" mp4_src="/services/data/monitor.mp4" alt="Getting performance metrics">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Move an arm" %}}
<div class="tabcontent">

```python
TODO
```

<div class="explanation">
  <div class="explanationtext">

  TODO

  </div>
  <div class="explanationvisual">

  TODO

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Operate custom hardware" %}}
<div class="tabcontent">

```python
TODO
```

<div class="explanation">
  <div class="explanationtext">

  To support more hardware and software, you can use _{{< glossary_tooltip term_id="module" text="modules" >}}_ from the [Viam Registry](/registry/) or create your own for custom needs.

  </div>
  <div class="explanationvisual">

  TODO

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page">
<br>
<br>
  <h2 class="frontpage-headers">Make your devices better and smarter</h2>
  <p>
    You can pick and choose from additional services to make your devices understand their environment, interact with it, collect information, and more:
  </p>
</div>

{{< tabs class="horizontalheaders services">}}
{{% tab name="Computer Vision" %}}

<div class="tabcontent">

```python
# get image from camera stream on construction site
cam = Camera.from_robot(machine, "construction-site-cam")
img = await cam.get_image()

# use machine learning model to gather information from the image
hardhat_detector = VisionClient.from_robot(machine, "hardhat_detector")
detections = await hardhat_detector.get_detections(img)

# check whether a person is detected not wearing a hardhat
for d in detections:
  if d.confidence > 0.8 and d.class_name == "NO-Hardhat":
    print("Violation detected.")
```

<div class="explanation">
  <div class="explanationtext">

  Computer vision enables your machine to use connected cameras to sense and interpret the world around them.
  With inferences about a machine's surroundings, you can program machine behavior to adapt to change accordingly.

  To find out more, see [vision service](/services/vision/) or check out the tutorial [Monitor Job Site Helmet Usage with Computer Vision](/tutorials/projects/helmet/).

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/helmet/hardhat.webm" mp4_src="/tutorials/helmet/hardhat.mp4" alt="A man without a hard hat is detected and labeled as No-Hardhat. Then he puts on a hard hat and a bounding box labeled Hardhat appears. He gives a thumbs-up to the camera.">}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Data Capture & Sync" %}}
<div class="tabcontent">

{{<imgproc src="/services/data/data-capture-sync.png" resize="1200x" declaredimensions=true alt="Configuration to capture data for a camera" class="imgzoom aligncenter" style="max-width:500px">}}

<div class="explanation">
  <div class="explanationtext">

Sync sensor data, images, and any other binary or timeseries data from all your machines to the cloud, where you can manage and query it.

If you have machines with intermittent internet connectivity, your data will sync whenever internet is available.
For more information, see [Data Management](/services/data/).

  </div>
  <div class="explanationvisual">

{{<imgproc src="/tutorials/data-management/shapes-dataset.png" resize="1200x" alt="A sample dataset." class="imgzoom fill aligncenter">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Motion" %}}
<div class="tabcontent">

{{< tabs >}}
{{% tab name="Python" %}}

```python
my_gripper_resource = Gripper.get_resource_name("gripper")

# Move the gripper in the -Z direction with respect to its own reference frame
gripper_pose_rev = Pose(x=0.0,
                        y=0.0,
                        z=-100.0,
                        o_x=0.0,
                        o_y=0.0,
                        o_z=1.0,
                        theta=0.0)
# Note the change in frame name
gripper_pose_rev_in_frame = PoseInFrame(
    reference_frame=my_gripper_resource.name,
    pose=gripper_pose_rev)

motion_service = MotionClient.from_robot(robot, "builtin")
await motion_service.move(component_name=my_gripper_resource,
                          destination=gripper_pose_rev_in_frame,
                          world_state=world_state)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
gripperName := "myGripper"
gripperResource := gripper.Named(gripperName)

// This will move the gripper in the -Z direction with respect to its own reference frame
gripperPoseRev := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -100.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
gripperPoseRevInFrame := referenceframe.NewPoseInFrame(gripperName, gripperPoseRev) // Note the change in frame name

motionService, err := motion.FromRobot(robot, "builtin")
_, err = motionService.Move(context.Background(), gripperResource, gripperPoseRevInFrame, worldState, nil, nil)
if err != nil {
  logger.Fatal(err)
}
```

{{% /tab %}}
{{< /tabs >}}


<div class="explanation">
  <div class="explanationtext">

The builtin motion service enables your machine to plan and move itself or its components relative to itself, other machines, and the world.

For more information, see [motion service](/services/motion/).

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/videos/motion_armmoving.webm" mp4_src="/tutorials/videos/motion_armmoving.mp4" alt="An arm moving with the motion service">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Navigation" %}}
<div class="tabcontent">

```python
TODO
```

<div class="explanation">
  <div class="explanationtext">

Example use case:

- Allow delivery robots to use their location and SLAM to navigate intelligently between GPS coordinates.

  </div>
  <div class="explanationvisual">

  TODO
  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Custom Logic" %}}
<div class="tabcontent">

```python
TODO
```

<div class="explanation">
  <div class="explanationtext">

  TODO

  </div>
  <div class="explanationvisual">

  /how-tos/develop-app/

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page">
<br>
<br>
  <h2 class="frontpage-headers">Go from one machine to thousands</h2>
  <p>
    When you connect machines to the cloud you get fleet management tools that let you scale from one prototype to thousands of machines you can manage and operate from one place using the Viam Cloud.
  </p>
</div>

{{< tabs class="horizontalheaders platform">}}
{{% tab name="Deployment" %}}

<div class="tabcontent">

```json
// Reusable configuration for using a software package
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      // specific version to deploy
      "version": "0.5.2"
    }
  ]
}
```

<div class="explanation">
  <div class="explanationtext">

Configure and update hardware, software, and machine learning models for groups of machines in one go.
Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.

For more information, see [Deploy and update packages across devices](/how-tos/deploy-packages/).

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Provisioning" %}}

<div class="tabcontent">

```sh {class="command-line" data-prompt="$" data-output="3-5,6,7"}
# Create configuration for provisioning machines with a fragment
echo "{
  "manufacturer": "Company",
  "model": "SmartRover",
  "fragment_id": "11d1059b-eaed-4ad8-9fd8-d60ad7386aa2"
}" >> viam-provisioning.json

# Get and run the script to install viam on a board.
wget https://storage.googleapis.com/packages.viam.com/apps/viam-agent/preinstall.sh
chmod 755 preinstall.sh
sudo ./preinstall.sh
```

<div class="explanation">
  <div class="explanationtext">

Provisioning allows you to complete part of the machine setup during the manufacturing process and perform the rest of the first-time setup once the machine is taken into operation.
When the machine is taken into operation, it will automatically get the latest configuration and updates.

For more information, see [Provisioning](/fleet/provision/).

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Observability" %}}

<div class="tabcontent">

```python
# Get all machines in a location
machines = await cloud.list_robots(location_id="abcde1fghi")
print("Found {} machines.".format(len(machines)))

for m in machines:
    # Connect and get status information or latest logs
    machine_parts = await cloud.get_robot_parts(m.id)
    main_part = next(filter(lambda part: part.main_part, machine_parts), None)
    print("Attempting to connect to {}...".format(main_part.fqdn))

    try:
        # Get status for machine
        machine = await connect(main_part.fqdn)
        status = await machine.get_machine_status()

    except ConnectionError:
        # If no connection can be made, get last logs
        logs = await cloud.get_robot_part_logs(
            robot_part_id=main_part.id, num_log_entries=5)
```

<div class="explanation">
  <div class="explanationtext">

Get status information and logs fromo all your deployed machines.

For more information, see [Fleet Management API](/appendix/apis/fleet/) and [Machine Management API](/appendix/apis/robot/).

  </div>
  <div class="explanationvisual">

{{< imgproc src="/fleet/dashboard.png" alt="Dashboard view of machine status information" resize="1200x" class="imgzoom" >}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Data Management" %}}

<div class="tabcontent">

```python
# Tag data from the my_camera component
my_filter = create_filter(component_name="my_camera")
tags = ["frontview", "trainingdata"]
res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)

# Query sensor data by filter
my_data = []
my_filter = create_filter(component_name="sensor-1",
    start_time=Timestamp('2024-10-01 10:00:00', tz='US/Pacific'),
    end_time=Timestamp('2024-10-12 18:00:00', tz='US/Pacific'))
last = None
while True:
    tabular_data, count, last = await data_client.tabular_data_by_filter(
        my_filter, last=last)
    if not tabular_data:
        break
    my_data.extend(tabular_data)

# Query sensor data for a location with SQL
tabular_data_sql = await data_client.tabular_data_by_sql(
    organization_id="abbc1c1c-d2e3-5f67-ab8c-de912345f678",
    sql_query="select count(*) as numStanding from readings \
      where location_id = 'abcde1fghi' and \
      component_name = 'my-ultrasonic-sensor' and \
      (CAST (data.readings.distance AS DOUBLE)) > 0.2"
)
```

<div class="explanation">
  <div class="explanationtext">


Data from your devices is synced to the cloud, where you can query and visualize it.

For more information, see [Data Management](/services/data/).

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="ML Training" %}}

<div class="tabcontent">

```python
# Start a training job to create a classification model based on the dataset
job_id = await ml_training_client.submit_training_job(
    org_id="abbc1c1c-d2e3-5f67-ab8c-de912345f678",
    dataset_id="12ab3cd4e56f7abc89de1fa2",
    model_name="recognize_gestures",
    model_version="1",
    model_type=ModelType.MODEL_TYPE_MULTI_LABEL_CLASSIFICATION,
    tags=["follow", "stop"]
)

# Get status information for training job
job_metadata = await ml_training_client.get_training_job(
    id=job_id)
```

<div class="explanation">
  <div class="explanationtext">

You can build machine learning models based on your machines' data using Viam's training algorithms or your own.

For more information, see [Train and deploy ML models](/how-tos/deploy-ml/) and [Create custom training scripts](/how-tos/create-custom-training-scripts/).

  </div>
  <div class="explanationvisual">

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" resize="1200x" class="imgzoom" >}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Collaboration" %}}

<div class="tabcontent">

```python
# Create a new machine
new_machine_id = await cloud.new_robot(
    name="new-machine", location_id="abcde1fghi")

# Get organization associated with authenticated user / API key
org_list = await cloud.list_organizations()

# Create a new API key with owner access for the new machine
auth = APIKeyAuthorization(
    role="owner",
    resource_type="robot",
    resource_id=new_machine_id
)
api_key, api_key_id = await cloud.create_key(
    org_list[0].id, [auth], "key_for_new_machine")

```

<div class="explanation">
  <div class="explanationtext">

Viam allows you to organize and manage any number of machines in collaboration with others using Role-Based Access Control (RBAC).

You can manage your fleet of machines and the access to them from the [Viam app](https://app.viam.com), using the [CLI](/cli/#authenticate), or using the [fleet management API](/appendix/apis/fleet/).

  </div>
  <div class="explanationvisual">

{{<imgproc src="/cloud/rbac.png" resize="1000x" declaredimensions=true alt="Organization page" class="imgzoom">}}

  </div>
</div>
</div>

{{% /tab %}}
{{< /tabs >}}
