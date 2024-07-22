---
title: "About the Motion Planning Algorithms"
linkTitle: "Algorithms"
weight: 20
type: "docs"
description: "Information about the motion planning algorithms Viam uses."
aliases:
  - "/services/motion/algorithms/"
  - "/mobility/motion/algorithms/"
no_service: true
---

Robotic motion planning is heavily reliant on planning algorithms to determine how to achieve motion for a particular scenario.
Many algorithms already exist for this problem, and motion planning is a domain where improvements and novel developments occur frequently.
Viam does not implement all motion planning algorithms but has implemented a few in its strategy for planning general robot motion.
The algorithms Viam supports are all based in principle on [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree):

The algorithms that Viam uses for motion planning depend on the type of the robot in question; planning for "Kinematic Chains", consisting of Gantry and Arm components is treated differently than planning for Base components

## Kinematic Chains

### RRT\*-Connect

RRT\*-Connect is an asymptotically optimal planner that samples the planning space randomly, connecting viable paths as it finds them.
It continues sampling after it finds its first valid path, and if it finds future paths that are more efficient, it updates to report those instead.
For Viam, efficiency/path quality is measured in terms of total kinematics state excursion.
For an arm, the sum of all joint changes is minimized.
For a gantry, the sum of all linear movement is minimized.
This algorithm can route around obstacles, but cannot satisfy topological constraints.

### CBiRRT

CBiRRT stands for Constrained, Bi-directional implementation of [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).
It creates paths which conform to specified constraints, and attempts to smooth them afterwards as needed.
By default, it does not constrain the path of motion at all.
This is to ensure that paths will be found when using defaults.
CBiRRT returns the first valid path that it finds.
The CBiRRT algorithm Viam uses is based on the algorithm described in the paper [Manipulation Planning on Constraint Manifolds](https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf)

### How the motion service applies these algorithms

By default, Viam's motion planning library uses a hybrid approach:

First, Viam runs RRT*-Connect for 1.5 seconds.
If RRT*-Connect does not return a path, then Viam calls CBiRRT to attempt to find a path.
CBiRRT takes a more incremental approach which often performs better in difficult, constrained scenarios.
If CBiRRT is successful, it returns a path.
If unsuccessful, CBiRRT returns an error.
However, if RRT*-Connect is initially successful, Viam evaluates the path for optimality.
If the total amount of joint excursion is more than double the minimum possible to go directly to the best Inverse Kinematics solution, then Viam runs CBiRRT to attempt to get a better path than what RRT*-Connect was able to create.
Viam smooths the two paths, then compares them to one another, and returns the most optimal path.

## Bases

### TP-Space-RRT

This algorithm is based on the research described in the paper: [TP-Space RRT – Kinematic Path Planning of Non-Holonomic Any-Shape Vehicles](https://www.researchgate.net/publication/275584014_TP-Space_RRT_-_Kinematic_Path_Planning_of_Non-Holonomic_Any-Shape_Vehicles). This algorithm is suitable to planning for Bases since it is able to incorporate non-holonomic constraints into the planner directly to only return plans that are kinematically feasible for the base.  One such example of a constraint that this allows us to impose is a minimum turning radius constraint, which is expressed through the Base's Properties method.  

This algorithm works by exploring a series of continuous trajectory-parameter spaces (TP-space) which describe different actions the base can take (for example, turn and then go straight). This concept is then utilized within an RRT framework to compose these different actions into a series of sequential actions to be taken in order to navigate the Base to its goal.  