---
title: "About the Motion Planning Algorithms"
linkTitle: "Algorithms"
weight: 20
type: "docs"
description: "Information about the motion planning algorithms Viam uses."
aliases:
  - "/services/motion/algorithms/"
---

Robotic motion planning is heavily reliant on planning algorithms to determine how to achieve motion for a particular scenario.
Many algorithms already exist for this problem, and motion planning is a domain where improvements and novel developments occur frequently.
Viam does not implement all motion planning algorithms but has implemented two in its strategy for planning general robot motion.
The two algorithms Viam supports are both based in principle on [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree):

## RRT\*-Connect

RRT\*-Connect is an asymptotically optimal planner that samples the planning space randomly, connecting viable paths as it finds them.
It continues sampling after it finds its first valid path, and if it finds future paths that are more efficient, it updates to report those instead.
For Viam, efficiency/path quality is measured in terms of total kinematics state excursion.
For an arm, the sum of all joint changes is minimized.
For a gantry, the sum of all linear movement is minimized.
This algorithm can route around obstacles, but cannot satisfy topological constraints.

## CBiRRT

CBiRRT stands for Constrained, Bi-directional implementation of [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).
It creates paths which conform to specified constraints, and attempts to smooth them afterwards as needed.
By default, it does not constrain the path of motion at all.
This is to ensure that paths will be found when using defaults.
CBiRRT returns the first valid path that it finds.
The CBiRRT algorithm Viam uses is based on the algorithm described in the paper [Manipulation Planning on Constraint Manifolds](https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf)

## How the motion service applies these algorithms

By default, Viam's motion planning library uses a hybrid approach:

First, Viam runs RRT*-Connect for 1.5 seconds.
If RRT*-Connect does not return a path, then Viam calls CBiRRT to attempt to find a path.
CBiRRT takes a more incremental approach which often performs better in difficult, constrained scenarios.
If CBiRRT is successful, it returns a path.
If unsuccessful, CBiRRT returns an error.
However, if RRT*-Connect is initially successful, Viam evaluates the path for optimality.
If the total amount of joint excursion is more than double the minimum possible to go directly to the best Inverse Kinematics solution, then Viam runs CBiRRT to attempt to get a better path than what RRT*-Connect was able to create.
Viam smooths the two paths, then compares them to one another, and returns the most optimal path.
