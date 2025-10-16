---
title: "Implement or use DoCommand"
linkTitle: "DoCommand"
weight: 67
type: "docs"
description: "Implement DoCommand in your module or use it from Viam's SDKs."
tags: ["sdk", "extend"]
date: "2025-04-29"
# updated: ""  # When the content was last entirely checked
---

The `DoCommand` method is a flexible wrapper that you can use to send commands that have no corresponding built-in API method.
`DoCommand` is part of every [component](/dev/reference/apis/#component-apis) and [service API](/dev/reference/apis/#service-apis), though most models do not implement it.

In the majority of cases, you should use a more specific method for your component or service.
As the developer of a resource, you can implement `DoCommand` in your module if you need to add custom commands to your resource.

As the user of a resource, you can only call `DoCommand` if it is implemented in the model you are using.
Refer to the model's documentation to see whether `DoCommand` is implemented and how to use it.

## Implement DoCommand in your component or service

`DoCommand` takes a map of key-value pairs as input.
The contents of the map are entirely up to the developer of the resource.

`DoCommand` also returns a map of key-value pairs, but many implementations return an empty map, or a map that confirms that the command was received.

There are many ways to implement `DoCommand` in your module, with the following example being just one.
See [More examples](#more-examples) for more.

### Example implementation

Imagine you have a robotic vacuum cleaner that has a docking sequence and can clean specific areas such as the kitchen and the living room.

You could [write a module](/operate/modules/other-hardware/create-module/) that implements the [base API](/dev/reference/apis/components/base/).
The base API includes methods like `MoveStraight` to drive the vacuum cleaner around, and like all resource APIs, it includes a `DoCommand` method.
In addition to the standard base methods, you could implement `DoCommand` to trigger the docking and cleaning sequences:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
async def do_command(
    self,
    command: Mapping[str, ValueTypes],
    *,
    timeout: Optional[float] = None,
    **kwargs
) -> Mapping[str, ValueTypes]:
    for name, value in command.items():
        if name == "action":
            action = value
            if action == "dock":
                await self.run_docking_sequence()
                return {"status": "docked"}
            elif isinstance(action, dict) and "clean_area" in action:
                area = action["clean_area"]
                if area in ["kitchen", "living_room"]:
                    await self.clean_area(area)
                    return {"status": f"cleaned {area}"}
                else:
                    raise ValueError(f"Unknown area: {area}")
            else:
                raise ValueError(f"Unknown action: {action}")
        else:
            raise ValueError(f"Unknown command: {command}")

# TODO: Implement run_docking_sequence()
# TODO: Implement clean_area()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func (s *Vacuum) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
  action, ok := cmd["action"]
  if !ok {
    return nil, fmt.Errorf("missing 'action' key in command")
  }

  switch action := action.(type) {
  case string:
    if action == "dock" {
      if err := s.runDockingSequence(ctx); err != nil {
        return nil, err
      }
      return map[string]interface{}{"status": "docked"}, nil
    }
  case map[string]interface{}:
    if cleanArea, ok := action["clean_area"].(string); ok {
      if cleanArea == "kitchen" || cleanArea == "living_room" {
        if err := s.cleanArea(ctx, cleanArea); err != nil {
          return nil, err
        }
        return map[string]interface{}{"status": fmt.Sprintf("cleaned %s", cleanArea)}, nil
      }
      return nil, fmt.Errorf("unknown area: %s", cleanArea)
    }
  }

  return nil, fmt.Errorf("unknown action: %v", action)
}

// TODO: Implement runDockingSequence()
// TODO: Implement cleanArea()
```

{{% /tab %}}
{{< /tabs >}}

## Use DoCommand in SDK code

Continuing with the vacuum cleaner example, you could use `DoCommand` in your control code as follows:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Dock the vacuum cleaner
await vacuum.do_command({"action": "dock"})

# Clean the kitchen
await vacuum.do_command({"action": {"clean_area": "kitchen"}})
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Dock the vacuum cleaner
_, err := vacuum.DoCommand(context.Background(), map[string]interface{}{
    "action": "dock"})
if err != nil {
  logger.Error(fmt.Errorf("failed to dock vacuum: %w", err))
}

// Clean the kitchen
_, err = vacuum.DoCommand(context.Background(), map[string]interface{}{
    "action": map[string]interface{}{"clean_area": "kitchen"},
})
if err != nil {
  logger.Error(fmt.Errorf("failed to clean area: %w", err))
}
```

{{% /tab %}}
{{< /tabs >}}

## Use DoCommand in the web UI

You can use `DoCommand` in the web UI:

1. Navigate to your machine's **CONTROL** tab.
1. Find your resource and expand the **DO COMMAND** section.
1. Enter a key and value in the text box using JSON syntax, for example

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "action": { "clean_area": "kitchen" }
   }
   ```

   {{<imgproc src="/components/generic/vacuum-control.png" resize="x1100" declaredimensions=true alt="DoCommand section of the vacuum generic resource's control panel, with clean_area set to kitchen." style="max-width:600px" class="shadow imgzoom" >}}

1. Click **Execute**.

## More examples

For an example that implements `DoCommand` in a generic API Python module, see [Add control logic to your module](/operate/modules/control-logic/#program-control-logic-in-module).

For additional examples, look at the GitHub repositories of [registry](https://app.viam.com/registry), especially modules that use the generic API.
Essentially all generic models implement `DoCommand` (since it is the only method of the generic API), and various other models implement it as well.

{{% hiddencontent %}}
`DoCommand` is styled as `do_command` in Python.
{{% /hiddencontent %}}
