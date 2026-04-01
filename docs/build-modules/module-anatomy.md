---
linkTitle: "Anatomy of a module"
title: "Anatomy of a module"
weight: 5
layout: "docs"
type: "docs"
description: "Understand the directory structure and key files that make up a Viam module."
---

When you run `viam module generate`, the CLI creates a complete project with
everything you need to build, test, and deploy a module. This page explains
the purpose of each file and when you need to edit it.

The examples on this page use a logic module called `temp-monitor` that
monitors a temperature sensor and logs a warning when readings exceed a
threshold. It depends on one sensor and uses `DoCommand` to report its
current state.

## Directory structure

{{< tabs >}}
{{% tab name="Python" %}}

```text
temp-monitor/
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI workflow for cloud builds
├── src/
│   ├── main.py                   # Entry point
│   └── models/
│       └── temp_monitor.py       # Resource implementation
├── build.sh                      # Packages the module for upload
├── meta.json                     # Module metadata for the registry
├── requirements.txt              # Python dependencies
├── run.sh                        # Entrypoint script for viam-server
└── setup.sh                      # Installs dependencies into a virtualenv
```

{{% /tab %}}
{{% tab name="Go" %}}

```text
temp-monitor/
├── .github/
│   └── workflows/
│       └── deploy.yml            # CI workflow for cloud builds
├── cmd/
│   └── module/
│       └── main.go               # Entry point
├── temp_monitor.go               # Resource implementation
├── go.mod                        # Go module definition
├── go.sum                        # Dependency checksums
├── Makefile                      # Build targets
├── meta.json                     # Module metadata for the registry
├── build.sh                      # Packages the module for upload
└── setup.sh                      # Installs build dependencies
```

{{% /tab %}}
{{< /tabs >}}

## Resource implementation

This is the main file you work in. The generator names it after the model you are implementing. A model implements a Viam API.
In this example, that is `src/models/temp_monitor.py` in Python and
`temp_monitor.go` in Go. The sections below walk through each section of this file.

### Model definition

The model definition identifies your resource in the registry as a triplet
of namespace, module name, and model name. Some examples from built-in Viam
modules: `viam:camera:webcam`, `viam:motor:gpio`, `viam:sensor:ultrasonic`.
In our example, the triplet is `my-org:temp-monitor:temp-monitor`.

{{< tabs >}}
{{% tab name="Python" %}}

```python
class TempMonitor(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "temp-monitor"), "temp-monitor"
    )
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
var Model = resource.NewModel("my-org", "temp-monitor", "temp-monitor")

func init() {
    resource.RegisterService(generic.API, Model, resource.Registration[
        resource.Resource, *Config,
    ]{
        Constructor: newTempMonitor,
    })
}
```

In Go, the `init()` function registers the model with `viam-server` when
the package is imported. The registration binds the model to the generic
service API and points to the constructor function.

{{% /tab %}}
{{< /tabs >}}

### Config and attributes

Config attributes are the fields a user sets when they add the service this model implements to a
machine. Each field maps to a key in the `attributes` block of the JSON
config:

```json
"attributes": {
  "sensor_name": "temp-1",
  "threshold": 40.0
}
```

{{< tabs >}}
{{% tab name="Python" %}}

```python
    sensor_name: str
    threshold: float
    sensor: Sensor
    exceeded: bool
```

In Python, declare config attributes, resolved dependencies, and runtime
state as instance variables on the class. This pattern is the same for any
module you write. Only the specific variables change.

{{% /tab %}}
{{% tab name="Go" %}}

```go
type Config struct {
    SensorName string  `json:"sensor_name"`
    Threshold  float64 `json:"threshold"`
}

type TempMonitor struct {
    resource.Named
    logger   logging.Logger
    cfg      *Config
    sensor   sensor.Sensor
    mu       sync.Mutex
    exceeded bool
    cancelFn func()
}
```

In Go, the `Config` struct defines the attributes. The `json` tags map each
field to its key in the JSON config. The resource struct holds the parsed
config, resolved dependencies, and runtime state. This pattern is the same
for any module you write. Only the specific fields change.

{{% /tab %}}
{{< /tabs >}}

### Validation

The validation method checks that attributes are valid and declares
dependencies on other resources. `viam-server` calls this before creating or
reconfiguring the resource. It returns two lists: required dependencies and
optional dependencies.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "sensor_name" not in fields:
            raise Exception("sensor_name is required")
        return [fields["sensor_name"].string_value], []
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.SensorName == "" {
        return nil, nil, fmt.Errorf("sensor_name is required")
    }
    return []string{cfg.SensorName}, nil, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### Constructor

`viam-server` calls the constructor when it creates your resource. The
constructor receives the config (containing the attributes the user set), a dependencies
map (containing running instances of the resources you declared in your
validation method), and in Go, a context and a logger.

If your resource uses `AlwaysRebuild` (the generated default in Go),
`viam-server` destroys and re-creates the resource on every config change,
calling the constructor again. If you implement a `Reconfigure` method
instead, `viam-server` calls that method in place without re-creating the
resource.

The constructor's job is to:

1. **Parse the config** into typed fields you can use (for example, extract
   `sensor_name` as a string and `threshold` as a float).
2. **Resolve dependencies** by looking up each one by name from the
   dependencies map. Each entry is a ready-to-use resource instance that
   `viam-server` has already started.
3. **Store everything on the struct or instance** so your API methods and
   background tasks can use them.
4. **Start background work** if your module runs continuously (for example,
   a goroutine or async task that polls a sensor on an interval).

To resolve a dependency, you look it up by name from the dependencies map.
In Go, every resource type in the SDK provides a `FromDependencies` helper
that does this and returns a typed interface (for example,
`sensor.FromDependencies` returns a `sensor.Sensor`). In Python, you build
the key with `Sensor.get_resource_name(name)` and index into the
dependencies map directly.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    @classmethod
    async def new(cls, config, dependencies) -> Self:
        monitor = cls(config.name)
        monitor.exceeded = False
        monitor.reconfigure(config, dependencies)
        return monitor

    def reconfigure(self, config, dependencies) -> None:
        fields = config.attributes.fields
        self.sensor_name = fields["sensor_name"].string_value
        self.threshold = (
            fields["threshold"].number_value
            if "threshold" in fields
            else 100.0
        )

        self.sensor = dependencies[
            Sensor.get_resource_name(self.sensor_name)
        ]

        ...
```

In Python, the common pattern is for `new` to call `reconfigure` so that
config-reading and dependency resolution logic lives in one place.

{{% /tab %}}
{{% tab name="Go" %}}

```go
func newTempMonitor(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (resource.Resource, error) {
    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }
    if cfg.Threshold == 0 {
        cfg.Threshold = 100.0
    }

    s, err := sensor.FromDependencies(deps, cfg.SensorName)
    if err != nil {
        return nil, err
    }

    monitorCtx, cancelFn := context.WithCancel(context.Background())
    tm := &TempMonitor{
        Named:    conf.ResourceName().AsNamed(),
        logger:   logger,
        cfg:      cfg,
        sensor:   s,
        cancelFn: cancelFn,
    }
    go tm.monitor(monitorCtx)
    return tm, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### API methods

API methods are how external code interacts with your resource. For a logic
module using the generic service API, the method is `DoCommand`. It accepts
and returns arbitrary key-value maps, so you define your own command
vocabulary.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    async def do_command(self, command, **kwargs):
        if command.get("command") == "status":
            return {
                "exceeded": self.exceeded,
                "threshold": self.threshold,
            }
        return {"error": f"unknown command: {command.get('command')}"}
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (tm *TempMonitor) DoCommand(
    ctx context.Context, cmd map[string]interface{},
) (map[string]interface{}, error) {
    if cmd["command"] == "status" {
        tm.mu.Lock()
        defer tm.mu.Unlock()
        return map[string]interface{}{
            "exceeded":  tm.exceeded,
            "threshold": tm.cfg.Threshold,
        }, nil
    }
    return nil, fmt.Errorf("unknown command: %v", cmd["command"])
}
```

{{% /tab %}}
{{< /tabs >}}

### Close

`viam-server` calls `Close` when it shuts down or removes the resource. Stop
background tasks and release any resources here.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    async def close(self):
        self._stop_event.set()
        if self._monitor_task is not None:
            await self._monitor_task
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (tm *TempMonitor) Close(ctx context.Context) error {
    tm.cancelFn()
    return nil
}
```

{{% /tab %}}
{{< /tabs >}}

For complete working examples, see
[Write a logic module](/build-modules/write-a-logic-module/) and
[Write a driver module](/build-modules/write-a-driver-module/).

## meta.json

Module metadata used by the Viam registry. The generator creates this file
and populates it from your answers to the generator prompts.

```json
{
  "module_id": "my-org:temp-monitor",
  "visibility": "private",
  "url": "https://github.com/my-org/temp-monitor",
  "description": "Logs a warning when a temperature sensor exceeds a threshold.",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "my-org:temp-monitor:temp-monitor"
    }
  ],
  "entrypoint": "run.sh",
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  }
}
```

| Field         | Purpose                                                             |
| ------------- | ------------------------------------------------------------------- |
| `module_id`   | Unique ID in the registry. Format: `namespace:name`.                |
| `visibility`  | Who can install the module: `private`, `public`, `public_unlisted`. |
| `url`         | Link to the source repository. Required for cloud builds.           |
| `description` | Shown in registry search results.                                   |
| `models`      | Resource models the module provides, each with `api` and `model`.   |
| `entrypoint`  | Command that starts the module inside the archive.                  |
| `build.setup` | Script that installs build dependencies (runs once).                |
| `build.build` | Script that compiles and packages the module.                       |
| `build.path`  | Path to the packaged output archive.                                |
| `build.arch`  | Target platforms to build for.                                      |

For the full schema, see
[Module developer reference](/build-modules/module-reference/#metajson-schema).

## Files you rarely edit

### Entry point

The entry point starts the module server and registers your models with
`viam-server`. You only edit this file when you add a second model to the
module.

{{< tabs >}}
{{% tab name="Python" %}}

**`src/main.py`**

```python
import asyncio
from viam.module.module import Module
from models.temp_monitor import TempMonitor  # noqa: F401

if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())
```

`run_from_registry()` discovers all imported resource classes and registers
them. To add another model, import its class here.

{{% /tab %}}
{{% tab name="Go" %}}

**`cmd/module/main.go`**

```go
package main

import (
    tempmonitor "my-org/temp-monitor"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/services/generic"
)

func main() {
    module.ModularMain(
        resource.APIModel{generic.API, tempmonitor.Model},
    )
}
```

`ModularMain` handles socket parsing, signal handling, and graceful shutdown.
The import of the resource package triggers its `init()` function, which
registers the model. To add another model, add another `resource.APIModel`
entry.

{{% /tab %}}
{{< /tabs >}}

### Build and deploy scripts

These scripts handle packaging and deployment. The generator creates working
defaults. You only need to edit them if your module has unusual build
requirements.

| File         | Purpose                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------- |
| `build.sh`   | Compiles (Go) or packages (Python) the module into a `.tar.gz` archive.                        |
| `setup.sh`   | Installs build dependencies. For Python, creates a virtualenv and installs `requirements.txt`. |
| `run.sh`     | (Python only) Entrypoint script that activates the virtualenv and runs `main.py`.              |
| `deploy.yml` | GitHub Actions workflow that triggers cloud builds on tagged releases.                         |
