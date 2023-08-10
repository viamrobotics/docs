---
title: "Code your own modules to create custom resources"
linkTitle: "Create"
weight: 20
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
no_list: true
---

The Viam module system allows you to integrate custom {{< glossary_tooltip term_id="resource" text="resources" >}} ([components](/components/) and [services](/services/)) into any robot running on Viam.

A common use case for modular resources is to create a new model that implements an existing Viam API.
However, you can also create and expose new APIs with modular resources.

{{% alert title="Modules vs. modular resources" color="tip" %}}

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

## Create a custom modular resource

To create your own modular resource, code a module in Go or Python using the module support libraries provided by [Viam's SDKs](/program/apis/) that implements at least one new {{< glossary_tooltip term_id="model" text="model" >}} or {{< glossary_tooltip term_id="subtype" text="subtype" >}} of {{< glossary_tooltip term_id="resource" text="resource" >}}:

{{< tabs >}}
{{% tab name="New Model" %}}
Define a new model of a built-in resource subtype:

1. [Code a new resource model](#code-a-new-resource-model) server implementing all methods the Viam RDK requires in `viam-servers`'s built-in API client of its subtype (ex. `rdk:component:base`).
Provide this as a file inside of your module, <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file>.

   Follow these instructions to find the appropriate source code before you start the process.

   **To prepare to code a new resource model**:

   The methods you will code in <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file> are your model's "**client** interface", or how your model's server will respond when `viam-server` asks your resource for something through the API.

   View the appropriate `viam-server` client interface to see what your resource's responses from `viam-server` will look like when your model is utilizing the subtype's API.
   This way, you can make the client interface you code return the type of response `viam-server` expects to receive.

   - Find the relevant `viam-server` client interface as `<resource-name>/client.go` or `<resource-name>/client.py` on [Viam's GitHub](https://github.com/viamrobotics/rdk/blob/main/).
   - For example, the base client is defined in [<file>rdk/components/base/client.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/client.go).
   - Base your edits to <file>my_modular_resource.go</file> or <file>my_modular_resource.py</file> on this first file.

    <br> **To prepare to import your custom model and your chosen resource subtype's API into your main program and register them with your chosen SDK:**

   - Find the subtype API as defined in the relevant `<resource-name>/<resource-name>.go` file in the RDK on Viam's GitHub.
   - For example, the base subtype is defined in [<file>rdk/components/base/base.go</file>](https://github.com/viamrobotics/rdk/blob/fdff22e90b8976061c318b2d1ca3b1034edc19c9/components/base/base.go#L37).
   - Base your edits to <file>main.go</file> or <file>main.py</file> on this second file. <br>

2. [Code a main program](#code-a-main-entry-point-program), <file>main.go</file> or <file>main.py</file>, that starts the module after adding your desired resources from the registry.
Import your custom model and API into the main program and register them with your chosen SDK.
This main program is the "entry point" to your module.

3. [Compile or package](#compile-the-module-into-an-executable) the module into a single executable that can receive a socket argument from Viam, open the socket, and start the module at the entry point.

{{% /tab %}}
{{% tab name="New Type" %}}
Define a new {{< glossary_tooltip term_id="api-namespace-triplet" text="type or subtype" >}} of resource:

1. Define the methods and messages of the new API in [protobuf](https://github.com/protocolbuffers/protobuf) and in Python or Go, then use a protobuf compiler to [generate the rest of the required protobuf files](https://grpc.io/docs/languages/python/generated-code/) based on that Python or Go code.
Find detailed instructions in [Define a New Resource Subtype](create-subtype/).

1. [Code at least one model](#code-a-new-resource-model) of this new resource.
Make sure to implement every method required in your API definition.
Import your custom models and APIs into the main program and register them with your chosen SDK.

1. [Code a main program](#code-a-main-entry-point-program) that starts the module after adding your desired resources from the registry.
This main program is the "entry point" to your module.

1. [Compile or package](#compile-the-module-into-an-executable) the module into a single executable that can receive a socket argument from Viam, open the socket, and start the module at the entry point.

{{% /tab %}}
{{% /tabs %}}

### Code a new resource model

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) [(rdk:service:base)](/extend/modular-resources/key-concepts/#models) as a new model, `"mybase"`:

The Go code for the custom model (<file>mybase.go</file>) and module entry point file (<file>main.go</file>) is adapted from the full demo modules available on the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources).

{{< tabs name="Sample SDK Code">}}
{{% tab name="Python"%}}

<file>my_base.py</file> implements "mybase", a custom model of the base component.

<details>
  <summary>Click to view sample code from <file>my_base.py</file></summary>

``` python {class="line-numbers linkable-line-numbers"}
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

class MyBase(Base, Reconfigurable):
    """
    MyBase implements a base that only supports set_power (basic forward/back/turn controls) is_moving (check if in motion), and stop (stop all motion).

    It inherits from the built-in resource subtype Base and conforms to the ``Reconfigurable`` protocol, which signifies that this component can be reconfigured.
    Additionally, it specifies a constructor function ``MyBase.new_base`` which confirms to the ``resource.types.ResourceCreator`` type required for all models.
    """

    # Here is where we define our new model's colon-delimited-triplet (acme:demo:mybase)
    # acme = namespace, demo = family, mybase = model name.
    MODEL: ClassVar[Model] = Model(ModelFamily("acme", "demo"), "mybase")

    def __init__(self, name: str, left: str, right: str):
        super().__init__(name, left, right)

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
        raise NotImplementedError

    # spin: unimplemented
    async def spin(self, angle: float, velocity: float, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        raise NotImplementedError

    # set_power: set the linear and angular velocity of the left and right motors on the base
    async def set_power(self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):

        # stop the base if absolute value of linear and angular velocity is less than .01
        if abs(linear.y) < 0.01 and abs(angular.z) < 0.01:
            return self.stop(extra=extra, timeout=timeout)

        # use linear and angular velocity to calculate percentage of max power to pass to SetPower for left & right motors
        sum = abs(linear.y) + abs(angular.z)

        self.left.set_power(power=((linear.y - angular.z) / sum), extra=extra, timeout=timeout)
        self.right.set_power(power=((linear.y + angular.z) / sum), extra=extra, timeout=timeout)

    # set_velocity: unimplemented
    async def set_velocity(self, linear: Vector3, angular: Vector3, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        raise NotImplementedError

    # get_properties: unimplemented
    async def get_properties(self, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        raise NotImplementedError

    # stop: stop the base from moving by stopping both motors
    async def stop(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        self.left.stop(extra=extra, timeout=timeout)
        self.right.stop(extra=extra, timeout=timeout)

    # is_moving: check if either motor on the base is moving with motors' is_powered
    async def is_moving(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> bool:
        return self.left.is_powered(extra=extra, timeout=timeout)[0] or self.right.is_powered(extra=extra, timeout=timeout)[0]
```

{{% /tab %}}
{{% tab name="Go"%}}

<file>mybase.go</file> implements "mybase", a custom model of the base component,  and registers the new model and API helper functions with the Go SDK.

<details>
  <summary>Click to view sample code from <file>mybase.go</file></summary>

``` go {class="line-numbers linkable-line-numbers"}
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

// Properties: unimplemented
func (base *MyBase) Spin(ctx context.Context, extra map[string]interface{}) error {
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

</details>

{{% /tab %}}
{{< /tabs >}}

### Code a main entry point program

{{< tabs name="Sample SDK Main Program Code">}}
{{% tab name="Python"%}}

<file>main.py</file> is the Python module's entry point file.
When executed, it registers the mybase custom model and API helper functions with the Python SDK and creates and starts the new module.

<details>
  <summary>Click to view sample code from <file>main.py</file></summary>

``` python {class="line-numbers linkable-line-numbers"}
import asyncio
import sys

from viam.components.base import Base
from viam.module.module import Module
from my_base import MyBase

async def main():
    """This function creates and starts a new module, after adding all desired resource models.
    Resource creators must be registered to the resource registry before the module adds the resource model. 
    """
    Registry.register_resource_creator(Base.SUBTYPE, MyBase.MODEL, ResourceCreatorRegistration(MyBase.new_base, MyBase.validate_config))
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

``` go {class="line-numbers linkable-line-numbers"}
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

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented`.
- Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

### Compile the module into an executable

To [add a module](/extend/modular-resources/configure/#configure-your-module) to the configuration of your robot, you need to have an [executable](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and cleanly exits when sent a termination signal.

Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

{{% tabs %}}
{{% tab name="Python" %}}

One option is to create and save a new shell script (<file>.sh</file>) that runs your module at your entry point (main program) file.

Make sure that you set up a Python virtual environment in the directory your module is in to compile your resource properly at execution.
See the [Python Documentation](https://docs.python-guide.org/dev/virtualenvs/) for help with this.

Include `venv` set-up and manage dependencies in your script as in the following template:

``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
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

``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
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

## Create a custom module using the Viam CLI

{{% alert title="Beta Notice" color="note" %}}
This feature is in beta, and may not be suitable for production use.
{{% /alert %}}

You can use the [Viam CLI](/manage/cli/) to create and upload your own custom modules to the Viam Registry.
With the CLI, you can create a new module from a template, register your module with the Viam Registry, and share it with other Viam users.
You can also create a private module that is shared only within your [organization](/manage/fleet/organizations/). For more information, see the [`viam module` command](/manage/cli/#module).

1. First, [install the Viam CLI](/manage/cli/#install) and [authenticate](/manage/cli/#authenticate) to Viam.

1. Next, choose your custom module name and create a new module template using the `viam module create` command:

   - To create a *public* module that will be visible to all Viam users, provide a unique [namespace](/extend/modular-resources/key-concepts/#namespace) when creating your module:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module create --name <your-module-name> --namespace <your-unique-namespace>
      ```

   - To create a *private* module that will only be accessible to users within your [organization](/manage/fleet/organizations/), provide your organization ID when creating your module:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module create --name <your-module-name> --org-id <org-id>
      ```

      You can find your organization ID by navigating to the [the Viam app](https://app.viam.com), selecting your user account in the upper-right corner, and clicking **Settings** from the drop down menu.

   This command creates a new `meta.json` file in your current working directory, which serves as a template on which to base your custom configurations.

1. Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module.
   Fill in the following fields. The `name` and `visibility` fields are pre-populated:

<table>
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Inclusion</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>name</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>The name of the module.</td>

  </tr>
  <tr>
    <td><code>visibility</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>Whether the module is visible to all Viam users (<code>public</code>), or accessible only to members of your <a href="/manage/fleet/organizations/">organization</a> (<code>private</code>). You can change this setting later using the <code>viam module update</code> command.<br><br>Default: <code>private</code></td>
  </tr>
  <tr>
    <td><code>url</code></td>
    <td>string</td>
    <td>Optional</td>
    <td>The URL of the GitHub repository containing the source code of the module.</td>
  </tr>
  <tr>
    <td><code>description</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>A description of your module and what it provides.</td>
  </tr>
  <tr>
    <td><code>models</code></td>
    <td>object</td>
    <td><strong>Required</strong></td>
    <td>A list of one or more <a href="/extend/modular-resources/key-concepts/#models">models</a> provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair. </td>
  </tr>
  <tr>
    <td><code>entrypoint</code></td>
    <td>string</td>
    <td><strong>Required</strong></td>
    <td>The path to the module file that starts your program.</td>
  </tr>
</table>

   For example, the following represents the configuration of an example `my-module` module:

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "name": "acme:my-module",
     "visibility": "private",
     "url": "https://github.com/acme-co/my-module",
     "description": "An example custom module.",
     "models": [
       {
         "api": "rdk:component:generic",
         "model": "acme:demo:my-model"
       }
     ],
     "entrypoint": "/usr/local/bin/my-module"
   }
   ```

  {{% alert title="Important" color="note" %}}
  If you are publishing a public module (`visibility: "public"`), the [namespace of your model](/extend/modular-resources/key-concepts/#namespace-1) must match the [namespace of your organization](/extend/modular-resources/key-concepts/#namespace). In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
  {{% /alert %}}

1. Run `viam module update` to register the configuration changes you just made to `meta.json`:

   - To register a *public* module, run the following command from within the same directory as your `meta.json` file:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update
      ```

   - To register a *private* module, run the following command from within the same directory as your `meta.json` file, providing your organization ID:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update --org-id <org-id>
      ```

   On successful update, the command will return a link to the updated module in the Viam Registry.

1. Package your custom module to get it ready to upload to the Viam Registry. Currently, the Registry only supports `tar.gz` format. Run the following command to zip your custom module as a `tar.gz` archive:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -zcf <module-name>.tar.gz <module-name>
   ```

   Where `module-name` is the directory that contains your module.

1. Run `viam module upload` to upload the updated custom module to the Viam Registry:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <packaged-module.tar.gz>
   ```

   Where:

   - `version` - provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`). The Viam Registry does not perform any validation on this value. You can later increment this value with subsequent `viam module upload` commands.
   - `platform` - provide one of the following, depending on the platform you have built your custom module for (You can use the `uname -m` command to determine your system architecture):
      - `darwin/arm64` - macOS computers running the `arm64` architecture, such as Apple Silicon.
      - `darwin/amd64` - macOS computers running the Intel `x86_64` architecture.
      - `linux/arm64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the `arm64` (`aarch64`) architecture, such as the Raspberry Pi.
      - `linux/amd64` - Linux computers or {{< glossary_tooltip term_id="board" text="boards" >}} running the Intel `x86_64` architecture.
   - `path` - provide the path to the compressed tarball, in `tar.gz` format, that contains your custom module.

   For example, the following command uploads the compressed `my-module.tar.gz` archive to the Viam Registry when run in the same directory:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.0 --platform darwin/arm64 my-module.tar.gz
   ```

For more information, see the [`viam module` command](/manage/cli/#module)

### Update an existing module

You can also use the [Viam CLI](/manage/cli/) to update an existing custom module in the Viam Registry.

1. Edit your custom module with the changes you'd like to make.

1. Update your custom module's `meta.json` file with the changes, if any.
   For example, if you have altered your model's name, or adjusted the endpoint path, you'll need to update `meta.json` with these changes.

1. Run `viam module update` to register the configuration changes to your module (and to `meta.json` if applicable):

   - To register a *public* module, run the following command from within the same directory as your `meta.json` file:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update
      ```

   - To register a *private* module, run the following command from within the same directory as your `meta.json` file, providing your organization ID:

      ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
      viam module update --org-id <org-id>
      ```

   On successful update, the command will return a link to the updated module in the Viam Registry.

1. Re-package your custom module to get it ready to upload to the Viam Registry. Currently, the Registry only supports `tar.gz` format. Run the following command to zip your custom module as a `tar.gz` archive:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -zcf <module-name>.tar.gz <module-name>
   ```

   Where `module-name` is the directory that contains your module. If you already have a `tar.gz` archive of your module present in the same directory, this command will error: remove the older `tar.gz` archive first, and then re-run this command.

1. Run `viam module upload` to upload the updated custom module to the Viam Registry:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <path-to-tar.gz>
   ```

   For example, the following command uploads the compressed `my-module.tar.gz` archive to the Viam Registry when run in the same directory, and increments the version of the module to version `1.0.1`:

   ``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version 1.0.1 --platform darwin/arm64 my-module.tar.gz
   ```

For more information, see the [`viam module` command](/manage/cli/#module)

## Next steps

Once you have created your custom resource, follow [these configuration instructions](/extend/modular-resources/configure/) to add the custom resource to your robot.
