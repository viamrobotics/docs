---
title: "Control an Intermode Rover with CAN bus and Viam"
linkTitle: "Control an Intermode Rover with Viam"
weight: 60
type: "docs"
tags: ["modular resources", "extending viam", "components", "base", "CAN bus", "Intermode"]
description: "Integrate an Intermode rover as a modular resource based component with CAN bus"
# SME: Matt Vella, Matt Dannenberg, James Otting
---

The Viam platform comes with a component called [base](/components/base/), which adds some very useful abstractions for simplified control of mobile robots.
Instead of controlling individual motors, the base component allows you to [issue commands](https://python.viam.dev/autoapi/viam/components/base/index.html#package-contents) like “move_straight”, “spin”, “set_velocity” and “stop”.  

Many robotic rovers can be controlled out-of-the-box with the Viam **wheeled** base model - simply by specifying how your motorized wheels are configured.
But what if you want to control a rover or other mobile robot that does not expose direct motor control?
This tutorial will show you how to create a [modular resource](/product-overviews/extending-viam/modular-resources/) (custom component), which can then be controlled seamlessly with the rest of your robot (sensors, etc) through the [Viam SDK](/product-overviews/sdk-as-client/) of your choice.

<img src="../img/intermode/rover_outside.png"  style="float:left;margin-right:12px" alt="Intermode rover pictured outdoors." title="Intermode rover pictured outdoors." width="400" />

While the concepts covered here are applicable to other hardware, we’ll specifically show you how to use Viam to control the <a href="https://www.intermode.io/" target="_blank">Intermode rover</a>.
This is a powerful pairing: **Intermode** aims to make the hardware aspects of a mobile robot-based business simple and worry-free, while Viam simplifies the software aspects of any robotics business.

The Intermode rover uses the <a href="https://en.wikipedia.org/wiki/CAN_bus" target="_blank">CAN bus</a> protocol, a robust and prevalent vehicle communication standard used in most modern vehicles.
This tutorial will show how we can both leverage this protocol and abstract it into the Viam base interface so that the rover can then be controlled securely from anywhere with the programming language of your choice.

## Requirements

{{% alert title="Note" color="note"%}}
Even if you don't have an Intermode rover, many of the other concepts presented here are still relevant to other robotic project(s).  
While this tutorial can be followed verbatim for the Intermode rover, much of it can be applied to other [base](/components/base/), **CAN bus**, or [modular resource](/product-overviews/extending-viam/modular-resources/)-based projects.
{{% /alert %}}

### Hardware

The tutorial uses the following hardware:

* <a href="https://a.co/d/bxEdcAT" target="_blank">Raspberry Pi with microSD card</a>, with viam-server installed per [our Raspberry Pi setup guide](https://docs.viam.com/getting-started/rpi-setup/).
* <a href="https://www.intermode.io/" target="_blank">An Intermode rover</a>
* <a href="https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/" target="_blank">PiCAN 2 - Canbus interface for Raspberry Pi</a>
* <a href="https://www.amazon.com/dp/B01M03288J" target="_blank">12V to 5V Buck Converter</a>
* <a href="https://www.amazon.com/Type-C-Cable-10inch-22AWG-Pigtail/dp/B09C7SLHFP" target="_blank">USB-C Male Plug to  Pigtail Cable</a>

## Initial Setup

### Raspberry Pi software setup

Before proceeding, [set up `viam-server` on your Raspberry Pi ](/installation/rpi-setup/) and configure a (for now) empty robot configuration.

Next, install the PiCAN 2 driver software <a href="https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/" target="_blank">following these instructions</a>.

### Hardware

Power your Raspberry Pi off and attach the PiCAN 2 by aligning the 40 way connector and fitting it to the top of the Pi using a spacer and a screw as per <a href="https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/" target="_blank">the instructions</a>.

<img src="../img/intermode/can_terminal_conn.png"  style="float:right;margin-right:12px" alt="PiCAN Terminal Wiring." title="PiCAN Terminal Wiring." width="400" />

Next, with the Intermode rover powered down, use the Intermode provided 6-wire amphenol connector to wire into 4 screw terminal on PiCAN bus.
Connect one of the 12v wires (red) to the +12V terminal, one of the ground wires (black) to the GND terminal, the CAN low wire (blue) to the CAN_L terminal, and the CAN high wire (white) to the CAN_H terminal.
You will have two remaining wires (12v and ground).

Now, connect the remaining two wires to the + (red) and - (black) **input** terminals on your buck converter.
Attach the USB-C adaptor to the **output** of your buck converter, and plug this into your Pi.
Powering up the Intermode should now power up your Pi and allow it to communicate with the rover via CAN bus!

<img src="../img/intermode/intermode_wiring.jpg"  style="margin-right:12px" alt="Intermode, Pi Wiring." title="Intermode, Pi Wiring." width="800" />

### Software for the Intermode base modular resource

We've created a github repository with a working modular resource implementation example, which is referenced in this tutorial and can be <a href="https://github.com/viam-labs/tutorial-intermode" target="_blank">found here</a>.

## Understanding the Intermode base modular resource

Viam includes [APIs](/product-overviews/extending-viam/modular-resources/#apis) for a number of common component types within viam-server.
The Viam component that exposes the interfaces for controlling a mobile robot's movements is the [base](/components/base) component.

We'll walk through how we leveraged this API interface using code found in the <a href="https://github.com/viam-labs/tutorial-intermode" target="_blank">tutorial repository</a>.  If you are interested only in how to configure this modular resource code with your robot, you can skip to [using the intermode base resource](#use-the-intermode-base-modular-resource)

### Create a custom model using the Viam RDK base API

For the Intermode rover, we'll want to conform to the base [API](/product-overviews/extending-viam/modular-resources/#apis), but create a new [model](/product-overviews/extending-viam/modular-resources/models) with its own implementation of each method.
Both the **API** and **model** are colon-separated triplets where the first element is a namespace.
Since we are conforming to an existing Viam API for [base](/components/base), the [API](/product-overviews/extending-viam/modular-resources/#apis) we'll use is:
**rdk:component:base**

We're creating this base model for tutorial purposes only, and will implement only partial functionality for demonstration purposes.
We'll use the namespace "viamlabs", an (arbitrary) model family called "tutorial" and lastly, we'll select a straight forward model name of "intermode". So our complete triplet is:
**viamlabs:tutorial:intermode**

The <a href="https://github.com/viam-labs/tutorial-intermode" target="_blank">module.go code</a> found in our tutorial's github repository creates this model and registers the component instance.  The *Subtype* of a resource contains its API triplet, so by using **base.Subtype** (see line 6 below) we are registering our new model with the *API* from the RDK's built-in base component(rdk:component:base).

```go
// namespace, model family, model
var model = resource.NewModel("viamlabs", "tutorial", "intermode")

func init() {
    registry.RegisterComponent(
        base.Subtype, // the "base" API: "rdk:component:base"
        model,
        registry.Component{Constructor: func(
            ctx context.Context,
            deps registry.Dependencies,
            config config.Component,
            logger golog.Logger,
        ) (interface{}, error) {
            return newBase(config.Name, logger) // note: newBase() is not shown in this tutorial
        }})
}

func main() {
    goutils.ContextualMain(mainWithArgs, golog.NewDevelopmentLogger("intermodeBaseModule"))
}

func mainWithArgs(ctx context.Context, args []string, logger golog.Logger) (err error) {
    modalModule, err := module.NewModuleFromArgs(ctx, logger)

    if err != nil {
        return err
    }
    modalModule.AddModelFromRegistry(ctx, base.Subtype, model)

    err = modalModule.Start(ctx)
    defer modalModule.Close(ctx)

    if err != nil {
        return err
    }
    <-ctx.Done()
    return nil
}
```

### Implement base methods

Now that the modular resource code has registered the API it is using and its custom model, we can implement any number of methods provided by the base API.
Since the Intermode rover's commands are in the CAN bus format, we'll need our modular resource code to translate any commands sent via the base API, like *SetPower*, *SetVelocity*, or *Stop* to <a href="https://en.wikipedia.org/wiki/CAN_bus#Frames" target="_blank">CAN bus frames</a>.
Intermode provides documentation on how its <a href="https://github.com/viam-labs/tutorial-intermode/blob/main/can_interface.pdf" target="_blank">CAN frames</a> are formatted.

This tutorial is not meant to line-by-line explain what this translation code does, but instead we'll point out the important details, and beyond that, you can follow the code implementation in the <a href="https://github.com/viam-labs/tutorial-intermode/blob/main/intermode-base/module.go" target="_blank">tutorial code</a>.

1. The SetPower command implements the SetPower interface from the *rdk:component:base* API
2. The parameters sent to SetPower are formatted as a *driveCommand*
3. The *driveCommand* is converted to a CAN frame, and set as the next command
4. *publishThread* runs a loop continuously, sending the current command every 10ms (the Intermode base will otherwise time out)

``` go
// this struct describes intermode base drive commands
type driveCommand struct {
    Accelerator   float64
    Brake         float64
    SteeringAngle float64
    Gear          byte
    SteerMode     byte
}

func (base *interModeBase) setNextCommand(ctx context.Context, cmd modalCommand) error {
    if err := ctx.Err(); err != nil {
        return err
    }
    select {
    case <-ctx.Done():
        return ctx.Err()
    case base.nextCommandCh <- cmd.toFrame(base.logger):
    }
    return nil
}

// toFrame convert the drive command to a CANBUS data frame.
func (cmd *driveCommand) toFrame(logger golog.Logger) canbus.Frame {
    frame := canbus.Frame{
        ID:   driveId,
        Data: make([]byte, 0, 8),
        Kind: canbus.SFF,
    }
    frame.Data = append(frame.Data, calculateAccelAndBrakeBytes(cmd.Accelerator)...)
    frame.Data = append(frame.Data, calculateSteeringAngleBytes(cmd.SteeringAngle)...)

    if cmd.Accelerator < 0 {
        cmd.Gear = gears[gearReverse]
    }
    frame.Data = append(frame.Data, cmd.Gear, cmd.SteerMode)

    logger.Debugw("frame", "data", frame.Data)

    return frame
}

func (base *interModeBase) SetPower(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    return base.setNextCommand(ctx, &driveCommand{
        Accelerator:   linear.Y * 100,  // the base API provides linear.Y between -1 (full reverse) and 1 (full forward)
        Brake:         0,
        SteeringAngle: angular.Z * 100, // the base API provides angular.Z between -1 (full left) and 1 (full right)
        Gear:          gears[gearDrive],
        SteerMode:     steerModes[steerModeFourWheelDrive],
    })
}
```

Now, the intermode base can receive and execute *SetPower* commands using the same interface you'd use to send *SetPower* commands to any rover that is Viam-controlled.

### Leaving some methods unimplemented

In some cases, you may not want to implement specific methods provided by the resource type's [API](/product-overviews/extending-viam/modular-resources/#apis).
For example, some hardware may not support specific functionality.
When you want to leave a method unimplemented you must provide that method, and return an appropriate error message.

In this example, we'll leave the *IsMoving* method unimplemented.

```go
func (base *interModeBase) IsMoving(ctx context.Context) (bool, error) {
    return false, utils.NewUnimplementedInterfaceError((*interModeBase)(nil), "intermodeBase does not yet support IsMoving()")
}
```

## Use the Intermode base modular resource

### Installing the modular resource

Our modular resource code leverages libraries (specifically a <a href="https://github.com/go-daq/canbus" target="_blank">Can bus library</a>) that can run on Linux and interface with the PiCAN socket.
We'll also be configuring RDK to load the module (after it is compiled.)
Therefore, we'll need to make the modular resource code available on our Raspberry Pi.
If you have git installed on your pi, this is as simple as running:

``` sh
git clone https://github.com/viam-labs/tutorial-intermode
```

in the directory you'd like to have the modular resource code run from.
If you don't have git installed on your pi, you'll need to first run:

``` sh
sudo apt install git
```

### Configuring the Intermode base resource

If needed, first create a new robot in the [Viam app](/getting-started/app-usage/) and follow instructions in the setup tab to ensure the configuration can be read by the robot from the cloud.

In order to drive the Intermode base with Viam, you'll need add it to the robot configuration.
You will specify where viam-server can find the module, and then configure a modular component instance for the Intermode base.

In this example, we've cloned the git tutorial repo to */home/me/tutorial-intermode/*.
Change this to the correct location in *executable_path* when adding the module to your robot configuration.

``` json
{
  "modules": [
    {
      "name": "intermode-base",
      "executable_path": "/home/me/tutorial-intermode/intermode-base/run.sh"
    }
  ],
    "components": [
        {
        "type": "component",
        "name": "base",
        "model": "viamlabs:tutorial:intermode",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": []
        }
    ]
}
```

More details about modules and how they work can be found in the [modular resources documentation](/product-overviews/extending-viam/modular-resources/#adding-a-module-to-your-robot-configuration).

### Control the rover

Once you save this configuration, you see a *base* card in the robot's *control* tab and can drive the rover from there. Be careful, the Intermode is a large and powerful rover - make sure you have the shutoff key in hand for emergencies and make sure you have enough space for the rover to move.

If you do not see the base card in the *control* tab, check the *logs* tab for possible setup or configuration errors.

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, head over to the <a href="https://viamrobotics.slack.com/" target="_blank">Viam Community Slack</a>.
