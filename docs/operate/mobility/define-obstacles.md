---
linkTitle: "Define static obstacles"
title: "Define static obstacles to avoid"
weight: 20
layout: "docs"
type: "docs"
description: "Spatially describe your robot's working environment for collision avoidance."
---

To prevent your machine from colliding with objects or surfaces in its environment, you can define obstacles and include them in calls to the [motion service API](/dev/reference/apis/services/motion/).
The motion service will take into account the obstacles as well as the geometry of the machine itself when planning motion.

Start by [defining your machine's geometry](/operate/mobility/define-geometry/) so that you can define the obstacles with respect to the machine's reference frame.

Next, define one or more obstacles.
Here is a Python example from the [Add constraints and transforms to a motion plan guide](/tutorials/services/constrain-motion/#modify-your-robots-working-environment):

```python {class="line-numbers linkable-line-numbers"}
box_origin = Pose(x=400, y=0, z=50+z_offset)
box_dims = Vector3(x=120.0, y=80.0, z=100.0)
box_object = Geometry(center=box_origin,
                      box=RectangularPrism(dims_mm=box_dims))

obstacles_in_frame = GeometriesInFrame(reference_frame="world",
                                       geometries=[table_object, box_object])
```

Finally, pass your obstacles to the motion planning API.
See the API documentation for the following methods which can take into account obstacles:

- [Move](/dev/reference/apis/services/motion/#move)
  - Obstacles are passed as part of the `world_state` parameter
- [MoveOnMap](/dev/reference/apis/services/motion/#moveonmap)
- [MoveOnGlobe](/dev/reference/apis/services/motion/#moveonglobe)

## Tutorials and example usage

{{< cards >}}
{{% card link="/tutorials/services/constrain-motion/" %}}
{{% card link="/tutorials/projects/claw-game/" %}}
{{< /cards >}}
