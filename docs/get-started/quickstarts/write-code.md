---
title: "Control machines with code in 4 minutes"
linkTitle: "Write code for machines (4 min)"
type: "docs"
weight: 80
cost: 75
images: ["/general/code.png"]
description: "Write code to control your machine with Viam's SDKs in 4 minutes."
---

Follow this guide to start writing code to perform actions with the {{< glossary_tooltip term_id="component" text="components" >}} or {{< glossary_tooltip term_id="service" text="services" >}} of a {{< glossary_tooltip term_id="machine" text="machine" >}}.

{{<youtube embed_url="https://www.youtube-nocookie.com/embed/tzJf0XfUCmA">}}

## Requirements

- A computer with a supported OS installed: Linux 64-bit, macOS, Windows Subsystem for Linux (WSL)
- A physical component such as a motor or a camera that is connected to the computer

{{% expand "No computer you can run `viam-server` on?" %}}
No problem.
Use [Try Viam](https://app.viam.com/try) to rent a rover online which is already configured with some components to test with.
If you are using a Try Viam rover **start with Step 4**.
{{% /expand%}}

## Instructions

Follow these steps to configure your machine inside the Viam app and write code to control it:

{{< expand "Step 1: Create a machine" >}}

Go to the Viam app.
Select a location and [add a new machine](/cloud/machines/#add-a-new-machine).

![The 'First Location' page on the Viam app with a new machine name in the New machine field and the Add machine button next to the field highlighted.](/fleet/app-usage/create-machine.png)

{{< /expand >}}
{{< expand "Step 2: Install viam-server" >}}

Navigate to the **CONFIGURE** tab of your machine's page in the [Viam app](https://app.viam.com).
Follow the {{< glossary_tooltip term_id="setup" text="setup instructions" >}} that appear on your new machine's **CONFIGURE** page to install `viam-server` on your computer and connect it to the Viam app.

You can install `viam-server` on your personal computer, or on a single-board computer (SBC).
If you are using a microcontroller instead of a 64-bit computer, you can install a [lightweight version of `viam-server`](/get-started/installation/#install-micro-rdk).

{{< /expand >}}
{{< expand "Step 3: Configure a component or service">}}

Viam uses a composable system of building blocks called {{< glossary_tooltip term_id="resource" text="resources" >}} which you can combine according to your specific needs.
Components drive your hardware, and services provide high-level software functionality.

Click on the **+** icon to create a component or service.
If you are not sure what to add and your computer has a webcam attached, add a [`webcam`](/components/camera/webcam/).

These are the available components and services:

<div class="cards max-page"><div class="row"><div class="col sectionlist"><div><h3>Components:</h3><ul class="sectionlist"><li><a href="../../../components/arm/" title="Arm Component"><div><picture><img src="../../../icons/components/arm.svg" width="../../../icons/components/arm" height="../../../icons/components/arm" alt="Arm" loading="lazy"></picture><p>Arm</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/base/" title="Base Component"><div><picture><img src="../../../icons/components/base.svg" width="../../../icons/components/base" height="../../../icons/components/base" alt="Base" loading="lazy"></picture><p>Base</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/board/" title="Board Component"><div><picture><img src="../../../icons/components/board.svg" width="../../../icons/components/board" height="../../../icons/components/board" alt="Board" loading="lazy"></picture><p>Board</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/camera/" title="Camera Component"><div><picture><img src="../../../icons/components/camera.svg" width="../../../icons/components/camera" height="../../../icons/components/camera" alt="Camera" loading="lazy"></picture><p>Camera</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/encoder/" title="Encoder Component"><div><picture><img src="../../../icons/components/encoder.svg" width="../../../icons/components/encoder" height="../../../icons/components/encoder" alt="Encoder" loading="lazy"></picture><p>Encoder</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/gantry/" title="Gantry Component"><div><picture><img src="../../../icons/components/gantry.svg" width="../../../icons/components/gantry" height="../../../icons/components/gantry" alt="Gantry" loading="lazy"></picture><p>Gantry</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/generic/" title="Generic Component"><div><picture><img src="../../../icons/components/generic.svg" width="../../../icons/components/generic" height="../../../icons/components/generic" alt="Generic" loading="lazy"></picture><p>Generic</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/gripper/" title="Gripper Component"><div><picture><img src="../../../icons/components/gripper.svg" width="../../../icons/components/gripper" height="../../../icons/components/gripper" alt="Gripper" loading="lazy"></picture><p>Gripper</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/input-controller/" title="Input Controller Component"><div><picture><img src="../../../icons/components/controller.svg" width="../../../icons/components/controller" height="../../../icons/components/controller" alt="Input Controller" loading="lazy"></picture><p>Input Controller</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/motor/" title="Motor Component"><div><picture><img src="../../../icons/components/motor.svg" width="../../../icons/components/motor" height="../../../icons/components/motor" alt="Motor" loading="lazy"></picture><p>Motor</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/movement-sensor/" title="Movement Sensor Component"><div><picture><img src="../../../icons/components/imu.svg" width="../../../icons/components/imu" height="../../../icons/components/imu" alt="Movement Sensor" loading="lazy"></picture><p>Movement Sensor</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/power-sensor/" title="Power Sensor Component"><div><picture><img src="../../../icons/components/power-sensor.svg" width="../../../icons/components/power-sensor" height="../../../icons/components/power-sensor" alt="Power Sensor" loading="lazy"></picture><p>Power Sensor</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/sensor/" title="Sensor Component"><div><picture><img src="../../../icons/components/sensor.svg" width="../../../icons/components/sensor" height="../../../icons/components/sensor" alt="Sensor" loading="lazy"></picture><p>Sensor</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../components/servo/" title="Servo Component"><div><picture><img src="../../../icons/components/servo.svg" width="../../../icons/components/servo" height="../../../icons/components/servo" alt="Servo" loading="lazy"></picture><p>Servo</p></div></a></li></ul></div></div><div class="col sectionlist"><div><h3>Services:</h3><ul class="sectionlist"><li><a href="../../../services/data/" title="Data Management Service"><div><picture><img src="../../../services/icons/data-capture.svg" alt="Data Management" loading="lazy"></picture><p>Data Management</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/motion/" title="Motion Service"><div><picture><img src="../../../services/icons/motion.svg" alt="Motion" loading="lazy"></picture><p>Motion</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/frame-system/" title="The Robot Frame System"><div><picture><img src="../../../services/icons/frame-system.svg" alt="Frame System" loading="lazy"></picture><p>Frame System</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/base-rc/" title="Base Remote Control Service"><div><picture><img src="../../../services/icons/base-rc.svg" alt="Base Remote Control" loading="lazy"></picture><p>Base Remote Control</p></div></a></li></ul><ul class="sectionlist"><li><a href="/services/ml/" title="ML Model Service"><div><picture><img src="../../../services/icons/ml.svg" alt="ML Model" loading="lazy"></picture><p>ML Model</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/navigation/" title="The Navigation Service"><div><picture><img src="../../../services/icons/navigation.svg" alt="Navigation" loading="lazy"></picture><p>Navigation</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/slam/" title="SLAM Service"><div><picture><img src="../../../services/icons/slam.svg" alt="SLAM" loading="lazy"></picture><p>SLAM</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/vision/" title="Vision Service"><div><picture><img src="../../../services/icons/vision.svg" alt="Vision" loading="lazy"></picture><p>Vision</p></div></a></li></ul><ul class="sectionlist"><li><a href="../../../services/generic/" title="Generic Service"><div><picture><img src="../../../icons/components/generic.svg" alt="Generic" loading="lazy"></picture><p>Generic</p></div></a></li></ul></div></div></div></div>

If you are unsure how to configure your [component](/components/) or a [service](/services/), follow the instructions in the model's documentation to configure any required attributes.

For more information, see [configuration](/configure/).

{{< /expand >}}
{{< expand "Step 4: Copy the sample code" >}}

Viam's APIs are standardized across all models of a given component or service.
This means you can test and change hardware without changing code.

After configuring your resource, navigate to your machine's **CONNECT** tab.
Click on any of the listed languages and follow the instructions to install the SDK.

To install your preferred Viam SDK on your Linux or macOS development machine or [single-board computer](/components/board/), run one of the following commands in your terminal:

{{< tabs >}}
{{% tab name="Python" %}}

If you are using the Python SDK, [set up a virtual environment](/sdks/python/python-venv/) to package the SDK inside before running your code, avoiding conflicts with other projects or your system.

For macOS (both Intel `x86_64` and Apple Silicon) or Linux (`x86`, `aarch64`, `armv6l`), run the following commands:

```sh {class="command-line" data-prompt="$"}
python3 -m venv .venv
source .venv/bin/activate
pip install viam-sdk
```

Windows is not supported.
If you are using Windows, use the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install) and install the Python SDK using the preceding instructions for Linux.
For other unsupported systems, see [Installing from source](https://python.viam.dev/#installing-from-source).

If you intend to use the [ML (machine learning) model service](/services/ml/), use the following command instead, which installs additional required dependencies along with the Python SDK:

```sh {class="command-line" data-prompt="$"}
pip install 'viam-sdk[mlmodel]'
```

{{% /tab %}}
{{% tab name="Go" %}}

```sh {class="command-line" data-prompt="$"}
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{% tab name="TypeScript" %}}

```sh {class="command-line" data-prompt="$"}
npm install @viamrobotics/sdk
```

{{< alert title="Info" color="info" >}}
The TypeScript SDK currently only supports building web browser apps.
{{< /alert >}}

{{% /tab %}}
{{% tab name="C++" %}}

Follow the [instructions on the GitHub repository](https://github.com/viamrobotics/viam-cpp-sdk/blob/main/BUILDING.md).

{{% /tab %}}
{{% tab name="Flutter" %}}

```sh {class="command-line" data-prompt="$"}
flutter pub add viam_sdk
```

{{% /tab %}}
{{< /tabs >}}

Then copy and run the sample code to connect to your machine.

The sample code will show you how to authenticate and connect to a machine, as well as some of the methods you can use on your configured components and services.

{{< /expand >}}

## Next steps

Now that you have run code to control your machine, see [Component APIs](/appendix/apis/#component-apis) and [Service APIs](/appendix/apis/#service-apis) for a full list of available API methods.

To run your code as a process on your machine whenever it boots, see [Processes](/configure/processes/#configure-a-process).

To see full sample projects, check out these tutorials:

{{< cards >}}
{{% card link="/tutorials/get-started/blink-an-led/" %}}
{{% card link="/get-started/quickstarts/drive-rover/" %}}
{{< /cards >}}

If you are looking to write code to support additional components or services or add custom functionality, see [how to create a module](/use-cases/create-module/).
