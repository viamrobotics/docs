---
linkTitle: "Geometry constructors"
title: "Geometry constructors"
weight: 40
layout: "docs"
type: "docs"
description: "Construct each geometry type a visual or an obstacle can carry, in JSON, Python, and Go."
---

Every geometry a visual or an obstacle carries is a `Geometry` proto: a box, sphere,
capsule, mesh, or point cloud. The Python and Go SDKs construct that proto directly, with
no helper library; the box, sphere, and capsule primitives also have a machine config
(JSON) form. The transform or `WorldState` you attach the geometry to supplies its
reference frame and pose. For what a geometry means to the scene and to the planner, see
[Visuals and collisions](/visualization/visuals-and-collisions/).

## Box

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

## Sphere

A sphere takes a radius in millimeters: the `r` key in JSON, the `radius_mm`
field in the proto.

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

## Capsule

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

## Mesh

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

## Point cloud

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

- [Visuals and collisions](/visualization/visuals-and-collisions/): what a transform
  carries and why a scene visual is not automatically a planner obstacle.
- [Geometry types](/motion-planning/obstacles/overview/#geometry-types): choosing a type
  to approximate a physical object.
- [draw library](/visualization/reference/draw-library/): the Go helpers that assemble a
  geometry into a transform.
