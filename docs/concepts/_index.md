---
linkTitle: "Concepts"
title: "Core concepts"
weight: 3
layout: "docs"
type: "docs"
no_list: true
description: "Cross-cutting ideas the rest of the docs assume: the platform model, confidence scores, inference latency, and data sampling."
---

Some ideas show up across the whole product. A vision page, a data page, and
a fleet page all lean on them, but none of those pages is the right place to
define them. This section is that place. Read a page here once, and the rest
of the docs read more clearly.

- [How Viam fits together](platform-model/): machines, parts, components,
  services, and modules, the vocabulary every other section uses.
- [What a confidence score is (and isn't)](confidence-scores/): why a `0.9`
  is not a 90% probability, and how to pick a threshold.
- [Inference latency and loop rate](inference-latency/): why a perception or
  control loop cannot run faster than the model behind it.
- [Capture frequency versus sample rate](capture-frequency/): the difference
  between how often you record and how fast a sensor measures.
