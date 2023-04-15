---
title: "Control a Component"
linkTitle: "Control a Component"
weight: 12
type: "docs"
description: "You can do something or other with your component."
tags: ["name", "components"]
draft: true
# SMEs:
---

The arm component supports the following methods:

| Method Name | Description |
| ----------- | ----------- |
| [MethodName](#methodname)    | Description    |
| [Method Name](#methodname)   | Description    |
| [Method Name](#methodname)   | Description    |

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

{{< snippet "social.md" >}}
