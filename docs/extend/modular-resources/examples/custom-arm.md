---
title: "Create a custom Arm model"
linkTitle: "Custom Arm"
weight: 40
type: "docs"
description: "Implement your own robot arm driver. Code a module with the Go or Python SDKs that provides a custom model of arm as a modular resource."
tags: ["motor", "odrive", "canbus", "serial", "module", "modular resources", "Python", "python SDK", "CAN"]
# SMEs: Nicole Jung
---

The RDK provides a number of built-in {{< glossary_tooltip term_id="model" text="models" >}} that implement the API protocol of the [arm](/components/arm) subtype of component, such as the `ur5e`, `xArm6`, and `xArm7`.

{{% alert title="Info" color="info" %}}

*Built-in* indicates each of these models has a driver for their native software in the RDK.
For example, the `ur5e`'s driver is defined in the RDK as found on [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/arm/universalrobots/ur.go).

Each of these models also has to have a [kinematics file](/internals/kinematic-chain-config/) that specifies the relative [orientation](/internals/orientation-vector/) of components in its kinematic chain, for services like [Motion](/services/motion/) to consume, which is located in the RDK in the same directory as the respective driver.
For example, the `ur5e`'s kinematics file, <file>ur5e.json</file> is defined in the RDK as found on [GitHub](https://github.com/viamrobotics/rdk/blob/main/components/arm/universalrobots/ur5e.json).

See [Arm Configuration](/components/arm/#configuration) for the current list of built-in models the RDK provides.

{{% /alert %}}

If you have a robot arm that's native software is not provided with a driver, you probably don't want to replace that arm ($$$), but you might want to use the [Arm API](/components/arm/#api) or use your arm with one of Viam's [services](/services/).

If you want to [program](/program/) and control your own robotic arm like a built-in resource:

   [Create your arm's kinematics file.](#create-your-arms-kinematics-file)

   [Create a custom arm model as a modular resource](#create-a-custom-arm-model-as-a-modular-resource). Code your own driver as a custom model of the arm resource subtype. Package it in a module with an entry point file and a resource registration file.

   Configure the module and modular resource on your robot.

Follow these instructions to implement a model of [arm component](/components/arm/) that is not built-in to the RDK.

{{% alert title="Modules vs. modular resources" color="tip" %}}

The Viam module system allows you to integrate custom {{< glossary_tooltip term_id="resource" text="resources" >}} ([components](/components/) and [services](/services/)) into any robot running on Viam.

A configured *module* can make one or more *modular resources* available for configuration.

{{% /alert %}}

## Create your arm's kinematics file

<!-- TODO: write instructions on this -->

## Create a custom arm model as a modular resource

To create a custom arm model, code a module in Python with the module support libraries provided by [Viam's SDKs](/program/apis/):

To define a new model of a built-in resource subtype:

1. [Code a new resource model](#code-a-new-resource-model) implementing all methods the Viam RDK requires in the API definition of its built-in subtype (ex. `rdk:component:arm`).
Import your custom model and API into the main program and register the new resource model with your chosen SDK.

1. [Code a main program](#code-a-main-entry-point-program) that starts the module after adding your desired resources from the registry.
This main program is the "entry point" to your module.

1. [Compile or package](#compile-the-module-into-an-executable) the module into a single executable that can receive a socket argument from Viam, open the socket, and start the module at the entry point.

### Code a new resource model

Save the following two files, <file>my_modular_arm.py</file> and <file>__init__.py</file>, on your computer and edit the code as applicable.

This module template registers a modular resource implementing Viam's built-in [Arm API](/components/arm/#api) [(rdk:service:arm)](/extend/modular-resources/key-concepts/#models) as a new model, `"myarm"`:

The Go code for the custom model (<file>my_modular_arm.py</file>), resource registration file (<file>\__init__.py</file>), and module entry point file (<file>main.go</file>) is adapted from the [Python SDK Docs](https://python.viam.dev/examples/example.html#custom-modular-arm-example).

<file>my_modular_arm.py</file> implements a custom model of the arm component built-in resource, "myarm".

<details>
  <summary>Click to view sample code from <file>my_modular_arm.py</file></summary>

``` python {class="line-numbers linkable-line-numbers"}
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

</details>
<br>
<file>__init__.py</file> registers the my_modular_arm custom model and API helper functions with the SDK.

<details>
  <summary>Click to view sample code from <file>__init__.py</file></summary>

``` python {class="line-numbers linkable-line-numbers"}
from viam.components.arm import Arm
from viam.resource.registry import Registry, ResourceCreatorRegistration
from .my_modular_arm import MyModularArm


Registry.register_resource_creator(Arm.SUBTYPE, MyModularArm.MODEL, ResourceCreatorRegistration(MyModularArm.new))
```

</details>

### Code a main entry point program

<file>main.py</file> is the Python module's entry point file.
When executed, it initializes the `myarm` custom model and API helper functions from the registry.

<details>
  <summary>Click to view sample code from <file>main.py</file></summary>

``` python {class="line-numbers linkable-line-numbers"}
import asyncio

from viam.module.module import Module
from viam.components.arm import Arm

from .my_modular_arm import MyModularArm 


async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
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

To [add a module](/extend/modular-resources/configure/#configure-your-module) to the configuration of your robot, you need to have an [executable](https://en.wikipedia.org/wiki/Executable) that runs your module when executed, can take a local socket as a command line argument, and cleanly exits when sent a termination signal.

Your options for completing this step are flexible, as this file does not need to be in a raw binary format.

One option is to create and save a new shell script (<file>.sh</file>) that runs your module at your entry point (main program) file.

For example:

``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
#!/bin/sh
cd `dirname $0`

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec python3 -m <your-module-directory-name>.<main-program-filename-without-extension> $@
```

To make this shell script executable, run the following command in your terminal:

``` sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sudo chmod +x <FILEPATH>/<FILENAME>
```

Ensure any dependencies for your module (including the [Python SDK](https://python.viam.dev/)) are installed on your robot's computer.
Your executable will be run by `viam-server` as root, so dependencies need to be available to the root user.

## Next steps

Follow [these configuration instructions](/extend/modular-resources/configure/) to add your custom resource to your robot.
