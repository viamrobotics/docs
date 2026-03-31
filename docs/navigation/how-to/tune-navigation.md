---
linkTitle: "Tune navigation"
title: "Tune navigation behavior"
weight: 50
layout: "docs"
type: "docs"
description: "Adjust speed, deviation threshold, and polling for your environment and GPS accuracy."
---

The navigation service starts with defaults that work for slow outdoor
robots with standard GPS. As you test in your environment, you'll want to
adjust these parameters.

All parameters can be changed in the Viam app without restarting
`viam-server`. Changes take effect on the next navigation cycle.

## Speed

| Parameter        | Default | What it controls                                            |
| ---------------- | ------- | ----------------------------------------------------------- |
| `meters_per_sec` | 0.3     | Linear speed. How fast the robot drives in a straight line. |
| `degs_per_sec`   | 20.0    | Angular speed. How fast the robot turns.                    |

**When to increase speed:** Your robot's motors and terrain support faster
movement, and your obstacle detection polling is fast enough to react at
the higher speed. At 1 m/s with 1 Hz obstacle polling, the robot travels
1 meter between obstacle checks.

**When to decrease speed:** The robot overshoots waypoints, turns are too
aggressive, or obstacle detection can't keep up. Reduce angular speed
first if turns are the problem.

## Plan deviation

| Parameter          | Default | What it controls                                                                                    |
| ------------------ | ------- | --------------------------------------------------------------------------------------------------- |
| `plan_deviation_m` | 2.6     | How far the robot can drift from its planned path (in meters) before the service triggers a replan. |

This is the most important tuning parameter. Set it relative to your GPS
accuracy:

| GPS type      | GPS error | Recommended `plan_deviation_m` |
| ------------- | --------- | ------------------------------ |
| Standard GPS  | 2-5m      | 5-10m                          |
| SBAS-enhanced | 1-3m      | 3-5m                           |
| RTK GPS       | 1-10cm    | 0.5-2m                         |

**If it's too low** (below your GPS error), the robot replans constantly
because normal GPS jitter looks like path deviation. You'll see the robot
stop and recalculate frequently, making slow progress.

**If it's too high**, the robot tolerates large deviations before
correcting. It might cut corners, drift off the intended path, or approach
obstacles before replanning.

## Polling frequencies

| Parameter                       | Default | What it controls                             |
| ------------------------------- | ------- | -------------------------------------------- |
| `position_polling_frequency_hz` | 1.0     | How often to check the robot's GPS position. |
| `obstacle_polling_frequency_hz` | 1.0     | How often to query obstacle detectors.       |

**Position polling** determines how quickly the service detects that the
robot has deviated from its plan. At 1 Hz, a deviation takes up to 1
second to detect. For fast-moving robots, increase this.

**Obstacle polling** determines how quickly new obstacles are detected.
Higher values improve reaction time but increase CPU and camera bandwidth
usage. Balance against your robot's speed: at 0.3 m/s and 1 Hz, the robot
moves 30 cm between checks. At 1 m/s, it moves 1 meter.

## Tuning workflow

1. **Start with defaults.** Navigate to a nearby waypoint in an open area
   with no obstacles.
2. **Check for excessive replanning.** If the robot stops frequently to
   recalculate, increase `plan_deviation_m`. Watch the Control tab map to
   see when replans happen.
3. **Adjust speed.** Increase `meters_per_sec` gradually. Watch for
   overshooting waypoints or unstable turns.
4. **Add obstacle detection.** Once basic navigation works, add obstacle
   detectors and test with known obstacles.
5. **Adjust polling.** If the robot doesn't detect obstacles quickly
   enough, increase `obstacle_polling_frequency_hz`. If the robot is
   slow because of excessive polling, decrease it.

## What's next

- [Navigation service configuration](/navigation/reference/navigation-service/):
  full reference for all parameters.
- [Monitor and troubleshoot](/navigation/how-to/monitor-and-troubleshoot/):
  debug navigation problems using the Control tab and logs.
