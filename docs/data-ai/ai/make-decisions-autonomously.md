---
linkTitle: "Make decisions autonomously"
title: "Make decisions autonomously"
weight: 70
layout: "docs"
type: "docs"
description: "Use the vision service API to act based on inferences."
next: "/data-ai/train/upload-external-data/"
aliases:
  - /data-ai/ai/act/
---

Use the [vision service API](/dev/reference/apis/services/vision/) to make inferences, then use [component APIs](/dev/reference/apis/#component-apis) to react to inferences with a machine.

## Follow a line

This module uses a vision service and a motor to program a machine to follow a line of a configurable color.

### Prerequisites

- An SBC, for example a Raspberry Pi 4
- A wheeled base component such as a [SCUTTLE robot](https://www.scuttlerobot.org/shop/)
- A webcam
- Colored tape, to create a path for your robot

### Configure your machine

Follow the [setup guide](/operate/get-started/setup/) to create a new machine.

Connect your SCUTTLE base to your SBC.
Add the following `components` configuration to create board, base, and motor components in Viam so you can control your SCUTTLE base:

```json
{
  "name": "my-board",
  "model": "pi",
  "api": "rdk:component:board",
  "attributes": {}
},
{
  "name": "leftm",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "a": "15",
      "b": "16"
    },
    "board": "my-board",
    "max_rpm": 200
  }
},
{
  "name": "rightm",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "b": "11",
      "dir": "",
      "pwm": "",
      "a": "12"
    },
    "board": "my-board",
    "max_rpm": 200
  }
},
{
  "name": "scuttlebase",
  "model": "wheeled",
  "api": "rdk:component:base",
  "attributes": {
    "width_mm": 400,
    "wheel_circumference_mm": 258,
    "left": ["leftm"],
    "right": ["rightm"]
  }
}
```

Connect your webcam to your SBC.
Add the following `components` configuration for your webcam:

```json
{
  "name": "my_camera",
  "model": "webcam",
  "api": "rdk:component:camera",
  "attributes": {
    "video_path": ""
  }
}
```

Finally, add the following `services` configuration for your vision service, replacing the `detect_color` value with the color of your line:

```json
{
  "name": "my_line_detector",
  "api": "rdk:service:vision",
  "model": "color_detector",
  "attributes": {
    "segment_size_px": 100,
    "detect_color": "#19FFD9", // replace with the color of your line
    "hue_tolerance_pct": 0.06
  }
}
```

### Create your module

In a terminal, run the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate
```

Enter the following configuration for your new module:

- **module name**: "autonomous_example_module"
- **language**: Python
- **visibility**: private
- **organization ID**: your organization ID, found on the Viam organization settings page
- **resource to be added to the module**: Generic Service
- **model name**: "line_follower"
- **Enable cloud build**: yes
- **Register module**: yes

Create a file called <file>reload.sh</file> in the root directory of your newly-generated module.
Copy and paste the following code into <file>reload.sh</file>:

```bash
#!/usr/bin/env bash

# bash safe mode. look at `set --help` to see what these are doing
set -euxo pipefail

cd $(dirname $0)
MODULE_DIR=$(dirname $0)
VIRTUAL_ENV=$MODULE_DIR/venv
PYTHON=$VIRTUAL_ENV/bin/python
./setup.sh

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec $PYTHON src/main.py $@
```

In a terminal, run the following command to make <file>reload.sh</file> executable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
chmod +x reload.sh
```

Create a virtual Python environment with the necessary packages by running the module setup script from within the module directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

Edit your <file>meta.json</file>, replacing the `"entrypoint"`, `"build"`, and `"path"` fields as follows:

```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
 "entrypoint": "reload.sh",
 "first_run": "",
 "build": {
   "build": "rm -f module.tar.gz && tar czf module.tar.gz requirements.txt src/*.py src/models/*.py meta.json setup.sh reload.sh",
   "setup": "./setup.sh",
   "path": "module.tar.gz",
   "arch": [
     "linux/amd64",
     "linux/arm64"
   ]
 }
```

### Code

Replace the contents of <file>src/models/line_follower.py</file> with the following code.
Replace the `<example-namespace>` placeholder with your organization namespace.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import Any, Mapping, Sequence, Tuple
from typing_extensions import Self

from viam.components.base import Base
from viam.components.camera import Camera
from viam.logging import getLogger
from viam.module.module import Module
from viam.resource.types import Model, ModelFamily
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.services.vision import VisionClient
from viam.components.base import Base, Vector3

class LineFollower(Module, ResourceBase):
    MODEL = Model(ModelFamily("<example-namespace>", "autonomous_example_module"), "line-follower")
    LOGGER = getLogger(__name__)

    def __init__(self, name: str):
        super().__init__(name)
        self.camera: Camera = None
        self.base: Base = None
        self.detector: VisionClient = None
        self._running_loop = False
        self._loop_task = None
        self.linear_power = 0.35
        self.angular_power = 0.3

    @classmethod
    def new_resource(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        instance = cls(config.name)
        instance.reconfigure(config, dependencies)
        return instance

    @classmethod
    def validate(cls, config: ComponentConfig) -> Tuple[Sequence[str], Sequence[str]]:
        camera_name = config.attributes.fields["camera_name"].string_value
        detector_name = config.attributes.fields["detector_name"].string_value
        base_name = config.attributes.fields["base_name"].string_value

        dependencies = [camera_name, detector_name, base_name]
        return dependencies, []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.camera_name = config.attributes.fields["camera_name"].string_value
        self.detector_name = config.attributes.fields["detector_name"].string_value
        self.detector_name = config.attributes.fields["base_name"].string_value

        for dependency_name, dependency in dependencies.items():
            if dependency_name.subtype == "camera" and dependency_name.name == self.camera_name:
                self.camera = dependency
            elif dependency_name.subtype == "vision" and dependency_name.name == self.detector_name:
                self.detector = dependency
            elif dependency_name.subtype == "base" and dependency_name.name == self.base_name:
                self.base = dependency

        if not self.camera:
            raise ValueError(f"Camera '{self.camera_name}' dependency not found.")
        if not self.detector:
            raise ValueError(f"Vision service '{self.detector_name}' dependency not found.")
        if not self.base:
            raise ValueError(f"Base '{self.base_name}' dependency not found.")

        LineFollower.LOGGER.info("Reconfigured.")

    async def start(self):
        LineFollower.LOGGER.info("Starting color following...")
        await self._start_color_following_internal()

    async def close(self):
        LineFollower.LOGGER.info("Stopping color following...")
        await self._stop_color_following_internal()
        LineFollower.LOGGER.info("Stopped.")

    async def _color_following_loop(self):
        LineFollower.LOGGER.info("Color following loop started.")

        while self._running_loop:
            try:
                # Check for color in front
                if await self._is_color_in_front():
                    LineFollower.LOGGER.info("Moving forward.")
                    await self.base.set_power(Vector3(y=self.linear_power), Vector3())
                # Check for color to the left
                elif await self._is_color_there("left"):
                    LineFollower.LOGGER.info("Turning left.")
                    await self.base.set_power(Vector3(), Vector3(z=self.angular_power))
                # Check for color to the right
                elif await self._is_color_there("right"):
                    LineFollower.LOGGER.info("Turning right.")
                    await self.base.set_power(Vector3(), Vector3(z=-self.angular_power))
                else:
                    LineFollower.LOGGER.info("No color detected. Stopping.")
                    await self.base.stop()

            except Exception as e:
                LineFollower.LOGGER.error(f"Error in color following loop: {e}")

            await asyncio.sleep(0.05)

        LineFollower.LOGGER.info("Color following loop finished.")
        await self.base.stop()

    async def _start_color_following_internal(self):
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._color_following_loop())
            LineFollower.LOGGER.info("Requested to start color following loop.")
        else:
            LineFollower.LOGGER.info("Color following loop is already running.")

    async def _stop_color_following_internal(self):
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task
                self._loop_task = None
            LineFollower.LOGGER.info("Requested to stop color following loop.")

    async def _is_color_in_front(self) -> bool:
        frame = await self.camera.get_image()
        detections = await self.detector.get_detections(frame)
        return any(detection.class_name == "target_color" for detection in detections)

    async def _is_color_there(self, location: str) -> bool:
        frame = await self.camera.get_image()
        if location == "left":
            # Crop logic for left side
            pass
        elif location == "right":
            # Crop logic for right side
            pass
        # Implement detection logic here
        detections = await self.detector.get_detections(frame)
        return any(detection.class_name == "target_color" for detection in detections)

# Register your module
Registry.register_resource_creator(
    LineFollower.MODEL,
    ResourceCreatorRegistration(LineFollower.new_resource, LineFollower.validate)
)

async def main():
    """
    Main entry point for the Viam module.
    """
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    LineFollower.LOGGER.info("Done.")
```

### Run your module

Find the [Part ID](/dev/reference/apis/fleet/#find-part-id) for your machine.
To deploy your module on your machine, run the following command, replacing `<your-part-id>` with your Part ID:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id <your-part-id>
```

Add the following `services` configuration for your new module:

```json
{
  "name": "generic-1",
  "api": "rdk:service:generic",
  "model": "<example-namespace>:autonomous_example_module:line_follower",
  "attributes": {
    "detector_name": "my_object_detector",
    "camera_name": "my_camera"
  }
}
```

Give your machine a few moments to load the new configuration, and you can begin testing your module.

## Follow a colored object

This module uses a vision service and a motor to program a machine to follow an object of a configurable color.

### Prerequisites

- An SBC, for example a Raspberry Pi 4
- A wheeled base component such as a [SCUTTLE robot](https://www.scuttlerobot.org/shop/)
- A webcam
- Colored tape, to create a path for your robot

### Configure your machine

Follow the [setup guide](/operate/get-started/setup/) to create a new machine.

Connect your SCUTTLE base to your SBC.
Add the following `components` configuration to create board, base, and motor components in Viam so you can control your SCUTTLE base:

```json
{
  "name": "my-board",
  "model": "pi",
  "api": "rdk:component:board",
  "attributes": {}
},
{
  "name": "leftm",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "a": "15",
      "b": "16"
    },
    "board": "my-board",
    "max_rpm": 200
  }
},
{
  "name": "rightm",
  "model": "gpio",
  "api": "rdk:component:motor",
  "attributes": {
    "pins": {
      "b": "11",
      "dir": "",
      "pwm": "",
      "a": "12"
    },
    "board": "my-board",
    "max_rpm": 200
  }
},
{
  "name": "my_base",
  "model": "wheeled",
  "api": "rdk:component:base",
  "attributes": {
    "width_mm": 400,
    "wheel_circumference_mm": 258,
    "left": ["leftm"],
    "right": ["rightm"]
  }
}
```

Connect your webcam to your SBC.
Add the following `components` configuration for your webcam:

```json
{
  "name": "my_camera",
  "model": "webcam",
  "api": "rdk:component:camera",
  "attributes": {
    "video_path": ""
  }
}
```

Add the following `services` configuration, replacing the `detect_color` value with the color of your object:

```json
{
  "name": "my_color_detector",
  "api": "rdk:service:vision",
  "model": "my_object_detector",
  "attributes": {
    "segment_size_px": 100,
    "detect_color": "#a13b4c", // replace with the color of your object
    "hue_tolerance_pct": 0.06
  }
}
```

### Create your module

In a terminal, run the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate
```

Enter the following configuration for your new module:

- **module name**: "autonomous_example_module"
- **language**: Python
- **visibility**: private
- **organization ID**: your organization ID, found on the Viam organization settings page
- **resource to be added to the module**: Generic Service
- **model name**: "object_follower"
- **Enable cloud build**: yes
- **Register module**: yes

Create a file called <file>reload.sh</file> in the root directory of your newly-generated module.
Copy and paste the following code into <file>reload.sh</file>:

```bash
#!/usr/bin/env bash

# bash safe mode. look at `set --help` to see what these are doing
set -euxo pipefail

cd $(dirname $0)
MODULE_DIR=$(dirname $0)
VIRTUAL_ENV=$MODULE_DIR/venv
PYTHON=$VIRTUAL_ENV/bin/python
./setup.sh

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec $PYTHON src/main.py $@
```

In a terminal, run the following command to make <file>reload.sh</file> executable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
chmod +x reload.sh
```

Create a virtual Python environment with the necessary packages by running the module setup script from within the module directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

Edit your <file>meta.json</file>, replacing the `"entrypoint"`, `"build"`, and `"path"` fields as follows:

```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
 "entrypoint": "reload.sh",
 "first_run": "",
 "build": {
   "build": "rm -f module.tar.gz && tar czf module.tar.gz requirements.txt src/*.py src/models/*.py meta.json setup.sh reload.sh",
   "setup": "./setup.sh",
   "path": "module.tar.gz",
   "arch": [
     "linux/amd64",
     "linux/arm64"
   ]
 }
```

### Code

Replace the contents of <file>src/models/object_follower.py</file> with the following code.
Replace the `<example-namespace>` placeholder with your organization namespace.

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import Any, Mapping, List, Literal, Sequence, Tuple
from typing_extensions import Self

from viam.components.base import Base
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
from viam.module.module import Module
from viam.resource.types import Model, Subtype
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.proto.app.v1 import ComponentConfig
from viam.services.vision import Detection

class ObjectFollower(Module):
    MODEL = Model("<example-namespace>", "autonomous_example_module", "object_follower")

    def __init__(self, name: str):
        super().__init__(name)
        self.base: Base = None
        self.camera: Camera = None
        self.detector: VisionClient = None

        self._running_loop = False
        self._loop_task = None

        self.spin_num = 10
        self.straight_num = 300
        self.vel = 500
        self.num_cycles = 200

    @classmethod
    def new_resource(cls, config: ComponentConfig, dependencies: Mapping[str, ResourceBase]) -> Self:
        instance = cls(config.name)
        instance.reconfigure(config, dependencies)
        return instance

    @classmethod
    def validate(cls, config: ComponentConfig) -> Tuple[Sequence[str], Sequence[str]]:
        camera_name = config.attributes.fields["camera_name"].string_value
        detector_name = config.attributes.fields["detector_name"].string_value
        base_name = config.attributes.fields["base_name"].string_value

        dependencies = [camera_name, detector_name, base_name]
        return dependencies, []

    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        self.camera_name = config.attributes.fields["camera_name"].string_value
        self.detector_name = config.attributes.fields["detector_name"].string_value
        self.detector_name = config.attributes.fields["base_name"].string_value

        for dependency_name, dependency in dependencies.items():
            if dependency_name.subtype == "camera" and dependency_name.name == self.camera_name:
                self.camera = dependency
            elif dependency_name.subtype == "vision" and dependency_name.name == self.detector_name:
                self.detector = dependency
            elif dependency_name.subtype == "base" and dependency_name.name == self.base_name:
                self.base = dependency

        if not self.camera:
            raise ValueError(f"Camera '{self.camera_name}' dependency not found.")
        if not self.detector:
            raise ValueError(f"Vision service '{self.detector_name}' dependency not found.")
        if not self.base:
            raise ValueError(f"Base '{self.base_name}' dependency not found.")

        LineFollower.LOGGER.info("Reconfigured.")

    async def start(self):
        """
        Called when the module starts. Get references to components.
        """
        ObjectFollower.LOGGER.info(f"'{self.name}' starting...")
        await self.start_object_tracking()
        ObjectFollower.LOGGER.info(f"'{self.name}' started.")

    async def close(self):
        """
        Called when the module is shutting down. Clean up tasks.
        """
        ObjectFollower.LOGGER.info(f"'{self.name}' closing...")
        await self.stop_object_tracking()
        ObjectFollower.LOGGER.info(f"'{self.name}' closed.")

    def left_or_right(self, detections: List[Detection], midpoint: float) -> Literal[0, 1, 2, -1]:
        """
        Get largest detection box and see if its center is in the left, center, or right third.
        Returns 0 for left, 1 for center, 2 for right, -1 if nothing detected.
        """
        largest_area = 0
        largest_detection: Detection = None

        if not detections:
            return -1

        for d in detections:
            area = (d.x_max - d.x_min) * (d.y_max - d.y_min)
            if area > largest_area:
                largest_area = area
                largest_detection = d

        if largest_detection is None:
            return -1

        centerX = largest_detection.x_min + (largest_detection.x_max - largest_detection.x_min) / 2

        if centerX < midpoint - midpoint / 6:
            return 0  # on the left
        elif centerX > midpoint + midpoint / 6:
            return 2  # on the right
        else:
            return 1  # basically centered

    async def _object_tracking_loop(self):
        """
        The core object tracking and base control logic loop.
        """
        ObjectFollower.LOGGER.info("Object tracking control loop started.")

        initial_frame = await self.camera.get_image(mime_type="image/jpeg")
        pil_initial_frame = viam_to_pil_image(initial_frame)
        midpoint = pil_initial_frame.size[0] / 2

        cycle_count = 0
        while self._running_loop and (self.num_cycles == 0 or cycle_count < self.num_cycles):
            try:
                detections = await self.detector.get_detections_from_camera(self.camera_name)

                answer = self.left_or_right(detections, midpoint)

                if answer == 0:
                    ObjectFollower.LOGGER.info("Detected object on left, spinning left.")
                    await self.base.spin(self.spin_num, self.vel)
                    await self.base.move_straight(self.straight_num, self.vel)
                elif answer == 1:
                    ObjectFollower.LOGGER.info("Detected object in center, moving straight.")
                    await self.base.move_straight(self.straight_num, self.vel)
                elif answer == 2:
                    ObjectFollower.LOGGER.info("Detected object on right, spinning right.")
                    await self.base.spin(-self.spin_num, self.vel)
                    await self.base.move_straight(self.straight_num, self.vel)
                else:
                    ObjectFollower.LOGGER.info("No object detected, stopping base.")
                    await self.base.stop()

            except Exception as e:
                ObjectFollower.LOGGER.info(f"Error in object tracking loop: {e}")

            cycle_count += 1
            await asyncio.sleep(0.1)

        ObjectFollower.LOGGER.info("Object tracking loop finished or stopped.")
        await self.base.stop()
        self._running_loop = False

    async def start_object_tracking(self):
        """
        Starts the background loop for object tracking and base control.
        """
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._object_tracking_loop())
            ObjectFollower.LOGGER.info("Requested to start object tracking loop.")
        else:
            ObjectFollower.LOGGER.info("Object tracking loop is already running.")

    async def stop_object_tracking(self):
        """
        Stops the background loop for object tracking and base control.
        """
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task  # Wait for the task to complete its current iteration and exit
                self._loop_task = None
            ObjectFollower.LOGGER.info("Requested to stop object tracking loop.")
        else:
            ObjectFollower.LOGGER.info("Object tracking loop is not running.")

# Register your module
Registry.register_resource_creator(
    ObjectFollower.MODEL,
    ResourceCreatorRegistration(ObjectFollower.new_resource, ObjectFollower.validate)
)

async def main():
    """
    Main entry point for the Viam module.
    """
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    ObjectFollower.LOGGER.info("Done.")
```

### Run your module

Find the [Part ID](/dev/reference/apis/fleet/#find-part-id) for your machine.
To deploy your module on your machine, run the following command, replacing `<your-part-id>` with your Part ID:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id <your-part-id>
```

Add the following `services` configuration for your new model:

```json
{
  "name": "generic-1",
  "api": "rdk:service:generic",
  "model": "<example-namespace>:autonomous_example_module:line_follower",
  "attributes": {
    "camera_name": "my_camera"
  }
}
```

Give your machine a few moments to load the new configuration, and you can begin testing your module.

## Notify when a certain object appears in a video feed

This module uses a vision service to program a machine to send a notification when a certain object appears in a video feed.
This example detects people with an IR camera, but you can use a different camera, ML model, or vision service to detect any object with the same logic.

### Prerequisites

- An SBC, for example a Raspberry Pi 4
- An IR camera, for example a [Raspberry Pi Camera Module 2 NoIR](https://www.raspberrypi.com/products/pi-noir-camera-v2/)

### Configure your machine

Follow the [setup guide](/operate/get-started/setup/) to create a new machine.

Connect your camera to your SBC.
Add the following `components` configuration for your camera:

```json
{
  "name": "my_camera",
  "model": "viam:camera:csi",
  "attributes": {
    "width_px": 1920,
    "height_px": 1080,
    "frame_rate": 30
  },
  "depends_on": [],
  "namespace": "rdk",
  "type": "camera"
}
```

Add the following `services` configuration:

```json
{
  "name": "ir-person-mlmodel",
  "type": "mlmodel",
  "namespace": "rdk",
  "model": "viam-labs:mlmodel:near-ir-person",
  "attributes": {}
},
{
  "name": "my-object-detector",
  "type": "vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "ir-person-mlmodel"
  }
}
```

### Create your module

In a terminal, run the following command:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module generate
```

Enter the following configuration for your new module:

- **module name**: "autonomous_example_module"
- **language**: Python
- **visibility**: private
- **organization ID**: your organization ID, found on the Viam organization settings page
- **resource to be added to the module**: Generic Service
- **model name**: "email_notifier"
- **Enable cloud build**: yes
- **Register module**: yes

Create a file called <file>reload.sh</file> in the root directory of your newly-generated module.
Copy and paste the following code into <file>reload.sh</file>:

```bash
#!/usr/bin/env bash

# bash safe mode. look at `set --help` to see what these are doing
set -euxo pipefail

cd $(dirname $0)
MODULE_DIR=$(dirname $0)
VIRTUAL_ENV=$MODULE_DIR/venv
PYTHON=$VIRTUAL_ENV/bin/python
./setup.sh

# Be sure to use `exec` so that termination signals reach the python process,
# or handle forwarding termination signals manually
exec $PYTHON src/main.py $@
```

In a terminal, run the following command to make <file>reload.sh</file> executable:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
chmod +x reload.sh
```

Create a virtual Python environment with the necessary packages by running the module setup script from within the module directory:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
sh setup.sh
```

Edit your <file>meta.json</file>, replacing the `"entrypoint"`, `"build"`, and `"path"` fields as follows:

```json {class="line-numbers linkable-line-numbers" data-start="13" data-line="1, 4, 6" }
 "entrypoint": "reload.sh",
 "first_run": "",
 "build": {
   "build": "rm -f module.tar.gz && tar czf module.tar.gz requirements.txt src/*.py src/models/*.py meta.json setup.sh reload.sh",
   "setup": "./setup.sh",
   "path": "module.tar.gz",
   "arch": [
     "linux/amd64",
     "linux/arm64"
   ]
 }
```

### Code

Replace the contents of <file>src/models/email_notifier.py</file> with the following code.
Replace the `<example-namespace>` placeholder with your organization namespace.

```python
import asyncio
import os
from typing import List, Mapping, Any

from viam.robot.client import RobotClient
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.module.module import Module
from viam.resource.types import Model
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.proto.app.v1 import ComponentConfig
from viam.services.generic import Generic
import smtplib
from email.mime.text import MIMEText

class EmailNotifier(Module, Generic):
    MODEL = Model("<example-namespace>", "autonomous_example_module", "email_notifier")

    def __init__(self, name: str):
        super().__init__(name)
        self.camera: Camera = None
        self.detector: VisionClient = None
        self.notification_sent: bool = False

        # Email configuration
        self.sender_email: str = os.getenv("SENDER_EMAIL", "your_email@example.com")
        self.sender_password: str = os.getenv("SENDER_PASSWORD", "your_email_password")
        self.receiver_email: str = os.getenv("RECEIVER_EMAIL", "recipient_email@example.com")
        self.smtp_server: str = os.getenv("SMTP_SERVER", "smtp.example.com")
        self.smtp_port: int = int(os.getenv("SMTP_PORT", 587))

        self._running_loop = False
        self._loop_task = None

    @classmethod
    def new_resource(cls, config: ComponentConfig):
        module = cls(config.name)
        if "camera_name" in config.attributes.fields:
            module.camera_name = config.attributes.fields["camera_name"].string_value
        if "detector_name" in config.attributes.fields:
            module.camera_name = config.attributes.fields["detector_name"].string_value
        if "sender_email" in config.attributes.fields:
            module.sender_email = config.attributes.fields["sender_email"].string_value
        if "sender_password" in config.attributes.fields:
            module.sender_password = config.attributes.fields["sender_password"].string_value
        if "receiver_email" in config.attributes.fields:
            module.receiver_email = config.attributes.fields["receiver_email"].string_value
        if "smtp_server" in config.attributes.fields:
            module.smtp_server = config.attributes.fields["smtp_server"].string_value
        if "smtp_port" in config.attributes.fields:
            module.smtp_port = int(config.attributes.fields["smtp_port"].number_value)

        return module

    async def start(self):
        EmailNotifier.LOGGER.info(f"'{self.name}' starting...")
        self.camera = await Camera.from_robot(self.robot, self.camera_name)
        self.detector = await VisionClient.from_robot(self.robot, self.detector_name)
        EmailNotifier.LOGGER.info(f"'{self.name}' started. Monitoring for detections.")

    async def close(self):
        EmailNotifier.LOGGER.info(f"'{self.name}' closing...")
        await self._stop_detection_monitoring_internal()
        EmailNotifier.LOGGER.info(f"'{self.name}' closed.")

    def _send_email(self, subject: str, body: str):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            EmailNotifier.LOGGER.info(f"Email sent successfully to {self.receiver_email}: '{subject}'")
            self.notification_sent = True
        except Exception as e:
            EmailNotifier.LOGGER.info(f"Failed to send email: {e}")
            self.notification_sent = False

    async def _detection_monitoring_loop(self):
        EmailNotifier.LOGGER.info("Detection monitoring loop started.")

        while self._running_loop:
            try:
                detections = await self.detector.get_detections_from_camera(self.camera_name)

                if detections and not self.notification_sent:
                    subject = "Viam Module Alert: Detection Found!"
                    body = "A detection was found by the vision service."
                    EmailNotifier.LOGGER.info("Detection found. Sending email notification...")
                    self._send_email(subject, body)
                elif not detections and self.notification_sent:
                    EmailNotifier.LOGGER.info("No detections found. Resetting notification status.")
                    self.notification_sent = False
                elif detections and self.notification_sent:
                    EmailNotifier.LOGGER.info("Detection still present, but notification already sent.")
                else:
                    EmailNotifier.LOGGER.info("No detections.")

            except Exception as e:
                EmailNotifier.LOGGER.info(f"Error in detection monitoring loop: {e}")

            await asyncio.sleep(5)

        EmailNotifier.LOGGER.info("Detection monitoring loop finished or stopped.")
        self.notification_sent = False

    async def _start_detection_monitoring_internal(self):
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._detection_monitoring_loop())
            EmailNotifier.LOGGER.info("Requested to start detection monitoring loop.")
            return {"status": "started"}
        else:
            EmailNotifier.LOGGER.info("Detection monitoring loop is already running.")
            return {"status": "already_running"}

    async def _stop_detection_monitoring_internal(self):
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task
                self._loop_task = None
            EmailNotifier.LOGGER.info("Requested to stop detection monitoring loop.")
            return {"status": "stopped"}
        else:
            EmailNotifier.LOGGER.info("Detection monitoring loop is not running.")
            return {"status": "not_running"}

    async def do_command(self, command: Mapping[str, Any], *, timeout: float | None = None, **kwargs) -> Mapping[str, Any]:
        if "start_monitoring" in command:
            EmailNotifier.LOGGER.info("Received 'start_monitoring' command via do_command.")
            return await self._start_detection_monitoring_internal()
        elif "stop_monitoring" in command:
            EmailNotifier.LOGGER.info("Received 'stop_monitoring' command via do_command.")
            return await self._stop_detection_monitoring_internal()
        else:
            raise NotImplementedError(f"Command '{command}' not recognized.")

# Register your module
Registry.register_resource_creator(
    Generic.SUBTYPE,
    EmailNotifier.MODEL,
    ResourceCreatorRegistration(EmailNotifier.new_resource, EmailNotifier.validate_config)
)

async def main():
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    EmailNotifier.LOGGER.info("Done.")
```

### Run your module

Find the [Part ID](/dev/reference/apis/fleet/#find-part-id) for your machine.
To deploy your module on your machine, run the following command, replacing `<your-part-id>` with your Part ID:

```sh {id="terminal-prompt" class="command-line" data-prompt="$"}
viam module reload --part-id <your-part-id>
```

Add the following `services` configuration for your new model:

```json
{
  "name": "generic-1",
  "api": "rdk:service:generic",
  "model": "<example-namespace>:autonomous_example_module:email_notifier",
  "attributes": {
    "detector_name": "my-object-detector",
    "camera_name": "my_camera"
  }
}
```

Give your machine a few moments to load the new configuration, and you can begin testing your module.
