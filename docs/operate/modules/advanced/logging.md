---
title: "Module logging"
linkTitle: "Module logging"
weight: 45
layout: "docs"
type: "docs"
description: "Use logging with modules"
---

From modules you can log messages at the [resource level](#resource-level-logging) or at the [machine level](#machine-level-logging).

## Resource-level logging

The following log severity levels are available for resource logs:

{{< tabs >}}
{{% tab name="Python" %}}

```python {class="line-numbers linkable-line-numbers"}
# Within some method, log information:
self.logger.debug("debug info")
self.logger.info("info")
self.logger.warn("warning info")
self.logger.error("error info")
self.logger.exception("error info", exc_info=True)
self.logger.critical("critical info")
```

{{% /tab %}}
{{% tab name="Go" %}}

```go {class="line-numbers linkable-line-numbers"}
fn (c *component) someFunction(ctx context.Context, a int) {
  // Log with severity info:
  c.logger.CInfof(ctx, "performing some function with a=%v", a)
  // Log with severity debug (using value wrapping):
  c.logger.CDebugw(ctx, "performing some function", "a" ,a)
  // Log with severity warn:
  c.logger.CWarnw(ctx, "encountered warning for component", "name", c.Name())
  // Log with severity error without a parameter:
  c.logger.CError(ctx, "encountered an error")
}
```

{{% /tab %}}
{{< /tabs >}}

Resource-level logs are recommended instead of global logs for modular resources, because they make it easier to determine which component or service an error is coming from.
Resource-level error logs appear in the <strong>ERROR LOGS</strong> section of each resource's configuration card in the app.

{{% alert title="Note" color="note" %}}
In order to see resource-level debug logs when using your modular resource, you'll either need to run `viam-server` with the `-debug` option or [configure your machine or individual resource to display debug logs](/operate/reference/viam-server/#logging).
{{% /alert %}}

## Machine-level logging

If you need to publish to the global machine-level logs instead of using the recommended resource-level logging, you can follow this example:

```python {class="line-numbers linkable-line-numbers" data-line="2,5"}
# In your import block, import the logging package:
from viam.logging import getLogger

# Before your first class or function, define the LOGGER variable:
LOGGER = getLogger(__name__)

# in some method, log information
LOGGER.debug("debug info")
LOGGER.info("info info")
LOGGER.warn("warn info")
LOGGER.error("error info")
LOGGER.exception("error info", exc_info=True)
LOGGER.critical("critical info")
```
