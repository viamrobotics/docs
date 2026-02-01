---
linkTitle: "Part 3: Control Logic"
title: "Part 3: Control Logic"
weight: 30
layout: "docs"
type: "docs"
description: "Write inspection logic that detects dented cans and rejects them."
date: "2025-01-30"
---

**Goal:** Write inspection logic that detects defective cans and rejects them.

**Skills:** Generate module scaffolding using the Viam CLI, experience with Viam SDKs, develop code iteratively against remote hardware

**Time:** ~15 min

## What You'll Build

Your vision pipeline detects defective cans and records the results with images synced to the cloud.
Now you'll write code that **acts** on those detections by rejecting defective cans.
This completes the **sense-think-act** cycle that defines robotics applications:

1. **Sense**—Camera captures images
2. **Think**—Vision service classifies cans as PASS/FAIL
3. **Act**—Rejector pushes defective cans off the belt

You'll use the **module-first development pattern**: write code on your laptop, test it against remote hardware over the network.
This workflow lets you iterate quickly—edit code, run it, see results—without redeploying after every change.

## Prerequisites

This part of the tutorial requires the Go programming language and the Viam CLI.

### Install Go

Check your Go version:

```bash
go version
```

You need Go 1.21 or later. If Go isn't installed or is outdated, download it from [go.dev/dl](https://go.dev/dl/).

### Install the Viam CLI

The Viam CLI is used for authentication, module generation, and deployment.

{{< tabs >}}
{{% tab name="macOS" %}}

```bash
brew tap viamrobotics/brews
brew install viam
```

{{% /tab %}}
{{% tab name="Linux" %}}

```bash
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod +x /usr/local/bin/viam
```

{{% /tab %}}
{{% tab name="Windows" %}}

```powershell
Invoke-WebRequest -Uri "https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-windows-amd64.exe" -OutFile "viam.exe"
```

Then run as `.\viam.exe` or add the directory to your PATH.

{{% /tab %}}
{{< /tabs >}}

### Verify and Log In

Verify the CLI is installed:

```bash
viam version
```

Log in to Viam:

```bash
viam login
```

This stores credentials that your code will use to connect to remote machines.

{{< alert title="Note" color="info" >}}
The Viam CLI (`viam`) is different from `viam-server`. The CLI runs on your development machine; `viam-server` runs on your robot/machine.
{{< /alert >}}

## 3.1 Generate the Module Scaffolding

A **module** in Viam is a package of code that adds capabilities to a machine. Modules run alongside viam-server and can provide custom components (like a new type of sensor) or services (like our inspection logic). By packaging code as a module, you can deploy it to any machine, share it with others, and manage versions through the Viam registry.

The Viam CLI can generate module boilerplate—saving you from writing registration code, build configuration, and project structure from scratch. This lets you focus on your business logic instead of infrastructure.

**Set your organization's namespace:**

Before creating a module, your organization needs a public namespace. This is a unique identifier used in module names (e.g., `my-namespace:inspection-module`).

1. Click the organization dropdown in the upper right corner of the Viam app next to your initials
2. Select **Settings**
3. Find **Public namespace** and enter a unique name (lowercase letters, numbers, hyphens)
4. Click **Save**

If your organization already has a namespace, you can skip this step.

**Generate the module scaffolding:**

```bash
viam module generate
```

The generator prompts you for several values. Here's what to enter and why:

**Module name:** `inspection-module`

This is the name that appears in the registry and how you'll reference the module in configurations. Use lowercase letters, numbers, and hyphens.

**Language:** `Go`

Viam supports Go and Python for module development. This tutorial uses Go. Both languages have full access to Viam's APIs—choose based on your preference.

**Visibility:** `Private`

Private modules are only visible to members of your organization. Public modules appear in the Viam registry for anyone to use. You can change visibility later if you decide to share your module.

**Namespace/Organization:** Select your organization

The namespace identifies who owns the module (e.g., `acme-corp:inspection-module`). If you belong to multiple organizations, choose the one where your machine is registered.

**Resource type:** `Generic Service`

Viam has built-in APIs for common hardware (camera, motor, arm). When your logic doesn't fit those categories, Generic Service provides a flexible `DoCommand` interface that accepts arbitrary key-value commands—ideal for application-specific logic like inspection. Your service can still _use_ cameras and other components internally.

**Model name:** `inspector`

The model name identifies this specific implementation within your module. A single module can contain multiple models. In your machine configuration, you'll reference this as `<namespace>:inspection-module:inspector`.

**Register module:** `Yes`

Registering creates an entry in Viam's registry for your organization. This does _not_ upload your source code—only metadata like the module name and version. Your source code stays on your machine until you explicitly upload a compiled binary. Registration enables cloud deployment: without it, you'd have to manually copy files to each machine. You can delete a registered module at any time.

### Understanding the Generated Files

The generator creates this structure:

```text
inspection-module/
├── cmd/
│   ├── cli/
│   │   └── main.go        # CLI for testing
│   └── module/
│       └── main.go        # Module entry point
├── go.mod
├── Makefile               # Build commands
├── meta.json              # Registry metadata
├── module.go              # Your service implementation
├── README.md
└── <your-namespace>_inspection-module_inspector.md
```

| File                                              | Purpose                                                                                                    |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `cmd/module/main.go`                              | Entry point when running as a module. Registers your service with viam-server. You won't modify this.      |
| `cmd/cli/main.go`                                 | Entry point for local testing. We'll modify this to connect to remote machines.                            |
| `go.mod`                                          | Go module definition. Declares the module name and Go version.                                             |
| `Makefile`                                        | Build commands. Run `make module.tar.gz` to build and package the module.                                  |
| `meta.json`                                       | Module metadata for the Viam registry. Defines module ID, visibility, entrypoint, and build configuration. |
| `module.go`                                       | Your service implementation. Contains Config, constructor, and methods. This is where your logic goes.     |
| `README.md`                                       | Template documentation for your module. Update with your module's description.                             |
| `<your-namespace>_inspection-module_inspector.md` | Template documentation for the inspector model. Describes configuration and DoCommand usage.               |

{{< alert title="Takeaway" color="tip" >}}
The `viam module` command handles infrastructure (registration, lifecycle, build config). You focus on `module.go` (your logic) and `cmd/cli/main.go` (testing).
{{< /alert >}}

## 3.2 Add Remote Machine Connection

The generated CLI creates your service with empty dependencies—fine for testing logic in isolation, but useless for testing against real hardware. We'll modify it to connect to your remote machine and access its resources. This enables the **module-first development pattern**: your code runs locally on your laptop, but it talks to real cameras and other hardware your machine configuration includes.

Why is this valuable? Traditional embedded development requires: edit code → build → deploy → test → repeat. With module-first development: edit code → run locally → see results on real hardware. The iteration cycle drops from minutes to seconds.

**Get your machine address:**

1. In the Viam app, go to your machine's **Configure** page
2. Click the **Online** dropdown
3. Click **Remote address** to copy your machine address

[SCREENSHOT: Code sample tab showing machine address]

### Step 1: Connect to Your Machine

The generated `realMain` function creates your inspector with empty dependencies—useful for testing in isolation, but it can't access your remote machine. We'll replace it with code that:

- Accepts a `-host` flag for your machine's address
- Uses your `viam login` credentials to authenticate
- Establishes a secure connection to the remote machine

Open `cmd/cli/main.go` and replace the import block with:

```go
import (
    "context"
    "flag"
    "fmt"

    "github.com/erh/vmodutils"
    "go.viam.com/rdk/logging"
)
```

Then replace the `realMain` function with:

```go
func realMain() error {
    ctx := context.Background()
    logger := logging.NewLogger("cli")

    host := flag.String("host", "", "Machine address (required)")
    flag.Parse()

    if *host == "" {
        return fmt.Errorf("need -host flag (get address from Viam app)")
    }

    logger.Infof("Connecting to %s...", *host)
    machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
    if err != nil {
        return fmt.Errorf("failed to connect: %w", err)
    }
    defer machine.Close(ctx)

    logger.Info("Connected successfully!")
    return nil
}
```

**Test the connection:**

```bash
go run cmd/cli/main.go -host YOUR_MACHINE_ADDRESS
```

You'll see WebRTC diagnostic output as the connection is established. Look for these messages confirming the connection:

```text
Connecting to your-machine.abc123.viam.cloud...
...
successfully (re)connected to remote at address
...
Connected successfully!
```

If you see an error, verify:

- Your machine is online (check the Viam app)
- You're logged in (`viam login`)
- The address is correct

### Step 2: Access Remote Resources

Now let's verify we can access the camera on the remote machine.

**Add the camera import:**

At the top of `cmd/cli/main.go`, add this import:

```go
"go.viam.com/rdk/components/camera"
```

**Fetch the camera dependencies:**

```bash
go mod tidy
```

**Add camera access after the connection:**

After the `logger.Info("Connected successfully!")` line, add:

```go
// Get the camera from the remote machine
cam, err := camera.FromRobot(machine, "inspection-cam")
if err != nil {
    return fmt.Errorf("failed to get camera: %w", err)
}

// Capture an image
images, _, err := cam.Images(ctx, nil, nil)
if err != nil {
    return fmt.Errorf("failed to get images: %w", err)
}

if len(images) == 0 {
    return fmt.Errorf("no images returned from camera")
}

logger.Infof("Got image from camera: %s", images[0].SourceName)
```

If your editor doesn't auto-format, run `gofmt -w cmd/cli/main.go` to fix indentation.

**Test resource access:**

```bash
go run cmd/cli/main.go -host YOUR_MACHINE_ADDRESS
```

You'll see the same WebRTC diagnostic output, followed by the camera confirmation:

```text
Connected successfully!
Got image from camera: inspection-cam
```

You've just accessed a camera on a remote machine from your local development environment. This same pattern works for any Viam resource—motors, sensors, vision services, or custom components.

{{< alert title="Takeaway" color="tip" >}}
The `vmodutils.ConnectToHostFromCLIToken` function uses your `viam login` credentials to establish a secure connection. Once connected, you access resources the same way you would in deployed code. This abstraction is what makes module-first development possible.
{{< /alert >}}

## 3.3 Add Detection Logic

Now we'll implement the actual inspection logic. The generator created `module.go` with stub methods—we'll fill them in to call the vision service and process results.

{{< alert title="Concept: Dependency Injection in Viam" color="info" >}}
Your inspector needs a vision service to detect cans. Rather than hardcoding how to find that service, you _declare_ the dependency in your Config, and Viam _injects_ it into your constructor. This means:

- Your code doesn't know where resources live (local or remote)
- You can swap implementations by changing config, not code
- The same code works in CLI testing and deployed modules
  {{< /alert >}}

**Update the Config struct:**

Find the `Config` struct in `module.go` and update it:

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
// - The CLI (deps come from a remote machine through vmodutils)
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

```text
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

- Verify `vision-service` exists in your machine config (Part 1)
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

**Update the imports in `module.go`:**

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
    VisionService: "vision-service",
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

```text
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

**[Continue to Part 4: Deploy a Module →](../part-4/)**
