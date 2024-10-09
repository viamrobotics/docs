---
title: "Viam Documentation"
linkTitle: "Viam Documentation"
description: "Viam is a complete software platform for smart machines that runs on any 64-bit Linux OS and macOS."
weight: 1
no_list: true
type: "docs"
noToc: true
hide_feedback: true
sitemap:
  priority: 1.0
outputs:
  - html
carouselscript: true
date: "2024-09-17"
# updated: ""  # When the content was last entirely checked
---

<div class="max-page">
  <p>
    Welcome to the Viam Documentation!
    Viam is a software platform that makes it easy to combine and integrate hardware and software to build machines, connect them with the cloud, and make them smarter with machine learning.
  </p>
  <div class="cards max-page use-cases aligncenter">
    <div class="front-card-container">
      <div class="hover-card primary">
        <a href="how-tos/" class="noanchor">
        <div>
          <p>How-to Guides</p>
        </div>
      </a>
      </div>
      <div class="hover-card">
        <a href="platform/" class="noanchor"><div>
        <p>Platform Reference</p></div>
        </a>
      </div>
    </div>
  </div>
</div>
<br>
<div class="max-page">
  <h2 class="frontpage-headers">Program any device</h2>
  <p>
    Viam integrates with hardware and software on <b>any device</b>. Once installed, you can control your devices and any attached physical hardware like this:
  </p>

{{< tabs class="horizontalheaders">}}
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
{{% tab name="Get image from camera" %}}
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
{{% tab name="Get sensor reading" %}}
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

  TODO

  </div>
  <div class="explanationvisual">

  TODO

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page">
  <h2 class="frontpage-headers">Make your devices better and smarter</h2>
  <p>
    You can pick and choose from additional tools to make your devices understand their environment, interact with it, and collect information:
  </p>
</div>

{{< tabs class="horizontalheaders">}}
{{% tab name="Computer Vision" %}}

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
{{% tab name="Machine Learning" %}}
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
{{% tab name="Data Management" %}}
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
{{% tab name="Motion" %}}
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
{{% tab name="Navigation" %}}
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

  TODO

  </div>
</div>
</div>
{{% /tab %}}
{{< /tabs >}}

<div class="max-page">
  <h2 class="frontpage-headers">Go from one machine to thousands</h2>
  <p>
    When you connect machines to the cloud you get fleet management tools that let you scale from one prototype to thousands of machines you can manage and operate from one place.
  </p>
</div>

{{< tabs class="horizontalheaders">}}
{{% tab name="Deployment" %}}

<div class="tabcontent">

```json
{
  "services": [ {
      "name": "speech-1",
      "namespace": "viam-labs",
      "type": "speech",
      "model": "viam-labs:speech:speechio",
    } ],
  "modules": [ {
      "type": "registry",
      "name": "viam-labs_speech",
      "module_id": "viam-labs:speech",
      "version": "0.5.2"
    } ]
}
```

<div class="explanation">
  <div class="explanationtext">

You can deploy software packages to many machines and keep those software packages versioned. Viam has a built-in tool called _{{< glossary_tooltip term_id="fragment" text="fragments" >}}_ for using the same configuration on multiple machines.

For more information, see [Deploy and update packages across devices](/how-tos/deploy-packages/).

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Provisioning" %}}

<div class="tabcontent">

```sh {class="command-line" data-prompt="$" data-output="2-5"}
echo "{
  "manufacturer": "Company",
  "model": "SmartRover",
  "fragment_id": "11d1059b-eaed-4ad8-9fd8-d60ad7386aa2"
}" >> viam-provisioning.json

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
{{% tab name="Remote Diagnostics" %}}

<div class="tabcontent">

```python
# Get all machines in a location
machines = await cloud.list_robots(location_id="gjmjt2xntj")
print("Found {} machines.".format(len(machines)))

for m in machines:
    # Connect and get status information or latest logs
    machine_parts = await cloud.get_robot_parts(m.id)
    main_part = next(filter(lambda part: part.main_part, machine_parts), None)
    print("Attempting to connect to {}...".format(main_part.fqdn))

    try:
        machine = await connect(main_part.fqdn)
        status = await machine.get_machine_status()
        print(status)

    except ConnectionError:
        print("Unable to establish a connection to the machine.")
        logs = await cloud.get_robot_part_logs(
            robot_part_id=main_part.id, num_log_entries=5)
        for log in logs:
            print("{}-{} {}: {}".format(
                log.logger_name, log.level, log.time, log.message))
```

<div class="explanation">
  <div class="explanationtext">

Get status information and logs fromo all your deployed machines.

For more information, see [Fleet Management API](/appendix/apis/fleet/) and [Machine Management API](/appendix/apis/robot/).

  </div>
</div>
</div>

{{% /tab %}}
{{% tab name="Data Management" %}}

<div class="tabcontent">

```python
# Query sensor data
data = await data_client.tabular_data_by_sql(
    org_id="<YOUR-ORG-ID>",
    sql_query="select count(*) as numStanding from readings \
      where robot_id = 'abcdef12-abcd-abcd-abcd-abcdef123456' and \
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
job_id = await ml_training_client.submit_training_job(
  org_id="bccf8f8f-e3c4-4f72-ab9a-fc547757f352",
  dataset_id="66db6fe7d93d1ade24cd1dc3",
  model_name="recognize_gestures",
  model_version="1",
  model_type=ModelType.MODEL_TYPE_MULTI_LABEL_CLASSIFICATION,
  tags=["follow", "stop"]
)

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
{{< /tabs >}}
