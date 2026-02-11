---
linkTitle: "Part 3: Control Logic"
title: "Part 3: Control Logic"
weight: 30
layout: "docs"
type: "docs"
description: "Write inspection logic and run it against remote hardware from your laptop."
date: "2025-01-30"
---

**Goal:** Write inspection logic and run it against remote hardware from your laptop.

**Skills:** Write code against remote hardware, connect to a machine over the network, iterate rapidly without deploying, call a built-in service from code.

**Time:** ~10 min

## What You'll Build

Your vision pipeline detects defective cans and your data capture records the results.
Now you'll write the inspection logic that calls the vision service and exposes detection results through `DoCommand`.
This detection data can drive dashboards, alerts, or—in a production system—trigger actuators to reject defective cans.

You'll use the **module-first development pattern**: write code on your laptop, run it against real hardware over the network, and see results in seconds.
No deploying, no SSH, no waiting.
When the code is ready, it deploys to the machine without changes.

## Prerequisites

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
The Viam CLI (`viam`) is different from `viam-server`.
The CLI runs on your development machine; `viam-server` runs on your robot/machine.
{{< /alert >}}

### Language Setup

{{< tabs >}}
{{% tab name="Python" %}}

**Install Python:**

Check your Python version:

```bash
python3 --version
```

You need Python 3.8 or later.
If Python isn't installed or is outdated, download it from [python.org](https://www.python.org/downloads/).

**Create an API key:**

The Python SDK authenticates with API keys (it does not support CLI token authentication).
Create one now:

1. In the Viam app, click your machine's name to go to its page
2. Click the **API keys** tab
3. Click **Generate key**
4. Copy the **API key** and **API key ID**

Set the environment variables in your terminal:

```bash
export VIAM_API_KEY="your-api-key"
export VIAM_API_KEY_ID="your-api-key-id"
```

{{< alert title="Tip" color="tip" >}}
Add these exports to your shell profile (`.bashrc`, `.zshrc`) so they persist across terminal sessions.
{{< /alert >}}

**Clone the starter repo:**

```bash
git clone https://github.com/viamrobotics/inspection-module-starter-python.git
cd inspection-module-starter-python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate the virtual environment with `venv\Scripts\activate` instead.

This repo contains a pre-built module with one method left for you to implement.

{{% /tab %}}
{{% tab name="Go" %}}

**Install Go:**

Check your Go version:

```bash
go version
```

You need Go 1.21 or later.
If Go isn't installed or is outdated, download it from [go.dev/dl](https://go.dev/dl/).

**Clone the starter repo:**

```bash
git clone https://github.com/viamrobotics/inspection-module-starter.git
cd inspection-module-starter
go mod tidy
```

This repo contains a pre-built module with one method left for you to implement.

{{% /tab %}}
{{< /tabs >}}

## 3.1 Why Start with a Module?

Viam development starts with modules, not scripts.
A **module** is a package of code that adds capabilities to a machine—custom components, services, or in this case, inspection logic.
By writing your code as a module from the start, the same code runs locally during development and on the machine in production.
There's no restructuring when you're ready to deploy.

This matters because the traditional embedded development loop—edit, build, deploy, test, repeat—is slow.
With a module, you edit code on your laptop, run it locally against remote hardware, and see results immediately.
The iteration cycle drops from minutes to seconds.

The starter repo includes everything you need: the module implementation, a deployment entry point, and a CLI for testing against remote hardware.
You'll implement one method, test it, iterate on it, and move on.
This is the development workflow you're used to, applied to physical devices.

## 3.2 Explore the Starter Module

Before writing code, walk through what the starter repo provides.
You won't modify any of these files in this section—just read them to understand the structure.

### Service implementation

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/inspector.py`. The key parts:

**validate_config** declares the resources your inspector needs and returns them as dependencies:

```python
@classmethod
def validate_config(
    cls, config: ComponentConfig
) -> Tuple[Sequence[str], Sequence[str]]:
    fields = config.attributes.fields
    if "camera" not in fields or not fields["camera"].string_value:
        raise Exception("camera is required")
    if "vision" not in fields or not fields["vision"].string_value:
        raise Exception("vision is required")
    return [fields["camera"].string_value, fields["vision"].string_value], []
```

The first element of the returned tuple lists required dependencies—Viam ensures these resources exist before creating your service.

**reconfigure** wires the vision service by extracting it from the injected dependencies:

```python
vision_resource_name = VisionClient.get_resource_name(vision_name)
self.detector = cast(VisionClient, dependencies[vision_resource_name])
```

Your code declares what it needs in `validate_config`, and Viam provides it through dependency injection.
This means the same code works whether dependencies come from a remote machine (during development) or from viam-server (in production).

**do_command** dispatches to `detect`, the method you'll implement:

```python
async def do_command(self, command, **kwargs):
    if "detect" in command:
        label, confidence = await self.detect()
        return {"label": label, "confidence": confidence}
    raise Exception(f"unknown command: {command}")
```

`do_command` is the public API for generic services.
External callers pass a command dict, and the method dispatches to internal logic.
This pattern keeps implementation details private while exposing a flexible interface.

**The stub:** `detect()` currently raises an error:

```python
async def detect(self) -> Tuple[str, float]:
    raise NotImplementedError("not implemented: fill in the detect method")
```

This is what you'll implement in the next section.

{{% /tab %}}
{{% tab name="Go" %}}

Open `module.go`. The key parts:

**Config** declares the resources your inspector needs—a camera and a vision service:

```go
type Config struct {
    Camera        string `json:"camera"`
    VisionService string `json:"vision"`
}
```

**Validate** returns these as dependencies so Viam injects them before creating your service:

```go
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

**NewInspector** wires the vision service by extracting it from the injected dependencies:

```go
detector, err := vision.FromProvider(deps, cfg.VisionService)
```

Your code declares what it needs in Config, and Viam provides it through dependency injection.
This means the same code works whether dependencies come from a remote machine (during development) or from viam-server (in production).

**DoCommand** dispatches to `detect`, the method you'll implement:

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

`DoCommand` is the public API for generic services.
External callers pass a command map, and the method dispatches to internal logic.
This pattern keeps implementation details private while exposing a flexible interface.

**The stub:** `detect()` currently returns an error:

```go
func (s *inspectionModuleInspector) detect(ctx context.Context) (string, float64, error) {
    return "", 0, fmt.Errorf("not implemented: fill in the detect method")
}
```

This is what you'll implement in the next section.

{{% /tab %}}
{{< /tabs >}}

### CLI

{{< tabs >}}
{{% tab name="Python" %}}

The CLI (`cli.py`) connects to your remote machine and runs the inspector against it.
It:

1. Accepts a `--host` argument for your machine's address
2. Reads `VIAM_API_KEY` and `VIAM_API_KEY_ID` from environment variables
3. Connects using `RobotClient.Options.with_api_key()`
4. Builds dependencies from the remote machine's resources
5. Creates an inspector instance and calls `do_command({"detect": True})`

{{< alert title="Resource names" color="info" >}}
The CLI hardcodes the camera and vision service names (`inspection-cam` and `can-detector`).
These must match the names you configured in Part 1.
If you used different names, update the `config` in `cli.py` before running.
{{< /alert >}}

{{% /tab %}}
{{% tab name="Go" %}}

The CLI (`cmd/cli/main.go`) connects to your remote machine and runs the inspector against it.
It:

1. Accepts a `-host` flag for your machine's address
2. Uses your `viam login` credentials to authenticate through `vmodutils.ConnectToHostFromCLIToken`
3. Converts the machine connection into dependencies your inspector can use
4. Creates an inspector instance and calls `DoCommand({"detect": true})`

{{< alert title="Resource names" color="info" >}}
The CLI hardcodes the camera and vision service names (`inspection-cam` and `can-detector`).
These must match the names you configured in Part 1.
If you used different names, update the `cfg` struct in `cmd/cli/main.go` before running.
{{< /alert >}}

{{% /tab %}}
{{< /tabs >}}

### Module entry point

{{< tabs >}}
{{% tab name="Python" %}}

`src/main.py` is the module entry point for deployment.
When your module runs on the machine, this file registers your service with viam-server through `Module.run_from_registry()`.
You won't modify this file.

{{% /tab %}}
{{% tab name="Go" %}}

`cmd/module/main.go` is the module entry point for deployment.
When your module runs on the machine, this file registers your service with viam-server.
You won't modify this file.

{{% /tab %}}
{{< /tabs >}}

## 3.3 Implement Detection

{{< tabs >}}
{{% tab name="Python" %}}

Open `src/models/inspector.py` and find the `detect` method stub. Replace it with:

```python
async def detect(self) -> Tuple[str, float]:
    detections = await self.detector.get_detections_from_camera(self.camera_name)

    if len(detections) == 0:
        return ("NO_DETECTION", 0.0)

    best = max(detections, key=lambda d: d.confidence)
    return (best.class_name, best.confidence)
```

`get_detections_from_camera` tells the vision service which camera to use.
The vision service grabs an image, runs the ML model, and returns structured detection results.
Python's `max()` with a `key` function finds the highest-confidence detection.

{{% /tab %}}
{{% tab name="Go" %}}

Open `module.go` and find the `detect` method stub. Replace it with:

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

`DetectionsFromCamera` tells the vision service which camera to use.
The vision service grabs an image, runs the ML model, and returns structured detection results.
The code finds the highest-confidence detection and returns its label and score.

{{% /tab %}}
{{< /tabs >}}

### Run it

1. In the Viam app, go to your machine's **Configure** page
2. Click the **Online** dropdown
3. Click **Remote address** to copy your machine address

   {{<imgproc src="/tutorials/first-project/machine-address.png" resize="x1100" declaredimensions=true alt="Live dropdown showing Remote address option with machine address visible." class="imgzoom shadow">}}

4. Run:

{{< tabs >}}
{{% tab name="Python" %}}

   ```bash
   python cli.py --host YOUR_MACHINE_ADDRESS
   ```

{{% /tab %}}
{{% tab name="Go" %}}

   ```bash
   go run ./cmd/cli -host YOUR_MACHINE_ADDRESS
   ```

{{% /tab %}}
{{< /tabs >}}

   You should see:

   ```text
   Connecting to your-machine-main.abc123.viam.cloud...
   Detection: PASS (94.2% confidence)
   ```

   Run it several times—results change as different cans pass under the camera.

{{< alert title="What just happened" color="info" >}}
Your laptop connected to the remote machine, your code called the vision service, and the vision service ran ML inference on an image from the camera.
The code runs locally but uses remote hardware—this is the module-first pattern in action.
{{< /alert >}}

{{< expand "Troubleshooting" >}}
**"failed to connect" or timeout errors:**

- Verify your machine is online in the Viam app
- Confirm the host address is correct
- **Go:** Check that you've run `viam login` successfully
- **Python:** Verify `VIAM_API_KEY` and `VIAM_API_KEY_ID` are set (`echo $VIAM_API_KEY`)

**"failed to get vision service" or "not found in dependencies" error:**

- Verify the vision service name in your CLI file matches your machine config from Part 1
- Check the exact name—it's case-sensitive

**"NO_DETECTION" result:**

- Normal if no can is in view—wait for one to appear
- Check the camera is working in the Viam app's Test panel

**Python: ModuleNotFoundError or ImportError:**

- Verify your virtual environment is activated (`source venv/bin/activate`)
- Verify dependencies are installed (`pip install -r requirements.txt`)
- Run from the repo root directory
{{< /expand >}}

## 3.4 Iterate — Filter for Failures

Your inspector reports every detection—PASS and FAIL.
In an inspection system, you often only care about failures.
Let's filter for them.

{{< tabs >}}
{{% tab name="Python" %}}

In `src/models/inspector.py`, add a check after finding the highest-confidence detection. Insert these lines just before the final `return` in `detect`:

```python
    # Only report failures — treat PASS as no detection
    if best.class_name != "FAIL":
        return ("NO_DETECTION", 0.0)
```

Run again:

```bash
python cli.py --host YOUR_MACHINE_ADDRESS
```

{{% /tab %}}
{{% tab name="Go" %}}

In `module.go`, add a check after finding the highest-confidence detection. Insert these lines just before the final `return` in `detect`:

```go
    // Only report failures — treat PASS as no detection
    if best.Label() != "FAIL" {
        return "NO_DETECTION", 0, nil
    }
```

Run again:

```bash
go run ./cmd/cli -host YOUR_MACHINE_ADDRESS
```

{{% /tab %}}
{{< /tabs >}}

Now it only flags defective cans.
PASS detections are treated as no detection.

Edit, run, see results on real hardware—seconds, not minutes.
This is the rapid iteration loop that module-first development gives you.

Before continuing to Part 4, **remove the filter** so the inspector reports all detections. Delete the filter block you just added, leaving the method as it was after section 3.3.

## 3.5 Summary

You wrote inspection logic and ran it against remote hardware from your laptop:

1. **Connected** to a remote machine over the network—no VPN, no SSH
2. **Implemented detection** by calling a built-in vision service from code
3. **Iterated rapidly** by editing and re-running—seconds, not minutes
4. **Used the module-first pattern**—the same code deploys to the machine without changes

### What You Learned

| Concept                      | What It Means                                         | Where You'll Use It                      |
| ---------------------------- | ----------------------------------------------------- | ---------------------------------------- |
| **Remote development**       | Code on your laptop talks to real hardware             | Any time you're developing control logic |
| **Module-first development** | Same code works in dev and production                  | Every module you build                   |
| **Dependency injection**     | Declare what you need, let Viam provide it            | Every module you build                   |
| **DoCommand pattern**        | Expose functionality through a flexible map-based API | Any generic service                      |

### The Key Insight

Your inspector code doesn't know whether it's running from the CLI on your laptop or deployed as a module on the machine.
It just uses the dependencies it's given.
This abstraction is what makes rapid iteration possible during development and seamless deployment to production.

**Your code is ready.**
In Part 4, you'll deploy it to run on the machine and configure data capture for the detection results.

**[Continue to Part 4: Deploy a Module →](../part-4/)**
