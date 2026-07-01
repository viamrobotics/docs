---
linkTitle: "Confidence scores"
title: "What a confidence score is (and isn't)"
weight: 20
layout: "docs"
type: "docs"
description: "What the confidence value on a detection or classification measures, why it is not a calibrated probability, and how to reason about accept and reject thresholds for a quality-control task."
---

Point a person detector at an image and it returns something like `person: 0.82`. That `0.82` is a confidence score: a number between `0.0` and `1.0` that rides along with every result from [`GetDetections`](/reference/apis/services/vision/#getdetections) and [`GetClassifications`](/reference/apis/services/vision/#getclassifications). It is one of the most useful signals the vision service gives you, and one of the easiest to misread. This page explains what the number measures, how far you can trust it, and how to turn it into an accept or reject decision.

## What the score measures

A confidence score is a value the model produces alongside a label to express how strongly the input matched what that label looks like. Within a single model, it works as an ordering signal: a detection at `0.90` matched the learned pattern for its label more strongly than one at `0.55`. Sort a batch of results by confidence and the ones most likely to be correct tend toward the top. That ranking is exactly what makes the score worth acting on.

The score is a raw model output, not a measured frequency. The model is not counting how often it has been right at `0.82` in the past; it is emitting a number that its training happened to settle on for inputs like this one. The value is meaningful, but it describes the strength of a match, not a track record.

## Why it is not a calibrated probability

It is tempting to read `person: 0.82` as "82 out of 100 detections like this one are correct." That reading assumes the score is _calibrated_: that across every detection scoring `0.80`, about 80% really are the labeled object. A calibrated probability makes that promise. A raw confidence score does not.

In practice, model scores skew. A model may report `0.95` on inputs that are correct only 70% of the time, or cluster everything between `0.40` and `0.60` even when it is usually right. The number still ranks results usefully within that one model, but its magnitude carries no guaranteed hit rate. Treat `0.82` as "high for this model," not as a 82% chance of being correct.

Three comparisons that feel natural also break down:

- **Across classes.** A `0.70` on `person` and a `0.70` on `forklift` from the same model can reflect very different real-world reliability. Each label has its own score distribution, so the two numbers are not interchangeable even inside one model.
- **Across models.** A `0.80` from one model says nothing about a `0.80` from another. They were trained differently and their scores land on different scales.
- **Across versions.** Retraining or re-exporting the same model can shift the whole score distribution. A threshold that fit last month's version can behave differently after an update.

Heuristic detectors expose a confidence value too, and it can mean even less. The [`color_detector`](/reference/services/vision/color_detector/) assigns every region it returns a constant confidence of `1.0`: the score reports that a color-matched region was found, and carries no information for ranking one detection above another. It is the clearest reminder that a confidence field is only ever as meaningful as the model behind it. Whatever produces the number, the discipline is the same: understand what it measures before you rank or threshold on it, and never read it as odds.

## Choosing a threshold for a quality-control task

Because the score orders results well within one model, the practical move is to pick a cutoff and act on everything above it. On the [ML model vision service](/reference/services/vision/mlmodel/), that cutoff lives in configuration as [`default_minimum_confidence`](/reference/services/vision/mlmodel/), which filters out every result below the value you set, and [`label_confidences`](/reference/services/vision/mlmodel/), which sets a separate cutoff per label. Per-label cutoffs exist precisely because scores are not comparable across classes: each label earns its own threshold.

Consider a station that inspects parts for a defect. A detector returns `defect: <score>` and you reject the part when that score is at or above a threshold `T`. Where you put `T` decides which of two mistakes you make more often:

- A **false accept** ships a defective part. The threshold was high enough that a real defect scored below it and passed.
- A **false reject** scraps a good part. The threshold was low enough that a clean part scored above it and got pulled.

The two errors trade against each other, and the score distribution is what you are sliding along:

- **Lower `T`** flags more parts as defective. Fewer defects slip through (fewer false accepts) at the cost of scrapping more good parts (more good parts scrapped).
- **Raise `T`** and the reverse holds: less good product wasted, but more defects escape.

There is no single correct `T`; there is the `T` that fits the cost of each error. If a shipped defect triggers a recall or a safety incident and a scrapped part costs a few cents of material, the defect is far more expensive, so favor a lower threshold and accept a higher false-reject rate. If scrap is costly and an escaped defect is caught cheaply downstream, a higher threshold makes sense. Ground the choice in those costs rather than in the number looking "high enough." To set `T` well, run the model over a labeled sample, look at where correct and incorrect results actually fall on the score scale, and choose the cutoff that puts the errors where they hurt least. Then revisit it whenever you retrain or re-export, because the distribution can move underneath you.

## Next steps

- [Detect objects](/vision/object-detection/detect/), work with detections and their confidence scores.
- [Classify images](/vision/classify/), work with classifications and their confidence scores.
- [Tune a detector](/vision/object-detection/tune/), adjust `default_minimum_confidence` and `label_confidences` in practice.
