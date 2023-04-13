---
title: "Create custom components and services as modular resources"
linkTitle: "Modular Resources"
description: "Use the Viam module system to implement custom resources that can be included in any Viam-powered robot."
image: "/tutorials/img/intermode/rover_outside.png"
weight: 10
type: "docs"
tags: ["server", "rdk", "extending viam", "modular resources", "components", "services"]
---

The Viam module system allows you to integrate custom [resources](/appendix/glossary/#term-resource) ([components](/components) and [services](/services)) into any robot running on Viam.

With modular resources, you can:

- Create new models of built-in component or service types
- Create brand new resource types

`viam-server` [manages](#modular-resource-management) modular resources configured on your robot like resources that are already built-in to the [Robot Development Kit (RDK)](/program/rdk).
This means that functionality that the [RDK](/program/rdk/) provides for built-in resources is also automatically provided for user-created modular resources.
Two key concepts exist across all Viam resources, built-in and modular, to facilitate this: [*APIs*](#apis) and [*models*](#models).

## Key concepts

### APIs

Every Viam [resource](/appendix/glossary/#term-resource) exposes an [Application Programming Interface (API)](https://www.ibm.com/topics/api).
This API describes the interface for the particular component or service type.
Viam APIs are uniquely namespaced, with each resource type represented as a *colon-delimited-triplet*.
For example:

- The API of built-in component type [camera](/components/camera) is `rdk:component:camera`.
It exposes methods such as `GetImage()`.
- The API of built-in service type [vision](/services/vision) is `rdk:service:vision`.
It exposes methods such as `GetDetectionsFromCamera()`.

Each API is described through <a href="https://developers.google.com/protocol-buffers" target="_blank">protocol buffers</a>.
Viam SDKs [expose these APIs](/internals/robot-to-robot-comms/).

{{% alert title="Note" color="note" %}}
You can see built-in Viam resource APIs in the <a href="https://github.com/viamrobotics/api" target="_blank">Viam GitHub</a>.
{{% /alert %}}

### Models

A *model* is an implementation of a resource type that implements all or some of the API methods of a resource type's API.

Models allow you to control any number of versions of a given resource with a consistent interface.
This is powerful, because you have all the same methods for interfacing with different models of the same component type.

For example, some DC motors can be controlled with GPIO, which you can interface with in different ways depending on the attached controlling hardware.
Other DC motors are controlled with various serial protocols.
This is simplified with Viam, as any motor model that implements the *rdk:component:motor* API can be powered with the `SetPower()` method.

Models are also represented by *colon-delimited-triplets*.
For example:

- The `rdk:builtin:gpio` model of the `rdk:component:motor` API provides RDK support for [GPIO-controlled DC motors](/components/motor/gpio/).
- The `rdk:builtin:DMC4000` model of the same `rdk:component:motor` API provides RDK support for the [DMC4000](/components/motor/dmc4000/) motor.

A common use-case for modular resources is to create a new model using an existing Viam API.
However, you can also create and expose new API types using modular resources.

## Use a modular resource with your robot

Add a modular resource to your robot configuration in five steps:

1. Code a module in Go or Python that implements a new resource and registers the component in the Viam RDK's [global registry of robotic parts](https://github.com/viamrobotics/rdk/blob/main/registry/registry.go).
2. Create an executable file that runs your module.
3. Save the executable in a location your `viam-server` instance can access.
4. Add a *module* referencing this executable to the configuration of your robot.
5. Add a new component or service referencing the custom resource provided by the configured *module* to the configuration of your robot.

{{% alert title="Modules vs. modular resources" color="tip" %}}

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

### Code your module

Code a module in the Go or Python programming languages with [Viam's SDKs](/program/sdk-as-client) that does the following:

1. Implements a new resource.

2. Validates the module and registers the component in the Viam RDK's [global registry of robotic parts](https://github.com/viamrobotics/rdk/blob/main/registry/registry.go).

For example:

{{%expand "Click to view an example of a module implementing a new model of the built-in base component type" %}}

``` go {class="line-numbers linkable-line-numbers"}
// Package mybase implements a base that only supports SetPower (basic forward/back/turn controls.)
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

var (
    Model            = resource.NewModel("acme", "demo", "mybase")
    errUnimplemented = errors.New("unimplemented")
)

// STEP 1: Implements the methods the Viam RDK defines for the base API.

// Instantiation
func newBase(ctx context.Context, deps registry.Dependencies, config config.Component, logger golog.Logger) (interface{}, error) {
    b := &MyBase{logger: logger}
    err := b.Reconfigure(config, deps)
    return b, err
}

// Reconfiguration
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

// Defines what the JSON for configuration should look like
type MyBaseConfig struct {
    LeftMotor  string `json:"motorL"`
    RightMotor string `json:"motorR"`
}

// Validates JSON for configuration
func (cfg *MyBaseConfig) Validate(path string) ([]string, error) {
    if cfg.LeftMotor == "" {
        return nil, fmt.Errorf(`expected "motorL" attribute for mybase %q`, path)
    }
    if cfg.RightMotor == "" {
        return nil, fmt.Errorf(`expected "motorR" attribute for mybase %q`, path)
    }

    return []string{cfg.LeftMotor, cfg.RightMotor}, nil
}

// Attributes of the base
type MyBase struct {
    generic.Echo
    left   motor.Motor
    right  motor.Motor
    logger golog.Logger
}

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

// SetPower of the motors on the base
func (base *MyBase) SetPower(ctx context.Context, linear, angular r3.Vector, extra map[string]interface{}) error {
    base.logger.Debugf("SetPower Linear: %.2f Angular: %.2f", linear.Y, angular.Z)
    if math.Abs(linear.Y) < 0.01 && math.Abs(angular.Z) < 0.01 {
        return base.Stop(ctx, extra)
    }
    sum := math.Abs(linear.Y) + math.Abs(angular.Z)
    err1 := base.left.SetPower(ctx, (linear.Y-angular.Z)/sum, extra)
    err2 := base.right.SetPower(ctx, (linear.Y+angular.Z)/sum, extra)
    return multierr.Combine(err1, err2)
}

// Stop the base
func (base *MyBase) Stop(ctx context.Context, extra map[string]interface{}) error {
    base.logger.Debug("Stop")
    err1 := base.left.Stop(ctx, extra)
    err2 := base.right.Stop(ctx, extra)
    return multierr.Combine(err1, err2)
}

// Check if the base is moving
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

func (base *MyBase) Close(ctx context.Context) error {
    return base.Stop(ctx, nil)
}


// STEP 2: Registers the component in the Viam RDK's global registry of robotic parts

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

This example is from the [Viam GitHub](https://github.com/viamrobotics/rdk/blob/main/examples/customresources/models/mybase/mybase.go), and creates a singular modular resource implementing Viam's built-in Base API (rdk:service:base).
See [Base API Methods](/components/base) and [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/base/base.go) for more information.

{{% /expand%}}

{{% alert title="Caution" color="caution" %}}

You must define all functions belonging to a built-in resource type if defining a new model. Otherwise, the class won’t instantiate.

- If you are using the Python SDK, raise an `NotImplementedError()` in the body of functions you do not want to implement or put `pass`.
- If you are using the Go SDK, return `errUnimplemented` or leave the body of functions you do not want to implement empty.

{{% /alert %}}

### Make your module executable

To add a module to your robot, you need to have an [executable file](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and eleanly exits when sent a termination signal.
Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

One option is creating and save a new shell script (<file>.sh</file>) that runs your module.
For example:

{{< tabs name="Template Shell Scripts as Module Executables" >}}
{{% tab name="Go" %}}

``` shell
#!/bin/sh
cd <path-to-your-module-directory>

go build ./
# Be sure to use `exec` so that termination signals reach the go process,
# or handle forwarding termination signals manually
exec ./<your-module-directory-name> $@
```

{{% /tab %}}
{{% tab name="Python" %}}

``` shell
#!/bin/sh
cd <path-to-your-module-directory>

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 <your-module-directory-name>.main $@
```

{{% /tab %}}
{{< /tabs >}}

To make this file executable, run the following command in your terminal:

``` shell
sudo chmod +x <FILEPATH>/<FILENAME>
```

### Make sure `viam-server` can access your executable

Ensure that the code defining your module is saved where the instance of `viam-server` behind your robot can read and execute it.

For example, if you are running `viam-server` on an Raspberry Pi, you'll need to save the module on the Pi's filesystem.

Obtain the path to the executable file on your computer's filesystem by running the following commands in your terminal:

``` shell
cd <path-to-your-module-directory>
pwd
```

### Configure your module

To configure your new *module* on your robot, navigate to the **CONFIG** tab of your robot's page on [the Viam app](https://app.viam.com) and click on the **MODULES** sub-tab.

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
      "name": <your-module-name>,
      "executable_path": <path-on-your-filesystem-to/your-module-directory>
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

All standard properties for configuration, such as `attributes` and `depends_on`, are also supported for modular resources.
The `attributes` available vary depending on your implementation.

{{< tabs >}}
{{% tab name="JSON Template" %}}

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [
    {
      "namespace": <module-namespace>,
      "type": <resource-type>,
      "depends_on": [],
      "model": <model-namespace>:<model-family-name>:<model-name>,
      "name": <string>
    }
  ],
  "modules": [ ... ] // Your module configuration.
}
```

{{% /tab %}}
{{% tab name="JSON Example" %}}

The following is an example configuration for a motor modular resource implementation.
It registers a custom model `viam-contributor:motor:super-custom` to use with the Viam [motor API](/components/motor#api):

```json {class="line-numbers linkable-line-numbers"}
{
  "modules": [
    {
      "name": "super-motor",
      "executable_path": "/home/me/super-custom-motor/run.sh"
    }
  ],
    "components": [
        {
            "type": "board",
            "name": "main-board",
            "model": "pi"
        },
        {
        "type": "motor",
        "name": "super-motor-1",
        "model": "viam-contributor:motor:super-custom",
        "namespace": "rdk",
        "attributes": {},
        "depends_on": [ "main-board" ]
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

Custom models of the [arm](/components/arm) component type are not yet supported, as kinematic information is not currently exposed through the arm API.
