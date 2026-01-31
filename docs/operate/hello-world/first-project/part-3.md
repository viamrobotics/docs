---
linkTitle: "Part 3: Control Logic"
title: "Part 3: Control Logic"
weight: 30
layout: "docs"
type: "docs"
description: "Write inspection logic that detects dented cans and rejects them."
date: "2025-01-30"
---

**Goal:** Write inspection logic that detects dented cans and rejects them, testing from your laptop.

**Skills:** Viam module generator, SDK usage, module-first development.

**Time:** ~15 min

## What You'll Build

Your vision pipeline detects dented cans and records the results. Now you'll write code that **acts** on those detections—rejecting defective cans automatically.

This completes the **sense-think-act** cycle that defines robotic systems:

1. **Sense**—Camera captures images
2. **Think**—Vision service classifies cans as PASS/FAIL
3. **Act**—Rejector pushes defective cans off the belt

You'll use the **module-first development pattern**: write code on your laptop, test it against remote hardware over the network. This workflow lets you iterate quickly—edit code, run it, see results—without redeploying after every change.

## Prerequisites

Before starting, verify you have the required tools installed.

**Check Go version:**

```bash
go version
```

You need Go 1.21 or later. If Go isn't installed or is outdated, download it from [go.dev/dl](https://go.dev/dl/).

**Install the Viam CLI:**

The Viam CLI is used for authentication, module generation, and deployment. Install it:

```bash
# macOS (Homebrew)
brew tap viamrobotics/brews
brew install viam

# Linux (binary)
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod +x /usr/local/bin/viam
```

Verify it's installed:

```bash
viam version
```

**Log in to Viam:**

```bash
viam login
```

This stores credentials that your code will use to connect to remote machines.

{{< alert title="Note" color="info" >}}
The Viam CLI (`viam`) is different from `viam-server`. The CLI runs on your development machine; `viam-server` runs on your robot/machine.
{{< /alert >}}

## 3.1 Generate the Module Scaffold

A **module** in Viam is a package of code that adds capabilities to a machine. Modules run alongside viam-server and can provide custom components (like a new type of sensor) or services (like our inspection logic). By packaging code as a module, you can deploy it to any machine, share it with others, and manage versions through the Viam registry.

The Viam CLI can generate module boilerplate—saving you from writing registration code, build configuration, and project structure from scratch. This lets you focus on your business logic instead of infrastructure.

**Create and generate the module:**

```bash
mkdir inspection-module && cd inspection-module
viam module generate
```

When prompted, enter:

- **Language:** `go`
- **Module name:** `inspection-module`
- **Model name:** `inspector`
- **Resource subtype:** `generic-service`
- **Namespace:** Your organization namespace (find it in Viam app under **Organization → Settings**)
- **Visibility:** `private`
- **Enable cloud build:** `no` (for simplicity during development)

{{< alert title="Why generic-service?" color="info" >}}
Viam has built-in APIs for common resource types (camera, motor, arm, etc.). When your logic doesn't fit those categories, `generic-service` provides a flexible interface via `DoCommand`—a method that accepts arbitrary commands as key-value maps. This is ideal for application-specific logic like inspection.
{{< /alert >}}

The generator creates this structure:

```
inspection-module/
├── cmd/
│   ├── cli/
│   │   └── main.go        # CLI for testing
│   └── module/
│       └── main.go        # Module entry point
├── inspector.go           # Your service implementation
├── meta.json              # Registry metadata
├── Makefile               # Build commands
└── go.mod
```

### Understanding the Generated Files

| File                 | Purpose                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| `cmd/module/main.go` | Entry point when running as a module. Registers your service with viam-server. You won't modify this.  |
| `cmd/cli/main.go`    | Entry point for local testing. We'll modify this to connect to remote machines.                        |
| `inspector.go`       | Your service implementation. Contains Config, constructor, and methods. This is where your logic goes. |
| `meta.json`          | Tells the Viam registry what your module provides. Used during deployment.                             |
| `Makefile`           | Build commands. `make` builds the module binary.                                                       |

{{< alert title="Takeaway" color="tip" >}}
The generator handles infrastructure (registration, lifecycle, build config). You focus on `inspector.go` (your logic) and `cmd/cli/main.go` (testing).
{{< /alert >}}

## 3.2 Add Remote Machine Connection

The generated CLI creates your service with empty dependencies—fine for testing logic in isolation, but useless for testing against real hardware. We'll modify it to connect to your remote machine and pull its resources as dependencies. This enables the **module-first development pattern**: your code runs locally on your laptop, but it talks to real cameras and motors over the network.

Why is this valuable? Traditional embedded development requires: edit code → build → deploy → test → repeat. With module-first development: edit code → run locally → see results on real hardware. The iteration cycle drops from minutes to seconds.

**Add the vmodutils dependency:**

```bash
go get github.com/erh/vmodutils
```

The `vmodutils` package provides helpers for connecting to remote machines using your Viam CLI credentials.

**Get your machine address:**

1. In the Viam app, go to your machine's page
2. Click **Code sample** in the top right
3. Copy the machine address (looks like `your-machine-main.abc123.viam.cloud`)

[SCREENSHOT: Code sample tab showing machine address]

**Modify the generated CLI:**

Open `cmd/cli/main.go`. The generator created a stub with empty dependencies:

```go
deps := resource.Dependencies{}
// can load these from a remote machine if you need
```

Replace the entire file with:

```go
package main

import (
	"context"
	"flag"
	"fmt"

	"github.com/erh/vmodutils"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/services/generic"

	inspector "inspection-module"
)

func main() {
	if err := realMain(); err != nil {
		panic(err)
	}
}

func realMain() error {
	// Context carries cancellation signals and deadlines through the call chain.
	// Most Viam APIs take a context as their first argument.
	ctx := context.Background()
	logger := logging.NewLogger("cli")

	// Parse command-line flags for machine address and command selection
	host := flag.String("host", "", "Machine address (required)")
	cmd := flag.String("cmd", "detect", "Command: detect or inspect")
	flag.Parse()

	if *host == "" {
		return fmt.Errorf("need -host flag (get address from Viam app → Code sample)")
	}

	// Configuration specifying which resources to use.
	// These names must match what you configured in the Viam app.
	conf := &inspector.Config{
		Camera:        "inspection-cam",
		VisionService: "can-detector",
	}

	if _, _, err := conf.Validate(""); err != nil {
		return err
	}

	// Connect to the remote machine.
	// This reads auth credentials from `viam login`, establishes a secure gRPC
	// connection, and returns a client that can access any resource on the machine.
	logger.Infof("Connecting to %s...", *host)
	machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
	if err != nil {
		return fmt.Errorf("failed to connect: %w", err)
	}
	defer machine.Close(ctx) // Always close connections when done

	// Convert the machine's resources into a Dependencies map.
	// This is the same format Viam uses when running as a module—so our
	// constructor works identically in both CLI and deployed contexts.
	deps, err := vmodutils.MachineToDependencies(machine)
	if err != nil {
		return fmt.Errorf("failed to get dependencies: %w", err)
	}

	// Create our inspector using the same constructor the module will use.
	// The inspector doesn't know (or care) whether deps came from a remote
	// machine or from viam-server's dependency injection.
	insp, err := inspector.NewInspector(ctx, deps, generic.Named("inspector"), conf, logger)
	if err != nil {
		return err
	}
	defer insp.Close(ctx)

	// Run the requested command
	switch *cmd {
	case "detect":
		label, confidence, err := insp.Detect(ctx)
		if err != nil {
			return err
		}
		logger.Infof("Detection: %s (%.1f%% confidence)", label, confidence*100)

	default:
		return fmt.Errorf("unknown command: %s (use 'detect')", *cmd)
	}

	return nil
}
```

{{< alert title="Takeaway" color="tip" >}}
The CLI connects to a remote machine, extracts its resources as dependencies, and passes them to your constructor. Your inspector code doesn't know whether it's running from the CLI or as a deployed module—it just uses the dependencies it's given. This abstraction is what makes module-first development possible.
{{< /alert >}}

## 3.3 Add Detection Logic

Now we'll implement the actual inspection logic. The generator created `inspector.go` with stub methods—we'll fill them in to call the vision service and process results.

{{< alert title="Concept: Dependency Injection in Viam" color="info" >}}
Your inspector needs a vision service to detect cans. Rather than hardcoding how to find that service, you _declare_ the dependency in your Config, and Viam _injects_ it into your constructor. This means:

- Your code doesn't know where resources live (local or remote)
- You can swap implementations by changing config, not code
- The same code works in CLI testing and deployed modules
  {{< /alert >}}

**Update the Config struct:**

Find the `Config` struct in `inspector.go` and update it:

```go
// Config declares which resources the inspector needs.
// The json tags map these fields to the JSON config in the Viam app.
// When deployed, users configure these values in the app UI.
type Config struct {
	Camera        string `json:"camera"`
	VisionService string `json:"vision_service"`
}

// Validate checks that required fields are present and returns dependency names.
// Viam calls this during startup to:
// 1. Catch config errors early (before trying to start the service)
// 2. Know which resources to inject into our constructor
// The first return value lists required dependencies; Viam ensures they exist.
func (cfg *Config) Validate(path string) ([]string, []string, error) {
	if cfg.Camera == "" {
		return nil, nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, nil, fmt.Errorf("vision_service is required")
	}
	// Returning these names tells Viam: "inject these resources into my constructor"
	return []string{cfg.Camera, cfg.VisionService}, nil, nil
}
```

**Update the imports:**

Make sure your imports include:

```go
import (
	"context"
	"fmt"

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/generic"
	"go.viam.com/rdk/services/vision"
)
```

**Update the Inspector struct:**

Find the struct (the generator may have named it differently) and ensure it has:

```go
// Inspector holds references to the resources we depend on.
// These are injected through the constructor—we never create them ourselves.
type Inspector struct {
	resource.AlwaysRebuild // Tells Viam to recreate this service on config changes

	name     resource.Name   // Unique identifier for this instance
	conf     *Config
	logger   logging.Logger
	detector vision.Service  // The vision service we'll call for detections
}
```

**Update the constructor:**

The generator created two constructors: `newInspector` (called by viam-server) and `NewInspector` (public, called by our CLI). Update `NewInspector`:

```go
// NewInspector creates an inspector from dependencies.
// This same constructor is used by both:
// - The CLI (deps come from a remote machine via vmodutils)
// - The module (deps come from viam-server's dependency injection)
func NewInspector(
	ctx context.Context,
	deps resource.Dependencies,
	name resource.Name,
	conf *Config,
	logger logging.Logger,
) (*Inspector, error) {
	// Extract the vision service from the dependencies map.
	// FromDependencies looks up the resource by name and returns it as the correct type.
	// If the resource doesn't exist or isn't a vision service, it returns an error.
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, fmt.Errorf("failed to get vision service %q: %w", conf.VisionService, err)
	}

	return &Inspector{
		name:     name,
		conf:     conf,
		logger:   logger,
		detector: detector,
	}, nil
}
```

Also update the module's internal constructor to delegate to our public one:

```go
// newInspector is called by viam-server when creating this service.
// It extracts typed config from the raw config and delegates to NewInspector.
func newInspector(ctx context.Context, deps resource.Dependencies, rawConf resource.Config, logger logging.Logger) (resource.Resource, error) {
	conf, err := resource.NativeConfig[*Config](rawConf)
	if err != nil {
		return nil, err
	}
	return NewInspector(ctx, deps, rawConf.ResourceName(), conf, logger)
}
```

**Add the Detect method:**

```go
// Detect captures an image and runs ML inference to classify the can.
// Returns: label (e.g., "PASS" or "FAIL"), confidence score (0.0-1.0), error
func (i *Inspector) Detect(ctx context.Context) (string, float64, error) {
	// DetectionsFromCamera tells the vision service which camera to use.
	// The vision service handles: grabbing the image, running the ML model,
	// and returning structured detection results.
	detections, err := i.detector.DetectionsFromCamera(ctx, i.conf.Camera, nil)
	if err != nil {
		return "", 0, err
	}

	// No detections means no can was visible (or the model didn't recognize one)
	if len(detections) == 0 {
		return "NO_DETECTION", 0, nil
	}

	// Find the highest-confidence detection.
	// When multiple objects are detected, we care about the most confident one.
	best := detections[0]
	for _, det := range detections[1:] {
		if det.Score() > best.Score() {
			best = det
		}
	}

	// Label() returns what the model classified this as (e.g., "PASS", "FAIL")
	// Score() returns confidence from 0.0 to 1.0
	return best.Label(), best.Score(), nil
}
```

**Test the connection and detection:**

```bash
go mod tidy
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud
```

You should see:

```
Connecting to your-machine-main.abc123.viam.cloud...
Detection: PASS (94.2% confidence)
```

Run it several times—results change as different cans pass under the camera.

{{< alert title="What just happened" color="info" >}}
Your laptop connected to the remote machine, your code called the vision service, and the vision service ran ML inference on an image from the camera. The code runs locally but uses remote hardware—this is the module-first pattern in action.
{{< /alert >}}

{{< expand "Troubleshooting: Connection or detection failures" >}}
**"failed to connect" or timeout errors:**

- Verify your machine is online in the Viam app (green dot)
- Check that you've run `viam login` successfully
- Confirm the host address is correct (copy fresh from Code sample tab)

**"failed to get vision service" error:**

- Verify `can-detector` exists in your machine config (Part 1)
- Check the exact name matches—it's case-sensitive

**"NO_DETECTION" result:**

- Normal if no can is in view—wait for one to appear
- Check the camera is working in the Viam app's Test panel
  {{< /expand >}}

### Milestone 1: Detection Working

You can now detect cans from your laptop. Run the CLI a few times and watch results change as cans pass under the camera.

{{< alert title="Takeaway" color="tip" >}}
You declared dependencies in Config, returned them from Validate, and extracted them in your constructor with `FromDependencies`. This pattern works for any Viam resource—cameras, motors, arms, other services. Your code is decoupled from how resources are created or where they live.
{{< /alert >}}

## 3.4 Configure the Rejector

Before writing rejection code, add the rejector hardware to your machine. This demonstrates that you can add new hardware to a running system and immediately use it from your code.

**Add the motor component:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Component**, then **motor**
4. For **Model**, select `fake` (simulated motor for testing)
5. Name it `rejector`
6. Click **Create**
7. Click **Save**

{{< alert title="Why a fake motor?" color="info" >}}
The `fake` model simulates motor behavior without physical hardware. Your code calls the same API (`GoFor`, `Stop`, etc.) and gets realistic responses. This lets you develop and test control logic before connecting real actuators. In production, you'd swap to a real motor model (like `gpio`) by changing configuration—no code changes needed.
{{< /alert >}}

**Test it in the Viam app:**

1. Find the `rejector` motor in your config
2. Click **Test** at the bottom of its card
3. Try the **Run** controls to verify it responds

[SCREENSHOT: Motor test panel showing rejector controls]

## 3.5 Add Rejection Logic

Now we'll close the control loop: detect a defect → decide to reject → actuate the motor. This is the "act" part of sense-think-act.

**Update the imports in `inspector.go`:**

```go
import (
	"context"
	"fmt"

	"go.viam.com/rdk/components/motor"  // Add this
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/generic"
	"go.viam.com/rdk/services/vision"
)
```

**Add Rejector to Config:**

```go
type Config struct {
	Camera        string `json:"camera"`
	VisionService string `json:"vision_service"`
	Rejector      string `json:"rejector"`  // Add the new dependency
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
	if cfg.Camera == "" {
		return nil, nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, nil, fmt.Errorf("vision_service is required")
	}
	if cfg.Rejector == "" {
		return nil, nil, fmt.Errorf("rejector is required")
	}
	// Now we depend on three resources
	return []string{cfg.Camera, cfg.VisionService, cfg.Rejector}, nil, nil
}
```

**Add rejector to Inspector struct:**

```go
type Inspector struct {
	resource.AlwaysRebuild

	name     resource.Name
	conf     *Config
	logger   logging.Logger
	detector vision.Service
	rejector motor.Motor  // Add this—same pattern as the vision service
}
```

**Update the constructor:**

```go
func NewInspector(
	ctx context.Context,
	deps resource.Dependencies,
	name resource.Name,
	conf *Config,
	logger logging.Logger,
) (*Inspector, error) {
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, fmt.Errorf("failed to get vision service %q: %w", conf.VisionService, err)
	}

	// Same pattern: extract the motor from dependencies by name
	rejector, err := motor.FromDependencies(deps, conf.Rejector)
	if err != nil {
		return nil, fmt.Errorf("failed to get rejector %q: %w", conf.Rejector, err)
	}

	return &Inspector{
		name:     name,
		conf:     conf,
		logger:   logger,
		detector: detector,
		rejector: rejector,
	}, nil
}
```

**Add the reject and Inspect methods:**

```go
// reject activates the rejector motor to push a defective can off the belt.
func (i *Inspector) reject(ctx context.Context) error {
	if err := i.rejector.GoFor(ctx, 100, 1, nil); err != nil {
		return err
	}
	i.logger.Info("Defective can rejected")
	return nil
}

// Inspect runs the full inspection cycle: detect, decide, and act.
// Returns: label, confidence, whether rejection was triggered, error
func (i *Inspector) Inspect(ctx context.Context) (string, float64, bool, error) {
	label, confidence, err := i.Detect(ctx)
	if err != nil {
		return "", 0, false, err
	}

	// Decision logic: reject if FAIL with sufficient confidence.
	// The threshold (0.7) avoids acting on uncertain detections.
	// In production, you'd tune this based on the cost of errors:
	// - Lower threshold: catch more defects, risk more false positives
	// - Higher threshold: fewer false positives, might miss some defects
	shouldReject := label == "FAIL" && confidence > 0.7

	if shouldReject {
		if err := i.reject(ctx); err != nil {
			// Log but don't fail—we still want to return the detection result
			// even if the actuator had a problem
			i.logger.Errorw("Failed to reject", "error", err)
		}
	}

	return label, confidence, shouldReject, nil
}
```

**Update the CLI config and add the inspect command:**

In `cmd/cli/main.go`, update the config:

```go
conf := &inspector.Config{
	Camera:        "inspection-cam",
	VisionService: "can-detector",
	Rejector:      "rejector",  // Add the new dependency
}
```

Update the command switch:

```go
switch *cmd {
case "detect":
	label, confidence, err := insp.Detect(ctx)
	if err != nil {
		return err
	}
	logger.Infof("Detection: %s (%.1f%% confidence)", label, confidence*100)

case "inspect":
	label, confidence, rejected, err := insp.Inspect(ctx)
	if err != nil {
		return err
	}
	logger.Infof("Inspection: %s (%.1f%%), rejected=%v", label, confidence*100, rejected)

default:
	return fmt.Errorf("unknown command: %s (use 'detect' or 'inspect')", *cmd)
}
```

**Test both commands:**

```bash
# Detection only (no actuation)
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd detect

# Full inspection with rejection
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
```

With a dented can:

```
Inspection: FAIL (87.3%), rejected=true
Defective can rejected
```

### Milestone 2: Full Inspection Loop Working

You now have a complete sense-think-act loop: camera senses, ML model thinks, motor acts. And it all runs from your laptop against remote hardware.

## 3.6 Summary

You built a complete inspection system using the module-first development pattern:

1. **Generated** the module scaffold—infrastructure handled, you focus on logic
2. **Connected** to remote hardware from local code using vmodutils
3. **Implemented detection** by calling the vision service and processing results
4. **Added rejection** by controlling a motor based on detection confidence

### What You Learned (Transferable to Any Viam Project)

| Concept                      | What It Means                                                     | Where You'll Use It                      |
| ---------------------------- | ----------------------------------------------------------------- | ---------------------------------------- |
| **Module-first development** | Test against real hardware without deploying                      | Any time you're developing control logic |
| **Dependency injection**     | Declare what you need, let Viam provide it                        | Every module you build                   |
| **Resource abstraction**     | Your code calls `motor.GoFor()`—works the same for any motor type | Swapping hardware without code changes   |
| **Incremental building**     | Get detection working, then add rejection                         | Any complex system                       |

### The Key Insight

Your inspector code doesn't know whether it's running from the CLI on your laptop or deployed as a module on the machine. It just uses the dependencies it's given. This abstraction is what makes rapid iteration possible during development and seamless deployment to production.

**Your code is ready.** In Part 4, you'll add the DoCommand interface (so clients can invoke your inspector remotely) and deploy it to run on the machine autonomously.

**[Continue to Part 4: Deploy as a Module →](../part-4/)**
