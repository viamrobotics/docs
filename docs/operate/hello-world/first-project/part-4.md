---
linkTitle: "Part 4: Deploy as a Module"
title: "Part 4: Deploy as a Module"
weight: 40
layout: "docs"
type: "docs"
description: "Add the DoCommand interface and deploy your inspector to run autonomously."
date: "2025-01-30"
---

**Goal:** Add the DoCommand interface and deploy your inspector to run on the machine autonomously.

**Skills:** DoCommand pattern, module packaging, registry deployment.

**Time:** ~10 min

## What You'll Do

In Part 3, you built inspection logic that runs from your laptop. That's great for development, but in production the code needs to run on the machine itself—so it works even when your laptop is closed.

The generator already created most of what you need:

- `cmd/module/main.go` — module entry point
- `meta.json` — registry metadata
- Model registration in `init()`

You just need to:

1. Add DoCommand so clients can invoke your inspector remotely
2. Build, package, and deploy

## 4.1 Add the DoCommand Interface

When your inspector runs as a module, clients need a way to invoke it. The **generic service** uses `DoCommand`—a flexible method that accepts commands as a map.

**Why DoCommand?** It provides flexibility without defining a custom API. Any client can send `{"detect": true}` or `{"inspect": true}` without generated client code. This is ideal for application-specific logic.

**Add the mapstructure import to `inspector.go`:**

```go
import (
	// ... existing imports ...
	"github.com/mitchellh/mapstructure"
)
```

Run `go get github.com/mitchellh/mapstructure` if needed.

**Add the Command struct and DoCommand method:**

```go
// Command represents the commands the inspector accepts via DoCommand.
type Command struct {
	Detect  bool `mapstructure:"detect"`
	Inspect bool `mapstructure:"inspect"`
}

// DoCommand handles incoming commands from clients.
func (i *Inspector) DoCommand(ctx context.Context, req map[string]interface{}) (map[string]interface{}, error) {
	var cmd Command
	if err := mapstructure.Decode(req, &cmd); err != nil {
		return nil, fmt.Errorf("failed to decode command: %w", err)
	}

	switch {
	case cmd.Detect:
		label, confidence, err := i.Detect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{
			"label":      label,
			"confidence": confidence,
		}, nil

	case cmd.Inspect:
		label, confidence, rejected, err := i.Inspect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{
			"label":      label,
			"confidence": confidence,
			"rejected":   rejected,
		}, nil

	default:
		return nil, fmt.Errorf("unknown command: %v", req)
	}
}
```

**Test DoCommand through the CLI:**

Update your CLI to call through DoCommand (optional but useful for verification). In `cmd/cli/main.go`, change the command handling:

```go
switch *cmd {
case "detect":
	result, err := insp.DoCommand(ctx, map[string]interface{}{"detect": true})
	if err != nil {
		return err
	}
	logger.Infof("Detection: %s (%.1f%%)",
		result["label"], result["confidence"].(float64)*100)

case "inspect":
	result, err := insp.DoCommand(ctx, map[string]interface{}{"inspect": true})
	if err != nil {
		return err
	}
	logger.Infof("Inspection: %s (%.1f%%), rejected=%v",
		result["label"], result["confidence"].(float64)*100, result["rejected"])

default:
	return fmt.Errorf("unknown command: %s", *cmd)
}
```

Test it:

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
```

Output should be identical to before—you've just formalized the interface.

## 4.2 Review the Generated Module Structure

The generator already created everything needed to run as a module. Let's review what's there.

**`cmd/module/main.go`** — The module entry point:

```go
func main() {
	module.ModularMain(
		resource.APIModel{API: generic.API, Model: inspector.Model},
	)
}
```

This registers your model with viam-server and handles all communication. You don't need to modify it.

**`inspector.go`** — Model registration in `init()`:

The generator created an `init()` function that registers your model:

```go
var Model = resource.NewModel("your-namespace", "inspection-module", "inspector")

func init() {
	resource.RegisterService(generic.API, Model,
		resource.Registration[resource.Resource, *Config]{
			Constructor: newInspector,
		},
	)
}
```

This runs automatically when the module starts, telling viam-server how to create instances of your service.

**`meta.json`** — Registry metadata:

```json
{
  "module_id": "your-namespace:inspection-module",
  "visibility": "private",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "your-namespace:inspection-module:inspector"
    }
  ],
  "entrypoint": "bin/inspection-module"
}
```

This tells the registry what your module provides.

{{< alert title="The key pattern" color="tip" >}}
The generator created module infrastructure. You added business logic (`Detect`, `Inspect`) and a client interface (`DoCommand`). The same `NewInspector` constructor works for both CLI testing and module deployment.
{{< /alert >}}

## 4.3 Build and Deploy

**Build the module binary:**

```bash
make
# Or manually: go build -o bin/inspection-module ./cmd/module
```

**Package for upload:**

```bash
tar czf module.tar.gz meta.json bin/
```

**Upload to the registry:**

```bash
viam module upload --version 1.0.0 --platform linux/amd64 module.tar.gz
```

{{< alert title="Note" color="info" >}}
Use `linux/arm64` for ARM machines (like Raspberry Pi).
{{< /alert >}}

**Add the module to your machine:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine
3. Select **Local module**, then **Local module**
4. Search for your module name (e.g., `your-namespace:inspection-module`)
5. Click **Add module**

**Add the inspector service:**

1. Click **+** next to your machine
2. Select **Service**, then **generic**
3. For **Model**, select your model (e.g., `your-namespace:inspection-module:inspector`)
4. Name it `inspector`
5. Click **Create**

**Configure the service attributes:**

```json
{
  "camera": "inspection-cam",
  "vision_service": "can-detector",
  "rejector": "rejector"
}
```

Click **Save**.

**Verify it's running:**

1. Go to the **Logs** tab
2. Look for log messages from the inspector module
3. You should see it starting and connecting to dependencies

The inspector now runs on the machine autonomously.

## 4.4 Summary

You deployed your inspection logic as a Viam module:

1. **Added DoCommand** — exposed operations via the generic service interface
2. **Reviewed** — the generator already created module structure and registration
3. **Deployed** — built, packaged, uploaded, configured

**The development pattern:**

- During development: CLI runs locally, uses remote hardware (fast iteration)
- In production: Module runs on machine, same code (autonomous operation)

**Your inspection system now runs 24/7** — detecting defects and rejecting bad cans without your laptop connected.

**[Continue to Part 5: Scale →](../part-5/)**
