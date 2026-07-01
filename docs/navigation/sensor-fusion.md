---
linkTitle: "Sensor fusion"
title: "Combine sensors with sensor fusion"
weight: 30
layout: "docs"
type: "docs"
description: "Understand what sensor fusion means, how it differs from Viam's merged movement sensor, and when combining an IMU with an absolute source produces a steadier pose estimate."
---

Picture a wheeled robot reporting where it is.
Its inertial measurement unit (IMU) updates hundreds of times a second and tracks fast, smooth motion, but its position estimate slowly slides away from the truth as small errors pile up.
A GPS receiver on the same robot reports an absolute position that never drifts, but it updates slowly and jumps around by a meter or more from one reading to the next.
Neither source alone gives you a position estimate that is both steady and correct.
Combine them, and you can get a pose that is smooth like the IMU and anchored like the GPS.

That combination is the idea behind sensor fusion.

## What sensor fusion is

Sensor fusion takes several noisy measurements of the same thing and blends them into a single estimate that is better than any input on its own.
The classic tool for this is a Kalman filter.
At a high level, a Kalman filter keeps a running estimate of the robot's state, such as position and velocity, along with a measure of how confident it is in that estimate.
Each new sensor reading updates the estimate in proportion to how trustworthy that reading is: a precise measurement pulls the estimate strongly, a noisy one nudges it gently.
The filter also predicts how the state should change between readings using motion, so it can smooth over gaps and reject outliers.

The result is a continuous estimate that carries information from every source at once.
A fused pose reflects the IMU's fast, fine-grained motion and the GPS's absolute anchor in the same number, weighted by how much each sensor can be trusted moment to moment.

## How Viam's `merged` movement sensor differs

Viam ships a [`merged` movement sensor](/components/movement-sensor/) model, and the name invites a natural assumption.
It is worth being precise, so you set the right expectations.

The `merged` model performs **selection and aggregation**, not statistical fusion.
You configure it by property, such as `position`, `orientation`, or `angular_velocity`, and for each property you list one or more source sensors.
When your code requests a reading, `merged` returns the value from the first sensor in that property's list that answers without error.
If that sensor fails or is unavailable, `merged` falls through to the next one.

This design does two useful things:

- **Aggregation across sensors.**
  A GPS reports position and a separate IMU reports orientation and angular velocity.
  `merged` presents both through one movement sensor client, so your application reads a complete pose from a single component instead of juggling several.
- **Failover within a property.**
  If you list two sensors that both report angular velocity, `merged` uses the first one that responds and switches to the second only when the first errors.

What `merged` does not do is blend two readings of the same quantity into a weighted average.
If two sensors both report position, `merged` picks one of them for each reading; it does not compute a combined position that is more accurate than either.
In short, `merged` is an excellent way to assemble a full set of readings from complementary hardware and to stay running when a sensor drops out, but it is not the Kalman-filter-style estimator described above.

## When fusing an IMU with an absolute source helps

True fusion earns its keep when your sources have complementary strengths and weaknesses.
The textbook pairing is a high-rate relative sensor with a low-rate absolute one:

- An **IMU** measures acceleration and rotation at a high rate.
  Integrating those measurements gives smooth, responsive short-term motion, but the estimate drifts over seconds to minutes because integration accumulates error.
- An **absolute source**, such as GPS outdoors or a localization service indoors, reports position in a fixed frame that does not drift, but updates slowly and carries per-reading noise.

Fusing the two lets each cover the other's weak spot.
The IMU fills the gaps between slow absolute updates and keeps the pose smooth during fast maneuvers.
The absolute source corrects the IMU's accumulated drift every time it reports, pinning the estimate back to ground truth.
The fused pose is steady between updates and stays accurate over long runs, which is exactly what a navigation or motion system wants.

Fusion is worth the effort when:

- One sensor is fast but drifts, and another is slow but absolute.
- You need a continuous pose at a higher rate than your absolute source alone provides.
- Outlier rejection matters, because a filter that models expected motion can discount readings that jump implausibly.

Fusion buys you less when a single sensor already meets your accuracy and update-rate needs, or when your sources share the same weakness, such as two receivers that both lose signal in the same tunnel.

## Getting fusion today

Because the built-in `merged` model selects rather than fuses, a statistically fused pose in Viam comes from one of two places:

- A **custom module** that reads the raw sensors, runs a filter such as a Kalman or complementary filter, and presents the fused result as its own movement sensor or sensor.
- An **upstream source** that already fuses internally, such as a GPS/IMU receiver or a SLAM system that outputs a filtered pose, which you then configure as a single movement sensor.

Either way, the fusion lives in software you choose or hardware you select, and Viam consumes the fused output like any other movement sensor.

## Next steps

- Learn how a machine turns sensor readings into a position estimate in [Localization](/navigation/localization/).
- See the available movement sensor models, including [`merged`](/components/movement-sensor/), to decide which sensors to combine.
