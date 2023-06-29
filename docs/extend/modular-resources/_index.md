---
title: "Create custom components and services"
linkTitle: "Modular Resources"
image: "/tutorials/img/intermode/rover_outside.png"
imageAlt: "An intermode rover pictured outdoors."
images: ["/tutorials/img/intermode/rover_outside.png"]
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
no_list: true
aliases:
    - "/program/extend/modular-resources/"
---

The Viam module system allows you to integrate custom [resources](/appendix/glossary/#term-resource) ([components](/components/) and [services](/services/)) into any robot running on Viam.

With modular resources, you can:

- Create new models of built-in component or service types
- Create brand new resource types

`viam-server` [manages](#modular-resource-management) modular resources configured on your robot like resources that are already built into the [Robot Development Kit (RDK)](/internals/rdk/).

Two key concepts exist across all Viam resources (both built-in and modular) to facilitate this: [*APIs*](#apis) and [*models*](#models).

## Key concepts

### APIs

Every Viam {{< glossary_tooltip term_id="resource" text="resource" >}} exposes an [Application Programming Interface (API)](https://en.wikipedia.org/wiki/API).
This can be understood as a description of how you can interact with that resource.
Each API is described through [protocol buffers](https://developers.google.com/protocol-buffers).
Viam SDKs [expose these APIs](/internals/robot-to-robot-comms/).

Each Viam resource's API is uniquely namespaced as a colon-delimited-triplet in the form of `namespace:type:subtype`.

For example:

- The API of built-in component [camera](/components/camera/) is `rdk:component:camera`, which exposes methods such as `GetImage()`.
- The API of built-in service [vision](/services/vision/) is `rdk:service:vision`, which exposes methods such as `GetDetectionsFromCamera()`.

{{% alert title="Note" color="note" %}}
You can see built-in Viam resource APIs in the [Viam GitHub](https://github.com/viamrobotics/api).
{{% /alert %}}

### Models

A *model* describes a specific implementation of a resource that implements (speaks) its API.
Models allow you to control different versions of resource types with a consistent interface.

For example:

Some DC motors use just [GPIO](/components/board/), while other DC motors use serial protocols like [SPI bus](/components/board/#spis).
Regardless, you can power any motor model that implements the *rdk:component:motor* API with the `SetPower()` method.

Models are also uniquely namespaced as colon-delimited-triplets in the form of `namespace:family:name`.

For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

A common use-case for modular resources is to create a new model using an existing Viam API.
However, you can also create and expose new API types using modular resources.

## Use a modular resource with your robot

If you are using an existing modular resource, you can skip to [Save the executable](#make-sure-viam-server-can-access-your-executable).
If you are creating your own modular resource, follow these steps:

1. [Code a module in Go or Python](#code-your-module), using the module support libraries provided by the Python or Go [Viam SDK](/program/apis/).
2. [Compile or package the module code](#make-your-module-executable) into an executable.
3. [Save the executable](#make-sure-viam-server-can-access-your-executable) in a location your `viam-server` instance can access.
4. [Add a **module**](#configure-your-module) referencing this executable to the configuration of your robot.
5. [Add a new component or service](#configure-your-modular-resource) referencing the custom resource provided by the configured **module** to the configuration of your robot.

{{% alert title="Modules vs. modular resources" color="tip" %}}

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

### Code your module

Code a module in the Go or Python programming languages with [Viam's SDKs](/program/apis/) that does the following:

{{< tabs >}}
{{% tab name="Define a New Model of a Built-In Resource Type" %}}

1. Code a new resource model implementing all methods the Viam RDK requires in the API definition of its built-in type (ex. `rdk:component:base`).
2. Code a main program to serve as the module itself, using the module helpers provided by your chosen SDK.
3. Import the API and models into the main program, and register them with the module helper SDK.
4. Compile and/or package your program.

{{% /tab %}}
{{% tab name="Define a New Type of Resource" %}}

1. Define the messages and methods of the new API in [protobuf](https://github.com/protocolbuffers/protobuf), then generate code in Python or Go and use the generated code to implement the higher level server and client functions required.
2. Code at least one model of this new resource.
Make sure to implement every method required in your API definition.
3. Code a main program to serve as the module itself, using the module helpers provided by your chosen SDK.
4. Import the API and models into the main program, and register them with the module helper SDK.
5. Compile and/or package your program.

{{% /tab %}}
{{% /tabs %}}

For example:

{{%expand "Click to view example code from a module implementing a new model of the base component built-in resource" %}}

{{< tabs name="Base Model Modules" >}}
{{% tab name="Go" %}}

This example module code is adapted from the full demo module available on the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go), and creates a singular modular resource implementing Viam's built-in Base API (rdk:service:base).
See [Base API Methods](/components/base/#api) and [Motor API Methods](/components/motor/#api) for more information.

``` go {class="line-numbers linkable-line-numbers"}
// Package mybase implements a base that only supports SetPower (basic forward/back/turn controls), IsMoving (check if in motion), and Stop (stop all motion).
// It extends the built-in resource type Base and implements methods to handle resource construction, attribute configuration, and reconfiguration.

package mybase

import (
    "context"
    "fmt"
    "math"

    "github.com/edaniels/golog"
    "github.com/golang/geo/r3"
    "github.com/pkg/errors"
    "go.uber.org/multierr"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/components/generic"
    "go.viam.com/rdk/components/motor"
    "go.viam.com/rdk/config"
    "go.viam.com/rdk/registry"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/utils"
)

// Here is where we define our new model's colon-delimited-triplet (acme:demo:mybase)
// acme = namespace, demo = family, mybase = model name.
var (
    Model            = resource.NewModel("acme", "demo", "mybase")
    errUnimplemented = errors.New("unimplemented")
)

// Constructor
func newBase(ctx context.Context, deps registry.Dependencies, config config.Component, logger golog.Logger) (interface{}, error) {
    b := &MyBase{logger: logger}
    err := b.Reconfigure(config, deps)
    return b, err
}

// Defines what the JSON configuration should look like
type MyBaseConfig struct {
    LeftMotor  string `json:"motorL"`
    RightMotor string `json:"motorR"`
}

// Validates JSON configuration
func (cfg *MyBaseConfig) Validate(path string) ([]string, error) {
    if cfg.LeftMotor == "" {
        return nil, fmt.Errorf(`expected "motorL" attribute for mybase %q`, path)
    }
    if cfg.RightMotor == "" {
        return nil, fmt.Errorf(`expected "motorR" attribute for mybase %q`, path)
    }

    return []string{cfg.LeftMotor, cfg.RightMotor}, nil
}

// Handles attribute reconfiguration
func (base *MyBase) Reconfigure(cfg config.Component, deps registry.Dependencies) error {
    base.left = nil
    base.right = nil
    baseConfig, ok := cfg.ConvertedAttributes.(*MyBaseConfig)
    if !ok {
        return utils.NewUnexpectedTypeError(baseConfig, cfg.ConvertedAttributes)
    }
    var err error

    base.left, err = motor.FromDependencies(deps, baseConfig.LeftMotor)
    if err != nil {
        return errors.Wrapf(err, "unable to get motor %v for mybase", baseConfig.LeftMotor)
    }

    base.right, err = motor.FromDependencies(deps, baseConfig.RightMotor)
    if err != nil {
        return errors.Wrapf(err, "unable to get motor %v for mybase", baseConfig.RightMotor)
    }

    // Stopping motors at reconfiguration
    return multierr.Combine(base.left.Stop(context.Background(), nil), base.right.Stop(context.Background(), nil))
}

// Attributes of the base
type MyBase struct {
    generic.Echo
    left   motor.Motor
    right  motor.Motor
    logger golog.Logger
}

// Implement the methods the Viam RDK defines for the base API (rdk:component:base)

// MoveStraight: unimplemented
func (base *MyBase) MoveStraight(ctx context.Context, distanceMm int, mmPerSec float64, extra map[string]interface{}) error {
    return errUnimplemented
}

// Spin: unimplemented
func (base *MyBase) Spin(ctx context.Context, angleDeg, degsPerSec float64, extra map[string]interface{}) error {
    return errUnimplemented
}

// SetVelocity: unimplemented
func (base *MyBase) SetVelocity(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    return errUnimplemented
}

// SetPower: sets the linear and angular velocity of the left and right motors on the base
func (base *MyBase) SetPower(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    // stop the base if absolute value of linear and angular velocity is less than .01
    if math.Abs(linear.Y) < 0.01 && math.Abs(angular.Z) < 0.01 {
        return base.Stop(ctx, extra)
    }

    // use linear and angular velocity to calculate percentage of max power to pass to SetPower for left & right motors
    sum := math.Abs(linear.Y) + math.Abs(angular.Z)
    err1 := base.left.SetPower(ctx, (linear.Y-angular.Z)/sum, extra)
    err2 := base.right.SetPower(ctx, (linear.Y+angular.Z)/sum, extra)
    return multierr.Combine(err1, err2)
}

// Stop: stops the base from moving by stopping both motors
func (base *MyBase) Stop(ctx context.Context, extra map[string]interface{}) error {
    base.logger.Debug("Stop")

    err1 := base.left.Stop(ctx, extra)
    err2 := base.right.Stop(ctx, extra)

    return multierr.Combine(err1, err2)
}

// IsMoving: checks if either motor on the base is moving with motors' IsPowered
func (base *MyBase) IsMoving(ctx context.Context) (bool, error) {
    for _, m := range []motor.Motor{base.left, base.right} {
        isMoving, _, err := m.IsPowered(ctx, nil)
        if err != nil {
            return false, err
        }
        if isMoving {
            return true, err
        }
    }
    return false, nil
}

// Stop the base from moving when closing a client's connection to the base
func (base *MyBase) Close(ctx context.Context) error {
    return base.Stop(ctx, nil)
}

// Register the component with the Go SDK
func init() {
    registry.RegisterComponent(base.Subtype, Model, registry.Component{Constructor: newBase})

    // VALIDATION: Uses RegisterComponentAttributeMapConverter to register a custom configuration struct that has a Validate(string) ([]string, error) method.
    // The Validate method will automatically be called in RDK's module manager to validate MyBase's configuration and register implicit dependencies.
    config.RegisterComponentAttributeMapConverter(
        base.Subtype,
        Model,
        func(attributes config.AttributeMap) (interface{}, error) {
            var conf MyBaseConfig
            return config.TransformAttributeMapToStruct(&conf, attributes)
        },
        &MyBaseConfig{})
}
```

{{% /tab %}}
{{% tab name="Python" %}}

This example module code is adapted from the full base demo module available on the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go), and creates a singular modular resource implementing Viam's built-in Base API (rdk:service:base).
See [Base API Methods](/components/base/#api) and [Motor API Methods](/components/motor/#api) for more information.

<file>my_base.py</file>

``` python {class="line-numbers linkable-line-numbers"}
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily

from viam.components.base import Base
from viam.components.motor import Motor

class MyBase(Base, Reconfigurable):
    """
    MyBase implements a base that only supports set_power (basic forward/back/turn controls) is_moving (check if in motion), and stop (stop all motion).

    It inherits from the built-in resource type Base and conforms to the ``Reconfigurable`` protocol, which signifies that this component can be reconfigured.

    Additionally, it specifies a constructor function ``MyBase.new_base`` which confirms to the ``resource.types.ResourceCreator`` type required for all models.
    """

    # Here is where we define our new model's colon-delimited-triplet (acme:demo:mybase)
    # acme = namespace, demo = family, mybase = model name.
    MODEL: ClassVar[Model] = Model(ModelFamily("acme", "demo"), "mybase")

    left: Motor # Left motor
    right: Motor # Right motor

    # Constructor
    @classmethod
    def new_base(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        base = cls(config.name)
        base.reconfigure(config, dependencies)
        return base

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        left_name = config.attributes.fields["motorL"].string_value
        if left_name == "":
            raise Exception("A motorL attribute is required for a MyBase component.")
        right_name= [config.attributes.fields["motorR"].string_value]
        if right_name == "":
            raise Exception("A motorR attribute is required for a MyBase component.")
        return [left_name, right_name]

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        left_name = config.attributes.fields["motorL"].string_value
        right_name = config.attributes.fields["motorR"].string_value

        left_motor = dependencies[Motor.get_resource_name(left_name)]
        right_motor = dependencies[Motor.get_resource_name(right_name)]

        self.left = cast(Motor, left_motor)
        self.right = cast(Motor, right_motor)

    """ Implement the methods the Viam RDK defines for the base API (rdk:component:base) """

    # move_straight: unimplemented
    async def move_straight(self, distance: int, velocity: float, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # spin: unimplemented
    async def spin(self, angle: float, velocity: float, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # set_velocity: unimplemented
    async def set_velocity( self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        pass

    # set_power: set the linear and angular velocity of the left and right motors on the base
    async def set_power(self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):

        # stop the base if absolute value of linear and angular velocity is less than .01
        if abs(linear.y) < 0.01 and abs(angular.z) < 0.01:
            return self.stop(extra=extra, timeout=timeout)

        # use linear and angular velocity to calculate percentage of max power to pass to SetPower for left & right motors
        sum = abs(linear.y) + abs(angular.z)

        self.left.set_power(power=((linear.y - angular.z) / sum), extra=extra, timeout=timeout)
        self.right.set_power(power=((linear.y + angular.z) / sum), extra=extra, timeout=timeout)

    # stop: stop the base from moving by stopping both motors
    async def stop(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        self.left.stop(extra=extra, timeout=timeout)
        self.right.stop(extra=extra, timeout=timeout)

    # is_moving: check if either motor on the base is moving with motors' is_powered
    async def is_moving(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> bool:
        return self.left.is_powered(extra=extra, timeout=timeout)[0] or self.right.is_powered(extra=extra, timeout=timeout)[0]
```

<file>`__init.py__`</file>

``` python {class="line-numbers linkable-line-numbers"}
"""
This file registers the MyBase model with the Python SDK.
"""

from viam.components.motor import *
from viam.components.base import Base
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .my_base import MyBase

Registry.register_resource_creator(Base.SUBTYPE, MyBase.MODEL, ResourceCreatorRegistration(MyBase.new_base, MyBase.validate_config))
```

<file>main.py</file>

``` python {class="line-numbers linkable-line-numbers"}
import asyncio
import sys

from viam.components.base import Base
from viam.module.module import Module
from .my_base import MyBase

async def main(address: str):
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    Args:
        address (str): The address to serve the module on
    """
    module = Module(address)
    module.add_model_from_registry(Base.SUBTYPE, MyBase.MODEL)
    await module.start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Need socket path as command line argument")

    asyncio.run(main(sys.argv[1]))

```

{{% /tab %}}
{{< /tabs >}}

{{% /expand%}}

{{% alert title="Note" color="note" %}}

You must define all functions belonging to a built-in resource type if defining a new model.
Otherwise, the class won’t instantiate.

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

### Make your module executable

To add a module to your robot, you need to have an [executable file](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and cleanly exits when sent a termination signal.
Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

If using the Go SDK, Go will build a binary when you compile your module.

If using the Python SDK, one option is creating and save a new shell script (<file>.sh</file>) that runs your module.
For example:

``` shell
#!/bin/sh
cd `dirname $0`

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 -m <your-module-directory-name>.<main-program-filename-without-extension> $@
```

To make this shell script executable, run the following command in your terminal:

``` shell
sudo chmod +x <FILEPATH>/<FILENAME>
```

You need to ensure any dependencies for your module (including the Viam SDK) are installed, as well.
Your executable will be run by `viam-server` as root, so dependencies need to be available to the root user.

### Make sure `viam-server` can access your executable

Ensure that the code defining your module is saved where the instance of `viam-server` behind your robot can read and execute it.

For example, if you are running `viam-server` on an Raspberry Pi, you'll need to save the module on the Pi's filesystem.

Obtain the real (absolute) path to the executable file on your computer/[board's](/components/board/) filesystem by running the following command in your terminal:

``` shell
realpath <path-to-your-module-directory>/<your-module>
```

### Configure your module

To configure your new *module* on your robot, navigate to the **Config** tab of your robot's page on [the Viam app](https://app.viam.com) and click on the **Modules** subtab.

The following properties are available for modules:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
`name` | string | **Required**| Name of the module you are registering. |
`executable_path` | string | **Required**| The robot's computer's filesystem path to the module executable. |

Add these properties to your module's configuration:

{{< tabs >}}
{{% tab name="Config Builder" %}}

![Creation of a new module in the Viam app config builder.](/program/img/modular-resources/module-ui-config.png)

{{% /tab %}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "<your-module-name>",
      "executable_path": "<path-on-your-filesystem-to/your-module-directory>/<your_executable.sh>"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

### Configure your modular resource

Once you have configured a module as part of your robot configuration, you can instantiate any number of instances of a modular resource made available by that module by adding new components or services configured with your modular resources' new type or [model](#models).

The following properties are available for modular resources:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `namespace` | string | **Required** | The namespace of the [API](#apis) (the first part of the [API](#apis) triplet). |
| `type` | string | **Required** | The subtype of the [API](#apis) (the third part of the [API](#apis) triplet). |
| `name` | string | **Required** | What you want to name this instance of your modular resource. |
| `model` | string | **Required** | The [full triplet](#models) of the modular resource. |
| `depends_on` | array | Optional | The `name` of components you want to confirm are available on your robot alongside your modular resource. Usually a [board](/components/board/). |

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "namespace": "<your-module-namespace>",
      "type": "<your-resource-type>",
      "model": "<model-namespace>:<model-family-name>:<model-name>",
      "name": "<your-module-name>",
      "depends_on": [],
    }
  ],
  "modules": [ ... ] // < INSERT YOUR MODULE CONFIGURATION >
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following is an example configuration for a base modular resource implementation.
The configuration adds `acme:demo:mybase` as a modular resource from the module `my_base`.
The custom model is configured as a component with the name "my-custom-base-1" and can be interfaced with the Viam [base API](/components/base/#api):

```json {class="line-numbers linkable-line-numbers"}
{
    "components": [
        {
            "type": "board",
            "name": "main-board",
            "model": "pi"
        },
        {
        "type": "base",
        "name": "my-custom-base-1",
        "model": "acme:demo:mybase",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": [ "main-board" ]
        }
    ],
    "modules": [
    {
      "name": "my-custom-base",
      "executable_path": "/home/my_username/my_base/run.sh"
    }
  ]
}
```

{{% /tab %}}
{{% /tabs %}}

## More information

### Modular resource management

#### Dependency Management

Modular resources may depend on other built-in resources or other modular resources, and vice versa.
The Viam RDK handles dependency management.

#### Start-up

The RDK ensures that any configured modules are loaded automatically on start-up, and that configured modular resource instances are started alongside configured built-in resource instances.

#### Reconfiguration

When you change the configuration of a Viam robot, the behavior of modular resource instances versus built-in resource instances is equivalent.
This means you can add, modify, and remove a modular resource instance from a running robot as normal.

#### Shutdown

During robot shutdown, the RDK handles modular resource instances similarly to built-in resource instances - it signals them for shutdown in topological (dependency) order.

### Modular resources as remotes

[Remote](/manage/parts-and-remotes/) parts may load their own modules and provide modular resources, just as the main part can.
This means that you can compose a robot of any number of parts running in different compute locations, each containing both built-in and custom resources.

### Limitations

Custom models of the [arm](/components/arm/) component type are not yet supported, as kinematic information is not currently exposed through the arm API.

{{< cards >}}
    {{% card link="/extend/modular-resources/examples/add-rplidar-module" size="small" %}}
    {{% card link="/tutorials/custom/controlling-an-intermode-rover-canbus/" size="small" %}}
{{< /cards >}}
