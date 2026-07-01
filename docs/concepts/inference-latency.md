---
linkTitle: "Inference latency and loop rate"
title: "Inference latency and loop rate"
weight: 30
layout: "docs"
type: "docs"
description: "Understand why model inference latency sets the ceiling on how fast a perception or control loop can run, and estimate an achievable loop rate from model size, image resolution, and hardware."
---

Consider a small program that watches a camera and reacts to what it sees:

```python
while True:
    detections = await detector.get_detections_from_camera("my-camera")
    steer(detections)
    await asyncio.sleep(0.05)  # aim for 20 Hz
```

The `sleep(0.05)` looks like it sets the pace: run 20 times per second.
In practice the loop rate depends far more on the line above it.
The call to [`GetDetectionsFromCamera`](/vision/) captures a frame, runs it through a machine learning model, and returns the results.
That call is synchronous: it blocks until inference finishes.
If the model takes 200&nbsp;ms to produce detections, one trip through the loop takes at least 200&nbsp;ms, and the loop runs near 5 Hz no matter what number you pass to `sleep`.

This page explains why inference latency sets the ceiling on loop rate, and how to estimate that ceiling before you build a real-time task.

## Why each iteration waits for inference

A perception or control loop does its work one iteration at a time, in order.
Each iteration acquires an input, computes on it, and acts on the result.
When the compute step is a model inference call, the loop reaches that call and waits for a return value before it can act or start the next iteration.

The wall-clock time of one iteration is the sum of its blocking steps.
The single largest term is usually inference:

- Acquiring a frame from a camera: a few milliseconds to tens of milliseconds.
- Running inference on that frame: milliseconds to hundreds of milliseconds.
- Acting on the result (sending a command to a motor or base): typically a few milliseconds.

Your `sleep` only adds idle time on top of that sum.
It can slow the loop down, but it cannot speed it up past the inference call.
The achievable loop rate is therefore bounded by the slowest blocking step, roughly:

```text
max_loop_rate ≈ 1 / max(inference_time, actuation_time, frame_time)
```

In most vision loops the inference term dominates, so `max_loop_rate ≈ 1 / inference_time`.
A 200&nbsp;ms model caps the loop near 5 Hz; a 20&nbsp;ms model allows up to about 50 Hz, before you add any deliberate `sleep`.

## What determines inference time

Inference time is a property of three things together: the model, the input, and the hardware.

**Model size and architecture.**
A larger model with more parameters and layers performs more arithmetic per frame.
A compact detector aimed at edge devices runs much faster than a large, high-accuracy backbone.
Quantized formats such as TFLite `int8` trade a small amount of accuracy for a substantial speedup.

**Input resolution.**
Compute grows with the number of pixels, which grows with the square of the linear resolution.
Halving both image dimensions cuts pixel count to a quarter and often cuts inference time by a similar factor.
Feeding a model a smaller frame is one of the cheapest ways to raise loop rate.

**Hardware.**
Where inference runs matters more than any other single factor.
As rough orders of magnitude, for a typical object detector:

| Where inference runs                                             | Rough per-frame latency     | Rough loop ceiling |
| ---------------------------------------------------------------- | --------------------------- | ------------------ |
| TFLite on a Raspberry Pi CPU                                     | ~150-500&nbsp;ms            | ~2-6 Hz            |
| Same model on a coprocessor or small GPU (for example, a Jetson) | ~10-40&nbsp;ms              | ~25-100 Hz         |
| Larger model on a desktop or server GPU                          | single-digit to ~20&nbsp;ms | ~50-200 Hz         |

Treat these as illustrative ranges, not specifications.
Actual numbers depend on the exact model, resolution, framework, and device, and the only reliable figure is one you measure on your own hardware.
The pattern holds across cases: moving the same model from a general-purpose CPU to an accelerator built for tensor math changes latency by roughly an order of magnitude.

## Why remote inference adds latency

The ML model service's `Infer` method is the lower-level call that a [vision service](/vision/) detection ultimately blocks on, and you can run that model locally on the machine or call one hosted elsewhere.
Running inference on a remote or cloud server can give you access to hardware far more powerful than an edge device.
That power comes with an added cost: every frame travels to the server and every result travels back.

Remote inference latency is the sum of the network round trip and the server-side compute:

```text
remote_inference_time ≈ upload_time + server_inference_time + download_time
```

Uploading a full-resolution frame over a constrained or high-latency link can add tens to hundreds of milliseconds and can vary from frame to frame.
For a monitoring task that reports a status every few seconds, that overhead is comfortably absorbed.
For a control loop steering a moving base, a variable extra 100&nbsp;ms per iteration both lowers the loop rate and makes its timing less predictable.

## Sizing a real-time task

The tolerable loop rate follows from what the loop controls.

**Real-time control** acts on the physical world, where staleness compounds.
A base moving at 1 m/s travels 20 cm during a 200&nbsp;ms inference call, so at 5 Hz every decision is based on a frame already 20 cm out of date.
For steering, obstacle avoidance, or closed-loop reaction, you generally want inference well under the physical time constant of the system, and you want that latency to be steady rather than bursty.
Viam's feedback controllers expose their own cadence directly: a [sensor-controlled base](/components/base/sensor-controlled/) accepts a `control_frequency_hz` value (default 10 Hz), and its movement sensors must report at least that fast for the loop to hold rate.

**Monitoring and logging** consume detections rather than steering on them, so a loop running at 1 Hz, or slower, is often plenty.
Here you can favor a larger, more accurate model or a remote GPU and accept the higher per-frame latency, because no actuator is waiting on the result.

To size a task, work backward from the required rate.
Decide the loop rate the application needs, invert it to get the latency budget per iteration, subtract the frame-capture and actuation time, and choose a model, resolution, and hardware whose measured inference time fits what remains.
If nothing fits, you have three levers: shrink or quantize the model, lower the input resolution, or move inference to faster hardware.
Because these levers trade accuracy and cost against speed, measuring inference time on the target device is the step that turns an estimate into a design you can rely on.

## Next steps

- Learn how detection and classification calls work in the [vision service](/vision/).
- See how a feedback loop consumes sensor input at a fixed rate on a [sensor-controlled base](/components/base/sensor-controlled/).
- Explore the [components](/components/) that a perception or control loop reads from and acts on.
