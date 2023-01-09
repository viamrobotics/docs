---
title: "Controlling an Intermode Rover with CAN bus and Viam"
linkTitle: "Controlling an Intermode Rover with CAN bus"
weight: 60
type: "docs"
tags: ["modular resources", "extending viam", "components", "base", "CAN bus"]
description: "Integrate an Intermode rover as a modular resource base component via CAN bus"
# SME: Matt Vella, Matt Dannenberg, James Otting
---

## Introduction

The Viam platform comes with a component called [base](/components/base/), which adds some very useful abstractions for simplified control of mobile robots.
Instead of controlling individual motors, the base component allows you to [do things](https://python.viam.dev/autoapi/viam/components/base/index.html#package-contents”) like “drive straight”, “spin”, “set velocity” and “stop”.  

Many robotic rovers can be controlled out-of-the-box with the Viam **wheeled** base model - simply by specifying how your motorized wheels are configured.
But what if you want to control a rover or other mobile robot that does not expose direct motor control?
This tutorial will show you how to create a [modular resource](/product-overviews/extending-viam/modular-resources/) (custom component), which can then be controlled seamlessly with the rest of your robot (sensors, etc) through the [Viam SDK](/product-overviews/sdk-as-client/) of your choice.

<img src="../img/intermode/rover_outside.png"  style="float:left;margin-right:12px" alt="Intermode rover pictured outdoors." title="Intermode rover pictured outdoors." width="400" />

While the concepts covered here are applicable to other hardware, we’ll specifically be showing you how to use Viam to control the <a href="https://www.intermode.io/" target="_blank">Intermode rover</a>.
This is a powerful pairing: **Intermode** aims to make the hardware aspects of a mobile robot-based business simple and worry-free, while Viam simplifies the software aspects of any robotics business.

The Intermode rover uses the [CAN bus](https://en.wikipedia.org/wiki/CAN_bus) protocol, a robust and prevalent vehicle communication standard (in fact, probably most vehicles you’ve ever been in use it!).
This tutorial will show how we can both leverage this protocol and abstract it into the Viam base interface so that the rover can then be controlled securely from anywhere with the programming language of your choice.

## What You’ll Need for This Tutorial

{{% alert title="Note" color="note"%}}
Even if you are not in possession of an Intermode rover, many of the other concepts presented here may be relevant to your robotic project(s).  
While this tutorial can be followed verbatim for the Intermode rover, much of it can be applied to other [base](/components/base/), **CAN bus**, or [modular resource](/product-overviews/extending-viam/modular-resources/)-based projects.
{{% /alert %}}

### Hardware

We used the following hardware to complete this project:

* [Raspberry Pi with microSD card](https://a.co/d/bxEdcAT), with viam-server installed per [our Raspberry Pi setup guide](https://docs.viam.com/getting-started/rpi-setup/).
* [An Intermode rover](https://www.intermode.io/)
* [PiCAN 2 - Canbus interface for Raspberry Pi](https://copperhilltech.com/pican-2-can-bus-interface-for-raspberry-pi/)
* [12V to 5V Buck Converter](https://www.amazon.com/dp/B01M03288J)
* [USB-C Male Plug to  Pigtail Cable](https://www.amazon.com/Type-C-Cable-10inch-22AWG-Pigtail/dp/B09C7SLHFP)

### Software for this tutorial

We've created a github repository with a working modular resource implementation example, which is referenced in this tutorial and can be [found here](https://github.com/viam-labs/tutorial-intermode).

## Initial Setup

### Raspberry Pi software setup

You'll want to first [follow these instructions](https://docs.viam.com/installation/rpi-setup/) to set up Viam Server on your Raspberry Pi and configure (for now) an empty robot configuration.

Next, you'll install the PiCAN 2 driver software [following these instructions](https://copperhilltech.com/blog/pican2-pican3-and-picanm-driver-installation-for-raspberry-pi/)

### Hardware

Now, power your Raspberry Pi off and attach the PiCAN 2 by aligning the 40 way connector and fitting to the top of the Pi using a spacer and screw as per the instructions [here](https://copperhilltech.com/pican2-controller-area-network-can-interface-for-raspberry-pi/).

<img src="../img/intermode/can_terminal_conn.png"  style="float:right;margin-right:12px" alt="PiCAN Terminal Wiring." title="PiCAN Terminal Wiring." width="400" />

Next, with the Intermode rover powered down, use the Intermode provided 6-wire amphenol connector to wire into 4 screw terminal on PiCAN bus.
Connect one of the 12v wires (red) to the +12V terminal, one of the ground wires (black) to the GND terminal, the CAN low wire (blue) to the CAN_L terminal, and the CAN high wire (white) to the CAN_H terminal.
You will have two remaining wires (12v and ground).

Now, connect the remaining two wires to the + (red) and - (black) **input** terminals on your buck converter.  Now, attach the USB-C adaptor to the **output** of your buck converter, and plug this into your Pi.  Powering up the Intermode should now power up your Pi and allow it to communicate with the rover via CAN bus!

<img src="../img/intermode/intermode_wiring.jpg"  style="margin-right:12px" alt="Intermode, Pi Wiring." title="Intermode, Pi Wiring." width="800" />


## Understanding the Intermode base resource 

Viam includes API interfaces for a number of common components within Viam Server (otherwise known as the RDK - Robot Development Kit).
The Viam component that exposes the interfaces for controlling a mobile robot's movements is the [base](/components/base) component.

### Using the Viam RDK base API with a custom model
For the Intermode rover , we'll want to conform to the base [API](/product-overviews/extending-viam/modular-resources/#apis) interface, but create a new [model](/product-overviews/extending-viam/modular-resources/models) with its own implementation of each method.
Both the **API** interface and **model** are namespaced as triplets in Viam.
Since we are conforming to an existing Viam API for [base](/components/base), the [API](/product-overviews/extending-viam/modular-resources/#apis)  namespace we'll use is: 

_rdk:component:base_

We're creating this base model for tutorial purposes only, and will implement only partial functionality for demonstration purposes.  Therefore, we'll use the following [model](/product-overviews/extending-viam/modular-resources/models) namespace:

_viamlabs:tutorial:intermode_

The [module.go code](https://github.com/viam-labs/tutorial-intermode/blob/main/intermode-base/module.go) found in our tutorial's github repository creates this model and registers the component instance.  Note that by using __base.Subtype__, we are registering it with the *API* from the RDK's built-in base component.

```go
var model = resource.NewModel("viamlabs", "tutorial", "intermode")

func init() {
	registry.RegisterComponent(
		base.Subtype,
		model,
		registry.Component{Constructor: func(
			ctx context.Context,
			deps registry.Dependencies,
			config config.Component,
			logger golog.Logger,
		) (interface{}, error) {
			return newBase(config.Name, logger)
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

### Implementing base methods

Now that the modular resource code has registered the API it is using and it's custom model, we can implement any number of methods provided by the base API.
Since the Intermode rover's commands are in the CAN bus format, we'll need our modular resource code to translate any commands sent via the base API, like *SetPower*, *SetVelocity*, or *Stop* to [CAN bus frames](https://en.wikipedia.org/wiki/CAN_bus#Frames).
Intermode provides documentation on how [its CAN frames](https://github.com/viam-labs/tutorial-intermode/blob/main/can_interface.pdf) are formatted.

This tutorial is not meant to line-by-line explain what this translation code does, but instead we'll point out the important details, and beyond that, you can follow the code implementation in the [tutorial code](https://github.com/viam-labs/tutorial-intermode/blob/main/intermode-base/module.go).

1. The SetPower command implements the SetPower interface from the _rdk:component:base_ API
2. The parameters sent to SetPower are formatted as a *driveCommand*
3. The *driveCommand* is converted to a CAN frame, and set as the next command

```
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
		Accelerator:   linear.Y * 100,
		Brake:         0,
		SteeringAngle: angular.Z * 100,
		Gear:          gears[gearDrive],
		SteerMode:     steerModes[steerModeFourWheelDrive],
	})
}
```

Now, the intermode base can receive and execute *SetPower* commands using the same interface you'd use to send *SetPower* commands to any rover that is Viam-controlled.

### Installing the modular resource

Our modular resource code leverages libraries (specifically a [Can bus library](https://github.com/go-daq/canbus)) that can run on Linux and interface with the PiCAN socket.
We'll also be registering the modular resource with the RDK.
Therefore, we'll need to make the modular resource code available on our Raspberry Pi.
If you have git installed on your pi, this is as simple as running:

```
git clone https://github.com/viam-labs/tutorial-intermode
```

in the directory you'd like to have the modular resource code run from.
If you don't have git installed on your pi, you'll need to first run:

```
sudo apt install git
```

### Configuring the Intermode base resource

If needed, first create a new robot in the [Viam app](/getting-started/app-usage/) and follow instructions in the setup tab to ensure the configuration can be read by the robot from the cloud.

In order to drive the Intermode base with Viam, you'll need add it to the robot configuration.
Details on how this works can be found in the [modular resources documentation](/product-overviews/extending-viam/modular-resources/#adding-a-module-to-your-robot-configuration).
What's important is that we tell RDK where to find the modular resource, and then configure a component instance for the Intermode base.

In this example, we've cloned the git tutorial repo to */home/me/tutorial-intermode/*.
Change this to the correct location in *executable_path* when adding the module configuration.

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

### Controlling the rover
Once we've saved this configuration, you should see a *base* card in the robot's *control* tab and can drive the rover from there!  Be careful, the Intermode is a large and powerful rover - make sure you have the space to avoid obstacles.

If you do not see the base card in the *control* tab, look in the *logs* tab for possible setup or configuration errors.

If you have any issues or if you want to connect with other developers learning how to build robots with Viam, head over to the [Viam Community Slack](https://viamrobotics.slack.com/).