---
title: "Build a robotic claw game with a Raspberry Pi"
linkTitle: "Build a Claw Game"
weight: 50
type: "docs"
description: "Build a Claw Game with a Raspberry Pi."
tags: ["app", "board", "motor", "gripper"]
webmSrc: "/tutorials/img/claw-game/preview.webm"
videoAlt: "GIF of the claw game in action at a party."

# Author: Arielle Mella, Matt Vella, Hazal Mestci 
---

Create your very own version of the famous claw machine game using a robotic arm, a repurposed claw from an arcade game, and some items to pick from.
You will create abstracted obstacles that the robotic arm needs to avoid using Python SDK, and even learn how to fabricate your own encasement for this machine and how to create a custom control interface using the Typescript SDK.

## Introduction

Have you ever stepped foot in an arcade or bustling shopping mall and indulged in a claw machine game?
Armed with a handful of quarters and unwavering determination, you try to grip that adorable stuffed duck that has captured your heart.
Attempt after attempt, the coveted prize escapes your mechanical grasp.
Undeterred, you recalibrate your approach, setting your sights on a fluffy bear precariously perched on the edge of the drop hole, convinced you will win this time.
Carefully, you maneuver the joystick, circling the glass enclosure to ensure an optimal angle, and then you make your move, commanding the claw to seize the prize.
The claw descends, nearly gripping the bear, but alas, its grip is feeble, capturing a lone ear before retreating empty-handed to the drop hole.
You decide these games are always rigged and you move on.

{{<gif webm_src="/tutorials/img/claw-game/preview.webm" gif_src="/tutorials/img/claw-game/preview.gif" alt="GIF of the claw game in action at a party." class="alignright" max-width="250px">}}

If only you possessed the ability to engineer your own machine - imagine a creation where you could fine-tune every intricate detail, from the precision of each grab, to the claw's strength, and even the aesthetics of your control interface.
Through this tutorial, you will acquire the knowledge and skills to fabricate your very own claw machine by learning how to configure the components using Viam, master the art of controlling your robot with our Motion Service, and learn how to design a personalized interface using the TypeScript SDK.

## Requirements

### Hardware

* [Raspberry Pi](https://a.co/d/bxEdcAT) with microSD card, setup per [these instructions](https://docs.viam.com/installation/prepare/rpi-setup/).
* Mac or Linux computer
* [xarm6](https://www.robotshop.com/products/xarm-6-dof-robotic-arm)
* [Arcade claw](https://www.ebay.com/itm/393988987705)
* [Relay](https://www.amazon.com/gp/product/B095YFJ69T)
* [24v power supply](https://www.amazon.com/gp/product/B08F7DVY8G) - for the claw
* iPad or other tablet
* 1-  4’ x 4’ fiberboard
* 10-  2” x 4” x 8’ lumber
* 4 - [5/16 2 inch lag screws](https://www.homedepot.com/p/Everbilt-5-16-in-x-2-in-Zinc-Plated-Hex-Drive-Hex-Head-Lag-Screw-801446/204645617)
* 1 -  box of 3” deck screws
* 8 - [⅜” 4 inch hex bolts](https://www.homedepot.com/p/Everbilt-3-8-in-24-TPI-x-4-in-Zinc-Plated-Grade-5-Fine-Thread-Hex-Bolt-851928/205029373) with nuts and washers
* [Velcro cable ties](https://www.amazon.com/Fastening-Adjustable-Organization-Microfiber-Management/dp/B08KH6WTJZ)
* 3 - 4’ x 2.5’ sheets of plexiglass
* Box of small wood screws for mounting plexiglass
* Items/balls to pick up

### Software

* [`viam-server`](https://github.com/viamrobotics/rdk/tree/0c550c246739b87b4d5a9e8d96d2b6fdb3948e2b), installed with [these instructions](https://docs.viam.com/installation/#install-viam-server).
* [Python 3](https://www.python.org/download/releases/3.0/)
* [Pip](https://pip.pypa.io/en/stable/#)
* [Viam Python SDK](https://python.viam.dev/)
* [Viam Typescript SDK](https://ts.viam.dev/)

### Tools

You will also need the following tools:

* Drill and drill bit set
* Miter saw or handsaw
* Jigsaw
* Sliding square rule
* Socket wrench set
* Safety glasses and ear protection
* Wood glue
* 3D printer
* Clamps
* Tape measure

## Build the robot

To get started with this project, you’ll first need to build an enclosure to make the game counter-height, so that you can mount the robotic arm, and have a space that holds the prizes.
In this tutorial, we’ll cover how to build a basic functional enclosure, but you can later add design elements to style it as you like.

### Build the table

To support the arm and create a surface to hold the prizes, you will create a flat surface that also has supporting beams so as to securely mount the arm.
You will build the table to a size that allows for the arm to reach anywhere on the table surface.
For the xArm6, a table that is 4 foot by 4 foot will accomplish that goal.

Cut one 2x4” in half, creating two 48 inch sides.
Then, take two 2x4s and cut them to four 46.5 inch lengths.
Now, place the 48 inch sides parallel to each other on a flat surface, and place the 4 other lengths perpendicular to and between the 48 inch sides.

Attach the 48 inch sides to two of the shorter lengths with deck screws, forming a 4 foot by 4 foot square.
Now, find the center of the 48 inch sides and mark this on both sides.
Measure 2.5 inches from there in either direction, and mark those points.
This will be the center points for where we attach the remaining lengths, which will provide a support structure for the robotic arm.
Attach these lengths with deck screws.

![4’ x 4’ square made with wood pieces on the floor.](/tutorials/img/claw-game/build-base.jpg)

{{< alert title="Info" color="info" >}}
The image above does not have the center lengths in the correct location - they are not yet centered or spaced.
{{< /alert >}}

The fiberboard will serve as a tabletop, but you will need to cut a prize exit hole in the fiberboard.
Center the exit, make it 10 inches wide, 8 inches long and cut the opening with a jigsaw.
We used two 2 foot by 4 foot fiberboards, but ideally you can use one 4 foot by 4 foot fiberboard.
Glue and clamp the tabletop and let it dry overnight.

![Wooden table top glued and secured with clamps.](/tutorials/img/claw-game/build-table.jpg)

### Add legs and mount the arm

Cut four 2x4s to 78 inches to serve as legs for the cabinet.
Measure 30 inches from the top of each and mark this with the sliding square rule.

For each leg, line the 30 inch mark up with the top surface of the table, and drill two holes ⅜ inch holes through the leg and table surface.
Push two hex bolts through drilled holes, add washers and nuts, and tighten.

For extra stability, cut two more 2x4s to 48 inch lengths, and mount these with deck screws on all four sides of the bottom of the cabinet, bridging the legs.
We also cut a 2x4 and mounted it like a 5th leg, going from the center arm supports to the floor.

Finally, mount the xArm6 to the top of the table using the lag screws.
Be sure that the lag screws are sinking into the 2x4 posts below, and that you are mounting the arm so that it is oriented straight, with the X axis facing the player.
You’ll need at least two people for this.

![The xarm6 attached to the middle of the enclosure.](/tutorials/img/claw-game/mount-arm.jpg)

## Configure the robot in the Viam app

Go to [the Viam app](https://app.viam.com) and create a new robot.
Now we are ready to configure all of our components.
For this project, we will use two parts in our robot:

* A main part representing our Raspberry Pi, which will be used to open and close the claw with GPIO.
* A subpart that we’ll use to run the motion service and communicate with the arm.

Technically you could configure all the components within one part, but motion planning is more performant when running on a computer like a macOS or a Linux laptop running `viam-server`.

Parts configured into a single Viam robot allow for secure communication over a single interface.

### Part/Sub Parts

Robots are organized into parts, where each part represents a computer (a [single-board computer](https://docs.viam.com/installation/), desktop, laptop, or other computer) running `viam-server`, the hardware [components](https://docs.viam.com/components/) attached to it, and any [services](https://docs.viam.com/services/) or other resources running on it.

Every robot has a main part which is automatically created when you create the robot.
Multi-part robots also have one or more sub-parts representing additional computers running `viam-server`.
If you have two computers within the _same robot_, you can use one as the main part and [connect the other to it as a sub-part](https://docs.viam.com/manage/parts-and-remotes/#configure-a-sub-part).
We are running the motion planning on a laptop and connecting that laptop as a sub-part to our robot.

Use the parts drop-down menu in the top banner of your robot’s page on [the Viam app](https://app.viam.com/) to add a new sub-part called “planning”:

![Screenshot of the Viam App, adding a sub part named planning.](/tutorials/img/claw-game/app-planning.png)

For more information about parts, see [Robot Architecture: Parts, Sub-Parts and Remotes](https://docs.viam.com/manage/parts-and-remotes/).

### Configure the board

In arm-main, add your [board](https://docs.viam.com/components/board/) with the name `myBoard`, type `board` and model `pi`. Click ****Create Component****.

![Create component panel, with the name attribute filled as myBoard, type attribute filled as board and model attribute filled as pi.](/tutorials/img/claw-game/app-component-myboard.png)

You can name your board whatever you want as long as you are consistent with it, we picked myBoard for simplicity. This is the only component in the main robot.

Use the parts drop-down menu in the top banner of your robot’s page on the [Viam app](https://app.viam.com/) to navigate to the sub-part “planning” you just created.

![Screenshot of the Viam App, navigating to a sub part named planning.](/tutorials/img/claw-game/app-subpart-planning.png)

In the sub-part section “planning”, let’s configure our arm and gripper.

### Configure the arm

In planning, add your [arm](https://docs.viam.com/components/arm/) with the name `myArm`, type `arm` and model `xArm6`. Click ****Create Component****.

![Create component panel, with the name attribute filled as myArm, type attribute filled as arm and model attribute filled as xArm6. In the Attributes section, host is filled 10.1.1.26 and in Frame section, there is a world frame.](/tutorials/img/claw-game/app-myarm.png)

Initialize the arm component with the correct IP address in the `host` field under Attributes.
We used `10.1.1.26` since that is the address corresponding to our arm, but you should use the IP address for your arm.

For more information on xArm6 configuration, see “[Configure an xArm6 Arm](https://docs.viam.com/components/arm/xarm6/).”

### Configure the gripper

Add your [gripper](https://docs.viam.com/components/gripper/) with the name `gripper`, type `gripper` and model `fake`. Click ****Create Component****.

![Create component panel, with the name attribute filled as gripper, type attribute filled as gripper and model attribute filled as fake. In the Frame section, there is a myArm parent in the frame.](/tutorials/img/claw-game/app-gripper.png)

Set up a `fake` model - we won’t be able to use the API methods to move the gripper, but we will use the `fake` gripper to represent the size of the claw in Viam’s frame system, used in motion planning.
You have to measure the claw for this part.
Ours is 120mm for the width and 180mm for the height.

## Set up the claw

### 3D print the claw mount

[Download the STL](https://github.com/viam-labs/claw-game/blob/main/xarm6ClawMount.stl) for the claw mount, and use a 3D printer to print the mount between the claw and the xArm6.

![3d printed claw mount part](/tutorials/img/claw-game/claw-mount.jpg)

### Attach the claw to the printed mount

* With a screwdriver, remove the metal top cap from the claw by removing the side screws.
* Remove the string that came with the claw, it is not needed.
* Extend 2 or 3 M3 button socket cap screws through the recessed inner holes of the printed mount and through the slots on the top of the claw cap.
* Secure the M3 screws with nuts and tighten.
* Attach the printed mount and claw end cap to the claw, add the previously removed screws and tighten.

### Mount the claw to the arm

* Using two M20 screws, attach the printed mount to the end of the arm and tighten.
* Using velcro cable ties, run the claw’s cable along each segment of the arm to the arm base, making sure the cord is secure but with some slack to allow for movement.

![Screw holes on the xarm6 head without the attachment](/tutorials/img/claw-game/mount-screw-holes.jpg)

![3d printed mount attached to the gripper and mounted to the arm](/tutorials/img/claw-game/mount-gripper.jpg)

![Gripper attached to the arm and cord wired around the arm](/tutorials/img/claw-game/mount-together.jpg)

### Wire and test the claw

The arcade claw is actuated when a solenoid is powered, acting as a magnet to pull the claw shut.
We will use a relay, which allows us to programmatically control when power flows to the claw’s solenoid.

Using a barrel jack adapter, connect the positive (red) wire from the claw to the positive terminal of the adapter.
Then, run the negative (black) wire from the claw to the ‘COM’ terminal on the relay.
Cut a length of wire and connect it between the ‘NO’ terminal on the relay and the negative terminal on the barrel jack adapter.
This creates a ‘normally open’ circuit, which means the circuit is normally not complete and the claw is therefore normally not powered.

In order to control the claw through Viam, we will now wire the relay to the Raspberry Pi.
First, power down the Pi. Then take 3 female jumper wires, cut off one end of each, and strip the ends.
Use one wire to connect the DC+ terminal on the relay to pin 2 (5v) on the Pi.
Use the second to connect the DC- terminal on the relay to pin 6 (ground) on the Pi.
Use the third to connect the IN terminal on the relay to pin 8 (GPIO) on the Pi.

![Wiring guide for the claw game showing all assembled components with the wiring plan for each component.](/tutorials/img/claw-game/wiring-guide.png)

Now power on the Pi and plug the 24V DC adapter into the wall and the barrel jack adapter.

Once `viam-server` has started, we can test closing and opening the claw.
The relay will trigger the claw circuit to be closed when the GPIO pin state is set to high.
The Viam `board` component gives us an interface for this.
Go to the **Control** tab for your robot, open the MyBoard card, enter 8 next to 'Set' under the GPIO interface, choose `high` and click **Set Pin State**.
Your claw will close.
Now select ‘low’ and click ‘Set Pin State’ again - the claw will open.

![GPIO pin 8 getting set as high on the Control panel.](/tutorials/img/claw-game/app-gpio-high.png)

## Create obstacles and a world state

To make sure the arm doesn’t hit the walls of the enclosure or the prize drop hole, we will create representations of obstacles around the arm that the motion service will avoid when planning.

Obstacles are geometries located at a pose relative to some frame.
When solving a motion plan with movable frames that contain inherent geometries, the solved path is constrained such that none of those inherent geometries intersect with the obstacles.

You can pass information about the robot’s environment (including obstacles) to the Viam platform through a data structure named [WorldState](https://python.viam.dev/autoapi/viam/proto/common/index.html#viam.proto.common.WorldState).

We are configuring obstacles for the claw game robot’s environment in a file that contains JSON obstacle representations in the project [repository](https://github.com/viam-labs/claw-game/blob/main/obstacles.json).
Represented are obstacles for the hole, front wall, back wall, right wall and left wall based on measurements we took from our enclosure.
These obstacles are configured in reference to the “world” frame, which is a special frame that represents the starting point for all other frames in the robot’s world.
The list of obstacles are included in a WorldState object, which is passed in each motion service [move()](https://docs.viam.com/services/motion/#move) call.  

If the dimensions of your enclosure differ from ours, you can adjust the obstacles.

{{< alert title="Note" color="note" >}}
If the arm is not mounted exactly perpendicular to the x/y axis of the enclosure, you can adjust the theta (_th_) of the arm by a number of degrees to compensate within the arm component configuration.
Obstacles can then be configured as if the arm were straight in the enclosure.
You can read more about the frame system in our [documentation](https://docs.viam.com/services/frame-system/).
{{< /alert >}}

### Find the home pose within the enclosure

By moving the arm through the Viam app control tab, we found the desired home pose used to start each game session and return to after a grab.
We also found the desired distance between the lateral plane and the pick up level.
These numbers could change depending on your enclosure and it’s best to test.
For us the hole pose and dimensions were as follows:

```sh
    hole_origin = Pose(x=470, y=125, z=0, o_x=0, o_y=0, o_z=1, theta=15)

    hole_dims = Vector3(x=250, y=400, z=300)
```

And the home position origin and dimensions where the arm should be located at in order to drop the prize were as follows:

```sh
    home_pose = Pose(x=390.0, y=105.0, z=500.0, o_x=0, o_y=0, o_z=-1, theta=0)

    home_pose_in_frame = PoseInFrame(reference_frame="world", pose=home_pose)
```

The floor level where the claw will drop has different numbers for x and y since you can pick from anywhere on the plane, but the Z axis is always the same since you always drop to the same level.
We tested between 240 and 280 for this level, but you can adjust it to your liking.

## Use Python code to control the arm

Use `git` to clone our [Claw Game project repository](https://github.com/viam-labs/claw-game/):

```sh
git clone https://github.com/viam-labs/claw-game
```

The repo includes the Python test script `CLI-test.py`, which connects to our robot, creates an orientation constraint so the last arm joint is always looking down, and provides functions to:

* Grab and release the claw
* Move the arm to the home position
* Move the arm to a test position
* Move the arm forward, backward, right and left
* Move the arm to the drop position
* Move the arm to the up position

This script provides an interface to run a single move command, or to run move commands in sequences.
You can adjust the code to your liking.

Below are different sections of the code explained.

First, we import Viam packages:

```python
import json

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.board import Board
from viam.components.arm import Arm
from viam.services.motion import MotionClient
from viam.proto.common import Pose, PoseInFrame, Vector3, Geometry, GeometriesInFrame, RectangularPrism, WorldState
from viam.proto.service.motion import Constraints, LinearConstraint, OrientationConstraint
```

Then we create an argument parser, defining required and optional arguments to create a user-friendly command line interface.

```python
parser = argparse.ArgumentParser()
parser.add_argument('--command', type=str, required=True)
parser.add_argument('--sequence', type=str, required=False)
parser.add_argument('--location', type=str, required=True)
parser.add_argument('--password', type=str, required=True)

args = parser.parse_args()
```

Next we create some constants such as how much the arm should move at each call, where the home position should be and where it should drop to grab the prizes.
You can tweak these numbers to your preference.

```python
# The amount to move in mm for each command forward, backward, left, right
move_increment = 50

# Define home position to return to 
home_plane = 500.0
home_pose = Pose(x=390.0, y=105.0, z=home_plane, o_x=0, o_y=0, o_z=-1, theta=0)

# Define plane to grab on
grab_plane = 240.0
```

Then we define the [constraints](https://python.viam.dev/autoapi/viam/proto/service/motion/index.html#viam.proto.service.motion.Constraints) - in this case we are using an [orientation constraint](https://docs.viam.com/services/motion/constraints/#orientation-constraint).
The orientation constraint places a restriction on the orientation change during a motion, as in our case we want the arm to be always looking down so the gripper is always in a position to be able to lower down and grab.  

```python
constraints = Constraints(orientation_constraint = [OrientationConstraint()])
```

We now import the `obstacles.json` file and define the `world_state` representing the robot’s physical environment.

```python
def get_world_state():
    with open('obstacles.json', 'r') as f:
        geometries = json.load(f)

    world_state_obstacles = []
    for geometry in geometries:
        center = geometry['translation']
        orientation = geometry['orientation']['value']
        center = Pose(
            x=center['x'], 
            y=center['y'], 
            z=center['z'], 
            o_x=orientation['x'], 
            o_y=orientation['y'], 
            o_z=orientation['z'], 
            theta=orientation['th'],
        )
        dims = Vector3(x=geometry['x'], y=geometry['y'], z=geometry['z'])
        world_state_obstacles.append(Geometry(center=center, box=RectangularPrism(dims_mm=dims), label=geometry['label']))

    obstacles_in_frame = GeometriesInFrame(reference_frame="world", geometries=world_state_obstacles)
    return WorldState(obstacles=[obstacles_in_frame])
world_state = get_world_state()
```

We define a grab function to use GPIO to open and close the gripper by setting the Raspberry Pi pin state to high or low.

```python
async def grab(board, doGrab):
    # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
    pin = await board.gpio_pin_by_name('8')
    if doGrab == True:
        #opens the gripper/release
        await pin.set(True)
    else:
       #closes the gripper/grab
       await pin.set(False)

```

We also define the functions `move_absolute()`, `home()`, `move_to_offset()` and `move_z()`, which construct new pose requests to send to the motion service.

We then include code to handle command-line arguments to move the arm in a sequence for testing and debugging.

```python
for command in commands:
        if command == "drop":
            print("will drop")
            await move_z(my_arm_resource, motion_service, grab_plane) 
        if command == "up":
            print("will go up")
            await move_z(my_arm_resource, motion_service, home_plane) 
        if command == "home":
            print("will return home")
            await home(my_arm_resource, motion_service) 
        if command == "left":
            print("will move left")
            await move_to_offset(my_arm_resource, motion_service, Vector3(x=0, y=-move_increment, z=0)) 
        if command == "right":
            print("will move right")
            await move_to_offset(my_arm_resource, motion_service, Vector3(x=0, y=move_increment, z=0)) 
        if command == "forward":
            print("will move forward")
            await move_to_offset(my_arm_resource, motion_service, Vector3(x=move_increment, y=0, z=0))
        if command == "backward":
            print("will move backward")
            await move_to_offset(my_arm_resource, motion_service, Vector3(x=-move_increment, y=0, z=0))
        if command == "grab":
            print("will grab")
            # Closes the gripper
            await grab(my_board, True)
        if command == "release":
            print("will release")
            # Opens the gripper
            await grab(my_board, False)
        if command == "sleep":
            print("will sleep one second")
            await asyncio.sleep(1)
        if command == "test":
            print("will move to test position, drop, grab, return home and release")
            await move_absolute(my_arm_resource, motion_service, Pose(x=0.0, y=380, z=home_plane, o_x=0, o_y=0, o_z=-1, theta=0)) 
            await move_z(my_arm_resource, motion_service, grab_plane) 
            await grab(my_board, True)
            await home(my_arm_resource, motion_service) 
            await grab(my_board, False)
```

Using `CLI-test.py`, you can run individual commands from the terminal, for example:

```sh
python3 CLI-test.py --password mypass --location mylocation --command grab
```

Or, you can run sequences of commands like:

```sh
python3 CLI-test.py --password mypass --location mylocation --command sequence --sequence grab,sleep,release,sleep,grab,sleep,release
```

Now that the arm is set up and you have a CLI script you can use for testing - try testing the motion and claw grab with different items.
Sometimes the claw will have a better time grabbing certain items over the others.
The size and weight of the object is important here, as well as the shape of it.
You can also try increasing the voltage of the claw power supply if you feel like it is not picking objects, especially if they are heavy (but don’t exceed the limits of the relay).

We tested with different Viam swag items such as t-shirts and hats, but ended up using foam balls.

## Add enclosure sides and fill it with prizes

In order to contain the prizes, you’ll need to enclose 3 sides (front, left, and right sides) of the upper cabinet with plexiglass.
Have someone hold the plexiglas in place while you carefully pre-drill holes for the wood screws.
Then carefully screw the wood screws in place, being sure to not tighten excessively (this can crack the plexiglass).

Finally, add a short barrier in the back to stop the prizes from falling out.
We used the remaining 2x4 section.
You will also need to do the same for the prize exit hole. We used some extra fiberboard and glue, but you could use cardboard, wood, or any other rigid material available.

Now you can fill the enclosure with prizes!
The more the merrier (we used over 600 balls at Viam’s General Availability launch party), but make sure they don’t overflow from the prize exit hole or the backstop.

## Create a custom interface using TypeScript

Now that you’ve built out and tested all of the main functionality of your DIY claw machine game, it’s time to design your custom interface.
We will be designing this for a touch screen tablet (in our project, we mounted an iPad to the facade of our claw machine prototype) to be hosted on a macOS or Linux computer locally and then accessed on the tablet via your computer's local address.

Within the project code repository, the `src` folder contains the main Typescript code that executes all robot commands.
The `static` folder contains the frontend code, including styling and HTML.

To use the Viam Typescript SDK you will have to install dependencies in your main project folder.
Make sure you have the [latest version of Node.JS installed](https://nodejs.org/en).

Once you have installed Node, you can now fetch all dependencies, including the [Viam Typescript SDK](https://ts.viam.dev/) by running the following command in your project directory:

```sh
npm install
```

The **process.env** file is a global object used to access all the environment variables of the environment your application is running.
This ensures that your security keys are not accessible to others when publishing your code.
You can find your robot secret and host link in the **Code Sample** tab in the Viam app.
Remember to use the host address of your main robot part as it will reference all parts of your robot.
You will use these to set the environment variables `VIAM_LOCATION` and `VIAM_SECRET`.
You can set them and start the Typescript app as follows:

```sh
export VIAM_LOCATION=mylocation;VIAM_SECRET=mysecret;npm run start-simple
```

Visit `localhost:8000` in a browser.
Press the buttons to execute commands defined in **main.ts** and watch your robot arm move around using the simple user interface.

The Typescript app reads in the obstacles and creates a world state from the same obstacle JSON file that we used with the Python testing script.

The Typescript interface code includes functions that define movements in each direction on a plane relative to the base of the game.
This includes forward, back, left, right, and home functions.
If you look through the code you will notice that they all follow the same conventions by using the Motion Client method [`move()`](https://ts.viam.dev/interfaces/Motion.html#move) and passing in all of the obstacles defined globally and [`WorldState`](https://ts.viam.dev/classes/commonApi.WorldState.html) variables in each function.

```js
async function right(motionClient: MotionClient, armClient: ArmClient) {
  if (ignoreInterrupts && await armClient.isMoving()) { return }

  // Get current position of the arm 
  console.log('im trying to print the current position')
  let currentPosition = await motionClient.getPose(myArm, 'world', [])
  console.log('current position:' + JSON.stringify(currentPosition))

// Define the new right position by adding to the y value incrementally so that your robot arm will move 
  let rightPose: Pose = {
    x: currentPosition.pose!.x,
    y: currentPosition.pose!.y + moveDistance,
    z: currentPosition.pose!.z,
    theta: 0,
    oX: 0,
    oY: 0,
    oZ: -1
  };

  let rightPoseInFrame: SDK.PoseInFrame ={
    referenceFrame: "world", 
    pose: rightPose
  }
// Call the move method with the new rightPose values to move your arm and pass in your robot component name, WorldState, and constraints 
  await motionClient.move(rightPoseInFrame, myArm, myWorldState, constraints)
}
```

For each function we created that moves the arm, we have corresponding buttons that trigger these actions in our browser environment.
Each of these button functions are initialized the same way for each corresponding `move()` function.
For the purpose of this tutorial, we will look at how we set this up for movements to the right.

```js
//Creating a button function that corresponds to the HTML element that will show on your webpage 
function rightbutton() {
  return <HTMLButtonElement>document.getElementById('right-button');
}

//Since we are designing for a touch screen, we are using a touchstart event for our button command
 rightbutton().ontouchstart = async () => {
    rightHandler()
  };

//This function is where the move function is called as well as adding some timeout and color changing media queries 
async function rightHandler() {
    if (rightbutton().classList.contains('error')) return;
    try {
      await right(motionClient, armClient);
      if (rightbutton().classList.contains('custom-box-shadow-active')) {await rightHandler()};
    } catch (error) {
      console.log(error);
      rightbutton().classList.add('error');
      rightbutton()?.querySelector('svg')?.classList.add('icon');
      setTimeout( () => { rightbutton().classList.remove('error'); }, 3000 )
    }
  }
```

As with the Python test script, the TypeScript code also controls our arcade claw with GPIO on a Raspberry Pi.
We control this in Typescript by setting the pin state to HIGH or LOW on the board component by using the [`setGPIO()`](https://ts.viam.dev/classes/BoardClient.html#setGPIO) method in the via Board Client.
Here we created a `grab` function that calls the `setGPIO()` method.

```js
//Global variable: GPIO pin used for claw relay on the board
const grabberPin = '8'

//Print out the pin state and set the GPIO state with a boolean value 
async function grab(boardClient: BoardClient) {
  try {
    console.log(await boardClient.getGPIO(grabberPin));
    console.log('i`m grabbin');
    await boardClient.setGPIO(grabberPin, true);  
  }
}
```

## Summary

In this tutorial, you learned how to:

* Fabricate your own claw machine.
* Test, configure and control a robot arm using Viam’s motion service in Python and in the Viam App.
* Design your own custom interface using the Viam TypeScript SDK.

For some next steps, you can:

* Use the advanced interface included in the project repository to leverage the motion service for larger, more complex moves within the enclosure.
* Add a camera and use Viam’s Vision Service with a color detection or an ML model to determine grab success and create a score counter.
* Design a hard mode where the prizes are shuffled around with the arm every few attempts.
* Add a camera and extend the interface to allow folks from anywhere in the world to to play the claw game and win (hint: Viam already allows you to securely control robots from anywhere).

If you want to connect with other developers learning how to build robots, or if you have any issues whatsoever getting Viam set up, let us know on our [Discord Server](https://discord.gg/viam), and we will be happy to help you get up and running.
