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
For example, imagine a camera component that uses an ultrasonic sensor to return a picture only when someone or something is detected closeby.
To implement this, you would make the sensor a dependency of the camera.

## Types of dependencies

There are two types of dependencies:

- **Required dependencies**: A dependency should be designated **required** if a module cannot function without it.
  `viam-server` will not start the resource until all required dependencies are started and functioning.
- **Optional dependencies**: A dependency should be designated **optional** if a module can function without it.
  If an optional dependency is not available when the modular resource starts, the resource will start without it and reconfigure when the optional dependency becomes available.
  `viam-server` attempts to start the optional dependency every 5 seconds.

## Implementation

When implementing a modular resource with dependencies, the `validate_config` and `reconfigure` functions ensure the resource has access to the dependencies:

{{< table >}}
{{% tablestep start=1 %}}
**Implement `validate_config`.**

To keep modular resources flexible, the names of the resource that are dependencies, get passed in the resource's configuration.
For example:

```json {class="line-numbers linkable-line-numbers" data-line="6"}
{
  "name": "mime-type-sensor",
  "api": "rdk:component:sensor",
  "model": "exampleorg:my-module:my-sensor",
  "attributes": {
    "camera_name": "camera-1"
  }
}
```

The `validate_config` method must:

- Check that required dependencies are present in the configuration.
- Return a list of the names of required dependencies and a list of the names of optional dependencies.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Add to imports
from viam.components.camera import *
from typing import cast


@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    req_deps = []
    fields = config.attributes.fields
    if "camera_name" not in fields:
        raise Exception("missing required camera_name attribute")
    elif not fields["camera_name"].HasField("string_value"):
        raise Exception("camera_name must be a string")
    camera_name = fields["camera_name"].string_value
    if not camera_name:
        raise ValueError("camera_name cannot be empty")
    req_deps.append(camera_name)
    return req_deps, []
```

{{% /tab %}}
{{% tab name="Go" %}}
todo
{{% /tab %}}
{{< /tabs >}}

{{% /tablestep %}}
{{% tablestep %}}

1. In your `reconfigure` method:

   - Access the dependency by using its name as a key in the `dependencies` mapping.
   - Cast the dependency to the correct type.

   ```python {class="line-numbers linkable-line-numbers"}
    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        camera_name = config.attributes.fields["camera_name"].string_value
        camera_resource = dependencies[Camera.get_resource_name(camera_name)]
        self.the_camera = cast(Camera, camera_resource)

        # If you need to use the camera name in your module,
        # for example to pass it to a vision service method,
        # you can store it in an instance variable.
        self.camera_name = camera_name

        return super().reconfigure(config, dependencies)
   ```

{{% /tablestep %}}
{{% tablestep %}}

1. You can now call API methods on the dependency resource within your module, for example:

   ```python {class="line-numbers linkable-line-numbers"}
   images, _ = await self.the_camera.get_images()
   img = images[0]
   ```

{{% /tablestep %}}
{{< /table >}}

For full examples, see [<file>ackermann.py</file>](https://github.com/mcvella/viam-ackermann-base/blob/main/src/ackermann.py) or [Viam complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src).

## Next steps

{{< alert title="Tip" color="tip" >}}
To make configuration easier for users, create a [discovery service](/operate/reference/services/discovery/) as a model within your module.
{{< /alert >}}

## Required dependencies

{{< tabs >}}
{{% tab name="Go" %}}

1. In your modular resource's `Config` struct, add the dependency attribute name like any other attribute.
   For example:

   ```go {class="line-numbers linkable-line-numbers"}
   type Config struct {
     CameraName string `json:"camera_name"`
   }
   ```

1. Add the dependency to the `<module-name><resource-name>` struct:

   ```go {class="line-numbers linkable-line-numbers" data-line="7"}
   type myModuleMySensor struct {
     resource.AlwaysRebuild

     name resource.Name
     logger logging.Logger
     cfg    *Config
     camera camera.Camera
     cancelCtx  context.Context
     cancelFunc func()
   }
   ```

1. In your modular resource's `Validate` method, check the configuration attributes, then add the dependency name to the list of dependencies:

   ```go {class="line-numbers linkable-line-numbers"}
   func (cfg *Config) Validate(path string) (requiredDeps []string, optionalDeps []string, err error) {
     var reqDeps []string
     if cfg.CameraName == "" {
       return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "camera_name")
     }
     reqDeps = append(reqDeps, cfg.CameraName)
     return reqDeps, nil, nil
   }
   ```

1. In your resource's constructor, initialize the dependency:

   ```go {class="line-numbers linkable-line-numbers" data-line="13-17"}
    func NewMySensor(ctx context.Context,deps resource.Dependencies,
      name resource.Name, conf *Config, logger logging.Logger) (sensor.Sensor, error) {

      cancelCtx, cancelFunc := context.WithCancel(context.Background())

      s := &myModuleMySensor{
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

      return s, nil
    }
   ```

1. You can now call API methods on the dependency resource within your module, for example:

   ```go {class="line-numbers linkable-line-numbers"}
   images, metadata, err := s.camera.Images(ctx, nil, nil)
   ```

{{% alert title="Note on reconfiguration" color="note" %}}

Most Go modules use `resource.AlwaysRebuild` within the `<module-name><resource-name>` struct, which means that the resource rebuilds every time the module is reconfigured.

The steps above use `resource.AlwaysRebuild`.
If you need to maintain the state of your resource, see [(Optional) Create and edit a `Reconfigure` function](/operate/modules/support-hardware/#implement-api-methods).

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

## Optional dependencies

Example use case for optional dependencies: If your module depends on multiple cameras, but can function even when some are unavailable, you can code the cameras as optional dependencies so that your module can construct and reconfigure without them.

{{< tabs >}}
{{% tab name="Python" %}}

1. If your module has optional dependencies, your `validate_config` function should add the dependency to the second element of the returned tuple:

   ```python {class="line-numbers linkable-line-numbers"}
   @classmethod
   def validate_config(
       cls, config: ComponentConfig
   ) -> Tuple[Sequence[str], Sequence[str]]:
       opt_deps = []
       fields = config.attributes.fields
       if "camera_name" not in fields:
           raise Exception("missing required camera_name attribute")
       elif not fields["camera_name"].HasField("string_value"):
           raise Exception("camera_name must be a string")
       camera_name = fields["camera_name"].string_value
       opt_deps.append(camera_name)
       return [], opt_deps
   ```

1. Add any missing imports for the resource and `cast`.

   ```python {class="line-numbers linkable-line-numbers"}
   from viam.components.camera import *
   from typing import cast
   ```

1. In your `reconfigure` method, allow for the dependency to be unavailable.
   For example:

   ```python {class="line-numbers linkable-line-numbers"}
   def reconfigure(self, config, dependencies):
    camera_name = config.attributes.fields["camera_name"].string_value

    # For optional dependencies, use .get() and handle None
    camera_resource = dependencies.get(Camera.get_resource_name(camera_name))
    if camera_resource is not None:
        self.the_camera = cast(Camera, camera_resource)
        self.camera_name = camera_name
        self.has_camera = True
    else:
        self.the_camera = None
        self.camera_name = camera_name
        self.has_camera = False

    return super().reconfigure(config, dependencies)
   ```

Be sure to handle the case where the dependency is not available in your API implementation as well.
For example:

```python {class="line-numbers linkable-line-numbers"}
async def get_readings(
    self,
    *,
    extra: Optional[Mapping[str, Any]] = None,
    timeout: Optional[float] = None,
    **kwargs
) -> Mapping[str, SensorReading]:
    if self.has_camera and self.the_camera is not None:
        # Use the camera
        images, _ = await self.the_camera.get_images()
        img = images[0]
        mimetype = img.mime_type
        return {
            "readings": {
                "mimetype": mimetype
            }
        }
    else:
        # Work without camera
        return {"readings": "no_camera_available"}
```

{{% /tab %}}
{{% tab name="Go" %}}

If your module has optional dependencies, the steps are the same as for required dependencies, except that your `Validate` function should add the dependency to the second returned element:

```go {class="line-numbers linkable-line-numbers"}
func (cfg *Config) Validate(path string) (requiredDeps []string, optionalDeps []string, err error) {
  var optDeps []string
  if cfg.CameraName == "" {
    return nil, nil, resource.NewConfigValidationFieldRequiredError(path, "camera_name")
  }
  optDeps = append(optDeps, cfg.CameraName)
  return nil, optDeps, nil
}
```

Be sure to handle the case where the dependency is not available in your API implementation as well.

{{% /tab %}}
{{< /tabs >}}

{{% hiddencontent %}}
There is not currently an SDK method to directly access configuration attributes of dependencies in Python or Go, but in Python it is possible to use `get_robot_part` to return information including the whole configuration of a machine part, and then access the configuration attributes of the dependency from there.
You must access the API key module environment variables to establish the app client connection.
{{% /hiddencontent %}}

## Special case: The `builtin` motion service

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
{{< /tabs >}}
