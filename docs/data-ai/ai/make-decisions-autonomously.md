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

This module uses a vision service and a motor to program a machine to follow a line.

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
  "attributes": {},
  "depends_on": []
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
  },
  "depends_on": ["my-board"]
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
  },
  "depends_on": ["my-board"]
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
  },
  "depends_on": ["leftm", "rightm"]
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
  "name": "green_detector",
  "api": "rdk:service:vision",
  "model": "my_line_detector",
  "attributes": {
    "segment_size_px": 100,
    "detect_color": "#19FFD9", // replace with the color of your line
    "hue_tolerance_pct": 0.06
  }
}
```

### Code

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import Literal

from viam.media.video import CameraMimeType
from viam.robot.client import RobotClient
from viam.components.base import Base, Vector3
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
from viam.module.module import Module
from viam.resource.types import Model, Subtype
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.proto.app.v1 import ComponentConfig

class LineFollowerAPI(ResourceBase):
    """
    LineFollowerAPI represents a custom API for controlling a base based on vision.
    """
    SUBTYPE = Subtype("example-namespace", "example-module", "line_follower")

    async def start_line_following(self):
        raise NotImplementedError

    async def stop_line_following(self):
        raise NotImplementedError

async def is_color_in_front(camera: Camera, detector: VisionClient):
    """
    Returns whether the appropriate path color is detected in front of the center of the robot.
    """
    frame = viam_to_pil_image(await camera.get_image(mime_type=CameraMimeType.JPEG))

    x, y = frame.size[0], frame.size[1]

    # Crop the image to get only the middle fifth of the top third of the original image
    cropped_frame = frame.crop((x / 2.5, 0, x / 1.25, y / 3))

    detections = await detector.get_detections(
        pil_to_viam_image(cropped_frame, CameraMimeType.JPEG)
    )

    if detections: # Check if the list is not empty
        return True
    return False


async def is_color_there(
    camera: Camera, detector: VisionClient, location: Literal["left", "right"]
):
    """
    Returns whether the appropriate path color is detected to the left/right of the robot's front.
    """
    frame = viam_to_pil_image(await camera.get_image(mime_type=CameraMimeType.JPEG))
    x, y = frame.size[0], frame.size[1]

    if location == "left":
        # Crop image to get only the left two fifths of the original image
        cropped_frame = frame.crop((0, 0, x / 2.5, y))

        detections = await detector.get_detections(
            pil_to_viam_image(cropped_frame, CameraMimeType.JPEG)
        )

    elif location == "right":
        # Crop image to get only the right two fifths of the original image
        cropped_frame = frame.crop((x / 1.25, 0, x, y))

        detections = await detector.get_detections(
            pil_to_viam_image(cropped_frame, CameraMimeType.JPEG)
        )
    else:
        detections = [] # Ensure detections is defined if location is neither 'left' nor 'right'

    if detections: # Check if the list is not empty
        return True
    return False


async def stop_robot(base: Base):
    """
    Stop the robot's motion.
    """
    await base.stop()

# Implement your custom control logic module
class LineFollowerModule(Module, LineFollowerAPI):
    MODEL = Model("example-namespace", "example-module", "line_follower_module")

    def __init__(self, name: str):
        super().__init__(name)
        self.camera: Camera = None
        self.base: Base = None
        self.detector: VisionClient = None
        self._running_loop = False
        self._loop_task = None

        # Speed parameters (can be configured via module config if desired)
        self.linear_power = 0.35
        self.angular_power = 0.3

    @classmethod
    def new_resource(cls, config: ComponentConfig):
        return cls(config.name)

    async def start(self):
        """
        Called when the module starts. Get references to components.
        """
        print(f"LineFollowerModule '{self.name}' starting...")
        # Access components directly from the robot object provided by the module framework
        self.camera = await Camera.from_robot(self.robot, "my_camera")
        self.base = await Base.from_robot(self.robot, "scuttlebase")
        # Replace "green_detector" with your actual vision service name
        self.detector = await VisionClient.from_robot(self.robot, "my_line_detector")
        print(f"LineFollowerModule '{self.name}' started.")

    async def close(self):
        """
        Called when the module is shutting down. Clean up tasks.
        """
        print(f"LineFollowerModule '{self.name}' closing...")
        await self.stop_line_following()
        print(f"LineFollowerModule '{self.name}' closed.")

    async def _line_follower_loop(self):
        """
        The core line following control logic loop.
        """
        print("Line follower control loop started.")
        counter = 0 # counter to increase robustness

        while self._running_loop and counter <= 3:
            try:
                if await is_color_in_front(self.camera, self.detector):
                    print("going straight")
                    # Moves the base slowly forward in a straight line
                    await self.base.set_power(Vector3(y=self.linear_power), Vector3())
                    counter = 0
                # If there is green to the left, turns the base left at a continuous, slow speed
                elif await is_color_there(self.camera, self.detector, "left"):
                    print("going left")
                    await self.base.set_power(Vector3(), Vector3(z=self.angular_power))
                    counter = 0
                # If there is green to the right, turns the base right at a continuous, slow speed
                elif await is_color_there(self.camera, self.detector, "right"):
                    print("going right")
                    await self.base.set_power(Vector3(), Vector3(z=-self.angular_power))
                    counter = 0
                else:
                    print(f"No color detected, counter: {counter}")
                    counter += 1
                    # Optionally, stop or slow down if no color is detected
                    await self.base.stop()

            except Exception as e:
                print(f"Error in line follower loop: {e}")

            await asyncio.sleep(0.05) # Adjust sleep time for desired loop frequency

        print("The path is behind us and forward is only open wasteland.")
        await stop_robot(self.base) # Stop the robot when the loop finishes
        self._running_loop = False # Ensure loop state is reset

    async def start_line_following(self):
        """
        Starts the background loop for line following.
        """
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._line_follower_loop())
            print("Requested to start line following loop.")
        else:
            print("Line following loop is already running.")

    async def stop_line_following(self):
        """
        Stops the background loop for line following.
        """
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task # Wait for the task to complete its current iteration and exit
                self._loop_task = None
            print("Requested to stop line following loop.")
        else:
            print("Line following loop is not running.")

# Register your module
Registry.register_resource_creator(
    LineFollowerAPI.SUBTYPE,
    LineFollowerModule.MODEL,
    ResourceCreatorRegistration(LineFollowerModule.new_resource, LineFollowerModule.validate_config)
)

async def main():
    """
    Main entry point for the Viam module.
    """
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    print("Done.")
```

## Follow a colored object

This module uses a vision service and a motor to program a machine to follow an object.

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
  "attributes": {},
  "depends_on": []
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
  },
  "depends_on": ["my-board"]
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
  },
  "depends_on": ["my-board"]
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
  },
  "depends_on": ["leftm", "rightm"]
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
},
```

### Code

```python {class="line-numbers linkable-line-numbers"}
import asyncio
from typing import List, Literal

from viam.robot.client import RobotClient
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

class ObjectTrackingBaseAPI(ResourceBase):
    """
    ObjectTrackingBaseAPI represents a custom API for controlling a base based on object tracking.
    """
    SUBTYPE = Subtype("example-namespace", "example-module", "object_tracking_base")

    async def start_object_tracking(self):
        raise NotImplementedError

    async def stop_object_tracking(self):
        raise NotImplementedError

def leftOrRight(detections: List[Detection], midpoint: float) -> Literal[0, 1, 2, -1]:
    """
    Get largest detection box and see if its center is in the left, center, or right third.
    Returns 0 for left, 1 for center, 2 for right, -1 if nothing detected.
    """
    largest_area = 0
    largest_detection: Detection = None # Initialize with None or a default Detection object

    if not detections:
        print("nothing detected :(")
        return -1

    for d in detections:
        # Calculate area using x_max, x_min, y_max, y_min
        area = (d.x_max - d.x_min) * (d.y_max - d.y_min)
        if area > largest_area:
            largest_area = area
            largest_detection = d

    if largest_detection is None: # Should not happen if detections is not empty, but for safety
        return -1

    # Calculate center X of the largest detection
    centerX = largest_detection.x_min + (largest_detection.x_max - largest_detection.x_min) / 2

    # Determine if center is left, center, or right
    if centerX < midpoint - midpoint / 6:
        return 0  # on the left
    elif centerX > midpoint + midpoint / 6:
        return 2  # on the right
    else:
        return 1  # basically centered

# Implement your custom control logic module
class ObjectTrackingBaseModule(Module, ObjectTrackingBaseAPI):
    MODEL = Model("example-namespace", "example-module", "object_tracking_base_module")

    def __init__(self, name: str):
        super().__init__(name)
        self.base: Base = None
        self.camera: Camera = None
        self.detector: VisionClient = None
        self.camera_name: str = "my_camera" # Default camera name, adjust in config if needed

        self._running_loop = False
        self._loop_task = None

        # Control parameters (can be configured via module config if desired)
        self.spin_num = 10         # when turning, spin the motor this much
        self.straight_num = 300    # when going straight, spin motor this much
        self.vel = 500             # go this fast when moving motor
        self.num_cycles = 200      # run the loop X times (module will run indefinitely if _running_loop is True)

    @classmethod
    def new_resource(cls, config: ComponentConfig):
        # You can parse attributes from the config here if you want to make
        # camera_name, spin_num, etc. configurable from the Viam app.
        # For simplicity, using defaults/hardcoded names for now.
        return cls(config.name)

    async def start(self):
        """
        Called when the module starts. Get references to components.
        """
        print(f"ObjectTrackingBaseModule '{self.name}' starting...")
        # Access components directly from the robot object provided by the module framework
        self.base = await Base.from_robot(self.robot, "my_base")
        self.camera = await Camera.from_robot(self.robot, self.camera_name)
        # Replace "my_color_detector" with your actual vision service name
        self.detector = await VisionClient.from_robot(self.robot, "my_object_detector")
        print(f"ObjectTrackingBaseModule '{self.name}' started.")

    async def close(self):
        """
        Called when the module is shutting down. Clean up tasks.
        """
        print(f"ObjectTrackingBaseModule '{self.name}' closing...")
        await self.stop_object_tracking()
        print(f"ObjectTrackingBaseModule '{self.name}' closed.")

    async def _object_tracking_loop(self):
        """
        The core object tracking and base control logic loop.
        """
        print("Object tracking control loop started.")

        # Get initial frame to determine midpoint for detection logic
        # This assumes the camera resolution doesn't change during operation
        initial_frame = await self.camera.get_image(mime_type="image/jpeg")
        pil_initial_frame = viam_to_pil_image(initial_frame)
        midpoint = pil_initial_frame.size[0] / 2

        cycle_count = 0
        while self._running_loop and (self.num_cycles == 0 or cycle_count < self.num_cycles):
            try:
                detections = await self.detector.get_detections_from_camera(self.camera_name)

                answer = leftOrRight(detections, midpoint)

                if answer == 0:
                    print("Detected object on left, spinning left.")
                    await self.base.spin(self.spin_num, self.vel)     # CCW is positive
                    await self.base.move_straight(self.straight_num, self.vel)
                elif answer == 1:
                    print("Detected object in center, moving straight.")
                    await self.base.move_straight(self.straight_num, self.vel)
                elif answer == 2:
                    print("Detected object on right, spinning right.")
                    await self.base.spin(-self.spin_num, self.vel) # CW is negative
                    await self.base.move_straight(self.straight_num, self.vel)
                else: # answer == -1 (nothing detected)
                    print("No object detected, stopping base.")
                    await self.base.stop() # Stop if nothing is detected

            except Exception as e:
                print(f"Error in object tracking loop: {e}")

            cycle_count += 1
            await asyncio.sleep(0.1) # Small delay to prevent busy-waiting

        print("Object tracking loop finished or stopped.")
        await self.base.stop() # Ensure base stops when loop ends
        self._running_loop = False # Reset state

    async def start_object_tracking(self):
        """
        Starts the background loop for object tracking and base control.
        """
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._object_tracking_loop())
            print("Requested to start object tracking loop.")
        else:
            print("Object tracking loop is already running.")

    async def stop_object_tracking(self):
        """
        Stops the background loop for object tracking and base control.
        """
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task # Wait for the task to complete its current iteration and exit
                self._loop_task = None
            print("Requested to stop object tracking loop.")
        else:
            print("Object tracking loop is not running.")

# Register your module
Registry.register_resource_creator(
    ObjectTrackingBaseAPI.SUBTYPE,
    ObjectTrackingBaseModule.MODEL,
    ResourceCreatorRegistration(ObjectTrackingBaseModule.new_resource, ObjectTrackingBaseModule.validate_config)
)

async def main():
    """
    Main entry point for the Viam module.
    """
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    print("Done.")
```

### Notify when a certain object appears in a video feed

This module uses a vision service to program a machine to send a notification when a certain object appears in a video feed.

### Prerequisites

- An SBC, for example a Raspberry Pi 4
- A webcam

### Configure your machine

Follow the [setup guide](/operate/get-started/setup/) to create a new machine.

Connect your SCUTTLE base to your SBC.
Add the following `components` configuration:

```json

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


### Code


```python
import asyncio
import os
from typing import List, Literal, Mapping, Any

from viam.robot.client import RobotClient
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.media.utils.pil import pil_to_viam_image, viam_to_pil_image
from viam.module.module import Module
from viam.resource.types import Model, Subtype
from viam.resource.base import ResourceBase
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.proto.app.v1 import ComponentConfig
from viam.services.vision import Detection
from viam.services.generic import Generic
import smtplib
from email.mime.text import MIMEText

class EmailNotifierModule(Module, Generic):
    MODEL = Model("example-namespace", "example-module", "email_notifier_generic")

    def __init__(self, name: str):
        super().__init__(name)
        self.camera: Camera = None
        self.detector: VisionClient = None
        self.camera_name: str = "my_camera" # Default camera name, adjust in config if needed
        self.detector_name: str = "my_object_detector" # Default vision service name
        self.target_object_name: str = "person" # The object to detect for notification

        # Email configuration (sensitive info should ideally be managed securely, e.g., environment variables)
        self.sender_email: str = os.getenv("SENDER_EMAIL", "your_email@example.com")
        self.sender_password: str = os.getenv("SENDER_PASSWORD", "your_email_password")
        self.receiver_email: str = os.getenv("RECEIVER_EMAIL", "recipient_email@example.com")
        self.smtp_server: str = os.getenv("SMTP_SERVER", "smtp.example.com")
        self.smtp_port: int = int(os.getenv("SMTP_PORT", 587)) # Typically 587 for TLS

        self._running_loop = False
        self._loop_task = None
        self._notification_sent = False

    @classmethod
    def new_resource(cls, config: ComponentConfig):
        # Parse attributes from the config here to make them configurable
        module = cls(config.name)
        if "camera_name" in config.attributes.fields:
            module.camera_name = config.attributes.fields["camera_name"].string_value
        if "detector_name" in config.attributes.fields:
            module.detector_name = config.attributes.fields["detector_name"].string_value
        if "target_object_name" in config.attributes.fields:
            module.target_object_name = config.attributes.fields["target_object_name"].string_value

        # Email configuration can also be set via config, but environment variables are often preferred for secrets
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
        """
        Called when the module starts. Get references to components.
        """
        print(f"EmailNotifierModule '{self.name}' starting...")
        self.camera = await Camera.from_robot(self.robot, self.camera_name)
        self.detector = await VisionClient.from_robot(self.robot, self.detector_name)
        print(f"EmailNotifierModule '{self.name}' started. Monitoring for '{self.target_object_name}'.")

    async def close(self):
        """
        Called when the module is shutting down. Clean up tasks.
        """
        print(f"EmailNotifierModule '{self.name}' closing...")
        await self._stop_detection_monitoring_internal() # Call internal stop method
        print(f"EmailNotifierModule '{self.name}' closed.")

    def _send_email(self, subject: str, body: str):
        """
        Helper function to send an email.
        """
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.receiver_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls() # Secure the connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print(f"Email sent successfully to {self.receiver_email}: '{subject}'")
            self._notification_sent = True # Mark that notification has been sent
        except Exception as e:
            print(f"Failed to send email: {e}")
            self._notification_sent = False # Reset if sending failed

    async def _detection_monitoring_loop(self):
        """
        The core object detection monitoring and email notification logic loop.
        """
        print("Detection monitoring loop started.")

        while self._running_loop:
            try:
                detections = await self.detector.get_detections_from_camera(self.camera_name)

                object_detected = False
                for d in detections:
                    if d.class_name == self.target_object_name:
                        object_detected = True
                        break

                if object_detected and not self._notification_sent:
                    subject = f"Viam Module Alert: {self.target_object_name} Detected!"
                    body = f"A {self.target_object_name} was detected by the vision service '{self.detector_name}' on camera '{self.camera_name}'."
                    print(f"Detected '{self.target_object_name}'. Sending email notification...")
                    self._send_email(subject, body)
                elif not object_detected and self._notification_sent:
                    # Reset notification status if the object is no longer detected,
                    # allowing another notification if it reappears.
                    print(f"'{self.target_object_name}' no longer detected. Resetting notification status.")
                    self._notification_sent = False
                elif object_detected and self._notification_sent:
                    print(f"'{self.target_object_name}' still detected, but notification already sent.")
                else: # not object_detected and not self._notification_sent
                    print(f"'{self.target_object_name}' not detected.")

            except Exception as e:
                print(f"Error in detection monitoring loop: {e}")

            await asyncio.sleep(5) # Check every 5 seconds

        print("Detection monitoring loop finished or stopped.")
        self._notification_sent = False # Reset state when loop stops

    async def _start_detection_monitoring_internal(self):
        """
        Internal method to start the background loop.
        """
        if not self._running_loop:
            self._running_loop = True
            self._loop_task = asyncio.create_task(self._detection_monitoring_loop())
            print("Requested to start detection monitoring loop.")
            return {"status": "started"}
        else:
            print("Detection monitoring loop is already running.")
            return {"status": "already_running"}

    async def _stop_detection_monitoring_internal(self):
        """
        Internal method to stop the background loop.
        """
        if self._running_loop:
            self._running_loop = False
            if self._loop_task:
                await self._loop_task # Wait for the task to complete its current iteration and exit
                self._loop_task = None
            print("Requested to stop detection monitoring loop.")
            return {"status": "stopped"}
        else:
            print("Detection monitoring loop is not running.")
            return {"status": "not_running"}

    async def do_command(self, command: Mapping[str, Any], *, timeout: float | None = None, **kwargs) -> Mapping[str, Any]:
        """
        Implement the do_command method to expose custom functionality.
        """
        if "start_monitoring" in command:
            print("Received 'start_monitoring' command via do_command.")
            return await self._start_detection_monitoring_internal()
        elif "stop_monitoring" in command:
            print("Received 'stop_monitoring' command via do_command.")
            return await self._stop_detection_monitoring_internal()
        else:
            raise NotImplementedError(f"Command '{command}' not recognized.")

# Register your module
Registry.register_resource_creator(
    Generic.SUBTYPE, # Register as a Generic service
    EmailNotifierModule.MODEL,
    ResourceCreatorRegistration(EmailNotifierModule.new_resource, EmailNotifierModule.validate_config)
)

async def main():
    """
    Main entry point for the Viam module.
    """
    await Module.serve()

if __name__ == "__main__":
    asyncio.run(main())
    print("Done.")
```