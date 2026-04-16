---
linkTitle: "Machine configuration"
title: "Machine configuration"
weight: 10
layout: "docs"
type: "docs"
description: "Understand the JSON configuration that defines your machine's components, and how to edit it."
date: "2025-03-07"
aliases:
  - /hardware-components/configure-components/
  - /hardware/configure-components/
---

When you add components through the Viam app, you're building a JSON
configuration that tells `viam-server` what hardware is attached and how to
talk to it. Understanding this configuration structure helps you work faster.
You can edit JSON directly, copy configurations between machines, and debug
issues by reading the raw config.

## Configuration blocks

Every component in your machine's configuration is a JSON block with these
fields:

| Field        | What it does                                                                                       |
| ------------ | -------------------------------------------------------------------------------------------------- |
| `name`       | A unique name for this component on this machine. Your code references the component by this name. |
| `api`        | The component type, in the form `rdk:component:<type>` (for example, `rdk:component:arm`).         |
| `model`      | The specific driver, in the form `namespace:family:name` (for example, `viam:ufactory:xArm6`).     |
| `attributes` | Model-specific settings that control how to connect to the hardware and how it should behave.      |
| `depends_on` | Other components this one requires (for example, a motor depends on a board).                      |
| `frame`      | Optional spatial relationship to a parent component, used by the motion service.                   |

### Example: a motor controlled by a board

Here's a simple configuration with a Raspberry Pi board and a DC motor
connected to its GPIO pins:

```json
{
  "components": [
    {
      "name": "my-board",
      "api": "rdk:component:board",
      "model": "pi",
      "attributes": {}
    },
    {
      "name": "my-motor",
      "api": "rdk:component:motor",
      "model": "gpio",
      "attributes": {
        "pins": {
          "a": "13",
          "b": "15",
          "pwm": "12"
        },
        "board": "my-board"
      },
      "depends_on": ["my-board"]
    }
  ]
}
```

A few things to note:

- **The board** uses `pi`, a built-in model. No attributes are needed
  because the Pi's GPIO layout is known.
- **The motor** uses `gpio`, a built-in model for DC motors driven by
  GPIO pins. The `pins` attribute maps the motor's control wires to
  specific board pins.
- **`depends_on`** tells `viam-server` to initialize the board before
  the motor, since the motor needs the board's GPIO pins to function.

### Modules section

When you use a model from the [Viam registry](https://app.viam.com/registry)
(not built into `viam-server`), your configuration includes a `modules`
section that tells `viam-server` what to download:

| Field       | What it does                                                                           |
| ----------- | -------------------------------------------------------------------------------------- |
| `type`      | Always `"registry"` for modules from the Viam registry.                                |
| `name`      | A local name for the module (used in logs).                                            |
| `module_id` | The registry identifier, in the form `namespace:module-name`.                          |
| `version`   | The version to use. Use a specific version for production; `"latest"` for development. |

You don't need to write this JSON by hand. When you add a module model
through the Viam app, the modules section is created automatically.

## Editing configuration

You can edit your machine's configuration in two ways:

- **Builder UI**: the visual editor in the Viam app. Best for adding
  components one at a time and using form fields for attributes.
- **JSON mode**: click **JSON** in the left-hand menu on the CONFIGURE tab
  to see and edit the raw JSON. Best for copying configurations, making bulk
  changes, or understanding exactly what's configured.

Both views edit the same underlying configuration. Changes in one are
reflected in the other.

## Related

- [Add a component](/hardware/common-components/): find the right type and follow step-by-step guides for each component.
- [Fragments](/hardware/fragments/): save and reuse working configurations.
