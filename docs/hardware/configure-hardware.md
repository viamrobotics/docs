---
linkTitle: "How components work"
title: "How components work"
weight: 1
layout: "docs"
type: "docs"
description: "Understand how Viam represents hardware, add components to your machine, and configure them."
date: "2025-03-07"
aliases:
  - /hardware-components/add-a-component/
  - /hardware/add-a-component/
---

Viam represents every piece of physical hardware on your machine as a
**component**.
Each component has three things:

- A **type** that defines what it can do: camera, motor, sensor, arm, and so on.
  Every component of the same type exposes the same API, regardless of the
  underlying hardware.
- A **model** that provides the driver for your specific hardware.
  For example, the camera type has models for USB webcams, IP cameras through
  FFmpeg, and others.
- **Attributes** that configure how the model talks to your hardware:
  a device path, a baud rate, a pin mapping, or whatever else the driver needs.

This abstraction means you can swap hardware without changing application code.
A program that captures images from a webcam works identically with an IP camera.
You change the model and attributes in configuration, not in your control logic.

## Models

When you add a component, you search for a **model** that matches your hardware. Models are drivers that know how to communicate with specific devices. Some models ship with `viam-server` (like `webcam` for USB cameras or `gpio` for motors wired to GPIO pins). Most hardware-specific models (arms, grippers, specialized sensors, motor controllers) come from **modules** in the [Viam registry](https://app.viam.com/registry).

You don't need to think about where a model comes from. The Viam app shows all available models in one search, and they all work the same way: same API, same data capture, same test sections, same SDKs.

If no model exists for your hardware, you can [write a driver module](/build-modules/write-a-driver-module/) that implements the Viam API for your device.

## Add a component

The process for adding any component is the same whether you're adding a motor,
a sensor, a board, or anything else. For step-by-step guides for specific
hardware, see [Add a component](/hardware/common-components/).

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.
If it shows as offline, verify that `viam-server` is running on your machine.

### 2. Add the component

1. Click the **+** button.
2. Select **Configuration block**.
3. Search for the model that matches your hardware (for example, "webcam", "gpio
   motor", "xArm6"). The search covers all available models and fragments.
4. Give your component a **name** and click **Create**. The name is how
   you reference it in code and configuration, so keep it short,
   descriptive, and unique on this machine.

### 3. Configure attributes

After creating the component, you'll see its configuration panel.
Every model has its own set of attributes. These settings tell the driver
how to communicate with your specific hardware.

Common attributes include:

- **Device paths** (for example, `/dev/video0`, `/dev/ttyUSB0`): which physical
  device to use.
- **Pin mappings**: which GPIO pins connect to the hardware.
- **Communication settings**: baud rate, I2C address, SPI bus.
- **Operational parameters**: resolution, speed limits, update frequency.

Check the model's reference page for the full list of attributes and their
defaults.
You can configure attributes using the form fields in the UI, or switch to
**JSON** mode to edit the configuration directly.

### 4. Set up dependencies (if needed)

Some components depend on other components.
For example:

- A **motor** may depend on a **board** for its GPIO pins.
- An **encoder** may depend on a **board** for its interrupt pins.
- A **sensor-controlled base** depends on a **base** and a **movement sensor**.

If your component depends on another, that other component must already exist in
your configuration. The model's reference page documents required dependencies.

### 5. Save the configuration

Click **Save** in the upper right of the configuration panel.

When you save, `viam-server` automatically reloads the configuration and
initializes the new component. You do not need to restart anything.

### 6. Test the component

Every component in Viam has a **test** section on its component card in the **CONFIGURE** tab. The test section uses the same API your code will use, so if the component works here, it will work in your programs.

1. Find your component in the configuration view.
2. Expand the **test** section at the bottom of the component card.
3. Interact with the component:
   - **Camera**: toggle the stream or capture an image.
   - **Motor**: set power or move to a position.
   - **Sensor**: view live readings.
   - **Servo**: move to an angle.
   - **Board**: read or set GPIO pin states.

If the test section shows expected results, your component is configured
correctly.

## Troubleshooting

{{< expand "Component not initializing (error in logs)" >}}

- Check the **LOGS** tab in the Viam app for error messages from `viam-server`.
- Verify that the device path or address in your attributes is correct.
- If the component depends on another (for example, a motor depends on a board),
  confirm the dependency is configured and working.

{{< /expand >}}

{{< expand "Model not appearing in the dropdown" >}}

- **Built-in models** appear automatically. If you don't see the expected model,
  confirm your `viam-server` version is up to date.
- **Module models** appear in the configuration block search alongside
  built-in models. If you don't see the model you expect, check that
  your search terms match the model or module name.

{{< /expand >}}

{{< expand "Test panel shows no data or errors" >}}

- Confirm the machine is **Live** in the Viam app.
- Check physical connections: cables, power, and wiring.
- Review attributes: wrong pin numbers, incorrect device paths, or typos in
  attribute names are common causes.
- Check the **LOGS** tab for specific error messages from the component.

{{< /expand >}}

## What's next

- [Add a component](/hardware/common-components/): step-by-step guides for
  each component type.
- [Capture and sync data](/data/capture-sync/capture-and-sync-data/): once your component
  works, start capturing its data to the cloud.
- [What is a module?](/build-modules/from-hardware-to-logic/): write code that
  reads from sensors and acts on what it finds.
