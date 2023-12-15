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
When a module initializes, it registers its {{< glossary_tooltip term_id="model" text="model or models" >}} and the associated [APIs](/build/program/apis/) with `viam-server`, making the new model available for use.

In most cases, the {{< glossary_tooltip term_id="modular-resource" text="modular resources" >}} you create should be a new {{< glossary_tooltip term_id="model" text="model" >}} that implements an existing Viam [API](/build/program/apis/).
For example, if you have a custom base, you can create a new base model that implements the `rdk:component:base` API.

## Find your reference files

Before you start coding a new resource model, follow these steps to find the appropriate source code as a reference for the methods you need to implement:

1. **Understand your model's client interface:**

   {{< tabs >}}
   {{% tab name="Python" %}}

To create a new resource model, you need to implement your model's **client** interface in a file called `my_modular_resource.py`.

This interface defines how your model's server responds to API requests.

To ensure the client interface you create returns the expected results, use the appropriate client interface defined in <file>components/\<resource-name\>/client.py</file> or <file>services/\<resource-name\>/client.py</file> in the [Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/) as a reference.

For example, the `base` component client is defined in the [<file>components/base/client.py</file>](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/client.py) file.

See [Valid APIs to implement in your model](#valid-apis-to-implement-in-your-model) for more information.

{{% /tab %}}
{{% tab name="Go" %}}

To create a new resource model, you need to implement your model's **client** interface in a file called `my_modular_resource.go`.

This interface defines how your model's server responds to API requests.

To ensure the client interface you create returns the expected results, use the appropriate client interface defined in <file>components/\<resource-name\>/client.go</file> or <file>services/\<resource-name\>/client.go</file> in the [Viam RDK](https://github.com/viamrobotics/rdk/blob/main/) as a reference.

For example, the `base` component client is defined in the [<file>components/base/client.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/client.go) file.

See [Valid APIs to implement in your model](#valid-apis-to-implement-in-your-model) for more information.

{{% /tab %}}
{{% tab name="C++" %}}

To create a new resource model, start by referencing the corresponding built-in resource's implementation in the [Viam C++ SDK](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/sdk).

For example, if you are implementing a new custom `base` component model, reference the [<file>components/base/base.hpp</file>](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base/base.hpp) implementation file to learn how the `BaseClient` class is implemented.

You can create your own derivative class in a <file>.cpp</file>, such as <file>my_modular_resource.cpp</file>, and optionally define the implementation of that class in a <file>.hpp</file> header file, such as <file>my_modular_resource.hpp</file>.
The example code in the following sections demonstrates an implementation using both files.

See [Valid APIs to implement in your model](#valid-apis-to-implement-in-your-model) for more information.

{{% /tab %}}
{{< /tabs >}}

1. **Prepare to Import Your Custom Model and Subtype's API:**

   To prepare to import your custom model and chosen resource subtype's API into your main program and register them with your preferred SDK:

   {{< tabs >}}
   {{% tab name="Python" %}}

Find the subtype API as defined in the relevant <file>components/\<resource-name\>/\<resource-name>\.py</file> or <file>services/\<resource-name\>/<resource-name>.py</file> file in the [Python SDK](https://github.com/viamrobotics/viam-python-sdk).

For example, the `base` component API is defined in [<file>components/base/base.py</file>](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/base.py#L11).

{{% /tab %}}
{{% tab name="Go" %}}

Find the subtype API as defined in the relevant <file>components/\<resource-name\>/\<resource-name\>.go</file> or <file>services/\<resource-name\>/\<resource-name\>.go</file> file in the [RDK](https://github.com/viamrobotics/rdk).

For example, the `base` component API is defined in [<file>components/base/base.go</file>](https://github.com/viamrobotics/rdk/blob/main/components/base/base.go#L37).

{{% /tab %}}
{{% tab name="C++" %}}

Find the subtype API as defined in the relevant <file>components/\<resource-name\>/\<resource-name>\.hpp</file> or <file>services/\<resource-name\>/<resource-name>.hpp</file> implementation (header) file in the [C++ SDK](https://github.com/viamrobotics/viam-cpp-sdk/).

For example, the `base` component API is defined in [<file>components/base/base.hpp</file>](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base/base.hpp).

{{% /tab %}}
{{< /tabs >}}

### Valid APIs to implement in your model

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing {{< glossary_tooltip term_id="component" text="component" >}}, valid [APIs](/build/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor`

When implementing a custom {{< glossary_tooltip term_id="model" text="model" >}} of an existing [service](/services/), valid [APIs](/build/program/apis/) always have the following parameters:

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `navigation`

#### Unique cases

If you are using unique hardware that does not already have an [appropriate API](/build/program/apis/#component-apis) defined to support it, you can use the [generic API](/components/generic/) to add support for that unique hardware type to your machine.

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

Your new resource model must implement all the methods that the Viam RDK requires, and should match the built-in {{< glossary_tooltip term_id="subtype" text="subtype" >}} API, like [`rdk:component:base`](https://python.viam.dev/autoapi/viam/components/base/index.html).

Create a folder for your module and save your code as a file named <file>my_modular_resource.py</file> inside.

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) (`rdk:components:base`) as a new model, `"mybase"`, using the model family `acme:demo:mybase`.

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

Your new resource model must implement all the methods that the Viam RDK requires, and should match the built-in {{< glossary_tooltip term_id="subtype" text="subtype" >}} API, like [`rdk:component:base`](https://pkg.go.dev/go.viam.com/rdk/components/base#pkg-functions).

Create a folder for your module and save your code as a file named <file>my_modular_resource.go</file> inside.

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) (`rdk:components:base`) as a new {{< glossary_tooltip term_id="model" text="model" >}}, `"mybase"`, using the model family `acme:demo:mybase`.

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
{{% tab name="C++" %}}

Your new resource model must implement all the methods that the Viam RDK requires, and should match the built-in {{< glossary_tooltip term_id="subtype" text="subtype" >}} API, like [`rdk:component:base`](https://cpp.viam.dev/classviam_1_1sdk_1_1Base.html).

Create a folder for your module and save your code as a file named <file>my_modular_resource.cpp</file> inside.

The following example module registers a modular resource implementing Viam's built-in [Base API](/components/base/#api) (`rdk:component:base`) as a new model, `"MyBase"`.
The `my_base.cpp` file defines the specific functionality of the module, while the `my_base.hpp` file defines the implementation of that functionality.

<details>
  <summary>Click to view sample code for <file>my_base.cpp</file></summary>

```cpp {class="line-numbers linkable-line-numbers"}
#include "base.hpp"

#include <exception>
#include <fstream>
#include <iostream>
#include <sstream>

#include <grpcpp/support/status.h>

#include <viam/sdk/components/base/base.hpp>
#include <viam/sdk/components/component.hpp>
#include <viam/sdk/config/resource.hpp>
#include <viam/sdk/resource/resource.hpp>

using namespace viam::sdk;

std::string find_motor(ResourceConfig cfg, std::string motor_name) {
    auto base_name = cfg.name();
    auto motor = cfg.attributes()->find(motor_name);
    if (motor == cfg.attributes()->end()) {
        std::ostringstream buffer;
        buffer << base_name << ": Required parameter `" << motor_name
               << "` not found in configuration";
        throw std::invalid_argument(buffer.str());
    }
    const auto* const motor_string = motor->second->get<std::string>();
    if (!motor_string || motor_string->empty()) {
        std::ostringstream buffer;
        buffer << base_name << ": Required non-empty string parameter `" << motor_name
               << "` is either not a string "
                  "or is an empty string";
        throw std::invalid_argument(buffer.str());
    }
    return *motor_string;
}

void MyBase::reconfigure(Dependencies deps, ResourceConfig cfg) {
    // Downcast `left` and `right` dependencies to motors.
    auto left = find_motor(cfg, "left");
    auto right = find_motor(cfg, "right");
    for (const auto& kv : deps) {
        if (kv.first.short_name() == left) {
            left_ = std::dynamic_pointer_cast<Motor>(kv.second);
        }
        if (kv.first.short_name() == right) {
            right_ = std::dynamic_pointer_cast<Motor>(kv.second);
        }
    }
}

std::vector<std::string> MyBase::validate(ResourceConfig cfg) {
    // Custom validation can be done by specifying a validate function at the
    // time of resource registration (see complex/main.cpp) like this one.
    // Validate functions can `throw` exceptions that will be returned to the
    // parent through gRPC. Validate functions can also return a vector of
    // strings representing the implicit dependencies of the resource.
    //
    // Here, we return the names of the "left" and "right" motors as found in
    // the attributes as implicit dependencies of the base.
    return {find_motor(cfg, "left"), find_motor(cfg, "right")};
}

bool MyBase::is_moving() {
    return left_->is_moving() || right_->is_moving();
}

void MyBase::stop(const AttributeMap& extra) {
    std::string err_message;
    bool throw_err = false;

    // make sure we try to stop both motors, even if the first fails.
    try {
        left_->stop(extra);
    } catch (const std::exception& err) {
        throw_err = true;
        err_message = err.what();
    }

    try {
        right_->stop(extra);
    } catch (const std::exception& err) {
        throw_err = true;
        err_message = err.what();
    }

    // if we received an err from either motor, throw it.
    if (throw_err) {
        throw std::runtime_error(err_message);
    }
}

void MyBase::set_power(const Vector3& linear, const Vector3& angular, const AttributeMap& extra) {
    // Stop the base if absolute value of linear and angular velocity is less
    // than 0.01.
    if (abs(linear.y()) < 0.01 && abs(angular.z()) < 0.01) {
        stop(extra);  // ignore returned status code from stop
        return;
    }

    // Use linear and angular velocity to calculate percentage of max power to
    // pass to set_power for left & right motors
    auto sum = abs(linear.y()) + abs(angular.z());
    left_->set_power(((linear.y() - angular.z()) / sum), extra);
    right_->set_power(((linear.y() + angular.z()) / sum), extra);
}

AttributeMap MyBase::do_command(const AttributeMap& command) {
    std::cout << "Received DoCommand request for MyBase " << Resource::name() << std::endl;
    return command;
}

std::vector<GeometryConfig> MyBase::get_geometries(const AttributeMap& extra) {
    auto left_geometries = left_->get_geometries(extra);
    auto right_geometries = right_->get_geometries(extra);
    std::vector<GeometryConfig> geometries(left_geometries);
    geometries.insert(geometries.end(), right_geometries.begin(), right_geometries.end());
    return geometries;
}

Base::properties MyBase::get_properties(const AttributeMap& extra) {
    // Return fake properties.
    return {2, 4, 8};
}
```

</details>
<br>
<details>
  <summary>Click to view sample code for the <file>my_base.hpp</file> header file</summary>

```cpp {class="line-numbers linkable-line-numbers"}
#pragma once

#include <viam/sdk/components/base/base.hpp>
#include <viam/sdk/components/component.hpp>
#include <viam/sdk/components/motor/motor.hpp>
#include <viam/sdk/config/resource.hpp>
#include <viam/sdk/resource/resource.hpp>

using namespace viam::sdk;

// `MyBase` inherits from the `Base` class defined in the viam C++ SDK and
// implements some of the relevant methods along with `reconfigure`. It also
// specifies a static `validate` method that checks config validity.
class MyBase : public Base {
   public:
    MyBase(Dependencies deps, ResourceConfig cfg) : Base(cfg.name()) {
        this->reconfigure(deps, cfg);
    };
    void reconfigure(Dependencies deps, ResourceConfig cfg) override;
    static std::vector<std::string> validate(ResourceConfig cfg);

    bool is_moving() override;
    void stop(const AttributeMap& extra) override;
    void set_power(const Vector3& linear,
                   const Vector3& angular,
                   const AttributeMap& extra) override;

    AttributeMap do_command(const AttributeMap& command) override;
    std::vector<GeometryConfig> get_geometries(const AttributeMap& extra) override;
    Base::properties get_properties(const AttributeMap& extra) override;

    void move_straight(int64_t distance_mm, double mm_per_sec, const AttributeMap& extra) override {
        throw std::runtime_error("move_straight unimplemented");
    }
    void spin(double angle_deg, double degs_per_sec, const AttributeMap& extra) override {
        throw std::runtime_error("spin unimplemented");
    }
    void set_velocity(const Vector3& linear,
                      const Vector3& angular,
                      const AttributeMap& extra) override {
        throw std::runtime_error("set_velocity unimplemented");
    }

   private:
    std::shared_ptr<Motor> left_;
    std::shared_ptr<Motor> right_;
};
```

</details>
<br>

Additional example modules are available in the [C++ SDK GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/examples/).

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

If you do not wish to implement all methods, raise a `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.

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

If you do not wish to implement all methods, raise an `errUnimplemented` error for the functions you do not want to implement.

Additionally, return any values designated in the function's return signature, typed correctly.

{{% /alert %}}

{{% /tab %}}
{{% tab name="C++" %}}

The main program starts the module.
<file>main.cpp</file> is the module's entry point file.

Import your custom model and API into the main program and register them with the C++ SDK.
When executed, the main program registers the `MyBase` custom model custom model and API helper functions with the C++ SDK, using the model family `acme:demo:mybase`, and creates and starts the new module.

<details>
  <summary>Click to view sample code for <file>main.cpp</file></summary>

```cpp {class="line-numbers linkable-line-numbers"}
#include <memory>
#include <signal.h>

#include <boost/log/trivial.hpp>
#include <grpcpp/grpcpp.h>
#include <grpcpp/server_context.h>

#include <viam/api/common/v1/common.grpc.pb.h>
#include <viam/api/component/generic/v1/generic.grpc.pb.h>
#include <viam/api/robot/v1/robot.pb.h>

#include <viam/sdk/components/base/base.hpp>
#include <viam/sdk/components/component.hpp>
#include <viam/sdk/config/resource.hpp>
#include <viam/sdk/module/module.hpp>
#include <viam/sdk/module/service.hpp>
#include <viam/sdk/registry/registry.hpp>
#include <viam/sdk/resource/resource.hpp>
#include <viam/sdk/rpc/dial.hpp>
#include <viam/sdk/rpc/server.hpp>

#include "base.hpp"

using namespace viam::sdk;

int main(int argc, char** argv) {
    API base_api = Base::static_api();
    Model mybase_model("acme", "demo", "mybase");

    std::shared_ptr<ModelRegistration> mybase_mr = std::make_shared<ModelRegistration>(
        base_api,
        mybase_model,
        [](Dependencies deps, ResourceConfig cfg) { return std::make_unique<MyBase>(deps, cfg); },
        MyBase::validate);

    std::vector<std::shared_ptr<ModelRegistration>> mrs = {mybase_mr};
    auto my_mod = std::make_shared<ModuleService>(argc, argv, mrs);
    my_mod->serve();

    return EXIT_SUCCESS;
};
```

</details>

{{% alert title="Important" color="note" %}}

You must define all _pure virtual methods_ belonging to a built-in resource subtype's API if defining a new model.
Otherwise, the class will not instantiate.
For example, you would need to implement the [`move_straight()` virtual method](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base/base.hpp#L72) for the `base` component, but you would not need to implement [`resource_registration()`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base/base.hpp#L56).

If you do not wish to implement all methods, `throw` a `runtime_error` in the body of functions you do not want to implement.

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

Make sure to [prepare a Python virtual environment](/build/program/python-venv/) in the directory your module is in to ensure your module has access to any required libraries:

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
Make sure to [prepare a Python virtual environment](/build/program/python-venv/) in the directory your module is in to ensure your module has access to any required libraries.
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
   You have to compile on your target architecture.

{{% /tab %}}
{{% tab name="Python: pyinstaller" %}}

Make sure to [prepare a Python virtual environment](/build/program/python-venv/) in the directory your module is so your module has access to any required libraries.
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
   You have to compile on your target architecture.

{{% /tab %}}
{{% tab name="Go" %}}

Use Go to [compile](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) and obtain a single executable for your module:

- Navigate to your module directory in your terminal.
- Run `go build` to compile your entry point (main program) file <file>main.go</file> and all other <file>.go</file> files in the directory, building your module and all dependencies into a single executable file.
- Run `ls` in your module directory to find the executable, which should have the same name as the module directory.

<file>main.go</file> adds the custom model <file>mybase.go</file> from the resource registry, while <file>mybase.go</file> defines and registers the module.
Expand the [Go module code](#code-a-main-entry-point-program) to view <file>main.go</file> for an example of this.

{{% /tab %}}
{{% tab name="C++" %}}

To compile your C++ module's executable, you must create a <file>CMakeLists.txt</file> file to handle compilation configuration, a <file>run.sh</file> file to wrap your executable, and then compile the executable using the C++ SDK build steps.

1. Create a <file>CMakeLists.txt</file> file in your module directory to instruct the compiler how to compile your module.

   The following example shows a basic configuration that automatically downloads the C++ SDK and handles compile-time linking for a module named `my-module`:

   ```cpp {class="line-numbers linkable-line-numbers"}
   cmake_minimum_required(VERSION 3.7 FATAL_ERROR)

   project(my-module LANGUAGES CXX)

   set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

   include(FetchContent)
   FetchContent_Declare(
     viam-cpp-sdk
     GIT_REPOSITORY https://github.com/viamrobotics/viam-cpp-sdk.git
     GIT_TAG main
     # SOURCE_DIR ${CMAKE_SOURCE_DIR}/../viam-cpp-sdk
     CMAKE_ARGS -DVIAMCPPSDK_USE_DYNAMIC_PROTOS=ON
     FIND_PACKAGE_ARGS
   )
   FetchContent_MakeAvailable(viam-cpp-sdk)

   FILE(GLOB sources *.cpp)
   add_executable(my-module ${sources})
   target_link_libraries(my-module PRIVATE viam-cpp-sdk::viamsdk)
   ```

2. Create a <file>run.sh</file> file in your module directory to wrap the executable and perform basic sanity checks at runtime.

   The following example shows a simple configuration that performs some basic sanity checks and handles system-level linking for a module named `my-module`:

   ```sh { class="command-line"}
   #!/usr/bin/env bash
   # run.sh -- entrypoint wrapper for the module

   # bash safe mode
   set -euo pipefail

   cd $(dirname $0)
   # get bundled .so files from this directory
   export LD_LIBRARY_PATH=${LD_LIBRARY_PATH-}:$PWD
   exec ./my-module $@
   ```

3. Use C++ to compile and obtain a single executable for your module:

   1. Create a new <file>build</file> directory within your module directory:

      ```sh { class="command-line"}
      mkdir build
      cd build
      ```

   2. Build and compile your module:

      ```sh { class="command-line"}
      cmake .. -G Ninja
      ninja all
      ninja install
      ```

   3. Run `ls` in your module's <file>build</file> directory to find the compiled executable, which should have the same name as the module directory (`my-module` in these examples):

For more information on building a module in C++, see the [C++ SDK Build Documentation](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

<file>main.cpp</file> adds the custom model <file>mybase.cpp</file> from the resource registry, while <file>mybase.cpp</file> defines and registers the module.
Expand the [C++ module code](#code-a-main-entry-point-program) to view <file>main.cpp</file> for an example of this.

{{% /tab %}}
{{% /tabs %}}

### Configure logging

To enable your module to write logs to the [Viam app](https://app.viam.com/), ensure that you have added the following lines of code to your respective module code.
Log messages are sent to the Viam app and appear under the [**Logs** tab](/fleet/machines/#logs) for your machine.

{{< tabs name="Configure logging">}}
{{% tab name="Python"%}}

To enable your Python module to write log messages to the Viam app, add the following lines to your code:

```python {class="line-numbers linkable-line-numbers" data-line="2,5"}
# In your import block, import the logging package:
from viam.logging import getLogger

# Before your first class or function, define the LOGGER variable:
LOGGER = getLogger(__name__)
```

{{% /tab %}}
{{% tab name="Go"%}}

To enable your Go module to write log messages to the Viam app, add the following lines to your code:

```go {class="line-numbers linkable-line-numbers"}
// In your import() block, import the logging package:
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
{{% tab name="C++" %}}

Messages sent to `std::cout` in your C++ code are automatically sent to the Viam app over gRPC when a network connection is available.

We recommend that you use a C++ logging library to assist with log message format and creation, such as the Boost trivial logger:

```cpp {class="line-numbers linkable-line-numbers"}
#include <boost/log/trivial.hpp>
```

{{% /tab %}}
{{< /tabs >}}

The examples from [Code a new resource model](#code-a-new-resource-model) include this logging setup.

## Next steps

Once you have created your module, you can use the [Viam CLI](/fleet/cli/) to [upload your module](/registry/upload/) to the [Viam registry](https://app.viam.com/registry) to share it with other Viam users or just to other users in your organization.
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
