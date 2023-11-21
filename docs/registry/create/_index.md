---
title: "Code your own modules to create modular resources"
linkTitle: "Create"
weight: 20
type: "docs"
tags:
  [
    "server",
    "rdk",
    "extending viam",
    "modular resources",
    "components",
    "services",
  ]
description: "Use the Viam module system to implement modular resources that can be included in any Viam-powered machine."
aliases:
  - "/extend/modular-resources/create/"
  - "/modular-resources/create/"
no_list: true
---

Viam provides built-in support for a variety of different {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}}, but you can also add support for unsupported resources by creating a module.
A _module_ provides one or more {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}}, which add support for {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="type" text="types" >}} or {{< glossary_tooltip term_id="model" text="models" >}} that are not built into Viam.

You can browse existing modules in the [Viam Registry](/registry/#the-viam-registry) to find one that supports your custom hardware or software, or you can write your own module.

Modules run alongside `viam-server` as separate processes, communicating with `viam-server` over UNIX sockets.
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and the associated [APIs](/program/apis/) with `viam-server`, making the new model available for use.

In most cases, the {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} you create should be a new {{< glossary_tooltip term_id="model" text="model" >}} that implements an existing Viam [API](/program/apis/).
For example, if you have a custom base, you can create a new base model that implements the `rdk:component:base` API.

## Find your reference files

Before you start coding a new resource model, follow these steps to find the appropriate source code as a reference for the methods you need to implement:

1. **Understand your model's client interface:**

   {{< tabs >}}
   {{% tab name="Python" %}}

To create a new resource model, you need to implement your model's **client** interface in a file called `my_modular_resource.py`.

This interface defines how your model's server responds to API requests.

To ensure the client interface you create returns the expected results, use the appropriate client interface defined in <file>components/\<resource-name\>/client.py</file> or <file>services/\<resource-name\>/client.py</file> in the [Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/) as a reference.

For example, the `base` component client is defined in the [<file>client.py</file>](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/client.py) file.

See [Valid APIs to implement in your model](#valid-apis-to-implement-in-your-model) for more information.

{{% /tab %}}
{{% tab name="Go" %}}

To create a new resource model, you need to implement your model's **client** interface in a file called `my_modular_resource.go`.

This interface defines how your model's server responds to API requests.

To ensure the client interface you create returns the expected results, use the appropriate client interface defined in <file>components/\<resource-name\>/client.go</file> or <file>services/\<resource-name\>/client.go</file> in the [Viam RDK](https://github.com/viamrobotics/rdk/blob/main/) as a reference.

For example, the `base` component client is defined in the [<file>client.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/client.go) file.

See [Valid APIs to implement in your model](#valid-apis-to-implement-in-your-model) for more information.

{{% /tab %}}
{{< /tabs >}}

1. **Prepare to Import Your Custom Model and Subtype's API:**

   To prepare to import your custom model and chosen resource subtype's API into your main program and register them with your preferred SDK:

   {{< tabs >}}
   {{% tab name="Python" %}}

Find the subtype API as defined in the relevant <file>components/\<resource-name\>/\<resource-name>\.py</file> or <file>services/\<resource-name\>/<resource-name>.py</file> file in the [Python SDK](https://github.com/viamrobotics/viam-python-sdk).

For example, the `base` component subtype is defined in [<file>viam-python-sdk/src/viam/components/base/base.py</file>](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/base.py).

{{% /tab %}}
{{% tab name="Go" %}}

Find the subtype API as defined in the relevant <file>components/\<resource-name\>/\<resource-name\>.go</file> or <file>services/\<resource-name\>/\<resource-name\>.go</file> file in the [RDK](https://github.com/viamrobotics/rdk).

For example, the `base` component subtype is defined in [<file>rdk/components/base/base.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/base.go#L37).

{{% /tab %}}
{{< /tabs >}}

### Valid APIs to implement in your model

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing {{< glossary_tooltip term_id="component" text="component" >}}, valid [APIs](/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor`

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing [service](/services/), valid [APIs](/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `navigation`

#### Unique cases

If you are using unique hardware that does not already have an [appropriate API](/program/apis/#component-apis) defined to support it, you can use the [generic API](/components/generic/) to add support for that unique hardware type to your machine.

Some use cases may require you to define a new API, or to deploy custom components using a server on a remote part.
For more information, see [Advanced Modular Resources](/registry/advanced/).

## Create a custom module

A custom module wraps one or more {{< glossary_tooltip term_id="model" text="models" >}}.
To create a custom module, follow these steps:

1. [Code a new resource model](#code-a-new-resource-model) server.
2. [Code a main program](#code-a-main-entry-point-program).
3. [Compile or package](#prepare-the-module-for-execution) the module into a single executable.

### Code a new resource model

{{% alert title="Naming your model" color="tip" %}}

Use the naming schema: `namespace:repo-name:name`.

For more information see [Naming your model](/registry/upload/#naming-your-model-namespacerepo-namename).

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}
Your new resource model server must have all the methods that the Viam RDK requires, and should match the built-in API client {{< glossary_tooltip term_id="subtype" text="subtype" >}} like [`rdk:component:base`](https://python.viam.dev/autoapi/viam/components/base/index.html).

Create a folder for your module and save your code as a file named <file>my_modular_resource.py</file> inside.

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) (`rdk:service:base`) as a new model, `"mybase"`, using the model family `acme:demo:mybase`.

<details>
  <summary>Click to view sample code for <file>my_base.py</file></summary>

```python {class="line-numbers linkable-line-numbers"}
from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, cast

from typing_extensions import Self

from viam.components.base import Base
from viam.components.motor import Motor
from viam.module.types import Reconfigurable
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.resource.types import Model, ModelFamily
from viam.utils import ValueTypes
from viam.logging import getLogger

LOGGER = getLogger(__name__)


class MyBase(Base, Reconfigurable):
    """
    MyBase implements a base that only supports set_power
    (basic forward/back/turn controls) is_moving (check if in motion), and stop
    (stop all motion).

    It inherits from the built-in resource subtype Base and conforms to the
    ``Reconfigurable`` protocol, which signifies that this component can be
    reconfigured. Additionally, it specifies a constructor function
    ``MyBase.new_base`` which confirms to the
    ``resource.types.ResourceCreator`` type required for all models.
    """

    # Here is where we define our new model's colon-delimited-triplet
    # (acme:demo:mybase) acme = namespace, demo = repo-name,
    # mybase = model name.
    MODEL: ClassVar[Model] = Model(ModelFamily("acme", "demo"), "mybase")

    def __init__(self, name: str, left: str, right: str):
        super().__init__(name, left, right)

    # Constructor
    @classmethod
    def new_base(cls,
                 config: ComponentConfig,
                 dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        base = cls(config.name)
        base.reconfigure(config, dependencies)
        return base

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        left_name = config.attributes.fields["motorL"].string_value
        if left_name == "":
            raise Exception(
                "A motorL attribute is required for a MyBase component.")
        right_name = [config.attributes.fields["motorR"].string_value]
        if right_name == "":
            raise Exception(
                "A motorR attribute is required for a MyBase component.")
        return [left_name, right_name]

    # Handles attribute reconfiguration
    def reconfigure(self,
                    config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]):
        left_name = config.attributes.fields["motorL"].string_value
        right_name = config.attributes.fields["motorR"].string_value

        left_motor = dependencies[Motor.get_resource_name(left_name)]
        right_motor = dependencies[Motor.get_resource_name(right_name)]

        self.left = cast(Motor, left_motor)
        self.right = cast(Motor, right_motor)

    """
    Implement the methods the Viam RDK defines for the base API
    (rdk:component:base)
    """

    # move_straight: unimplemented
    async def move_straight(self,
                            distance: int,
                            velocity: float,
                            *,
                            extra: Optional[Dict[str, Any]] = None,
                            timeout: Optional[float] = None,
                            **kwargs):
        raise NotImplementedError

    # spin: unimplemented
    async def spin(self,
                   angle: float,
                   velocity: float,
                   *,
                   extra: Optional[Dict[str, Any]] = None,
                   timeout: Optional[float] = None,
                   **kwargs):
        raise NotImplementedError

    # set_power: set the linear and angular velocity of the left and right
    # motors on the base
    async def set_power(self,
                        linear: Vector3,
                        angular: Vector3,
                        *,
                        extra: Optional[Dict[str, Any]] = None,
                        timeout: Optional[float] = None,
                        **kwargs):

        # stop the base if absolute value of linear and angular velocity is
        # less than .01
        if abs(linear.y) < 0.01 and abs(angular.z) < 0.01:
            return self.stop(extra=extra, timeout=timeout)

        # use linear and angular velocity to calculate percentage of max power
        # to pass to SetPower for left & right motors
        sum = abs(linear.y) + abs(angular.z)

        self.left.set_power(power=((linear.y - angular.z) / sum),
                            extra=extra,
                            timeout=timeout)
        self.right.set_power(power=((linear.y + angular.z) / sum),
                             extra=extra,
                             timeout=timeout)

    # set_velocity: unimplemented
    async def set_velocity(self,
                           linear: Vector3,
                           angular: Vector3,
                           *,
                           extra: Optional[Dict[str, Any]] = None,
                           timeout: Optional[float] = None,
                           **kwargs):
        raise NotImplementedError

    # get_properties: unimplemented
    async def get_properties(self,
                             extra: Optional[Dict[str, Any]] = None,
                             timeout: Optional[float] = None,
                             **kwargs):
        raise NotImplementedError

    # stop: stop the base from moving by stopping both motors
    async def stop(self,
                   *,
                   extra: Optional[Dict[str, Any]] = None,
                   timeout: Optional[float] = None,
                   **kwargs):
        self.left.stop(extra=extra, timeout=timeout)
        self.right.stop(extra=extra, timeout=timeout)

    # is_moving: check if either motor on the base is moving with motors'
    # is_powered
    async def is_moving(self,
                        *,
                        extra: Optional[Dict[str, Any]] = None,
                        timeout: Optional[float] = None,
                        **kwargs) -> bool:
        return self.left.is_powered(extra=extra, timeout=timeout)[0] or \
            self.right.is_powered(extra=extra, timeout=timeout)[0]
```

</details>
<br>

Additional example modules are available in the [Python SDK GitHub repository](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples).

{{% /tab %}}
{{% tab name="Go"%}}

Your new resource model server must have all the methods that the Viam RDK requires, and should match the built-in API client {{< glossary_tooltip term_id="subtype" text="subtype" >}} like [`rdk:component:base`](https://pkg.go.dev/go.viam.com/rdk/components/base#pkg-functions).

Create a folder for your module and save your code as a file named <file>my_modular_resource.go</file> inside.

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) (`rdk:service:base`) as a new {{< glossary_tooltip term_id="model" text="model" >}}, `"mybase"`, using the model family `acme:demo:mybase`.

<details>
  <summary>Click to view sample code for <file>mybase.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package mybase implements a base that only supports SetPower (basic forward/back/turn controls), IsMoving (check if in motion), and Stop (stop all motion).
// It extends the built-in resource subtype Base and implements methods to handle resource construction, attribute configuration, and reconfiguration.

package mybase

import (
    "context"
    "fmt"
    "math"

    "github.com/golang/geo/r3"
    "github.com/pkg/errors"
    "go.uber.org/multierr"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/components/base/kinematicbase"
    "go.viam.com/rdk/components/motor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/spatialmath"
)

// Here is where we define your new model's colon-delimited-triplet (acme:demo:mybase)
// acme = namespace, demo = repo-name, mybase = model name.
var (
    Model            = resource.NewModel("acme", "demo", "mybase")
    errUnimplemented = errors.New("unimplemented")
)

const (
    myBaseWidthMm        = 500.0 // Base has a wheel tread of 500 millimeters
    myBaseTurningRadiusM = 0.3   // Base turns around a circle of radius .3 meters
)

func init() {
    resource.RegisterComponent(base.API, Model, resource.Registration[base.Base, *Config]{
        Constructor: newBase,
    })
}

func newBase(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger) (base.Base, error) {
    b := &myBase{
        Named:  conf.ResourceName().AsNamed(),
        logger: logger,
    }
    if err := b.Reconfigure(ctx, deps, conf); err != nil {
        return nil, err
    }
    return b, nil
}


// Reconfigure reconfigures with new settings.
func (b *myBase) Reconfigure(ctx context.Context, deps resource.Dependencies, conf resource.Config) error {
    b.left = nil
    b.right = nil

    // This takes the generic resource.Config passed down from the parent and converts it to the
    // model-specific (aka "native") Config structure defined, above making it easier to directly access attributes.
    baseConfig, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return err
    }

    b.left, err = motor.FromDependencies(deps, baseConfig.LeftMotor)
    if err != nil {
        return errors.Wrapf(err, "unable to get motor %v for mybase", baseConfig.LeftMotor)
    }

    b.right, err = motor.FromDependencies(deps, baseConfig.RightMotor)
    if err != nil {
        return errors.Wrapf(err, "unable to get motor %v for mybase", baseConfig.RightMotor)
    }

    geometries, err := kinematicbase.CollisionGeometry(conf.Frame)
    if err != nil {
        b.logger.Warnf("base %v %s", b.Name(), err.Error())
    }
    b.geometries = geometries

    // Stop motors when reconfiguring.
    return multierr.Combine(b.left.Stop(context.Background(), nil), b.right.Stop(context.Background(), nil))
}

// DoCommand simply echos whatever was sent.
func (b *myBase) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    return cmd, nil
}

// Config contains two component (motor) names.
type Config struct {
    LeftMotor  string `json:"motorL"`
    RightMotor string `json:"motorR"`
}

// Validate validates the config and returns implicit dependencies,
// this Validate checks if the left and right motors exist for the module's base model.
func (cfg *Config) Validate(path string) ([]string, error) {
    // check if the attribute fields for the right and left motors are non-empty
    // this makes them reuqired for the model to successfully build
    if cfg.LeftMotor == "" {
        return nil, fmt.Errorf(`expected "motorL" attribute for mybase %q`, path)
    }
    if cfg.RightMotor == "" {
        return nil, fmt.Errorf(`expected "motorR" attribute for mybase %q`, path)
    }

    // Return the left and right motor names so that `newBase` can access them as dependencies.
    return []string{cfg.LeftMotor, cfg.RightMotor}, nil
}

type myBase struct {
    resource.Named
    left       motor.Motor
    right      motor.Motor
    logger     logging.Logger
    geometries []spatialmath.Geometry
}

// MoveStraight does nothing.
func (b *myBase) MoveStraight(ctx context.Context, distanceMm int, mmPerSec float64, extra map[string]interface{}) error {
    return errUnimplemented
}

// Spin does nothing.
func (b *myBase) Spin(ctx context.Context, angleDeg, degsPerSec float64, extra map[string]interface{}) error {
    return errUnimplemented
}

// SetVelocity does nothing.
func (b *myBase) SetVelocity(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    return errUnimplemented
}

// SetPower computes relative power between the wheels and sets power for both motors.
func (b *myBase) SetPower(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    b.logger.Debugf("SetPower Linear: %.2f Angular: %.2f", linear.Y, angular.Z)
    if math.Abs(linear.Y) < 0.01 && math.Abs(angular.Z) < 0.01 {
        return b.Stop(ctx, extra)
    }
    sum := math.Abs(linear.Y) + math.Abs(angular.Z)
    err1 := b.left.SetPower(ctx, (linear.Y-angular.Z)/sum, extra)
    err2 := b.right.SetPower(ctx, (linear.Y+angular.Z)/sum, extra)
    return multierr.Combine(err1, err2)
}

// Stop halts motion.
func (b *myBase) Stop(ctx context.Context, extra map[string]interface{}) error {
    b.logger.Debug("Stop")
    err1 := b.left.Stop(ctx, extra)
    err2 := b.right.Stop(ctx, extra)
    return multierr.Combine(err1, err2)
}

// IsMoving returns true if either motor is active.
func (b *myBase) IsMoving(ctx context.Context) (bool, error) {
    for _, m := range []motor.Motor{b.left, b.right} {
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

// Properties returns details about the physics of the base.
func (b *myBase) Properties(ctx context.Context, extra map[string]interface{}) (base.Properties, error) {
    return base.Properties{
        TurningRadiusMeters: myBaseTurningRadiusM,
        WidthMeters:         myBaseWidthMm * 0.001, // converting millimeters to meters
    }, nil
}

// Geometries returns physical dimensions.
func (b *myBase) Geometries(ctx context.Context, extra map[string]interface{}) ([]spatialmath.Geometry, error) {
    return b.geometries, nil
}

// Close stops motion during shutdown.
func (b *myBase) Close(ctx context.Context) error {
    return b.Stop(ctx, nil)
}
```

</details>
<br>

The code for the custom model (<file>mybase.go</file>) and module entry point file (<file>main.go</file>) is adapted from the full demo modules available in the [in the RDK](https://github.com/viamrobotics/rdk/blob/main/examples/customresources).
Additional examples are available in the [examples directory of the RDK](https://github.com/viamrobotics/rdk/blob/main/examples/).

{{% /tab %}}
{{< /tabs >}}

### Code a main entry point program

{{< tabs name="Sample SDK Main Program Code">}}
{{% tab name="Python"%}}

The main program starts the module.
<file>main.py</file> is the module's entry point file.

Import your custom model and API into the main program and register them with the Python SDK.
When executed, the main program registers the `mybase` custom model and API helper functions with the Python SDK and creates and starts the new module.

<details>
  <summary>Click to view sample code for <file>main.py</file></summary>

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.components.base import Base
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from my_base import MyBase


async def main():
    """
    This function creates and starts a new module, after adding all desired
    resource models. Resource creators must be registered to the resource
    registry before the module adds the resource model.
    """
    Registry.register_resource_creator(
        Base.SUBTYPE,
        MyBase.MODEL,
        ResourceCreatorRegistration(MyBase.new_base, MyBase.validate_config))
    module = Module.from_args()

    module.add_model_from_registry(Base.SUBTYPE, MyBase.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
```

</details>

{{% alert title="Important" color="note" %}}

You must define all functions belonging to a built-in resource subtype's API if defining a new model.
Otherwise, the class will not instantiate.

If you do not wish to implement all methods, raise an`NotImplementedError()` in the body of functions you do not want to implement or put `pass`.

Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

{{% /tab %}}
{{% tab name="Go"%}}

The main program starts the module.
<file>main.go</file> is the module's entry point file.

Import your custom model and API into the main program and register them with the RDK.
When executed, the main program registers the `mybase` custom model and API helper functions with the Python SDK and creates and starts the new module.

<details>
  <summary>Click to view sample code for <file>main.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package main is a module which serves the mybase custom model.
package main

import (
    "context"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/module"
    "go.viam.com/utils"

    // NOTE: You must update the following line to import your local package "mybase"
    "go.viam.com/rdk/examples/customresources/models/mybase"
)

func main() {
    // NewLoggerFromArgs will create a logging.Logger at "DebugLevel" if
    // "--log-level=debug" is an argument in os.Args and at "InfoLevel" otherwise.
    utils.ContextualMain(mainWithArgs, module.NewLoggerFromArgs("yourmodule"))
}

func mainWithArgs(ctx context.Context, args []string, logger logging.Logger) (err error) {
    myMod, err := module.NewModuleFromArgs(ctx, logger)
    if err != nil {
        return err
    }

    // Models and APIs add helpers to the registry during their init().
    // They can then be added to the module here.
    err = myMod.AddModelFromRegistry(ctx, base.API, mybase.Model)
    if err != nil {
        return err
    }

    err = myMod.Start(ctx)
    defer myMod.Close(ctx)
    if err != nil {
        return err
    }
    <-ctx.Done()
    return nil
}
```

</details>

{{% alert title="Important" color="note" %}}

You must define all functions belonging to a built-in resource subtype's API if defining a new model.
Otherwise, the class will not instantiate.

If you do not wish to implement all methods, raise `errUnimplemented` for the functions you do not want to implement.

Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

### Prepare the module for execution

To [add a module](/registry/configure/) to the configuration of your robot, you need to have an [executable](https://en.wikipedia.org/wiki/Executable) that:

- runs your module when executed,
- takes a local socket as a command line argument, and
- exits cleanly when sent a termination signal.

Your options for completing this step are flexible, as this file does not need to be in raw binary format.

{{% tabs %}}
{{% tab name="Python: venv (recommended)" %}}

Create and save a new shell script (<file>.sh</file>) that runs your module at your entry point (main program) file.

Make sure to [prepare a Python virtual environment](/program/python-venv/) in the directory your module is in to ensure your module has access to any required libraries:

1. Create a `requirements.txt` file containing a list of all the dependencies your module relies on.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`) is installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   ```

   Add additional dependencies as needed.
   See the [pip `requirements.txt` file documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more information.

2. Add a shell script that creates a new virtual environment, installs the dependencies listed in `requirements.txt`, and runs the module entry point file `main.py`:

   ```sh { class="command-line" data-prompt="$"}
   #!/bin/sh
   cd `dirname $0`

   # Create a virtual environment to run our code
   VENV_NAME="venv"
   PYTHON="$VENV_NAME/bin/python"

   python3 -m venv $VENV_NAME
   $PYTHON -m pip install -r requirements.txt -U # remove -U if viam-sdk should not be upgraded whenever possible

   # Be sure to use `exec` so that termination signals reach the python process,
   # or handle forwarding termination signals manually
   exec $PYTHON <your-src-dir-if-inside>/main.py $@
   ```

   To make your shell script executable, run the following command in your terminal:

   ```sh { class="command-line" data-prompt="$"}
   sudo chmod +x <your-file-path-to>/<run.sh>
   ```

{{% /tab %}}
{{% tab name="Python: nuitka" %}}

Install a [supported C compiler](https://github.com/Nuitka/Nuitka#c-compiler) on your machine.
Make sure to [prepare a Python virtual environment](/program/python-venv/) in the directory your module is in to ensure your module has access to any required libraries.
Compile your module as follows:

1. Create a `requirements.txt` file containing a list of all the dependencies your module relies on.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`) and Nuitka (`nuitka`) are installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   nuitka
   ```

   Add additional dependencies as needed.

2. After installing dependencies in your virtual environment, compile your module with the following command:

   ```sh { class="command-line" data-prompt="$"}
   python -m nuitka --onefile src/main.py
   ```

   Any data files you want to include you must specify through a CLI option as follows:

   ```sh { class="command-line" data-prompt="$"}
   python -m nuitka --onefile --include-data-files=src/arm/my_arm_kinematics.json=src/arm/my_arm_kinematics.json src/main.py
   ```

   No relative imports (imports starting with `.`) will work with this option.
   In addition, no cross compiling is allowed.
   You have to compile on your target platform/architecture.

{{% /tab %}}
{{% tab name="Python: pyinstaller" %}}

Make sure to [prepare a Python virtual environment](/program/python-venv/) in the directory your module is so your module has access to any required libraries.
Compile your module as follows:

1. Create a `requirements.txt` file containing a list of all the dependencies your module relies on.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`), PyInstaller (`pyinstaller`), and the Google API Python client (`google-api-python-client`) are installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   pyinstaller
   google-api-python-client
   ```

   Add additional dependencies as needed.

2. Add the Google API python client as a hidden import when compiling your module.
   After installing the required dependencies in your virtual environment, compile your module as follows:

   ```sh { class="command-line" data-prompt="$"}
   python -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
   ```

   Any data files you want to include you must specify through a CLI option as follows:

   ```sh { class="command-line" data-prompt="$"}
   python -m PyInstaller --onefile --hidden-import="googleapiclient" --add-data src/arm/my_arm_kinematics.json:src/arm/ src/main.py
   ```

   No relative imports (imports starting with `.`) will work with this option.
   In addition, no cross compiling is allowed.
   You have to compile on your target platform/architecture.

{{% /tab %}}
{{% tab name="Go" %}}

Use Go to [compile](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) and obtain a single executable for your module:

- Navigate to your module directory in your terminal.
- Run `go build` to compile your entry point (main program) file <file>main.go</file> and all other <file>.go</file> files in the directory, building your module and all dependencies into a single executable file.
- Run `ls` in your module directory to find the executable, which should have the same name as the module directory.

<file>main.go</file> adds the custom model <file>mybase.go</file> from the resource registry, while <file>mybase.go</file> defines and registers the module.
Expand the [Go module code](#code-a-main-entry-point-program) to view <file>main.go</file> for an example of this.

{{% /tab %}}
{{% /tabs %}}

### Configure logging

To enable your module to write logs to the [Viam app](https://app.viam.com/), ensure that you have added the following lines of code to your respective module code.
Log messages are sent to the Viam app and appear under the **Logs** tab for your machine.

{{< tabs name="Configure logging">}}
{{% tab name="Python"%}}

To enable your Python module to write log messages to the Viam app, add the following lines to your code:

```python {class="line-numbers linkable-line-numbers" data-line="2,5"}
# In your import block, import viam.logging getLogger:
from viam.logging import getLogger

# Before your first class or function, define the LOGGER variable:
LOGGER = getLogger(__name__)
```

{{% /tab %}}
{{% tab name="Go"%}}

To enable your Go module to write log messages to the Viam app, add the following lines to your code:

```go {class="line-numbers linkable-line-numbers"}
// In your import() block, import the logger package:
import(
       ...
       "go.viam.com/rdk/logging"
)
// Alter your component to hold a logger
type component struct {
    ...
 logger logging.Logger
}
// Then, alter your component's constructor to save the logger:
func init() {
 registration := resource.Registration[resource.Resource, *Config]{
  Constructor: func(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger logging.Logger) (resource.Resource, error) {
     ...
     return &component {
         ...
         logger: logger
     }, nil
  },
 }
 resource.RegisterComponent(...)
}
// Finally, when you need to log, use the functions on your component's logger:
fn (c *component) someFunction(a int) {
  // Log with severity info:
  c.logger.Infof("performing some function with a=%v",a)
  // Log with severity debug (using value wrapping):
  c.logger.Debugw("performing some function","a",a)
  // Log with severity error without a parameter:
  c.logger.Errorln("performing some function")
}
```

{{% /tab %}}
{{< /tabs >}}

The examples from [Code a new resource model](#code-a-new-resource-model) include this logging setup.

## Next steps

Once you have created your module, you can use the [Viam CLI](/manage/cli/) to [upload your module](/registry/upload/) to the [Viam registry](https://app.viam.com/registry) to share it with other Viam users or just to other users in your organization.
For added convenience, you can configure [automated uploads for new module versions](/registry/upload/#update-an-existing-module-using-a-github-action) through a continuous integration (CI) workflow, using a GitHub Action.

You can also add your module to your robot as a [local module](/registry/configure/#local-modules), without uploading it to the Viam registry.

{{< cards >}}
{{% card link="/registry/upload/" %}}
{{% manualcard link="/registry/configure/#local-modules" %}}

<h4>Local module</h4>

Add a module to your robot as a local module.

{{% /manualcard %}}
{{< /cards >}}

<br>

You can also check out these tutorials that create modules:

{{< cards >}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/registry/examples/custom-arm/" %}}
{{< /cards >}}
