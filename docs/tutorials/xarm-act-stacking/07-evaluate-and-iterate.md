---
title: "Phase 7: Evaluate and iterate"
linkTitle: "7. Evaluate and iterate"
type: "docs"
slug: "evaluate-and-iterate"
weight: 70
description: "Optional: measure your policy, find where it fails, record targeted demonstrations, retrain, and compare."
workshop: "xarm-act-stacking"
toc_hide: true
phase: 7
phase_total: 7
time_estimate: "90 minutes plus a retraining job"
prev: "/tutorials/xarm-act-stacking/deploy-the-policy/"
next: "/tutorials/xarm-act-stacking/wrap-up/"
languages: ["python"]
capabilities: ["ml-training", "sequences", "datasets", "docs"]
diataxis: tutorial
draft: true
---

This phase is optional. The previous phase already gave you a working policy: the xArm stacks a block with no human input. This phase makes it measurably better. You measure where it fails, record demonstrations aimed at those failures, retrain, and compare. It's also the jumping-off point for hackathon teams, who can take this loop and run it on their own tasks.

## Measure

You can't improve what you haven't counted. Run 10 trials, two in each zone of the mat. Reset the blocks before every trial, and start each one the way you did in [Phase 6](/tutorials/xarm-act-stacking/deploy-the-policy/). Copy this table and fill it in as you go:

<!-- TODO(dep): zone count on the printables/ mat -->

```markdown
| Trial | Zone | Result       | Failure type |
| ----- | ---- | ------------ | ------------ |
| 1     | A    | success/fail |              |
| 2     | A    | success/fail |              |
| 3     | B    | success/fail |              |
| 4     | B    | success/fail |              |
| 5     | C    | success/fail |              |
| 6     | C    | success/fail |              |
| 7     | D    | success/fail |              |
| 8     | D    | success/fail |              |
| 9     | E    | success/fail |              |
| 10    | E    | success/fail |              |
```

If your mat has a different number of zones, spread the 10 trials across them evenly. Call a trial a success only if the red block rests on the blue block when the arm stops. For each failure, record one failure type:

- **Missed grasp:** the gripper closed without the block.
- **Dropped:** the arm grasped the block, then lost it on the way.
- **Misaligned stack:** the red block landed on the blue block but fell off or sits crooked.
- **Froze:** the arm stopped moving partway through the task.

Your success rate is the number of successes divided by 10. Write it down. This is your baseline for model version 1.

## Find the pattern

Sort your failures by zone and by type.

- **Failures that cluster in one zone** point to missing coverage. The policy hasn't seen enough starts like that one.
- **Failures at the grasp** (missed grasps, drops) point to precision. Add demonstrations with slower, more deliberate grasps.
- **Froze** may be the gripper latency described in the [Phase 6 troubleshooting table](/tutorials/xarm-act-stacking/deploy-the-policy/#troubleshooting). If the arm pauses for seconds at each gripper change, more data won't fix it.

## Record targeted demonstrations

Record 15 to 20 more episodes aimed at your failure cases. For example, if zone D failed twice, record several episodes that start in zone D. Use the same task, `stack the red block on the blue block`, and leave **FPS** at 10, so the new episodes match the old ones. Training rejects sequences with mixed rates.

Follow [Phase 3](/tutorials/xarm-act-stacking/record-demonstrations/) to record, and review the new episodes the way you did in [Phase 4](/tutorials/xarm-act-stacking/review-and-build-a-dataset/#review-in-the-webapp): tag each one `review:keep` or discard it.

## Version the dataset

Create a new dataset named `xarm-stacking-v2`. It holds all the kept episodes from v1 plus the new keepers. Don't overwrite or edit `xarm-stacking-v1`. Keeping v1 intact means you can still reproduce model version 1, and the comparison stays honest.

Use the script from [Phase 4](/tutorials/xarm-act-stacking/review-and-build-a-dataset/#create-the-sequence-dataset). Change the dataset name from `xarm-stacking-v1` to `xarm-stacking-v2`, or create it in the Viam app the same way. The script keeps every sequence tagged `review:keep`, which now includes your new episodes.

## Retrain

Submit the same training job as [Phase 5](/tutorials/xarm-act-stacking/train-a-policy/), with two changes: select `xarm-stacking-v2` (or pass its dataset ID with the CLI) and give the model a new version, for example `2` (`--model-version=2` with the CLI). Keep every other argument the same, so the dataset is the only variable. Every `--model-version` must be new.

## Compare

When the job finishes, point the policy at the new model.

1. In your machine's JSON config, change the `version` of the `xarm-stacking` package to `2`, as in [Phase 6](/tutorials/xarm-act-stacking/deploy-the-policy/#add-the-policy).
2. Save, and wait until `act-policy` reports `"state": "ready"` from `status`.
3. Run the same 10 trials, in the same zones, with the same block starts.
4. Fill in a second copy of the table and compute the success rate.

{{< checkpoint >}}
You have a success rate for model version 1 and one for model version 2, from the same 10 trials.
{{< /checkpoint >}}

Ten trials is a small sample. A difference of one trial can be noise. Look at which failure types went away, not only the total.

## Other knobs

If more demonstrations don't help, or you want to tune something else, these are the settings to try.

- **`actions_per_chunk`:** Change it when the arm stalls between chunks (`starved_ticks` rising) or acts on stale information. It's a controller setting, so it needs no retraining. See [Why `actions_per_chunk` matters](/tutorials/xarm-act-stacking/deploy-the-policy/#why-actions_per_chunk-matters).
- **Training `steps`:** Raise it when the loss curve is still falling at the end of the job, which means the model is underfit.

  <!-- TODO(dep): default steps from the companion training/ README -->

- **`image_size`:** Lowering it can shorten training time, at the cost of image detail. Raise it only if fine details such as the block edges matter.

  <!-- TODO(dep): default image_size from the companion training/ README -->

- **More demonstrations or more steps:** When failures cluster by situation, more demonstrations usually beat more steps. More steps on the same data can't teach the policy situations it never saw.

{{< workshop-nav >}}
