---
title: "Get resource status with Status"
linkTitle: "Status"
weight: 68
type: "docs"
description: "Use the Status method in Go SDK to retrieve component or service status."
tags: ["sdk", "go"]
date: "2026-03-30"
# updated: ""  # When the content was last entirely checked
---

Use the `Status` method to retrieve status information from any component or service in your Go code.
`Status` is part of every [component](/dev/reference/apis/#component-apis) and [service API](/dev/reference/apis/#service-apis) in the Go SDK.

By default, `Status` returns an empty map.
If you are developing a module, you can implement custom status reporting by providing a `StatusFunc` in your resource implementation.

## Use Status in Go SDK code

Call `Status` on any component or service to retrieve its current status:

```go {class="line-numbers linkable-line-numbers"}
myArm, err := arm.FromProvider(machine, "my_arm")
if err != nil {
    logger.Error(err)
    return
}

// Get the status of the arm
status, err := myArm.Status(context.Background())
if err != nil {
    logger.Error(err)
    return
}

// Log the status
logger.Infof("Arm status: %v", status)
```

**Parameters:**

- `ctx` [(Context)](https://pkg.go.dev/context#Context): A Context carries a deadline, a cancellation signal, and other values across API boundaries.

**Returns:**

- [(map[string]interface{})](https://pkg.go.dev/builtin#string): A map containing status information specific to the resource. The contents depend on the resource's implementation.
- [(error)](https://pkg.go.dev/builtin#error): An error, if one occurred.

## Implement Status in your module

If you are developing a [module](/operate/modules/write-a-driver-module/), you can implement custom status reporting by defining a `StatusFunc`.
The status information you return depends on what is relevant for your resource.

For example, a motor module might report its current speed and direction:

```go {class="line-numbers linkable-line-numbers"}
func (m *MyMotor) Status(ctx context.Context) (map[string]interface{}, error) {
    return map[string]interface{}{
        "speed":     m.currentSpeed,
        "direction": m.currentDirection,
        "is_moving": m.isMoving,
    }, nil
}
```

A sensor module might report its last reading timestamp and connection state:

```go {class="line-numbers linkable-line-numbers"}
func (s *MySensor) Status(ctx context.Context) (map[string]interface{}, error) {
    return map[string]interface{}{
        "last_reading_time": s.lastReadingTime.Format(time.RFC3339),
        "connected":         s.isConnected,
        "error_count":       s.errorCount,
    }, nil
}
```

## Availability

The `Status` method is available in the Go SDK for all components and services.
It is not currently available in the Python, TypeScript, or Flutter SDKs.
