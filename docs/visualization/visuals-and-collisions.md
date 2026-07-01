---
linkTitle: "Visuals and collisions"
title: "Visuals and collisions"
weight: 10
layout: "docs"
type: "docs"
description: "How a Transform defines a custom visual, and which geometry the motion planner actually collision-checks."
---

A geometry is a simple shape, such as a box, sphere, or capsule, that represents an
object's physical extent. Viam uses one set of geometry types for two jobs: drawing a
custom visual in the 3D scene, and telling the motion planner about an obstacle.

To create a custom visual, you attach a geometry to `Transform.Geometry` and provide
that transform to a [world state store service](/reference/apis/services/world-state-store/).
This service holds the transforms you publish and streams them to the 3D scene. This
page covers what a transform contains, the difference between planner geometry and
visualization geometry, and how to build each geometry type.

## Anatomy of a transform

A `Transform` carries four things that together place and style a visual:

- **Reference frame and pose**: This defines the visual's origin.
- **Geometry**: the shape to draw (a box, sphere, capsule, mesh, or point
  cloud).
- **Metadata**: styling such as color and opacity.
- **UUID**: a stable identifier for this specific visual.

The reference frame and pose decide _where_, the geometry decides _what shape_,
and the metadata decides _how it looks_.

## The UUID gives a visual a stable identity

Each transform has a UUID. That identifier is what lets a module change one
visual without disturbing the rest of the scene: to update a visual, the module
re-sends a transform with the same UUID; to remove it, it references that UUID;
to add a new one, it uses a fresh UUID. Without stable identifiers the client
would have to re-render everything on every change. With them, the scene applies
incremental add, update, and remove operations to individual visuals.

## Metadata styles the visual

The metadata is a set of rendering attributes the scene reads when it draws the
geometry:

- `color`: the fill color
- `opacity`: how transparent the shape is
- per-point colors: for point cloud geometry
- `collision_allowed`: a rendering hint that marks the visual as a permitted
  contact, for display only

These are all **visualization attributes**: they control how the visual looks,
`collision_allowed` included. The planner reads its solid geometry from the frame
system and the [`WorldState`](/motion-planning/obstacles/) you pass to `Move`, so
metadata changes what you see without changing what the planner plans around.

## The scene draws, the planner collision-checks

The geometry on a world state store transform renders in the 3D scene: publishing a
box draws a box. The motion planner collision-checks a separate geometry, which it
reads from two places:

- The **frame system**: each component's `frame.geometry`.
- The **`WorldState`** you pass to a `Move` call: obstacles and transforms
  supplied for that single planning request.

Despite the similar names, these are different things: the
[world state store service](/reference/apis/services/world-state-store/) holds transforms
for the scene to draw, and the [`WorldState`](/motion-planning/obstacles/) you pass to
`Move` carries obstacles for the planner to avoid. A world state store transform and a
`WorldState` obstacle travel two paths, each with its own job: one is drawn in the scene,
the other is planned around. The same shape can take both paths.

## Making a geometry both visible and collision-checked

If you want a geometry to appear in the scene _and_ be avoided by the planner,
you do both, separately:

- **For the scene**: publish it as a transform through the world state store
  service (see [Publish visuals from a module](/visualization/publish-visuals-from-a-module/)).
- **For planning**: add it to the frame system, or include it in the
  `WorldState` you pass to `Move`.

Today these are two separate outputs you produce from the same source data: one
transform for the scene, one geometry for the planner.

## Geometry types

The supported types are:

- **box**: dimensions in millimeters
- **sphere**: a radius
- **capsule**: a radius and length
- **mesh**: an arbitrary triangle mesh
- **point cloud**: a set of points

Choose the type that matches what you are representing: a box or capsule to
approximate a physical object, a mesh for a precise model, a point cloud for
sensor data.

You build a geometry as a `Geometry` proto, the same type a world state store
transform and a `WorldState` obstacle both carry. The Python SDK and the Go SDK
construct that proto directly, with no helper library. The box, sphere, and
capsule primitives also have a machine config (JSON) form. The transform you
attach the geometry to supplies its reference frame and pose.

### Box

A box takes its `x`, `y`, and `z` dimensions in millimeters.

{{< tabs >}}
{{% tab name="JSON" %}}

```json
{ "type": "box", "x": 100, "y": 100, "z": 100 }
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.proto.common import Geometry, RectangularPrism, Vector3

box = Geometry(
    label="box",
    box=RectangularPrism(dims_mm=Vector3(x=100, y=100, z=100)),
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import commonpb "go.viam.com/api/common/v1"

box := &commonpb.Geometry{
    Label: "box",
    GeometryType: &commonpb.Geometry_Box{
        Box: &commonpb.RectangularPrism{
            DimsMm: &commonpb.Vector3{X: 100, Y: 100, Z: 100},
        },
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### Sphere

A sphere takes a radius `radius_mm` in millimeters.

{{< tabs >}}
{{% tab name="JSON" %}}

```json
{ "type": "sphere", "r": 50 }
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.proto.common import Geometry, Sphere

sphere = Geometry(label="sphere", sphere=Sphere(radius_mm=50))
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import commonpb "go.viam.com/api/common/v1"

sphere := &commonpb.Geometry{
    Label: "sphere",
    GeometryType: &commonpb.Geometry_Sphere{
        Sphere: &commonpb.Sphere{RadiusMm: 50},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### Capsule

A capsule takes a radius and a length in millimeters. The length must be at
least twice the radius.

{{< tabs >}}
{{% tab name="JSON" %}}

```json
{ "type": "capsule", "r": 50, "l": 200 }
```

{{% /tab %}}
{{% tab name="Python" %}}

```python
from viam.proto.common import Capsule, Geometry

capsule = Geometry(
    label="capsule",
    capsule=Capsule(radius_mm=50, length_mm=200),
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import commonpb "go.viam.com/api/common/v1"

capsule := &commonpb.Geometry{
    Label: "capsule",
    GeometryType: &commonpb.Geometry_Capsule{
        Capsule: &commonpb.Capsule{RadiusMm: 50, LengthMm: 200},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### Mesh

A mesh comes from an STL or PLY file. Read the file and embed its bytes in the
geometry with a `content_type`. The renderer draws PLY, so convert an STL file
to PLY first.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from pathlib import Path

from viam.proto.common import Geometry, Mesh

mesh = Geometry(
    label="mesh",
    mesh=Mesh(content_type="ply", mesh=Path("model.ply").read_bytes()),
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "os"

    commonpb "go.viam.com/api/common/v1"
)

plyBytes, err := os.ReadFile("model.ply")
if err != nil {
    return err
}
mesh := &commonpb.Geometry{
    Label: "mesh",
    GeometryType: &commonpb.Geometry_Mesh{
        Mesh: &commonpb.Mesh{ContentType: "ply", Mesh: plyBytes},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

### Point cloud

A point cloud is sensor output, so you read it as PCD bytes in binary PCD format
and embed them in the geometry. Add a color per point in the PCD data itself.
A point cloud has no machine config form, so you build it in code.

{{< tabs >}}
{{% tab name="Python" %}}

```python
from pathlib import Path

from viam.proto.common import Geometry, PointCloud

point_cloud = Geometry(
    label="point-cloud",
    pointcloud=PointCloud(point_cloud=Path("cloud.pcd").read_bytes()),
)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
    "os"

    commonpb "go.viam.com/api/common/v1"
)

pcdBytes, err := os.ReadFile("cloud.pcd")
if err != nil {
    return err
}
pointCloud := &commonpb.Geometry{
    Label: "point-cloud",
    GeometryType: &commonpb.Geometry_Pointcloud{
        Pointcloud: &commonpb.PointCloud{PointCloud: pcdBytes},
    },
}
```

{{% /tab %}}
{{< /tabs >}}

## What's next

- [Publish visuals from a module](/visualization/publish-visuals-from-a-module/):
  implement a world state store service that publishes transforms.
- [Define obstacles](/motion-planning/obstacles/): the geometry the planner
  collision-checks.
- [Frame system](/motion-planning/frame-system/): how the planner gets the
  geometry and frames it plans around.
