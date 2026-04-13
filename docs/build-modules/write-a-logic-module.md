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

For background on the generic service API, module lifecycle, dependencies, and
background tasks, see the [overview](/build-modules/overview/).

## Steps

When writing a logic module, follow the steps outlined below. To illustrate
each step we'll use a temperature alert monitor as a worked example. It watches
one or more sensors, compares their readings against configurable thresholds,
and maintains a list of active alerts that your application code can query.

### 1. Generate a generic service module

```bash
viam module generate
```

| Prompt           | What to enter               | Why                              |
| ---------------- | --------------------------- | -------------------------------- |
| Module name      | `alert-monitor`             | A short, descriptive name        |
| Language         | `python` or `go`            | Your implementation language     |
| Visibility       | `private`                   | Keep it private while developing |
| Namespace        | Your organization namespace | Scopes the module to your org    |
| Resource subtype | `generic` (under services)  | Flexible service API             |
| Model name       | `temp-alert`                | The model name for your service  |
| Register         | `yes`                       | Registers the module with Viam   |

The generator creates a complete project. The key files you will edit:

{{< tabs >}}
{{% tab name="Python" %}}

| File                       | Purpose                                                     |
| -------------------------- | ----------------------------------------------------------- |
| `src/models/temp_alert.py` | Service class skeleton -- you will edit this                |
| `src/main.py`              | Entry point -- starts the module server (no changes needed) |
| `meta.json`                | Module metadata for the registry                            |

{{% /tab %}}
{{% tab name="Go" %}}

| File                 | Purpose                                                     |
| -------------------- | ----------------------------------------------------------- |
| `alert_monitor.go`   | Service implementation skeleton -- you will edit this       |
| `cmd/module/main.go` | Entry point -- starts the module server (no changes needed) |
| `meta.json`          | Module metadata for the registry                            |

{{% /tab %}}
{{< /tabs >}}

### 2. Define the config

Open the generated resource file. Define config attributes for the sensors to
monitor and the alert thresholds.

{{< tabs >}}
{{% tab name="Python" %}}

In `src/models/temp_alert.py`, add config attributes to your class:

```python
class TempAlert(Generic, EasyResource):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "alert-monitor"), "temp-alert"
    )

    sensor_names: list[str]
    max_temp: float
    poll_interval: float
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

Update `validate_config`, `new`, and `reconfigure`:

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
        instance = cls(config.name)
        instance.alerts = []
        instance._monitor_task = None
        instance._stop_event = asyncio.Event()
        instance.reconfigure(config, dependencies)
        return instance

    def reconfigure(self, config: ComponentConfig,
                    dependencies: Mapping[ResourceName, ResourceBase]) -> None:
        # Stop any existing monitor loop
        if self._monitor_task is not None:
            self._stop_event.set()
            self._monitor_task = None

        fields = config.attributes.fields
        self.sensor_names = [
            v.string_value
            for v in fields["sensor_names"].list_value.values
        ]
        self.max_temp = fields["max_temp"].number_value
        self.poll_interval = (
            fields["poll_interval_secs"].number_value
            if "poll_interval_secs" in fields
            else 10.0
        )

        # 2. Resolve: find each sensor in the dependencies map
        self.sensors = {}
        for name, dep in dependencies.items():
            if name.name in self.sensor_names:
                self.sensors[name.name] = dep

        # Start the monitor loop
        self._stop_event = asyncio.Event()
        self._monitor_task = asyncio.create_task(self._monitor_loop())
```

{{% /tab %}}
{{% tab name="Go" %}}

Update the struct and constructor. `resource.Named` provides the `Name()`
method that `viam-server` requires. `resource.NativeConfig` converts the raw
config into your typed struct. `sensor.FromProvider` looks up a sensor
dependency by name from the dependencies map.

```go
type TempAlert struct {
    resource.Named
    logger   logging.Logger
    cfg      *Config
    sensors  map[string]sensor.Sensor
    mu       sync.Mutex
    alerts   []Alert
    cancelFn func()
}

type Alert struct {
    Sensor    string  `json:"sensor"`
    Value     float64 `json:"value"`
    Threshold float64 `json:"threshold"`
    Time      string  `json:"time"`
}

func newTempAlert(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (resource.Resource, error) {
    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }

    // 2. Resolve: find each sensor in the dependencies map
    sensors := make(map[string]sensor.Sensor)
    for _, name := range cfg.SensorNames {
        s, err := sensor.FromProvider(deps, name)
        if err != nil {
            return nil, fmt.Errorf("sensor %q not found: %w", name, err)
        }
        sensors[name] = s
    }

    monitorCtx, cancelFn := context.WithCancel(context.Background())
    svc := &TempAlert{
        Named:    conf.ResourceName().AsNamed(),
        logger:   logger,
        cfg:      cfg,
        sensors:  sensors,
        alerts:   []Alert{},
        cancelFn: cancelFn,
    }

    // Start background monitor loop
    go svc.monitorLoop(monitorCtx)

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
                    timeout=self.poll_interval,
                )
                break  # Stop event was set
            except asyncio.TimeoutError:
                pass  # Continue polling
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
func (s *TempAlert) monitorLoop(ctx context.Context) {
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

func (s *TempAlert) checkSensors(ctx context.Context) {
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
            return {"alerts": self.alerts}

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
func (s *TempAlert) DoCommand(
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
func (s *TempAlert) Close(ctx context.Context) error {
    s.cancelFn()
    s.logger.CInfof(ctx, "TempAlert monitor stopped")
    return nil
}
```

In Go, the `Reconfigure` method should also stop the old loop and start a new
one:

```go
func (s *TempAlert) Reconfigure(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
) error {
    // Stop the old loop
    s.cancelFn()

    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return err
    }

    sensors := make(map[string]sensor.Sensor)
    for _, name := range cfg.SensorNames {
        sens, err := sensor.FromProvider(deps, name)
        if err != nil {
            return fmt.Errorf("sensor %q not found: %w", name, err)
        }
        sensors[name] = sens
    }

    monitorCtx, cancelFn := context.WithCancel(context.Background())

    s.mu.Lock()
    s.cfg = cfg
    s.sensors = sensors
    s.cancelFn = cancelFn
    s.mu.Unlock()

    go s.monitorLoop(monitorCtx)
    return nil
}
```

{{% /tab %}}
{{< /tabs >}}

### 7. Test locally

**Deploy with hot reloading:**

Ensure you have at least one sensor configured on your machine (this is the resource your logic module will monitor).

Use the CLI to build and deploy your module:

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

After deploying, configure the service's attributes in the Viam app:

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

You should see a response with any alerts that have been triggered.

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

### 8. Schedule logic with jobs (optional)

Instead of running a continuous background loop, you can use
{{< glossary_tooltip term_id="job" text="jobs" >}} to have `viam-server` call
your service's `DoCommand` method on a schedule. This is useful for periodic
tasks that don't need sub-second polling.

1. In the [Viam app](https://app.viam.com), click the **+** icon next to your
   machine part and select **Job**.
2. Name the job and click **Create**.
3. Set the **Schedule** to one of:
   - **Interval** -- a Go duration string like `5s`, `1m`, or `2h30m`.
   - **Cron** -- a 5- or 6-part cron expression (for example, `0 */5 * * *`).
4. Select your service resource by name.
5. Select the `DoCommand` **Method** and specify the **Command**, for example:

   ```json
   { "command": "get_alerts" }
   ```

6. Click **Save**.

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
- Verify the `poll_interval_secs` is greater than 0.
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
