---
title: "Motion Service"
linkTitle: "Motion"
weight: 40
type: "docs"
description: "The motion service enables your machine to plan and move its components relative to itself, other machines, and the world."
tags: ["motion", "motion planning", "services"]
icon: true
images: ["/services/icons/motion.svg"]
no_list: true
aliases:
  - "/services/motion/"
  - "/mobility/motion/"
no_service: true
date: "2022-01-01"
# updated: ""  # When the content was last entirely checked
# SME: Motion team
---

The motion service enables your machine to plan and move itself or its components relative to itself, other machines, and the world.
The motion service:

1. Gathers the current positions of the machine’s components as defined with the [frame system](/operate/reference/services/frame-system/).
2. Plans the necessary motions to move a component to a given destination while obeying any [constraints you configure](constraints/).

The motion service can:

- use motion [planning algorithms](algorithms/) locally on your machine to plan coordinated motion across many components.
- pass movement requests through to individual components which have implemented their own motion planning.

## Configuration

You need to configure frames for your machine's components with the [frame system](/operate/reference/services/frame-system/).
This defines the spatial context within which the motion service operates.

The motion service itself is enabled on the machine by default, so you do not need to add any extra configuration to enable it.

## Access the motion service in your code

Use the motion service in your code by creating a motion service client and then calling its methods.
As with other resource clients, how you get the client depends on whether your code is part of a client application or a module:

{{< tabs >}}
{{% tab name="From a client application" %}}

To access a motion service, use its name from the machine configuration.
To access the motion service built into `viam-server` from your client application code, use the resource name `builtin` to get a motion service client:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Get a motion service client
motion_service = MotionClient.from_robot(machine, "builtin")

# Then use the motion service, for example:
moved = await motion_service.move(gripper_name, destination, world_state)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Get a motion service client
motionService, err := motion.FromRobot(machine, "builtin")
if err != nil {
  logger.Fatal(err)
}

// Then use the motion service, for example:
moved, err := motionService.Move(context.Background(), motion.MoveReq{
  ComponentName: gripperName,
  Destination: destination,
  WorldState: worldState
})
```

{{% /tab %}}
{{< /tabs >}}

{{% /tab %}}
{{% tab name="From within a module" %}}

To access a motion service, use its name from the machine configuration.
To access the motion service built into `viam-server` from your module code, you need to add the motion service as a [module dependency](/operate/modules/other-hardware/create-module/dependencies/), using the resource name `builtin`.
For example:

{{< tabs >}}
{{% tab name="Python" %}}

1. Edit your `validate_config` function to add the `builtin` motion service as a dependency so that it is available to your module.
   You do not need to check for it in your config because the built-in motion service is always enabled.

   ```python {class="line-numbers linkable-line-numbers"}
   @classmethod
   def validate_config(
       cls, config: ComponentConfig
   ) -> Tuple[Sequence[str], Sequence[str]]:
       req_deps = []
       req_deps.append("builtin")
       return req_deps, []
   ```

1. Edit your `reconfigure` function to add the motion service as an instance variable so that you can use it in your module:

   ```python {class="line-numbers linkable-line-numbers"}
   def reconfigure(
       self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
   ):
       motion_resource = dependencies[Motion.get_resource_name("builtin")]
       self.motion_service = cast(MotionClient, motion_resource)

       return super().reconfigure(config, dependencies)
   ```

1. You can now use the motion service in your module, for example:

   ```python {class="line-numbers linkable-line-numbers"}
   def move_around_in_some_way(self):
       moved = await self.motion_service.move(gripper_name, destination, world_state)
       return moved
   ```

{{% /tab %}}
{{% tab name="Go" %}}

The following example assumes your module uses `AlwaysRebuild` and does not have a `Reconfigure` function defined.

```go {class="line-numbers linkable-line-numbers"}
// Return the motion service as a dependency
func (cfg *Config) Validate(path string) ([]string, []string, error) {
  deps := []string{motion.Named("builtin").String()}
  return deps, nil, nil
}

// Then use the motion service, for example:
func (c *Component) MoveAroundInSomeWay() error {
  c.Motion, err = motion.FromDependencies(deps, "builtin")
  if err != nil {
    return nil, err
  }
  moved, err := c.Motion.Move(context.Background(), motion.MoveReq{
    ComponentName: gripperName,
    Destination: destination,
    WorldState: worldState
  })
  return moved, err
}
```

{{% /tab %}}
{{< /tabs >}}

If you created your own custom motion service, you can access it using the resource name you gave it in your machine's configuration.
You'll also need to check for it in your validate function, since it is not built into `viam-server`.

{{% /tab %}}
{{< /tabs >}}

## API

The [motion service API](/dev/reference/apis/services/motion/) supports the following methods:

{{< readfile "/static/include/services/apis/generated/motion-table.md" >}}

## Test the motion service

You can test motion on your machine from the [**CONTROL** tab](/manage/troubleshoot/teleoperate/default-interface/).

![Motion card on the Control tab](/services/motion/motion-rc-card.png)

Enter x and y coordinates to move your machine to, then click the **Move** button to issue a `MoveOnMap()` request.

{{< alert title="Info" color="info" >}}

The `plan_deviation_m` for `MoveOnMap()` on calls issued from the **CONTROL** tab is 0.5 m.

{{< /alert >}}

## Next steps

The following tutorials contain complete example code for interacting with a robot arm through the arm component API, and with the motion service API, respectively:

{{< cards >}}
{{% card link="/operate/mobility/move-arm/" %}}
{{% card link="/tutorials/services/plan-motion-with-arm-gripper" %}}
{{< /cards >}}
