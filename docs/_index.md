---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam integrates with hardware and software on any device. Use AI, machine learning, and more to make any machine smarter — for one machine to thousands."
weight: 1
no_list: true
type: "docs"
noToc: true
hide_feedback: true
sitemap:
  priority: 1.0
outputs:
  - html
imageAlt: "/general/understand.png"
images: ["/general/understand.png"]
noedit: true
date: "2024-09-17"
updated: "2024-10-11"
---

<div class="max-page">
  <div class="hero-container">
    <div class="hero-text">
      <h1>Viam Documentation</h1>
      <p>
        Viam integrates with hardware and software on <b>any device</b>. Use AI, machine learning, and more to make any machine smarter—for one machine to thousands.
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
    <img src=viam.svg alt="Robot illustration" class="hero">
  </div>
</div>
<br>

<div class="max-page frontpage">

## Program any device

To get started, install Viam on any device and create a configuration that describes connected hardware as {{< glossary_tooltip term_id="component" text="components" >}}. Then you can control your device and any attached physical hardware securely **from anywhere in the world**. Or from local networks.

{{< tabs class="horizontalheaders program" navheader="Examples">}}
{{% tab name="Drive a base" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def moveInSquare(base):
    for _ in range(4):
        # Move forward 500mm at 500mm/s
        await base.move_straight(velocity=500, distance=500)
        # Spin 90 degrees at 100 degrees/s
        await base.spin(velocity=100, angle=90)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func moveInSquare(ctx context.Context, base base.Base, logger logging.Logger) {
    for i := 0; i < 4; i++ {
        // Move forward 500mm at 500mm/s
        base.MoveStraight(ctx, 600, 500.0, nil)
        // Spin 90 degrees at 100 degrees/s
        base.Spin(ctx, 90, 100.0, nil)
    }
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts
async function moveInSquare(baseClient: VIAM.BaseClient) {
  for (let i = 0; i < 4; i++) {
    // Move forward 500mm at 500mm/s
    await baseClient.moveStraight(500, 500);
    // Spin 90 degrees at 100 degrees/s
    await baseClient.spin(90, 100);
  }
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
Future<void> moveSquare() async {
  for (var i=0; i<4; i++) {
    // Move forward 500mm at 500mm/s
    await base.moveStraight(500, 500);
    // Spins the rover 90 degrees at 100 degrees/s
    await base.spin(90, 100);
  }
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
void move_in_square(std::shared_ptr<viam::sdk::Base> base) {
  for (int i = 0; i < 4; ++i) {
    // Move forward 500mm at 500mm/s
    base->move_straight(500, 500);
    // Spins the rover 90 degrees at 100 degrees/s
    base->spin(90, 100);
  }
}
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

You can use any robotic base with Viam. Configure it as a base component. Then you can drive it using the base API.

[Drive a base →](/how-tos/drive-rover/)

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/try-viam-sdk/image1.webm" mp4_src="/tutorials/try-viam-sdk/image1.mp4" alt="Overhead view of the Viam Rover showing it as it drives in a square.">}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Control motor" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def spin_motor(motor):
    # Turn the motor at 35% power forwards
    await motor.set_power(power=0.35)
    # Let the motor spin for 3 seconds
    time.sleep(3)
    # Stop the motor
    await motor.stop()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func spinMotor(ctx context.Context, motor motor.Motor, logger logging.Logger) {
  // Turn the motor at 35% power forwards
  err = motor.SetPower(context.Background(), 0.35, nil)
  // Let the motor spin for 3 seconds
  time.Sleep(3 * time.Second)
  // Stop the motor
  err = motor.Stop(context.Background(), nil)
}
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts
async function spinMotor(motorClient: VIAM.MotorClient) {
  // Turn the motor at 35% power forwards
  await motorClient.setPower(0.35);
  // Let the motor spin for 3 seconds
  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));
  await sleep(3000);
  // Stop the motor
  await motorClient.stop();
}
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
Future<void> spinMotor() async {
  // Turn the motor at 35% power forwards
  await motorClient.setPower(0.35);
  // Let the motor spin for 3 seconds
  await Future.delayed(Duration(seconds: 3));
  // Stop the motor
  await motorClient.stop();
}
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
void spin_motor(std::shared_ptr<viam::sdk::Motor> motor) {
  // Turn the motor at 35% power forwards
  motor->set_power(0.35);
  // Let the motor spin for 3 seconds
  sleep(3);
  // Stop the motor
  motor->stop();
}
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

You can use any motor with Viam. Configure it as a motor component. Then you can operate it using the motor API.

[Control a motor →](/how-tos/control-motor/)

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/motor.webm" mp4_src="/motor.mp4" alt="A moving motor">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Get sensor reading" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Get the readings provided by the sensor.
co_2_monitor = Sensor.from_robot(machine, "co2-monitor")
co_2_monitor_return_value = await co_2_monitor.get_readings()
print(f"co2-monitor get_readings return value: {co_2_monitor_return_value}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Get the readings provided by the sensor.
co2Monitor, err := sensor.FromRobot(machine, "co2-monitor")
co2MonitorReturnValue, err := co2Monitor.Readings(
  context.Background(), map[string]interface{}{})
logger.Infof("co2-monitor return value: %+v", co2MonitorReturnValue)
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```ts
// Get the readings provided by the sensor.
const co2MonitorClient = new VIAM.SensorClient(machine, "co2-monitor");
const co2MonitorReturnValue = await co2MonitorClient.getReadings();
console.log("co2-monitor return value:", co2MonitorReturnValue);
```

{{% /tab %}}
{{% tab name="Flutter" %}}

```dart
// Get the readings provided by the sensor.
final co2Monitor = Sensor.fromRobot(client, "co2-monitor");
var readings = await co2Monitor.readings();
print(readings);
```

{{% /tab %}}
{{% tab name="C++" %}}

```cpp
// Get the readings provided by the sensor.
auto co2monitor = machine->resource_by_name<Sensor>("co2-monitor");
auto co2monitor_get_readings_return_value = co2monitor->get_readings();
std::cout << "co2-monitor get_readings return value " << co2monitor_get_readings_return_value << "\n";
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

You can use any physical sensor or anything else that provides measurements with Viam. Configure it as a sensor component. Then you can get sensor readings using the sensor API.

[Collect sensor data →](/how-tos/collect-sensor-data/)

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Move an arm" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Command a joint position move: move the forearm of the arm slightly up
cmd_joint_positions = JointPositions(values=[0, 0, -30.0, 0, 0, 0])
await my_arm_component.move_to_joint_positions(
    positions=cmd_joint_positions)

# Generate a simple pose move +100mm in the +Z direction of the arm
cmd_arm_pose = await my_arm_component.get_end_position()
cmd_arm_pose.z += 100.0
await my_arm_component.move_to_position(pose=cmd_arm_pose)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Command a joint position move: move the forearm of the arm slightly up
cmdJointPositions := &armapi.JointPositions{Values: []float64{0.0, 0.0, -30.0, 0.0, 0.0, 0.0}}
err = myArmComponent.MoveToJointPositions(context.Background(), cmdJointPositions, nil)

// Generate a simple pose move +100mm in the +Z direction of the arm
currentArmPose, err := myArmComponent.EndPosition(context.Background(), nil)
adjustedArmPoint := currentArmPose.Point()
adjustedArmPoint.Z += 100.0
cmdArmPose := spatialmath.NewPose(adjustedArmPoint, currentArmPose.Orientation())

err = myArmComponent.MoveToPosition(context.Background(), cmdArmPose, referenceframe.NewEmptyWorldState(), nil)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

You can use any robotic arm with Viam.
Configure it as an arm component. Then you can move it using the arm API.

[Move a robotic arm →](/tutorials/services/accessing-and-moving-robot-arm/)

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Operate custom hardware" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
my_button = Generic.from_robot(robot=machine, name="my_button")

# Use a custom command to push the button 5
command = {"cmd": "push_button", "button": 5}
result = await my_button.do_command(command)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
myButton, err := generic.FromRobot(machine, "my_button")

// Use a custom command to push the button 5
command := map[string]interface{}{"cmd": "push_button", "button": 5}
result, err := myButton.DoCommand(context.Background(), command)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Using the Viam Registry you can create _{{< glossary_tooltip term_id="resource" text="resources" >}}_ for additional hardware types or models and then deploy them to your machines.
You can use an existing component or service type or create generic resources.

[Create a module →](/how-tos/hello-world-module/)

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page frontpage">
<br>
<br>

## Make your devices better and smarter

  <p>
    Pick and choose from additional services. Make your devices understand their environment, interact with it, collect data, and more:
  </p>
</div>

{{< tabs class="horizontalheaders services" navheader="Services">}}
{{% tab name="Computer Vision" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Get image from camera stream on construction site
cam = Camera.from_robot(machine, "construction-site-cam")
img = await cam.get_image()

# Use machine learning model to gather information from the image
hardhat_detector = VisionClient.from_robot(machine, "hardhat_detector")
detections = await hardhat_detector.get_detections(img)

# Check whether a person is detected not wearing a hardhat
for d in detections:
    if d.confidence > 0.8 and d.class_name == "NO-Hardhat":
        print("Violation detected.")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Get image from camera stream on construction site
myCamera, err := camera.FromRobot(machine, "construction-site-cam")
camStream, err := myCamera.Stream(context.Background())
img, release, err := camStream.Next(context.Background())
defer release()

// Use machine learning model to gather information from the image
visService, err := vision.FromRobot(machine, "hardhat_detector")
detections, err := visService.Detections(context.Background(), img, nil)

// Check whether a person is detected not wearing a hardhat
for i := 0; i < len(detections); i++ {
  if (detection[i].confidence > 0.8) && (detection[i].class_name == "NO-Hardhat")  {
    logger.Info("Violation detected.")
  }
}
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Computer vision enables your machine to use connected cameras to interpret the world around it.
With inferences about a machine's surroundings, you can program machines to act based on this input.

[Try the vision service →](/tutorials/projects/helmet/)

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/helmet/hardhat.webm" mp4_src="/tutorials/helmet/hardhat.mp4" alt="A man without a hard hat is detected and labeled as No-Hardhat. Then he puts on a hard hat and a bounding box labeled Hardhat appears. He gives a thumbs-up to the camera.">}}

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Data Management" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Captured Data" %}}

{{<imgproc src="/services/data/air-quality-data.png" resize="1200x" alt="Captured air quality data" class="imgzoom fill aligncenter">}}

{{% /tab %}}
{{% tab name="Query Data" %}}

```python
# Tag data from the my_camera component
my_filter = create_filter(component_name="my_camera")
tags = ["frontview", "trainingdata"]
res = await data_client.add_tags_to_binary_data_by_filter(tags, my_filter)

# Query sensor data by filter
my_data = []
my_filter = create_filter(
    component_name="sensor-1",
    start_time=Timestamp('2024-10-01 10:00:00', tz='US/Pacific'),
    end_time=Timestamp('2024-10-12 18:00:00', tz='US/Pacific')
)
tabular_data, count, last = await data_client.tabular_data_by_filter(
    my_filter, last=None)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Sync sensor data, images, and any other binary or timeseries data from all your machines to the cloud. There, you can query and visualize it.

Intermittent internet connectivity? Your data will sync whenever internet is available.

[Learn about Data Management →](/services/data/)

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Motion" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Add a table obstacle to a WorldState
table_origin = Pose(x=-202.5, y=-546.5, z=-19.0)
table_dimensions = Vector3(x=635.0, y=1271.0, z=38.0)
table_object = Geometry(center=table_origin,
                        box=RectangularPrism(dims_mm=table_dimensions))
obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[table_object])
world_state = WorldState(obstacles=[obstacles_in_frame])

# Destination pose to move to
dest_in_frame = PoseInFrame(
    reference_frame="world",
    pose=Pose(x=510.0, y=0.0, z=526.0, o_x=0.7, o_y=0.0, o_z=-0.7, theta=0.0))

# Move arm to destination pose
motion_service = MotionClient.from_robot(robot, "builtin")
await motion_service.move(
    component_name=Arm.get_resource_name("myArm"),
    destination=dest_in_frame, world_state=world_state)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// Add a table obstacle to a WorldState
obstacles := make([]spatialmath.Geometry, 0)
tableOrigin := spatialmath.NewPose(
  r3.Vector{X: 0.0, Y: 0.0, Z: -10.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.0, OY: 0.0, OZ: 1.0, Theta: 0.0},
)
tableDimensions := r3.Vector{X: 2000.0, Y: 2000.0, Z: 20.0}
tableObj, err := spatialmath.NewBox(tableOrigin, tableDimensions, "table")
obstacles = append(obstacles, tableObj)
obstaclesInFrame := referenceframe.NewGeometriesInFrame(referenceframe.World, obstacles)
worldState, err := referenceframe.NewWorldState([]*referenceframe.GeometriesInFrame{obstaclesInFrame}, nil)

// Destination pose to move to
destinationPose := spatialmath.NewPose(
  r3.Vector{X: 510.0, Y: 0.0, Z: 526.0},
  &spatialmath.OrientationVectorDegrees{OX: 0.7071, OY: 0.0, OZ: -0.7071, Theta: 0.0},
)
destPoseInFrame := referenceframe.NewPoseInFrame(
  referenceframe.World, destinationPose)

// Move arm to destination pose
motionService, err := motion.FromRobot(robot, "builtin")
_, err = motionService.Move(context.Background(), arm.Named("myArm"), destPoseInFrame, worldState, nil, nil)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

The motion service enables your machine to plan and move relative to itself, other machines, and the world.

[Try the motion service →](/tutorials/services/plan-motion-with-arm-gripper/)

  </div>
  <div class="explanationvisual">

{{<gif webm_src="/tutorials/videos/motion_armmoving.webm" mp4_src="/tutorials/videos/motion_armmoving.mp4" alt="An arm moving with the motion service">}}

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Navigation" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Create a new waypoint at the specified latitude and longitude
location = GeoPoint(latitude=40.76275, longitude=-73.96)

# Add waypoint to the service's data storage
await my_nav.add_waypoint(point=location)

my_nav = NavigationClient.from_robot(robot=robot, name="my_nav_service")

# Set the service to operate in waypoint mode and begin navigation
await my_nav.set_mode(Mode.ValueType.MODE_WAYPOINT)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Create a new waypoint at the specified latitude and longitude
location = geo.NewPoint(40.76275, -73.96)

// Add waypoint to the service's data storage
err := myNav.AddWaypoint(context.Background(), location, nil)

myNav, err := navigation.FromRobot(robot, "my_nav_service")

// Set the service to operate in waypoint mode and begin navigation
mode, err := myNav.SetMode(context.Background(), Mode.MODE_WAYPOINT, nil)
```

{{% /tab %}}
{{% tab name="Viam app" %}}

{{< imgproc src="/services/navigation/navigation-control-card.png" alt="An example control interface for a navigation service in the Viam app Control Tab." resize="1200x" class="imgzoom aligncenter" >}}

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Use the navigation service to autonomously navigate a machine to defined waypoints.

[Try the navigation service →](/tutorials/services/navigate-with-rover-base/)

  </div>
</div>
</div>
{{% /tab %}}
{{% tab name="Custom Logic" %}}
<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Python" %}}

```python
my_twilio_svc = Generic.from_robot(robot=machine, name="my_twilio_svc")

# Use a custom command to send a text message with Twilio
command = {"to": "+1 234 567 8901", "body": "Hello world!"}
result = await my_twilio_svc.do_command(command)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
myTwilioSvc, err := generic.FromRobot(machine, "my_twilio_svc")

// Use a custom command to send a text message with Twilio
command := map[string]interface{}{"to": "+1 234 567 8901", "body": "Hello world!"}
result, err := myTwilioSvc.DoCommand(context.Background(), command)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Using the Viam Registry you can turn services and your own custom business logic into _{{< glossary_tooltip term_id="module" text="modules" >}}_. You can then deploy your modules to your machines.

[Create a module →](/how-tos/create-module/)

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page frontpage">
<br>
<br>

## Go from one machine to thousands

  <p>
    When you connect machines to the cloud you get fleet management tools that let you scale. Go from one prototype to thousands of machines you can manage and operate from one place using the Viam Cloud.
  </p>
</div>

{{< tabs class="horizontalheaders platform" navheader="Capabilities">}}
{{% tab name="Deployment" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Fragment" %}}

```json
// Reusable configuration for using a software package
{
  "services": [
    {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio"
    }
  ],
  "modules": [
    {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      // Specific version to deploy
      "version": "0.5.2"
    }
  ]
}
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Manage hardware and software for multiple machines using a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_.
You can make changes to some or all of your machines in one go.

[Deploy packages across devices →](/how-tos/deploy-packages/)

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Provisioning" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Shell" %}}

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

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Provisioning allows you to complete part of the machine setup during the manufacturing process. The rest of the first-time setup happens once the machine is taken into operation.
This way, machines automatically get the latest updates.

[Learn about provisioning →](/fleet/provision/)

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Observability" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Viam app" %}}

{{< imgproc src="/fleet/dashboard.png" alt="Dashboard view of machine status information" resize="1200x" class="imgzoom aligncenter" >}}

{{% /tab %}}
{{% tab name="Python" %}}

```python
# Get all machines in a location
machines = await cloud.list_robots(location_id="abcde1fghi")

for m in machines:
    # Connect and get status information or latest logs
    machine_parts = await cloud.get_robot_parts(m.id)
    main_part = next(filter(lambda part: part.main_part, machine_parts), None)

    try:
        # Get status for machine
        machine = await connect(main_part.fqdn)
        status = await machine.get_machine_status()
    except ConnectionError:
        # If no connection can be made, get last logs
        logs = await cloud.get_robot_part_logs(
            robot_part_id=main_part.id, num_log_entries=5)
```

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Get status information and logs from all your deployed machines.

[Learn about Platform APIs →](/appendix/apis/#platform-apis)

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="ML Training" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Viam app" %}}

{{< imgproc src="/tutorials/data-management/train-model.png" alt="The data tab showing the train a model pane" resize="1200x" class="imgzoom" >}}

{{% /tab %}}
{{% tab name="Python" %}}

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

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Build machine learning models based on your machines' data. You can pick from different training algorithms or create your own.

[Train and deploy ML models →](/how-tos/train-deploy-ml/)

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Collaboration" %}}

<div class="innertabcontentcontainer">

{{< tabs >}}
{{% tab name="Viam app" %}}

{{<imgproc src="/cloud/rbac.png" resize="1000x" declaredimensions=true alt="Organization page" class="imgzoom fill aligncenter">}}

{{% /tab %}}
{{% tab name="Python" %}}

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

{{% /tab %}}
{{< /tabs >}}

<div class="explanation">
  <div class="explanationtext">

Viam allows you to organize and manage any number of machines. When collaborating with others, you can assign permissions using Role-Based Access Control (RBAC).

[Learn about access control →](/cloud/rbac/)

  </div>
</div>
</div>

{{% /tab %}}
{{< /tabs >}}
