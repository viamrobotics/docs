---
linkTitle: "Write a Driver Module"
title: "Write a Hardware Driver Module"
weight: 20
layout: "docs"
type: "docs"
description: "Build a module that implements a resource API and runs as a separate process."
date: "2025-01-30"
aliases:
  - /build/development/write-a-module/
  - /development/write-a-module/
  - /development/write-a-driver-module/
  - /registry/create/
  - /use-cases/create-module/
  - /how-tos/create-module/
  - /how-tos/sensor-module/
  - /registry/advanced/iterative-development/
  - /build/program/extend/modular-resources/
  - /program/extend/modular-resources/
  - /extend/
  - /extend/modular-resources/
  - /extend/modular-resources/create/
  - /build/program/extend/modular-resources/key-concepts/
  - /modular-resources/key-concepts/
  - /modular-resources/
  - /extend/modular-resources/examples/custom-arm/
  - /modular-resources/examples/custom-arm/
  - /registry/examples/custom-arm/
  - /program/extend/modular-resources/examples/
  - /extend/modular-resources/examples/
  - /modular-resources/examples/
  - /registry/examples/
  - /operate/get-started/other-hardware/
  - /operate/get-started/other-hardware/create-module/
  - /operate/modules/other-hardware/create-module/
  - /how-tos/hello-world-module/
  - /operate/get-started/other-hardware/hello-world-module/
  - /operate/modules/create-module/hello-world-module/
  - /operate/modules/supported-hardware/hello-world-module/
  - /operate/modules/support-hardware/
---

You want to use hardware that Viam doesn't support out of the box. A driver
module integrates it with the platform by implementing a standard resource API
(sensor, camera, motor, or any other type). Once your hardware speaks a Viam
API, data capture, TEST cards, the SDKs, and other platform features work
with it automatically.

A driver module runs as a separate process alongside `viam-server`. It has its
own dependencies, can crash without affecting `viam-server`, and can be
packaged and distributed through the Viam registry.

{{< alert title="Driver modules versus local modules" color="tip" >}}
Both [local modules](/operate/modules/write-an-inline-module/) and registry modules
can implement any resource API. All modules run as separate child processes
alongside `viam-server`. The difference is deployment: a local module references
an executable on the machine's filesystem, while a registry module is downloaded
from the Viam registry. Local modules cannot be distributed through the registry.

Choose a registry module (this page covers building one) for production use and
distribution. Choose a local module for quick prototyping on a single machine.
{{< /alert >}}

## Concepts

### Choosing a resource API

Viam defines standard APIs for common resource types. Pick the API that best
matches your hardware or service:

| API | Use when your hardware... | Key methods |
|-----|---------------------------|-------------|
| `sensor` | Produces readings (temperature, distance, humidity) | `GetReadings` |
| `camera` | Produces images or point clouds | `GetImage`, `GetPointCloud` |
| `motor` | Drives rotational or linear motion | `SetPower`, `GoFor`, `Stop` |
| `servo` | Moves to angular positions | `Move`, `GetPosition` |
| `board` | Exposes GPIO pins, analog readers, digital interrupts | `GPIOPinByName`, `AnalogByName` |
| `encoder` | Tracks position or rotation | `GetPosition`, `ResetPosition` |
| `movement_sensor` | Reports position, orientation, velocity | `GetPosition`, `GetLinearVelocity` |
| `generic` | Does not fit any of the above | `DoCommand` |

For the full list of component and service APIs, see
[Resource APIs](/dev/reference/apis/).

Using the right API means data capture, TEST cards, and other platform
features work with your component automatically.

Every resource also has a `DoCommand` method. Use it for functionality that
does not map to the standard API methods -- for example, a sensor that also has
a calibration routine. `DoCommand` accepts and returns arbitrary key-value maps.

### Module lifecycle

Every module goes through a defined lifecycle:

1. **Startup** -- `viam-server` launches the module as a separate process. The
   module registers its models and opens a gRPC connection back to the server.
2. **Validation** -- For each configured resource, `viam-server` calls the
   model's config validation method to check attributes and declare
   dependencies.
3. **Creation** -- If validation passes, `viam-server` calls the model's
   constructor with the resolved dependencies.
4. **Reconfiguration** -- If the user changes the configuration, `viam-server`
   calls the validation method again, then the reconfiguration method.
5. **Shutdown** -- `viam-server` calls the resource's close method. Clean up
   resources here.

For more detail, see [Module Lifecycle](/operate/modules/lifecycle-of-a-module/).

### Dependencies

Dependencies let your resource use other resources on the same machine. You
declare dependencies in your config validation method by returning the names of
resources your module needs. `viam-server` resolves these, ensures the
depended-on resources are ready, and passes them to your constructor.

## Steps

When writing a module, follow the steps outlined below. To illustrate each step we'll use a sensor module as a worked example. The same patterns
apply to any resource type -- substitute the appropriate API and methods for
your use case.

### 1. Generate the module

Run the Viam CLI generator:

```bash
viam module generate
```

| Prompt | What to enter | Why |
|--------|---------------|-----|
| Module name | `my-sensor-module` | A short, descriptive name |
| Language | `python` or `go` | Your implementation language |
| Visibility | `private` | Keep it private while developing |
| Namespace | Your organization namespace | Scopes the module to your org |
| Resource subtype | `sensor` | The resource API to implement |
| Model name | `my-sensor` | The model name for your sensor |
| Register | `yes` | Registers the module with Viam |

The generator creates a complete project with the following files:

{{< tabs >}}
{{% tab name="Python" %}}

| File | Purpose |
|------|---------|
| `src/main.py` | Entry point -- starts the module server |
| `src/models/my_sensor.py` | Resource class skeleton -- you will edit this |
| `requirements.txt` | Python dependencies |
| `meta.json` | Module metadata for the registry |
| `setup.sh` | Installs dependencies into a virtualenv |
| `build.sh` | Packages the module for upload |
| `.github/workflows/deploy.yml` | CI workflow for cloud builds |

{{% /tab %}}
{{% tab name="Go" %}}

| File | Purpose |
|------|---------|
| `cmd/module/main.go` | Entry point -- starts the module server |
| `my_sensor_module.go` | Resource implementation skeleton -- you will edit this |
| `go.mod` | Go module definition |
| `Makefile` | Build targets |
| `meta.json` | Module metadata for the registry |
| `.github/workflows/deploy.yml` | CI workflow for cloud builds |

{{% /tab %}}
{{< /tabs >}}

### 2. Implement the resource API

Open the generated resource file. The generator creates a class (Python) or
struct (Go) with stub methods. You need to make three changes:

1. Define your config attributes.
2. Add validation logic.
3. Implement the API methods for your resource type.

The following example builds a sensor that reads temperature and humidity from
a custom HTTP API endpoint. Replace the HTTP call with whatever data source
your sensor uses.

#### Define your config attributes

Config attributes are the fields a user sets when they configure your component
in the Viam app. The generator creates an empty config; add a field for each
attribute your module needs.

{{< tabs >}}
{{% tab name="Python" %}}

In `src/models/my_sensor.py`, add instance attributes to your class. These will
be set in the `reconfigure` method:

```python
class MySensor(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "my-sensor-module"), "my-sensor"
    )

    # Add your config attributes as instance variables
    source_url: str
    poll_interval: float
```

{{% /tab %}}
{{% tab name="Go" %}}

In the generated `.go` file, find the empty `Config` struct and add fields.
Each field needs a `json` tag that matches the attribute name users will set in
their config JSON:

```go
type Config struct {
    SourceURL    string  `json:"source_url"`
    PollInterval float64 `json:"poll_interval"`
}
```

{{% /tab %}}
{{< /tabs >}}

#### Add validation logic

The generator creates an empty validation method. Add checks for required
fields and return any [dependencies](#dependencies) your module needs.

{{< tabs >}}
{{% tab name="Python" %}}

Find `validate_config` in your class and add validation:

```python
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "source_url" not in fields:
            raise Exception("source_url is required")
        if not fields["source_url"].string_value.startswith("http"):
            raise Exception("source_url must be an HTTP or HTTPS URL")
        return [], []  # No required or optional dependencies
```

{{% /tab %}}
{{% tab name="Go" %}}

Find the `Validate` method on your `Config` struct and add validation:

```go
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.SourceURL == "" {
        return nil, nil, fmt.Errorf("source_url is required")
    }
    return nil, nil, nil // No required or optional dependencies
}
```

{{% /tab %}}
{{< /tabs >}}

The validation method returns two lists: required dependencies and optional
dependencies. For a standalone sensor with no dependencies, return empty lists.
See [Step 5](#5-handle-dependencies) for modules that depend on other
components.

#### Implement the constructor and reconfigure method

The constructor creates your resource and the reconfigure method updates it when
the config changes. In Python, the typical pattern is for `new` to call
`reconfigure` so the config-reading logic lives in one place.

{{< tabs >}}
{{% tab name="Python" %}}

Update `new` and add a `reconfigure` method:

```python
    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]) -> None:
        fields = config.attributes.fields
        self.source_url = fields["source_url"].string_value
        self.poll_interval = (
            fields["poll_interval"].number_value
            if "poll_interval" in fields
            else 10.0
        )
```

{{% /tab %}}
{{% tab name="Go" %}}

Find the generated constructor function. Update it to read your config fields
and initialize your struct:

```go
func newMySensor(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (sensor.Sensor, error) {
    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }

    timeout := time.Duration(cfg.PollInterval) * time.Second
    if timeout == 0 {
        timeout = 10 * time.Second
    }

    return &MySensor{
        Named:     conf.ResourceName().AsNamed(),
        logger:    logger,
        sourceURL: cfg.SourceURL,
        client:    &http.Client{Timeout: timeout},
    }, nil
}
```

You will also need to add fields to the generated struct for any state your
module needs at runtime:

```go
type MySensor struct {
    resource.Named
    resource.AlwaysRebuild
    logger    logging.Logger
    sourceURL string
    client    *http.Client
}
```

The generated struct includes `resource.AlwaysRebuild`, which tells
`viam-server` to destroy and re-create the resource on every config change.
This is the simplest approach and works well for most modules. For in-place
reconfiguration, see [Step 6](#6-handle-reconfiguration-optional).

{{% /tab %}}
{{< /tabs >}}

#### Implement the API method

For a sensor, the key method is `GetReadings`, which returns a map of reading
names to values. This is the method that data capture calls and your application
code queries.

The generator creates a stub that returns an error. Replace it with your
implementation:

{{< tabs >}}
{{% tab name="Python" %}}

Add a `get_readings` method to your class. The return type is
`Mapping[str, SensorReading]` (import `SensorReading` from `viam.utils`):

```python
    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, SensorReading]:
        try:
            response = requests.get(self.source_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return {
                "temperature": data["temp"],
                "humidity": data["humidity"],
            }
        except requests.RequestException as e:
            self.logger.error(f"Failed to read from {self.source_url}: {e}")
            return {"error": str(e)}
```

{{% /tab %}}
{{% tab name="Go" %}}

Find the `Readings` method stub and replace it:

```go
type sensorResponse struct {
    Temp     float64 `json:"temp"`
    Humidity float64 `json:"humidity"`
}

func (s *MySensor) Readings(
    ctx context.Context,
    extra map[string]interface{},
) (map[string]interface{}, error) {
    resp, err := s.client.Get(s.sourceURL)
    if err != nil {
        s.logger.CErrorw(ctx, "failed to read from source",
            "url", s.sourceURL, "error", err)
        return nil, fmt.Errorf("failed to read from %s: %w", s.sourceURL, err)
    }
    defer resp.Body.Close()

    var data sensorResponse
    if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
        return nil, fmt.Errorf("failed to decode response: %w", err)
    }

    return map[string]interface{}{
        "temperature": data.Temp,
        "humidity":    data.Humidity,
    }, nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{< expand "View the complete resource file" >}}

For reference, here is the complete resource file after all the changes above.

{{< tabs >}}
{{% tab name="Python" %}}

`src/models/my_sensor.py`:

```python
import requests
from typing import Any, ClassVar, Mapping, Optional, Sequence, Self, Tuple

from viam.components.sensor import Sensor
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading


class MySensor(Sensor, EasyResource):
    """A custom sensor that reads from an HTTP endpoint."""

    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "my-sensor-module"), "my-sensor"
    )

    source_url: str
    poll_interval: float

    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "source_url" not in fields:
            raise Exception("source_url is required")
        if not fields["source_url"].string_value.startswith("http"):
            raise Exception("source_url must be an HTTP or HTTPS URL")
        return [], []

    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]) -> None:
        fields = config.attributes.fields
        self.source_url = fields["source_url"].string_value
        self.poll_interval = (
            fields["poll_interval"].number_value
            if "poll_interval" in fields
            else 10.0
        )

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, SensorReading]:
        try:
            response = requests.get(self.source_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return {
                "temperature": data["temp"],
                "humidity": data["humidity"],
            }
        except requests.RequestException as e:
            self.logger.error(f"Failed to read from {self.source_url}: {e}")
            return {"error": str(e)}

    async def close(self):
        self.logger.info("Shutting down MySensor")
```

{{% /tab %}}
{{% tab name="Go" %}}

`my_sensor_module.go`:

```go
package mysensormodule

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "time"

    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/resource"
)

var Model = resource.NewModel("my-org", "my-sensor-module", "my-sensor")

type Config struct {
    SourceURL    string  `json:"source_url"`
    PollInterval float64 `json:"poll_interval"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.SourceURL == "" {
        return nil, nil, fmt.Errorf("source_url is required")
    }
    return nil, nil, nil
}

func init() {
    resource.RegisterComponent(sensor.API, Model,
        resource.Registration[sensor.Sensor, *Config]{
            Constructor: newMySensor,
        },
    )
}

type MySensor struct {
    resource.Named
    resource.AlwaysRebuild
    logger    logging.Logger
    sourceURL string
    client    *http.Client
}

func newMySensor(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (sensor.Sensor, error) {
    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }

    timeout := time.Duration(cfg.PollInterval) * time.Second
    if timeout == 0 {
        timeout = 10 * time.Second
    }

    return &MySensor{
        Named:     conf.ResourceName().AsNamed(),
        logger:    logger,
        sourceURL: cfg.SourceURL,
        client:    &http.Client{Timeout: timeout},
    }, nil
}

type sensorResponse struct {
    Temp     float64 `json:"temp"`
    Humidity float64 `json:"humidity"`
}

func (s *MySensor) Readings(
    ctx context.Context,
    extra map[string]interface{},
) (map[string]interface{}, error) {
    resp, err := s.client.Get(s.sourceURL)
    if err != nil {
        s.logger.CErrorw(ctx, "failed to read from source",
            "url", s.sourceURL, "error", err)
        return nil, fmt.Errorf("failed to read from %s: %w", s.sourceURL, err)
    }
    defer resp.Body.Close()

    var data sensorResponse
    if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
        return nil, fmt.Errorf("failed to decode response: %w", err)
    }

    return map[string]interface{}{
        "temperature": data.Temp,
        "humidity":    data.Humidity,
    }, nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

#### Understanding the entry point

The generator also creates the entry point file that `viam-server` launches.
You typically do not need to modify it.

{{< tabs >}}
{{% tab name="Python" %}}

`src/main.py`:

```python
import asyncio
from viam.module.module import Module
from models.my_sensor import MySensor  # noqa: F401


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
```

`run_from_registry()` automatically discovers all imported resource classes and
registers them with `viam-server`. If you add more models to your module, import
them here.

{{% /tab %}}
{{% tab name="Go" %}}

`cmd/module/main.go`:

```go
package main

import (
    mysensormodule "my-org/my-sensor-module"
    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
)

func main() {
    module.ModularMain(resource.APIModel{sensor.API, mysensormodule.Model})
}
```

`ModularMain` handles socket parsing, signal handling, and graceful shutdown.
The import of the resource package triggers its `init()` function, which calls
`resource.RegisterComponent` to register the model. If you add more models,
add more `resource.APIModel` entries to the `ModularMain` call.

{{% /tab %}}
{{< /tabs >}}

### 3. Test locally

Configure the module on your machine and verify it works.

**Configure as a local module:**

1. In the [Viam app](https://app.viam.com), navigate to your machine's
   **CONFIGURE** tab.
2. Click **+**, select **Advanced**, then **Local module**.
3. Set the **Executable path** to your module binary or script.
4. Click **Create**.
5. Click **+**, select **Advanced**, then **Local component**.
6. Select your module, set the type and model, and configure attributes:

   ```json
   {
     "source_url": "https://api.example.com/sensor/data"
   }
   ```

7. Click **Save**.

**Test using the TEST card:**

1. Find your sensor component and expand the **TEST** section.
2. Your temperature and humidity values appear automatically under
   **GetReadings**.

**Get a ready-to-run code sample:**

The **CONNECT** tab on your machine's page in the Viam app provides generated
code samples in Python and Go that connect to your machine and access all
configured components. Use this as a starting point for application code that
interacts with your module.

**Rebuild and redeploy during development:**

`viam-server` does not automatically detect changes to your module's source
files or binary. After making changes, use the CLI to rebuild and redeploy:

```bash
# Build locally, transfer to machine, and restart the module
viam module reload-local --part-id <machine-part-id>

# Restart the module without rebuilding (e.g., after editing Python source)
viam module restart --part-id <machine-part-id>
```

The `reload-local` command runs your build command from `meta.json`, transfers
the artifact to the target machine, updates the machine config, and restarts
the module. Use `--no-build` to skip the build step if you already built
manually.

### 4. Add logging

Both the Python and Go SDKs provide a logger that writes to `viam-server`'s log
stream, visible in the **LOGS** tab.

{{< tabs >}}
{{% tab name="Python" %}}

```python
self.logger.info("Sensor initialized with source URL: %s", self.source_url)
self.logger.debug("Raw response from source: %s", data)
self.logger.warning("Source returned unexpected field: %s", field_name)
self.logger.error("Failed to connect to source: %s", error)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
s.logger.CInfof(ctx, "Sensor initialized with source URL: %s", s.sourceURL)
s.logger.CDebugf(ctx, "Raw response from source: %v", data)
s.logger.CWarnw(ctx, "Source returned unexpected field", "field", fieldName)
s.logger.CErrorw(ctx, "Failed to connect to source", "error", err)
```

{{% /tab %}}
{{< /tabs >}}

Use `info` for significant events, `debug` for detailed data, `warning` for
recoverable problems, and `error` for failures.

### 5. Handle dependencies

Many modules need access to other resources on the same machine. To use
another resource, you need to do three things:

1. **Declare the dependency** in your config validation method by returning the
   resource name in the required (or optional) dependencies list.
2. **Resolve the dependency** in your constructor or reconfigure method by
   looking it up from the `dependencies` map that `viam-server` passes in.
3. **Call methods on it** in your API implementation, just like any other
   typed resource.

The following example shows all three. It implements a sensor that depends on
another sensor -- it reads Celsius temperature readings from the source sensor
and converts them to Fahrenheit. Watch for the numbered comments in the code:

{{< tabs >}}
{{% tab name="Python" %}}

```python
class TempConverterSensor(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "my-sensor-module"), "temp-converter"
    )

    source_sensor: Sensor

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "source_sensor" not in fields:
            raise Exception("source_sensor is required")
        source = fields["source_sensor"].string_value
        # 1. Declare: return the source sensor name as a required dependency
        return [source], []

    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]) -> None:
        source_name = config.attributes.fields["source_sensor"].string_value
        # 2. Resolve: find the dependency in the map viam-server passes in
        for name, dep in dependencies.items():
            if name.name == source_name:
                self.source_sensor = dep
                break

    async def get_readings(self, *, extra=None, timeout=None,
                           **kwargs) -> Mapping[str, SensorReading]:
        # 3. Use: call methods on the dependency like any typed resource
        readings = await self.source_sensor.get_readings()
        celsius = readings["temperature"]
        return {"temperature_f": celsius * 9.0 / 5.0 + 32.0}
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
type ConverterConfig struct {
    SourceSensor string `json:"source_sensor"`
}

func (cfg *ConverterConfig) Validate(path string) ([]string, []string, error) {
    if cfg.SourceSensor == "" {
        return nil, nil, fmt.Errorf("source_sensor is required")
    }
    // 1. Declare: return the source sensor name as a required dependency
    return []string{cfg.SourceSensor}, nil, nil
}

type TempConverterSensor struct {
    resource.Named
    resource.AlwaysRebuild
    logger logging.Logger
    source sensor.Sensor
}

func newTempConverter(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (sensor.Sensor, error) {
    cfg, err := resource.NativeConfig[*ConverterConfig](conf)
    if err != nil {
        return nil, err
    }

    // 2. Resolve: look up the dependency by name from the map viam-server passes in
    src, err := sensor.FromProvider(deps, cfg.SourceSensor)
    if err != nil {
        return nil, fmt.Errorf("source sensor %q not found: %w",
            cfg.SourceSensor, err)
    }

    return &TempConverterSensor{
        Named:  conf.ResourceName().AsNamed(),
        logger: logger,
        source: src,
    }, nil
}

func (s *TempConverterSensor) Readings(
    ctx context.Context,
    extra map[string]interface{},
) (map[string]interface{}, error) {
    // 3. Use: call methods on the dependency like any typed resource
    readings, err := s.source.Readings(ctx, extra)
    if err != nil {
        return nil, fmt.Errorf("failed to read source sensor: %w", err)
    }
    celsius, ok := readings["temperature"].(float64)
    if !ok {
        return nil, fmt.Errorf("source sensor did not return a temperature reading")
    }
    return map[string]interface{}{
        "temperature_f": celsius*9.0/5.0 + 32.0,
    }, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 6. Handle reconfiguration (optional)

When a user changes a resource's configuration, `viam-server` calls your
reconfiguration method instead of destroying and re-creating the resource.
This is faster and preserves internal state like open connections.

The generated code uses `resource.AlwaysRebuild` (Go) by default, which
tells `viam-server` to destroy and re-create the resource on every config
change. This is the simplest approach and works well for most modules.

For in-place reconfiguration, implement the reconfiguration method to update
your resource's fields directly:

{{< tabs >}}
{{% tab name="Python" %}}

Implement `reconfigure` to update your resource from the new config. This
method is also typically called from `new` (see the example in Step 2):

```python
def reconfigure(self, config: ComponentConfig,
                dependencies: Mapping[ResourceName, ResourceBase]) -> None:
    fields = config.attributes.fields
    self.source_url = fields["source_url"].string_value
    self.poll_interval = (
        fields["poll_interval"].number_value
        if "poll_interval" in fields
        else 10.0
    )
```

{{% /tab %}}
{{% tab name="Go" %}}

Remove `resource.AlwaysRebuild` from your struct and implement `Reconfigure`:

```go
type MySensor struct {
    resource.Named
    logger    logging.Logger
    sourceURL string
    client    *http.Client
}

func (s *MySensor) Reconfigure(ctx context.Context,
    deps resource.Dependencies, conf resource.Config) error {
    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return err
    }
    s.sourceURL = cfg.SourceURL
    s.client.Timeout = time.Duration(cfg.PollInterval) * time.Second
    return nil
}
```

Go provides these helper traits as alternatives to writing a `Reconfigure`
method. Embed one in your struct:

| Trait | Behavior |
|-------|----------|
| `resource.AlwaysRebuild` | Resource is destroyed and re-created on every config change (the generated default). |
| `resource.TriviallyReconfigurable` | Config changes are accepted silently with no action. |

{{% /tab %}}
{{< /tabs >}}

### 7. Use the module data directory

Every module gets a persistent data directory at the path specified by the
`VIAM_MODULE_DATA` environment variable. Use this for caches, databases, or
any state that should survive module restarts.

{{< tabs >}}
{{% tab name="Python" %}}

```python
import os

data_dir = os.environ.get("VIAM_MODULE_DATA", "/tmp")
cache_path = os.path.join(data_dir, "readings_cache.json")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
dataDir := os.Getenv("VIAM_MODULE_DATA")
cachePath := filepath.Join(dataDir, "readings_cache.json")
```

{{% /tab %}}
{{< /tabs >}}

The directory is created automatically by `viam-server` at
`$VIAM_HOME/module-data/<machine-id>/<module-name>/` (where `VIAM_HOME`
defaults to `~/.viam`) and persists across module
restarts and reconfigurations.

## Try It

1. Generate a sensor module using `viam module generate`.
2. Open the generated resource file and implement your config validation and
   `GetReadings` method.
3. Configure the module on your machine as a local module.
4. Expand the **TEST** section on your sensor. Verify readings appear
   automatically under **GetReadings**.
5. Enable data capture on the sensor. Wait one minute, then check the **DATA**
   tab to confirm readings are flowing to the cloud.
6. Add a new key to the readings map (for example, `"pressure": 1013.25`).
   Rebuild and redeploy with `viam module reload-local`. Verify the new reading
   appears on the TEST card.

## Troubleshooting

{{< expand "Module crashes on startup" >}}

- Check the **LOGS** tab for the crash traceback. The most common cause is a
  missing dependency -- a Python import not in `requirements.txt` or a Go
  package not in `go.mod`.
- For Python, verify the module runs outside of `viam-server`:
  `python3 -m src.main` (from your module directory, with the virtualenv
  activated).
- For Go, verify the binary runs: `./bin/<your-module-name>` (the output path
  is set in your `Makefile`).
- Check that your entrypoint script has execute permissions: `chmod +x run.sh`.

{{< /expand >}}

{{< expand "Module times out on startup" >}}

`viam-server` expects the module to respond to a ready check within about 15
seconds of launch. If your module does heavy initialization (loading large
files, connecting to slow services), it may time out.

- Move slow initialization out of `init()` or model registration and into the
  constructor instead, where it runs per-resource rather than blocking module
  startup.
- Check the **LOGS** tab for timeout errors.

{{< /expand >}}

{{< expand "Dependency not found" >}}

- Confirm the dependency name returned by your config validation method matches
  the resource name on the machine exactly (names are compared as strings, so
  case and spelling must match).
- Verify the depended-on resource exists and is configured correctly.
- Check for circular dependencies -- if A depends on B and B depends on A,
  both will fail to start. Check the **LOGS** tab for "circular dependency"
  errors.

{{< /expand >}}

{{< expand "Readings returning None or nil" >}}

- Add logging inside your `GetReadings` implementation to see what data your
  source returns.
- `GetReadings` must return a non-nil map. If it returns `nil` (Go) or `None`
  (Python), `viam-server` treats this as an error.
- Check network connectivity from the machine if your sensor reads from an
  external source.

{{< /expand >}}

{{< expand "Module not restarting after code changes" >}}

`viam-server` does not watch your module's source files or binary for changes.
To deploy changes:

- Use `viam module reload-local --part-id <id>` to rebuild and redeploy.
- Use `viam module restart --part-id <id>` to restart without rebuilding.

{{< /expand >}}

{{< expand "Data capture not recording readings" >}}

Data capture requires both the data management service and a per-resource
capture configuration:

- Verify the data management service is configured and does not have
  `capture_disabled` set to `true`.
- Verify your sensor component has a data capture configuration with
  `capture_frequency_hz` greater than `0`.
- Check that `GetReadings` returns a valid, non-nil map.
- If the capture frequency is very low, you may need to wait longer to see
  data appear on the [**Data** page](https://app.viam.com/data).

{{< /expand >}}

## What's Next

- [Write a Logic Module](/operate/modules/write-a-logic-module/) -- write a module
  that monitors sensors, coordinates components, or runs automation logic.
- [Deploy a Module](/operate/modules/deploy-a-module/) -- package your module
  and upload it to the Viam registry for distribution.
