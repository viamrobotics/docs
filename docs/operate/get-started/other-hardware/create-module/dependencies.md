---
title: "Access other resources from within a module"
linkTitle: "Module dependencies"
weight: 25
layout: "docs"
type: "docs"
description: "Write your validate and reconfigure functions to handle dependencies in your custom modular resource."
aliases:
  - /operate/get-started/other-hardware/dependencies/
---

## What are dependencies?

Dependencies are other {{< glossary_tooltip term_id="resource" text="resources" >}} that your modular resource needs to access in order to function.

For example, you could write a sensor component that has a camera component as a dependency.
This allows the sensor module to access data from the camera by using the camera API methods on the camera client from within the sensor module.

The component configuration for the sensor could look like this, with the name of the camera as an attribute:

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
The difference is that dependencies represent other resources, and they are treated specially in the `validate_config` and `reconfigure` functions.

When [`viam-server` builds all the resources on a machine](/operate/get-started/other-hardware/lifecycle-module/), it builds the dependencies first.

## Write dependencies into your module

From within a module, you cannot access resources in the same way that you would in a client application.
For example, you cannot call `Camera.from_robot()` to get a camera resource.

To access resources from within a module, use dependencies:

### Required dependencies

Use required dependencies when your module should fail to build or reconfigure if a dependency does not successfully start.

`viam-server` builds required dependencies before building the resource that depends on them.

`viam-server` will not build or reconfigure a resource if the resource has required dependencies that are not available.

{{< tabs >}}
{{% tab name="Python" %}}

1. In your modular resource's `validate_config` method, check the configuration attributes, then add the dependency name to the first list of dependencies in the returned tuple:
   For example:

   ```python {class="line-numbers linkable-line-numbers"}
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
   img, imgMetadata, err := s.camera.Image(ctx, utils.MimeTypeJPEG, nil)
   ```

{{% alert title="Note on reconfiguration" color="note" %}}

Most Go modules use `resource.AlwaysRebuild` within the `<module-name><resource-name>` struct, which means that the resource rebuilds every time the module is reconfigured.

The steps above use `resource.AlwaysRebuild`.
If you need to maintain the state of your resource, see [(Optional) Create and edit a `Reconfigure` function](/operate/get-started/other-hardware/create-module/#implement-the-component-api).

{{% /alert %}}

{{% /tab %}}
{{< /tabs >}}

### Optional dependencies

If an optional dependency does not start, the modular resource will continue to build and reconfigure without it.
`viam-server` reattempts to construct the optional dependency every 5 seconds.
When an optional dependency constructs successfully, your modular resource reconfigures so it can access the optional dependency.

Optional dependencies are not necessarily built first, even if they are available.

Use optional dependencies for intermittently available resources.

Example use case for optional dependencies: If your module depends on multiple cameras, but can function even when some are unavailable, you can code the cameras as optional dependencies so that your module can construct and reconfigure without them.

{{< tabs >}}
{{% tab name="Python" %}}

1. If your module has optional dependencies, your `validate_config` function should add the dependency to the second element of the returned tuple.
   For example:

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
        img = await self.the_camera.get_image()
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

## Use SDK methods on dependencies

Once you have added a dependency to your modular resource, you can use SDK methods on the resource client.
For example:

{{< tabs >}}
{{% tab name="Components" %}}

For components such as arms, cameras, and sensors, you can use SDK methods to access the resource client following the pattern in this example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
img = await self.the_camera.get_image()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
img, imgMetadata, err := s.camera.Image(ctx, utils.MimeTypeJPEG, nil)
```

{{% /tab %}}
{{% /tabs %}}

{{% /tab %}}
{{% tab name="Services" %}}

For services such as vision and navigation, you can use SDK methods to access the resource client following the pattern in this example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# "self.my_detector" is the vision service dependency,
# and "my_camera" is the name of the camera in the machine config.
detections = await self.my_detector.get_detections_from_camera("my_camera")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// "s.myDetector" is the vision service dependency,
// and "my_camera" is the name of some camera in the machine config.
detections, err := s.myDetector.GetDetectionsFromCamera(ctx, "my_camera")
```

{{% /tab %}}
{{< /tabs >}}

Note that because the module code in this example is calling the vision service API, the vision service must be a dependency.
Meanwhile, because the module code is not calling the camera API, the camera does not need to be a dependency.

### Special case: The motion service

The motion service is available by default as part of `viam-server`.
This default motion service is available using the resource name `builtin` even though it does not appear in your machine config.
You do not need to check for it being configured in your `Validate` function because it is always enabled.

If you are accessing a different motion service, use the resource name you configured, and add it to your `Validate` function.

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

{{% /tab %}}
{{% tab name="Platform clients" %}}

The following APIs do not require a dependency, but you must authenticate using API keys and create a `ViamClient`:

- [Fleet management (`app_client`)](/dev/reference/apis/fleet/)
- [Data client (`data_client`)](/dev/reference/apis/data-client/)
  - For the [data management API](/dev/reference/apis/services/data/), use the typical service client pattern.
- [ML training (`ml_training_client`)](/dev/reference/apis/ml-training-client/)
- [Billing (`billing_client`)](/dev/reference/apis/billing-client/)

You can use [module environment variables](/operate/get-started/other-hardware/module-configuration/) to access the API keys.
Then, get the client you need from the ViamClient.
For example:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
import os
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


async def create_appclient_from_module():
    # Get API credentials from module environment variables
    api_key = os.environ.get("VIAM_API_KEY")
    api_key_id = os.environ.get("VIAM_API_KEY_ID")

    if not api_key or not api_key_id:
        raise Exception("VIAM_API_KEY and VIAM_API_KEY_ID " +
                        "environment variables are required")

    # Create dial options with API key authentication
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=api_key,
        ),
        auth_entity=api_key_id
    )

    # Create ViamClient and get app_client
    viam_client = await ViamClient.create_from_dial_options(dial_options)
    app_client = viam_client.app_client

    return app_client


# Use the appclient in your module
async def some_module_function(self):
    app_client = await create_appclient_from_module()

    # Now you can use app_client methods, for example:
    orgs = await app_client.list_organizations()
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="Machine management" %}}

To use the [machine management (`robot_client`) API](/dev/reference/apis/robot/), you must get the machine's FQDN and API keys from the module environment variables.

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# For robot client, you can also use the machine's FQDN:
async def create_robotclient():
    # Get API credentials from module environment variables
    api_key = os.environ.get("VIAM_API_KEY")
    api_key_id = os.environ.get("VIAM_API_KEY_ID")
    machine_fqdn = os.environ.get("VIAM_MACHINE_FQDN")

    if not api_key or not api_key_id or not machine_fqdn:
        raise Exception("VIAM_API_KEY, VIAM_API_KEY_ID, and " +
                        "VIAM_MACHINE_FQDN " +
                        "environment variables are required")

    # Create robot client options with API key authentication
    opts = RobotClient.Options.with_api_key(
        api_key=api_key,
        api_key_id=api_key_id
    )

    # Create RobotClient using the machine's FQDN
    robot_client = await RobotClient.at_address(machine_fqdn, opts)

    return robot_client


# Use the robot client
async def some_module_function(self):
    robot_client = await create_robotclient()

    # Now you can use robot_client methods, for example:
    resources = await robot_client.resource_names()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func createRobotClientFromModule(ctx context.Context) (client.RobotClient, error) {
    // Get API credentials and machine FQDN from module environment variables
    apiKey := os.Getenv("VIAM_API_KEY")
    apiKeyID := os.Getenv("VIAM_API_KEY_ID")
    machineFQDN := os.Getenv("VIAM_MACHINE_FQDN")

    if apiKey == "" || apiKeyID == "" || machineFQDN == "" {
        return nil, fmt.Errorf("VIAM_API_KEY, VIAM_API_KEY_ID, and " +
            "VIAM_MACHINE_FQDN environment variables are required")
    }

    logger := logging.NewLogger("client")

    // Create robot client with API key authentication
    robotClient, err := client.New(
        ctx,
        machineFQDN,
        logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            apiKeyID,
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: apiKey,
            })),
    )
    if err != nil {
        return nil, fmt.Errorf("failed to create robot client: %w", err)
    }

    return robotClient, nil
}

// Use the robot client
func (c *Component) SomeModuleFunction(ctx context.Context) error {
    robotClient, err := createRobotClientFromModule(ctx)
    if err != nil {
        return err
    }

    // Now you can use robot client methods, for example:
    resources := robotClient.ResourceNames()
```

{{% /tab %}}
{{% /tabs %}}
{{% /tab %}}
{{< /tabs >}}

## Configure your module's dependencies more easily with a discovery service

If your module requires dependencies, you can make it easier for users to configure them by writing a [discovery service](/operate/reference/services/discovery/) as one model within your module.
