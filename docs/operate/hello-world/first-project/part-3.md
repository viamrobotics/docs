---
linkTitle: "Part 3: Control Logic"
title: "Part 3: Control Logic"
weight: 30
layout: "docs"
type: "docs"
description: "Write inspection logic that detects defective cans."
date: "2025-01-30"
---

**Goal:** Write inspection logic that detects defective cans.

**Skills:** Generate module scaffolding using the Viam CLI, experience with Viam SDKs, develop code iteratively against remote hardware

**Time:** ~15 min

## What You'll Build

Your vision pipeline detects defective cans and records the results with images synced to the cloud. Now you'll write a module that calls the vision service and exposes detection results through `DoCommand`. This detection data can drive dashboards, alerts, or—in a production system—trigger actuators to reject defective cans.

You'll use the **module-first development pattern**: write code on your laptop, test it against remote hardware over the network. This workflow lets you iterate quickly—edit code, run it, see results—without redeploying after every change.

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

Before creating a module, your organization needs a public namespace. This is a unique identifier used in module names (for example, `my-namespace:inspection-module`).

1. Click the organization dropdown in the upper right corner of the Viam app next to your initials
2. Select **Settings**
3. Find **Public namespace** and enter a unique name (lowercase letters, numbers, hyphens)
4. Click **Save**

{{<imgproc src="/tutorials/first-project/org-settings-dropdown.png" resize="x1100" declaredimensions=true alt="Organization dropdown menu showing Settings option." class="imgzoom shadow">}}

If your organization already has a namespace, you can skip this step.

**Generate the module scaffolding:**

```bash
viam module generate
```

Enter these values when prompted:

| Prompt                 | Value                      |
| ---------------------- | -------------------------- |
| Module name            | `inspection-module`        |
| Language               | `Go`                       |
| Visibility             | `Private`                  |
| Namespace/Organization | _Select your organization_ |
| Resource type          | `Generic Service`          |
| Model name             | `inspector`                |
| Register module        | `Yes`                      |

**Why Generic Service?** Viam has built-in APIs for hardware (camera, motor, arm). When your logic doesn't fit those categories, Generic Service provides a flexible `DoCommand` interface—ideal for application-specific logic like inspection.

**What does "Register module" do?** Creates an entry in the Viam registry (just metadata, not your code). This enables cloud deployment later.

### Files You'll Work With

The generator creates a complete module structure. You'll focus on three files:

- **`module.go`**—Your service implementation. Contains Config, constructor, and methods. This is where your inspection logic goes.
- **`cmd/cli/main.go`**—CLI for local testing. We'll modify this to connect to your remote machine so you can test against real hardware without deploying.
- **`cmd/module/main.go`**—Entry point when deployed. Registers your service with viam-server. You won't modify this.

This is the **module-first development pattern**: write logic in `module.go`, test locally with the CLI against your real machine, then deploy.

## 3.2 Add Remote Machine Connection

The generated CLI creates your service with empty dependencies—fine for testing logic in isolation, but useless for testing against real hardware. We'll modify it to connect to your remote machine and access its resources. This enables the **module-first development pattern**: your code runs locally on your laptop, but it talks to real cameras and other hardware your machine configuration includes.

Why is this valuable? Traditional embedded development requires: edit code → build → deploy → test → repeat. With module-first development: edit code → run locally → see results on real hardware. The iteration cycle drops from minutes to seconds.

**Get your machine address:**

1. In the Viam app, go to your machine's **Configure** page
2. Click the **Online** dropdown
3. Click **Remote address** to copy your machine address

{{<imgproc src="/tutorials/first-project/machine-address.png" resize="x1100" declaredimensions=true alt="Live dropdown showing Remote address option with machine address visible." class="imgzoom shadow">}}

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

Complete all five steps below, then test at the end.

{{< alert title="Concept: Dependency Injection" color="info" >}}
Your inspector needs a vision service to detect cans. Rather than hardcoding how to find that service, you _declare_ the dependency in your Config, and Viam _injects_ it into your constructor. This means:

- Your code doesn't know where resources live (local or remote)
- The same code works in CLI testing and deployed modules
  {{< /alert >}}

### Step 1: Declare Dependencies

The Config struct tells Viam what resources your inspector needs. The Validate method returns those resource names so Viam knows to inject them.

Remember in Part 1 when you configured the camera with `"id": "/inspection_camera"`? When you add the service we're building now to your machine (in Part 4 of this tutorial), you'll configure it with attributes for the camera and vision service to use.

The Config struct in the code below specifies what the names of those attributes will be in the configuration JSON you'll update after including this module in your machine config.

In `module.go`, find the `Config` struct and `Validate` method and replace them with the code below.

```go
type Config struct {
    Camera        string `json:"camera"`
    VisionService string `json:"vision"`
}

func (cfg *Config) Validate(path string) ([]string, []string, error) {
    if cfg.Camera == "" {
        return nil, nil, fmt.Errorf("camera is required")
    }
    if cfg.VisionService == "" {
        return nil, nil, fmt.Errorf("vision is required")
    }
    return []string{cfg.Camera, cfg.VisionService}, nil, nil
}
```

The first return value from Validate lists dependencies—Viam ensures these resources exist before creating your service.

### Step 2: Store Dependencies

The generated struct needs a field to hold the vision service that Viam will inject.

Find the `inspectionModuleInspector` struct in `module.go` and add a `detector` field:

```go
type inspectionModuleInspector struct {
    resource.AlwaysRebuild

    name   resource.Name
    logger logging.Logger
    cfg    *Config

    cancelCtx  context.Context
    cancelFunc func()

    detector vision.Service  // Add this field
}
```

The `detector` field will hold a reference to the vision service.

Add the vision import to your import block:

```go
"go.viam.com/rdk/services/vision"
```

### Step 3: Wire Dependencies

The constructor extracts the vision service from the dependencies map and stores it in the struct. This validates that the vision service exists on the machine and that methods on that struct in the module we're writing have access to it.

Update `NewInspector` in `module.go`:

```go
func NewInspector(ctx context.Context, deps resource.Dependencies, name resource.Name, cfg *Config, logger logging.Logger) (resource.Resource, error) {
    cancelCtx, cancelFunc := context.WithCancel(context.Background())

    // --- Add this block ---
    detector, err := vision.FromProvider(deps, cfg.VisionService)
    if err != nil {
        return nil, fmt.Errorf("failed to get vision service %q: %w", cfg.VisionService, err)
    }
    // --- End add ---

    s := &inspectionModuleInspector{
        name:       name,
        logger:     logger,
        cfg:        cfg,
        cancelCtx:  cancelCtx,
        cancelFunc: cancelFunc,
        detector:   detector,  // Add this field
    }
    return s, nil
}
```

`vision.FromProvider` looks up the resource by name and returns it as the correct type. If the resource doesn't exist or isn't a vision service, it returns an error.

### Step 4: Add Detection Logic

Now add the internal method that performs inspection, and update `DoCommand` to expose it.

Add the `detect` method to `module.go` (lowercase—it's internal):

```go
func (s *inspectionModuleInspector) detect(ctx context.Context) (string, float64, error) {
    detections, err := s.detector.DetectionsFromCamera(ctx, s.cfg.Camera, nil)
    if err != nil {
        return "", 0, err
    }

    if len(detections) == 0 {
        return "NO_DETECTION", 0, nil
    }

    best := detections[0]
    for _, det := range detections[1:] {
        if det.Score() > best.Score() {
            best = det
        }
    }

    return best.Label(), best.Score(), nil
}
```

`DetectionsFromCamera` tells the vision service which camera to use. The vision service grabs an image, runs the ML model, and returns structured detection results. We find the highest-confidence detection and return its label and score.

Now update the generated `DoCommand` stub to dispatch to `detect`:

```go
func (s *inspectionModuleInspector) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    if _, ok := cmd["detect"]; ok {
        label, confidence, err := s.detect(ctx)
        if err != nil {
            return nil, err
        }
        return map[string]interface{}{
            "label":      label,
            "confidence": confidence,
        }, nil
    }
    return nil, fmt.Errorf("unknown command: %v", cmd)
}
```

`DoCommand` is the public API for generic services. External callers pass a command map, and the method dispatches to internal logic. This pattern keeps implementation details private while exposing a flexible interface.

### Step 5: Update the CLI

Now wire everything together in `cmd/cli/main.go` so we can test. This replaces the camera test code from section 3.2.

Replace the `realMain` function:

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

    cfg := &inspectionmodule.Config{
        Camera:        "inspection-cam",
        VisionService: "vision-service",
    }

    deps, err := vmodutils.MachineToDependencies(machine)
    if err != nil {
        return fmt.Errorf("failed to get dependencies: %w", err)
    }

    inspector, err := inspectionmodule.NewInspector(
        ctx,
        deps,
        generic.Named("inspector"),
        cfg,
        logger,
    )
    if err != nil {
        return fmt.Errorf("failed to create inspector: %w", err)
    }

    result, err := inspector.DoCommand(ctx, map[string]interface{}{"detect": true})
    if err != nil {
        return fmt.Errorf("detection failed: %w", err)
    }

    label := result["label"].(string)
    confidence := result["confidence"].(float64)
    logger.Infof("Detection: %s (%.1f%% confidence)", label, confidence*100)
    return nil
}
```

The CLI creates the inspector with dependencies from the remote machine, then calls `DoCommand` with `{"detect": true}`. This is the same pattern used in production Viam modules, where `DoCommand` is the public API for generic services.

Update the imports:

```go
import (
    "context"
    "flag"
    "fmt"

    "inspectionmodule"
    "github.com/erh/vmodutils"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/services/generic"
)
```

### Test Detection

Fetch dependencies and run:

```bash
go mod tidy
go run ./cmd/cli -host YOUR_MACHINE_ADDRESS
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

{{< expand "Troubleshooting" >}}
**"failed to connect" or timeout errors:**

- Verify your machine is online in the Viam app
- Check that you've run `viam login` successfully
- Confirm the host address is correct

**"failed to get vision service" error:**

- Verify `vision-service` exists in your machine config (Part 1)
- Check the exact name matches—it's case-sensitive

**"NO_DETECTION" result:**

- Normal if no can is in view—wait for one to appear
- Check the camera is working in the Viam app's Test panel
  {{< /expand >}}

{{< alert title="Checkpoint" color="success" >}}
You can now detect cans from your laptop. You declared dependencies in Config, returned them from Validate, and extracted them in the constructor. This pattern works for any Viam resource.
{{< /alert >}}

## 3.4 Summary

You built a complete inspection system using the module-first development pattern:

1. **Generated** the module scaffold—infrastructure handled, you focus on logic
2. **Connected** to remote hardware from local code using vmodutils
3. **Implemented detection** by calling the vision service and exposing results through `DoCommand`

{{< alert title="Extending the inspector" color="tip" >}}
In a production system, you could extend `DoCommand` to trigger actuators—for example, a motor that pushes defective cans off the belt. The same dependency injection pattern applies: declare the motor in Config, extract it in the constructor, and call it from your detection logic.
{{< /alert >}}

### What You Learned

| Concept                      | What It Means                                         | Where You'll Use It                      |
| ---------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| **Module-first development** | Test against real hardware without deploying          | Any time you're developing control logic |
| **Dependency injection**     | Declare what you need, let Viam provide it            | Every module you build                   |
| **DoCommand pattern**        | Expose functionality through a flexible map-based API | Any generic service                      |

### The Key Insight

Your inspector code doesn't know whether it's running from the CLI on your laptop or deployed as a module on the machine. It just uses the dependencies it's given. This abstraction is what makes rapid iteration possible during development and seamless deployment to production.

**Your code is ready.** In Part 4, you'll deploy it to run on the machine and configure data capture for the detection results.

**[Continue to Part 4: Deploy a Module →](../part-4/)**
