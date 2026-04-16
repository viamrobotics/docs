---
linkTitle: "Configure workspace obstacles"
title: "Configure workspace obstacles"
weight: 10
layout: "docs"
type: "docs"
description: "Configure the static collision geometry for your workspace through the Viam app so the motion planner routes around tables, walls, fixtures, and work-cell boundaries."
---

Static obstacles are the fixed shapes in your workspace: the table the arm is bolted to, a back wall, a ceiling, a bin the arm reaches into.
Configure them once through the Viam app and the motion planner includes them on every plan.

Three config patterns cover most cases:

| Pattern                                                                   | Use when                                                                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| [`erh:vmodutils:obstacle`](#default-obstacle-pattern)                     | Most workspace obstacles: tables, walls, fixtures, bespoke shapes. One component, any geometry.        |
| [`rdk:builtin:fake` generic component](#configure-a-single-primitive)     | A single box, sphere, or capsule when you do not want to add a registry module.                        |
| [`erh:vmodutils:obstacle-open-box`](#containers-and-work-cell-boundaries) | Containers, bins, or rectangular work-cell envelopes. Generates five geometries from outer dimensions. |

For obstacles your code builds at runtime (objects detected by vision, temporary keep-out zones), see [Plan collision-free paths](/motion-planning/obstacles/avoid-obstacles/) instead.

## Before you start

- An arm or gantry configured on a machine.
- [Frame system](/motion-planning/frame-system/) configured so the arm has a known parent frame.
- [Obstacle concepts](/motion-planning/obstacles/) read (geometry types, sizing, static versus dynamic).

## Default obstacle pattern

The `erh:vmodutils:obstacle` module accepts a list of geometries under one component, validates the config at startup, and gives each obstacle a meaningful name in your config.

### 1. Add the obstacle component

1. In the Viam app, open your machine's **CONFIGURE** tab.
2. Click the **+** icon and select **Configuration block**.
3. Search for `obstacle` and click the **gripper/obstacle** result card for the `erh:vmodutils` module.
   The Viam app installs the `erh:vmodutils` module automatically.
4. Click **Add component** on the detail page.
5. Name the component after what it represents (for example, `table`, `back-wall`, `ceiling`) and click **Add component**.

{{< alert title="Why a gripper?" color="note" >}}
The obstacle module is registered under the gripper API because that API natively exposes a `Geometries()` method, which is what the motion planner reads to pull custom collision shapes.
The component never grabs anything; treat the gripper label as cosmetic.
{{< /alert >}}

### 2. Define the geometry

On the new component's card, paste a `geometries` list into the attributes editor:

```json
{
  "geometries": [{ "type": "box", "x": 1800, "y": 1100, "z": 40 }]
}
```

For a single obstacle, the list has one entry.
For a rigid multi-part fixture (an L-bracket, a staging area with a floor and front wall), put several entries in the list and they move as one unit with the component's frame.

Supported geometry types are described in [Geometry types](/motion-planning/obstacles/#geometry-types).

### 3. Position the obstacle with a frame

Click **Frame** on the same component card.
The Frame section opens a JSON editor.
Replace the JSON with the obstacle's pose in the world:

```json
{
  "parent": "world",
  "translation": { "x": 500, "y": 0, "z": -20 },
  "orientation": {
    "type": "ov_degrees",
    "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
  }
}
```

The geometry origin sits at the center of the box, so to place a 40 mm thick table with its top surface at world z = 0, translate the frame to z = -20.

Click **Save** in the top-right of the page, or press ⌘/Ctrl+S.

### 4. Group obstacles in the sidebar

Add a `ui_folder` field to each obstacle component to collapse them under one folder in the **Resources** sidebar:

```json
"ui_folder": { "name": "obstacles" }
```

This has no effect on the motion planner.
It keeps the sidebar readable when you have six or eight obstacle components.

### Full workcell example

A bench setup with a table, a back wall, a side wall, and a ceiling, each as its own component for independent visibility toggling in **3D SCENE**:

```json
{
  "name": "table",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [{ "type": "box", "x": 1800, "y": 1100, "z": 40 }]
  },
  "frame": {
    "parent": "world",
    "translation": { "x": 500, "y": 0, "z": -20 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  },
  "ui_folder": { "name": "obstacles" }
}
```

```json
{
  "name": "back-wall",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [{ "type": "box", "x": 20, "y": 1100, "z": 1000 }]
  },
  "frame": {
    "parent": "world",
    "translation": { "x": -400, "y": 0, "z": 500 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  },
  "ui_folder": { "name": "obstacles" }
}
```

```json
{
  "name": "wall-left",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [{ "type": "box", "x": 1800, "y": 20, "z": 1000 }]
  },
  "frame": {
    "parent": "world",
    "translation": { "x": 500, "y": -550, "z": 500 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  },
  "ui_folder": { "name": "obstacles" }
}
```

```json
{
  "name": "ceiling",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle",
  "attributes": {
    "geometries": [{ "type": "box", "x": 1800, "y": 1100, "z": 20 }]
  },
  "frame": {
    "parent": "world",
    "translation": { "x": 500, "y": 0, "z": 1000 },
    "orientation": {
      "type": "ov_degrees",
      "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
    }
  },
  "ui_folder": { "name": "obstacles" }
}
```

### One obstacle per component, or many geometries per component?

Use one component per logical obstacle (table, ceiling, each wall) when the obstacles have independent positions or when you want to toggle them separately in **3D SCENE**.

Use several geometries under one component when the shapes form a rigid unit: an L-bracket, an enclosure, a tool stand with a base and a post.
The component's frame positions the whole group.

## Configure a single primitive

For a single primitive shape when you do not want to add the `erh:vmodutils` module, use a `generic`/`fake` component:

1. Click the **+** icon and select **Configuration block**.
2. Search for `generic` and click the **generic/fake** result card. Click **Add component**.
3. Name the component (for example, `table`) and click **Add component**.
4. Click **Frame** on the new component card. Replace the JSON:

   ```json
   {
     "parent": "world",
     "translation": { "x": 500, "y": 0, "z": -20 },
     "orientation": {
       "type": "ov_degrees",
       "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
     },
     "geometry": {
       "type": "box",
       "x": 1800,
       "y": 1100,
       "z": 40
     }
   }
   ```

5. Click **Save**.

The `generic`/`fake` pattern carries one geometry per component, so a multi-shape fixture needs one component per shape.
For anything beyond a single primitive, prefer `erh:vmodutils:obstacle`.

## Containers and work-cell boundaries

For containers, bins, or rectangular work-cell envelopes, use `erh:vmodutils:obstacle-open-box`.
It builds five geometries (floor plus four walls, no top) from outer dimensions.
One component covers what would take five entries in a `vmodutils:obstacle` geometries list.

The component's frame origin sits at the center of the cavity at mid-height.
Positive z faces up (the "open" side).

### Container example

A placement bin on a table, with an optional one-call action to move the arm above it:

```json
{
  "name": "placement-bin",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle-open-box",
  "attributes": {
    "length": 300,
    "width": 200,
    "height": 150,
    "thickness": 5,
    "to_move": "arm",
    "motion": "builtin",
    "offset": 50
  },
  "frame": {
    "parent": "world",
    "translation": { "x": 600, "y": 0, "z": 75 }
  },
  "ui_folder": { "name": "obstacles" }
}
```

With `to_move` set to the arm's name and `motion` set to a motion service, calling `gripper.Grab()` on this component moves the arm `offset` mm above the bin, tool-down.
You can drive that from a switch, a script, or the UI without writing a `motion.Move` call.

Leave `to_move` unset if you only want the collision geometry.

### Work-cell boundary example

A rectangular work-cell envelope with no ceiling:

```json
{
  "name": "work-cell",
  "api": "rdk:component:gripper",
  "model": "erh:vmodutils:obstacle-open-box",
  "attributes": {
    "length": 1800,
    "width": 1100,
    "height": 1000,
    "thickness": 20
  },
  "frame": {
    "parent": "world",
    "translation": { "x": 500, "y": 0, "z": 500 }
  },
  "ui_folder": { "name": "obstacles" }
}
```

This gives a floor plus four walls in one component.
If the arm can reach above its envelope (ceiling-mounted installations, tall arms), add a separate `erh:vmodutils:obstacle` for the ceiling.

### Caveats

- **Opens in +z only.** If your container opens in a different direction, rotate the whole component through the frame's `orientation`, but note that the `Grab` action assumes a tool-down approach regardless.
- **Rectangular only.** L-shaped cells or irregular enclosures need multiple components.
- **Thickness defaults to 1 mm.** Thin but still a solid collision surface. Raise it for visual clarity in **3D SCENE** or for a wider safety margin.

## Attach geometry to a moving component

Some objects are always attached to a moving component but have no API of their own: a camera mount bolted to an arm, a tool-changer plate, a cable bundle.
The motion planner should treat them as collision volume, but Viam has no component to talk to.

Use the `generic`/`fake` pattern, parented to the moving component instead of `world`:

1. Click the **+** icon and select **Configuration block**.
2. Search for `generic` and click the **generic/fake** result card. Click **Add component**.
3. Name the component descriptively (for example, `arm-camera-mount`) and click **Add component**.
4. Click **Frame** on the new component card. Set `parent` to the component the object attaches to (the arm's name for an end-effector mount, the gripper's name for a gripper attachment). Add a `geometry` field:

   ```json
   {
     "parent": "my-arm",
     "translation": { "x": 0, "y": 0, "z": 80 },
     "orientation": {
       "type": "ov_degrees",
       "value": { "x": 0, "y": 0, "z": 1, "th": 0 }
     },
     "geometry": {
       "type": "capsule",
       "r": 20,
       "l": 160
     }
   }
   ```

The motion planner treats the geometry as part of the parent's kinematic chain.
The fake component never runs; it exists only to hold the geometry.

`vmodutils:obstacle` has no advantage here (a single geometry, a moving parent frame, no validation payoff), so `generic`/`fake` is the right fit.

For objects the robot grasps and releases dynamically, see [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/) instead.

## Verify

1. Save the configuration.
2. Open the **3D SCENE** tab.
3. Orbit the scene. Each configured obstacle appears as a translucent shape at the position you configured. Each component shows up under the **World** panel; click a component to see its pose and geometry in the **Details** panel.
4. Check coverage against the physical workspace. If the arm can reach past an obstacle into the physical object, the geometry is too small.

For the full visualization and verification workflow, see [Set up obstacle avoidance](/motion-planning/3d-scene/set-up-obstacle-avoidance/).

## Try it

1. Add a table obstacle with `erh:vmodutils:obstacle` and verify it appears in the **3D SCENE** tab.
2. Move the arm near the table through **CONTROL** and confirm motion stops before contact. If it does not, the geometry is too small or mispositioned.
3. Add a back wall. Move the arm from one side of the table to the other and confirm the planner routes around the wall, not through it.

## Troubleshooting

{{< expand "Motion planner cannot find a path" >}}

- The obstacles may be too large or too close together, leaving no valid path. Reduce obstacle dimensions slightly.
- The destination may be inside or very close to an obstacle.
- The motion planner does not add clearance by default. If paths come too close to obstacles, increase obstacle dimensions or pass a larger `collision_buffer_mm` value through the `extra` map on the Move request.

{{< /expand >}}

{{< expand "Obstacles appear in the wrong position" >}}

- Verify the reference frame. Positions are relative to the specified parent frame's origin.
- Check units. Positions are in millimeters.
- For box geometries, remember the origin is the box's center, not a corner.
- Use the **3D SCENE** tab to see where obstacles appear.

{{< /expand >}}

{{< expand "Arm clips through obstacles" >}}

- The obstacle geometry may be too small. Add a 20 to 50 mm safety margin.
- The arm's own collision geometry may be missing. Check the arm's kinematics file for link geometry definitions.
- Make thin obstacles (walls, panels) at least 20 mm thick.

{{< /expand >}}

{{< expand "vmodutils module fails to start" >}}

`erh:vmodutils:obstacle` parses every geometry at startup and fails with a clear error if any are malformed. Common causes:

- A box with fewer than three dimensions (a box needs all three: `x`, `y`, `z`).
- A capsule with `l` less than twice `r` (capsule length must be at least twice the radius).
- A mistyped `type` value (valid values are `box`, `sphere`, `capsule`, `point`, `mesh`).

Fix the geometry in the component's attributes and save again.

{{< /expand >}}

## What's next

- [Plan collision-free paths](/motion-planning/obstacles/avoid-obstacles/): pass runtime obstacles through `WorldState` for objects that change between calls.
- [Set up obstacle avoidance](/motion-planning/3d-scene/set-up-obstacle-avoidance/): full verification workflow in the **3D SCENE** tab.
- [Attach and detach geometries](/motion-planning/obstacles/attach-detach-geometries/): attach a grasped object to the gripper frame for the duration of a pickup.
- [Allow specific frames to collide](/motion-planning/obstacles/allow-frame-collisions/): permit expected contact between frames.
