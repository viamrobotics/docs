---
linkTitle: "Capture frequency versus sample rate"
title: "Capture frequency versus sample rate"
weight: 40
layout: "docs"
type: "docs"
description: "Understand how the data-capture polling frequency differs from a sensor's internal sample rate, and how to choose a capture frequency that balances fidelity against storage cost."
---

Suppose you configure data capture on a temperature sensor with `capture_frequency_hz` set to `1`, and the sensor hardware samples its internal thermistor at 100&nbsp;Hz.
These two numbers describe different things, and the gap between them is where most surprises come from.
The sensor produces a fresh internal reading 100 times per second, but `viam-server` reads the sensor's API once per second and stores only that one value.
The other 99 readings in each second never reach the data pipeline.

Knowing which number governs your stored data helps you set a frequency that captures the events you care about without paying for data you do not need.

## Two independent rates

The **sample rate** is a property of the hardware.
It is how often the physical device measures the world and refreshes the value it exposes through its API.
A GPS module might update its position at 10&nbsp;Hz, an accelerometer might sample at 1&nbsp;kHz, and a slow environmental sensor might refresh once every few seconds.
You usually cannot change this rate from your machine configuration; it is fixed by the device or its driver.

The **capture frequency** is a property of your data-capture configuration.
The data manager service polls the component's API at the rate you set in `capture_frequency_hz` and writes each returned reading to disk for syncing to the cloud.
Setting `capture_frequency_hz` to `0.5` records one reading every two seconds; setting it to `5` records five readings per second.
This is a polling loop on top of the API, entirely separate from whatever the hardware is doing internally.

Because the two rates are independent, your capture frequency decides the resolution of your stored history, while the sample rate decides the freshest value available at the moment `viam-server` polls.

## Undersampling and aliasing

When the capture frequency is much lower than the rate at which the signal changes, you record a sparse set of snapshots.
Between snapshots, anything can happen and go unrecorded.
A tank-level sensor polled once per minute will miss a valve that opens and closes in ten seconds, even though the hardware measured the whole event at 100&nbsp;Hz.
The event was visible to the sensor and invisible to your dataset.

A subtler failure is aliasing.
When you sample a periodic signal slower than about twice its frequency, the recorded points trace out a false, lower-frequency pattern that was never really there.
A vibration that oscillates at 10&nbsp;Hz, captured at 9&nbsp;Hz, can appear in your data as a slow 1&nbsp;Hz drift.
The stored numbers look plausible and lead you to the wrong conclusion.
To represent a signal that oscillates at some frequency, capture at more than twice that frequency; to catch a transient event, capture often enough that at least one reading lands inside the event's shortest duration.

## The cost of a high frequency

Raising the capture frequency is not free.
Every stored reading consumes disk on the machine, bandwidth during sync, and storage and query cost in the cloud, and these scale linearly with frequency.
A sensor captured at 50&nbsp;Hz produces fifty times the rows of the same sensor at 1&nbsp;Hz, across every machine in a fleet, every hour of every day.
High frequencies can also strain the hardware: polling a device faster than it can comfortably serve readings degrades performance, which is why capture rates should stay within what the component can handle.

The choice is therefore a trade-off.
Too low, and you alias or miss events.
Too high, and you pay for redundant readings that all report the same slowly-changing value.

## Choosing a frequency from the event timescale

Let the shortest event you need to observe set the rate.
Start from the timescale of what you are monitoring, then capture two or more times faster than that:

- A room-temperature reading that drifts over minutes is well served by `0.017`&nbsp;Hz (once a minute) or even slower.
- A door-open sensor for a room that people enter every few seconds needs a reading every second or two to reliably catch each entry.
- A motor-current signal used to detect a stall that resolves in under a second needs several readings per second so that at least one lands during the stall.

Then weigh that against cost and event rate.
If events are rare but you still want to catch them, pair a modest steady capture frequency with [edge filtering](/data/filter-at-the-edge/) so that the machine stores readings only when something interesting happens, rather than polling fast around the clock.
This keeps fidelity high during events and storage low the rest of the time.

## Two clocks on every reading

Each captured reading carries two timestamps, which helps you reason about when a measurement actually happened versus when it landed in the cloud.
`time_requested` records when the machine's data manager polled the component, using the machine's own clock.
`time_received` records when the Viam cloud received and stored the reading.

The gap between them reflects buffering and sync latency, which can be seconds during normal operation or hours for a machine that syncs only when it regains connectivity.
Because `time_received` is indexed, it is the timestamp to use for time-range queries; `time_requested` is the one that tells you when the event occurred on the machine.
Keeping the two clocks distinct means intermittent connectivity never corrupts your sense of when data was actually captured.

## Next steps

To configure capture and choose a frequency for each method, see:

- [Capture data](/data/)
- [Filter at the edge](/data/filter-at-the-edge/)
