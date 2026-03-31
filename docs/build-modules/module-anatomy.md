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
what each file does and when you need to edit it.

## Directory structure

{{< tabs >}}
{{% tab name="Python" %}}

```
my-sensor-module/
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI workflow for cloud builds
├── src/
│   ├── main.py               # Entry point
│   └── models/
│       └── my_sensor.py      # Resource implementation
├── build.sh                  # Packages the module for upload
├── meta.json                 # Module metadata for the registry
├── requirements.txt          # Python dependencies
├── run.sh                    # Entrypoint script for viam-server
└── setup.sh                  # Installs dependencies into a virtualenv
```

{{% /tab %}}
{{% tab name="Go" %}}

```
my-sensor-module/
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI workflow for cloud builds
├── cmd/
│   └── module/
│       └── main.go           # Entry point
├── my_sensor_module.go       # Resource implementation
├── go.mod                    # Go module definition
├── go.sum                    # Dependency checksums
├── Makefile                  # Build targets
├── meta.json                 # Module metadata for the registry
├── build.sh                  # Packages the module for upload
└── setup.sh                  # Installs build dependencies
```

{{% /tab %}}
{{< /tabs >}}

## Files you edit

### Resource implementation

This is the main file you work in. It contains your resource class (Python)
or struct (Go) with:

- **Model definition** -- identifies your resource in the registry using a
  triplet of namespace, module name, and model name.
- **Config struct** -- defines the attributes users set when they configure
  your resource. Each field maps to a key in the JSON config.
- **Validation method** -- checks that config attributes are valid and declares
  dependencies on other resources. Called by `viam-server` before creating or
  reconfiguring the resource.
- **Constructor** -- creates an instance of your resource. Receives the
  validated config and a map of resolved dependencies.
- **Reconfigure method** -- updates a running resource when its config changes.
  Many modules call `reconfigure` from the constructor so config-reading logic
  lives in one place.
- **API methods** -- the methods defined by the resource API you are
  implementing. For a sensor, this is `GetReadings`. For a motor, this is
  `SetPower`, `GoFor`, `Stop`, and so on.
- **Close method** -- called when `viam-server` shuts down or removes the
  resource. Clean up connections, stop background tasks, and release resources
  here.

{{< tabs >}}
{{% tab name="Python" %}}

**`src/models/my_sensor.py`**

```python
from typing import ClassVar, Mapping, Sequence, Tuple, Self
from viam.components.sensor import Sensor
from viam.module.easy_resource import EasyResource
from viam.proto.app.robot import ComponentConfig
from viam.resource.base import ResourceBase, ResourceName
from viam.utils import SensorReading

class MySensor(Sensor, EasyResource):
    # Model definition: namespace:module-name:model-name
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "my-sensor-module"), "my-sensor"
    )

    # Config attributes as instance variables
    source_url: str
    poll_interval: float

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        """Validate attributes and declare dependencies.

        Returns (required_deps, optional_deps).
        """
        fields = config.attributes.fields
        if "source_url" not in fields:
            raise Exception("source_url is required")
        return [], []

    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        """Create a new instance."""
        sensor = cls(config.name)
        sensor.reconfigure(config, dependencies)
        return sensor

    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]) -> None:
        """Update config and dependencies."""
        fields = config.attributes.fields
        self.source_url = fields["source_url"].string_value
        self.poll_interval = (
            fields["poll_interval"].number_value
            if "poll_interval" in fields
            else 10.0
        )

    async def get_readings(self, **kwargs) -> Mapping[str, SensorReading]:
        """Return sensor readings."""
        # Your implementation here
        ...

    async def close(self):
        """Clean up resources."""
        ...
```

{{% /tab %}}
{{% tab name="Go" %}}

**`my_sensor_module.go`**

```go
package mysensormodule

import (
    "context"
    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/resource"
)

// Model definition: namespace:module-name:model-name
var Model = resource.NewModel("my-org", "my-sensor-module", "my-sensor")

func init() {
    resource.RegisterComponent(sensor.API, Model, resource.Registration[
        sensor.Sensor, *Config,
    ]{
        Constructor: newMySensor,
    })
}

// Config defines the attributes users set in their JSON config.
type Config struct {
    SourceURL    string  `json:"source_url"`
    PollInterval float64 `json:"poll_interval"`
}

// Validate checks config and declares dependencies.
// Returns (required_deps, optional_deps, error).
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.SourceURL == "" {
        return nil, nil, fmt.Errorf("source_url is required")
    }
    return nil, nil, nil
}

// MySensor implements the sensor API.
type MySensor struct {
    resource.Named
    resource.AlwaysRebuild
    logger    logging.Logger
    sourceURL string
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
    return &MySensor{
        Named:     conf.ResourceName().AsNamed(),
        logger:    logger,
        sourceURL: cfg.SourceURL,
    }, nil
}

func (s *MySensor) Readings(
    ctx context.Context, extra map[string]interface{},
) (map[string]interface{}, error) {
    // Your implementation here
    return nil, nil
}

func (s *MySensor) Close(ctx context.Context) error {
    // Clean up resources
    return nil
}
```

{{% /tab %}}
{{< /tabs >}}

### meta.json

Module metadata used by the Viam registry. The generator creates this file
and populates it from your answers to the generator prompts.

```json
{
  "module_id": "my-org:my-sensor-module",
  "visibility": "private",
  "url": "https://github.com/my-org/my-sensor-module",
  "description": "A custom sensor module.",
  "models": [
    {
      "api": "rdk:component:sensor",
      "model": "my-org:my-sensor-module:my-sensor"
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

| Field          | Purpose                                                          |
| -------------- | ---------------------------------------------------------------- |
| `module_id`    | Unique ID in the registry. Format: `namespace:name`.             |
| `visibility`   | Who can install the module: `private`, `public`, `public_unlisted`. |
| `url`          | Link to the source repository. Required for cloud builds.        |
| `description`  | Shown in registry search results.                                |
| `models`       | Resource models the module provides, each with `api` and `model`. |
| `entrypoint`   | Command that starts the module inside the archive.               |
| `build.setup`  | Script that installs build dependencies (runs once).             |
| `build.build`  | Script that compiles and packages the module.                    |
| `build.path`   | Path to the packaged output archive.                             |
| `build.arch`   | Target platforms to build for.                                   |

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
from models.my_sensor import MySensor  # noqa: F401

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
    mysensormodule "my-org/my-sensor-module"
    "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
)

func main() {
    module.ModularMain(
        resource.APIModel{sensor.API, mysensormodule.Model},
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

| File         | Purpose                                                   |
| ------------ | --------------------------------------------------------- |
| `build.sh`   | Compiles (Go) or packages (Python) the module into a `.tar.gz` archive. |
| `setup.sh`   | Installs build dependencies. For Python, creates a virtualenv and installs `requirements.txt`. |
| `run.sh`     | (Python only) Entrypoint script that activates the virtualenv and runs `main.py`. |
| `deploy.yml` | GitHub Actions workflow that triggers cloud builds on tagged releases. |
