---
title: "How to create and deploy a new module"
linkTitle: "Create a module"
type: "docs"
weight: 25
images: ["/registry/module-puzzle-piece.svg"]
tags: ["modular resources", "components", "services", "registry"]
description: "Add a custom resource by creating and deploying a module to your machine."
aliases:
  - /registry/create/
  - /registry/upload/
  - /extend/modular-resources/upload/
  - /modular-resources/upload/
---

{{<imgproc src="/registry/module-diagram.png" resize="x900" declaredimensions=true alt="Representation of the Viam registry, some modules within it, and a rover they support." >}}
<br>

Viam provides built-in support for a variety of different {{< glossary_tooltip term_id="component" text="components" >}} and {{< glossary_tooltip term_id="service" text="services" >}}, but you can add support for your own [custom {{< glossary_tooltip term_id="resource" text="resources" >}}](/registry/) by creating a {{< glossary_tooltip term_id="module" text="module" >}}.

You can search the [Viam Registry](https://app.viam.com/registry) and [deploy an existing module to your machine](/registry/configure/) in a few clicks if you find one that meets your needs.
If no existing modules support your specific use case, you can write your own module, and either upload it to the Viam registry to share with others, or deploy it to your machine as a local module without uploading it to the registry.

Follow the instructions below to learn how to write a new module using your preferred language and its corresponding [Viam SDK](/sdks/), and then deploy it to your machines.

{{% alert title="In this page" color="tip" %}}

1. [Write a custom module to support a new resource.](#write-a-module)
1. [Test your module locally.](#test-your-module-locally)
1. [Upload your module to the modular resource registry.](#upload-your-module-to-the-modular-resource-registry)
1. [Deploy your module on more machines.](#deploy-your-module-to-more-machines)

{{% /alert %}}

{{< alert title="Note: Micro-RDK modules" color="note" >}}
The [micro-RDK](/get-started/installation/#install-micro-rdk) works differently from the RDK (and `viam-server`), so creating modular resources for it is different from the process described on this page.
Refer to the [Micro-RDK Module Template on GitHub](https://github.com/viamrobotics/micro-rdk/tree/main/templates/module) for information on how to create custom resources for your micro-RDK machine.
You will need to [recompile and flash your ESP32 yourself](/get-started/installation/#install-micro-rdk) instead of using Viam's prebuilt binary and installer.
{{< /alert >}}

You can also watch this guide to creating a vision service module:

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/Yz6E07To9Mc">}}

## Write a module

Generally, to write a module, you will complete the following steps:

1. Choose a Viam API to implement in your model.
1. Write your new model definition code to map all the capabilities of your model to the API.
1. Write an entry point (main program) file that registers your model with the Viam SDK and starts it up.
1. Compile or package the model definition file or files, main program file, and any supporting files into a single executable file (a module) that can be run by `viam-server`.

While you can certainly combine the resource model definition and the main program code into a single file if desired (for example, a single `main.py` program that includes both the model definition and the `main()` program that uses it), this guide will use separate files for each.

### Choose an API to implement in your model

Look through the [component API](/appendix/apis/#component-apis) and [service API](/appendix/apis/#service-apis) and find the API that best fits your use case.
Each API contains various methods which you will need to define in your module:

- One or more methods specific to that API, such as the servo component's `Move` and `GetPosition` methods.
- Inherited [ResourceBase methods](/appendix/apis/#resourcebase-methods) such as `DoCommand` and `Close`, common to all Viam {{< glossary_tooltip term_id="resource" text="resource" >}} APIs.
- (For some APIs) Other inherited methods, for example all actuator APIs such as the motor API and servo API inherit `IsMoving` and `Stop`.

{{< expand "Click for more guidance" >}}
Think about what functionality you want your module to provide, what methods you need, and choose an API to implement accordingly.
For example, the [sensor API](/appendix/apis/#sensor) has a `GetReadings` method, so if you create a module for a model of sensor, you'll need to write code to provide a response to the `GetReadings` method.
If instead of just getting readings, you actually have an encoder and need to be able to reset the zero position, use the [encoder API](/appendix/apis/#encoder) so you can define functionality behind the `GetPosition` and `ResetPosition` methods.

In addition to the list of methods, another reason to choose one API over another is how certain APIs fit into the Viam ecosystem.
For example, though you could technically implement a GPS as a sensor with just the `GetReadings` method, if you implement it as a movement sensor then you have access to methods like `GetCompassHeading` which allow you to use your GPS module with the [navigation service](/services/navigation/).
For this reason, it's generally best to choose the API that most closely matches your hardware or software.
{{< /expand >}}

{{% alert title=Note color="note" %}}
If you want to write a module to add support to a new type of component or service that is relatively unique, consider using the generic API for your resource type to build your own API:

- If you are working with a component that doesn't fit into any of the existing component APIs, you can use the [generic component](/components/generic/) to build your own component API.
- If you are designing a service that doesn't fit into any of the existing service APIs, you can use the [generic service](/services/generic/) to build your own service API.
- It is also possible to [define an entirely new API](/registry/advanced/create-subtype/), but this is even more advanced than using `generic`.

Most module use cases, however, benefit from implementing an existing API instead of `generic`.
{{% /alert %}}

#### Valid API identifiers

Each existing component or service API has a unique identifier in the form of a colon-delimited triplet.
You will use this {{< glossary_tooltip term_id="api-namespace-triplet" text="API namespace triplet" >}} when creating your new model, to indicate which API it uses.

The API namespace triplet is the same for all built-in and modular models that implement a given API.
For example, every model of motor built into Viam, as well as every custom model of motor provided by a module, all use the same API namespace triplet `rdk:component:motor` to indicate that they implement the [motor API](/components/motor/#api).

The three pieces of the API namespace triplet are as follows:

{{< tabs >}}
{{% tab name="Component" %}}

- `namespace`: `rdk`
- `type`: `component`
- `subtype`: any one of [these component proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/component), for example `motor` if you are creating a new model of motor

{{% /tab %}}
{{% tab name="Service" %}}

- `namespace`: `rdk`
- `type`: `service`
- `subtype`: any one of [these service proto files](https://github.com/viamrobotics/api/tree/main/proto/viam/service), for example `vision` if you are creating a new model of vision service

{{% /tab %}}
{{< /tabs >}}

### Name your new resource model

In addition to determining which existing API namespace triplet to use when creating your module, you need to decide on a separate triplet unique to your model.

A resource model is identified by a unique name, often called the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet" >}}, using the format: `namespace:repo-name:model-name`, where:

- `namespace` is the [namespace of your organization](/cloud/organizations/#create-a-namespace-for-your-organization).
  - For example, if your organization uses the `acme` namespace, your models must all begin with `acme`, like `acme:repo-name:mybase`.
    If you do not intend to [upload your module](#upload-your-module-to-the-modular-resource-registry) to the [Viam registry](https://app.viam.com/registry), you do not need to use your organization's namespace as your model's namespace.
- `repo-name` is the code repository (GitHub repo) that houses your module code.
  - Ideally, your `repo-name` should describe the common functionality provided across the model or models of that module.
- `model-name` is the name of the new resource model that your module will provide.

For example, if your organization namespace is `acme`, and you have written a new base implementation named `mybase` which you have pushed to a repository named `my-custom-base-repo`, you would use the namespace `acme:my-custom-base-repo:mybase` for your model.

More requirements:

- Your model triplet must be all-lowercase.
- Your model triplet may only use alphanumeric (`a-z` and `0-9`), hyphen (`-`), and underscore (`_`) characters.

Determine the model name you want to use based on these requirements, then proceed to the next section.

#### API namespace triplet and model namespace triplet examples

- The `rand:yahboom:arm` model and the `rand:yahboom:gripper` model use the repository name [yahboom](https://github.com/viam-labs/yahboom).
  The models implement the `rdk:component:arm` and the `rdk:component:gripper` API to support the Yahboom DOFBOT arm and gripper, respectively:

  ```json
  {
      "api": "rdk:component:arm",
      "model": "rand:yahboom:arm"
  },
  {
      "api": "rdk:component:gripper",
      "model": "rand:yahboom:gripper"
  }
  ```

- The `viam-labs:audioout:pygame` model uses the repository name [audioout](https://github.com/viam-labs/audioout).
  It implements the custom API `viam-labs:service:audioout`:

  ```json
  {
    "api": "viam-labs:service:audioout",
    "model": "viam-labs:audioout:pygame"
  }
  ```

The `viam` namespace is reserved for models provided by Viam.

### Write your new resource model definition

In this step, you will code the logic that is unique to your model.

{{% alert title="Tip (optional)" color="tip" %}}

If you are using Golang, use the [Golang Module templates](https://github.com/viam-labs/module-templates-golang) which contain detailed instructions for creating your module.

If you are using Python, you can use the [Viam module generator](https://github.com/viam-labs/generator-viam-module/tree/main) to generate the scaffolding for a module with one resource model.

{{% /alert %}}

{{< expand "Additional example modules" >}}

Browse additional example modules by language:

{{< tabs >}}
{{% tab name="Python" %}}

<!-- prettier-ignore -->
| Module | Repository | Description |
| ------ | ---------- | ----------- |
| [monocular-visual-odometry](https://app.viam.com/module/viam/monocular-visual-odometry) | [viamrobotics/viam-visual-odometry](https://github.com/viamrobotics/viam-visual-odometry) | Extends the built-in [movement sensor API](/components/movement-sensor/#api) to support using monocular visual odometry to enable any calibrated camera to function as a movement sensor. |
| [oak](https://app.viam.com/module/viam/oak) | [viamrobotics/viam-camera-oak](https://github.com/viamrobotics/viam-camera-oak) | Extends the built-in [camera API](/components/camera/#api) to support OAK cameras. |
| [odrive](https://app.viam.com/module/viam/odrive) | [viamrobotics/odrive](https://github.com/viamrobotics/odrive) | Extends the built-in [motor API](/components/motor/#api) to support the ODrive motor. This module provides two models, one for a `canbus`-connected ODrive motor, and one for a `serial`-connected ODrive motor. |
| [yahboom](https://app.viam.com/module/rand/yahboom) | [viamlabs/yahboom](https://github.com/viam-labs/yahboom) | Extends the built-in [arm API](/components/arm/#api) and [gripper API](/components/gripper/#api) to support the Yahboom Dofbot robotic arm. |

For more Python module examples:

- See the [Python SDK `examples` directory](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples) for sample module code of varying complexity.
- For tutorials featuring modular resource creation, see the [Modular resource examples](/registry/examples/) page.
- For an example featuring a sensor, see [MCP300x](https://github.com/viam-labs/mcp300x-adc-sensor).
- For additional examples use the [modular resources search](/registry/#modular-resources) to search for examples of the model you are implementing, and click on the model's link to be able to browse its code.

{{% /tab %}}
{{% tab name="Go" %}}

<!-- prettier-ignore -->
| Module | Repository | Description |
| ------ | ---------- | ----------- |
| [agilex-limo](https://app.viam.com/module/viam/agilex-limo) | [viamlabs/agilex](https://github.com/viam-labs/agilex/) | Extends the built-in [base API](/components/base/#api) to support the Agilex Limo base. |
| [rplidar](https://app.viam.com/module/viam/rplidar) | [viamrobotics/rplidar](https://github.com/viamrobotics/rplidar) | Extends the built-in [camera API](/components/camera/#api) to support several models of the SLAMTEC RPlidar. |
| [filtered-camera](https://app.viam.com/module/erh/filtered-camera) | [erh/filtered_camera](https://github.com/erh/filtered_camera) | Extends the built-in [camera API](/components/camera/#api) to enable filtering captured images by comparing to a defined ML model, and only syncing matching images to the Viam app. See the [filtered-camera tutorial](/tutorials/projects/filtered-camera/) for more information. |

For more Go module examples:

- See the [Go SDK `examples` directory](https://github.com/viamrobotics/rdk/blob/main/examples/) for sample module code of varying complexity.
- For additional examples use the [modular resources search](/registry/#modular-resources) to search for examples of the model you are implementing, and click on the model's link to be able to browse its code.

{{% /tab %}}
{{% tab name="C++" %}}

<!-- prettier-ignore -->
| Module | Repository | Description |
| ------ | ---------- | ----------- |
| [csi-cam](https://app.viam.com/module/viam/csi-cam) | [viamrobotics/csi-camera](https://github.com/viamrobotics/csi-camera/) | Extends the built-in [camera API](/components/camera/#api) to support the Intel CSI camera. |
<!-- | [module-example-cpp](https://app.viam.com/module/viam/module-example-cpp) | [viamrobotics/module-example-cpp](https://github.com/viamrobotics/module-example-cpp) | Extends the built-in [sensor API](/components/sensor/#api) to report wifi statistics. | -->

{{% /tab %}}
{{% /tabs %}}

Explore the full list of available modules in the [Viam registry](https://app.viam.com/registry).
{{< /expand >}}

Follow the instructions below to define the capabilities provided by your model, for the language you are using to write your module code:

{{% alert title="Note: Pin numbers" color="note" %}}

If your module references {{< glossary_tooltip term_id="pin-number" text="pin numbers" >}}, you should use physical board pin numbers, _not_ GPIO (BCM) numbers, to maintain consistency across {{< glossary_tooltip term_id="resource" text="resources" >}} from different sources.

{{% /alert %}}

{{< tabs >}}
{{% tab name="Python" %}}

First, inspect the built-in class provided by the resource API that you are extending.

For example, if you wanted to add support for a new [base component](/components/base/) to Viam (the component that represents the central physical platform of your machine, to which all other components are connected), you would start by looking at the built-in `Base` component class, which is defined in the [Viam Python SDK](https://github.com/viamrobotics/viam-python-sdk) in the following file:

<!-- prettier-ignore -->
| Resource Model File | Description |
| ------------------- | ----------- |
| [src/viam/components/base/base.py](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/base.py) | Defines the built-in `Base` class, which includes several built-in methods such as `move_straight()`. |

{{% alert title="Tip" color="tip" %}}
You can view the other built-in component classes in similar fashion.
For example, the `Camera` class is defined in [camera.py](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/camera/camera.py) and the `Sensor` class is defined in [sensor.py](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/sensor/sensor.py).
The same applies to service APIs.
For example, the `MLModel` class for the ML Model service is defined in [mlmodel.py](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/services/mlmodel/mlmodel.py).
{{% /alert %}}

Take note of the methods defined as part of the class API, such as `move_straight()` for the `Base` class.
Your new resource model must either:

- implement all of the methods that the corresponding resource API provides, or
- explicitly raise a `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.

Otherwise, your new class will not instantiate.

Next, create a file that will define your new resource model.
This file will inherit from the existing class for your resource type, implement each built-in method for that class (or raise a `NotImplementedError()` for it), and define any new functionality you want to include as part of your model.

For example, the following file, `my_base.py`:

- defines a new model `acme:my-custom-base-repo:mybase` by implementing a new `MyBase` class, which inherits from the built-in class `Base`.
- defines a new constructor `new_base()` and a new method `validate_config()`.
- does not implement several built-in methods, including `get_properties()` and `set_velocity()`, but instead raises a `NotImplementedError` error in the body of those functions.
  This prevents these methods from being used by new base components that use this modular resource, but meets the requirement that all built-in methods either be defined or raise a `NotImplementedError()` error, to ensure that the new `MyBase` class successfully instantiates.

{{< expand "Click to view sample code for my_base.py" >}}

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

    # Here is where we define our new model's colon-delimited-triplet:
    # acme:my-custom-base-repo:mybase
    # acme = namespace, my-custom-base-repo = repo-name, mybase = model name.
    MODEL: ClassVar[Model] = Model(
        ModelFamily("acme", "my-custom-base-repo"), "mybase")

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

{{< /expand >}}

When implementing built-in methods from the Viam Python SDK in your model, be sure your implementation of those methods returns any values designated in the built-in function's return signature, typed correctly.
For example, the `is_moving()` implementation in the example code above returns a `bool` value, which matches the return value of the built-in `is_moving()` function as defined in the Viam Python SDK in the file [`base.py`](https://github.com/viamrobotics/viam-python-sdk/blob/main/src/viam/components/base/base.py).

For more information on the base component API methods used in this example, see the following resources:

- [Python SDK documentation for the `Base` class](https://python.viam.dev/autoapi/viam/components/base/index.html)
- [Base API methods](/components/base/#api)

{{% /tab %}}
{{% tab name="Go"%}}

First, inspect the built-in package provided by the resource API that you are extending.

For example, if you wanted to add support for a new [base component](/components/base/) to Viam (the component that represents the central physical platform of your machine, to which all other components are connected), you would start by looking at the built-in `base` component package, which is defined in the [Viam Go SDK](https://github.com/viamrobotics/rdk/) in the following file:

<!-- prettier-ignore -->
| Resource Model File | Description |
| ------------------- | ----------- |
| [components/base/base.go](https://github.com/viamrobotics/rdk/blob/main/components/base/base.go) | Defines the built-in `base` package, which includes several built-in methods such as `MoveStraight()`. |

{{% alert title="Tip" color="tip" %}}
You can view the other built-in component packages in similar fashion.
For example, the `camera` package is defined in [camera.go](https://github.com/viamrobotics/rdk/blob/main/components/camera/camera.go) and the `sensor` package is defined in [sensor.go](https://github.com/viamrobotics/rdk/blob/main/components/sensor/sensor.go).
The same applies to service APIs.
For example, the `mlmodel` package for the ML Model service is defined in [mlmodel.go](https://github.com/viamrobotics/rdk/blob/main/services/mlmodel/mlmodel.go).
{{% /alert %}}

Take note of the methods defined as part of the package API, such as `MoveStraight()` for the `base` package.
Your new resource model must either:

- implement all of the methods that the corresponding resource API provides, or
- explicitly return an `errUnimplemented` error in the body of functions you do not want to implement.

Otherwise, your new package will not instantiate.

Next, create a file that will define your new resource model.
This file will inherit from the existing package for your resource type, implement - or return an `errUnimplemented` error for - each built-in method for that package, and define any new functionality you want to include as part of your model.

For example, the following file, `mybase.go`:

- defines a new model `acme:my-custom-base-repo:mybase` by implementing a new `mybase` package, which inherits from the built-in package `base`.
- defines a new constructor `newBase()` and a new method `Validate()`.
- does not implement several built-in methods, including `MoveStraight()` and `SetVelocity()`, but instead returns an `errUnimplemented` error in the body of those methods.
  This prevents these methods from being used by new base components that use this modular resource, but meets the requirement that all built-in methods either be defined or return an `errUnimplemented` error, to ensure that the new `mybase` package successfully instantiates.

{{< expand "Click to view sample code for mybase.go" >}}

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

// Here is where we define your new model's colon-delimited-triplet (acme:my-custom-base-repo:mybase)
// acme = namespace, my-custom-base-repo = repo-name, mybase = model name.
var (
    Model            = resource.NewModel("acme", "my-custom-base-repo", "mybase")
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
        b.logger.CWarnf(ctx, "base %v %s", b.Name(), err.Error())
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
    // this makes them required for the model to successfully build
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
    b.logger.CDebugf(ctx, "SetPower Linear: %.2f Angular: %.2f", linear.Y, angular.Z)
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
    b.logger.CDebug(ctx, "Stop")
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

{{< /expand >}}

{{< alert title="Note" color="note" >}}
For an example featuring a sensor, see [MCP3004-8](https://github.com/mestcihazal/mcp3004-8-go).

For additional examples use the [modular resources search](/registry/#modular-resources) to search for examples of the model you are implementing, and click on the model's link to be able to browse its code.
{{< /alert >}}

When implementing built-in methods from the Viam Go SDK in your model, be sure your implementation of those methods returns any values designated in the built-in method's return signature, typed correctly.
For example, the `SetPower()` implementation in the example code above returns a `multierr` value (as provided by the [`multierr` package](https://pkg.go.dev/go.uber.org/multierr)), which allows for transparently combining multiple Go `error` return values together.
This matches the `error` return type of the built-in `SetPower()` method as defined in the Viam Go SDK in the file [`base.go`](https://github.com/viamrobotics/rdk/blob/main/components/base/base.go).

For more information on the base component API methods used in this example, see the following resources:

- [Go SDK documentation for the `base` package](https://pkg.go.dev/go.viam.com/rdk/components/base#pkg-functions)
- [Base API methods](/components/base/#api)

{{% /tab %}}
{{% tab name="C++" %}}

First, inspect the built-in class provided by the resource API that you are extending.
In the C++ SDK, all built-in classes are abstract classes.

For example, if you wanted to add support for a new [base component](/components/base/) to Viam (the component that represents the central physical platform of your machine, to which all other components are connected), you would start by looking at the built-in `Base` component class, which is defined in the [Viam C++ SDK](https://cpp.viam.dev/) in the following files:

<!-- prettier-ignore -->
| Resource Model File | Description |
| ------------------- | ----------- |
| [components/base/base.hpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base.hpp) | Defines the API of the built-in `Base` class, which includes the declaration of several purely virtual built-in functions such as `move_straight()`. |
| [components/base/base.cpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base.cpp) | Provides implementations of the non-purely virtual functionality defined in `base.hpp`. |

{{% alert title="Tip" color="tip" %}}
You can view the other built-in component classes in similar fashion.
For example, the API of the built-in `Camera` class is defined in [camera.hpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/camera.hpp) and its non-purely virtual functions are declared in [camera.cpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/camera.cpp), while the API of the built-in `Sensor` class is defined in [sensor.hpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/sensor.hpp) and its non-purely virtual functions are declared in [sensor.cpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/sensor.cpp).
The same applies to service APIs.
For example, the API of the built-in `MLModelService` class for the ML Model service is defined in [mlmodel.hpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/services/mlmodel.hpp) and its non-purely virtual functions declared in [mlmodel.cpp](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/services/mlmodel.cpp).
{{% /alert %}}

Take note of the functions defined as part of the class API, such as `move_straight()` for the `Base` class.
Your new resource model must either:

- define all _pure virtual methods_ that the corresponding resource API provides, or
- explicitly `throw` a `runtime_error` in the body of functions you do not want to implement.

Otherwise, your new class will not instantiate.
For example, if your model implements the `base` class, you would either need to implement the [`move_straight()` virtual method](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base.hpp#L72), or `throw` a `runtime_error` in the body of that function.
However, you would _not_ need to implement the [`resource_registration()`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base.hpp#L56) function, as it is not a virtual method.

Next, create your header file (`.hpp`) and source file (`.cpp`), which together define your new resource model.
The header file defines the API of your class, and includes the declaration of any purely virtual functions, while the source file includes implementations of the functionality of your class.

For example, the files below define the new `MyBase` class and its constituent functions:

- The `my_base.hpp` header file defines the API of the `MyBase` class, which inherits from the built-in `Base` class.
  It defines a new method `validate()`, but does not implement several built-in functions, including `move_straight()` and `set_velocity()`, instead it raises a `runtime_error` in the body of those functions.
  This prevents these functions from being used by new base components that use this modular resource, but meets the requirement that all built-in functions either be defined or `throw` a `runtime_error` error, to ensure that the new `MyBase` class successfully instantiates.
- The `my_base.cpp` source file contains the function and object definitions used by the `MyBase` class.

Note that the model triplet itself, `acme:my-custom-base-repo:mybase` in this example, is defined in the entry point (main program) file `main.cpp`, which is described in the next section.

{{< expand "Click to view sample code for the my_base.hpp header file" >}}

```cpp {class="line-numbers linkable-line-numbers"}
#pragma once

#include <viam/sdk/components/base/base.hpp>
#include <viam/sdk/components/component.hpp>
#include <viam/sdk/components/motor/motor.hpp>
#include <viam/sdk/config/resource.hpp>
#include <viam/sdk/resource/resource.hpp>

using namespace viam::sdk;

// `MyBase` inherits from the `Base` class defined in the Viam C++ SDK and
// implements some of the relevant methods along with `reconfigure`. It also
// specifies a static `validate` method that checks configuration validity.
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

{{< /expand >}}

{{< expand "Click to view sample code for the my_base.cpp source file" >}}

```cpp {class="line-numbers linkable-line-numbers"}
#include "my_base.hpp"

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
    // time of resource registration (see main.cpp) like this one.
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

{{< /expand >}}

When implementing built-in functions from the Viam C++ SDK in your model, be sure your implementation of those functions returns any values designated in the built-in function's return signature, typed correctly.
For example, the `set_power()` implementation in the example code above returns three values of type `Vector3`, `Vector3`, `AttributeMap`, which matches the return values of the built-in `set_power()` function as defined in the Viam C++ SDK in the file [`base.hpp`](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/src/viam/sdk/components/base.hpp).

For more information on the base component API methods used in these examples, see the following resources:

- [C++ SDK documentation for the `Base` class](https://cpp.viam.dev/classviam_1_1sdk_1_1Base.html)
- [Base API methods](/components/base/#api)

For more C++ module examples of varying complexity,see the [C++ SDK `examples` directory](https://github.com/viamrobotics/viam-cpp-sdk/tree/main/src/viam/examples/modules/).

{{% /tab %}}
{{< /tabs >}}

### Write an entry point (main program) file

A main entry point file starts the module, and adds the resource model.

Follow the instructions below for the language you are using to write your module code:

{{< tabs name="Sample SDK Main Program Code">}}
{{% tab name="Python"%}}

Create a <file>main.py</file> file to serve as the module's entry point file, which:

- imports the custom model
- defines a `main()` function that registers the model with the Python SDK
- creates and starts the module

For example, the following `main.py` file serves as the entry point file for the `MyBase` custom model.
It imports the `MyBase` model from the `my_base.py` file that provides it, and defines a `main()` function that registers it.

{{< expand "Click to view sample code for main.py" >}}

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

{{< /expand >}}

{{% /tab %}}
{{% tab name="Go"%}}

Create a <file>main.go</file> file to serve as the module's entry point file, which:

- imports the custom model
- defines a `main()` function that registers the model with the Viam Go SDK
- creates and starts the module

For example, the following `main.go` file serves as the entry point file for the `mybase` custom model.
It imports the `mybase` model from the `my_base.go` file that provides it, and defines a `main()` function that registers it.

{{< expand "Click to view sample code for main.go" >}}

```go {class="line-numbers linkable-line-numbers"}
// Package main is a module which serves the mybase custom model.
package main

import (
    "context"

    "go.viam.com/rdk/components/base"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/utils"

    // Import your local package "mybase"
    // NOTE: Update this path if your custom resource is in a different location,
    // or has a different name:
    "go.viam.com/rdk/examples/customresources/models/mybase"
)

func main() {
    // NewLoggerFromArgs will create a logging.Logger at "DebugLevel" if
    // "--log-level=debug" is an argument in os.Args and at "InfoLevel" otherwise.
    utils.ContextualMain(mainWithArgs, module.NewLoggerFromArgs("mybase"))
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

{{< /expand >}}

{{% /tab %}}
{{% tab name="C++" %}}

Create a <file>main.cpp</file> file to serve as the module's entry point file, which:

- imports the custom model implementation and definitions
- includes a `main()` function that registers the model with the Viam C++ SDK
- creates and starts the module

For example, the following `main.cpp` file serves as the entry point file for the `mybase` custom model.
It imports the `mybase` model implementation from the `my_base.hpp` file that provides it, declares the model triplet `acme:my-custom-base-repo:mybase`, and defines a `main()` function that registers it.

{{< expand "Click to view sample code for main.cpp" >}}

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

#include "my_base.hpp"

using namespace viam::sdk;

int main(int argc, char** argv) {
    API base_api = Base::static_api();
    Model mybase_model("acme", "my-custom-base-repo", "mybase");

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

{{< /expand >}}

{{% /tab %}}
{{< /tabs >}}

#### (Optional) Configure logging

If desired, you can configure your module to output log messages to the [Viam app](https://app.viam.com/).
Log messages sent to the Viam app appear under the [**LOGS** tab](/cloud/machines/#logs) for your machine in an easily-parsable and searchable manner.

Log messages generated when your machine is offline are queued, and sent together when your machine connects to the internet once more.

Add the following code to your module code to enable logging to the Viam app, depending on the language you using to code your module. You can log in this fashion from the model definition file or files, the entry point (main program) file, or both, depending on your logging needs:

{{% alert title="Tip" color="tip" %}}
The example code shown above under [Write your new resource model definition](#write-your-new-resource-model-definition) includes the requisite logging code already.
{{% /alert %}}

{{< tabs name="Configure logging">}}
{{% tab name="Python"%}}

To enable your Python module to write log messages to the Viam app, add the following lines to your code:

```python {class="line-numbers linkable-line-numbers" data-line="2,5"}
# In your import block, import the logging package:
from viam.logging import getLogger

# Before your first class or function, define the LOGGER variable:
LOGGER = getLogger(__name__)

# in some method, log information
LOGGER.debug("debug info")
LOGGER.info("info info")
LOGGER.warn("warn info")
LOGGER.error("error info")
LOGGER.exception("error info", exc_info=True)
LOGGER.critical("critical info")
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
fn (c *component) someFunction(ctx context.Context, a int) {
  // Log with severity info:
  c.logger.CInfof(ctx, "performing some function with a=%v", a)
  // Log with severity debug (using value wrapping):
  c.logger.CDebugw(ctx, "performing some function", "a" ,a)
  // Log with severity warn:
  c.logger.CWarnw(ctx, "encountered warning for component", "name", c.Name())
  // Log with severity error without a parameter:
  c.logger.CError(ctx, "encountered an error")
}
```

{{% /tab %}}
{{% tab name="C++" %}}

`viam-server` automatically gathers all output sent to the standard output (`STDOUT`) in your C++ code and forwards it to the Viam app when a network connection is available.

We recommend that you use a C++ logging library to assist with log message format and creation, such as the [Boost trivial logger](https://www.boost.org/doc/libs/1_84_0/libs/log/doc/html/log/tutorial/trivial_filtering.html):

```cpp {class="line-numbers linkable-line-numbers"}
#include <boost/log/trivial.hpp>
```

{{% /tab %}}
{{< /tabs >}}

### Compile or package your module

The final step to creating a new module is to create an executable file that `viam-server` can use to run your module on demand.

This executable file:

- runs your module when executed
- takes a local UNIX socket as a command line argument
- exits cleanly when sent a termination signal

Depending on the language you are using to code your module, you may have options for how you create your executable file:

{{% tabs %}}
{{% tab name="Python: pyinstaller (recommended)" %}}

The recommended approach for Python is to use [`PyInstaller`](https://pypi.org/project/pyinstaller/) to compile your module into a packaged executable: a standalone file containing your program, the Python interpreter, and all of its dependencies.
When packaged in this fashion, you can run the resulting executable on your desired target platform or platforms without needing to install additional software or manage dependencies manually.

To create a packaged executable:

1. First, [create a Python virtual environment](/build/program/python-venv/) in your module's directory to ensure your module has access to any required libraries.
   Be sure you are within your Python virtual environment for the rest of these steps: your terminal prompt should include the name of your virtual environment in parenthesis.

1. Create a `requirements.txt` file containing a list of all the dependencies your module requires.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`), PyInstaller (`pyinstaller`), and the Google API Python client (`google-api-python-client`) are installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   pyinstaller
   google-api-python-client
   ```

   Add additional dependencies for your module as needed.
   See the [pip `requirements.txt` file documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more information.

1. Install the dependencies listed in your `requirements.txt` file within your Python virtual environment using the following command:

   ```sh { class="command-line" data-prompt="$"}
   python -m pip install -r requirements.txt -U
   ```

1. Then compile your module, adding the Google API Python client as a hidden import:

   ```sh { class="command-line" data-prompt="$"}
   python -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
   ```

   If you need to include any additional data files to support your module, specify them using the `--add-data` flag:

   ```sh { class="command-line" data-prompt="$"}
   python -m PyInstaller --onefile --hidden-import="googleapiclient" --add-data src/arm/my_arm_kinematics.json:src/arm/ src/main.py
   ```

   By default, the output directory for the packaged executable is <file>dist</file>, and the name of the executable is derived from the name of the input script (in this case, main).

We recommend you use PyInstaller with the [`build-action` GitHub action](https://github.com/viamrobotics/build-action) which provides a simple cross-platform build setup for multiple platforms: x86 and Arm Linux distributions, and MacOS.
Follow the instructions to [Update an existing module using a GitHub action](/use-cases/manage-modules/#update-an-existing-module-using-a-github-action) to add the build configuration to your machine.

With this approach, you can make a build script like the following to
build your module, and configure the resulting executable (<file>dist/main</file>) as your module `"entrypoint"`:

```sh { class="command-line"}
#!/bin/bash
set -e

sudo apt-get install -y python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
python3 -m PyInstaller --onefile --hidden-import="googleapiclient" src/main.py
tar -czvf dist/archive.tar.gz dist/main
```

This script automates the process of setting up a Python virtual environment on a Linux arm64 machine, installing dependencies, packaging the Python module into a standalone executable using PyInstaller, and then compressing the resulting executable into a tarball.
For more examples of build scripts see [Update an existing module using a GitHub action](/use-cases/manage-modules/#update-an-existing-module-using-a-github-action).

{{% alert title="Note" color="note" %}}

PyInstaller does not support relative imports in entrypoints (imports starting with `.`).
If you get `"ImportError: attempted relative import with no known parent package"`, set up a stub entrypoint as described on [GitHub](https://github.com/pyinstaller/pyinstaller/issues/2560).

In addition, PyInstaller does not support cross-compiling: you must compile your module on the target architecture you wish to support.
For example, you cannot run a module on a Linux `arm64` system if you compiled it using PyInstaller on a Linux `amd64` system.
Viam makes this easy to manage by providing a build system for modules.
Follow [these instructions](/cli/#using-the-build-subcommand) to automatically build for each system your module can support using Viam's [CLI](/cli/).

{{% /alert %}}

{{% /tab %}}
{{% tab name="Python: venv" %}}

Create a `run.sh` shell script that creates a new Python virtual environment, ensures that the package dependencies your module requires are installed, and runs your module.
This is the recommended approach for modules written in Python:

1. Create a `requirements.txt` file containing a list of all the dependencies your module requires.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`) is installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   ```

   Add additional dependencies for your module as needed.
   See the [pip `requirements.txt` file documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more information.

1. Add a shell script that creates a new virtual environment, installs the dependencies listed in `requirements.txt`, and runs the module entry point file `main.py`:

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

1. Make your shell script executable by running the following command in your terminal:

   ```sh { class="command-line" data-prompt="$"}
   sudo chmod +x <your-file-path-to>/run.sh
   ```

Using a virtual environment together with a `requirements.txt` file and a `run.sh` file that references it ensures that your module has access to any packages it requires during runtime.
If you intend to share your module with other users, or to deploy it to a fleet of machines, this approach handles dependency resolution for each deployment automatically, meaning that there is no need to explicitly determine and install the Python packages your module requires to run on each machine that installs your module.
See [prepare a Python virtual environment](/build/program/python-venv/) for more information.

{{% /tab %}}
{{% tab name="Python: nuitka" %}}

Use the [`nuitka` Python compiler](https://pypi.org/project/Nuitka/) to compile your module into a single executable file:

1. In order to use Nuitka, you must install a [supported C compiler](https://github.com/Nuitka/Nuitka#c-compiler) on your machine.

1. Then, [create a Python virtual environment](/build/program/python-venv/) in your module's directory to ensure your module has access to any required libraries.
   Be sure you are within your Python virtual environment for the rest of these steps: your terminal prompt should include the name of your virtual environment in parenthesis.

1. Create a `requirements.txt` file containing a list of all the dependencies your module requires.
   For example, a `requirements.txt` file with the following contents ensures that the Viam Python SDK (`viam-sdk`) and Nuitka (`nuitka`) are installed:

   ```sh { class="command-line" data-prompt="$"}
   viam-sdk
   nuitka
   ```

   Add additional dependencies for your module as needed.
   See the [pip `requirements.txt` file documentation](https://pip.pypa.io/en/stable/reference/requirements-file-format/) for more information.

1. Install the dependencies listed in your `requirements.txt` file within your Python virtual environment using the following command:

   ```sh { class="command-line" data-prompt="$"}
   python -m pip install -r requirements.txt -U
   ```

1. Then, compile your module using Nuitka with the following command:

   ```sh { class="command-line" data-prompt="$"}
   python -m nuitka --onefile src/main.py
   ```

   If you need to include any additional data files to support your module, specify them using the `--include-data-files` flag:

   ```sh { class="command-line" data-prompt="$"}
   python -m nuitka --onefile --include-data-files=src/arm/my_arm_kinematics.json src/main.py
   ```

Compiling your Python module in this fashion ensures that your module has access to any packages it requires during runtime.
If you intend to share your module with other users, or to deploy it to a fleet of machines, this approach "bundles" your module code together with its required dependencies, making your module highly-portable across like architectures.

However, used in this manner, Nuitka does not support relative imports (imports starting with `.`).
In addition, Nuitka does not support cross-compiling: you can only compile your module on the target architecture you wish to support if using the Nutika approach.
If you want to cross-compile your module, consider using a different local compilation method, or the [`module build start` command](/cli/#using-the-build-subcommand) to build your module on a cloud build host, which supports building for multiple platforms.
For example, you cannot run a module on a Linux `arm64` system if you compiled it using Nuitka on a Linux `amd64` system.

{{% /tab %}}
{{% tab name="Go" %}}

Use Go to compile your module into a single executable:

- Navigate to your module directory in your terminal.
- Run `go build` to compile your entry point (main program) file <file>main.go</file> and all other <file>.go</file> files in the directory, building your module and all dependencies into a single executable file.
- Run `ls` in your module directory to find the executable, which should have the same name as the module directory.

Compiling your Go module also generates the `go.mod` and `go.sum` files that define dependency resolution in Go.

See the [Go compilation documentation](https://pkg.go.dev/cmd/go#hdr-Compile_packages_and_dependencies) for more information.

{{% /tab %}}
{{% tab name="C++" %}}

Create a <file>CMakeLists.txt</file> file to define how to compile your module and a <file>run.sh</file> file to wrap your executable, and then use C++ to compile your source files into a single executable:

1. Create a <file>CMakeLists.txt</file> file in your module directory to instruct the compiler how to compile your module.
   For example, the following basic configuration downloads the C++ SDK and handles compile-time linking for a module named `my-base`:

   ```sh {class="line-numbers linkable-line-numbers"}
   cmake_minimum_required(VERSION 3.7 FATAL_ERROR)

   project(my-base LANGUAGES CXX)

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
   add_executable(my-base ${sources})
   target_link_libraries(my-base PRIVATE viam-cpp-sdk::viamsdk)
   ```

1. Create a <file>run.sh</file> file in your module directory to wrap the executable and perform basic sanity checks at runtime.

   The following example shows a simple configuration that runs a module named `my-base`:

   ```sh {class="line-numbers linkable-line-numbers"}
   #!/usr/bin/env bash

   # bash safe mode
   set -euo pipefail

   cd $(dirname $0)
   exec ./my-base $@
   ```

1. Use C++ to compile and obtain a single executable for your module:

   1. Create a new <file>build</file> directory within your module directory:

      ```sh { class="command-line"}
      mkdir build
      cd build
      ```

   1. Build and compile your module:

      ```sh { class="command-line"}
      cmake .. -G Ninja
      ninja all
      ninja install
      ```

   1. Run `ls` in your module's <file>build</file> directory to find the compiled executable, which should have the same name as the module directory (`my-base` in these examples):

For more information on building a module in C++, see the [C++ SDK Build Documentation](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% /tabs %}}

### (Optional) Create a README

To provide usage instructions for any modular resources in your module, you should create a <file>README.md</file> file following this template:

{{< expand "Click to view template" >}}

Strings of the form `<INSERT X>` indicate placeholders that you need to replace with your values.

{{< tabs >}}
{{% tab name="Template" %}}

````md
# [`<INSERT MODULE NAME>` module](<INSERT LINK TO MODULE REPO>)

This [module](https://docs.viam.com/registry/#modular-resources) implements the [`<INSERT API TRIPLET>` API]<INSERT LINK TO DOCS (if applicable)> in an <INSERT MODEL> model.
With this model, you can...

## Requirements

_Add instructions here for any requirements._

```bash

```

## Configure your <INSERT MODEL NAME> <INSERT API NAME>

Navigate to the [**CONFIGURE** tab](https://docs.viam.com/build/configure/) of your [machine](https://docs.viam.com/fleet/machines/) in [the Viam app](https://app.viam.com/).
[Add <INSERT COMPONENT TYPE / INSERT RESOURCE NAME> to your machine](https://docs.viam.com/build/configure/#components).

On the new component panel, copy and paste the following attribute template into your <INSERT API NAME>’s attributes field:

```json
{
  <INSERT SAMPLE ATTRIBUTES>
}
```

### Attributes

The following attributes are available for `<INSERT MODEL TRIPLET>` <INSERT API NAME>s:

| Name    | Type   | Required?    | Description |
| ------- | ------ | ------------ | ----------- |
| `todo1` | string | **Required** | TODO        |
| `todo2` | string | Optional     | TODO        |

### Example configuration

```json
{
  <INSERT SAMPLE CONFIGURATION(S)>
}
```

### Next steps

_Add any additional information you want readers to know and direct them towards what to do next with this module._
_For example:_

- To test your...
- To write code against your...

## Troubleshooting

_Add troubleshooting notes here._
````

{{% /tab %}}
{{% tab name="Example" %}}

````md
# [`agilex-limo` module](https://app.viam.com/module/viam/agilex-limo)

This module implements the [`rdk:component:base` API](/components/base/#api) in an `agilex` model for the [AgileX LIMO](https://global.agilex.ai/products/limo-pro) base to be used with [`viam-server`](/). This driver supports differential, ackermann, and omni directional steering modes over the serial port.

## Configure your `agilex-limo` base

> [!NOTE]
> Before configuring your base, you must [create a machine](/cloud/machines/#add-a-new-machine).

Navigate to the **CONFIGURE** tab of your machine’s page in [the Viam app](https://app.viam.com/).
[Add `base` / `agilex-limo` to your machine](https://docs.viam.com/build/configure/#components).

On the new component panel, copy and paste the following attribute template into your base’s attributes field:

```json
{
  "drive_mode": "<ackermann|differential|omni>",
  "serial_path": "<your-serial-path>"
}
```

> [!NOTE]
> For more information, see [Configure a Machine](/build/configure/).

### Attributes

The following attributes are available for `viam:base:agilex-limo` bases:

<!-- prettier-ignore -->
| Name          | Type   | Required?    | Description |
| ------------- | ------ | ------------ | ----------- |
| `drive_mode`  | string | **Required** | LIMO [steering mode](https://docs.trossenrobotics.com/agilex_limo_docs/operation/steering_modes.html#switching-steering-modes). Options: `differential`, `ackermann`, `omni` (mecanum). |
| `serial_path` | string | Optional     | The full filesystem path to the serial device, starting with <file>/dev/</file>. With your serial device connected, you can run `sudo dmesg \| grep tty` to show relevant device connection log messages, and then match the returned device name, such as `ttyTHS1`, to its device file, such as <file>/dev/ttyTHS1</file>. If you omit this attribute, Viam will attempt to automatically detect the path.<br>Default: `/dev/ttyTHS1` |

### Example configurations:

```json
{
  "drive_mode": "differential"
}
```

```json
{
  "drive_mode": "omni",
  "serial_path": "/dev/ttyTHS1"
}
```

## Next steps

- To test your base, go to the [**CONTROL** tab](/fleet/control/).
- To write code against your base, use one of the [available SDKs](/build/program/).
- To view examples using a base component, explore [these tutorials](/tutorials/).

## Local development

This module is written in Go.

To build: `make limobase`<br>
To test: `make test`
````

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

## Test your module locally

{{% alert title="Tip" color="tip" %}}

If you would like to test your module locally against a target platform other than your development machine before uploading it, you can follow the steps for [Iterative module development](/registry/advanced/iterative-development/) to verify that any code changes you have made work as expected on your target platform.

{{% /alert %}}

To use a local module on your machine, first add its module to your machine's config, then add the component or service it implements:

1. Navigate to the **CONFIGURE** tab of your machine's page in [the Viam app](https://app.viam.com).

1. Click the **+** (Create) icon next to your machine part in the left-hand menu and select **Local module**, then **Local module**.

1. Enter a **Name** for this instance of your module.

1. Enter the module's **Executable path**.
   This path must be the absolute path on your machine's filesystem to either:

   - the module's [executable file](/use-cases/create-module/#compile-or-package-your-module), such as `run.sh` or a compiled binary.
   - a [packaged tarball](https://www.cs.swarthmore.edu/~newhall/unixhelp/howto_tar.html) of your module, ending in `.tar.gz` or `.tgz`.
     If you are providing a tarball file in this field, be sure that your packaged tarball contains your module's [`meta.json` file](/cli/#the-metajson-file) within it.

1. Then, click the **Create** button, and click **Save** in the upper right corner to save your config.

1. Still on your machine's **CONFIGURE** tab, click the **+** (Create) icon next to your machine part in the left-hand menu.

1. Select **Local module**, then select **Local component** or **Local service**.

1. Select the type of modular resource provided by your module, such as a [camera](/components/camera/), from the dropdown menu.

1. Enter the {{< glossary_tooltip term_id="model-namespace-triplet" text="model namespace triplet">}} of your modular resource's {{< glossary_tooltip term_id="model" text="model" >}}.

   {{<imgproc src="registry/configure/add-local-module-create.png" resize="250x" declaredimensions=true alt="The add a component model showing the create a module step for an intel realsense module">}}

1. Enter a name for this instance of your modular resource.
   This name must be different from the module name.

1. Click **Create** to create the modular resource provided by the local module.

Once you've added your local module using steps 1-5, you can repeat steps 6-11 to add as many additional instances of your modular resource as you need.

## Upload your module to the modular resource registry

Once you are satisfied with the state of your module, you can upload your module to the Viam registry to:

- share your module with other Viam users
- deploy your module to a fleet of machines from a central interface

You can choose to upload it to the Viam registry as a _public module_ that is shared with other Viam users, or as a _private module_ that is shared only within your [organization](/cloud/organizations/).

To upload your custom module to the [Viam registry](https://app.viam.com/registry), either as a public or private module, use the Viam CLI commands `create` and `upload` following these instructions:

1. First, [install the Viam CLI](/cli/#install) and [authenticate](/cli/#authenticate) to Viam, from the same machine that you intend to upload your module from.

2. Next, run the `viam module create` command to choose a custom module name and generate the required metadata for your module.
   By default, a new module is created as _private_, meaning that it is only accessible to members of your [organization](/cloud/organizations/), but you can choose to set the `visibility` of your module to _public_ to make it accessible to all Viam users.

   Select the private or public tab for instructions to upload your module with the respective `visibility` setting:

   {{< tabs >}}
   {{% tab name="Private" %}}

Get the `org-id` for your {{< glossary_tooltip term_id="organization" text="organization" >}} from your organization's **Settings** page in [the Viam App](https://app.viam.com/) and run the following command from the same directory as your custom module to generate metadata for your module:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module create --name <your-module-name> --org-id <your-org-id>
```

If you later wish to make your module public, you can use the [`viam module update` command](/cli/#module).

{{% /tab %}}
{{% tab name="Public" %}}

1.  If you haven't already, [create a new namespace](/cloud/organizations/#create-a-namespace-for-your-organization) for your organization.
    If you have already created a namespace, you can find it on your organization's **Settings** page in [the Viam App](https://app.viam.com/), or by running the [`viam organizations list`](/cli/#organizations) command.

2.  To generate metadata for your module using your public namespace, run the following command from the same directory as your custom module:

    ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
    viam module create --name <your-module-name> --public-namespace <your-unique-namespace>
    ```

    {{% /tab %}}
    {{< /tabs >}}

    This command creates a new `meta.json` metadata file in your current working directory, which serves as a template.

3.  Edit the newly-created `meta.json` file, and provide the required configuration information for your custom module by filling in the following fields.

    <table class="table table-striped">
      <tr>
        <th>Name</th>
        <th>Type</th>
        <th>Inclusion</th>
        <th>Description</th>
      </tr>
      <tr>
        <td><code>module_id</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>The module ID, which includes either the module <a href="/cloud/organizations/#create-a-namespace-for-your-organization">namespace</a> or <a href="/cloud/organizations/">organization-id</a>, followed by its name (pre-populated using the <code>--name</code> you provided in the <code>viam module create</code> command).
        <div class="alert alert-caution" role="alert">
      <h4 class="alert-heading">Caution</h4>

      <p>The <code>module_id</code> uniquely identifies your module.
      Do not change the <code>module_id</code>.</p>

      </div>
        </td>

      </tr>
      <tr>
        <td><code>visibility</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>Whether the module is accessible only to members of your <a href="/cloud/organizations/">organization</a> (<code>private</code>), or visible to all Viam users (<code>public</code>). You can later make a private module public using the <code>viam module update</code> command. Once you make a module public, you can change it back to private if it is not configured on any machines outside of your organization.<br><br>Default: <code>private</code></td>
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
        <td><p>A list of one or more {{< glossary_tooltip term_id="model" text="models" >}} provided by your custom module. You must provide at least one model, which consists of an <code>api</code> and <code>model</code> key pair. If you are publishing a public module (<code>"visibility": "public"</code>), the namespace of your model must match the <a href="/cloud/organizations/#create-a-namespace-for-your-organization">namespace of your organization</a>.</p><p>For more information, see <a href="/create-module/#name-your-new-resource-model">naming your model</a>.</p></td>
      </tr>
      <tr>
        <td><code>entrypoint</code></td>
        <td>string</td>
        <td><strong>Required</strong></td>
        <td>The name of the file that starts your module program. This can be a compiled executable, a script, or an invocation of another program. If you are providing your module as a single file to the <code>upload</code> command, provide the path to that single file. If you are providing a directory containing your module to the <code>upload</code> command, provide the path to the entry point file contained within that directory.</td>
      </tr>
      <tr>
        <td><code>build</code></td>
        <td>object</td>
        <td><strong>Optional</strong></td>
        <td>An object containing the command to run to build your module, as well as optional fields for the path to your dependency setup script, the target architectures to build for, and the path to your built module. Use this with the <a href="/cli/#using-the-build-subcommand">Viam CLI's build subcommand</a>. </td>
      </tr>

    </table>

    For example, the following represents the configuration of an example `my-module` public module in the `acme` namespace:

    {{< expand "Click to view example meta.json with build object" >}}

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model"
    }
  ],
  "build": {
    "path": "dist/archive.tar.gz", // optional - path to your built module
    "build": "./build.sh", // command that will build your module
    "arch": ["linux/amd64", "linux/arm64"] // architecture(s) to build for
  },
  "entrypoint": "dist/main" // path to executable
}
```

    {{< /expand >}}

    {{< expand "Click to view example meta.json without build object" >}}

```json {class="line-numbers linkable-line-numbers"}
{
  "module_id": "acme:my-module",
  "visibility": "public",
  "url": "https://github.com/<my-repo-name>/my-module",
  "description": "An example custom module.",
  "models": [
    {
      "api": "rdk:component:generic",
      "model": "acme:demo:my-model"
    }
  ],
  "entrypoint": "my-module.sh" // path to executable
}
```

    {{< /expand >}}

    {{% alert title="Important" color="note" %}}

In the example above, the model namespace is set to `acme` to match the owning organization's namespace.
If the two namespaces do not match, the command will return an error.

For more information, see [Name your new resource model](/use-cases/create-module/#name-your-new-resource-model).

    {{% /alert %}}

    See [`meta.json` file](/cli/#the-metajson-file) for more information.

1. For modules written in Python, you should package your module files as an archive first, before uploading.
   Other languages can proceed to the next step to upload their module directly.
   To package a module written in Python, run the following command from the same directory as your `meta.json` file:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czvf dist/archive.tar.gz <PATH-TO-EXECUTABLE>
   ```

   where `<PATH-TO-EXECUTABLE>` is the [packaged executable](/use-cases/create-module/#compile-or-package-your-module) that runs the module at the [entry point](/use-cases/create-module/#write-an-entry-point-main-program-file).
   If using PyInstaller, by default this would be `dist/main`.

   For a Python module built using the `venv` approach, the command might look like this:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   tar -czf module.tar.gz run.sh requirements.txt src
   ```

   Where `run.sh` is your [entrypoint file](/use-cases/create-module/#compile-or-package-your-module), `requirements.txt` is your [pip dependency list file](/use-cases/create-module/#compile-or-package-your-module), and `src` is the directory that contains the source code of your module.

   Supply the path to the resulting archive file in the next step.

1. Run `viam module upload` to upload your custom module to the Viam registry.
   Specify the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code:

   ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
   viam module upload --version <version> --platform <platform> <module-path>
   ```

   where:

   - `version`: provide a version for your custom module, using [semantic versioning](https://semver.org/) (example: `1.0.0`).
     You can later increment this value with subsequent `viam module upload` commands.
     See [Using the `--version` argument](/cli/#using-the---version-argument) for more information.
   - `platform`: provide the system architecture your custom module supports.
     You can only provide one `platform` argument at a time to the `viam module upload` command.
     See [Using the `--platform` argument](/cli/#using-the---platform-argument) for the full list of supported architectures.
   - `module-path`: provide the path to the file, directory, or compressed archive (with `.tar.gz` or `.tgz` extension) that contains your custom module code.

   {{% alert title="Important" color="note" %}}
   The `viam module upload` command only supports one `platform` argument at a time.
   If you would like to upload your module with support for multiple platforms, you must run a separate `viam module upload` command for each platform.
   Use the _same version number_ when running multiple `upload` commands of the same module code if only the `platform` support differs.
   The Viam registry page for your module displays the platforms your module supports for each version you have uploaded.
   {{% /alert %}}

   For example:

   - To upload a custom module that is defined in a single file named `my-module-file` in a local `bin` directory:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 ./bin/my-module-file
     ```

   - To upload a custom module that includes multiple files, as well as a separate entry point file, all contained with a local `bin` directory:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 ./bin
     ```

   - To upload a custom module that has been compressed as an archive named `packaged-module.tar.gz`:

     ```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
     viam module upload --version 1.0.0 --platform linux/amd64 packaged-module.tar.gz
     ```

   When you `upload` a module, the command performs basic [validation](/cli/#upload-validation) of your module to check for common errors.

   For more information, see the [`viam module` command](/cli/#module).

## Deploy your module to more machines

You have now created a module, and are ready to deploy it to a fleet of machines.
There are two ways to deploy a module:

- Through the Viam registry: Once you have uploaded your new module to the Viam registry, [add the module to one or more machines in the Viam app](/registry/configure/).
  You can also choose to configure [automated uploads for new module versions](/use-cases/manage-modules/#update-an-existing-module-using-a-github-action) through a continuous integration (CI) workflow, using a GitHub Action if desired, greatly simplifying how you push changes to your module to the registry as you make them.
- As a local module (without uploading it to the Viam app), as you did in the [Test your module locally step above](#test-your-module-locally).
  This is a great way to test, but if you'd like to use the module on more machines it's easiest to add it to the registry either publicly or privately.

Often, developers first test their new module by deploying it as a local module to a test machine.
With a local installation, you can test your module in a controlled environment to confirm that it functions as expected, and make changes to your module as needed.

## Next steps

For instructions on how to update or delete modules you've created, see the following how-to guide:

{{< cards >}}
{{% card link="/use-cases/manage-modules/" %}}
{{< /cards >}}

To read more about module development at Viam, check out these tutorials that create modules:

{{< cards >}}
{{% card link="/tutorials/custom/custom-base-dog/" %}}
{{% card link="/registry/examples/custom-arm/" %}}
{{% card link="/tutorials/configure/pet-photographer/" %}}
{{< /cards >}}
