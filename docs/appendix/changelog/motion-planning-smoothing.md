---
title: Motion planning path smoothing
date: "2022-12-01"
color: "improved"
---

- RRT\* paths now undergo rudimentary smoothing, resulting in improvements to path quality with negligible change to planning performance.
- Plan manager now performs direct interpolation for any solution within some factor of the best score, instead of only in the case where the best inverse kinematics solution could be interpolated.
