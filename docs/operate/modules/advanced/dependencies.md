---
title: "Access machine resources from within a module"
linkTitle: "Module dependencies"
weight: 26
layout: "docs"
type: "docs"
description: "From within a modular resource, you can access other machine resources using dependencies."
aliases:
  - /operate/modules/other-hardware/dependencies/
  - /operate/modules/support-hardware/create-module/dependencies/
date: "2025-11-05"
---

From within a modular resource, you can access other machine {{< glossary_tooltip term_id="resource" text="resources" >}} using dependencies.

## Types of dependencies

There are two types of dependencies:

- **Required dependencies**: A dependency should be designated **required** if a module cannot function without it.
  `viam-server` will not start the resource until all required dependencies are started and functioning.
- **Optional dependencies**: A dependency should be designated **optional** if a module can function without it.
  If an optional dependency is not available when the modular resource starts, the resource will start without it and reconfigure when the optional dependency becomes available.
  `viam-server` attempts to start the optional dependency every 5 seconds.

## Implementation

When implementing a modular resource with dependencies, the validation and constructor or reconfiguration functions ensure the resource has access to the dependencies:

**Example:** Imagine a camera component that implements logic to capture images from another camera only if an ultrasonic sensor determines that someone is nearby.
The camera stores a picture only if someone is detected nearby.
To implement this, you would make the sensor and the camera required dependencies of the camera component.

Ultrasonic sensors only determine that something is near, not necessarily a person.
To make the camera component more reliably only capture images if a person is nearby, you could add a vision service.
To make the camera component work with and without a vision service, you would make the camera an optional dependency.

{{< table >}}
{{% tablestep start=1 %}}
**Implement resource config validation.**

To keep modular resources flexible, the names of the resource that are dependencies, get passed in the resource's configuration.
For example:

```json {class="line-numbers linkable-line-numbers" data-line="6-8"}
{
  "name": "proximity-camera",
  "api": "rdk:component:sensor",
  "model": "exampleorg:examplemodule:examplecamera",
  "attributes": {
    "camera_name": "camera-1",
    "sensor_name": "sensor-1",
    "vision_name": "vision-1"
  }
}
```

{{< tabs >}}
{{% tab name="Python" %}}

The `validate_config` method must:

- Check that required dependencies are present in the configuration.
- Return a list of the names of required dependencies and a list of the names of optional dependencies.

```python {class="line-numbers linkable-line-numbers"}
# Add to imports
from viam.components.camera import *
from viam.components.sensor import *
from viam.services.vision import *
from typing import cast


@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    req_deps = []
    opt_deps = []
    fields = config.attributes.fields

    if "camera_name" not in fields:
        raise Exception("missing required camera_name attribute")
    elif not fields["camera_name"].HasField("string_value"):
        raise Exception("camera_name must be a string")
    camera_name = fields["camera_name"].string_value
    if not camera_name:
        raise ValueError("camera_name cannot be empty")
    req_deps.append(camera_name)

    if "sensor_name" not in fields:
        raise Exception("missing required sensor_name attribute")
    elif not fields["sensor_name"].HasField("string_value"):
        raise Exception("sensor_name must be a string")
    sensor_name = fields["sensor_name"].string_value
    if not sensor_name:
        raise ValueError("sensor_name cannot be empty")
    req_deps.append(sensor_name)

    # Optional dependencies may not be present in the config
    if "vision_name" in fields:
        if not fields["vision_name"].HasField("string_value"):
            raise Exception("vision_name must be a string")
        vision_name = fields["vision_name"].string_value
        if not vision_name:
            raise ValueError("vision_name cannot be empty")
        opt_deps.append(vision_name)

    return req_deps, opt_deps
```

{{% /tab %}}
{{% tab name="Go" %}}

In your resource's `Config` struct, add the dependency attribute name.
For example:

```go {class="line-numbers linkable-line-numbers"}
type Config struct {
  CameraName string `json:"camera_name"`
  SensorName string `json:"sensor_name"`
  VisionName string `json:"vision_name"`
}
```

The `Validate` method must:

- Check that required dependencies are present in the configuration.
- Return a list of the names of required dependencies and a list of the names of optional dependencies.

```go {class="line-numbers linkable-line-numbers"}
func (cfg *Config) Validate(path string) (requiredDeps []string, optionalDeps []string, err error) {
  var reqDeps []string
  var optDeps []string
  if cfg.CameraName == "" {
    return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "camera_name")
  }
  reqDeps = append(reqDeps, cfg.CameraName)

  if cfg.SensorName == "" {
    return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "sensor_name")
  }

  if cfg.VisionName != "" {
    optDeps = append(optDeps, cfg.VisionName)
  }

  return reqDeps, optDeps, nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}

Accessing dependencies from the resource works differently for different programming languages:

{{< tabs >}}
{{% tab name="Python" %}}

To be able to access the dependencies, use the `reconfigure` method to:

- Access the dependency by using its name as a key in the `dependencies` mapping.
- Cast the dependency to the correct type and store it.

```python {class="line-numbers linkable-line-numbers"}
def reconfigure(
    self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
):
    camera_name = config.attributes.fields["camera_name"].string_value
    camera_resource = dependencies[Camera.get_resource_name(camera_name)]
    self.camera = cast(Camera, camera_resource)

    # If you need to use the camera name in your module,
    # for example to pass it to a vision service method,
    # you can store it in an instance variable.
    self.camera_name = camera_name

    sensor_name = config.attributes.fields["sensor_name"].string_value
    sensor_resource = dependencies[Sensor.get_resource_name(sensor_name)]
    self.sensor = cast(Sensor, sensor_resource)

    # Optional dependencies may not be present in the config
    self.vision_svc = None
    if "vision_name" in config.attributes.fields:
        vision_name = config.attributes.fields["vision_name"].string_value

        # For optional dependencies, use .get() and handle None
        vision_resource = dependencies.get(VisionClient.get_resource_name(vision_name))
        if vision_resource is not None:
            self.vision_svc = cast(VisionClient, vision_resource)

    return super().reconfigure(config, dependencies)
```

{{% /tab %}}
{{% tab name="Go" %}}

Add the dependency to the `<module-name><resource-name>` struct:

```go {class="line-numbers linkable-line-numbers" data-line="7-9"}
type myModuleMyCamera struct {
  resource.AlwaysRebuild

  name resource.Name
  logger logging.Logger
  cfg    *Config
  camera camera.Camera
  sensor sensor.Sensor
  vision vision.Vision

  cancelCtx  context.Context
  cancelFunc func()
}
```

Then, use your resource's constructor to access and store the dependency:

```go {class="line-numbers linkable-line-numbers" data-line=""}
// Add to import
import (
	camera "go.viam.com/rdk/components/camera"
	sensor "go.viam.com/rdk/components/sensor"
	vision "go.viam.com/rdk/services/vision"
)

func NewMyCamera(ctx context.Context,deps resource.Dependencies,
  name resource.Name, conf *Config, logger logging.Logger) (camera.Camera, error) {

  cancelCtx, cancelFunc := context.WithCancel(context.Background())

  s := &myModuleMyCamera{
    name:       name,
    logger:     logger,
    cfg:        conf,
    cancelCtx:  cancelCtx,
    cancelFunc: cancelFunc,
  }
  camera, err := camera.FromDependencies(deps, conf.CameraName)
  if err != nil {
    return nil, errors.New("failed to get camera dependency")
  }
  s.camera = camera

  sensor, err := sensor.FromDependencies(deps, conf.SensorName)
  if err != nil {
    return nil, errors.New("failed to get sensor dependency")
  }
  s.sensor = sensor

  // optional dependency
  vision, err := vision.FromDependencies(deps, conf.VisionName)
  if err == nil {
    s.vision = vision
  }

  return s, nil
}
```

{{% alert title="Need to maintain state when reconfiguring?" color="note" %}}

Most Go modules use `resource.AlwaysRebuild` within the `<module-name><resource-name>` struct, which rebuilds the resource every time the module is reconfigured.

If you need to maintain the state of your resource, see [(Optional) Set up model configuration options](/operate/modules/support-hardware/#set-up-model-configuration-options).

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}

You can now call API methods on dependency resources within your module, for example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Add to imports
from viam.utils import from_dm_from_extra
from viam.errors import NoCaptureToStoreError

async def get_images(
    self,
    *,
    filter_source_names: Optional[Sequence[str]] = None,
    extra: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
) -> Tuple[Sequence[NamedImage], ResponseMetadata]:
    images, metadata = await self.camera.get_images()
    readings = await self.sensor.get_readings()

    # If called by the data manager to store image
    # only return image image if person nearby
    if from_dm_from_extra(extra):
        if readings["distance"] <= 5:
            if self.vision_svc:
                detections = await self.vision_svc.get_detections(images[0])
                for detection in detections:
                    if detection.class_name == "Person":
                        return images, metadata
            else:
                return images, metadata
        # No person nearby
        raise NoCaptureToStoreError()

    return images, metadata
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
images, metadata, err := s.camera.Images(ctx, nil, nil)
```

{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{< /table >}}

For more information on capturing data only if conditions are met, see [Pet photographer](/tutorials/configure/pet-photographer/).

{{% hiddencontent %}}
There is currently no SDK method to directly access configuration attributes of dependencies in Python or Go, but in Python it is possible to use `get_robot_part` to return information including the whole configuration of a machine part, and then access the configuration attributes of the dependency from there.
You must access the API key module environment variables to establish the app client connection.
{{% /hiddencontent %}}

For full examples of modules with dependencies, see the [Desk Safari tutorial](/operate/hello-world/tutorial-desk-safari/) or [Viam complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src).

<!-- ## Special case: The `builtin` motion service

The motion service is available by default as part of `viam-server`.
This default motion service is available using the resource name `builtin` even though it does not appear in your machine config.
You do not need to check for its configuration in your `Validate` function because it is always enabled.

This example shows how to access the default motion service:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Return the motion service as a dependency
@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    req_deps = []
    req_deps.append("builtin")
    return req_deps, []


# Add the motion service as an instance variable
def reconfigure(
    self, config: ComponentConfig, dependencies: Mapping[
      ResourceName, ResourceBase]
):
    motion_resource = dependencies[Motion.get_resource_name("builtin")]
    self.motion_service = cast(MotionClient, motion_resource)

    return super().reconfigure(config, dependencies)


# Use the motion service
def move_around_in_some_way(self):
    moved = await self.motion_service.move(
        gripper_name, destination, world_state)
    return moved
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Return the motion service as a dependency
func (cfg *Config) Validate(path string) ([]string, []string, error) {
  deps := []string{motion.Named("builtin").String()}
  return deps, nil, nil
}

// Then use the motion service, for example:
func (c *Component) MoveAroundInSomeWay() error {
  c.Motion, err = motion.FromDependencies(deps, "builtin")
  if err != nil {
    return nil, err
  }
  moved, err := c.Motion.Move(context.Background(), motion.MoveReq{
    ComponentName: gripperName,
    Destination: destination,
    WorldState: worldState
  })
  return moved, err
}
```

{{% /tab %}}
{{< /tabs >}} -->
