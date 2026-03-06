---
linkTitle: "Write an Inline Module"
title: "Write an Inline Module"
weight: 10
layout: "docs"
type: "docs"
description: "Write and deploy a custom module directly in the browser using Viam's inline module editor."
date: "2025-01-30"
aliases:
  - /build/development/write-an-inline-module/
  - /development/write-an-inline-module/
---

Viam provides built-in support for many types of hardware and software, but you
may want to use hardware that Viam doesn't support out of the box, or add
application-specific logic. Modules let you add that support yourself.

An inline module is the fastest way to get started. You write your module code
directly in the Viam app's browser-based editor -- no IDE, terminal, or GitHub
account required. When you click **Save & Deploy**, Viam builds your module in
the cloud and deploys it to your machine automatically.

{{< alert title="Availability" color="tip" >}}
Inline modules are currently available to organizations that have the feature
enabled. If you do not see the **Viam-hosted** option when adding code, contact
Viam support to request access.
{{< /alert >}}

## Concepts

### What is an inline module?

An inline module is a Viam-hosted module. Viam manages the source code,
versioning, builds, and deployment for you. You edit a single source file in the
browser, and Viam handles everything else:

- **Source code** is stored and versioned by Viam (not in a git repository).
- **Builds** run automatically in the cloud when you save.
- **Deployment** happens automatically -- machines configured with your module
  receive the new version within minutes.

### Inline modules versus externally managed modules

|                          | Inline (Viam-hosted)                                   | Externally managed                                            |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------- |
| **Where you write code** | Browser editor in the Viam app                         | Your own IDE, locally or in a repo                            |
| **Source control**       | Managed by Viam                                        | Your own git repository                                       |
| **Build system**         | Automatic cloud builds on save                         | CLI upload or GitHub Actions                                  |
| **Versioning**           | Automatic (`0.0.1`, `0.0.2`, ...)                      | You choose semantic versions                                  |
| **Visibility**           | Private to your organization                           | Private or public                                             |
| **Best for**             | Prototyping, simple control logic, no-toolchain setups | Production modules, public distribution, complex dependencies |

Both types run identically at runtime -- as child processes communicating with
`viam-server` over gRPC. The difference is how you create, edit, and deploy the
module.

If you want to manage your own source code and build pipeline, see
[Write a Driver Module](/operate/modules/write-a-driver-module/) or
[Write a Logic Module](/operate/modules/write-a-logic-module/) instead.

### The Generic service

Inline modules create a Generic **service** (not a component). The Generic
service provides a single method -- `DoCommand` -- that accepts an arbitrary
JSON command and returns a JSON response. Your control logic goes inside
`DoCommand`.

Use the Generic service when:

- You want to coordinate multiple components (read a sensor, move a servo).
- You need a simple command-response interface.
- You are prototyping and want to iterate quickly.

## Steps

### 1. Create the module

1. In the [Viam app](https://app.viam.com), navigate to your machine's
   **CONFIGURE** tab.
2. Click **+** and select **Control code**.
3. In the "Choose where to host your code" dialog, select **Viam-hosted** and
   click **Choose**.
4. Name your module (for example, `servo-distance-control`) and choose a language
   (**Python** or **Go**).
5. Click **Create module**.

The browser opens the code editor with a working template that includes all
necessary imports and method stubs.

### 2. Understand the template

The editor opens a single file -- your module's main source file. The template
includes three methods you need to fill in:

{{< tabs >}}
{{% tab name="Python" %}}

The editable file is `src/models/generic_service.py`. It contains a class that
extends `GenericService` and `EasyResource`:

```python
class MyGenericService(GenericService, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "my-module"), "generic-service"
    )
```

The three methods to implement:

- **`validate_config`** -- check that configuration attributes are valid and
  declare dependencies.
- **`new`** -- initialize your service with attributes and dependencies.
- **`do_command`** -- your control logic.

{{< alert title="Important" color="caution" >}}
Do not change the class name or the `MODEL` triplet. Viam uses these
auto-generated values to identify your module. Changing them will break your
inline module.
{{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

The editable file is `module.go`. It contains a struct, a config type, and
registration logic:

```go
var GenericService = resource.NewModel(
    "my-org", "my-module", "generic-service",
)

func init() {
    resource.RegisterService(genericservice.API, GenericService,
        resource.Registration[resource.Resource, *Config]{
            Constructor: newGenericService,
        },
    )
}
```

The three areas to implement:

- **`Validate`** on the `Config` struct -- check attributes, return
  dependencies.
- **`NewGenericService`** -- initialize the service with attributes and
  dependencies.
- **`DoCommand`** -- your control logic.

{{< alert title="Important" color="caution" >}}
Do not change the model name triplet, struct names, or public function names.
Viam uses these auto-generated values to identify your module. Changing them
will break your inline module.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

### 3. Implement validate_config

The validate method runs every time the machine configuration changes. It checks
that the attributes passed to your service are valid and declares dependencies
on other components or services.

This example validates attributes for a distance-responsive servo controller --
a service that reads an ultrasonic sensor and adjusts a servo angle based on
distance:

{{< tabs >}}
{{% tab name="Python" %}}

```python
@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    attrs = struct_to_dict(config.attributes)

    # Required numeric attributes
    sensor_range_start = attrs.get("sensor_range_start")
    if sensor_range_start is None or not isinstance(
        sensor_range_start, (int, float)
    ):
        raise ValueError(
            "attribute 'sensor_range_start' is required "
            "and must be an int or float value"
        )

    sensor_range_end = attrs.get("sensor_range_end")
    if sensor_range_end is None or not isinstance(
        sensor_range_end, (int, float)
    ):
        raise ValueError(
            "attribute 'sensor_range_end' is required "
            "and must be an int or float value"
        )

    # Required dependency attributes
    required_deps: List[str] = []

    servo_name = attrs.get("servo")
    if not isinstance(servo_name, str) or not servo_name:
        raise ValueError(
            "attribute 'servo' (non-empty string) is required"
        )
    required_deps.append(servo_name)

    sensor_name = attrs.get("sensor")
    if not isinstance(sensor_name, str) or not sensor_name:
        raise ValueError(
            "attribute 'sensor' (non-empty string) is required"
        )
    required_deps.append(sensor_name)

    return required_deps, []
```

The return value is a tuple of two lists:

1. **Required dependencies** -- component or service names that must exist and
   be ready before your service starts.
2. **Optional dependencies** -- names your service can use if available but
   does not require.

{{% /tab %}}
{{% tab name="Go" %}}

```go
type Config struct {
    SensorRangeStart float64 `json:"sensor_range_start"`
    SensorRangeEnd   float64 `json:"sensor_range_end"`
    ServoAngleMin    *int64  `json:"servo_angle_min"`
    ServoAngleMax    *int64  `json:"servo_angle_max"`
    Reversed         *bool   `json:"reversed"`
    Servo            string  `json:"servo"`
    Sensor           string  `json:"sensor"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.SensorRangeStart == 0 {
        return nil, nil, fmt.Errorf(
            "%s: 'sensor_range_start' is required and must be non-zero",
            path,
        )
    }
    if cfg.SensorRangeEnd == 0 {
        return nil, nil, fmt.Errorf(
            "%s: 'sensor_range_end' is required and must be non-zero",
            path,
        )
    }

    requiredDeps := []string{}
    if cfg.Servo == "" {
        return nil, nil, fmt.Errorf(
            "%s: 'servo' (non-empty string) is required", path,
        )
    }
    requiredDeps = append(requiredDeps, cfg.Servo)

    if cfg.Sensor == "" {
        return nil, nil, fmt.Errorf(
            "%s: 'sensor' (non-empty string) is required", path,
        )
    }
    requiredDeps = append(requiredDeps, cfg.Sensor)

    return requiredDeps, []string{}, nil
}
```

The `Validate` method returns two slices (required dependencies and optional
dependencies) and an error.

{{% /tab %}}
{{< /tabs >}}

### 4. Implement the constructor

The constructor runs when the service is first created and again whenever its
configuration changes. Use it to parse attributes and resolve dependencies.

{{< tabs >}}
{{% tab name="Python" %}}

```python
@classmethod
def new(
    cls, config: ComponentConfig,
    dependencies: Mapping[ResourceName, ResourceBase]
) -> Self:
    attrs = struct_to_dict(config.attributes)
    self = cls(config.name)

    # Required attributes
    self.sensor_range_start = float(attrs.get("sensor_range_start"))
    self.sensor_range_end = float(attrs.get("sensor_range_end"))

    # Optional attributes with defaults
    self.servo_angle_min = float(attrs.get("servo_angle_min", 0))
    self.servo_angle_max = float(attrs.get("servo_angle_max", 180))
    self.reversed = attrs.get("reversed", False)

    # Resolve dependencies
    servo_name = attrs.get("servo")
    sensor_name = attrs.get("sensor")
    self.servo = dependencies[Servo.get_resource_name(servo_name)]
    self.sensor = dependencies[Sensor.get_resource_name(sensor_name)]

    return self
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func NewGenericService(
    ctx context.Context, deps resource.Dependencies,
    name resource.Name, conf *Config, logger logging.Logger,
) (resource.Resource, error) {
    cancelCtx, cancelFunc := context.WithCancel(context.Background())

    // Apply defaults for optional fields
    servoAngleMin := int64(0)
    if conf.ServoAngleMin != nil {
        servoAngleMin = *conf.ServoAngleMin
    }
    servoAngleMax := int64(180)
    if conf.ServoAngleMax != nil {
        servoAngleMax = *conf.ServoAngleMax
    }
    reversed := false
    if conf.Reversed != nil {
        reversed = *conf.Reversed
    }

    // Resolve dependencies
    servoDep, err := servo.FromProvider(deps, conf.Servo)
    if err != nil {
        return nil, err
    }
    sensorDep, err := sensor.FromProvider(deps, conf.Sensor)
    if err != nil {
        return nil, err
    }

    return &genericService{
        name:             name,
        logger:           logger,
        cfg:              conf,
        cancelCtx:        cancelCtx,
        cancelFunc:       cancelFunc,
        servo:            servoDep,
        sensor:           sensorDep,
        sensorRangeStart: conf.SensorRangeStart,
        sensorRangeEnd:   conf.SensorRangeEnd,
        servoAngleMin:    servoAngleMin,
        servoAngleMax:    servoAngleMax,
        reversed:         reversed,
    }, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Implement DoCommand

`DoCommand` is where your control logic goes. This example reads a distance
sensor and maps the reading to a servo angle:

{{< tabs >}}
{{% tab name="Python" %}}

```python
async def do_command(
    self, command: Mapping[str, ValueTypes], *,
    timeout: Optional[float] = None, **kwargs
) -> Mapping[str, ValueTypes]:
    readings = await self.sensor.get_readings()
    if not readings:
        raise ValueError("No sensor readings available")

    value = next(iter(readings.values()))

    # Map sensor range to servo angle range
    t = (value - self.sensor_range_start) / (
        self.sensor_range_end - self.sensor_range_start
    )
    t = max(0.0, min(1.0, 1.0 - t if self.reversed else t))

    angle = self.servo_angle_min + t * (
        self.servo_angle_max - self.servo_angle_min
    )
    await self.servo.move(int(angle))

    return {"servo_angle_deg": angle}
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (s *genericService) DoCommand(
    ctx context.Context, cmd map[string]interface{},
) (map[string]interface{}, error) {
    readings, err := s.sensor.Readings(ctx, nil)
    if err != nil {
        return nil, err
    }
    value, ok := readings["distance"].(float64)
    if !ok {
        return nil, fmt.Errorf("sensor reading 'distance' must be a float64")
    }

    // Map sensor range to servo angle range
    t := (value - s.sensorRangeStart) /
        (s.sensorRangeEnd - s.sensorRangeStart)
    if t < 0 { t = 0 } else if t > 1 { t = 1 }
    if s.reversed { t = 1 - t }

    angle := float64(s.servoAngleMin) +
        t * (float64(s.servoAngleMax) - float64(s.servoAngleMin))
    return map[string]interface{}{
        "servo_angle_deg": angle,
    }, s.servo.Move(ctx, uint32(angle), nil)
}
```

{{% /tab %}}
{{< /tabs >}}

In this example no DoCommand payload is used. You can use the command payload to
customize behavior per invocation. Attributes are constant across all
invocations; the DoCommand payload can vary with each call.

### 6. Save and deploy

1. Click **Save & Deploy** in the code editor toolbar.
2. Viam uploads your code as a new version and starts a cloud build.
3. Builds typically take 2-5 minutes. You can continue editing while a build
   runs -- your next save creates a new version.
4. If the build fails, click **View Logs** to see what went wrong.

Each save creates a new version in your module's history. You can switch between
versions using the version dropdown in the editor toolbar.

### 7. Test on a machine

#### Add the module to a machine

1. In the code editor, click **Add to machine**.
2. Select a location, machine, and part.
3. Click **Add**.

The Viam app navigates you to the machine's **CONFIGURE** tab with your module
added.

#### Configure the service

1. In the module section, click **Add** to add a model of your generic service.
2. Click **+** to add each dependency your service requires (for example, a servo and
   a sensor). Configure each dependency with the appropriate attributes.
3. Configure the attributes for your generic service:

```json
{
  "sensor_range_start": 0.05,
  "sensor_range_end": 0.3,
  "servo_angle_min": 40,
  "servo_angle_max": 270,
  "reversed": true,
  "servo": "servo-1",
  "sensor": "sensor-1"
}
```

4. Click **Save**.

#### Send test commands

1. On the **CONFIGURE** tab, expand your generic service's card.
2. Find the **DoCommand** section.
3. Enter a command (or an empty map `{}` if your DoCommand does not use the
   payload):

```json
{}
```

4. Click **Execute**. You should see a response like:

```json
{ "servo_angle_deg": 155.0 }
```

### 8. Automate with a scheduled job

The DoCommand section in the Viam app runs your logic once per click. To have
it run automatically:

1. Click **+** and select **Job**.
2. Name the job and click **Create**.
3. Choose a schedule. For control logic that should always run, select
   **Continuous**.
4. Select your generic service as the resource.
5. Edit the DoCommand payload or leave it as an empty map if no payload is
   needed.
6. Click **Save**.

## Try It

1. Create a new inline module from the **+** menu.
2. Implement `validate_config`, the constructor, and `do_command`.
3. Click **Save & Deploy** and wait for the build to complete.
4. Add the module to a machine and configure the service with dependencies.
5. Execute a DoCommand and verify the response.
6. Set up a scheduled job to run the logic continuously.

## Troubleshooting

{{< expand "\"Viam-hosted\" option not visible" >}}

The inline module feature is gated by a feature flag. If you do not see the
"Viam-hosted" option when clicking **+** → **Control code**, your organization
may not have the feature enabled. Contact Viam support to request access.

{{< /expand >}}

{{< expand "Build fails after saving" >}}

- Click **View Logs** in the build progress bar to see the error.
- Common causes: syntax errors, missing imports, incompatible dependencies.
- You can fix the code and save again -- each save creates a new version.

{{< /expand >}}

{{< expand "Module not appearing on machine" >}}

- Verify the machine is online and connected to the cloud.
- Check that you added the module using the **Add to machine** button in the
  code editor, or that the module appears in the machine's configuration.
- The module version defaults to `latest`. After a successful build, the machine
  picks up the new version automatically within a few minutes.

{{< /expand >}}

{{< expand "DoCommand returns an error" >}}

- Check that all dependencies are configured on the machine and are working.
  Use the test section of each dependency to verify them in isolation.
- Verify the attribute names in your service configuration match what
  `validate_config` expects.
- Check the **LOGS** tab for detailed error messages.

{{< /expand >}}

{{< expand "Changes to code not taking effect" >}}

- Make sure the build completed successfully. Check the build progress bar in
  the code editor.
- The machine must be online to receive the updated module. Check the machine's
  status in the Viam app.
- By default, modules are configured with version `latest`, which means every
  new build deploys automatically. If the version is pinned, update it manually.

{{< /expand >}}

## What's Next

- [Write a Driver Module](/operate/modules/write-a-driver-module/) -- build a module
  with a typed resource API when you need to manage your own source code and
  build pipeline.
- [Write a Logic Module](/operate/modules/write-a-logic-module/) -- build control
  logic as an externally managed module with full IDE support.
- [Deploy a Module](/operate/modules/deploy-a-module/) -- package and upload
  a module to the Viam registry for distribution to other machines or users.
