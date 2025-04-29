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

The `DoCommand` method is a generic wrapper that you can use to send commands that don't fit into any other method.
DoCommand is part of every resource API, though most models do not implement it.

In the majority of cases, you should use a more specific method for your component or service.

As the user of a resource, you can only call `DoCommand` if it is implemented in the model you are using.
Refer to the model's documentation (for example, the module README) to see whether `DoCommand` is implemented and how to use it.

As the developer of a resource, you can implement `DoCommand` in your module if you need to.

## Implement DoCommand in your component or service

`DoCommand` takes a map of key-value pairs as input.
The contents of the map are entirely up to the developer of the resource.

`DoCommand` also returns a map of key-value pairs, but many implementations return an empty map, or a map that confirms that the command was received.

There are many ways to implement `DoCommand` in your module, with the following example being just one.
See [More examples](#more-examples) for more.

### Example implementation

Imagine you have a vacuum cleaner resource that can run a docking sequence and clean a specific area such as the kitchen or the living room.
You could implement `DoCommand` to trigger the docking and cleaning sequences:

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
        if command.keys() == {"dock"}:
            await self.run_docking_sequence()
            return {"dock": True}
        if command.keys() == {"clean_area"}:
            area = command["clean_area"]
            if area in ["kitchen", "living_room"]:
                await self.clean_area(area)
            else:
                raise ValueError(f"Unknown area: {area}")
            return {"clean_area": area}
        return {"error": f"Unknown command: {command}"}

    # TODO: Implement run_docking_sequence()
    # TODO: Implement clean_area()
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
func (s *Vacuum) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
  if len(cmd) == 1 {
    if _, ok := cmd["dock"]; ok {
      if err := s.runDockingSequence(ctx); err != nil {
        return nil, err
      }
      return map[string]interface{}{"dock": true}, nil
    }
    if area, ok := cmd["clean_area"].(string); ok {
      if area == "kitchen" || area == "living_room" {
        if err := s.cleanArea(ctx, area); err != nil {
          return nil, err
        }
        return map[string]interface{}{"clean_area": area}, nil
      }
      return nil, fmt.Errorf("unknown area: %s", area)
    }
  }
  return map[string]interface{}{"error": fmt.Sprintf("unknown command: %v", cmd)}, nil
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
# Since the docking DoCommand implementation uses the key but not a value,
# you can use either of the following:
await vacuum.do_command({"dock": True})
# OR
await vacuum.do_command({"dock": ""})

# The cleaning DoCommand implementation uses the key and a value,
# so you must use the following:
await vacuum.do_command({"clean_area": "kitchen"})
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
// Since the docking DoCommand implementation uses the key but not a value,
// you can use either of the following:
_, err := vacuum.DoCommand(context.Background(), map[string]interface{}{"dock": true})
if err != nil {
  logger.Error(fmt.Errorf("failed to dock vacuum: %w", err))
}
// OR
_, err = vacuum.DoCommand(context.Background(), map[string]interface{}{"dock": ""})
if err != nil {
  logger.Error(fmt.Errorf("failed to dock vacuum: %w", err))
}

// The cleaning DoCommand implementation uses the key and a value,
// so you must use the following:
_, err = vacuum.DoCommand(context.Background(), map[string]interface{}{"clean_area": "kitchen"})
if err != nil {
  logger.Error(fmt.Errorf("failed to clean area: %w", err))
}
```

{{% /tab %}}
{{< /tabs >}}

## Use DoCommand from the Viam app

You can use `DoCommand` from the Viam app:

1. Navigate to your machine's **CONTROL** tab.
1. Find your resource and expand the **DO COMMAND** section.
1. Enter a key and value in the text box using JSON syntax, for example

   ```json {class="line-numbers linkable-line-numbers"}
   {
     "clean_area": "kitchen"
   }
   ```

   {{<imgproc src="/components/generic/vacuum-control.png" resize="x1100" declaredimensions=true alt="DoCommand section of the vacuum generic resource's control panel, with clean_area set to kitchen." style="max-width:600px" class="shadow imgzoom" >}}

1. Click **Execute**.

## More examples

For an example of how to implement `DoCommand` in a Python module, as well as how to use it from SDKs and the Viam app, see [Add control logic to your module](/manage/software/control-logic/#add-control-logic-to-your-module).

For additional examples, look at the GitHub repositories of [modules in the registry](https://app.viam.com/registry), especially modules that use the generic API.
Essentially all generic models implement `DoCommand` (since it is the only method of the generic API), and various other models implement it as well.
