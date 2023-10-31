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
description: "Use the Viam module system to implement modular resources that can be included in any Viam-powered smart machine."
no_list: true
aliases:
  - "/extend/modular-resources/create/"
---

You can extend Viam by creating a custom {{< glossary_tooltip term_id="module" text="module" >}} that provides one or more modular {{< glossary_tooltip term_id="resource" text="resource" >}} {{< glossary_tooltip term_id="model" text="models" >}}.

A common use case for modular resources is to create a new [model](/modular-resources/key-concepts/#models) that implements an existing Viam [API](/program/apis/).

Once you have created your modular resource, you can use the [Viam CLI](/manage/cli/) to [upload your modular resource](/modular-resources/upload/) to the [Viam registry](https://app.viam.com/registry), to share it with other users in your organization or all other Viam users.
You can also configure [automatic uploads of new versions of your module](/modular-resources/upload/#update-an-existing-module-using-a-github-action) as part of a continuous integration (CI) workflow, using a GitHub Action.

You can also add your module to your robot as a [local module](/modular-resources/configure/#local-modules), without uploading it to the Viam registry.

## Create a custom module

To create a custom module, follow the steps below.
A custom module can implement one or more [models](/modular-resources/key-concepts/#models).

1.  [Code a new resource model](#code-a-new-resource-model) server implementing all methods the Viam RDK requires in `viam-server`'s built-in API client of its subtype (ex. `rdk:component:base`).
    Provide this as a file inside of your module, <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file>.

    Follow these instructions to find the appropriate source code before you start the process.

    **To prepare to code a new resource model**:

    The methods you will code in <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file> are your model's "**client** interface", or how your model's server will respond when `viam-server` asks your resource for something through the API.

    View the appropriate `viam-server` client interface to see what your resource's responses from `viam-server` will look like when your model is utilizing the subtype's API.
    This way, you can make the client interface you code return the type of response `viam-server` expects to receive.

    - Find the relevant `viam-server` client interface as `<resource-name>/client.go` or `<resource-name>/client.py` on [Viam's GitHub](https://github.com/viamrobotics/rdk/blob/main/).
      See [Valid APIs to implement in your model](/modular-resources/key-concepts/#valid-apis-to-implement-in-your-model) for more information.
    - For example, the base client is defined in [<file>rdk/components/base/client.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/client.go).
    - Base your edits to <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file> on this first file.
    - Name your model according to the namespace of the built-in API you are implementing.
      For more information see [Naming your model](/modular-resources/key-concepts/#naming-your-model-namespacerepo-namename).

      <br> **To prepare to import your custom model and your chosen resource subtype's API into your main program and register them with your chosen SDK:**

    - Find the subtype API as defined in the relevant `<resource-name>/<resource-name>.go` file in the RDK on Viam's GitHub.
    - For example, the base subtype is defined in [<file>rdk/components/base/base.go</file>](https://github.com/viamrobotics/rdk/blob/fdff22e90b8976061c318b2d1ca3b1034edc19c9/components/base/base.go#L37).
    - Base your edits to <file>main.go</file> or <file>main.py</file> on this second file.<br>

2.  [Code a main program](#code-a-main-entry-point-program), <file>main.go</file> or <file>main.py</file>, that starts the module after adding your desired resources from the registry.
    Import your custom model and API into the main program and register them with your chosen SDK.
    This main program is the "entry point" to your module.

3.  [Compile or package](#compile-the-module-into-an-executable) the module into a single executable that can receive a socket argument from Viam, open the socket, and start the module at the entry point.

### Code a new resource model

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) [(rdk:service:base)](/modular-resources/key-concepts/#models) as a new model, `"mybase"`, using the model `acme:demo:mybase`.
For more information see [Naming your model](/modular-resources/key-concepts/#naming-your-model-namespacerepo-namename).

The Go code for the custom model (<file>mybase.go</file>) and module entry point file (<file>main.go</file>) is adapted from the full demo modules available on the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources).

{{% alert title="Tip" color="tip" %}}

Name your model with all lowercase letters for optimal performance with Viam's SDKs.
For example, `mybase` or `my-cool-sensor`.

{{% /alert %}}

{{< tabs name="Sample SDK Code">}}
{{% tab name="Python"%}}

<file>my_base.py</file> implements "mybase", a custom model of the base component.

<details>
  <summary>Click to view sample code from <file>my_base.py</file></summary>

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

{{% /tab %}}
{{% tab name="Go"%}}

<file>mybase.go</file> implements "mybase", a custom model of the base component, and registers the new model and API helper functions with the Go SDK.

<details>
  <summary>Click to view sample code from <file>mybase.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package mybase implements a base that only supports SetPower (basic forward/back/turn controls), IsMoving (check if in motion), and Stop (stop all motion).
// It extends the built-in resource subtype Base and implements methods to handle resource construction, attribute configuration, and reconfiguration.

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
    "go.viam.com/rdk/components/base/kinematicbase"
    "go.viam.com/rdk/components/motor"
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

func newBase(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger golog.Logger) (base.Base, error) {
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
    logger     golog.Logger
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

{{% /tab %}}
{{< /tabs >}}

### Code a main entry point program

{{< tabs name="Sample SDK Main Program Code">}}
{{% tab name="Python"%}}

<file>main.py</file> is the Python module's entry point file.
When executed, it registers the `mybase` custom model and API helper functions with the Python SDK and creates and starts the new module.

<details>
  <summary>Click to view sample code from <file>main.py</file></summary>

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

{{% /tab %}}
{{% tab name="Go"%}}

<file>main.go</file> is the Go module's entry point file.
When executed, it initializes the `mybase` custom model and API helper functions from the registry.

<details>
  <summary>Click to view sample code from <file>main.go</file></summary>

```go {class="line-numbers linkable-line-numbers"}
// Package main is a module which serves the mybase custom model.
package main

import (
    "context"

    "github.com/edaniels/golog"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/module"
    "go.viam.com/utils"

    // NOTE: You must update the following line to import your local package "mybase"
    "go.viam.com/rdk/examples/customresources/models/mybase"
)


func main() {
    // NewLoggerFromArgs will create a golog.Logger at "DebugLevel" if
    // "--log-level=debug" is an argument in os.Args and at "InfoLevel" otherwise.
    utils.ContextualMain(mainWithArgs, module.NewLoggerFromArgs("yourmodule"))
}

func mainWithArgs(ctx context.Context, args []string, logger golog.Logger) (err error) {
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

{{% /tab %}}
{{< /tabs >}}

{{% alert title="Important" color="note" %}}

You must define all functions belonging to a built-in resource subtype's API if defining a new model.
Otherwise, the class won’t instantiate.

- If you are using the Python SDK, raise a `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

### Compile the module into an executable

To [add a module](/modular-resources/configure/) to the configuration of your robot, you need to have an [executable](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and cleanly exits when sent a termination signal.

Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

{{% tabs %}}
{{% tab name="Python" %}}

One option is to create and save a new shell script (<file>.sh</file>) that runs your module at your entry point (main program) file.

Make sure that you set up a Python virtual environment in the directory your module is in to compile your resource properly at execution.
See the [Python virtual environment documentation](https://docs.python-guide.org/dev/virtualenvs/) for more information.

You will also need to create a `requirements.txt` file containing a list of all the dependencies your module relies on.
For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`) is installed.
You may also add additional dependencies as needed:

```sh { class="command-line" data-prompt="$"}
viam-sdk
```

See the [pip `requirements.txt` file documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more information.

The following template sets up a new virtual environment (`venv`), installs the dependencies listed in `requirements.txt`, and runs the module entry point file `main.py`:

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
{{% tab name="Go" %}}

Use Go to [compile](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) and obtain a single executable for your module:

- Navigate to your module directory in your terminal.
- Run `go build` to compile your entry point (main program) file <file>main.go</file> and all other <file>.go</file> files in the directory, building your module and all dependencies into a single executable file.
- Run `ls` in your module directory to find the executable, which should have been named after the module directory.

Expand the [Go module code](#code-a-main-entry-point-program) to view <file>main.go</file> for an example of this.

<file>main.go</file> adds the custom model <file>mybase.go</file> from the resource registry, while <file>mybase.go</file> defines and registers the module.

{{% /tab %}}
{{% /tabs %}}

You need to ensure any dependencies for your module (including the Python or Go [Viam SDK](/program/)) are installed as well.
Your executable will be run by `viam-server` as root, so dependencies need to be available to the root user.

### Configure logging

To enable your module to write logs to the [Viam app](https://app.viam.com/), you must add the following configuration to your respective module code.
Once configured in this way, log messages are sent to the Viam app and appear under the **Logs** tab for your smart machine.

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
// In your import() block, import the golog package:
import(
       ...
       "github.com/edaniels/golog"
)
// Alter your component to hold a logger
type component struct {
    ...
 logger golog.Logger
}
// Then, alter your component's constructor to save the logger:
func init() {
 registration := resource.Registration[resource.Resource, *Config]{
  Constructor: func(ctx context.Context, deps resource.Dependencies, conf resource.Config, logger golog.Logger) (resource.Resource, error) {
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

The examples under [Code a new resource model](#code-a-new-resource-model) include this logging configuration.

## Next steps

Once you have created your custom resource, you can use the [Viam CLI](/manage/cli/) to [upload your custom resource](/modular-resources/upload/) to the Viam registry, to share it with other Viam users or just to other users in your organization.

You can also add your module to your robot as a [local module](/modular-resources/configure/#local-modules), without uploading it to the Viam registry.
