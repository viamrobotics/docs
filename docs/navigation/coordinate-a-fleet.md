---
linkTitle: "Coordinate a multi-robot fleet"
title: "Coordinate a multi-robot fleet"
weight: 50
layout: "docs"
type: "docs"
description: "How centralized and decentralized coordination avoid deadlock among many robots, and which Viam primitives support task hand-off across machines."
---

Picture a warehouse with a fleet of autonomous mobile robots (AMRs) moving totes
between storage and packing. Two robots approach the same narrow aisle from opposite
ends. If both enter, neither can pass and neither can back out cleanly: the aisle is
deadlocked, and the throughput of the whole floor drops while they wait. Scale that to
fifty robots sharing intersections, charging docks, and pick faces, and coordination
becomes the hardest part of the application. A single robot that navigates well is not
enough; the fleet has to agree on who does what and who goes where.

This page explains the coordination problem, contrasts centralized and decentralized
approaches to solving it, and maps each approach onto the Viam primitives you can build
with. It assumes you already know how to command one machine through its component and
service APIs.

## The coordination problem

Coordinating a fleet breaks down into three intertwined questions:

- **Task allocation:** which robot handles which job. Assigning the nearest free robot
  to each new pick request keeps travel time low, but a naive assignment can send three
  robots to the same zone while another region sits idle.
- **Traffic and deadlock:** how robots share physical space. Aisles, doorways, and
  charging docks are finite resources. When two robots each hold part of what the other
  needs, such as opposite ends of a one-lane aisle, they can wait on each other
  indefinitely. Avoiding this requires reserving space in advance or detecting and
  resolving the standoff.
- **Shared state:** how robots agree on a common picture. A map of which zones are
  occupied, which jobs are claimed, and which docks are free has to stay consistent
  across machines that each see only their own surroundings.

The design choice that shapes all three is where the decisions are made.

## Centralized coordination

In a centralized design, a coordinator service holds the authoritative view of the
fleet and hands out instructions. Robots report their status and requests to the
coordinator; the coordinator allocates tasks, reserves zones, and grants passage. Before
a robot enters the contested aisle, it asks the coordinator for a reservation. The
coordinator grants the aisle to one robot at a time and queues the other, so the
deadlock never forms.

The strength of this approach is global reasoning. Because one component sees every
robot and every reservation, it can allocate tasks optimally, prevent deadlock by
construction, and give operators a single place to observe and override behavior. The
trade-offs are that the coordinator is a single point of failure, it can become a
throughput bottleneck as the fleet grows, and every robot depends on reliable
connectivity to it. Careful designs mitigate these with redundancy, regional
coordinators, and fallback behavior for when a robot loses contact.

## Decentralized coordination

In a decentralized design, robots negotiate locally. Each robot carries its own share of
the decision logic and resolves conflicts with the neighbors it can currently sense or
reach. At the aisle, the two robots exchange messages and settle who proceeds first
using an agreed rule, such as the robot with the higher-priority job or the one already
partway in.

The strength here is resilience and scale. There is no central bottleneck, robots keep
working when connectivity to the cloud drops, and adding robots does not overload one
component. The trade-off is that local decisions can be globally suboptimal, and
guaranteeing freedom from deadlock is harder to prove when no single component sees the
whole picture. Robust decentralized systems lean on well-chosen priority rules and
protocols that provably break symmetric standoffs.

Most production fleets blend the two: a coordinator sets high-level goals and zone
policy while robots handle immediate, latency-sensitive conflicts on their own.

## Which Viam primitives support fleet coordination

Viam gives you the building blocks for either approach rather than a turnkey traffic
manager. You compose the coordination layer yourself from these primitives:

- **Each robot is an independent machine.** You drive its motion, sensing, and
  navigation through the standard component and service
  [APIs](/reference/apis/). Any coordinator, or any peer robot, commands a machine
  through the same interfaces you already use for one robot.
- **A coordinator can run as an application or service.** Build it with the
  [fleet management API](/reference/apis/) to enumerate machines, read their status,
  and act on the fleet as a whole. The coordinator can live in the cloud or on a machine
  on the floor.
- **Machine-to-machine communication** lets robots and coordinators talk directly.
  [Machine-to-machine comms](/reference/machine-to-machine-comms/) support both the
  centralized pattern, where robots call a coordinator, and the decentralized pattern,
  where peers negotiate.
- **Shared data in the cloud** provides common state. Robots write occupancy, claimed
  jobs, and dock status to Viam's cloud data, and other machines and services read it to
  form a shared picture of the fleet.
- **Scheduled jobs** run coordination logic on a cadence. Use jobs to rebalance task
  allocation, expire stale zone reservations, or sweep for stuck robots without keeping
  a process running continuously.

Fleet management, the APIs, machine-to-machine comms, shared data, and jobs are the
pieces; the allocation policy, reservation scheme, and deadlock-resolution rules are
the part you design for your application. Viam supplies robust, tested primitives so
that your effort goes into the coordination logic rather than the plumbing.

## Next steps

- Learn how [fleet management](/fleet/) organizes and operates many machines.
- Review the [component and service APIs](/reference/apis/) you use to command each
  machine.
- See [machine-to-machine communication](/reference/machine-to-machine-comms/) for
  direct links between machines and coordinators.
