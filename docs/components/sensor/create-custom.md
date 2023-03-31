---
title: "Create a Custom Sensor Model"
linkTitle: "custom model"
weight: 40
draft: false
type: "docs"
description: "Define a custom sensor model and build your robot with another type of sensor."
tags: ["sensor", "components"]
image: "/components/img/components/sensor.png"
imageAlt: "sensor"
# SME: #team-bucket
---

You can implement a model of sensor that is not natively supported by Viam by creating and registering your own model of a sensor resource.
This allows you to have the same access and control of the sensor through Viam as you would if it was already a registered model.

<<<<<<< HEAD
You have two options for doing so:
=======
<!-- TODO: Might delete second option if first option continues to go well -->
You have two options:

1. Use the Viam module system to create and expose a custom model as [a modular resource](/program/extend/modular-resources/) (Recommended)
<<<<<<< Updated upstream
2. Use a Viam SDK to subclass the sensor class to [create and register a custom model](/program/extend/sdk-as-server/) as a [remote](/manage/parts-and-remotes/)
=======
2. Use a Viam SDK to subclass the sensor class to [create and register a custom model](/program/extend/sdk-as-server/) as a [remote](/manage/parts-and-remotes/s)
>>>>>>> Stashed changes

## Create a Custom Sensor Model as a Modular Resource

1. Code a module in Go or Python that implements a new component in the `sensor` resource subtype and registers the component in the Viam RDK's [global registry of robotic parts](https://github.com/viamrobotics/rdk/blob/main/registry/registry.go).
2. Create a binary executable file that runs your module.
3. Save the module binary in a location where it can be accessed by the RDK.
4. Add a *module*, which is built from the module binary, to the configuration of your robot.
5. Add a sensor component referencing the custom sensor resource provided by the configured *module* to the configuration of your robot.

### Step 1: Code a module for your custom resource

{{%expand "Click to view Go Code" %}}

```json {class="line-numbers linkable-line-numbers"}

```

See [Github here](https://github.com/viamrobotics/rdk/tree/main/examples/customresources/models) for more examples of creating custom modular resources with Go.

{{% /expand%}}

{{%expand "Click to view Python Code" %}}

```python {class="line-numbers linkable-line-numbers"}

```

See [GitHub here](https://github.com/viamrobotics/viam-python-sdk/tree/main/examples/module) for more examples of creating custom modular resources with Python.

{{% /expand%}}

<!-- Example Repositories are available [here] (or link within individual examples) -->

### Step 2: Create a binary executable file that runs your module

1. Create the file:

```
#!/bin/sh
cd `dirname $0`

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec poetry run python -m src.main $@
```

2. Make it executable:

### Step 3: Save the binary in a location where it's accessible to the RDK

### Step 4: Add a module to the configuration of your robot

### Step 5: Add your custom sensor model to the configuration of your robot

```json {class="line-numbers linkable-line-numbers"}
{
  "components": [ ],
  "services": [
    {
      "name": "data_manager",
      "type": "data_manager",
      "attributes": {
        "sync_interval_mins": 0.1,
        "capture_dir": "/.viam/capture"
      }
    }
  ]
}
```

{{% /expand%}}

<!-- ## Create a Custom Sensor Model as a remote -->

Instructions can be found [here](https://github.com/viamrobotics/rdk/tree/main/examples/mysensor) <!-- TODO: also reference matt and i's tutorials in a next steps section here -->
## Next Steps
>>>>>>> a225a4e (changes)

1. Use a Viam SDK to subclass the sensor class to [create and register a custom model](/program/extend/sdk-as-server/)
3. Use the Viam module system to create and expose a custom model as [a modular resource](/program/extend/modular-resources/)

You can read more about sensor implementation in the [Python SDK Documentation](https://python.viam.dev/autoapi/viam/components/sensor/index.html) or the [Go SDK Documentation](https://pkg.go.dev/go.viam.com/rdk).

TODO: also reference matt and i's tutorials in a next steps section here
