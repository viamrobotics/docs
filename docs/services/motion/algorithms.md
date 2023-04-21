---
title: "Use Motion Planning Algorithms"
linkTitle: "Algorithms"
weight: 20
type: "docs"
description: "Choose a planning algorithm to fit your desired Motion Service behavior."
---

Viam implements two planning algorithms, both based in principle on [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).

## RRT*-Connect

RRT*-Connect is an asypmptotically optimal planner that samples the planning space randomly, connecting viable paths as it finds them.
It will continue sampling after it finds its first valid path, and if it finds future paths that are more efficient, it will update to report those instead.
For Viam, efficiency/path quality is measured in terms of total kinematics state excursion.
For an arm, this refers to joints; the total amount of joint change will be minimized.
For a gantry, this refers to the amount of linear movement.
This algorithm is able to route around obstacles, but is unable to satisfy topological constraints.

## CBiRRT

CBiRRT stands for Constrained, Bidirectional implementation of [RRT](https://en.wikipedia.org/wiki/Rapidly-exploring_random_tree).
It will create paths which are guaranteed to conform to specified constraints, and attempt to smooth them afterwards as needed.
By default, it will use a "free" constraint, that is, it will not constrain the path of motion at all.
This is to ensure that paths will be found when using defaults.
CBiRRT will return the first valid path that it finds.
The CBiRRT algorithm used by Viam is based on the algorithm described in this paper: <https://www.ri.cmu.edu/pub_files/2009/5/berenson_dmitry_2009_2.pdf>

By default, Viam uses a hybrid approach.
First, RRT*-Connect is run for 1.5 seconds.
If a path is not returned, then CBiRRT is called to attempt to find a path, as it takes a more incremental approach which tends to be more likely to find paths in more difficult, constrained scenarios.
If CBiRRT is successful, then this path will be returned.
If unsuccessful, an error is returned.
However, if RRT*-Connect is initially successful, the path will be evaluated for optimality.
If the total amount of joint excursion is more than double the minimum possible to go directly to the best Inverse Kinematics solution, then CBiRRT will be run to attempt to get a better path than what RRT*-Connect was able to create.
The two paths will be smoothed, then compared to one another, and the most optimal path will be returned.
