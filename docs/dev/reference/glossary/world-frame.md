---
title: World Reference Frame
id: world-frame
full_link:
short_description: The fixed, user-defined global coordinate system that is the reference point for all other coordinate frames in a robotic system.
aka: world frame, world
---

The world reference frame is the fixed, global coordinate system that serves as the reference point for all other coordinate frames in a robotic system.
It provides a consistent basis for describing the position and orientation of robots, components, and objects in the physical space.
All other coordinate frames (like robot frames, component frames, etc.) are defined relative to this world frame.

The user defines the world frame.
For example, if you have a robot arm mounted on a table and you define the arm's base frame as the world frame, then the arm's base frame is the origin of the world frame.
