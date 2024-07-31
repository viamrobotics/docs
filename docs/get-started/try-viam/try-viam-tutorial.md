---
title: "Control A Rented Viam Rover"
linkTitle: "Control A Rented Viam Rover"
weight: 39
type: "docs"
description: "Remotely control a Viam Rover located on-site at Viam in New York."
images: ["/get-started/try-viam/rover-resources/viam-rover/rover-front.jpg"]
imageAlt: "The front of the assembled Viam Rover"
tags: ["try viam", "app"]
no_list: true
aliases:
  - "/try-viam/try-viam-tutorial/"
---

_Try Viam_ is a way to try out the Viam platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab to play around!

The rental rover is made up of a chassis with a Raspberry Pi 4B single-board computer, two motors, encoders, and a camera.
The Try Viam area also has an overhead camera to provide a view of the rental rover, allowing you to view its movements in real time.

Watch this tutorial video for a walkthrough of Try Viam, including [how to reserve a Viam Rover](/get-started/try-viam/reserve-a-rover/#using-the-reservation-system), [navigate the Viam platform](/fleet/), and [drive the rover](#control-tab):

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/YYpZ9CVDwMU">}}

## **CONTROL** tab

Click on the rover name at the top to go to the rental rover's **CONTROL** tab where you can drive the machine and interact with each of the machine's components.

At the top of the page you can see the randomly assigned name of the rover, the host, and the IP address.

![The top banner of a Try Viam rover machine page. The randomly generated name for this rover is 'silent-forest'](get-started/try-viam/try-viam/bannerinfo.png)

The **CONTROL** tab contains panels for each of the rover's components:

- the base,
- the left and right motors,
- the web game pad,
- the board, and
- two cameras.

The order of these components may vary.

{{<imgproc src="/get-started/try-viam/try-viam/control-panel-list.png" resize="700x" declaredimensions=true alt="The component panels on the CONTROL tab of the Try Viam rover. None of them are expanded yet so they display as thin rectangles with component names and types shown.">}}

### Base control

The [base component](/components/base/) is the platform that the other parts of a mobile machine attach to.

Click the `viam_base` component to expand the base control pane to reveal the camera feed and driving interfaces.

![The viam_base component panel on the CONTROL tab. The Keyboard Disabled toggle is grey and not yet enabled.](get-started/try-viam/try-viam/initial-base-control.png)

#### Camera views

In the `viam_base` component panel, select the `cam` for the front-facing camera and the `overhead-cam:overheadcam` for an overhead view of your rover.
We recommend enabling both cameras so you can have a better sense of what's happening in the space.

![The viam_base component panel showing both the 'cam' and 'overheadcam' camera feeds enabled.](get-started/try-viam/try-viam/enable-both-cameras.png)

You can also view and control the camera streams from the [individual camera components](/get-started/try-viam/try-viam-tutorial/#camera-control).

#### Movement control

To move your rover, click on **viam_base**.
You can use the **W**, **A**, **S**, and **D** buttons to move forward, turn left, move backwards, and turn right.

If you enable the keyboard toggle, you can also control the rover's movement with the **W**, **A**, **S**, and **D** keys and the arrow keys on your keyboard.

{{% alert title="Tip" color="tip" %}}

Each time you show or hide a camera, **Keyboard Enabled** automatically toggles to **Keyboard Disabled**.

If you change your camera configurations, you must re-enable your keyboard control to control your rover again.
This behavior is for safety purposes.

{{% /alert %}}

##### Discrete movement control

If you go from the from **Keyboard** to the **Discrete** tab, you can choose between:

- Different movement modes: `Straight` or `Spin`
- Different movement types: `Continuous` or `Discrete`

  In _continuous_ movement mode you can set a speed at which the rover will move indefinitely in the specified direction.
  In _discrete_ movement mode you can set a speed at which to move and a distance to cover before stopping.

- Directions: `Forwards` and `Backwards`.

![The DISCRETE tab of the viam_base component panel. Movement mode, movement type, and direction mode toggles are shown as well as a speed (mm/sec) field and a distance field (the latter of which is greyed out because the movement type toggle is set to continuous instead of discrete movement).](get-started/try-viam/try-viam/discrete.png)

### Camera control

While you can view the camera streams [from the base component panel](#camera-views), you can access more features on each individual [camera component](/components/camera/) panel. In these panels, you can:

- Set the refresh frequency
- Export screenshots
- View point cloud data (for machines with depth cameras)

**cam Stream**:

![The front-facing camera panel (for the component named 'cam').](get-started/try-viam/try-viam/cam-panel.png)

**overhead-cam:overheadcam Stream**:

![The overhead camera panel (for the component named 'overhead-cam').](get-started/try-viam/try-viam/overhead-cam-panel.png)

### Motor control

The [motor components](/components/motor/) enable you to move the base.
The motors are named `left` and `right`, corresponding to their location on the rover base.
Their initial state is **Idle**.
You can click on each motor panel and make the motor **RUN** or **STOP**.

![The left and right motor panels on the CONTROL tab.](get-started/try-viam/try-viam/left-right-panels.png)

Run each motor at a different power level to go faster or slower, and toggle rotation directions to go forwards or backwards.
You can also see their current positions (based on encoder readings) in real time:

![The left motor running at 20% power and forwards and right motor running at 80% power and backwards.](get-started/try-viam/try-viam/motors-running.png)

{{<gif webm_src="/get-started/try-viam/rotating.webm" mp4_src="/get-started/try-viam/rotating.mp4" alt="The robot rotating with the left motor running at 20% power and forwards and right motor running at 80% power and backwards." max-width="400px" class="aligncenter">}}

#### Board control

The [board component](/components/board/) is the signal wire hub of a machine which allows you to control the states of individual GPIO pins on the board.

For the Viam Rover, the board component is named `local` and controls a Raspberry Pi on the Viam Rover.
With it, you can control the states of individual GPIO pins on the board.

![The board panel in the CONTROL tab, including fields to get and set GPIO pin states.](get-started/try-viam/try-viam/board-panel.png)

#### Web gamepad control

The [web gamepad component](/components/input-controller/webgamepad/) is disabled by default, but if you have a compatible gamepad, you can enable the **Enabled** toggle.

## Learn about machine configuration

On the Viam app, navigate to the **Components** subtab, under **CONFIGURE**.
There you can view the configuration for each component in the machine: attributes, component dependencies, pin assignments, and more.

![The CONFIG tab in Builder mode (as opposed to Raw JSON). The board component panel and right motor panel are visible.](get-started/try-viam/try-viam/config-builder.png)

### Board configuration

The [board component](/components/board/) component is the signal wire hub of a machine.
Configuring a board component allows you to control the states of individual GPIO pins to command the electrical signals sent through and received by the board.
For the Viam Rover, the board component is a Raspberry Pi with **Name** `local`, **Type** `board`, and **Model** `pi`.

### Encoder configuration

An [encoder](/components/encoder/) is a device that is used to sense angular position, direction and/or speed of rotation.
In this case, the encoders on the left and right motors are `Lenc` and `Renc` and configure the pins to `le` and `re`.

{{< alert title="Important" color="note" >}}
When configuring encoded motors for your own robot, you must configure the encoders before the motors because the motors depend on the encoders.
{{< /alert >}}

![The right encoder config panel with the board attribute set to 'local' and the pins struct containing 'i' set to 're'.](get-started/try-viam/try-viam/right-encoder.png)

### Motor configuration

Both [motors](/components/motor/) on this rover use the model `gpio` which is the model for basic DC motors that are connected to and controlled by the configured board.

The attributes section lists the board the motor is wired to, and since the rover's motors are encoded the user interface also shows the encoded motor attributes: the encoder name, motor ramp rate limit, encoder ticks per rotation, and max RPM limit.

You can click **{}** (Switch to Advanced) on the top right of the component's card to view the attributes field in raw JSON format.
The attributes pane contains the current JSON configuration for this component.
Click **Switch to Builder** to return to the default graphical user interface.

### Base configuration

The [base component](/components/base/) is the platform that the other parts of a mobile robot attach to.
By configuring a base component, the individual components are organized to produce coordinated movement and you gain an interface to control the movement of the whole physical base of the robot without needing to send separate commands to individual motors.
The base's type is `base` and its model is `wheeled` which configures a robot with wheels on its base, like the Viam Rover.
The **left** and **right** attributes configure the motors on the left and right side of the rover, which are named `left` and `right`, respectively.

The **Wheel Circumference** (in millimeters) is 217.
The **Width** is the distance between wheel centerlines, 260mm in this case.
The **Spin Slip Factor** of 1.76 is used in steering calculations to account for slippage of the wheels against the ground while turning.

![The base configuration panel, showing right and left motors, wheel circumference set to 217, width set to 260mm, and spin slip factor set to 1.76.](get-started/try-viam/try-viam/base-config.png)

### Camera configuration

The [camera component](/components/camera/) configures the webcam that is plugged into the Raspberry Pi of the rover.
The camera component has the **Type** `camera`, the **Model** `webcam`, and the **Video Path** is `video0`.

For more information on choosing the correct video path, refer to our [webcam documentation](/components/camera/webcam/).

![The video path in the webcam configuration panel is set to 'video0'.](get-started/try-viam/try-viam/camera-config.png)

### Gamepad configuration

The [web gamepad](/components/input-controller/webgamepad/) component has the **Type** `input_controller` and the **Model** `webgamepad`.

![The gamepad configuration panel. No attributes are configured.](get-started/try-viam/try-viam/gamepad-config.png)

If you connect a generic gamepad controller to your computer, you can use it to control your machine.

If you are configuring your own machine, be aware that using the gamepad requires a service.
To see how the service is configured, navigate to the **Services** section under the **CONFIGURE** tab.
The **Services** subtab contains the "Base Remote Control" service which uses three attributes:

- **base**: `viam_base`
- **control_mode**: `joystickControl`
- **input_controller**: `WebGamepad`

The names for **base** and **input_controller** correspond to the naming scheme from the **Components** tab.

![The base remote control service named 'base_rc' on the Services subtab of the CONFIG tab.](get-started/try-viam/try-viam/base-rc.png)

### Raw JSON

The 'Builder' configuration mode provides a user-friendly, guided experience for you.
In the background, the Viam app translates the Viam machine configuration into JSON.
You can view the complete JSON for your rover by clicking on **Raw JSON** at the top left of the **CONFIGURE** tab.

![The CONFIG tab with the mode toggled to Raw JSON. A section of the full raw JSON config is displayed but one would have to scroll to see all of it.](get-started/try-viam/try-viam/raw-json.png)

You can [copy this `JSON` config between rental rovers](/get-started/try-viam/faq/#how-can-i-reuse-my-rented-rover).

## Next steps

If you have questions, check out our [FAQ](/get-started/try-viam/faq/) or join our [Discord Community](https://discord.gg/viam), where you can ask questions and meet other people working on robots.

{{< cards >}}
{{% card link="/get-started/quickstarts/drive-rover/" %}}
{{% card link="/tutorials/services/basic-color-detection/" %}}
{{% card link="/get-started/try-viam/rover-resources/" %}}
{{< /cards >}}
