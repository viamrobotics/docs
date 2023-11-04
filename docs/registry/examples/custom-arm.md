---
title: "Create a Custom Arm Model"
linkTitle: "Custom Arm"
weight: 100
type: "docs"
description: "Implement your own robot arm driver. Code a module with the Go or Python SDKs that provides a custom model of arm as a modular resource."
tags:
  [
    "motor",
    "odrive",
    "canbus",
    "serial",
    "module",
    "modular resources",
    "Python",
    "python SDK",
    "CAN",
  ]
aliases:
  - "/extend/registry/examples/custom-arm/"
  - "/modular-resources/examples/custom-arm/"
# SMEs: Nicole Jung
---

The {{< glossary_tooltip term_id="rdk" text="RDK" >}} provides a number of built-in arm {{< glossary_tooltip term_id="model" text="models" >}} that implement the API protocol of the [arm](/components/arm/) {{< glossary_tooltip term_id="subtype" text="subtype" >}} of component, such as the `ur5e`, `xArm6`, and `xArm7`.

{{% alert title="Info" color="info" %}}

_Built-in_ models each have a software driver in the RDK.
For example, the `ur5e`'s driver is implemented in [`ur.go`](https://github.com/viamrobotics/rdk/blob/main/components/arm/universalrobots/ur.go) in the RDK.

Each of these models must also include a [kinematics file](/internals/kinematic-chain-config/), which specifies the relative [orientation](/internals/orientation-vector/) of links and joints in its kinematic chain.
Each built-in driver in the RDK includes a corresponding kinematics file located in the same directory as the driver.
For example, the `ur5e`'s kinematics file, [`ur5e.json`](https://github.com/viamrobotics/rdk/blob/main/components/arm/universalrobots/ur5e.json), is provided in the RDK in the same directory as its driver, `ur.go`.

See [Arm Configuration](/components/arm/#supported-models) for the current list of built-in models the RDK provides.

{{% /alert %}}

If you have a robot arm that is not already supported by the RDK, create a module that provides a customized model for your arm to [program](/program/) and control it with the [arm API](/components/arm/#api), or use it with [services](/services/) like [Motion](/services/motion/), just as you would with a built-in model.

See [Modular Resources](/registry/) for more information.

## Get your arm's kinematics file

The way arms move through space is more complicated than Viam's other [components](/components/).
Because of this, an arm, unlike other components, requires a [kinematic configuration file](/internals/kinematic-chain-config/) describing its geometry.
This provides the necessary information for the [frame system service](/services/frame-system/) and built-in [motion service](/services/motion/) to work with the arm.

**Find a pre-built kinematics file:**

- `viam-server` will work with <file>URDF</file> [(United Robot Description Format)](https://wiki.ros.org/urdf) kinematics files, which are currently the standard for ROS drivers.
  You can find <file>URDF</file> "robot descriptions" for many industrial robot arm models on GitHub that are compatible with the Viam platform.

**Create your own kinematics file:**

- Follow the instructions on [Configure Complex Kinematic Chains](/internals/kinematic-chain-config/) to write a file detailing the geometry of your arm.
  - Use the [Spatial Vector Algebra (SVA)](/internals/kinematic-chain-config/#kinematic-parameters) kinematic parameter type.
  - Define the parameters in a </file>.json</file> file.
  - Follow the frame system's guide to [Configure a Reference Frame](/services/frame-system/frame-config/) when working out the relative [orientations](/internals/orientation-vector/) of the `links` on your arm.
    You can view existing examples of the SVA and JSON format in Viam's [built-in arm drivers](https://github.com/viamrobotics/rdk/blob/main/components/arm).

Create a new directory.
Give it the name your want you call your custom {{< glossary_tooltip term_id="model" text="model" >}} of arm.
Save the JSON as <file>your-model-name.json</file> inside of this directory.
While completing the following step, make sure to save any new files that you generate inside of this same directory.

## Create a custom arm model as a modular resource

To create a custom arm model, code a module in Python with the module support libraries provided by [Viam's SDKs](/program/apis/):

1. [Code a new resource model](#code-a-new-resource-model) implementing all methods the Viam RDK requires in the API definition of its built-in {{< glossary_tooltip term_id="subtype" text="subtype" >}}, `rdk:component:arm`, which is available for reference [on GitHub](https://github.com/viamrobotics/rdk/blob/main/components/arm/arm.go).
   Import your custom model and API into the main program and register the new resource model with the Python SDK.

1. [Code a main program](#code-a-main-entry-point-program) that starts the module after adding your desired resources from the registry.
   This main program is the "entry point" to your module.

1. [Compile or package](#compile-the-module-into-an-executable) the module into a single executable that can receive a socket argument from `viam-server`, open the socket, and start the module at the entry point.

### Code a new resource model

{{% alert title="Info" color="info" %}}

This guide uses Viam's Python SDK to implement a custom arm module, but if you want to use the Go Client SDK, you can.
Follow [this guide](/registry/create/#code-a-new-resource-model) and select **Go** on the code samples to learn how to code a modular arm in Go.

{{% /alert %}}

Save the following two files, <file>my_modular_arm.py</file> and <file>\_\_init\_\_.py</file>, on your computer and edit the code as applicable.

This module template registers a modular resource implementing Viam's built-in [Arm API](/components/arm/#api) [(rdk:service:arm)](/registry/key-concepts/#models) as a new model, `"myarm"`:

- <file>my_modular_arm.py</file> implements a custom model of the arm component built-in resource, `"myarm"`.

    <details>
    <summary>Click to view sample code from <file>my_modular_arm.py</file></summary>

  ```python {class="line-numbers linkable-line-numbers"}
  import asyncio
  import os
  from typing import Any, ClassVar, Dict, Mapping, Optional, Tuple
  from typing_extensions import Self

  from viam.components.arm import Arm, JointPositions, KinematicsFileFormat, Pose
  from viam.operations import run_with_operation
  from viam.proto.app.robot import ComponentConfig
  from viam.proto.common import ResourceName
  from viam.resource.base import ResourceBase
  from viam.resource.types import Model, ModelFamily


  class MyModularArm(Arm):
      # Subclass the Viam Arm component and implement the required functions
      MODEL: ClassVar[Model] = Model(ModelFamily("acme", "demo"), "myarm")

      def __init__(self, name: str):
          # Starting joint positions
          self.joint_positions = JointPositions(values=[0, 0, 0, 0, 0, 0])
          super().__init__(name)

      @classmethod
      def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
          arm = cls(config.name)
          return arm

      async def get_end_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> Pose:
          raise NotImplementedError()

      async def move_to_position(self, pose: Pose, extra: Optional[Dict[str, Any]] = None, **kwargs):
          raise NotImplementedError()

      async def get_joint_positions(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> JointPositions:
          return self.joint_positions

      @run_with_operation
      async def move_to_joint_positions(self, positions: JointPositions, extra: Optional[Dict[str, Any]] = None, **kwargs):
          operation = self.get_operation(kwargs)

          self.is_stopped = False

          # Simulate the length of time it takes for the arm to move to its new joint position
          for x in range(10):
              await asyncio.sleep(1)

              # Check if the operation is cancelled and, if it is, stop the arm's motion
              if await operation.is_cancelled():
                  await self.stop()
                  break

          self.joint_positions = positions
          self.is_stopped = True

      async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
          self.is_stopped = True

      async def is_moving(self) -> bool:
          return not self.is_stopped

      async def get_kinematics(self, **kwargs) -> Tuple[KinematicsFileFormat.ValueType, bytes]:
          dirname = os.path.dirname(__file__)
          filepath = os.path.join(dirname, "./xarm6_kinematics.json")
          with open(filepath, mode="rb") as f:
              file_data = f.read()
          return (KinematicsFileFormat.KINEMATICS_FILE_FORMAT_SVA, file_data)
  ```

    </details><br>

- <file>\_\_init\_\_.py</file> registers the `my_modular_arm` custom model and API helper functions with the Python SDK.

    <details>
    <summary>Click to view sample code from <file>__init__.py</file></summary>

  ```python {class="line-numbers linkable-line-numbers"}
  from viam.components.arm import Arm
  from viam.resource.registry import Registry, ResourceCreatorRegistration
  from .my_modular_arm import MyModularArm


  Registry.register_resource_creator(Arm.SUBTYPE, MyModularArm.MODEL, ResourceCreatorRegistration(MyModularArm.new))
  ```

    </details>

{{% alert title="Info" color="info" %}}

The Python code for the custom model (<file>my_modular_arm.py</file>), resource registration file (<file>\_\_init\_\_.py</file>), and module entry point file (<file>main.py</file>) is adapted from the [Python SDK modular arm example](https://python.viam.dev/examples/example.html#custom-modular-arm-example).

{{% /alert %}}

### Code a main entry point program

<file>main.py</file> is the Python module's entry point file.
When executed, it initializes the `myarm` custom model and API helper functions from the registry.

<details>
<summary>Click to view sample code from <file>main.py</file></summary>

```python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.module.module import Module
from viam.components.arm import Arm

from .my_modular_arm import MyModularArm


async def main():
    """This function creates and starts a new module, after adding all desired
    resources. Resources must be pre-registered. For an example, see the
    `__init__.py` file.
    """

    module = Module.from_args()
    module.add_model_from_registry(Arm.SUBTYPE, MyModularArm.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

{{% alert title="Important" color="note" %}}

You must define all functions belonging to a built-in resource subtype's API if defining a new model.
Otherwise, the class won’t instantiate.

The best practice with the Python SDK is to put `pass` or raise an `NotImplementedError()` in the body of functions you don't want to implement.

{{% /alert %}}

### Compile the module into an executable

To [add a module](/registry/configure/) to the configuration of your robot, you need to have an [executable](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and cleanly exits when sent a termination signal.

Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

One option is to create and save a new shell script (<file>.sh</file>) that runs your module at your entry point (main program) file.

For example:

```sh { class="command-line" data-prompt="$"}
#!/bin/sh
cd `dirname $0`

exec python3 -m <your-module-directory-name>.<main-program-filename-without-extension> $@
```

This script uses exec to be able to ensure that termination signals reach the python process.
If you omit this, be sure to handle the forwarding of termination signals accordingly.

To make this shell script executable, run the following command in your terminal:

```sh { class="command-line" data-prompt="$"}
sudo chmod +x <FILEPATH>/<FILENAME>
```

Ensure any dependencies for your module (including the [Python SDK](https://python.viam.dev/)) are installed on your robot's computer.
Your executable will be run by `viam-server` as root, so dependencies need to be available to the root user.

## Configure the module and modular resource on your robot

Follow [these configuration instructions](/registry/configure/) to add your custom resource to your robot.
