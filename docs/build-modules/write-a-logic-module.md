---
linkTitle: "Write a logic module"
title: "Write a logic module"
weight: 25
layout: "docs"
type: "docs"
description: "Build a module that monitors sensors, coordinates components, or runs automation logic."
date: "2025-03-06"
aliases:
  - /development/write-a-logic-module/
  - /manage/software/control-logic
  - /operate/modules/control-logic/
  - /operate/modules/write-a-logic-module/
---

Your machine has resources -- sensors, motors, cameras -- that work individually.
A logic module makes them work together. It runs as a service alongside
`viam-server`, declares dependencies on the resources it needs, and implements
whatever control, monitoring, or coordination logic your application requires.

Use a logic module when you need your machine to make decisions based on what
it senses: trigger actions when readings cross a threshold, coordinate multiple
components to accomplish a task, aggregate data from several sources, or run
any continuous process that reads from some resources and acts on others.

{{< alert title="Driver modules and logic modules" color="tip" >}}
A [driver module](/build-modules/write-a-driver-module/) wraps hardware -- it implements
a component API like sensor or motor so that `viam-server` can talk to a
specific piece of hardware.

A logic module (this page) orchestrates existing resources -- it reads from
sensors, commands motors, and makes decisions. It typically implements a service
API.

Both are modules. The difference is what they do, not how they're built. The
lifecycle, config validation, dependency, and deployment patterns are the same.
{{< /alert >}}

The generic service API is a minimal service interface that exposes `DoCommand` and `GetStatus`. If you are writing custom control logic for a robotics application, this is the API you want. Pick a more specific typed API like vision or motion only when your module's work fits one.

For background on module lifecycle, dependencies, and background tasks, see the [overview](/build-modules/overview/).

## Steps {#program-control-logic-in-module}

When writing a logic module, follow the steps outlined below. To illustrate
each step we'll use a temperature alert monitor as a worked example. It watches
one or more sensors, compares their readings against configurable thresholds,
and maintains a list of active alerts that your application code can query.

### 1. Generate a generic service module

Before you run the generator, [install the Viam CLI](/cli/overview/#install) and log in with `viam login`.

The generator prompts for your organization's public namespace. If you have not set one yet, click the organization dropdown at the upper right of the Viam app, select **Settings**, then **Set a public namespace**. You can also enter your Org ID at the prompt instead.

Run the Viam CLI generator:

```bash
viam module generate
```

The generator creates a new directory named after your module (for example, `alert-monitor`) in your current working directory. `cd` into that directory for the rest of the steps.

When run without flags, the generator prompts for each value below. If you pass these as `--name`, `--language`, `--visibility`, `--public-namespace`, `--resource-subtype`, `--model-name`, and `--register` flags instead, use the flag forms noted in the table (where different from the interactive labels).

| Prompt                                       | What to enter                               | Why                                                                                                                                                                                                      |
| -------------------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Set a module name:                           | `alert-monitor`                             | A short, descriptive name                                                                                                                                                                                |
| Specify the language for the module:         | `python` or `go`                            | Your implementation language                                                                                                                                                                             |
| Visibility:                                  | `private`                                   | `private`: visible only within your org. `public`: visible to everyone. `public_unlisted`: usable by anyone who knows the module ID, but hidden from the registry page. You can change visibility later. |
| Namespace/Organization ID                    | Your organization namespace                 | Scopes the module to your org                                                                                                                                                                            |
| Select a resource to be added to the module: | `Generic Service` (flag: `generic-service`) | Flexible service API                                                                                                                                                                                     |
| Set a model name of the resource:            | `temp-alert`                                | The model name for your service                                                                                                                                                                          |
| Register module                              | `yes`                                       | Registers the module with Viam                                                                                                                                                                           |

The generator creates a complete project. The key files you will edit:

{{< tabs >}}
{{% tab name="Python" %}}

| File                           | Purpose                                      |
| ------------------------------ | -------------------------------------------- |
| `src/main.py`                  | Entry point -- starts the module server      |
| `src/models/temp_alert.py`     | Service class skeleton -- you will edit this |
| `requirements.txt`             | Python dependencies                          |
| `meta.json`                    | Module metadata for the registry             |
| `setup.sh`                     | Installs dependencies into a virtualenv      |
| `build.sh`                     | Packages the module for upload               |
| `.github/workflows/deploy.yml` | CI workflow for cloud builds                 |

{{% /tab %}}
{{% tab name="Go" %}}

| File                           | Purpose                                               |
| ------------------------------ | ----------------------------------------------------- |
| `cmd/module/main.go`           | Entry point -- starts the module server               |
| `module.go`                    | Service implementation skeleton -- you will edit this |
| `go.mod`                       | Go module definition                                  |
| `Makefile`                     | Build targets                                         |
| `meta.json`                    | Module metadata for the registry                      |
| `.github/workflows/deploy.yml` | CI workflow for cloud builds                          |

{{% /tab %}}
{{< /tabs >}}

### 2. Define the config

Open the generated resource file. Define config attributes for the sensors to
monitor and the alert thresholds. For this example, we use:

- `sensor_names` — names of the sensors to poll. Required.
- `max_temp` — temperature threshold above which to create an alert. Required; units match whatever your sensor reports.
- `poll_interval_secs` — seconds between polls. Optional; defaults to 10.

{{< tabs >}}
{{% tab name="Python" %}}

In `src/models/temp_alert.py`, find the generated `class TempAlert(Generic, EasyResource):` and add the following instance-variable declarations inside the class, after the existing `MODEL` declaration:

```python
    sensor_names: list[str]
    max_temp: float
    poll_interval_secs: float
    alerts: list[dict]
    _monitor_task: Optional[asyncio.Task]
    _stop_event: asyncio.Event
```

{{% /tab %}}
{{% tab name="Go" %}}

In the generated `.go` file, add fields to the `Config` struct. Each field
needs a `json` tag matching the attribute name users set in their config JSON.

Then update the `Validate` method. It returns three values: a list of required
dependency names, a list of optional dependency names, and an error.

```go
type Config struct {
    SensorNames  []string `json:"sensor_names"`
    MaxTemp      float64  `json:"max_temp"`
    PollInterval float64  `json:"poll_interval_secs"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if len(cfg.SensorNames) == 0 {
        return nil, nil, fmt.Errorf("sensor_names is required")
    }
    if cfg.MaxTemp == 0 {
        return nil, nil, fmt.Errorf("max_temp is required")
    }
    // 1. Declare: return all sensor names as required dependencies
    return cfg.SensorNames, nil, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 3. Implement the constructor

The constructor receives the validated config and a `dependencies` map
containing the resources you declared in the validation method. Look up each
dependency by name, store it on your struct/instance, and start the background
monitoring loop.

{{< tabs >}}
{{% tab name="Python" %}}

Update `validate_config` and `new`:

```python
    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "sensor_names" not in fields:
            raise Exception("sensor_names is required")
        if "max_temp" not in fields:
            raise Exception("max_temp is required")
        sensor_names = [
            v.string_value
            for v in fields["sensor_names"].list_value.values
        ]
        # 1. Declare: return sensor names as required dependencies
        return sensor_names, []

    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        instance = super().new(config, dependencies)
        instance.alerts = []

        fields = config.attributes.fields
        instance.sensor_names = [
            v.string_value
            for v in fields["sensor_names"].list_value.values
        ]
        instance.max_temp = fields["max_temp"].number_value
        instance.poll_interval_secs = (
            fields["poll_interval_secs"].number_value
            if "poll_interval_secs" in fields
            else 10.0
        )

        # 2. Resolve: find each sensor in the dependencies map
        instance.sensors = {}
        for name, dep in dependencies.items():
            if name.name in instance.sensor_names:
                instance.sensors[name.name] = dep

        # Start the monitor loop
        instance._stop_event = asyncio.Event()
        instance._monitor_task = asyncio.create_task(instance._monitor_loop())
        return instance
```

The generator also emits `do_command` and `get_status` method stubs that raise `NotImplementedError`. You'll replace `do_command` in Step 5; leave `get_status` alone unless your service has a meaningful status to report.

{{% /tab %}}
{{% tab name="Go" %}}

The generator emits a compound struct type (`alertMonitorTempAlert`) with `resource.AlwaysRebuild` embedded and two constructor functions; a private `newAlertMonitorTempAlert` that unpacks the raw config and delegates to a public `NewTempAlert` that takes a typed `*Config`. Keep that layout. `resource.NativeConfig` converts the raw config into your typed struct. `sensor.FromProvider` looks up a sensor dependency by name from the dependencies map.

The generator also emits `Name()`, `Close()`, `DoCommand()`, and `Status()` methods on the struct. Leave `Name()` and `Status()` as generated. You'll replace `DoCommand()` in Step 5 and `Close()` in Step 6.

```go
type alertMonitorTempAlert struct {
    resource.AlwaysRebuild

    name resource.Name

    logger  logging.Logger
    cfg     *Config
    sensors map[string]sensor.Sensor

    mu     sync.Mutex
    alerts []Alert

    cancelCtx  context.Context
    cancelFunc func()
}

type Alert struct {
    Sensor    string  `json:"sensor"`
    Value     float64 `json:"value"`
    Threshold float64 `json:"threshold"`
    Time      string  `json:"time"`
}

func newAlertMonitorTempAlert(ctx context.Context, deps resource.Dependencies, rawConf resource.Config, logger logging.Logger) (resource.Resource, error) {
    conf, err := resource.NativeConfig[*Config](rawConf)
    if err != nil {
        return nil, err
    }
    return NewTempAlert(ctx, deps, rawConf.ResourceName(), conf, logger)
}

func NewTempAlert(ctx context.Context, deps resource.Dependencies, name resource.Name, conf *Config, logger logging.Logger) (resource.Resource, error) {
    // 2. Resolve: find each sensor in the dependencies map
    sensors := make(map[string]sensor.Sensor)
    for _, sensorName := range conf.SensorNames {
        s, err := sensor.FromProvider(deps, sensorName)
        if err != nil {
            return nil, fmt.Errorf("sensor %q not found: %w", sensorName, err)
        }
        sensors[sensorName] = s
    }

    cancelCtx, cancelFunc := context.WithCancel(context.Background())
    svc := &alertMonitorTempAlert{
        name:       name,
        logger:     logger,
        cfg:        conf,
        sensors:    sensors,
        alerts:     []Alert{},
        cancelCtx:  cancelCtx,
        cancelFunc: cancelFunc,
    }

    // Start background monitor loop
    go svc.monitorLoop(cancelCtx)

    return svc, nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 4. Implement the background loop

The monitor loop polls sensors at a fixed interval and checks readings against
thresholds. When a reading exceeds the threshold, it creates an alert.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    async def _monitor_loop(self):
        while not self._stop_event.is_set():
            for name, s in self.sensors.items():
                try:
                    # 3. Use: call methods on dependencies
                    readings = await s.get_readings()
                    temp = readings.get("temperature")
                    if temp is not None and temp > self.max_temp:
                        alert = {
                            "sensor": name,
                            "value": temp,
                            "threshold": self.max_temp,
                            "time": datetime.now().isoformat(),
                        }
                        self.alerts.append(alert)
                        self.logger.warning(
                            "Alert: %s reported %.1f (threshold: %.1f)",
                            name, temp, self.max_temp,
                        )
                except Exception as e:
                    self.logger.error("Failed to read %s: %s", name, e)

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self.poll_interval_secs,
                )
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Continue polling
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (s *alertMonitorTempAlert) monitorLoop(ctx context.Context) {
    interval := time.Duration(s.cfg.PollInterval) * time.Second
    if interval == 0 {
        interval = 10 * time.Second
    }

    ticker := time.NewTicker(interval)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            s.checkSensors(ctx)
        }
    }
}

func (s *alertMonitorTempAlert) checkSensors(ctx context.Context) {
    s.mu.Lock()
    defer s.mu.Unlock()

    for name, sens := range s.sensors {
        // 3. Use: call methods on dependencies
        readings, err := sens.Readings(ctx, nil)
        if err != nil {
            s.logger.CErrorw(ctx, "failed to read sensor", "sensor", name, "error", err)
            continue
        }
        temp, ok := readings["temperature"].(float64)
        if !ok {
            continue
        }
        if temp > s.cfg.MaxTemp {
            alert := Alert{
                Sensor:    name,
                Value:     temp,
                Threshold: s.cfg.MaxTemp,
                Time:      time.Now().Format(time.RFC3339),
            }
            s.alerts = append(s.alerts, alert)
            s.logger.CWarnw(ctx, "alert triggered",
                "sensor", name, "value", temp, "threshold", s.cfg.MaxTemp)
        }
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 5. Implement DoCommand

`DoCommand` is the interface your application code uses to interact with the
service. Define a command vocabulary that makes sense for your module.

The generic service API also provides `GetStatus`. The generator does not implement it; calling it on an unmodified generated service raises `NotImplementedError`. Override it if your service has a meaningful status to report.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        cmd = command.get("command", "")

        if cmd == "get_alerts":
            # Snapshot so the list isn't mutated during serialization
            return {"alerts": list(self.alerts)}

        if cmd == "get_alert_count":
            return {"count": len(self.alerts)}

        if cmd == "acknowledge":
            self.alerts.clear()
            return {"status": "ok"}

        if cmd == "set_threshold":
            self.max_temp = command["max_temp"]
            return {"status": "ok", "max_temp": self.max_temp}

        raise Exception(f"Unknown command: {cmd}")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (s *alertMonitorTempAlert) DoCommand(
    ctx context.Context,
    cmd map[string]interface{},
) (map[string]interface{}, error) {
    command, _ := cmd["command"].(string)

    switch command {
    case "get_alerts":
        s.mu.Lock()
        defer s.mu.Unlock()
        // Convert alerts to interface slice for serialization
        alertList := make([]interface{}, len(s.alerts))
        for i, a := range s.alerts {
            alertList[i] = map[string]interface{}{
                "sensor":    a.Sensor,
                "value":     a.Value,
                "threshold": a.Threshold,
                "time":      a.Time,
            }
        }
        return map[string]interface{}{"alerts": alertList}, nil

    case "get_alert_count":
        s.mu.Lock()
        defer s.mu.Unlock()
        return map[string]interface{}{"count": len(s.alerts)}, nil

    case "acknowledge":
        s.mu.Lock()
        defer s.mu.Unlock()
        s.alerts = s.alerts[:0]
        return map[string]interface{}{"status": "ok"}, nil

    case "set_threshold":
        newMax, ok := cmd["max_temp"].(float64)
        if !ok {
            return nil, fmt.Errorf("max_temp must be a number")
        }
        s.mu.Lock()
        s.cfg.MaxTemp = newMax
        s.mu.Unlock()
        return map[string]interface{}{"status": "ok", "max_temp": newMax}, nil

    default:
        return nil, fmt.Errorf("unknown command: %s", command)
    }
}
```

{{% /tab %}}
{{< /tabs >}}

### 6. Handle shutdown

When `viam-server` stops the module or reconfigures it, your background loop
must stop cleanly. Without this, goroutines or async tasks leak.

{{< tabs >}}
{{% tab name="Python" %}}

```python
    async def close(self):
        self._stop_event.set()
        if self._monitor_task is not None:
            await self._monitor_task
            self._monitor_task = None
        self.logger.info("TempAlert monitor stopped")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (s *alertMonitorTempAlert) Close(ctx context.Context) error {
    s.cancelFunc()
    s.logger.CInfof(ctx, "TempAlert monitor stopped")
    return nil
}
```

On a config change, `viam-server` calls `Close` on the old instance and then
invokes your constructor again with the new config. `Close` stops the old
loop; the fresh constructor starts a new one.

{{% /tab %}}
{{< /tabs >}}

{{< expand "View the complete resource file" >}}

For reference, here is the complete resource file after all the changes above. `my-org` in these samples stands in for the namespace you entered when running the generator.

{{< tabs >}}
{{% tab name="Python" %}}

`src/models/temp_alert.py`:

```python
import asyncio
from datetime import datetime
from typing import ClassVar, Mapping, Optional, Sequence, Tuple

from typing_extensions import Self
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.services.generic import *
from viam.utils import ValueTypes


class TempAlert(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "alert-monitor"), "temp-alert"
    )

    sensor_names: list[str]
    max_temp: float
    poll_interval_secs: float
    alerts: list[dict]
    _monitor_task: Optional[asyncio.Task]
    _stop_event: asyncio.Event

    @classmethod
    def validate_config(
        cls, config: ComponentConfig
    ) -> Tuple[Sequence[str], Sequence[str]]:
        fields = config.attributes.fields
        if "sensor_names" not in fields:
            raise Exception("sensor_names is required")
        if "max_temp" not in fields:
            raise Exception("max_temp is required")
        sensor_names = [
            v.string_value
            for v in fields["sensor_names"].list_value.values
        ]
        return sensor_names, []

    @classmethod
    def new(cls, config: ComponentConfig,
            dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        instance = super().new(config, dependencies)
        instance.alerts = []

        fields = config.attributes.fields
        instance.sensor_names = [
            v.string_value
            for v in fields["sensor_names"].list_value.values
        ]
        instance.max_temp = fields["max_temp"].number_value
        instance.poll_interval_secs = (
            fields["poll_interval_secs"].number_value
            if "poll_interval_secs" in fields
            else 10.0
        )

        instance.sensors = {}
        for name, dep in dependencies.items():
            if name.name in instance.sensor_names:
                instance.sensors[name.name] = dep

        instance._stop_event = asyncio.Event()
        instance._monitor_task = asyncio.create_task(instance._monitor_loop())
        return instance

    async def _monitor_loop(self):
        while not self._stop_event.is_set():
            for name, s in self.sensors.items():
                try:
                    readings = await s.get_readings()
                    temp = readings.get("temperature")
                    if temp is not None and temp > self.max_temp:
                        alert = {
                            "sensor": name,
                            "value": temp,
                            "threshold": self.max_temp,
                            "time": datetime.now().isoformat(),
                        }
                        self.alerts.append(alert)
                        self.logger.warning(
                            "Alert: %s reported %.1f (threshold: %.1f)",
                            name, temp, self.max_temp,
                        )
                except Exception as e:
                    self.logger.error("Failed to read %s: %s", name, e)

            try:
                await asyncio.wait_for(
                    self._stop_event.wait(),
                    timeout=self.poll_interval_secs,
                )
                break
            except asyncio.TimeoutError:
                pass

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[str, ValueTypes]:
        cmd = command.get("command", "")

        if cmd == "get_alerts":
            return {"alerts": list(self.alerts)}

        if cmd == "get_alert_count":
            return {"count": len(self.alerts)}

        if cmd == "acknowledge":
            self.alerts.clear()
            return {"status": "ok"}

        if cmd == "set_threshold":
            self.max_temp = command["max_temp"]
            return {"status": "ok", "max_temp": self.max_temp}

        raise Exception(f"Unknown command: {cmd}")

    async def get_status(
        self, *, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, ValueTypes]:
        self.logger.error("`get_status` is not implemented")
        raise NotImplementedError()

    async def close(self):
        self._stop_event.set()
        if self._monitor_task is not None:
            await self._monitor_task
            self._monitor_task = None
        self.logger.info("TempAlert monitor stopped")
```

{{% /tab %}}
{{% tab name="Go" %}}

`module.go`:

```go
package alertmonitor

import (
    "context"
    "errors"
    "fmt"
    "sync"
    "time"

    sensor "go.viam.com/rdk/components/sensor"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/resource"
    generic "go.viam.com/rdk/services/generic"
)

var (
    TempAlert        = resource.NewModel("my-org", "alert-monitor", "temp-alert")
    errUnimplemented = errors.New("unimplemented")
)

func init() {
    resource.RegisterService(generic.API, TempAlert,
        resource.Registration[resource.Resource, *Config]{
            Constructor: newAlertMonitorTempAlert,
        },
    )
}

type Config struct {
    SensorNames      []string `json:"sensor_names"`
    MaxTemp          float64  `json:"max_temp"`
    PollIntervalSecs float64  `json:"poll_interval_secs"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if len(cfg.SensorNames) == 0 {
        return nil, nil, fmt.Errorf("sensor_names is required")
    }
    if cfg.MaxTemp == 0 {
        return nil, nil, fmt.Errorf("max_temp is required")
    }
    return cfg.SensorNames, nil, nil
}

type Alert struct {
    Sensor    string  `json:"sensor"`
    Value     float64 `json:"value"`
    Threshold float64 `json:"threshold"`
    Time      string  `json:"time"`
}

type alertMonitorTempAlert struct {
    resource.AlwaysRebuild

    name resource.Name

    logger  logging.Logger
    cfg     *Config
    sensors map[string]sensor.Sensor

    mu     sync.Mutex
    alerts []Alert

    cancelCtx  context.Context
    cancelFunc func()
}

func newAlertMonitorTempAlert(ctx context.Context, deps resource.Dependencies, rawConf resource.Config, logger logging.Logger) (resource.Resource, error) {
    conf, err := resource.NativeConfig[*Config](rawConf)
    if err != nil {
        return nil, err
    }
    return NewTempAlert(ctx, deps, rawConf.ResourceName(), conf, logger)
}

func NewTempAlert(ctx context.Context, deps resource.Dependencies, name resource.Name, conf *Config, logger logging.Logger) (resource.Resource, error) {
    sensors := make(map[string]sensor.Sensor)
    for _, sensorName := range conf.SensorNames {
        s, err := sensor.FromProvider(deps, sensorName)
        if err != nil {
            return nil, fmt.Errorf("sensor %q not found: %w", sensorName, err)
        }
        sensors[sensorName] = s
    }

    cancelCtx, cancelFunc := context.WithCancel(context.Background())
    svc := &alertMonitorTempAlert{
        name:       name,
        logger:     logger,
        cfg:        conf,
        sensors:    sensors,
        alerts:     []Alert{},
        cancelCtx:  cancelCtx,
        cancelFunc: cancelFunc,
    }

    go svc.monitorLoop(cancelCtx)

    return svc, nil
}

func (s *alertMonitorTempAlert) Name() resource.Name {
    return s.name
}

func (s *alertMonitorTempAlert) monitorLoop(ctx context.Context) {
    interval := time.Duration(s.cfg.PollIntervalSecs) * time.Second
    if interval == 0 {
        interval = 10 * time.Second
    }

    ticker := time.NewTicker(interval)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return
        case <-ticker.C:
            s.checkSensors(ctx)
        }
    }
}

func (s *alertMonitorTempAlert) checkSensors(ctx context.Context) {
    s.mu.Lock()
    defer s.mu.Unlock()

    for name, sens := range s.sensors {
        readings, err := sens.Readings(ctx, nil)
        if err != nil {
            s.logger.CErrorw(ctx, "failed to read sensor", "sensor", name, "error", err)
            continue
        }
        temp, ok := readings["temperature"].(float64)
        if !ok {
            continue
        }
        if temp > s.cfg.MaxTemp {
            alert := Alert{
                Sensor:    name,
                Value:     temp,
                Threshold: s.cfg.MaxTemp,
                Time:      time.Now().Format(time.RFC3339),
            }
            s.alerts = append(s.alerts, alert)
            s.logger.CWarnw(ctx, "alert triggered",
                "sensor", name, "value", temp, "threshold", s.cfg.MaxTemp)
        }
    }
}

func (s *alertMonitorTempAlert) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    command, _ := cmd["command"].(string)

    switch command {
    case "get_alerts":
        s.mu.Lock()
        defer s.mu.Unlock()
        alertList := make([]interface{}, len(s.alerts))
        for i, a := range s.alerts {
            alertList[i] = map[string]interface{}{
                "sensor":    a.Sensor,
                "value":     a.Value,
                "threshold": a.Threshold,
                "time":      a.Time,
            }
        }
        return map[string]interface{}{"alerts": alertList}, nil

    case "get_alert_count":
        s.mu.Lock()
        defer s.mu.Unlock()
        return map[string]interface{}{"count": len(s.alerts)}, nil

    case "acknowledge":
        s.mu.Lock()
        defer s.mu.Unlock()
        s.alerts = s.alerts[:0]
        return map[string]interface{}{"status": "ok"}, nil

    case "set_threshold":
        newMax, ok := cmd["max_temp"].(float64)
        if !ok {
            return nil, fmt.Errorf("max_temp must be a number")
        }
        s.mu.Lock()
        s.cfg.MaxTemp = newMax
        s.mu.Unlock()
        return map[string]interface{}{"status": "ok", "max_temp": newMax}, nil

    default:
        return nil, fmt.Errorf("unknown command: %s", command)
    }
}

func (s *alertMonitorTempAlert) Status(ctx context.Context) (map[string]interface{}, error) {
    return nil, fmt.Errorf("not implemented")
}

func (s *alertMonitorTempAlert) Close(ctx context.Context) error {
    s.cancelFunc()
    s.logger.CInfof(ctx, "TempAlert monitor stopped")
    return nil
}
```

{{% /tab %}}
{{< /tabs >}}

{{< /expand >}}

### 7. Review the entry point

The generator also creates the entry point file that `viam-server` launches. You typically do not need to modify it.

{{< tabs >}}
{{% tab name="Python" %}}

`src/main.py`:

```python
import asyncio
from viam.module.module import Module
from models.temp_alert import TempAlert as TempAlertModel


if __name__ == '__main__':
    asyncio.run(Module.run_from_registry())
```

`run_from_registry()` automatically discovers all imported resource classes and registers them with `viam-server`. If you add more models to your module, import them here.

{{% /tab %}}
{{% tab name="Go" %}}

`cmd/module/main.go`:

```go
package main

import (
    "alertmonitor"

    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
    generic "go.viam.com/rdk/services/generic"
)

func main() {
    // ModularMain can take multiple APIModel arguments, if your module implements multiple models.
    module.ModularMain(resource.APIModel{generic.API, alertmonitor.TempAlert})
}
```

`ModularMain` handles socket parsing, signal handling, and graceful shutdown. The import of the resource package triggers its `init()` function, which calls `resource.RegisterService` to register the model. If you add more models, add more `resource.APIModel` entries to the `ModularMain` call.

{{% /tab %}}
{{< /tabs >}}

### 8. Test locally

**Deploy with hot reloading:**

Ensure you have at least one sensor configured on your machine (this is the resource your logic module will monitor).

Use the CLI to build and deploy your module. Replace `<machine-part-id>` with your machine's part ID. At the top of your machine's page, click the **Live** / **Offline** status dropdown, then click **Part ID** to copy it.

```bash
# Build in the cloud and deploy to the machine
viam module reload --part-id <machine-part-id>
```

If your development machine and target machine share the same architecture, you can build locally instead:

```bash
# Build locally and transfer to the machine
viam module reload-local --part-id <machine-part-id>
```

Use `reload` (cloud build) when developing on a different architecture than your target. Use `reload-local` when architectures match for faster iteration.

After deploying, open the machine's **CONFIGURE** tab and set your new service's attributes. Replace `"my-temp-sensor"` with the name of a sensor configured on your machine. Adjust `max_temp` and `poll_interval_secs` for your use case.

```json
{
  "sensor_names": ["my-temp-sensor"],
  "max_temp": 30.0,
  "poll_interval_secs": 5
}
```

Click **Save**.

**Test with DoCommand:**

On the **CONFIGURE** tab, expand your service's **Test** section and then expand **DoCommand**. Send a command:

```json
{ "command": "get_alerts" }
```

You should see a response shaped like:

```json
{
  "alerts": [
    {
      "sensor": "my-temp-sensor",
      "value": 32.5,
      "threshold": 30.0,
      "time": "2026-04-24T14:23:17Z"
    }
  ]
}
```

A Python implementation returns the same shape, but `time` matches `datetime.now().isoformat()` output:

```json
{
  "alerts": [
    {
      "sensor": "my-temp-sensor",
      "value": 32.5,
      "threshold": 30.0,
      "time": "2026-04-24T14:23:17.123456"
    }
  ]
}
```

If no alerts have triggered yet, the `alerts` array is empty.

**Get a ready-to-run code sample:**

The **CONNECT** tab on your machine's page in the Viam app provides generated
code samples in Python and Go that connect to your machine and access all
configured resources. Use this as a starting point for application code that
sends `DoCommand` requests to your service.

**Rebuild and redeploy during development:**

Each time you make changes, run `viam module reload` (or `reload-local`) again. Use `viam module restart` to restart without rebuilding (for example, after editing Python source).

**Test the alert flow:**

1. Verify your sensor is returning temperature readings on the TEST card.
2. Set `max_temp` to a value below the current temperature so alerts trigger.
3. Wait for one poll interval, then send `{"command": "get_alerts"}`.
4. You should see alerts in the response.
5. Send `{"command": "acknowledge"}` to clear them.

### 9. Schedule logic with jobs (optional)

Instead of running a continuous background loop, you can use
{{< glossary_tooltip term_id="job" text="jobs" >}} to have `viam-server` call
your service's `DoCommand` method on a schedule. This is useful for periodic
tasks that don't need sub-second polling.

1. In the [Viam app](https://app.viam.com), open your machine's **CONFIGURE** tab. Click the **+** icon to add a resource and select **Job**.
2. Name the job and click **Create**.
3. Set the **Schedule** to one of:
   - **Interval** -- a Go duration string like `5s`, `1m`, or `2h30m`.
   - **Cron** -- a 5- or 6-part cron expression (for example, `0 */5 * * *`).
4. Select your service resource by name.
5. Select the `DoCommand` **Method** and specify the **Command**, for example:

   ```json
   { "command": "get_alerts" }
   ```

6. Optionally, adjust the **Log threshold** to raise or lower the log verbosity for this job's invocations compared to the module's default.
7. Click **Save**.

`viam-server` calls `DoCommand` with the specified arguments on the configured
schedule. You can view job history (last 10 successes and failures) in the
machine's configuration.

Jobs also support calling other gRPC methods on resources (such as
`GetReadings` on a sensor), but only `DoCommand` accepts command arguments.

## Try It

1. Generate a generic service module using `viam module generate`.
2. Define config attributes for monitored sensors and thresholds.
3. Implement the constructor to resolve sensor dependencies and start the
   monitor loop.
4. Implement `DoCommand` with `get_alerts`, `acknowledge`, and `set_threshold`
   commands.
5. Configure the module on your machine with a real sensor.
6. Lower the threshold below the current temperature and verify alerts appear.

## Troubleshooting

{{< expand "Background loop not running" >}}

- Check the **LOGS** tab for errors from the monitor loop. A failing sensor
  read can cause the loop to exit silently.
- In Python, ensure you are creating an `asyncio.Task` (not just calling the
  async function without `await` or `create_task`).
- In Go, ensure the goroutine context is not prematurely canceled. Use
  `context.Background()` for the loop context, not the request context.

{{< /expand >}}

{{< expand "DoCommand returning unexpected results" >}}

- Verify the `command` field in your request matches the command names in your
  implementation exactly (case-sensitive).
- Check that value types match. JSON numbers are `float64` in Go and `float`
  in Python. If you send `"max_temp": 30`, Go receives it as `float64(30)`.
- Add logging inside `DoCommand` to see the raw command map.

{{< /expand >}}

{{< expand "Sensor dependency not available" >}}

- Confirm the sensor names in `sensor_names` match the names of sensors
  configured on the machine exactly.
- Verify the sensors are configured and working before the logic module starts.
  Check the **CONTROL** tab to confirm each sensor returns readings.
- If a sensor is added after the logic module is already running, reconfigure
  the logic module (re-save its config) so `viam-server` re-resolves
  dependencies.

{{< /expand >}}

{{< expand "Alerts not appearing" >}}

- Check that your sensor's readings map includes a `"temperature"` key. The
  monitor loop checks for this specific key.
- Verify `max_temp` is set below the actual temperature so alerts trigger.
- Check the **LOGS** tab for warning messages from the monitor loop.

{{< /expand >}}

## What's Next

- [Write a Driver Module](/build-modules/write-a-driver-module/) -- write a module
  that wraps custom hardware.
- [Deploy a Module](/build-modules/deploy-a-module/) -- package and upload your
  module to the Viam registry.
- [Module Reference](/build-modules/module-reference/) -- complete reference
  for meta.json, CLI commands, environment variables, and resource interfaces.
