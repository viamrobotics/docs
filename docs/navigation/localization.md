---
linkTitle: "How a robot knows where it is"
title: "How a robot knows where it is"
weight: 10
layout: "docs"
type: "docs"
description: "Understand localization: how a robot estimates its own pose from odometry, GPS, and SLAM, and how to choose the right sensors for a deployment."
---

A cleaning robot finishes a run and needs to return to its charging dock.
To drive back, it has to answer one question: where am I right now?
The dock sits at a fixed spot, but the robot has been turning and rolling around a room for an hour.
Answering that question is called **localization**: estimating the robot's **pose** (its position and orientation) within a chosen reference **frame**, such as the corner of the room or a point on the globe.

In Viam, a pose lives in the frame system, which tracks where each part of a machine sits relative to a common origin.
Localization is the process of keeping the robot's own pose in that frame accurate as it moves.
No single sensor answers "where am I" perfectly, so it helps to understand the three common sources and what each one is good at.

## Odometry: counting your own motion

Wheel **odometry** estimates pose by adding up the robot's own movement.
Encoders on the wheels report how far each wheel turned; from those counts and the robot's geometry, the software integrates a running estimate of how far and which way the robot traveled.
This technique is called **dead reckoning**: you start from a known pose and accumulate motion to guess your current one.

Odometry is cheap, works anywhere, and updates quickly.
Its weakness is **drift**.
Every wheel slip, uneven tile, or rounding error adds a small mistake to the estimate, and because dead reckoning has no outside reference to check against, those small mistakes accumulate.
After a long run the estimated pose can be meters away from the true pose, even though each individual reading looked reasonable.
Drift is why a robot that relies only on odometry gradually loses track of the dock.

Viam exposes wheel odometry through the [movement sensor](/reference/components/movement-sensor/) component, using the `wheeled-odometry` model, which derives velocity and position from motor encoders.

## GPS: an absolute outdoor fix

**GPS** takes the opposite approach.
Instead of accumulating motion, a GPS receiver reports an **absolute** position from satellite signals, expressed as latitude and longitude.
Because each reading is independent, GPS does not drift: an error in one reading does not corrupt the next.

The trade-offs are environment and precision.
GPS needs a clear view of the sky, so it works outdoors but degrades or fails indoors, in tunnels, and under dense cover.
Standard GPS is accurate to a few meters, which is fine for a lawn robot crossing a yard but too coarse to dock precisely.
In Viam, GPS receivers and inertial measurement units (IMUs) are also [movement sensor](/reference/components/movement-sensor/) models, so the same component API surfaces both absolute position and orientation.

## SLAM: building a map while you use it

**SLAM** (Simultaneous Localization and Mapping) works where GPS cannot reach.
The robot builds a map of its surroundings from a range sensor such as a LIDAR or depth camera, and at the same time uses that map to figure out where it sits within it.
Matching current sensor readings against the map gives an absolute pose relative to the mapped space, so SLAM corrects drift the way GPS does, but indoors.

The cost is hardware and computation: SLAM needs a capable range sensor and more processing than reading an encoder, and its accuracy depends on the environment having enough structure to recognize.
Viam provides SLAM through the [SLAM service](/navigation/slam-and-mapping/).

## Comparing the three sources

| Source   | Reference                    | Drift over time | Environment        | Relative cost                   |
| -------- | ---------------------------- | --------------- | ------------------ | ------------------------------- |
| Odometry | Relative (integrated motion) | Accumulates     | Anywhere           | Low (encoders)                  |
| GPS      | Absolute (satellite)         | None            | Outdoor, open sky  | Low to medium (receiver)        |
| SLAM     | Absolute (built map)         | None            | Indoor, structured | Higher (range sensor + compute) |

The key split is **relative** versus **absolute**.
Odometry is relative: it tells you how you moved but never resets, so it drifts.
GPS and SLAM are absolute: each fix is anchored to an outside reference, so they stay bounded but depend on their environment and cost more to run.

## Why fuse relative and absolute sources

The two kinds of source complement each other, which is why many deployments combine them.
Odometry updates fast and smoothly but drifts; an absolute source updates the true position but can be slow, noisy, or briefly unavailable (a GPS signal drops under a bridge, or a SLAM scan finds a bare hallway).
Sensor fusion blends them: odometry fills in the fast, in-between motion, while the absolute source periodically corrects the accumulated drift.
The result is an estimate that is both smooth and bounded, better than either source alone.
For how Viam combines readings from several movement sensors into one pose estimate, see [sensor fusion](/navigation/sensor-fusion/).

## Choosing sources for a deployment

Which sources a machine needs follows from where it runs and how precise it must be.

- **Outdoor, meter-scale** (a lawn mower, a field rover): a GPS movement sensor gives absolute position; add wheel odometry or an IMU so the estimate stays smooth between GPS updates and survives brief signal loss.
- **Indoor, no GPS** (a warehouse or home robot): use SLAM with a LIDAR or depth camera for absolute indoor localization, fused with odometry for fast updates.
- **Short, controlled runs** (a robot that never strays far from a known start): odometry alone can be enough, since drift stays small over a short distance and time.
- **High precision anywhere** (docking, tight aisles): pair an absolute source with odometry, because odometry alone will not stay accurate long enough to line up.

Start from the environment to rule sources in or out (GPS outdoors, SLAM indoors), then decide whether the required precision and run length demand an absolute source at all.
That decision tells you which [movement sensors](/reference/components/movement-sensor/) or range sensors to put on the machine.

## Next steps

- [Movement sensor component](/reference/components/movement-sensor/): configure GPS, IMU, and wheeled-odometry models.
- [SLAM and mapping](/navigation/slam-and-mapping/): build and use maps for indoor localization.
- [Sensor fusion](/navigation/sensor-fusion/): combine relative and absolute sources into one pose estimate.
