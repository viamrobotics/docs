---
title: "Module dependencies"
linkTitle: "Module dependencies"
weight: 25
layout: "docs"
type: "docs"
description: "Handle dependencies in your custom modular resource."
---

## What are dependencies?

Dependencies are other {{< glossary_tooltip term_id="resource" text="resources" >}} that your modular resource needs to access in order to function.

For example, you could write a sensor component that requires a camera component, meaning that the camera is a dependency of that sensor.

```json {class="line-numbers linkable-line-numbers" data-line="6"}
{
  "name": "mime-type-sensor",
  "api": "rdk:component:sensor",
  "model": "jessamy:my-module:my-sensor",
  "attributes": {
    "camera_name": "camera-1"
  }
}
```

Dependencies are configured just like any other resource attribute.
The difference is that dependencies represent other resources that must be built before the resource that depends on them.

When [`viam-server` builds all the resources on a machine](/operate/get-started/other-hardware/#how-and-where-do-modules-run), it builds the dependencies first.

## Use dependencies

From within a module, you cannot access resources in the same way that you would in a client application.
For example, you cannot call `Camera.from_robot()` to get a camera resource.

Instead, you must access dependencies by writing your module code as follows:

### Required dependencies

{{< tabs >}}
{{% tab name="Python" %}}

1. In your modular resource's `validate_config` method, check the configuration attributes, then add the dependency name to the list of dependencies.
   For example:

   ```python {class="line-numbers linkable-line-numbers"}
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        deps = []
        fields = config.attributes.fields
        if not "camera_name" in fields:
            raise Exception("missing required camera_name attribute")
        elif not fields["camera_name"].HasField("string_value"):
            raise Exception("camera_name must be a string")
        camera_name = fields["camera_name"].string_value
        deps.append(camera_name)
        return deps
   ```

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

1. You can now call API methods on the dependency resource within your module, for example:

   ```python {class="line-numbers linkable-line-numbers"}
   img = await self.the_camera.get_image()
   ```

For full examples, see [<file>ackermann.py</file>](https://github.com/mcvella/viam-ackermann-base/blob/main/src/ackermann.py) or [Viam complex module examples on GitHub](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/complex_module/src).

{{% /tab %}}
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
   func (cfg *Config) Validate(path string) ([]string, error) {
     var deps []string
     if cfg.CameraName == "" {
       return nil, resource.NewConfigValidationFieldRequiredError(path, "camera_name")
     }
     if reflect.TypeOf(cfg.CameraName).Kind() != reflect.String {
       return nil, errors.New("camera_name must be a string")
     }
     deps = append(deps, cfg.CameraName)
     return deps, nil
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
   img, imgMetadata, err := s.camera.Image(ctx, utils.MimeTypeJPEG, nil)
   ```

{{% alert title="Note on reconfiguration" color="note" %}}

Most Go modules use `resource.AlwaysRebuild` within the `<module-name><resource-name>` struct, which means that the resource rebuilds every time the module is reconfigured.

The steps above use `resource.AlwaysRebuild`.
If you need to maintain the state of your resource, see [(Optional) Create and edit a `Reconfigure` function](/operate/get-started/other-hardware/#implement-the-component-api).

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

### Optional dependencies

{{< tabs >}}
{{% tab name="Python" %}}

If your module has optional dependencies, the steps are the same as for required dependencies, except that your `validate_config` method can treat the dependency as optional by returning an empty list if the dependency is not configured:

```python {class="line-numbers linkable-line-numbers"}
@classmethod
def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
    deps = []
    fields = config.attributes.fields
    if "camera_name" not in fields:
        self.logger.info(
          "camera_name not configured, using no camera")
    else:
        if not fields["camera_name"].HasField("string_value"):
            raise Exception("camera_name must be a string")
        deps.append(fields["camera_name"].string_value)
    return deps
```

Be sure to handle the case where the dependency is not configured in your API implementation as well.

{{% /tab %}}
{{% tab name="Go" %}}

If your module has optional dependencies, the steps are the same as for required dependencies, except that your `Validate` method can treat the dependency as optional by returning an empty list if the dependency is not configured:

```go {class="line-numbers linkable-line-numbers"}
func (cfg *Config) Validate(path string) ([]string, error) {
  var deps []string
  if cfg.CameraName == "" {
    logger.Info("camera_name not configured, using no camera")
    return nil, nil
  }
  if reflect.TypeOf(cfg.CameraName).Kind() != reflect.String {
    return nil, errors.New("camera_name must be a string")
  }
  deps = append(deps, cfg.CameraName)
  return deps, nil
}
```

Be sure to handle the case where the dependency is not configured in your API implementation as well.

{{% /tab %}}
{{< /tabs >}}

{{% hiddencontent %}}
There is not currently an SDK method to directly access configuration attributes of dependencies in Python or Go, but in Python it is possible to use `get_robot_part` to return information including the whole configuration of a machine part, and then access the configuration attributes of the dependency from there.
You must access the API key module environment variables to establish the app client connection.
{{% /hiddencontent %}}

### Explicit dependencies (deprecated)

Some older modules use explicit dependencies, which require users to list the names of dependencies in the `depends_on` field of the resource's configuration, for example:

```json {class="line-numbers linkable-line-numbers"}
  "name": "mime-type-sensor",
  "api": "rdk:component:sensor",
  "model": "jessamy:my-module:my-sensor",
  "attributes": {
    "camera_name": "camera-1"
  },
  "depends_on": ["camera-1"]
}
```

This is deprecated and not recommended when writing new modules.

Instead, we recommend using implicit dependencies (as shown in the examples above), which do not require users to list the names of dependencies in the `depends_on` field.

## Configure your module's dependencies more easily with a discovery service

If your module requires dependencies, you can make it easier for users to configure them by writing a [discovery service](/operate/reference/services/discovery/) as one model within your module.
