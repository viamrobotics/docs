---
title: "Part 2: Choose an API and generate code"
linkTitle: "Part 2: Choose API"
weight: 32
layout: "docs"
type: "docs"
description: "Select the right Viam API for your hardware and generate your module code structure."
---

**Part 2 of 5** | ⏱️ 15 minutes

## What you'll do in this part

- Understand how modules map hardware to Viam APIs
- Choose the right API for your hardware
- Generate module code using the Viam CLI
- Understand the generated file structure

## Choose an API

A module wraps your hardware driver in a standardized Viam API. This means:
- Your hardware works seamlessly with all Viam SDKs
- You can use Viam services (vision, data capture, etc.)
- Configuration is consistent across all components

### How to choose

You can think of a module as a packaged wrapper around a script. The module takes the functionality of the script and maps it to a standardized API for use within the Viam ecosystem.

Review the available [component APIs](/dev/reference/apis/#component-apis) and choose the one whose methods map most closely to the functionality you need.

If you need a method that is not in your chosen API, you can use the flexible `DoCommand` (which is built into all component APIs) to create custom commands. See [Run control logic](/operate/modules/control-logic/) for more information.

### Hardware-to-API mapping guide

| Hardware Type | Viam API | When to Use | Example Devices | Key Methods |
|---------------|----------|-------------|-----------------|-------------|
| **Image capture** | [Camera](/dev/reference/apis/components/camera/) | Captures still images or video streams | Webcam, Raspberry Pi Camera, RTSP stream, CV pipeline | `GetImages`, `GetPointCloud` |
| **Measurement sensor** | [Sensor](/dev/reference/apis/components/sensor/) | Reads numeric values or data | Temperature, IMU, distance, air quality, GPS | `GetReadings` |
| **Single motor** | [Motor](/dev/reference/apis/components/motor/) | Controls one motor independently | DC motor, stepper motor, servo | `SetPower`, `GoTo`, `GetPosition` |
| **Multi-motor platform** | [Base](/dev/reference/apis/components/base/) | Coordinated control of multiple motors | Rover, mobile robot, wheeled platform | `MoveStraight`, `Spin`, `SetVelocity` |
| **Robotic arm** | [Arm](/dev/reference/apis/components/arm/) | Multi-joint arm with kinematics | Robot arm, manipulator | `MoveToPosition`, `MoveToJointPositions` |
| **Other hardware** | [Generic](/dev/reference/apis/components/generic/) | Doesn't fit standard categories | Custom actuators, unique hardware | `DoCommand` only |

### Decision process

**Step 1:** Identify your hardware's primary function

**Step 2:** Check if an existing API provides the methods you need
- [Full API reference](/dev/reference/apis/#component-apis)
- Each API has specific methods designed for that type of hardware

**Step 3:** For multiple functions, create multiple models
- Each model implements one API
- One module can contain many models
- You'll learn how to do this in [Part 5](/operate/modules/support-hardware/part-5-multiple-models/)

### Example: The hello-world module

**Hardware capabilities:**
1. Returns an image from a file path
2. Returns a random number

**API mapping:**
1. Image retrieval → [Camera API](/dev/reference/apis/components/camera/) (`GetImages` method)
2. Number reading → [Sensor API](/dev/reference/apis/components/sensor/) (`GetReadings` method)

**Result:** Two models in one module

{{< alert title="Can't decide?" color="note" >}}
Start with the Generic API and migrate later if needed. You're not locked into your initial choice.
{{< /alert >}}

## Generate module code

Use the [Viam CLI](/dev/tools/cli/) to generate template files for your module. You can work on your module either on the device running `viam-server` or on another computer.

### Run the generator

Run the `module generate` command in your terminal:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate
```

The CLI will prompt you for several configuration options:

{{< expand "Understanding each prompt" >}}

| Prompt | Description | Example |
| -------| ----------- | ------- |
| **Module name** | Choose a name that describes the set of {{< glossary_tooltip term_id="resource" text="resources" >}} it supports | `hello-world` |
| **Language** | Choose the programming language for the module: `Python` or `Golang` | `Python` |
| **Visibility** | Choose `Private` to share only with your organization, or `Public` to share publicly with all organizations | `Private` (for testing) |
| **Namespace/Organization ID** | Navigate to your organization settings through the menu in the upper-right corner of the page. Find the **Public namespace** (or create one if you haven't already) and copy that string | `exampleorg` |
| **Resource to add** | The [component API](/dev/reference/apis/#component-apis) your module will implement | `camera` |
| **Model name** | Name your component model based on what it supports. Must be all-lowercase and use only alphanumeric characters (`a-z` and `0-9`), hyphens (`-`), and underscores (`_`) | `hello-camera` |
| **Enable cloud build** | If you select `Yes` (recommended) and push the generated files (including the <file>.github</file> folder) to GitHub and create a release of the format `X.X.X`, the module will build for all architectures | `Yes` |
| **Register module** | Select `Yes` unless you're creating a local-only module for testing purposes | `Yes` |

{{< /expand >}}

### Example command

For the hello-world module, you can skip the interactive prompts by providing all options on the command line:

{{< tabs >}}
{{% tab name="Python" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language python --model-name hello-camera \
  --name hello-world --resource-subtype=camera --public false \
  --enable-cloud true
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate --language go --model-name hello-camera \
  --name hello-world --resource-subtype=camera --public false \
  --enable-cloud true
```

{{% /tab %}}
{{< /tabs >}}

{{< alert title="Note" color="note" >}}
The CLI only supports generating code for one model at a time. You'll add the sensor model in [Part 5](/operate/modules/support-hardware/part-5-multiple-models/).
{{< /alert >}}

## Understand the generated files

The generator creates a directory containing stub files for your modular component. Here's what you need to know about each file:

{{< tabs >}}
{{% tab name="Python" %}}

```treeview
hello-world/
└── src/
|   ├── models/
|   |   └── hello_camera.py
|   └── main.py
└── README.md
└── <org-id>_hello-world_hello-camera.md
└── build.sh
└── meta.json
└── requirements.txt
└── run.sh
└── setup.sh
```

### 📝 Files you'll actively edit

These are where your main work happens:

**`src/models/hello_camera.py`**
- Your hardware control logic goes here
- Implement API methods (`GetImages`, etc.)
- Add configuration validation
- **This is your primary workspace**

**`requirements.txt`**
- List Python package dependencies
- Installed automatically by `setup.sh`
- Example: Add `Pillow` for image processing

**`README.md`** and **`<org-id>_hello-world_hello-camera.md`**
- Module and model documentation
- Shows in the Viam registry
- Helps users configure your module

### ⚙️ Files you'll occasionally edit

**`meta.json`**
- Module metadata
- Entrypoint configuration
- Build settings
- Edit when: Adding models, changing description, configuring builds

**`src/main.py`**
- Registers models with viam-server
- Edit when: Adding new models to existing module

### 🤖 Generated/managed files (usually don't edit)

**`setup.sh`, `build.sh`, `run.sh`**
- Build and execution scripts
- Generated by CLI
- Edit only for custom build requirements

**`.github/workflows/build.yml`**
- GitHub Actions for cloud build
- Auto-uploads module on release
- Edit only to customize CI/CD

{{% /tab %}}
{{% tab name="Go" %}}

```treeview
hello-world/
└── cmd/
|   ├── cli/
|   |   └── main.go
|   └── module/
|       └── main.go
└── Makefile
└── README.md
└── <org-id>_hello-world_hello-camera.md
└── go.mod
└── module.go
└── meta.json
```

### 📝 Files you'll actively edit

**`module.go`**
- Your hardware control logic goes here
- Implement API methods (`Images`, etc.)
- Add configuration validation
- **This is your primary workspace**

**`README.md`** and **`<org-id>_hello-world_hello-camera.md`**
- Module and model documentation
- Shows in the Viam registry
- Helps users configure your module

### ⚙️ Files you'll occasionally edit

**`meta.json`**
- Module metadata
- Entrypoint configuration
- Build settings
- Edit when: Adding models, changing description

**`cmd/module/main.go`**
- Registers models with viam-server
- Edit when: Adding new models to existing module

### 🤖 Generated/managed files (usually don't edit)

**`cmd/cli/main.go`**
- Test runner for local development
- Run with: `go run ./cmd/cli`

**`Makefile`**
- Build and setup commands
- Generated by CLI

**`go.mod`**
- Go module dependencies
- Managed by Go toolchain

**`.github/workflows/build.yml`**
- GitHub Actions for cloud build
- Auto-uploads module on release

{{% /tab %}}
{{< /tabs >}}

💡 **Getting started tip:** Focus on the main model file (`hello_camera.py` or `module.go`). Everything else can wait until you need it.

## What you've accomplished

✅ **API selected:**
- Understand how hardware maps to Viam APIs
- Chosen the right API for your hardware (Camera for the example)

✅ **Module generated:**
- Created module structure with CLI
- Understand what each file does
- Know which files to edit first

✅ **Ready to code:**
- Have a working module scaffold
- Ready to implement API methods

## Next steps

Now that you have your module structure, continue to [Part 3: Implement your module](/operate/modules/support-hardware/part-3-implement-single-model/) to write the code that makes your hardware work.

---

**Tutorial navigation:**
- **Previous:** [← Part 1: Prerequisites and setup](/operate/modules/support-hardware/part-1-prerequisites-setup/)
- **Current:** Part 2: Choose an API and generate code
- **Next:** [Part 3: Implement your module →](/operate/modules/support-hardware/part-3-implement-single-model/)
- **All parts:** [Module creation tutorial](/operate/modules/support-hardware/)
