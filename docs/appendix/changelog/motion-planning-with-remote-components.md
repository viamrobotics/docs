---
title: Motion planning with remote components
date: "2023-12-01"
color: "improved"
---

The [motion service](/mobility/motion/) is now agnostic to the networking topology of a machine.

- Kinematic information is now transferred over the robot API.
  This means that the motion service is able to get kinematic information for every component on the machine, regardless of whether it is on a main or remote viam-server.
- Arms are now an input to the motion service.
  This means that the motion service can plan for a machine that has an arm component regardless of whether the arm is connected to a main or {{< glossary_tooltip term_id="remote" text="remote" >}} instance of `viam-server`.
