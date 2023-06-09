---
title: "Tipsy: Create an Autonomous Drink Carrying Robot"
linkTitle: "Drink Serving Robot"
weight: 60
type: "docs"
tags: ["raspberry pi", "app", "board", "motor", "camera"]
description: "Create an autonomous drink carrying robot with motion sensing and machine learning."
images: ["/tutorials/img/tipsy/tipsy-preview.gif"]
videoAlt: "Tipsy robot carrying drinks"
webmSrc: "/tutorials/img/tipsy/tipsy-preview.webm"
mp4Src: "/tutorials/img/tipsy/tipsy-preview.mp4"

# Author: Hazal
---

<img src="../../img/tipsy/tipsy.jpg" alt="Tipsy robot carrying drinks" class="alignright" width="300px">

Tipsy makes it easy to replenish everyone's drinks at a party.
Designed with ultrasonic sensors and cameras, Tipsy is equipped to detect the presence of obstacles and people in its surrounding area.
While avoiding the obstacles with the ultrasonic sensor distance measurements, it identifies the people using a ML model and object detection and moves towards them with ease.
Once it reaches the person, Tipsy allows people to grab a drink without ever having to leave their spot, since Tipsy brings a bucket of ice cold drinks within arm's reach.

This tutorial will teach you how to build your own drink-carrying robot.

## Requirements

### Hardware

To build your own drink-carrying robot, you need the following hardware:

* [Raspberry Pi](https://a.co/d/bxEdcAT), with [microSD card](https://www.amazon.com/Lexar-Micro-microSDHC-Memory-Adapter/dp/B08XQ7NGG1/ref=sr_1_13), setup following the [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/).
* Assembled [Scuttle rover](https://www.scuttlerobot.org/product/scuttle-v3) with the motors and motor driver that comes with it.
* [T-slotted framing](https://www.mcmaster.com/products/structural-framing/t-slotted-framing-rails-4/system-of-measurement~metric/rail-height~30mm/): 4 single 4 slot rails, 30 mm square, hollow, 3’ long.
These are for the height of the robot.
* [T-slotted framing](https://www.mcmaster.com/products/structural-framing/t-slotted-framing-rails-4/system-of-measurement~metric/rail-height~30mm/): 2 single 4 slot rail, 30 mm square, hollow, 12 inches long.
These are to create a base inside the robot to securely hold the drink box.
* [T-slotted framing structural brackets](https://www.amazon.com/Aluminum-Connector-Extrusion-Profiles-Accessories/dp/B08NC46L9K/ref=sr_1_14): 30mm rail height.
* Two [ultrasonic sensors](https://www.amazon.com/WWZMDiB-HC-SR04-Ultrasonic-Distance-Measuring/dp/B0B1MJJLJP/ref=sr_1_4)
* A [12V battery](https://www.amazon.com/ExpertPower-EXP1270-Rechargeable-Lead-Battery/dp/B003S1RQ2S/ref=sr_1_4) with [charger](https://www.amazon.com/dp/B0BC3Y5N3Q/ref=vp_d_pd_b2b_qd_vp_pd)
* DC-DC converter, 12v in, 5v out
* USB camera
* A box to hold drinks
* Optional: velcro tape
* Optional: Acrylic panels to cover the sides
* Optional: 3D printer

### Software

To build your own drink-carrying robot, you need the following software:

* [`viam-server`](/installation/#install-viam-server)
* [Python 3.8 or newer](https://www.python.org/downloads/)
* [Viam Python SDK](https://python.viam.dev/).
* [Project repository on GitHub](https://github.com/viam-labs/devrel-demos/)

## Wire your robot

Follow the wiring diagram below to wire together your Raspberry Pi, buck converter, USB camera, motors, motor driver, ultrasonic sensors, and battery:

![Tipsy wiring diagram](../../img/tipsy/wiring-diagram.png)

The Tipsy robot uses an assembled Scuttle rover base with some modifications: Tipsy does not use the camera that came with the Scuttle rover because the cable is not long enough to allow the camera to be attached on top of the robot.
Additionally, Tipsy also does not use the encoders or the batteries that come with the kit.
These changes are reflected in the wiring diagram.

## Configure your components

In the [Viam app](https://app.viam.com), create a new robot and give it a name like `tipsy`.
Follow the instructions on the **Setup** tab to install `viam-server` on your Raspberry Pi and connect to your robot.

{{< tabs >}}
{{% tab name="Builder UI" %}}

Navigate to the **Config** tab of your robot's page in [the Viam app](https://app.viam.com).
Click on the **Components** subtab and navigate to the **Create component** menu.

1. **Configure the Pi as a board**

    Add your {{< glossary_tooltip term_id="board" text="board" >}} with the name `local`, type `board` and model `pi`.
    Click **Create component**.

    ![Create component panel, with the name attribute filled as local, type attribute filled as board and model attribute filled as Pi.](../../img/tipsy/app-board-create.png)

    You can name your board whatever you want as long as you refer to it by the same name in your code.

    ![Board component configured in the Viam app, the component tab is named local, with a type attribute board and model attribute Pi.](../../img/tipsy/app-board-attribute.png)

2. **Configure the motors**

    Add your right [motor](/components/motor/) with the name `rightMotor`, type `motor`, and model `gpio`.

    ![Create component panel, with the name attribute filled as rightMotor, type attribute filled as motor and model attribute filled as gpio.](../../img/tipsy/app-motor-create.png)

    After clicking **Create component**, a panel will pop up with empty sections for Attributes, Component Pin Assignment, and other information.

    ![Alt text: rightMotor component panel with empty sections for Attributes, Component Pin Assignment, and other information.](../../img/tipsy/app-motor-attribute.png)

    In the **Board** drop-down within attributes, choose the name of the board `local` which the motor is wired to.
    This will ensure that the board initializes before the motor when the robot boots up.

    Then set **Max RPM** to 100 and enable direction flip.

    In the **Component Pin Assignment** section, toggle the type to **In1/In2.**
    In the drop downs for A/In1 and B/In2, choose `15 GPIO 22` and `16 GPIO 23` corresponding to the right motor wiring.
    Leave PWM (pulse-width modulation) pin blank, because this specific motor driver’s configuration does not require a separate PWM pin.

    ![Motor component configured in the Viam app, the component tab is named rightMotor, with a type attribute motor and model attribute gpio. It has the attributes as of the board as local, encoder as non-encoded, max rpm as 1000, component pin assignment type as In1/In2, enable pins as neither, a/In1 as 15 GPIO 22, b/In2 as 16 GPIO 23, pwm as blank.](../../img/tipsy/app-motor-pins.png)

    Now let’s add the left motor which is similar to the right motor.
    Add your left [motor](/components/motor/) with the name “leftMotor”, type `motor`, and model `gpio`.
    Select `local` from the **Board** drop-down, set **Max RPM** to `100`, configure the motors pins as A/In1 and B/In2 corresponding to`12 GPIO 18` and `11 GPIO 17` respectively (according to the wiring diagram), and leave PWM blank.

3. **Configure the base**

    Next, add a [base component](/components/base/), which describes the geometry of your chassis and wheels so the software can calculate how to steer the rover in a coordinated way.
    Name your base `tipsy-base`. Select `base` for **Type** and `wheeled` for **Model**.
    In the **Right Motors** drop-down, select `rightMotor` and in the **Left Motors** drop-down select `leftMotor`.
    Enter `250` for **Wheel Circumference (mm)** and `400` for **Width (mm)**.
    The width describes the distance between the midpoints of the wheels.
    Add `local`, `rightMotor`, and `leftMotor` to the **Depends on** field.

    ![tipsy-base component panel filled with attributes right motors as rightMotor, left motors as leftMotor, wheel circumference as 250 and width as 400. It depends on local, rightMotor and leftMotor. ](../../img/tipsy/app-base-attribute.png)

4. **Configure the camera**

    Next, add the [camera component](/components/camera/). Name it `cam`, with the type `camera` and model `webcam`, and click **Create Component**.
    In the configuration panel, click the video path field.
    If your robot is connected to the Viam app, you will see a drop-down populated with available camera names.

    Select the camera you want to use.
    If you are unsure which camera to select, selecte one, save the configuration and go to the **Control** tab to confirm you can see the expected video stream.

    ![cam component panel with type camera and model webcam, and the usb camera selected as the video path.](../../img/tipsy/app-camera-attribute.png)

    Then make it depend on `local` so it initializes after the board component.

5. **Configure the ultrasonic sensors**

    Add a [sensor component](/components/sensor/) with the name `ultrasonic`, type `sensor`, and model `ultrasonic`.
    Then fill in the attributes: enter `38` for `echo_interrupt_pin` and `40` for `trigger_pin`, according to the wiring diagram.
    Enter `local` for `board`.

    ![Ultrasonic component panel with Attributes trigger_pin as 40, echo_interrupt_pin as 38, and board as local.](../../img/tipsy/app-ultrasonic-attribute.png)

    You have to configure the other ultrasonic sensors.
    Tipsy uses 5 in total: two up top underneath the beer box, two on the sides of the robot, and one in the bottom.
    You can change the amount based on your preference.

    For each of the additional ultrasonic sensors, create a new component with the name `ultrasonic2`, type `sensor` and model `ultrasonic`.
    In the attributes textbox, fill in the `trigger_pin` and  `echo_interrupt_pin` corresponding to the pins your ultrasonic sensors are connected to.

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following JSON configuration for your [board](/components/board/), your [motors](/components/motor/), your [base](/components/base/), your [camera](/components/camera/), and your [ultrasonic sensors](/components/sensor/ultrasonic/):

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "model": "pi",
      "name": "local",
      "type": "board",
      "attributes": {
        "i2cs": [
          {
            "bus": "1",
            "name": "default_i2c"
          }
        ]
      },
      "depends_on": []
    },
    {
      "model": "gpio",
      "name": "rightMotor",
      "type": "motor",
      "attributes": {
        "max_rpm": 100,
        "pins": {
          "a": "15",
          "b": "16",
          "pwm": ""
        },
        "board": "local",
        "dir_flip": true
      },
      "depends_on": []
    },
    {
      "attributes": {
        "max_rpm": 100,
        "pins": {
          "pwm": "",
          "a": "12",
          "b": "11"
        },
        "board": "local"
      },
      "depends_on": [],
      "model": "gpio",
      "name": "leftMotor",
      "type": "motor"
    },
    {
      "depends_on": [
        "local",
        "rightMotor",
        "leftMotor"
      ],
      "model": "wheeled",
      "name": "tipsy-base",
      "type": "base",
      "attributes": {
        "wheel_circumference_mm": 250,
        "width_mm": 400,
        "left": [
          "leftMotor"
        ],
        "right": [
          "rightMotor"
        ]
      }
    },
    {
      "depends_on": [
        "local"
      ],
      "name": "cam",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video4"
      }
    },
    {
      "name": "ultrasonic",
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "echo_interrupt_pin": "38",
        "board": "local",
        "trigger_pin": "40"
      },
      "depends_on": [
        "local"
      ]
    },
    {
      "attributes": {
        "board": "local",
        "trigger_pin": "13",
        "echo_interrupt_pin": "7"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic2",
      "type": "sensor",
      "model": "ultrasonic"
    },
    {
      "model": "ultrasonic",
      "attributes": {
        "board": "local",
        "trigger_pin": "35",
        "echo_interrupt_pin": "37"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic3",
      "type": "sensor"
    },
    {
      "attributes": {
        "board": "local",
        "trigger_pin": "28",
        "echo_interrupt_pin": "32"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic4",
      "type": "sensor",
      "model": "ultrasonic"
    },
    {
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": "24",
        "echo_interrupt_pin": "26",
        "board": "local"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic5",
      "type": "sensor"
    },
    {
      "name": "imu",
      "type": "movement_sensor",
      "model": "gyro-mpu6050",
      "attributes": {
        "i2c_bus": "default_i2c",
        "board": "local"
      },
      "depends_on": [
        "local"
      ]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

### Test your components

With the components configured, navigate to the **Control** tab.
On the control tab, you will see panels for each of your configured components.

1. Motors

   Click on both motor panels and check that they run as expected by clicking **RUN**.

   ![Left and right motor panels in the Control tab.](../../img/tipsy/app-control-motors.png)

2. Base

   Click on the base panel and enable the keyboard.
   Then move your rover base around by pressing A, S, W, and D on your keyboard.

   You can also adjust the power level to your preference.

   ![tipsy-base component in the Control tab, with Motor Control buttons to drive it around and change the power percentage.](../../img/tipsy/app-control-motor.png)

3. Camera

   To see your camera working, click on the camera panel and toggle the camera on.

   <img src="../../img/tipsy/app-control-camera.png" alt="cam component panel in the Control tab, cam toggled on and the live stream showing a person." width="300px" class="aligncenter">

4. Ultrasonic Sensors

   Click on your ultrasonic sensors panels and test that you can get readings from all of them.

   Click **Get Readings** to get the distance reading of the sensor.

   ![Ultrasonic component panel in the Control tab, sensor distance reading is 12.0770.](../../img/tipsy/app-control-ultrasonic.png)

## Configure your services

This tutorial uses pre-trained ML packages.
If you want to train your own, you can [train a model](/manage/ml/train-model/).

To use the provided Machine Learning model, copy the <file>[effdet0.tflite](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/effdet0.tflite)</file> file and the <file>[labels.txt](https://github.com/viam-labs/devrel-demos/raw/main/Light%20up%20bot/labels.txt)</file> to your Raspberry Pi:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
scp effdet0.tflite tipsy@tipsy.local:/home/tipsy/effdet0.tflite
scp labels.txt tipsy@tipsy.local:/home/tipsy/labels.txt
```

{{< tabs >}}
{{% tab name="Builder UI" %}}

Click on the **Services** subtab and navigate to the **Create service** menu.

1. **Configure the ML Model Service**

    Add an [mlmodel](/services/ml/) service with the name `people`, type `mlmodel` and model `tflite_cpu`.
    Click **Create service**.

    ![Create service panel, with the type attribute filled as mlmodel, name attribute filled as people, and model attribute filled as tflite_cpu.](../../img/tipsy/app-service-ml-create.png)

    In the new ML Models service panel, configure your service.

    ![mlmodel service panel with empty sections for Model Path, and Optional Settings such as Label Path and Number of threads.](../../img/tipsy/app-service-ml-before.png)

    Select the **Path to Existing Model On Robot** for the **Deployment** field.
    Then specify the absolute **Model Path** as <file>/home/tipsy/effdet0.tflite</file> and any **Optional Settings** such as the absolute **Label Path** as <file>/home/tipsy/labels.txt</file> and the **Number of threads** as 1.

    ![mlmodel service panel, Deployment selected as Path to Existing Model On Robot, Model Path filled as /home/tipsy/effdet0.tflite and Label Path filled as /home/tipsy/labels.txt, Number of threads is 1.](../../img/tipsy/app-service-ml-after.png)

1. **Configure a mlmodel detector**

    Add a [vision service](/services/vision/) with the name `myPeopleDetector`, type `vision` and model `mlmodel`.
    Click **Create service**.

    ![Create service panel, with the type  attribute filled as mlmodel, name attribute filled as people, and model attributed filled as tflite_cpu.](../../img/tipsy/app-service-vision-create.png)

    In the new Vision Service panel, configure your service.

    ![vision service panel called myPeopleDetector with empty Attributes section](../../img/tipsy/app-service-vision-before.png)

    Name the ml model name `people`.

    ![vision service panel called myPeopleDetector with filled Attributes section, mlmodel_name is “people”.](../../img/tipsy/app-service-vision-after.png)

1. **Configure the detection camera**

    To be able to test that the vision service is working, add a `transform` camera which will add bounding boxes and labels around the objects the service detects.

    Click on the **Components** subtab and navigate to the **Create component** menu.
    Create a [transform camera](/components/camera/transform/) with the name `detectionCam`, the type `camera` and the model `transform`.

    ![detectionCam component panel with type camera and model transform, Attributes section has source and pipeline but they are empty.](../../img/tipsy/app-detection-before.png)

    In the new transform camera panel, replace the attributes JSON object with the following object which specifies the camera source that the `transform` camera will be using and defines a pipeline that adds the defined `myPeopleDetector`:

    ```json
    {
    "source": "cam",
    "pipeline": [
        {
        "type": "detections",
        "attributes": {
            "detector_name": "myPeopleDetector",
            "confidence_threshold": 0.5
        }
        }
    ]
    }
    ```

    Click **Save config** in the bottom left corner of the screen.

    Your configuration should now resemble the following:

    ![detectionCam component panel with type camera and model transform, Attributes section filled with source and pipeline information.](../../img/tipsy/app-detection-after.png)

{{% /tab %}}
{{% tab name="Raw JSON" %}}

On the [`Raw JSON` tab](/manage/configuration/#the-config-tab), replace the configuration with the following complete JSON configuration which adds the configuration for the ML model service, the vision service and a transform camera:

```json {class="line-numbers linkable-line-numbers"}
{
  "services": [
    {
      "attributes": {
        "mlmodel_name": "people"
      },
      "model": "mlmodel",
      "name": "myPeopleDetector",
      "type": "vision"
    },
    {
      "type": "mlmodel",
      "model": "tflite_cpu",
      "attributes": {
        "label_path": "/home/tipsy/labels.txt",
        "num_threads": 1,
        "model_path": "/home/tipsy/effdet0.tflite"
      },
      "name": "people"
    }
  ],
  "components": [
    {
      "model": "pi",
      "name": "local",
      "type": "board",
      "attributes": {
        "i2cs": [
          {
            "bus": "1",
            "name": "default_i2c"
          }
        ]
      },
      "depends_on": []
    },
    {
      "model": "gpio",
      "name": "rightMotor",
      "type": "motor",
      "attributes": {
        "max_rpm": 100,
        "pins": {
          "a": "15",
          "b": "16",
          "pwm": ""
        },
        "board": "local",
        "dir_flip": true
      },
      "depends_on": []
    },
    {
      "attributes": {
        "max_rpm": 100,
        "pins": {
          "pwm": "",
          "a": "12",
          "b": "11"
        },
        "board": "local"
      },
      "depends_on": [],
      "model": "gpio",
      "name": "leftMotor",
      "type": "motor"
    },
    {
      "depends_on": [
        "local",
        "rightMotor",
        "leftMotor"
      ],
      "model": "wheeled",
      "name": "tipsy-base",
      "type": "base",
      "attributes": {
        "wheel_circumference_mm": 250,
        "width_mm": 400,
        "left": [
          "leftMotor"
        ],
        "right": [
          "rightMotor"
        ]
      }
    },
    {
      "depends_on": [
        "local"
      ],
      "name": "cam",
      "type": "camera",
      "model": "webcam",
      "attributes": {
        "video_path": "video4"
      }
    },
    {
      "model": "transform",
      "attributes": {
        "pipeline": [
          {
            "type": "detections",
            "attributes": {
              "confidence_threshold": 0.5,
              "detector_name": "myPeopleDetector"
            }
          }
        ],
        "source": "cam"
      },
      "depends_on": [],
      "name": "detectionCam",
      "type": "camera"
    },
    {
      "name": "ultrasonic",
      "type": "sensor",
      "model": "ultrasonic",
      "attributes": {
        "echo_interrupt_pin": "38",
        "board": "local",
        "trigger_pin": "40"
      },
      "depends_on": [
        "local"
      ]
    },
    {
      "attributes": {
        "board": "local",
        "trigger_pin": "13",
        "echo_interrupt_pin": "7"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic2",
      "type": "sensor",
      "model": "ultrasonic"
    },
    {
      "model": "ultrasonic",
      "attributes": {
        "board": "local",
        "trigger_pin": "35",
        "echo_interrupt_pin": "37"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic3",
      "type": "sensor"
    },
    {
      "attributes": {
        "board": "local",
        "trigger_pin": "28",
        "echo_interrupt_pin": "32"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic4",
      "type": "sensor",
      "model": "ultrasonic"
    },
    {
      "model": "ultrasonic",
      "attributes": {
        "trigger_pin": "24",
        "echo_interrupt_pin": "26",
        "board": "local"
      },
      "depends_on": [
        "local"
      ],
      "name": "ultrasonic5",
      "type": "sensor"
    },
    {
      "name": "imu",
      "type": "movement_sensor",
      "model": "gyro-mpu6050",
      "attributes": {
        "i2c_bus": "default_i2c",
        "board": "local"
      },
      "depends_on": [
        "local"
      ]
    }
  ]
}
```

Click **Save config** in the bottom left corner of the screen.

{{% /tab %}}
{{< /tabs >}}

### Test your detection camera

Now you can test if the detections work.
Navigate to the **Control** tab and click on the `detectionCam` panel.
Toggle the camera on to start the video stream.

<img src="../../img/tipsy/app-control-detection-person.png" alt="detectionCam component panel in the Control tab, DetectionCam toggled on and a person is in front of the frame with a red detection box around her saying Person: 0.63" width="350px" class="aligncenter">

You can also see your physical camera stream and detection camera stream together on the base panel.

<img src="../../img/tipsy/app-control-detection-match.png" alt="tipsy-base component panel in the Control tab, with two camera streams on the right showing the same person, the bottom with a red detection box around her saying Person: 0.72." width="550px" class="aligncenter">

At this point, it is a simple detection camera: it will detect any object in the `label.txt` file.
When we write the code for the robot, we can differentiate between, say, a person or a chair.

<img src="../../img/tipsy/app-control-detection-chair.png" alt="tipsy-base component panel in the Control tab, with two camera streams on the right showing the same char, the bottom with a red detection box around the chair saying 0.50. Cam and DetectionCam toggled on." width="550px" class="aligncenter">

## Design your robot

<img src="../../img/tipsy/assembly-frame.jpg" alt="four T-slotted framing rails connected to the Scuttle base with brackets for height, and two T-slotted framing rails connected to underneath the box with brackets for holding the drinks." width="350px" class="alignleft">

Now that you have all your components wired, configured, and tested, you can assemble your robot.

Add four 3’ long T-slotted framing rails along the corners of the Scuttle rover base to make it a tall structure.
Then add two 12 inches long T-slotted framing rails in the middle of the structure at the height that you want to hold the box at.
Secure them using T-slotted framing structural brackets.

Next, add the wired Raspberry Pi, motor driver, and 12V battery to the base.

You can use the 3D-printed holders that come with the assembled Scuttle base for the Raspberry Pi and the motor driver.
You can also print holders based on Scullte degins from [grabcad](https://grabcad.com/library?page=1&time=all_time&sort=recent&query=scuttle).

Secure the 12V battery to the bottom using velcro tape or other tape, and secure the sides using T-slotted brackets.

<img src="../../img/tipsy/assembly-rails-velcro.jpg" alt="velcro tape on T-slotted rails secured from the sides." width="400px" class="aligncenter">

Secure the buck converter with velcro tape, double sided tape, or a 3D printed holder.

<img src="../../img/tipsy/assembly-driver.jpg" alt="motor driver secured to the robot base with 3D printed attachment and wired to the Raspberry Pi." width="400px" class="aligncenter">

Use velcro or something else to secure the USB camera to the box that holds the drinks so it faces the front, towards any people who may interact with the robot.

For ultrasonic sensors to fit the framing, we recommend 3D printing enclosures.
This step is optional but makes the project look more aesthetically pleasing and ensures that the sensors don’t fall out as your robot moves around.

You can design your own enclosure, or you can use our design:

![3D printed enclosure of the ultrasonic sensor.](../../img/tipsy/assembly-sensor-3dmodel.jpg)

The STL files we used can be found in our [project repository](https://github.com/viam-labs/devrel-demos/tree/main/tipsy-bot/stl-files).

Scuttle also has a design for a 3D printed enclosure with a twist bracket that fits the rails.

If you decide not to use a 3D printer, you can tape the ultrasonic sensors to the rails.
We recommend that you do so within the enclosure, perhaps under the drink box and above the rover base, so they don’t touch people or obstacles as the robot moves around, as this could cause them to fall off or get damaged.

<img src="../../img/tipsy/assembly-ultrasonic-sensor.jpg" alt="A finger pointing to the placement of where the ultrasonic sensor would live within the rover base." style="height:450px" class="aligncenter">
<img src="../../img/tipsy/assembly-sensor.jpg" alt="Installation of the 3D printed enclosure of the ultrasonic sensor on the frame." style="height:450px" class="aligncenter">

{{< alert title="Info" color="info" >}}
The photo of the sensor being installed shows two batteries, but you will only use one for this tutorial.
{{< /alert >}}

Now we are ready to make Tipsy look pretty!
Optionally, add acrylic side panels and cover the electronics.

<img src="../../img/tipsy/assembly-complete.jpg" alt="Tipsy with black acrylic sides." width="400px" class="aligncenter">

We drilled and screwed the panels onto the railing.
You can also use a laser cutter to cut them into the sizes you prefer, if you want different side panels.

## Add the robot logic

Download the [full code](https://raw.githubusercontent.com/viam-labs/devrel-demos/main/tipsy-bot/tipsy.py) onto your computer.

Let’s take a look at what it does.
First, the code imports the required libraries:

```python {class="line-numbers linkable-line-numbers"}
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor
from viam.components.base import Base
from viam.services.vision import VisionClient
```

Then it connects to our robot using a robot location secret and address.
Replace these values with your robot’s own location secret and address which you can obtain from the **Code sample** tab, when you enable **Include secret**.

```python {class="line-numbers linkable-line-numbers"}
robot_secret = os.getenv('ROBOT_SECRET') or ''
robot_address = os.getenv('ROBOT_ADDRESS') or ''
#change this if you named your base differently in your robot configuration
base_name = os.getenv('ROBOT_BASE') or 'tipsy-base'
#change this if you named your camera differently in your robot configuration
camera_name = os.getenv('ROBOT_CAMERA') or 'cam'
pause_interval = os.getenv('PAUSE_INTERVAL') or 3
```

Next, the code defines functions for obstacle detection.
The first method, `obstacle_detect()`, gets readings from a sensor, and the second method, `obstacle_detect_loop()`, asynchronously loops through the readings to stop the base if it’s closer than a certain distance from an obstacle:

```python {class="line-numbers linkable-line-numbers"}
async def obstacle_detect(sensor):
   reading = (await sensor.get_readings())["distance"]
   return reading

async def obstacle_detect_loop(sensor, sensor2, base):
   while(True):
       reading = await obstacle_detect(sensor)
       reading2 = await obstacle_detect(sensor2)
       if reading < 0.4 or reading2 <0.4:
           # stop the base if moving straight
           if base_state == "straight":
               await base.stop()
               print("obstacle in front")
       await asyncio.sleep(.01)
```

Then, we define a person detection loop, where the robot is constantly looking for a person, and if it finds the person, it goes towards them as long as there are no obstacles in front.
If it doesn’t find a person, it will continue looking by rotating the robot base 45 degrees at a time and looking again.

Lines 12 and 13 are where it checks specifically for detections with the label `Person` and not every object in the `labels.txt` file:

```python {class="line-numbers linkable-line-numbers" data-line="12-13"}
async def person_detect(detector, sensor, sensor2, base):
   while(True):
       # look for person
       found = False
       global base_state
       print("will detect")
       detections = await detector.get_detections_from_camera(camera_name)
       for d in detections:
           if d.confidence > .7:
               print(d.class_name)
              #specify it is just the person we want to detect
               if (d.class_name == "Person"):
                   found = True
       if (found):
           print("I see a person")
           # first manually call obstacle_detect - don't even start moving if someone in the way
           distance = await obstacle_detect(sensor)
           distance2 = await obstacle_detect(sensor2)
           if (distance > .4 or distance2 > .4):
               print("will move straight")
               base_state = "straight"
               await base.move_straight(distance=800, velocity=250)
               base_state = "stopped"
       else:
           print("I will turn and look for a person")
           base_state = "spinning"
           await base.spin(45, 45)
           base_state = "stopped"

       await asyncio.sleep(pause_interval)
```

Finally, the `main()` function initializes the base, the sensors, and the detector.
It also creates two background tasks running asynchronously, one looking for obstacles and avoiding them (`obstacle_task`), and one looking for people and moving towards them (`person_task`):

```python {class="line-numbers linkable-line-numbers"}
async def main():
   robot = await connect()
   base = Base.from_robot(robot, base_name)
   sensor = Sensor.from_robot(robot, "ultrasonic")
   sensor2 = Sensor.from_robot(robot, "ultrasonic2")
   detector = VisionServiceClient.from_robot(robot, "myPeopleDetector")

   # create a background task that looks for obstacles and stops the base if its moving
   obstacle_task = asyncio.create_task(obstacle_detect_loop(sensor, sensor2, base))
   # create a background task that looks for a person and moves towards them, or turns and keeps looking
   person_task = asyncio.create_task(person_detect(detector, sensor, sensor2, base))
   results= await asyncio.gather(obstacle_task, person_task, return_exceptions=True)
   print(results)
```

When you run the code, you should see results like this:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
will detect
Person
I see a person
will move straight
obstacle in front
will detect
Person
I see a person
will move straight
obstacle in front
will detect
I will turn and look for a person
will detect
I will turn and look for a person
will detect
Person
I see a person
```

## Summary

<img src="../../img/tipsy/tipsy-at-party.jpg" alt="Tipsy at a party." width="400px" class="alignright">

In this tutorial, you learned how to make your own drink-carrying robot.
You no longer have to interrupt your conversations or activities just to grab another drink.
Overall, Tipsy is the ultimate drink buddy for any social event.
With its people detection and obstacle avoidance technology, convenient autonomous operation, and modern design, it's sure to impress all your guests.

To make Tipsy even more advanced, you can try to:

* Add more ultrasonic sensors so it doesn’t hit objects at different heights, you can also attach them to a moving gantry along the side rails
* Add a depth camera to detect obstacles and how close they are to Tipsy
* Add an imu to see if Tipsy is tipping backwards
* Add a lidar

You can also design another robot for collecting the empty beer cans, or a bartender robot with pumps that can mix you some drinks.
Till then, sit back, relax, and let Tipsy handle the beer carrying duties for you!

For more robotics projects, check out our [other tutorials](/tutorials/).
