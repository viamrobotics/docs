---
title: World frame
id: world-frame
full_link: /operate/mobility/move-arm/frame-how-to/
short_description: The fixed, user-defined global coordinate system that is the reference point for all other coordinate frames in a robotic system.
aka: world frame, world
---

The world reference [frame](/operate/reference/services/frame-system/) is the fixed, global coordinate system that serves as the reference point for all other coordinate frames in a robotic system.
It provides a consistent basis for describing the position and orientation of robots, components, and objects in the physical space.
All other coordinate frames (such as machine frames and component frames) are defined relative to this world frame, either directly or through a chain of transformations.

The user chooses the world frame, and defines it implicitly.
For example, if you have a robot arm mounted on a table and you define the arm's origin frame as having no translation or orientation relative to the world frame, then the arm's origin frame is the origin of the world frame.
