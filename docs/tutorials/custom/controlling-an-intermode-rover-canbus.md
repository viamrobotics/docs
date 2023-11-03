---
title: "Control an Intermode Rover with CAN Bus and Viam"
linkTitle: "Control an Intermode Rover with Viam"
type: "docs"
tags:
  [
    "modular resources",
    "extending viam",
    "components",
    "rover",
    "base",
    "CAN bus",
    "Intermode",
  ]
description: "Integrate an Intermode rover as a modular-resource-based component with CAN bus."
image: "/tutorials/intermode/rover_outside.png"
imageAlt: "Intermode rover pictured outdoors."
images: ["/tutorials/intermode/rover_outside.png"]
authors: ["Matt Vella"]
languages: ["go"]
viamresources: ["base", "custom"]
level: "Intermediate"
date: "2023-01-22"
# updated: ""
cost: 1500
no_list: true
# SME: Matt Vella, Matt Dannenberg, James Otting
---

The Viam platform comes with a component called [base](/components/base/), which adds useful abstractions for simplified control of mobile robots.
Instead of controlling individual motors, the base component allows you to [issue commands](https://python.viam.dev/autoapi/viam/components/base/index.html#package-contents) like "move_straight", "spin", "set_velocity" and "stop".

Many robotic rovers can be controlled out-of-the-box with the Viam "wheeled" base model - simply by specifying how your motorized wheels are configured.
But what if you want to control a rover or other mobile robot that does not expose direct motor control?
This tutorial shows you how to create a {{< glossary_tooltip term_id="modular-resource" text="modular resource" >}} (custom component).
Creating a modular resouce for your robot allows you to issue commands using the same interface as you would with native Viam components. Once you have created the custom component, you can control both the Viam components and the modular resources using the [Viam SDK](/program/apis/) of your choice.

<div class="td-max-width-on-larger-screens">
{{<imgproc src="/tutorials/intermode/rover_outside.png" resize="400x" declaredimensions=true alt="Intermode rover pictured outdoors." class="alignright" style="max-width:300px">}}
</div>

While the concepts covered here are applicable to other hardware, we’ll specifically show you an example of how you can get started using Viam to control the [Intermode rover](https://www.intermode.io/).
This is a powerful pairing: **Intermode** aims to make the hardware aspects of a mobile-robot-based business simple and worry-free, while Viam simplifies the software aspects of any robotics business.

The Intermode rover uses the [CAN bus](https://en.wikipedia.org/wiki/CAN_bus) protocol, a robust and prevalent vehicle communication standard used in most modern vehicles.
This tutorial will show how we can both leverage this protocol and abstract it into the Viam base interface so that the rover can then be controlled securely from anywhere with the programming language of your choice.

## Hardware requirements

{{% alert title="Tip" color="tip"%}}
Even if you don't have an Intermode rover, many of the other concepts presented here are still relevant to other robotic projects.
While this tutorial can be followed verbatim for the Intermode rover, much of it can be applied to other [base](/components/base/), **CAN bus**, or [modular resource](/modular-resources/)-based projects.
{{% /alert %}}

The tutorial uses the following hardware:

- <a href="https://a.co/d/bxEdcAT" target="_blank">Raspberry Pi with microSD card</a>, with `viam-server` installed per [our Raspberry Pi setup guide](/installation/prepare/rpi-setup/).
- [An Intermode rover](https://www.intermode.io/)
- [PiCAN 2 - Canbus interface for Raspberry Pi](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/)
- [12V to 5V Buck Converter](https://www.amazon.com/dp/B01M03288J)
- [USB-C Male Plug to Pigtail Cable](https://www.amazon.com/Type-C-Cable-10inch-22AWG-Pigtail/dp/B09C7SLHFP)

## Initial Setup

### Raspberry Pi software setup

Before proceeding, [set up `viam-server` on your Raspberry Pi](/installation/prepare/rpi-setup/) and configure a (for now) empty robot configuration.

Next, install the PiCAN 2 driver software [following these instructions](https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/).

{{% alert title="Tip" color="tip" %}}
If you restart your Pi, you will need to bring up the CAN interface again, as the above linked instructions do not set this process up to be managed on system start.
{{% /alert %}}

### Hardware

{{% alert title="Caution" color="caution" %}}
Always disconnect devices from power before plugging, unplugging or moving wires or otherwise modifying electrical circuits.
{{% /alert %}}

Power your Raspberry Pi off and attach the PiCAN 2 by aligning the 40 way connector and fitting it to the top of the Pi [using a spacer and a screw](https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi).

<div class="td-max-width-on-larger-screens">
    {{<imgproc src="/tutorials/intermode/can_terminal_conn.png" resize="400x" declaredimensions=true alt="PiCAN Terminal Wiring." class="alignright" style="max-width:400px">}}
</div>

Next, with the Intermode rover powered down, connect the 6-wire amphenol connector that comes with the rover to the 4 screw terminal on PiCAN bus:

- Connect one of the 12V wires (red) to the +12V terminal
- Connect one of the ground wires (black) to the GND terminal
- Connect the CAN low wire (blue) to the CAN_L terminal
- Connect the CAN high wire (white) to the CAN_H terminal.

You will have two remaining wires (12V and ground).

Connect the remaining two wires to the + (red) and - (black) **input** terminals on your buck converter.
Attach the USB-C adapter wires to the **output** of your buck converter, and plug the other end of the USB-C adapter into your Pi.
You can now power up the rover, which will provide power to your Pi and allow it to communicate with the rover using CAN bus!

![Intermode, Pi Wiring.](/tutorials/intermode/intermode_wiring.jpg)

### Software for the Intermode base modular resource

Check out this [GitHub repository](https://github.com/viam-labs/tutorial-intermode) for the working modular resource implementation example which we use in this tutorial.

## A modular resource for the Intermode base

Viam includes [APIs](/program/apis/) for common component types within `viam-server`.
The Viam component that exposes the interfaces for controlling a mobile robot's movements is the [base component](/components/base/).

If you want to learn how to leverage this API to create a custom modular resource using code found in the [tutorial repository](https://github.com/viam-labs/tutorial-intermode), continue reading.
If you want to directly configure this modular resource code with your robot, skip to [using the intermode base resource](#use-the-intermode-base-modular-resource)

### Create a custom model using the Viam RDK base API

The [base](/components/base/) component exposes an API for controlling a mobile robot’s movements.
To use it for the Intermode rover, you must create a new [model](/modular-resources/key-concepts/#models) with its own implementation of each method.

Both the **API** and **model** of any Viam resource are represented as colon-separated triplets where the first element is a namespace.
Since you will conform to an existing Viam API for [base](/components/base/), the [API](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model) you will use is:
**rdk:component:base**

This base model is being created for tutorial purposes only, and will implement only partial functionality for demonstration purposes.
Therefore, use the namespace "viamlabs", an (arbitrary) repo-name called "tutorial" and lastly, a model name of "intermode".
The complete triplet is:
**viamlabs:tutorial:intermode**

The [module.go code](https://github.com/viam-labs/tutorial-intermode) creates this model and registers the component instance.
The _Subtype_ of a resource contains its API triplet, so using `base.Subtype` (see line 30 below) registers our new model with the _API_ from the RDK's built-in base component (rdk:component:base).

```go {class="line-numbers linkable-line-numbers"}
// namespace, repo-name, model
var model = resource.NewModel("viamlabs", "tutorial", "intermode")

func main() {
    goutils.ContextualMain(mainWithArgs, logger.NewDevelopmentLogger("intermodeBaseModule"))
}

func mainWithArgs(ctx context.Context, args []string, logger logger.Logger) (err error) {
    registerBase()
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

// helper function to add the base's constructor and metadata to the component registry, so that we can later construct it.
func registerBase() {
    registry.RegisterComponent(
        base.Subtype, // the "base" API: "rdk:component:base"
        model,
        registry.Component{Constructor: func(
            ctx context.Context,
            deps registry.Dependencies,
            config config.Component,
            logger logger.Logger,
        ) (interface{}, error) {
            return newBase(config.Name, logger) // note: newBase() is not shown in this tutorial
        }})
}
```

### Implement base methods

Now that the modular resource code has registered the API it is using and its custom model, you can implement any number of methods provided by the base API.
Since the Intermode rover's commands are in the CAN bus format, you need the modular resource code to translate any commands sent from the base API, like _SetPower_, _SetVelocity_, or _Stop_ to [CAN bus frames](https://en.wikipedia.org/wiki/CAN_bus#Frames).
Intermode provides documentation on how its [CAN frames](https://github.com/viam-labs/tutorial-intermode/blob/main/can_interface.pdf) are formatted.

At a high level, the [tutorial code](https://github.com/viam-labs/tutorial-intermode/blob/main/intermode-base/module.go) does the following:

1. The SetPower command implements the SetPower interface from the _rdk:component:base_ API
2. The parameters sent to SetPower are formatted as a _driveCommand_
3. The _driveCommand_ is converted to a CAN frame, and set as the next command
4. _publishThread_ runs a loop continuously, sending the current command every 10ms (the Intermode base will otherwise time out)

```go
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
func (cmd *driveCommand) toFrame(logger logger.Logger) canbus.Frame {
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

Now the intermode base can receive and execute _SetPower_ commands using the same interface you'd use to send _SetPower_ commands to any rover that is Viam-controlled.

### Leaving some methods unimplemented

In some cases, you may not want to implement specific methods provided by the resource type's [API](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model).
For example, some hardware may not support specific functionality.
When you want to leave a method unimplemented you must still create that method, but return an appropriate error message.

In this tutorial, you will leave the _IsMoving_ method unimplemented (for illustrative purposes).

```go {class="line-numbers linkable-line-numbers"}
func (base *interModeBase) IsMoving(ctx context.Context) (bool, error) {
    return false, errors.New("IsMoving(): unimplemented")
}
```

## Use the Intermode base modular resource

### Copy the modular resource binary

This tutorial's modular resource code leverages libraries (specifically a [CAN bus library](https://github.com/go-daq/canbus)) that run on Linux and interface with the PiCAN socket on your Raspberry Pi.
The tutorial repository includes a compiled binary that is ready to run on 64-bit [Raspberry Pi OS](https://www.raspberrypi.com/software/).
If you make changes to the tutorial code, you'll need to re-compile to create a new binary.

To run the modular resource, first copy the module binary to your Raspberry Pi.
If you have git installed on your Pi, this is as simple as running the following command in the directory for your modular resource code:

```sh {class="command-line" data-prompt="$"}
git clone https://github.com/viam-labs/tutorial-intermode
```

If you don't have git installed on your Pi, you'll need to first run:

```sh {class="command-line" data-prompt="$"}
sudo apt install git
```

### Configure the Intermode base resource

If you have not already, first create a new robot in the [Viam app](https://app.viam.com/) and follow the instructions in the **Setup** tab to connect the robot to the cloud.

In order to drive the Intermode base with Viam, you need to add it to the robot configuration.
You will specify where `viam-server` can find the module, and then configure a modular component instance for the Intermode base.

In this example, we've cloned the git tutorial repo to `/home/me/tutorial-intermode/`.
Change this to the correct location in `executable_path` when adding the module to your robot configuration.

```json
{
  "modules": [
    {
      "name": "intermode-base",
      "executable_path": "/home/me/tutorial-intermode/intermode-base/intermode-model"
    }
  ],
  "components": [
    {
      "type": "base",
      "name": "base",
      "model": "viamlabs:tutorial:intermode",
      "namespace": "rdk",
      "attributes": {},
      "depends_on": []
    }
  ]
}
```

More details about modules and how they work can be found in the [modular resources documentation](/modular-resources/).

### Control the rover

Once you save this configuration, you see a _base_ card in the robot's **Control** tab and can drive the rover from there.
Be careful, the Intermode is a large and powerful rover - make sure you have the shutoff key in hand for emergencies and make sure you have enough space for the rover to move.

If you do not see the base card in the **Control** tab, check the **Logs** tab for possible setup or configuration errors.

{{< snippet "social.md" >}}
