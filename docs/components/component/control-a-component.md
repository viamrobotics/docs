---
title: "Control a Component"
linkTitle: "Control a Component"
weight: 12
type: "docs"
draft: false
description: "You can do something or other with your component."
tags: ["name", "components"]
draft: true

# SMEs:
---

The arm component supports the following methods:

| Method Name | Golang | Python | Description |
| ----------- | ------ | ------ | ----------- |
| [MethodName](#methodname)   | [MethodName][go_method_code]   | [method_name][python_method_code]   | Description    |
| [Method Name](#method-name)   | [MethodName][go_method_code]   | [method_name][python_method_code]   | Description    |
| [Method Name](#method-name)   | [MethodName][go_method_code]   | [method_name][python_method_code]   | Description    |

[go_method_code]: https://pkg.go.dev/go.viam.com/rdk/components/component#Arm
[python_method_code]: https://python.viam.dev/autoapi/viam/components/arm/index.html#viam.components.arm.Arm.get_end_position

### `MethodName`

{{< tabs >}}
{{% tab name="Python" %}}

```python
from viam.components.component import Component

robot = await connect()
component1 = Component.from_robot(robot, "component1")

# useful comment
await component1.method1(1)
await asyncio.sleep(3)
await component1.method2(1)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
import (
"time"
"go.viam.com/rdk/components/component"
)

robot, err := client.New()

c1, err := component.FromRobot(robot, "component1")

// useful comment
c1.Method1(context.Background(), 1, nil)
time.Sleep(3 * time.Second)
c1.Method2(context.Background(), 1, nil)
```

{{% /tab %}}
{{< /tabs >}}

## Troubleshooting

### Issue description

Resolution description

You can find additional assistance in the [Troubleshooting section](/appendix/troubleshooting/).

You can also ask questions on the [Viam Community Slack](https://join.slack.com/t/viamrobotics/shared_invite/zt-1f5xf1qk5-TECJc1MIY1MW0d6ZCg~Wnw) and we will be happy to help.

## Next Steps

<div class="container text-center">
  <div class="row">
    <div class="col" style="border: 1px solid #000; box-shadow: 5px 5px 0 0 #000; margin: 1em">
        <a href="install">
            <br>
            <h4 style="text-align: left; margin-left: 0px;">Relevant tutorial name</h4>
            <p style="text-align: left;">Description.</p>
        </a>
    </div>
  </div>
</div>
