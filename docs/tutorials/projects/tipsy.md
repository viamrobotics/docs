---
title: "Tipsy: Create an Autonomous Beer Carrying Robot"
linkTitle: "Build a Beer Serving Robot"
weight: 60
type: "docs"
tags: ["raspberry pi", "app", "board", "motor", "camera"]
description: "Tipsy: Create an autonomous beer carrying robot with motion sensing and machine learning."
image: "/tutorials/img/tipsy/preview.jpg"
images: ["/tutorials/img/tipsy/preview.jpg"]
imageAlt: "Tipsy robot carrying beers"
# Author: Hazal
---

Are you tired of constantly making trips to the fridge during a party just to replenish everyone's drinks?
Are your guests tired of going to grab their own drinks?
Well, now everyone can sit back and relax while Tipsy takes care of all your beer carrying needs.

Designed with ultrasonic sensors and cameras, Tipsy is equipped to detect the presence of obstacles and people in its surrounding area.
While avoiding the obstacles with the ultrasonic sensor distance measurements, it identifies the people using a ML model and object detection and moves towards them with ease.
Once it reaches the person, Tipsy allows people to grab a beer without ever having to leave their spot, since a bucket of ice cold beers are within arm's reach.

![Tipsy robot carrying beers](/tutorials/img/tipsy/preview.jpg)

## Requirements

### Hardware

You will require the following hardware:

* [Raspberry Pi](https://a.co/d/bxEdcAT), with [microSD card](https://www.amazon.com/Lexar-Micro-microSDHC-Memory-Adapter/dp/B08XQ7NGG1/ref=sr_1_13?crid=2MYQRKA7TX2KM&keywords=microsd%2Bcard%2Bwith%2Badaptor&qid=1682364645&sprefix=microsd%2Bcard%2Bwith%2Badaptor%2Caps%2C79&sr=8-13&th=1), setup following our [Raspberry Pi Setup Guide](/installation/prepare/rpi-setup/).
* A macOS or Linux computer
* Assembled [Scuttle rover](https://www.scuttlerobot.org/product/scuttle-v3). We are using the motors and motor driver that came with it.
* [T-slotted framing](https://www.mcmaster.com/products/structural-framing/t-slotted-framing-rails-4/system-of-measurement~metric/rail-height~30mm/): single 4 slot rail, 30 mm square, hollow, 3’ long, 4 of them.
These are for the height of the robot.
* [T-slotted framing](https://www.mcmaster.com/products/structural-framing/t-slotted-framing-rails-4/system-of-measurement~metric/rail-height~30mm/): single 4 slot rail, 30 mm square, hollow, 12 inches long, 2 of them.
These are for the inside of the robot, holding the drink box securely on top by creating a base underneath it.
* [T-slotted framing structural brackets](https://www.amazon.com/Aluminum-Connector-Extrusion-Profiles-Accessories/dp/B08NC46L9K/ref=sr_1_14?crid=2JIU8AVOQKM7W&keywords=3030+structural+framing&qid=1681152812&sprefix=3030+structural+framing%2Caps%2C67&sr=8-14): 30mm rail height.
* Two [ultrasonic sensors](https://www.amazon.com/WWZMDiB-HC-SR04-Ultrasonic-Distance-Measuring/dp/B0B1MJJLJP/ref=sr_1_4?crid=2OY2AFEUQMTSP&keywords=ultrasonic+sensor&qid=1682443408&sprefix=ultrasonic+sensor%2Caps%2C88&sr=8-4)
* A [12V battery](https://www.amazon.com/ExpertPower-EXP1270-Rechargeable-Lead-Battery/dp/B003S1RQ2S/ref=sr_1_4?crid=FGUVJZV13VF7&keywords=expert+power+12v+battery&qid=1682365772&sprefix=expert+power+%2Caps%2C122&sr=8-4) with [charger](https://www.amazon.com/dp/B0BC3Y5N3Q/ref=vp_d_pd_b2b_qd_vp_pd?_encoding=UTF8&pf_rd_p=18ac4947-fc02-409d-a460-4117e58667a4&pf_rd_r=GG6532H6SF32SEC3EZKA&pd_rd_wg=6Boz9&pd_rd_i=B0BC3Y5N3Q&pd_rd_w=u2uS7&content-id=amzn1.sym.18ac4947-fc02-409d-a460-4117e58667a4&pd_rd_r=3bf79f54-e36d-4bcc-967c-2acae5e7e98d)
* Dc-Dc converter, 12v in, 5v out
* USB camera
* A box to hold the drinks
* Optional: velcro tape
* Optional: Acrylic panels to cover the sides
* Optional: 3D printer

### Software

You will require the following software:

* `viam-server` installed following our [Installation Guide](/installation/#install-viam-server)
* [Python 3.8 or newer](https://www.python.org/downloads/)
* [Viam Python SDK](https://python.viam.dev/)
  * The Viam Python SDK (software development kit) lets you control your Viam-powered robot by writing custom scripts in the Python programming language.
  Install the Viam Python SDK by following [these instructions](https://python.viam.dev/).
* [Project repo on GitHub](https://github.com/viam-labs/devrel-demos/)

## Wire your robot

Following the wiring diagram, wire your Raspberry Pi, buck converter, USB camera, motors, motor driver, ultrasonic sensors, and battery.

We are using an assembled Scuttle rover base, but with some modifications.
We are not using the camera that came with it because the cable was not long enough to allow the camera to be attached on top of the robot.
We are also not using the encoders or the batteries that came with the kit.
You will see these changes reflected in the wiring diagram.

{{< alert title="Info" color="info" >}}
Wiring diagram forthcoming.
{{< /alert >}}

## Configure your robot on the Viam app

In [the Viam app](https://app.viam.com), create a new robot and give it a name.
We named ours Tipsy.

![A robot page header in the Viam app, its under the location DevRel Demos, and named tipsy.](/tutorials/img/tipsy/app-name-tipsy.png)

Then navigate to the robot’s **CONFIG** tab to start configuring your components.

### Configure the Pi as a board

Add your {{< glossary_tooltip term_id="board" text="board" >}} with the name `local`, type `board` and model `pi`.
Click **Create component**.

![Create component panel, with the name attribute filled as local, type attribute filled as board and model attribute filled as Pi.](/tutorials/img/tipsy/app-board-create.png)

You can name your board whatever you want as long as you refer to it by the same name in your code.

![Board component configured in the Viam app, the component tab is named local, with a type attribute board and model attribute Pi.](/tutorials/img/tipsy/app-board-attribute.png)

### Configure the motors

Add your right [motor](/components/motor/) with the name `rightMotor`, type `motor`, and model `gpio`.

![Create component panel, with the name attribute filled as rightMotor, type attribute filled as motor and model attribute filled as gpio.](/tutorials/img/tipsy/app-motor-create.png)

After clicking **Create component**, a panel will pop up with empty sections for Attributes, Component Pin Assignment, and other information.

![Alt text: rightMotor component panel with empty sections for Attributes, Component Pin Assignment, and other information.](/tutorials/img/tipsy/app-motor-attribute.png)

In the **Board** drop-down within attributes, choose the name of the board `local` which the motor is wired to.
This will ensure that the board initializes before the motor when the robot boots up.

Then set **Max RPM** to 100 and enable direction flip.

In the **Component Pin Assignment** section, toggle the type to **In1/In2.**
In the drop downs for A/In1 and B/In2, choose `15 GPIO 22` and `16 GPIO 23` corresponding to the right motor wiring.
Leave PWM (pulse-width modulation) pin blank, because this specific motor driver’s configuration does not require a separate PWM pin.

![Motor component configured in the Viam app, the component tab is named rightMotor, with a type attribute motor and model attribute gpio. It has the attributes as of the board as local, encoder as non-encoded, max rpm as 1000, component pin assignment type as In1/In2, enable pins as neither, a/In1 as 15 GPIO 22, b/In2 as 16 GPIO 23, pwm as blank.](/tutorials/img/tipsy/app-motor-pins.png)

Now let’s add the left motor which is pretty similar to the right motor.
Add your left [motor](/components/motor/) with the name “leftMotor”, type `motor`, and model `gpio`.
Select `local` from the **Board** drop-down, set **Max RPM** to `100`, configure the motors pins as A/In1 and B/In2 corresponding to`12 GPIO 18` and `11 GPIO 17` respectively (according to the wiring diagram), and leave PWM blank.

If you navigate to the **Control** tab, you will see your motors and separately control them.

![Left and right motor panels in the Control tab.](/tutorials/img/tipsy/app-control-motors.png)

### Configure the base

It’s time to configure a [base component](/components/base/), which describes the geometry of your chassis and wheels so that the software can calculate how to steer the rover in a coordinated way.
From the **Config** tab, give your base a name, we named ours `tipsy-base`. Enter `base` for **Type** and `wheeled` for **Model**.
In the **Right Motors** drop-down select `rightMotor` and **Left Motors** drop-down select `leftMotor`.
Enter `250` for **Wheel Circumference (mm)** and `400` for **Width (mm)** (which is measured between the midpoints of the wheels).
Add `local`, `rightMotor`, and `leftMotor` to the **Depends on** field.

![tipsy-base component panel filled with attributes right motors as rightMotor, left motors as leftMotor, wheel circumference as 250 and width as 400. It depends on local, rightMotor and leftMotor. ](/tutorials/img/tipsy/app-base-attribute.png)

Save your configuration.
Now you can move around your base in the control panel.

![tipsy-base component in the Control tab, with Motor Control buttons to drive it around and change the power percentage.](/tutorials/img/tipsy/app-control-motor.png)

When you enable keyboard, you will be able to move your rover base around by pressing A, S, W, and D on your keyboard.
You can also adjust the power level to your preference.

### Configure the camera

Now to configure the camera component. Name it `cam`, with the type `camera` and model `webcam`, and click **Create Component**.
Now, you’ll see the configuration panel for the camera component.

Click the video path field to reveal a drop-down populated with camera paths that have been identified on your machine.

Select the path to the camera you want to use.
Often on Linux systems, this is `video14`, `video15` or a USB path. On macOS, this is often a long string of letters and numbers.

![cam component panel with type camera and model webcam, video path selecting the usb path.](/tutorials/img/tipsy/app-camera-attribute.png)

Then make it depends on local so it initializes after the board component, and click **Save config**.

Now navigate to the control tab where you can see your camera working.

![cam component panel in the Control tab, cam toggled on and the live stream showing a person.](/tutorials/img/tipsy/app-control-camera.png)

### Configure the detection camera

Configure a [transform camera](/components/camera/transform) to view output from the detector overlaid on images from the physical camera.

Name it `detectionCam`, with the type `camera` and model `transform`, and click **Create component**.
You’ll see the panel for the detection camera component with empty attributes.

![detectionCam component panel with type camera and model transform, Attributes section has source and pipeline but they are empty.](/tutorials/img/tipsy/app-detection-before.png)

Delete the content of the **Attributes** section and copy the attributes below into it:

```js
{
 "source": "cam",
 "pipeline": [
   {
     "attributes": {
       "confidence_threshold": 0.5,
       "detector_name": "myPeopleDetector"
     },
     "type": "detections"
   }
 ]
}
```

Your configuration should now resemble the following:

![detectionCam component panel with type camera and model transform, Attributes section filled with source and pipeline information.](/tutorials/img/tipsy/app-detection-after.png)

Here you are adding the source camera, which is your actual camera component that will get transformed.
You are also adding a detector with the name `myPeopleDetector`.
Since we haven't yet configured the Vision Service, or created our ML Model, this detector won’t work.
Let’s add them.

### Download and move label.txt and effdet0.tflite packages

Download `label.txt` and the `tflite` package from the project repository. We are using pre-trained ML packages; if you want to train yours, you can [train a model](/manage/ml/train-model).

Then add your `label.txt` and `tflite` package into your robot by copying from your local computer where you saved it, and pasting it to your board.
You will later reference this in your ML Model Service.

![moving effdet0.tflite and labels.txt files from Macbook Pro Downloads folder to tipsy local home folder.](/tutorials/img/tipsy/copy-training-files.png)

Then, go to the [the Viam app](https://app.viam.com) and navigate to **Services** subtab under the **Config** tab.

### Configure the ML Model Service

Add your [mlmodel](/services/ml/) with the name `people`, type `mlmodel` and model `tflite_cpu`.
Click **Create service**.

![Create service panel, with the type attribute filled as mlmodel, name attribute filled as people, and model attribute filled as tflite_cpu.](/tutorials/img/tipsy/app-service-ml-create.png)

This will create the empty panel for ml model you just created.

![mlmodel service panel with empty sections for Model Path, and Optional Settings such as Label Path and Number of threads.](/tutorials/img/tipsy/app-service-ml-before.png)

To configure your service with an existing model on the robot, select **Path to Existing Model On Robot** for the **Deployment** field.
Then specify the absolute **Model Path** and any **Optional Settings** such as the absolute **Label Path** and the **Number of threads**.
This will correspond to where you added your effdet0.tflite and the label.txt files, which is in the board on Tipsy.

![mlmodel service panel, Deployment selected as Path to Existing Model On Robot, Model Path filled as /home/tipsy/effdet0.tflite and Label Path filled as /home/tipsy/labels.txt, Number of threads is 1.](/tutorials/img/tipsy/app-service-ml-after.png)

### Configure the Vision Service and a mlmodel detector

Add your vision service with the name `myPeopleDetector`, type `vision` and model `mlmodel`.
Click **Create service**.

![Create service panel, with the type  attribute filled as mlmodel, name attribute filled as people, and model attributed filled as tflite_cpu.](/tutorials/img/tipsy/app-service-vision-create.png)

This will create the empty panel for service you just created.

![vision service panel called myPeopleDetector with empty Attributes section](/tutorials/img/tipsy/app-service-vision-before.png)

Here we have to add the ml model name. Since we are detecting people with the intention to move towards them, let’s name this `people`.

![vision service panel called myPeopleDetector with filled Attributes section, mlmodel_name is “people”.](/tutorials/img/tipsy/app-service-vision-after.png)

Now you can test if the detections work from the **Control** tab.
If you go to the `detectionCam` panel, since you configured the necessary services, the camera should start streaming the detections.

![detectionCam component panel in the Control tab, DetectionCam toggled on and a person is in front of the frame with a red detection box around her saying Person: 0.63](/tutorials/img/tipsy/app-control-detection-person.png)

You will also be able to see your physical camera stream and detection camera stream together on the base panel.

![tipsy-base component panel in the Control tab, with two camera streams on the right showing the same person, the bottom with a red detection box around her saying Person: 0.72.](/tutorials/img/tipsy/app-control-detection-match.png)

At this point, it is a simple detection camera: it will detect any object in the `label.txt` file.
We did not differentiate between, say, a person or a chair yet.
We will do that in the Python coding section after configuring the ultrasonic sensors.

![tipsy-base component panel in the Control tab, with two camera streams on the right showing the same char, the bottom with a red detection box around the chair saying 0.50. Cam and DetectionCam toggled on.](/tutorials/img/tipsy/app-control-detection-chair.png)

### Configure the ultrasonic sensors

Click back to the **Components** section under the **Config** tab, and create a new component with the name `ultrasonic`, type `sensor`, and model `ultrasonic`.
Then fill in the attributes: enter `38` for `echo_interrupt_pin` and `40` for `trigger_pin`, according to the wiring diagram.
Enter `local` for `board`.

![Ultrasonic component panel with Attributes trigger_pin as 40, echo_interrupt_pin as 38, and board as local.](/tutorials/img/tipsy/app-ultrasonic-attribute.png)

If you navigate to **Control** tab, you can test your ultrasonic sensor.
If you click **Get Readings**, you will get the distance reading of the sensor.

![Ultrasonic component panel in the Control tab, sensor distance reading is 12.0770.](/tutorials/img/tipsy/app-control-ultrasonic.png)

Now it’s time to configure the other ultrasonic sensors.
We used 5 in total: two up top underneath the beer box, two on the sides of the robot, and one in the bottom.
You can change the amount based on your preference.  

Create a new component with the name name `ultrasonic2`, type `sensor` and model `ultrasonic`.
In the attributes textbox, add `trigger_pin` as `13` and  `echo_interrupt_pin` as `7`, corresponding to the wiring diagram.

When you go to the **Control** tab, you can see both of the ultrasonic sensors and get readings from them.
It is recommended to test them both before you start the hardware section.

## Design your robot

Now that we have all our components wired, configured, and tested, we can assemble the robot.

Add four 3’ long T-slotted framing rails along the corners of the Scuttle rover base, making it a tall structure.
Then add two 12 inches long T-slotted framing rails in the middle of the structure at a height that you want to hold the box at.
Secure them using T-slotted framing structural brackets.

![four T-slotted framing rails connected to the Scuttle base with brackets for height, and two T-slotted framing rails connected to underneath the box with brackets for holding the drinks.](/tutorials/img/tipsy/assembly-frame.jpg)

Now add the wired Raspberry Pi, motor driver, and 12V battery and to the base.

We are using the 3D-printed holders that came with the Scuttle base for the Raspberry Pi and the motor driver.
These came with the assembled Scuttle rover, but you can print more Scuttle tagged designs from [here](https://grabcad.com/library?page=1&time=all_time&sort=recent&query=scuttle) since it's very extensible.

We secured the 12V battery to the bottom using velcro tape, and secured from the sides using T-slotted brackets.

![velcro tape on T-slotted rails secured from the sides.](/tutorials/img/tipsy/assembly-rails-velcro.jpg)

We used velcro tape for the buck converter too.
This is optional and you can secure them as you prefer.
Double sided tape would work just fine, or you can 3D print special holders for them.

![motor driver secured to the robot base with 3D printed attachment and wired to the Raspberry Pi.](/tutorials/img/tipsy/assembly-driver.jpg)

We also used velcro tape to secure the USB camera to the box that holds the drinks so it faces the front, towards any people who may interact with the robot.

For ultrasonic sensors to fit the framing, we 3D printed enclosures for them.
This step is optional but makes the project look more aesthetically pleasing and makes sure that the sensors don’t fall out (as they potentially could if they were loosely taped to the side of the framing) as your robot moves around.

Scuttle has a design for a 3D printed enclosure with a twist bracket that fits the rails.
If you have access to a 3D printer, you can print them here.

{{< alert title="Info" color="info" >}}
STL links forthcoming
{{< /alert >}}

If you decide not to use a 3D printer, you can tape the ultrasonic sensors to the rails.
If you do so, we recommend that you do so within the enclosure, perhaps under the drink box and above the rover base, so they don’t touch people or obstacles as the robot moves around, and potentially fall off or become damaged.

![A finger pointing to the placement of where the ultrasonic sensor would live within the rover base.](/tutorials/img/tipsy/assembly-ultrasonic-sensor.jpg)

![3D printed enclosure of the ultrasonic sensor.](/tutorials/img/tipsy/assembly-sensor-3dmodel.jpg)

![Installation of the 3D printed enclosure of the ultrasonic sensor on the frame.](/tutorials/img/tipsy/assembly-sensor.jpg)

{{< alert title="Info" color="info" >}}
The photo of the sensor being installed shows two batteries, but you will only use one.
{{< /alert >}}

Now we are ready to make it look pretty!
You can add acrylic side panels and cover the electronics so Tipsy can look clean!

![Tipsy with black acrylic sides.](/tutorials/img/tipsy/assembly-complete.jpg)

We drilled and screwed the panels on to the railing.
You can also use a laser cutter to cut them into sizes you prefer, if you want different side panels.

## Write some code

Download the full code from the project repository and let’s take a deep dive into it.

{{< alert title="Info" color="info" >}}
Repository link forthcoming
{{< /alert >}}

First, we are importing necessary libraries:

```python
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor
from viam.components.base import Base
from viam.services.vision import VisionClient
```

Then we are connecting to our robot using our robot secret and address.
This allows us to connect to our specific robot.
Replace these values with your robot’s own secret and address.

Next, the code is defining functions for obstacle detection.
The first method, `obstacle_detect()`, gets readings from the sensor, and the second method, `obstacle_detect_loop()`, asynchronously loops the readings to stop the base if it’s closer than a certain distance from an obstacle:

```python
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

Then, we define a person detection loop, where the robot is constantly looking for a person using camera detection, and if it finds the person, it goes towards them as long as there are no obstacles in front.
If it doesn’t find a person, it will continue looking by rotating the robot base 45 degrees each time and looking again.

This is where we tell our detector to only look for people and not every object in the `labels.txt` file:

```python
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

Finally, the `main()` function defines all the ultrasonic sensors, and the detector. It also creates two background tasks running asynchronously, one looking for obstacles and avoiding them (`obstacle_task`), and one looking for people and moving towards them (`person_task`):

```python
async def main():
   robot = await connect()
   base = Base.from_robot(robot, base_name)
   sensor = Sensor.from_robot(robot, "ultrasonic")
   sensor2= Sensor.from_robot(robot, "ultrasonic2")
   detector = VisionServiceClient.from_robot(robot, "myPeopleDetector")

   # create a background task that looks for obstacles and stops the base if its moving
   obstacle_task = asyncio.create_task(obstacle_detect_loop(sensor, sensor2, base))
   # create a background task that looks for a person and moves towards them, or turns and keeps looking
   person_task = asyncio.create_task(person_detect(detector, sensor, sensor2, base))
   results= await asyncio.gather(obstacle_task, person_task, return_exceptions=True)
   print(results)
```

When you run the code, you should see results like this:

![Terminal window showing results of running python code, including indications of each person or obstacle encountered.](/tutorials/img/tipsy/run-code-results.png)

```none
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

{{< alert title="Info" color="info" >}}
Delete one of the above.
{{< /alert >}}

## Summary

In this tutorial, you learned how to make your own drink-carrying robot.
You no longer have to interrupt your conversations or activities just to grab another drink.
Overall, Tipsy is the ultimate beer buddy for any social event.
With its people detection and obstacle avoidance technology, convenient autonomous operation, and modern design, it's sure to impress all your guests.

![Tipsy at a party.](/tutorials/img/tipsy/tipsy-at-party.jpg)

To make Tipsy even more advanced, you can try to:

* Add more ultrasonic sensors so it doesn’t hit objects at different heights, you can also have them on a moving gantry all along the side rails
* Add a depth camera to detect obstacles and how close they are to Tipsy
* Add an imu to see if Tipsy is tipping backwards
* Add a lidar

You can also design another robot that is for collecting the empty beer cans, or a bartender robot with pumps that can mix you some drinks.
Till then, sit back, relax, and let Tipsy handle the beer carrying duties for you!

For more robotics projects, check out our [other tutorials](/tutorials/).

If you want to connect with other developers learning how to build robots, or if you have any issues whatsoever getting Viam set up, let us know on our [Discord Server](https://discord.gg/viam), and we will be happy to help you get up and running.
