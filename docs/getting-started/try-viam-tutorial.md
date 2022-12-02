---
title: "Try Viam: Reserving and Controlling a Camera-Equipped Viam Rover Remotely"
linkTitle: "Try Viam: Viam Rover Tutorial"
weight: 5
type: "docs"
description: "Instructions for using the Viam app to rent and configure a camera-equipped Viam Rover with a Raspberry Pi."
---

**Try Viam** is a way you can try out the platform without setting up any hardware yourself.
You can take over a Viam Rover in our robotics lab for 15 minutes to play around!

This tutorial will guide you through using a Viam Rover that you will be renting in the rover rink.
Viam Rover is pre-assembled with a Raspberry Pi microcontroller, two motors, a base, encoders, and a camera.
It also has an overhead camera for you to be able to see it in relation to the space.

## How to reserve a slot to try Viam

- **Click on "TRY' in the Viam app.** Log into Viam and go to the TRY tab.

  - Don't have a Viam account? Sign up [here](https://app.viam.com/try) to easily create one.

- **Reserve your slot.** If no one's using a Viam Rover, you'll take over immediately.
 Otherwise, you'll see an estimate for the next time slot, and we'll send you a reminder email when your reserved slot is approaching.

The email will look like this:

![](../img/try-viam-tutorial/image3.png)

Now that you are on the website, and there is availability, click **TRY NOW**, to start your reservation and start setting up your robot.

![](../img/try-viam-tutorial/image29.png)
![](../img/try-viam-tutorial/image11.png)

![](../img/try-viam-tutorial/image33.png)
![](../img/try-viam-tutorial/image9.png)

If you scroll on the **SETTING UP ROBOT**, it will tell you that the wait time could take about 30 seconds.

![](../img/try-viam-tutorial/image6.png)

After it establishes a connection and sets up your robot, new buttons will pop up.
If you click on **TRY YOUR ROBOT**, it will open a new window for the Viam App, which will be your robot.
In the same page, you will be able to **CANCEL RESERVATION** or **EXTEND RESERVATION**.

![](../img/try-viam-tutorial/image21.png)

You can always return to the generic rental page by clicking on the **TRY** tab. Clicking on the timer in the header will redirect you to specific robot control page.

![](../img/try-viam-tutorial/image5.png)

## Viam explained, and driving around with UI

The first screen you will see is your robot page and the **CONTROL** panel.
In the header you will be able to see your rover name, your rover host, and remote address.
This information is randomly generated for you.

![](../img/try-viam-tutorial/image12.png)

In the **CONTROL** panel you will be able to see your base, left and right motors, web game pad, the board, and two cameras.
These are not in a relative order, so don't worry if yours look different.

![](../img/try-viam-tutorial/image4.png)

To move your rover around with the UI, you have to click on **viam_base** and toggle your keyboard enabled.
You can use **W** and **S** to go forward and back, and **A** and **D** to arc and spin. You can also use your arrow keys to control the same.
They correspond to A = left arrow, W = up arrow, D = right arrow and S = down arrow.

If you select a camera (you will have two options, one for the front camera of the rover and second for the overhead camera), you will be able to see around as you move your rover.

![](../img/try-viam-tutorial/image24.png)

![](../img/try-viam-tutorial/image10.png)

The camera selection panel looks like this when expanded:

![](../img/try-viam-tutorial/image30.png)

If both of the cameras are selected in the panel, it will look like this:

![](../img/try-viam-tutorial/image36.png)

Each time you show or hide a camera, your **Keyboard Enabled** will automatically toggle down to **Keyboard Disabled**.
So if you change your camera configurations, don't forget to retoggle your keyboard control to enabled.
This automation is for safety purposes.

If you toggle to **DISCRETE** tab, then you'll see different movement modes such as "Straight" and "Spin"; and different movement types such as "Continuous" and "Discrete" and directions such as "Forwards" and "Backwards."
You will also be able to tinker with speed.

![](../img/try-viam-tutorial/image31.png)

If you want to go down in your config to individual cameras and their streams, you can click on them to expand, and toggle **Show Camera**.
In these panels, you will be able to refresh your camera on certain frequency (it can be live all the time, or refresh every minute, etc.), and you can export screenshots from your camera streams.

![](../img/try-viam-tutorial/image2.png)

![](../img/try-viam-tutorial/image28.png)

Some other components you will have preconfigured in your robot config will be the motors (which allows you to move the base).
We named these motors "left" and "right" corresponding to their location on the rover base.
Their initial state is **Idle**. You can click on the each panel and make your motor **RUN** or **STOP**.

![](../img/try-viam-tutorial/image32.png)

A running left motor state would look like this:

![](../img/try-viam-tutorial/image22.png)

Both motors running at the same time would look like this:

![](../img/try-viam-tutorial/image26.png)

In these panels, you can change the motors' direction of rotation (which will allow them to go forward or backwards), and their power levels (which will allow them to go faster or slower).
You can also see their current positions in real time.

One other component you will have preconfigured in your robot config will be the board.
The board we have on the Viam Rover is the Raspberry Pi.

![](../img/try-viam-tutorial/image7.png)
![](../img/try-viam-tutorial/image20.png)

Finally, you will see your web gamepad.
It is default to disabled, but you can enable it by toggling the button.

![](../img/try-viam-tutorial/image17.png)
![](../img/try-viam-tutorial/image27.png)

## Learning about robot configuration

Now that you learned how to drive your rover with the UI, let's go a bit further.
One other thing you can do withing your experience is that you get to see your configuration.
If you click on to your **CONFIG** panel, under **COMPONENTS**, you will be able to see each component you have in the robot, and get more information about how they are configured.
Some of the information you will be able to see will be: if they require any attributes, if they depend on a board or to other components, their pin assignments...

![](../img/try-viam-tutorial/image16.png)

In your config your right motor will look like this:

![](../img/try-viam-tutorial/image15.png)

Here you will be able to see your motor model, which is gpio. You will be able to see your your motor is encoded, and that encoder is named "Renc" and has specific ticks per rotation and a max RPM. Its type is In1/In2, and the In1 pin is 16 GPIO 23, and In2 pin is 18 GPIO 24, and PWM is 22 GPIO 25. It depends on the local, and the Renc.

Your left motor will look pretty similar to the right:

![](../img/try-viam-tutorial/image8.png){

Here you will be able to see your motor model, which is gpio the same as the right motor.
You will be able to see your your motor is encoded, and that encoder is named "Lenc" and has specific ticks per rotation and a max RPM. Its type is In1/In2, and the In1 pin is 11 GPIO 17, and In2 pin is 13 GPIO 27, and PWM is 15 GPIO 22.
It depends on the local, and the Lenc.

Then you will be able to see your base.
We named it "viam_base" and its type is "base" and model is "wheeled".
The "wheel_circumference_mm" is 217, and the "width_mm" is 260. The "width_mm" is measured between the midpoints of the wheels.
For "left" we entered "left", and "right" in "right".
The left and right attributes represent the motors corresponding to the left and right sides of the rover.
Since we named the motors "left" and "right", we simply added "left" and "right" between the brackets for the set of motors, respectively.

![](../img/try-viam-tutorial/image18.png){

In the camera component, you will see the type as "camera" and the model "webcam".
The video path will be "video0" but if you like to learn more, see our [camera configuration tutorial](/tutorials/configure-a-camera/#connect-and-configure-a-webcam) for more information on choosing the correct video path.

![](../img/try-viam-tutorial/image14.png){

Then you will have your encoders, respectively named "Renc" and "Lenc".
They both will depend on "local" which is our board.

![](../img/try-viam-tutorial/image1.png)

![](../img/try-viam-tutorial/image35.png)

Finally, you will have your web gamepad in your components.
Its type is "input_controller" and the model is a webgamepad.
If you connect your generic gamepad controller to your computer, you can use it to control the rover in the rover rink.
For this to work though, we need a service. Fortunately, we added one for you!

![](../img/try-viam-tutorial/image34.png)

If you go to **SERVICES** tab under the **CONFIG**, you will see the "Base Remote Control" service.
This takes few attributes, which are "base", "control_mode" and "input_controller".
The names for "base" and "input_controller" are corresponding to how we named them in **COMPONENTS** tab.

![](../img/try-viam-tutorial/image13.png)

Now that we learned about components and services, one other thing we can do is to see the code that's generated for our rover as we added those components and services.

Within the **CONFIG** tab, if you change the "Mode" from **Builder** to **Raw JSON** you will be able to see the entire code.

![](../img/try-viam-tutorial/image23.png)

When you are done with your time, if you go back to your Try Viam page [app.viam.com/try](https://app.viam.com/try), you will see the button say **FINISHED**.
You can click **TRY NOW** to rent the rover again if no one is in the queue.

![](../img/try-viam-tutorial/image25.png)

## Connecting to a Viam rover with the Viam SDK

You can write your own code to control the Viam robot.
Before you get started, you will need to:

- First, be sure that you have reserved your slot to try out a Viam rover.

- **Install the Viam SDK locally.**
You can install the Viam SDK for [Python](https://python.viam.dev/) or [Go](https://pkg.go.dev/go.viam.com/rdk).

- **Copy a SDK snippet from the CODE SNIPPET tab.**
Copy the code snippet from the **CODE SAMPLE** tab.
This snippet imports all the necessary libraries and sets up a connection with the Viam app in the cloud.

You will see that here:

![](../img/try-viam-tutorial/image19.png)

You can find more information about using Viam's SDKs to control the Viam rover in our SDK docs.

Now let's try to do ...

Find a color in the rover rink...
